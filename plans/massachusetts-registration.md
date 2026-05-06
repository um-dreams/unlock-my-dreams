# Massachusetts Business Registration Plan

## Scope

Automated filing of **LLCs** and **Sole Proprietorships** in Massachusetts through the Secretary of the Commonwealth's online systems.

---

## 1. Entity Types & Filing Requirements

### 1.1 LLC — Certificate of Organization

| Field | Details |
|-------|---------|
| **Filing Authority** | Secretary of the Commonwealth, Corporations Division |
| **Portal** | [CORP Online Filing](https://corp.sec.state.ma.us/corp/loginsystem/login_form.asp) |
| **Form** | Certificate of Organization (online or paper) |
| **Filing Fee** | $500 (online), $520 (paper) |
| **Turnaround** | 1–2 business days (online), 5–10 days (mail) |
| **Annual Report** | Due by anniversary date; $500 fee |

#### Required Data Points

- LLC name (must include "LLC", "L.L.C.", or "Limited Liability Company")
- Name availability check (real-time via CORP search)
- Street address of principal office (MA address not required)
- Registered agent name and MA street address (PO Box not accepted)
- General character of business (brief description)
- Manager-managed vs. member-managed designation
- Effective date (filing date or future date up to 90 days)
- Authorized signatory name, title, and signature
- Organizer name and address

### 1.2 Sole Proprietorship — Business Certificate (DBA)

| Field | Details |
|-------|---------|
| **Filing Authority** | City/Town Clerk (not state-level) |
| **Form** | Business Certificate / DBA |
| **Filing Fee** | $25–$65 (varies by municipality) |
| **Renewal** | Every 4 years |

#### Required Data Points

- Business name
- Owner full legal name
- Owner residential address
- Business address (within the municipality)
- Nature of business
- Date business commenced or will commence

> **Important**: Sole proprietorship filings in MA are handled at the **municipal level** — each city/town clerk has their own process. Many still require in-person or mail filing. Automation feasibility varies drastically by municipality.

---

## 2. Bot Detection & Anti-Automation Concerns

### 2.1 Known Issues

The MA Secretary of State's CORP system has been observed to:

- **Block datacenter/cloud IP ranges** (AWS, Azure, GCP, DigitalOcean)
- **Rate-limit or CAPTCHA** on repeated form submissions
- **Session-based fingerprinting** that flags headless browsers
- **Network-level blocking** of IPs associated with automated traffic
- **TLS fingerprinting** that can distinguish Selenium/Playwright from real browsers

### 2.2 Recommended Mitigation: Isolated VM Strategy

```
┌─────────────────────────────────────────────────┐
│  UMD Backend (AWS)                              │
│                                                 │
│  ┌──────────────┐    WireGuard/SSH Tunnel       │
│  │ Filing Queue  │──────────────────────┐       │
│  │ (Celery)      │                      │       │
│  └──────────────┘                      ▼       │
│                               ┌────────────────┐│
│                               │ Isolated VM     ││
│                               │ (Residential IP)││
│                               │                 ││
│                               │ • Playwright    ││
│                               │ • Real browser  ││
│                               │ • Residential   ││
│                               │   ISP/proxy     ││
│                               └────────┬───────┘│
│                                        │        │
└────────────────────────────────────────┼────────┘
                                         │
                                         ▼
                              ┌──────────────────┐
                              │  MA CORP Portal   │
                              │  sec.state.ma.us  │
                              └──────────────────┘
```

#### Option A: Dedicated Residential VM (Recommended for MVP)

- Lease a mini PC or NUC hosted at a residential location (or colocation with residential IP block)
- Run a lightweight agent that receives filing tasks over a secure tunnel (WireGuard or SSH)
- Use Playwright with a real Chromium profile (not headless) via Xvfb
- Human-like interaction patterns: randomized delays, mouse movements, typing cadence
- Residential IP avoids datacenter IP blacklists

**Estimated cost**: $30–60/month (mini PC power + residential internet)

#### Option B: Residential Proxy Service

- Use a residential proxy provider (Bright Data, Oxylabs, SmartProxy)
- Route Playwright traffic through rotating residential IPs
- Less reliable than dedicated VM but easier to set up
- Risk: proxy IPs can still get flagged if shared

**Estimated cost**: $50–150/month depending on bandwidth

#### Option C: Manual Filing Fallback

- For MVP, accept filings through UMD and queue them
- Human operator completes the filing on the CORP portal
- Notify user of completion via email/dashboard
- Gradually automate as bot detection patterns are mapped

**Recommended approach**: Start with **Option C** (manual fallback) + **Option A** (residential VM) in parallel. Use Option C while building and testing the automated pipeline on Option A.

### 2.3 Technical Implementation for Automated Filing

```python
# Pseudocode for MA filing agent
class MAFilingAgent:
    """Runs on isolated VM with residential IP."""

    def __init__(self):
        self.browser = None
        self.session_profile = "ma_corp_profile"

    async def file_llc(self, filing_data: dict) -> FilingResult:
        # 1. Launch real browser (not headless)
        self.browser = await launch_browser(
            headless=False,  # Use Xvfb for virtual display
            profile=self.session_profile,
            viewport=randomize_viewport(),
        )

        # 2. Navigate with human-like delays
        await self.navigate("https://corp.sec.state.ma.us/...")
        await human_delay(2, 5)  # 2-5 second random wait

        # 3. Name availability check
        await self.check_name(filing_data["llc_name"])

        # 4. Fill form fields with typing simulation
        await self.type_field("org_name", filing_data["llc_name"], wpm=45)
        await self.type_field("address", filing_data["address"], wpm=40)
        # ... remaining fields

        # 5. Handle payment (Stripe -> MA portal payment)
        await self.process_payment(filing_data["payment"])

        # 6. Capture confirmation
        confirmation = await self.capture_confirmation()
        return FilingResult(
            status="submitted",
            confirmation_number=confirmation,
            screenshots=self.screenshots,
        )
```

---

## 3. Name Availability Search

Before filing, UMD should check name availability:

- **Endpoint**: CORP Entity Search at `https://corp.sec.state.ma.us/CorpWeb/CorpSearch/CorpSearch.aspx`
- **Method**: Can be scraped (less anti-bot protection on search vs. filing)
- **Fallback**: Instruct users to check manually and confirm

### Name Rules (Massachusetts)

- Must contain "Limited Liability Company", "LLC", or "L.L.C."
- Cannot contain words implying it's a different entity type (Corp, Inc)
- Cannot contain restricted words (Bank, Insurance, University) without approval
- Must be distinguishable from existing registered entities

---

## 4. Registered Agent Requirements

- Must be a MA resident individual OR a business entity authorized to do business in MA
- Must have a physical street address in MA (no PO Boxes)
- Must be available during normal business hours

### UMD Strategy

- **Phase 1**: Partner with an existing registered agent service (Northwest, Incfile)
- **Phase 2**: Evaluate becoming a registered agent service ourselves (requires MA presence)

---

## 5. Post-Filing Requirements

| Task | When | Fee |
|------|------|-----|
| Obtain EIN from IRS | After filing approved | Free |
| File Annual Report | Anniversary of formation | $500 |
| MA DOR Registration | If collecting sales tax | Free |
| Business Certificate (local) | If operating under DBA | $25–65 |
| Workers' Comp Insurance | Before hiring employees | Varies |

---

## 6. Data to Collect from Users

### Required for Filing

- Full legal name of organizer(s)
- Business name (desired LLC name + 2 alternates)
- Business description / purpose
- Principal office address
- Registered agent selection (use our partner or provide own)
- Manager-managed vs. member-managed preference
- Member names and addresses (for operating agreement)

### Additional for UMD Platform Value

- Phone number and email (for filing notifications)
- Industry / NAICS code
- Expected revenue range
- Number of planned employees
- Funding source (self-funded, investors, loan)
- Timeline urgency (standard vs. expedited)

### Feedback & Analytics Data

- Time spent on each form section
- Fields where users hesitate or backtrack
- Name availability search attempts (how many names rejected)
- Drop-off point in the funnel
- Support tickets / chat messages during filing
- Post-filing satisfaction survey
- Source/referral tracking (how they found UMD)

---

## 7. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| MA portal blocks our automation | Filing fails | Manual fallback queue + residential VM |
| MA changes portal UI | Automation breaks | Visual regression tests + alerts + manual fallback |
| Filing rejected by state | User delay | Pre-validation of all fields before submission |
| Registered agent partner issues | Compliance risk | Multiple RA partnerships + in-house backup |
| Municipal DBA fragmentation | Can't automate sole props | Start with LLC only; add municipalities incrementally |

---

## 8. MVP Scope (Massachusetts)

1. **LLC filing only** (sole proprietorships deferred — too fragmented across municipalities)
2. **Manual filing with automated data collection** (Option C)
3. **Name availability search** (automated scraping of CORP search)
4. **Partner registered agent** (Northwest or similar)
5. **Post-filing checklist** (EIN, annual report reminders, DOR registration)
6. **Isolated VM infrastructure** built in parallel for future automation
