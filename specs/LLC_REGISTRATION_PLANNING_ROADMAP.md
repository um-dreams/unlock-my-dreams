# LLC Registration — Full Planning Roadmap

## Context

UMD needs to offer LLC registration across all 50 US states + DC. Before writing any code, there's significant research, legal, and business planning needed. A key concern is avoiding IP blocking when interacting with state filing systems at scale. This roadmap covers every planning step required before implementation begins.

Related spec: `specs/LLC_REGISTRATION_PLAN.md` (technical architecture draft)

---

## Research IP Protection Strategy

Before any research begins, we need a methodology that protects our IP address from being flagged or banned by state SOS systems. This applies to the entire planning phase — even passive browsing of 51 state portals in quick succession can look like reconnaissance to WAFs and bot-detection systems.

### Principle: Never Touch State Portals Directly During Research

The research phase should use **zero direct requests** to state SOS websites from our own infrastructure. Every piece of data we need can be gathered through indirect channels.

### Layer 1: Third-Party Aggregator Sources (Primary)

Most state filing data (fees, forms, processing times, required fields) is already compiled by established services. Use these first — they're public, frequently updated, and involve zero state portal interaction:

| Source | What It Provides | URL Pattern |
|--------|-----------------|-------------|
| **Northwest Registered Agent** state guides | Fees, forms, step-by-step filing, requirements per state | Public website |
| **Nolo.com** LLC guides | Legal requirements, state comparisons, operating agreement rules | Public website |
| **Incfile / ZenBusiness** state pages | Fee breakdowns, processing times, expedited options | Public website |
| **NASS (Nat'l Assoc. of SOS)** | Official directory of all SOS offices, links, contact info | Public website |
| **Wikipedia** state SOS articles | Portal names, basic filing info, history | Public website |
| **Harborcompliance.com** | Annual report requirements, compliance calendars per state | Public website |

**Action**: Use web search and these aggregators to fill 80-90% of the STATE_MATRIX before ever considering a state portal visit.

### Layer 2: AI-Assisted Web Research (Secondary)

Use AI tools with built-in web search to gather data without our IP making direct requests:

- **Gemini (via MCP)** — has web search capability, 1M context. Can research multiple states per query.
- **General web search** — search for specific data points rather than browsing portals directly.

Example queries:
- `"California LLC filing fee 2026 bizfileOnline"`
- `"Texas SOSDirect LLC articles of organization requirements"`
- `"which US states have SOS API for business filing"`

The AI tool's infrastructure makes the web requests, not our IP.

### Layer 3: VPN/Proxy for Spot-Check Verification (Last Resort)

For the small number of data points that can't be found through aggregators or web search (e.g., verifying a specific portal's CAPTCHA type, checking if a state added an API since last documented):

- [ ] **Use a commercial VPN** (Mullvad, ProtonVPN, or similar) — switch to an exit node in the target state
- [ ] **One state per session** — don't visit 10 state portals in one sitting
- [ ] **Space visits** — max 2-3 state portal visits per day via VPN
- [ ] **Use a clean browser profile** — private/incognito window, clear cookies between states
- [ ] **Behave like a human** — browse naturally, don't use dev tools or inspect network traffic while on the portal
- [ ] **Never run scripts** against state portals during research — manual browsing only

### Layer 4: FOIA / Direct Contact (For Sensitive Questions)

For questions about API access, bulk filer programs, or registered agent portal availability:

- [ ] **Email the state SOS office directly** — ask about electronic filing options, API programs, bulk filer accounts
- [ ] **Call the SOS business filing division** — many states have helpful staff who will explain their electronic filing options
- [ ] **FOIA requests** — for states where API/portal documentation isn't public, a FOIA request can surface technical specs

This approach is slower but produces the most authoritative answers and creates a paper trail that legitimizes our interest.

### Research Data Collection Template

For each state, gather the following through the layers above (in order of preference):

```
State: [XX]
Source: [aggregator/web search/VPN spot-check/SOS contact]

Filing Portal:
  - Name:
  - URL:
  - Electronic filing available: [yes/no]
  - API/bulk filing program: [yes/no/unknown]

Fees:
  - Standard filing fee: $
  - Expedited fee: $
  - Name reservation fee: $

Processing:
  - Standard processing time:
  - Expedited processing time:

Requirements:
  - Required fields on articles of organization:
  - Registered agent required: [yes/no]
  - Publication requirement: [yes/no]
  - Notarization required: [yes/no]
  - Organizer restrictions:

Anti-Bot Observations (if spot-checked):
  - CAPTCHA present: [yes/no/type]
  - Login required to file: [yes/no]
  - Rate limiting observed: [yes/no]
  - ToS mentions automated access: [yes/no]

Notes:
```

### Research Phase Timeline with IP Protection

