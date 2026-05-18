# Pennsylvania Business Registration Plan

## Scope

Automated filing of **LLCs** and **Sole Proprietorships** in Pennsylvania through the Department of State's online systems.

---

## 1. Entity Types & Filing Requirements

### 1.1 LLC — Certificate of Organization

| Field | Details |
|-------|---------|
| **Filing Authority** | PA Department of State, Bureau of Corporations and Charitable Organizations |
| **Portal** | [PENN File](https://www.dos.pa.gov/BusinessCharities/Business/Pages/PENN-File.aspx) |
| **Form** | Certificate of Organization (DSCB:15-8821) |
| **Filing Fee** | $125 (online) |
| **Turnaround** | Same day to 3 business days (online) |
| **Annual Report** | $7/year, due Sept 30 (replaced decennial report in 2025 via Act 122 of 2022) |

#### Required Data Points

- LLC name (must include "Limited Liability Company", "LLC", "L.L.C.", or approved abbreviation)
- Name availability check (via PENN File business search)
- Registered office address in PA (street address, no PO Box)
- Effective date (filing date or specified future date)
- Organizer name and signature
- Optional: specific purpose clause (default is "any lawful purpose")

> **Key advantage over MA**: PA has a much lower filing fee ($125 vs. $500) and a minimal annual report ($7/year vs. $500/year in MA). This makes PA an attractive filing state.

### 1.2 Sole Proprietorship — Fictitious Name Registration

| Field | Details |
|-------|---------|
| **Filing Authority** | PA Department of State (state-level, unlike MA) |
| **Portal** | [PENN File](https://www.dos.pa.gov/BusinessCharities/Business/Pages/PENN-File.aspx) |
| **Form** | Registration of Fictitious Name (DSCB:54-311) |
| **Filing Fee** | $70 |
| **Renewal** | Every 10 years |

#### Required Data Points

- Fictitious (business) name
- Entity type (individual, general partnership, etc.)
- Address where business is conducted
- Each individual's name and address
- Brief statement of character/nature of business
- Signature of each owner

> **Advantage**: Unlike MA, PA handles sole proprietorship / DBA at the **state level** through the same PENN File system — much more automatable.

---

## 2. Automation Feasibility

### 2.1 PENN File System Assessment

The PA PENN File portal is **significantly more automation-friendly** than MA's CORP system:

- Modern-ish web application (rebuilt in recent years)
- Less aggressive bot detection compared to MA
- API-like behavior in some form submission flows
- Consistent form structure across entity types
- Reasonable rate limits

### 2.2 Automation Approach

```
┌──────────────────────────────────────────────────┐
│  UMD Backend (AWS)                               │
│                                                  │
│  ┌──────────────┐                                │
│  │ Filing Queue  │                               │
│  │ (Celery)      │                               │
│  └──────┬───────┘                                │
│         │                                        │
│         ▼                                        │
│  ┌──────────────┐     ┌─────────────────┐        │
│  │ PA Filing     │────▶│ Playwright      │        │
│  │ Worker        │     │ (can run on AWS)│        │
│  └──────────────┘     └────────┬────────┘        │
│                                │                  │
└────────────────────────────────┼──────────────────┘
                                 │
                                 ▼
                      ┌──────────────────┐
                      │  PENN File Portal │
                      │  dos.pa.gov       │
                      └──────────────────┘
```

- **No isolated VM needed** for PA (unlike MA) — standard cloud infrastructure should work
- Use Playwright in headed mode on ECS with Xvfb as a precaution
- Standard retry logic with exponential backoff
- Screenshot every step for audit trail

### 2.3 Technical Implementation

```python
class PAFilingAgent:
    """Runs on standard AWS infrastructure."""

    async def file_llc(self, filing_data: dict) -> FilingResult:
        browser = await launch_browser(headless=True)

        # Navigate to PENN File
        await browser.goto("https://www.dos.pa.gov/.../PENN-File.aspx")

        # Select entity type: LLC
        await browser.select("entity_type", "LLC")

        # Fill Certificate of Organization
        await browser.fill("llc_name", filing_data["name"])
        await browser.fill("registered_office", filing_data["pa_address"])
        await browser.fill("organizer_name", filing_data["organizer"])

        # Payment processing
        await browser.fill_payment(filing_data["payment_info"])

        # Submit and capture confirmation
        await browser.click("submit")
        confirmation = await browser.wait_for_confirmation()

        return FilingResult(
            status="submitted",
            confirmation_number=confirmation,
            receipt_url=await browser.get_receipt_url(),
        )

    async def file_sole_prop(self, filing_data: dict) -> FilingResult:
        browser = await launch_browser(headless=True)

        await browser.goto("https://www.dos.pa.gov/.../PENN-File.aspx")
        await browser.select("entity_type", "Fictitious Name")

        await browser.fill("business_name", filing_data["business_name"])
        await browser.fill("owner_name", filing_data["owner_name"])
        await browser.fill("owner_address", filing_data["owner_address"])
        await browser.fill("business_address", filing_data["business_address"])
        await browser.fill("business_nature", filing_data["description"])

        await browser.fill_payment(filing_data["payment_info"])
        await browser.click("submit")

        confirmation = await browser.wait_for_confirmation()
        return FilingResult(
            status="submitted",
            confirmation_number=confirmation,
        )
```

---

## 3. Name Availability Search

- **Endpoint**: [Business Entity Search](https://www.dos.pa.gov/BusinessCharities/Business/Pages/Business-Search.aspx)
- **Method**: Automated search is feasible — less restrictive than MA
- **Response**: Returns matching/similar entity names

### Name Rules (Pennsylvania)

- Must contain "Limited Liability Company", "LLC", "L.L.C.", "Ltd. Liability Co.", or similar
- Must be distinguishable from existing registered entities
- Cannot contain restricted words (Bank, University, Insurance) without authorization
- Cannot imply a purpose the LLC is not authorized to pursue

---

## 4. Registered Office Requirements

PA uses a **registered office** concept (not "registered agent"):

- Must be a real street address in Pennsylvania
- The entity itself is its own registered agent at that address
- Can use a **Commercial Registered Office Provider (CROP)** instead — this is PA's version of a registered agent service
- CROP must be registered with the Department of State

### UMD Strategy

- **Phase 1**: Partner with a PA-registered CROP (CT Corporation, Northwest, etc.)
- **Phase 2**: Register UMD as a CROP in PA if volume justifies

---

## 5. Post-Filing Requirements

| Task | When | Fee |
|------|------|-----|
| Obtain EIN from IRS | After filing approved | Free |
| PA Revenue Registration | Before conducting business | Free (via PA-100 form) |
| Local Business Privilege License | Varies by municipality | $25–300 |
| Annual Report | Due by Sept 30 each year (starting year after formation) | $7 |
| UCC Filing (if applicable) | As needed | $50+ |

> **Note**: As of 2025, PA requires an **annual report** ($7/year, due Sept 30) replacing the old decennial report. No penalties for missed 2025–2026 reports; enforcement (administrative dissolution after 6-month grace period) begins with 2027 reports. Reinstatement costs $35 + $15/missed year.

---

## 6. Data to Collect from Users

### Required for LLC Filing

- Full legal name of organizer(s)
- Desired LLC name (+ 2 alternates)
- Business purpose (or "any lawful purpose")
- Registered office address in PA (or use our CROP partner)
- Effective date preference
- Member/manager structure preference

### Required for Sole Proprietorship (Fictitious Name)

- Business (fictitious) name
- Owner(s) full legal name(s)
- Owner(s) home address(es)
- Business address in PA
- Nature of business description

### Additional for UMD Platform Value

- Phone number and email
- Industry / NAICS code
- Expected first-year revenue
- Number of planned employees
- Whether they'll need to collect sales tax
- Preferred start date

### Feedback & Analytics Data

- Time spent per form section
- Auto-save snapshots (track where users pause/struggle)
- Name search history and rejection count
- Entity type selection changes (did they switch from LLC to sole prop or vice versa?)
- Completion rate by entity type
- PA vs. MA selection reasoning (if user was offered both)
- Post-filing NPS score
- Support interactions during filing
- Referral source and UTM tracking

---

## 7. PA vs. MA Comparison (for user guidance)

| Factor | Pennsylvania | Massachusetts |
|--------|-------------|---------------|
| LLC Filing Fee | $125 | $500 |
| Annual Report | Annual, $7 (replaced decennial in 2025) | Annual, $500 |
| Sole Prop Filing | State-level ($70) | Municipal-level ($25-65, fragmented) |
| Processing Time | Same day – 3 days | 1–2 days (online) |
| Automation Friendly | Yes | No (bot detection) |
| Tax Climate | 8.99% corp flat tax | 8% corp excise tax |
| Total Year 1 Cost | ~$125 | ~$1,000 |
| Total Year 2+ Cost | $7/year (annual report) | $500/year |

> UMD should surface this comparison to users who might be flexible on state — PA is dramatically cheaper for LLC formation and ongoing maintenance ($7/year vs. $500/year).

---

## 8. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| PENN File UI changes | Automation breaks | Visual regression tests + alerts |
| Filing rejected | User delay | Pre-validate all fields before submission |
| CROP partner issues | No registered office | Multiple CROP partnerships |
| PA adds bot detection | Similar to MA problem | Already have MA VM infrastructure as fallback |
| Payment processing on portal | Filing fails | Retry logic + manual fallback queue |

---

## 9. MVP Scope (Pennsylvania)

1. **LLC filing** (automated via Playwright on standard AWS infra)
2. **Sole proprietorship / Fictitious Name filing** (automated — same PENN File system)
3. **Name availability search** (automated)
4. **CROP partner integration** (for registered office)
5. **PA Revenue Registration guidance** (post-filing checklist item)
6. **EIN application assistance** (link to IRS + pre-filled data)

PA is the **recommended launch state** — lower fees, less bot detection, and both entity types can be automated through a single portal.
