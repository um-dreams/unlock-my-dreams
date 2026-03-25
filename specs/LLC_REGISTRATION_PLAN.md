# LLC Registration — Architecture & Anti-Blocking Strategy

## Problem Statement

UMD needs to register LLCs across all 50 US states + DC on behalf of users. Each state has its own Secretary of State (SOS) office with different:
- Filing portals, forms, and APIs
- Fee structures ($50–$500+)
- Processing times (same-day to 4+ weeks)
- Technical infrastructure (some have APIs, most have web portals, some are mail-only)

**Key risk**: Automated submissions to state portals can trigger IP blocks, CAPTCHAs, rate limits, or outright bans — jeopardizing the entire product.

---

## Phase 1: Partner API (MVP — Low Risk)

Use established filing partners who already have relationships and integrations with state systems.

### Candidates

| Partner | Coverage | API? | Pricing | Notes |
|---------|----------|------|---------|-------|
| **Northwest Registered Agent** | 50 states | Yes (reseller program) | ~$100 + state fee | Well-known, white-label option |
| **Incfile / ZenBusiness** | 50 states | Reseller API | ~$0–$149 + state fee | Competitive pricing |
| **Stripe Atlas** | Delaware only | Limited API | $500 flat | Only Delaware, expensive |
| **Swyft Filings** | 50 states | Reseller API | ~$49+ | Budget option |
| **LegalInc** | 50 states | Full B2B API | Custom pricing | Built for platforms like UMD |
| **CSC Global** | 50 states | Enterprise API | Premium | Enterprise-grade, compliance focus |

### Recommended Approach
1. **Primary**: LegalInc or Northwest — purpose-built reseller/B2B APIs
2. **Fallback**: Swyft or ZenBusiness — budget alternative
3. Build an **abstraction layer** so we can swap providers per state

### Architecture (Phase 1)
```
User → UMD API → Filing Abstraction Layer → Partner API → State SOS
                                          ↓
                              Status polling / webhooks
                                          ↓
                              UMD DB (status tracking)
```

**IP blocking risk: ZERO** — the partner handles all state interactions.

---

## Phase 2: Direct State Filing (Higher Margins, Higher Risk)

### Why Go Direct?
- Partner markup eliminated → save $50–$150 per filing
- Full control over status/timeline
- Better user experience (real-time status vs partner delays)
- At scale (1000+ filings/mo), savings are significant

### State Filing Infrastructure Landscape

States fall into roughly 4 categories:

#### Category A: States with Official APIs (Easiest)
Some states offer electronic filing APIs (EDGAR-style or SOAP/REST):
- Delaware (ICIS system — bulk filer accounts available)
- Nevada (SilverFlume — API for registered agents)
- Wyoming (some electronic filing)
- A few others with registered agent portals

**Strategy**: Apply for bulk/registered agent filing accounts. These are *intended* for automated use. No IP blocking risk.

#### Category B: States with Online Portals (Most Common)
Most states have web-based filing portals (e.g., California bizfileOnline, New York DOS, Texas SOSDirect).

**This is where IP blocking is the primary concern.**

#### Category C: States with PDF Form Submission
Some states accept filled PDF forms via email or upload.

**Strategy**: Programmatic PDF filling + email/upload submission. Low blocking risk.

#### Category D: Mail-Only States
A shrinking number still require physical mail.

**Strategy**: Integration with a mail API (Lob, Click2Mail) to print and mail forms. No blocking risk.

---

## Anti-IP-Blocking Strategy (Category B States)

### 1. Registered Agent Network (BEST APPROACH)

**Instead of hitting state portals directly, become/partner with a registered agent in each state.**

- Registered agents get **official filing accounts** with state SOS offices
- These accounts have higher rate limits, API access, or dedicated portals
- Many states provide registered agents with bulk filing interfaces
- This is the *legitimate* way to file at scale

**Implementation**:
- Partner with an existing RA network (e.g., CSC, CT Corporation) for filing channel access
- Or establish UMD as a registered agent in key states (requires physical presence/address in each state — use virtual office providers)

**IP blocking risk: MINIMAL** — you're using official channels.

### 2. Distributed Filing Infrastructure

For states where portal automation is necessary:

#### a. Residential Proxy Rotation
- Use residential proxy services (Bright Data, Oxylabs, SmartProxy)
- Rotate IPs per request, spread across geographic regions matching the target state
- Mimic real users filing from that state

#### b. Rate Limiting & Request Spacing
- **Never burst** — space requests 30–120 seconds apart per state portal
- Max 5–10 filings per state per day per IP
- Queue filings and process overnight during off-peak hours
- Randomize timing (jitter) to avoid pattern detection

#### c. Browser Fingerprint Diversification
- Use headless browsers (Playwright) with randomized fingerprints
- Rotate: User-Agent, screen resolution, timezone, WebGL renderer, canvas fingerprint
- Use browser automation frameworks that resist fingerprinting detection (e.g., `playwright-stealth`, `puppeteer-extra-plugin-stealth`)

#### d. CAPTCHA Handling
- Integrate CAPTCHA solving services (2Captcha, Anti-Captcha, CapSolver)
- Implement retry logic with exponential backoff
- Fall back to manual queue for persistent CAPTCHAs

### 3. Hybrid Model (RECOMMENDED)

| Filing Volume | Strategy |
|---------------|----------|
| 0–100/mo | Partner API (Phase 1) |
| 100–500/mo | RA network + Partner API fallback |
| 500–2000/mo | RA network + direct filing for API states |
| 2000+/mo | Full RA network + distributed infrastructure |