```
Days 1-3:   Layer 1 — Aggregator scrape (Northwest, Nolo, Incfile guides)
            → Fills ~80% of STATE_MATRIX for all 51 jurisdictions
Days 4-5:   Layer 2 — AI web search for gaps
            → Fills to ~95% coverage
Days 6-10:  Layer 4 — Email/call SOS offices for API/bulk filer questions
            → Authoritative answers on filing channels
Days 11-14: Layer 3 — VPN spot-checks for remaining gaps (CAPTCHA types, portal UX)
            → Max 2-3 state portals per day, completes PORTAL_DEFENSES data
```

---

## Planning Steps

### 1. State Filing Research (per-state audit)

- [ ] **1a. Catalog all 50 states + DC filing methods**
  - For each state: what is the SOS portal URL, does it have an API, does it accept electronic filing, PDF, or mail-only?
  - Document: filing fees, processing times, expedited options, required fields
  - Output: `specs/llc-states/STATE_MATRIX.md` — master spreadsheet of all 51 jurisdictions

- [ ] **1b. Identify states with official APIs or bulk filer programs**
  - Delaware ICIS, Nevada SilverFlume, others
  - What are the application requirements? (registered agent status, volume minimums, fees)
  - Output: list of states where automated filing is officially supported

- [ ] **1c. Document state-specific quirks**
  - New York publication requirement
  - States requiring notarization
  - States requiring specific organizer qualifications
  - States with name reservation requirements before filing
  - Annual report / franchise tax obligations per state
  - Output: `specs/llc-states/STATE_QUIRKS.md`

- [ ] **1d. Analyze state portal anti-bot protections**
  - Which portals use CAPTCHAs? What type (reCAPTCHA v2/v3, hCaptcha, custom)?
  - Rate limiting behavior (requests/min, IP-based, session-based)?
  - ToS restrictions on automated access?
  - Output: `specs/llc-states/PORTAL_DEFENSES.md`

---

### 2. Partner API Evaluation

- [ ] **2a. Contact and evaluate filing partner APIs**
  - LegalInc, Northwest Registered Agent, Swyft Filings, ZenBusiness, CSC Global
  - For each: request API docs, pricing sheet, SLA, coverage (all 50 states?), white-label options
  - Output: `specs/PARTNER_EVALUATION.md` — comparison matrix

- [ ] **2b. Test partner API sandboxes**
  - Which partners offer sandbox/test environments?
  - Evaluate: response times, error handling, status webhook support, document delivery format
  - Output: technical evaluation notes per partner

