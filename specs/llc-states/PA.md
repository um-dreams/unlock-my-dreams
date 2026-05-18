---
state: Pennsylvania
code: PA
last_updated: 2026-05-18
sources:
  - https://www.llcuniversity.com/pennsylvania-llc/annual-report/
  - https://www.harborcompliance.com/pennsylvania-decennial-report
  - https://www.llcuniversity.com/pennsylvania-llc/forms/
  - https://www.llcuniversity.com/how-long-does-it-take-to-get-an-llc-in-pennsylvania/
  - https://www.zenbusiness.com/pennsylvania-filing-fees/
  - https://www.northwestregisteredagent.com/llc/pennsylvania/operating-agreement
  - https://www.wolterskluwer.com/en/solutions/bizfilings/state-guides/pennsylvania-llc-requirements
confidence: high
needs_spot_check: no
---

# Pennsylvania — LLC Formation Requirements

## Filing Authority
- **Office**: Pennsylvania Department of State, Bureau of Corporations and Charitable Organizations (BCCO)
- **Portal Name**: Business Filing Services (BFS)
- **Portal URL**: https://www.dos.pa.gov/
- **Electronic Filing**: yes
- **API/Bulk Filing Program**: no official API — bulk data lists available at $0.25/name
- **Filing Method Category**: B (online portal)

## Fees
- **Standard Filing Fee**: $125
- **Expedited Fee**: $100 (same-day), $300 (3-hour), $1,000 (1-hour) — in-person at Harrisburg only
- **Name Reservation Fee**: $70
- **Certified Copy Fee**: $40
- **DBA Registration**: $70

## Processing Times
- **Standard (Online)**: 1–7 business days
- **Standard (Mail)**: 10–15 business days (2–3 weeks)
- **Expedited**: Same-day to 1-hour — in-person at Harrisburg office only, cannot expedite online or mail

## Formation Requirements
- **Document Name**: Certificate of Organization (form DSCB:15-8821)
- **Additional Form Required**: Docketing Statement (DSCB:15-134A) — filed alongside Certificate
- **Required Fields**:
  - LLC name (must include "Limited Liability Company", "LLC", or "L.L.C.")
  - Registered office address (must be physical PA address)
  - Name and address of each organizer
  - Member-managed or manager-managed designation
  - Effective date (upon filing or future date)
  - Organizer signature(s)
- **Registered Agent**: PA uses "registered office" not "registered agent" — must be a physical address in PA where someone is available during business hours (9-5)
- **Organizer Restrictions**: none found
- **Members Listed on Filing**: no — organizers are listed, not members
- **Operating Agreement**: not required by law (PA LLC Act §8816), but strongly recommended

## State-Specific Quirks
- **Publication Requirement**: no
- **Notarization Required**: no
- **Name Reservation Required Before Filing**: no (optional, $70)
- **Foreign LLC Registration**: required if doing business in PA
- **Series LLC Available**: no
- **Veteran Fee Waiver**: $125 filing fee waived for veterans and reservists with proof of status
- **Two-Form Filing**: PA is unusual in requiring both a Certificate of Organization AND a Docketing Statement to be filed together

## Ongoing Compliance

### Annual Report (NEW — replaces Decennial Report)
- **Requirement**: mandatory — effective January 1, 2025 (Act 122 of 2022)
- **Due Date**: by September 30 annually (filing window: January 1 – September 30)
- **First Report Due**: the year after LLC formation
- **Filing Fee**: $7
- **Online Filing Available**: yes
- **Required Information**: entity name, PA entity number, registered office address, principal business address, at least one governor name, names/titles of principal officers
- **Grace Period**: no penalties for missed 2025 or 2026 reports; full enforcement (6-month grace then administrative dissolution) begins with 2027 reports
- **Reinstatement After Dissolution**: $35 + $15 late fee per missed report

### Old Decennial Report (DEPRECATED)
- **Status**: replaced by annual report as of 2025
- **History**: previously required every 10 years in years ending in "1" (2001, 2011, 2021)
- **Fee was**: $7
- **Note**: entities formed after Jan 1, 2012 were already exempt from the decennial report

### Franchise Tax
- No franchise tax for LLCs

## Anti-Bot Observations
- **CAPTCHA on Portal**: unknown
- **Login Required to File**: yes — account required on BFS portal
- **Rate Limiting Observed**: unknown
- **ToS Restricts Automation**: unknown

## Notes
- PA is a Category B state for UMD — portal filing, no official API
- The two-form requirement (Certificate + Docketing Statement) adds complexity to the filing adapter
- Veteran fee waiver is a nice UX touch to surface in the product
- Annual report is cheap ($7) and simple — low compliance burden for users
- No bulk filer API exists; partner API is the clear path for PA filings
