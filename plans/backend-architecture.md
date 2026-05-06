# Backend Architecture — Business Registration Service

## Overview

The registration backend handles user data collection, state-specific filing orchestration, payment processing, and comprehensive analytics. Designed to maximize data capture for feedback and product improvement.

---

## 1. High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                          FRONTEND (Next.js / Vercel)                 │
│                                                                      │
│  Registration Wizard ──▶ Auto-save drafts ──▶ Submit filing         │
└──────────────────┬───────────────────────────────────┬───────────────┘
                   │ REST API                          │ WebSocket
                   ▼                                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│                          API LAYER (FastAPI)                         │
│                                                                      │
│  ┌─────────────┐ ┌─────────────┐ ┌──────────────┐ ┌──────────────┐ │
│  │ Registration │ │ Name Check  │ │ Payment      │ │ Analytics    │ │
│  │ Router       │ │ Router      │ │ Router       │ │ Router       │ │
│  └──────┬──────┘ └──────┬──────┘ └──────┬───────┘ └──────┬───────┘ │
│         │               │               │                │          │
│  ┌──────┴──────┐ ┌──────┴──────┐ ┌──────┴───────┐ ┌─────┴────────┐ │
│  │ Registration │ │ Name Check  │ │ Stripe       │ │ Event        │ │
│  │ Service      │ │ Service     │ │ Service      │ │ Collector    │ │
│  └─────────────┘ └─────────────┘ └──────────────┘ └──────────────┘ │
└──────────────────────────┬───────────────────────────────────────────┘
                           │
              ┌────────────┼────────────────┐
              ▼            ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  PostgreSQL  │  │  Redis       │  │  S3          │
│  (RDS)       │  │ (ElastiCache)│  │ (Documents)  │
│              │  │              │  │              │
│  • Filings   │  │  • Job queue │  │  • Filed docs│
│  • Users     │  │  • Sessions  │  │  • Receipts  │
│  • Drafts    │  │  • Rate limit│  │  • Screenshots│
│  • Events    │  │  • Cache     │  │  • Exports   │
└──────────────┘  └──────┬───────┘  └──────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────────────┐
│                     WORKER LAYER (Celery)                            │
│                                                                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │
│  │ Filing Workers   │  │ Notification    │  │ Analytics       │     │
│  │                  │  │ Workers         │  │ Workers         │     │
│  │ • PA automation  │  │                 │  │                 │     │
│  │ • MA manual queue│  │ • Email         │  │ • Event agg.   │     │
│  │ • Status polling │  │ • In-app alerts │  │ • Funnel calc. │     │
│  │ • Doc generation │  │ • SMS (future)  │  │ • Report gen.  │     │
│  └────────┬────────┘  └─────────────────┘  └─────────────────┘     │
│           │                                                          │
│           ▼                                                          │
│  ┌─────────────────────────────────────────────┐                    │
│  │  Filing Agents (per state)                   │                    │
│  │                                              │                    │
│  │  ┌──────────────┐    ┌──────────────┐       │                    │
│  │  │ PA Agent     │    │ MA Agent     │       │                    │
│  │  │ (Playwright  │    │ (Isolated VM │       │                    │
│  │  │  on AWS)     │    │  via tunnel) │       │                    │
│  │  └──────────────┘    └──────────────┘       │                    │
│  └─────────────────────────────────────────────┘                    │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 2. Data Models

### 2.1 Core Models

