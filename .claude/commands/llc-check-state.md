# LLC State Requirements Check

Research and document LLC formation requirements for a specific US state.

## Instructions

You are researching LLC formation requirements for: **$ARGUMENTS**

If no state is provided, ask the user which state to research.

### IP Protection Rules (CRITICAL)
Follow the project's IP protection strategy from `specs/LLC_REGISTRATION_PLANNING_ROADMAP.md`:
1. **NEVER visit state SOS portals directly** — no direct fetching of state government websites
2. Use third-party aggregator sites first (Northwest, Nolo, Incfile/ZenBusiness, HarborCompliance)
3. Use web search to fill gaps
4. Only flag items that need manual VPN spot-check verification

### Research Process

**Step 1: Web Search** — Search for the state's LLC requirements using queries like:
- `"[State] LLC filing fee 2026"`
- `"[State] articles of organization requirements"`
- `"[State] LLC registered agent requirements"`
- `"[State] secretary of state business filing portal"`
- `"[State] LLC processing time"`
- `"[State] LLC annual report requirements"`

**Step 2: Aggregator Sites** — Fetch data from these trusted sources:
- Northwest Registered Agent state guide: search `"northwest registered agent [State] LLC"`
- Nolo LLC guide: search `"nolo [State] LLC"`
- ZenBusiness/Incfile state page: search `"zenbusiness [State] LLC"`
- HarborCompliance: search `"harborcompliance [State] LLC annual report"`

**Step 3: Compile Data** — Fill in ALL fields in the template below. Mark any field you couldn't verify as `[UNVERIFIED — needs spot-check]`.

**Step 4: Write the file** — Save to `specs/llc-states/{STATE_CODE}.md` using the exact template below.

**Step 5: Update the index** — Add or update the entry in `specs/llc-states/STATE_MATRIX.md`.

### Output Template

```markdown
---
state: [Full State Name]
code: [XX]
last_updated: [YYYY-MM-DD]
sources: [list of URLs/sources used]
confidence: [high/medium/low]
needs_spot_check: [yes/no]
---

# [State Name] — LLC Formation Requirements

## Filing Authority
- **Office**: [Secretary of State / Division of Corporations / etc.]
- **Portal Name**: [e.g., bizfileOnline, SilverFlume, SOSDirect]
- **Portal URL**: [URL — gathered from aggregator, not visited directly]
- **Electronic Filing**: [yes/no]
- **API/Bulk Filing Program**: [yes/no/unknown]
- **Filing Method Category**: [A: API / B: Portal / C: PDF / D: Mail-only]

## Fees
- **Standard Filing Fee**: $[amount]
- **Expedited Fee**: $[amount] ([processing time])
- **Name Reservation Fee**: $[amount]
- **Certified Copy Fee**: $[amount]

## Processing Times
- **Standard**: [timeframe]
- **Expedited**: [timeframe]
- **Online vs Mail**: [difference if any]

## Formation Requirements
- **Document Name**: [Articles of Organization / Certificate of Formation / etc.]
- **Required Fields**:
  - LLC name (must include: [LLC/L.L.C./Limited Liability Company])
  - Registered agent name and address
  - [list all other required fields]
- **Registered Agent**: [required/not required — almost always required]
- **Organizer Restrictions**: [any age/residency/entity requirements]
- **Members Listed on Filing**: [yes/no — public record implications]
- **Operating Agreement**: [required by law / recommended / not required]

## State-Specific Quirks
- **Publication Requirement**: [yes/no — if yes, details]
- **Notarization Required**: [yes/no]
- **Name Reservation Required Before Filing**: [yes/no]
- **Foreign LLC Registration**: [requirements for out-of-state LLCs]
- **Series LLC Available**: [yes/no]
- **Other Notable Rules**: [anything unusual]

## Ongoing Compliance
- **Annual Report**: [required/not required]
  - **Due Date**: [date or interval]
  - **Filing Fee**: $[amount]
  - **Online Filing Available**: [yes/no]
- **Franchise Tax**: [yes/no — amount if applicable]
- **Other Recurring Obligations**: [list any]

## Anti-Bot Observations
> These fields should be marked [UNVERIFIED] unless confirmed via aggregator reports or web search.
- **CAPTCHA on Portal**: [yes/no/unknown — type if known]
- **Login Required to File**: [yes/no/unknown]
- **Rate Limiting Observed**: [unknown — needs spot-check]
- **ToS Restricts Automation**: [unknown — needs spot-check]

## Notes
[Any additional context, warnings, or recommendations]
```

### Quality Checks
Before saving, verify:
- [ ] All dollar amounts have a source
- [ ] Processing times are current (2025-2026 data preferred)
- [ ] State-specific quirks section is filled (publication req, notarization, etc.)
- [ ] Confidence level accurately reflects data quality
- [ ] Items needing spot-check are clearly marked
