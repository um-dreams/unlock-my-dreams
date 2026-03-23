# LLC Registration — Full Planning Roadmap

## Context

UMD needs to offer LLC registration across all 50 US states + DC. Before writing any code, there's significant research, legal, and business planning needed. A key concern is avoiding IP blocking when interacting with state filing systems at scale. This roadmap covers every planning step required before implementation begins.

Related spec: `specs/LLC_REGISTRATION_PLAN.md` (technical architecture draft)

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