```python
class RegistrationDraft(Base):
    """Auto-saved form state — every field change persisted."""
    __tablename__ = "registration_drafts"

    id = Column(UUID, primary_key=True, default=uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    state = Column(String(2), nullable=False)  # "MA" or "PA"
    entity_type = Column(String(20), nullable=False)  # "llc" or "sole_prop"
    form_data = Column(JSONB, nullable=False, default={})
    current_step = Column(Integer, default=1)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)
    abandoned_at = Column(DateTime, nullable=True)


class Filing(Base):
    """Submitted filing — the source of truth after payment."""
    __tablename__ = "filings"

    id = Column(UUID, primary_key=True, default=uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    draft_id = Column(UUID, ForeignKey("registration_drafts.id"))
    state = Column(String(2), nullable=False)
    entity_type = Column(String(20), nullable=False)

    # Business info
    business_name = Column(String(255), nullable=False)
    alternate_names = Column(ARRAY(String), default=[])
    business_description = Column(Text)
    industry = Column(String(100))

    # Entity-specific (JSONB for flexibility across states/types)
    entity_details = Column(JSONB, nullable=False)
    # LLC: {management_type, members[], organizer, effective_date}
    # Sole prop: {owner_name, owner_address, business_address, start_date}

    # Registered agent
    agent_type = Column(String(20))  # "umd_service" or "own_agent"
    agent_details = Column(JSONB)

    # Filing status
    status = Column(String(20), default="pending_payment")
    # pending_payment -> paid -> queued -> submitted -> processing
    # -> approved -> rejected -> needs_amendment
    confirmation_number = Column(String(100), nullable=True)
    state_filing_number = Column(String(100), nullable=True)
    rejection_reason = Column(Text, nullable=True)

    # Payment
    stripe_payment_intent_id = Column(String(255), nullable=True)
    amount_charged = Column(Integer)  # cents
    state_fee = Column(Integer)  # cents
    service_fee = Column(Integer)  # cents

    # Timestamps
    created_at = Column(DateTime, default=utcnow)
    paid_at = Column(DateTime, nullable=True)
    submitted_at = Column(DateTime, nullable=True)
    approved_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    # Documents
    documents = relationship("FilingDocument", back_populates="filing")
    events = relationship("FilingEvent", back_populates="filing")


class FilingDocument(Base):
    """Documents generated or received during filing."""
    __tablename__ = "filing_documents"

    id = Column(UUID, primary_key=True, default=uuid4)
    filing_id = Column(UUID, ForeignKey("filings.id"), nullable=False)
    doc_type = Column(String(50))
    # "certificate_of_org", "operating_agreement", "receipt",
    # "screenshot", "rejection_letter", "amendment"
    s3_key = Column(String(500), nullable=False)
    filename = Column(String(255))
    created_at = Column(DateTime, default=utcnow)


class FilingEvent(Base):
    """Audit log for every state change and action on a filing."""
    __tablename__ = "filing_events"

    id = Column(UUID, primary_key=True, default=uuid4)
    filing_id = Column(UUID, ForeignKey("filings.id"), nullable=False)
    event_type = Column(String(50), nullable=False)
    # "created", "paid", "queued", "submitted", "status_checked",
    # "approved", "rejected", "amendment_filed", "document_uploaded"
    details = Column(JSONB, default={})
    created_at = Column(DateTime, default=utcnow)
    created_by = Column(String(50))  # "system", "user", "admin", "worker"
```

### 2.2 Analytics Models

```python
class AnalyticsEvent(Base):
    """Every frontend interaction during registration flow."""
    __tablename__ = "analytics_events"

    id = Column(UUID, primary_key=True, default=uuid4)
    user_id = Column(UUID, nullable=True)  # nullable for anonymous
    session_id = Column(String(100), nullable=False)
    event_name = Column(String(100), nullable=False, index=True)
    event_data = Column(JSONB, default={})
    page = Column(String(200))
    referrer = Column(String(500))
    user_agent = Column(String(500))
    ip_hash = Column(String(64))  # hashed, not raw IP
    created_at = Column(DateTime, default=utcnow, index=True)

    __table_args__ = (
        Index("ix_analytics_user_event", "user_id", "event_name"),
        Index("ix_analytics_session", "session_id"),
    )


class FormInteraction(Base):
    """Field-level interaction tracking for UX optimization."""
    __tablename__ = "form_interactions"

    id = Column(UUID, primary_key=True, default=uuid4)
    user_id = Column(UUID, nullable=True)
    session_id = Column(String(100), nullable=False)
    draft_id = Column(UUID, ForeignKey("registration_drafts.id"), nullable=True)
    step = Column(Integer, nullable=False)
    field_name = Column(String(100), nullable=False)
    interaction_type = Column(String(20), nullable=False)
    # "focus", "blur", "change", "error", "clear"
    duration_ms = Column(Integer, nullable=True)  # time spent on field
    error_message = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=utcnow)


class FunnelSnapshot(Base):
    """Daily aggregated funnel metrics — pre-computed for dashboards."""
    __tablename__ = "funnel_snapshots"

    id = Column(UUID, primary_key=True, default=uuid4)
    date = Column(Date, nullable=False)
    state = Column(String(2), nullable=True)  # null = all states
    entity_type = Column(String(20), nullable=True)  # null = all types

    visitors = Column(Integer, default=0)
    started_registration = Column(Integer, default=0)
    completed_step_1 = Column(Integer, default=0)
    completed_step_2 = Column(Integer, default=0)
    completed_step_3 = Column(Integer, default=0)
    completed_step_4 = Column(Integer, default=0)
    reached_review = Column(Integer, default=0)
    initiated_payment = Column(Integer, default=0)
    completed_payment = Column(Integer, default=0)
    filing_submitted = Column(Integer, default=0)
    filing_approved = Column(Integer, default=0)

    avg_time_to_complete_ms = Column(Integer, nullable=True)
    avg_name_search_attempts = Column(Float, nullable=True)

    __table_args__ = (
        UniqueConstraint("date", "state", "entity_type"),
    )


class UserFeedback(Base):
    """Explicit user feedback collected at key moments."""
    __tablename__ = "user_feedback"

    id = Column(UUID, primary_key=True, default=uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    filing_id = Column(UUID, ForeignKey("filings.id"), nullable=True)
    trigger_point = Column(String(50), nullable=False)
    # "post_filing", "post_approval", "abandonment", "support_ticket"
    nps_score = Column(Integer, nullable=True)  # 0-10
    rating = Column(Integer, nullable=True)  # 1-5 stars
    comment = Column(Text, nullable=True)
    tags = Column(ARRAY(String), default=[])
    created_at = Column(DateTime, default=utcnow)
```