**Start with the registered agent path, not portal scraping.** Portal automation is fragile, legally grey, and creates operational risk. RA accounts are the legitimate at-scale approach.

---

## State-by-State Complexity Matrix

### Priority Tiers (by filing volume demand)

**Tier 1 — Launch States** (highest demand, most LLC-friendly):
| State | Portal | API? | Fee | Complexity |
|-------|--------|------|-----|------------|
| Delaware | ICIS | Yes (bulk filer) | $90 | Low — API available |
| Wyoming | WY SOS | Partial | $100 | Low |
| Nevada | SilverFlume | Yes (RA) | $425 | Low — API for RAs |
| Florida | Sunbiz | No | $125 | Medium — portal only |
| Texas | SOSDirect | No | $300 | Medium — portal only |

**Tier 2 — High Demand**:
- California, New York, Illinois, Georgia, North Carolina, Virginia, Colorado, Washington

**Tier 3 — Remaining States**:
- Roll out based on user demand data

---

## Technical Architecture (Phase 2)

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│  UMD API    │────▶│ Filing Engine     │────▶│ State Adapters      │
│  (FastAPI)  │     │ (Celery Workers)  │     │ (per-state modules) │
└─────────────┘     └──────────────────┘     └─────────────────────┘
                           │                          │
                    ┌──────┴──────┐            ┌──────┴──────────┐
                    │ Filing Queue │            │ State Router    │
                    │ (Redis)      │            │                 │
                    └─────────────┘            ├─ API adapter    │
                                               ├─ Portal adapter │
                                               ├─ PDF adapter    │
                                               └─ Mail adapter   │
                                                                  │
                                               ┌──────────────────┘
                                               │
                                        ┌──────┴──────┐
                                        │ Proxy Layer  │
                                        │ (if needed)  │
                                        └─────────────┘
```

### Key Components

1. **State Adapter Interface** — Uniform interface, per-state implementation
   ```python
   class StateAdapter(ABC):
       state_code: str
       filing_method: Literal["api", "portal", "pdf", "mail"]

       async def validate_filing(data: FilingData) -> ValidationResult
       async def submit_filing(data: FilingData) -> FilingSubmission
       async def check_status(filing_id: str) -> FilingStatus
       async def get_fees(entity_type: str) -> FeeSchedule
   ```

2. **Filing Queue** — Priority queue with state-aware rate limiting
3. **Proxy Manager** — IP rotation with state-geo-targeting
4. **Status Tracker** — Polling + webhook receiver for filing status
5. **Document Generator** — Fills state-specific forms from UMD business plan data
6. **Retry Engine** — Exponential backoff, circuit breaker per state

---

## Legal & Compliance Considerations

1. **Terms of Service**: Many state portals prohibit automated access. Using RA accounts sidesteps this since those are official filing channels.
2. **Registered Agent Requirements**: Must maintain a physical address in each state where you serve as RA. Virtual office providers (Regus, WeWork, Alliance Virtual) can fulfill this.
3. **Unauthorized Practice of Law (UPL)**: UMD fills forms based on user input — does NOT provide legal advice. Need clear disclaimers.
4. **Data Security**: Handling SSNs (for EIN), addresses, personal info. Must be SOC 2 compliant, encrypt at rest and in transit.
5. **State-Specific Rules**: Some states require notarization, publication (NY), or specific organizer qualifications.

---

## Recommended Execution Plan

### Step 1: Partner API Integration (Weeks 5-6 of MVP)
- [ ] Evaluate and select partner (LegalInc, Northwest, or Swyft)
- [ ] Build abstraction layer (`FilingProvider` interface)
- [ ] Implement partner adapter
- [ ] Build filing status tracking
- [ ] UI: filing flow, status dashboard, document viewer

### Step 2: Registered Agent Research (Post-MVP, Month 2-3)
- [ ] Research RA requirements per state
- [ ] Evaluate RA network partnerships (CSC, CT Corp, Northwest)
- [ ] Cost analysis: partner API fees vs RA network costs at projected volume
- [ ] Decision point: build own RA network vs partner

### Step 3: Direct Filing for API States (Month 3-4)
- [ ] Apply for bulk filer account in Delaware
- [ ] Apply for RA filing access in Nevada (SilverFlume)
- [ ] Build API adapters for states with official APIs
- [ ] A/B test: direct vs partner for these states

### Step 4: Scale Direct Filing (Month 4-6)
- [ ] Build portal adapters for Tier 1 non-API states
- [ ] Set up proxy infrastructure
- [ ] Implement CAPTCHA handling
- [ ] Build monitoring & alerting for filing failures
- [ ] Gradual rollout state by state

---

---

## Research Phase IP Protection

Even during the planning/research phase, visiting all 51 state SOS portals in quick succession can trigger bot detection. See `specs/LLC_REGISTRATION_PLANNING_ROADMAP.md` — "Research IP Protection Strategy" section for the full methodology.

**Summary**: Use a 4-layer approach — third-party aggregator sites first, AI web search second, direct SOS contact third, VPN spot-checks last. Never hit state portals directly from our own infrastructure during research.

---

## Key Takeaway

**Don't scrape state portals from day one.** The path to avoiding IP blocks is:

1. **Start with partner APIs** — zero IP risk, fast to market
2. **Get registered agent accounts** — official filing channels, minimal IP risk
3. **Only automate portals as last resort** — and when you do, use residential proxies, rate limiting, and browser fingerprint rotation

The registered agent path is not just an anti-blocking strategy — it's the *right* business model for filing at scale. Every major competitor (LegalZoom, ZenBusiness, Northwest) operates this way.