- [ ] **2c. Negotiate terms**
  - Volume pricing tiers
  - White-label / co-branding options
  - SLA guarantees (filing turnaround, uptime)
  - Data handling & privacy terms (they'll receive user PII)
  - Output: shortlist of 1 primary + 1 backup partner

---

### 3. Registered Agent Strategy

- [ ] **3a. Research RA requirements per state**
  - Physical address requirement in each state
  - Registration/licensing requirements to serve as RA
  - Annual fees and compliance obligations
  - Output: `specs/REGISTERED_AGENT_STRATEGY.md`

- [ ] **3b. Evaluate RA network partnerships**
  - CSC Global, CT Corporation, Northwest, National Registered Agents
  - Can we white-label their RA services?
  - Do they provide filing channel access (bulk portals, API access)?
  - Cost per state per year

- [ ] **3c. Cost modeling: partner API vs own RA network**
  - At 100, 500, 1000, 5000 filings/month — what's the break-even?
  - Factor in: per-filing fees, RA annual fees, virtual office costs, compliance overhead
  - Output: financial model showing when direct filing becomes profitable

- [ ] **3d. Decision: build vs partner for RA**
  - If building own RA network: which states first? Virtual office providers to use?
  - If partnering: which RA network? What access do they provide?

---

### 4. Anti-IP-Blocking Strategy (for direct portal filing)

- [ ] **4a. Categorize states by blocking risk**
  - Low risk: API states, PDF/mail states
  - Medium risk: portals with basic rate limiting
  - High risk: portals with aggressive bot detection (CAPTCHA, fingerprinting, IP bans)
  - Output: risk matrix

- [ ] **4b. Proxy infrastructure research**
  - Evaluate residential proxy providers: Bright Data, Oxylabs, SmartProxy, IPRoyal
  - Compare: pricing per GB, IP pool size, geo-targeting (state-level), rotation options
  - Test: can we get IPs in specific US states?
  - Output: proxy provider recommendation

- [ ] **4c. Browser automation approach**
  - Evaluate: Playwright vs Puppeteer vs Selenium
  - Stealth plugins: playwright-stealth, puppeteer-extra-plugin-stealth
  - Fingerprint randomization capabilities
  - CAPTCHA solving: 2Captcha vs Anti-Captcha vs CapSolver — pricing, accuracy, speed
  - Output: automation stack recommendation

- [ ] **4d. Rate limiting design**
  - Per-state request budgets (filings/day, requests/minute)
  - Queue design: how to distribute filings across time windows
  - Circuit breaker: what happens when a state portal blocks us?
  - Fallback chain: direct → partner API → manual queue
  - Output: rate limiting specification

- [ ] **4e. Monitoring & alerting plan**
  - How to detect when we're being blocked (HTTP 429, CAPTCHA frequency spike, connection resets)
  - Alerting thresholds
  - Automatic fallback triggers
  - Output: monitoring specification

---

### 5. Legal & Compliance Planning

- [ ] **5a. UPL (Unauthorized Practice of Law) review**
  - What can we legally do vs what requires a licensed attorney?
  - State-by-state UPL rules for document preparation services
  - Competitor analysis: how do LegalZoom, ZenBusiness handle this?
  - Output: legal boundaries document, disclaimer language

- [ ] **5b. Data security & privacy requirements**
  - PII handling: SSNs, addresses, financial info
  - SOC 2 Type II requirements and timeline
  - Encryption requirements (at rest, in transit)
  - Data retention policies
  - Output: security requirements spec

- [ ] **5c. Terms of Service & liability**
  - Draft ToS sections for LLC filing service
  - Liability limitations for filing errors/delays
  - Refund policy for failed filings
  - Output: legal team review checklist

- [ ] **5d. State-specific compliance obligations**
  - Do we need to register as a document preparation service in any state?
  - Business licensing requirements for offering filing services
  - Money transmitter considerations (collecting fees on behalf of states)

---

### 6. Product & UX Planning

- [ ] **6a. User filing flow design**
  - What info do we collect from the user? At what point in the journey?
  - How does business plan data pre-fill filing forms?
  - Multi-member LLC vs single-member flow differences
  - Output: user flow wireframes / diagrams

- [ ] **6b. Status tracking UX**
  - Filing states: draft → submitted → processing → approved → completed
  - How do we communicate processing times (varies 1 day to 6 weeks by state)?
  - Document delivery: how/where do users access formation docs?
  - Output: status tracking design spec

- [ ] **6c. Pricing model for filing fees**
  - Pass-through at cost vs markup?
  - How to handle expedited filing options?
  - Bundling: registered agent fee included in subscription or separate?
  - Output: pricing decision document

- [ ] **6d. Error handling & support flow**
  - What happens when a filing is rejected? (name conflict, missing info, state error)
  - Automated retry vs manual intervention thresholds
  - Customer support escalation path
  - Output: error handling specification

---

### 7. Technical Architecture Planning

- [ ] **7a. Database schema design for filings**
  - Filing records, status history, documents, state configurations
  - Multi-tenant considerations
  - Output: schema draft in `specs/`

- [ ] **7b. State adapter interface design**
  - Abstract interface that all state adapters implement
  - Partner API adapter vs direct filing adapter
  - Output: interface spec with method signatures

- [ ] **7c. Queue & worker architecture**
  - Celery task design for filing submission, status polling, document retrieval
  - Priority queuing (expedited vs standard)
  - Retry policies per state
  - Output: queue architecture spec

- [ ] **7d. Document generation pipeline**
  - Operating agreement templates (state-specific variations)
  - Articles of Organization generation
  - EIN application assistance flow
  - Output: document template strategy

---

### 8. Go-to-Market Sequencing

- [ ] **8a. State launch order**
  - Rank states by: user demand, filing ease, fee cost, processing speed
  - Recommended: Delaware, Wyoming, Nevada, Florida, Texas first
  - Output: phased state rollout plan

- [ ] **8b. MVP scope definition**
  - Which states in MVP? (suggest: top 5 only)
  - Partner API only in MVP? (yes — direct filing is post-MVP)
  - What filing types in MVP? (single-member LLC only?)
  - Output: MVP scope document

- [ ] **8c. Success metrics**
  - Filing completion rate target
  - Average filing turnaround time
  - Filing error/rejection rate threshold
  - Customer satisfaction score
  - Output: KPI definitions

---

## Recommended Planning Order

```
Week 1:  Steps 1a, 2a, 5a (parallel — state research, partner outreach, legal review)
Week 2:  Steps 1b, 1c, 2b, 3a (dig deeper on states, test partner APIs, RA research)
Week 3:  Steps 2c, 3b, 3c, 6a (negotiate partners, RA cost model, UX design)
Week 4:  Steps 1d, 4a, 4b, 5b (portal analysis, proxy research, security planning)
Week 5:  Steps 3d, 6b, 6c, 7a, 7b (decisions, UX, schema design)
Week 6:  Steps 4c, 4d, 4e, 7c, 7d (automation stack, queue design, doc pipeline)
Week 7:  Steps 5c, 5d, 6d, 8a, 8b, 8c (legal finalization, launch planning)
```