---

## 3. API Endpoints

### 3.1 Registration Flow

```
POST   /api/v1/registration/drafts              Create new draft
PATCH  /api/v1/registration/drafts/{id}          Auto-save draft update
GET    /api/v1/registration/drafts/{id}          Resume draft
DELETE /api/v1/registration/drafts/{id}          Abandon draft

POST   /api/v1/registration/filings              Submit filing (from draft)
GET    /api/v1/registration/filings/{id}         Get filing details + status
GET    /api/v1/registration/filings              List user's filings

GET    /api/v1/registration/name-check           Check name availability
         ?state=PA&name=Acme+Solutions+LLC
```

### 3.2 Payment

```
POST   /api/v1/payments/create-intent            Create Stripe PaymentIntent
POST   /api/v1/payments/confirm                  Confirm payment & queue filing
GET    /api/v1/payments/{filing_id}/receipt       Get payment receipt
POST   /api/v1/webhooks/stripe                   Stripe webhook handler
```

### 3.3 Analytics (Internal / Admin)

```
POST   /api/v1/analytics/events                  Batch event ingestion
POST   /api/v1/analytics/form-interactions        Batch form interaction ingestion

GET    /api/v1/admin/analytics/funnel             Funnel report (date range, filters)
GET    /api/v1/admin/analytics/drop-offs          Drop-off analysis
GET    /api/v1/admin/analytics/field-friction      Field-level friction report
GET    /api/v1/admin/analytics/name-searches      Name search analytics
GET    /api/v1/admin/filings                      Admin filing management
```

### 3.4 Feedback

```
POST   /api/v1/feedback                          Submit user feedback
GET    /api/v1/admin/feedback                     Admin feedback dashboard
GET    /api/v1/admin/feedback/summary             Aggregated NPS/ratings
```

---

## 4. Event Collection Pipeline

### 4.1 Frontend Event Collection

```typescript
// Lightweight event collector — batches and sends every 5 seconds
// or on page unload (via sendBeacon)

class EventCollector {
  private queue: AnalyticsEvent[] = [];
  private flushInterval = 5000;

  track(name: string, data: Record<string, unknown>) {
    this.queue.push({
      event_name: name,
      event_data: data,
      page: window.location.pathname,
      timestamp: Date.now(),
      session_id: this.sessionId,
    });
  }

  // Auto-flush every 5s
  private async flush() {
    if (this.queue.length === 0) return;
    const batch = this.queue.splice(0);
    await fetch("/api/v1/analytics/events", {
      method: "POST",
      body: JSON.stringify({ events: batch }),
    });
  }

  // Flush on page unload via sendBeacon
  private onUnload() {
    if (this.queue.length === 0) return;
    navigator.sendBeacon(
      "/api/v1/analytics/events",
      JSON.stringify({ events: this.queue })
    );
  }
}
```

### 4.2 Backend Event Processing

```
Frontend ──▶ POST /analytics/events ──▶ Redis Queue ──▶ Analytics Worker
                                                              │
                                                    ┌─────────┴─────────┐
                                                    ▼                   ▼
                                            analytics_events     funnel_snapshots
                                            (raw events)         (daily aggregates)
```

Events are written to Redis first (fast, non-blocking to the user), then Celery workers batch-insert into PostgreSQL. Funnel snapshots are computed nightly by a scheduled task.

### 4.3 Events to Capture

#### Registration Flow Events

| Event | Payload | Why It Matters |
|-------|---------|----------------|
| `registration.started` | state, entity_type, source | Top of funnel |
| `registration.state_changed` | from_state, to_state | State switching behavior |
| `registration.entity_changed` | from_type, to_type | Entity confusion |
| `registration.step_entered` | step, time_since_start | Funnel progression |
| `registration.step_completed` | step, time_on_step, fields_modified | Completion rates |
| `registration.step_abandoned` | step, last_field, time_on_step | Drop-off diagnosis |
| `registration.draft_resumed` | draft_age_hours, step | Return visitors |
| `registration.submitted` | state, entity_type, total_time | Conversions |

#### Name Search Events

| Event | Payload | Why It Matters |
|-------|---------|----------------|
| `name.searched` | query_length, state | Search volume |
| `name.available` | state, attempt_number | Success rate |
| `name.unavailable` | state, attempt_number, similar_count | Frustration signal |
| `name.selected` | was_primary, attempt_number | Resolution |

#### Form Interaction Events

| Event | Payload | Why It Matters |
|-------|---------|----------------|
| `field.focused` | field_name, step | Entry point tracking |
| `field.blurred` | field_name, duration_ms, had_value | Time-per-field |
| `field.error` | field_name, error_type | Validation friction |
| `field.ai_assist_used` | field_name, feature | AI feature adoption |
| `field.help_viewed` | field_name, tooltip_or_modal | Confusion signals |

#### Payment Events

| Event | Payload | Why It Matters |
|-------|---------|----------------|
| `payment.initiated` | amount, method | Payment funnel |
| `payment.completed` | amount, method, processing_time_ms | Revenue |
| `payment.failed` | error_code, method | Payment friction |
| `payment.abandoned` | time_on_page | Cart abandonment |

#### Post-Filing Events

| Event | Payload | Why It Matters |
|-------|---------|----------------|
| `status.checked` | filing_id, times_checked, hours_since_submit | User anxiety |
| `checklist.item_clicked` | item_name, filing_status | Post-filing engagement |
| `feedback.submitted` | trigger, nps_score, has_comment | Satisfaction |

---

## 5. Filing Worker Architecture

### 5.1 Filing State Machine

```
                    ┌──────────────┐
                    │ pending_     │
         ┌─────────│ payment      │
         │         └──────┬───────┘
         │                │ payment confirmed
         │                ▼
         │         ┌──────────────┐
         │         │ paid         │
         │         └──────┬───────┘
         │                │ queued for filing
         │                ▼
         │         ┌──────────────┐
         │         │ queued       │
         │         └──────┬───────┘
         │                │ worker picks up
         │                ▼
         │         ┌──────────────┐
         │    ┌────│ submitting   │────┐
         │    │    └──────────────┘    │
         │    │ success               │ failure
         │    ▼                       ▼
         │  ┌──────────────┐  ┌──────────────┐
         │  │ submitted    │  │ failed       │──── retry (3x)
         │  └──────┬───────┘  └──────────────┘
         │         │ state processes
         │         ▼
         │  ┌──────────────┐
         │  │ processing   │
         │  └──────┬───────┘
         │         │
         │    ┌────┴────┐
         │    ▼         ▼
         │  ┌────────┐ ┌──────────┐
         │  │approved│ │ rejected │
         │  └────────┘ └────┬─────┘
         │                  │ user fixes
         │                  ▼
  refund │           ┌─────────────┐
    ◄────┘           │ needs_      │
                     │ amendment   │
                     └─────────────┘
```

### 5.2 Worker Implementation

```python
@celery_app.task(bind=True, max_retries=3, default_retry_delay=300)
def process_filing(self, filing_id: str):
    filing = get_filing(filing_id)

    # Select the right state agent
    agent = get_filing_agent(filing.state)
    # PA -> PAFilingAgent (runs on AWS)
    # MA -> MAFilingAgent (routes to isolated VM)

    try:
        update_filing_status(filing_id, "submitting")

        result = agent.file(filing)

        update_filing_status(filing_id, "submitted",
            confirmation_number=result.confirmation_number)

        # Store screenshots for audit trail
        for screenshot in result.screenshots:
            upload_document(filing_id, "screenshot", screenshot)

        # Start polling for approval
        poll_filing_status.apply_async(
            args=[filing_id],
            countdown=3600  # check after 1 hour
        )

    except FilingError as e:
        log_filing_event(filing_id, "submission_failed", {"error": str(e)})
        update_filing_status(filing_id, "failed")
        raise self.retry(exc=e)


@celery_app.task
def poll_filing_status(filing_id: str):
    filing = get_filing(filing_id)
    agent = get_filing_agent(filing.state)

    status = agent.check_status(filing.confirmation_number)

    if status == "approved":
        update_filing_status(filing_id, "approved",
            state_filing_number=status.filing_number)
        download_and_store_documents(filing_id, status.document_urls)
        send_approval_notification(filing.user_id, filing_id)

    elif status == "rejected":
        update_filing_status(filing_id, "rejected",
            rejection_reason=status.reason)
        send_rejection_notification(filing.user_id, filing_id, status.reason)

    else:
        # Still processing — check again in 4 hours
        poll_filing_status.apply_async(
            args=[filing_id],
            countdown=14400
        )
```

---

## 6. Data Collection Summary

### What we collect and why

| Category | Data | Purpose |
|----------|------|---------|
| **Behavioral** | Page views, clicks, time on page, scroll depth | Understand user journey |
| **Form-level** | Field focus/blur/error, time per field, backtracking | Identify UX friction |
| **Funnel** | Step completion rates, drop-off points, return rate | Optimize conversion |
| **Search** | Name queries, availability results, attempt counts | Improve name suggestion AI |
| **Financial** | Payment attempts, failures, amounts, methods | Revenue optimization |
| **Filing** | Submission success/failure, processing time, rejection reasons | Operational quality |
| **Satisfaction** | NPS, star ratings, free-text feedback, support tickets | Product quality |
| **Comparative** | State selection, entity type switches, AI recommendations taken | Feature effectiveness |
| **Session** | Source/referral, device, browser, return visits | Marketing attribution |

### Privacy & compliance

- PII is stored encrypted at rest (RDS encryption + application-level for SSN if ever needed)
- IP addresses are hashed, never stored raw
- Analytics events use session IDs, not user IDs, for anonymous visitors
- Data retention: raw events kept 2 years, aggregates kept indefinitely
- GDPR/CCPA: user data export and deletion endpoints required before launch
- No selling or sharing of user data with third parties

---

## 7. Infrastructure for MA Bot Mitigation

### Isolated VM Communication

```
┌─────────────────────────────────────────┐
│  AWS (us-east-1)                        │
│                                         │
│  Celery Worker                          │
│    │                                    │
│    │  1. Encrypt filing data            │
│    │  2. Send via WireGuard tunnel      │
│    ▼                                    │
│  WireGuard Interface ◄──── Tunnel ────► │
└─────────────────────┼──────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────┐
│  Isolated VM (residential IP)           │
│                                         │
│  Filing Agent Service                   │
│    │                                    │
│    │  1. Receive filing task            │
│    │  2. Launch browser (Xvfb)         │
│    │  3. Complete filing on MA portal   │
│    │  4. Return confirmation + screens  │
│    ▼                                    │
│  Playwright + Real Chromium             │
│    │                                    │
│    ▼                                    │
│  sec.state.ma.us (residential IP)       │
└─────────────────────────────────────────┘
```

### Communication protocol

- Filing tasks sent as encrypted JSON over WireGuard
- VM agent exposes a simple REST API (localhost only, tunnel-accessible)
- Health check endpoint for monitoring VM availability
- Automatic fallback to manual queue if VM is unreachable

---

## 8. Admin Dashboard (Internal)

### Key views for operations team

1. **Filing Queue** — pending, in-progress, needs attention
2. **Funnel Dashboard** — daily/weekly conversion rates by state and entity type
3. **Field Friction Report** — which fields cause the most errors/hesitation
4. **Name Search Analytics** — most searched names, availability rates
5. **Revenue Dashboard** — filings by state, revenue, average order value
6. **Feedback Feed** — NPS trends, recent comments, tagged issues
7. **System Health** — worker status, VM status, filing success rates

---

## 9. Tech Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Event storage | PostgreSQL (not a separate analytics DB) | Simpler for MVP; migrate to ClickHouse/BigQuery when volume warrants |
| Event ingestion | Redis queue → batch insert | Non-blocking to user, handles bursts |
| Filing automation | Playwright | Best headless browser control, good stealth plugins |
| State machine | In-app (not a workflow engine) | Fewer moving parts; Temporal/Prefect later if needed |
| Payment | Stripe PaymentIntents | Industry standard, handles SCA, easy refunds |
| Document storage | S3 with presigned URLs | Secure, scalable, cheap |
| VM communication | WireGuard tunnel | Fast, encrypted, stable — better than SSH tunnels for long-running connections |
