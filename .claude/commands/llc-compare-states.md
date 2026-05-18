# LLC State Comparison

Compare LLC formation requirements across multiple states to help users choose where to form.

## Instructions

Compare states: **$ARGUMENTS**

If no arguments provided, compare the Tier 1 launch states: Delaware, Wyoming, Nevada, Florida, Texas.

Accepts: comma-separated state codes (e.g., `DE,WY,NV`) or `tier1`, `tier2`, `cheapest`, `fastest`.

### Process

**Step 1: Load state data** — Read each state's file from `specs/llc-states/{STATE_CODE}.md`.

If any requested state hasn't been documented yet, run the research process for it first (following `/llc-check-state` instructions and IP protection rules).

**Step 2: Build comparison** — Create a comparison covering:

1. **Cost Comparison**
   - Filing fee
   - Expedited fee
   - Annual report fee
   - Franchise tax
   - Total first-year cost
   - Total ongoing annual cost

2. **Speed Comparison**
   - Standard processing time
   - Expedited processing time
   - Online filing available

3. **Privacy & Structure**
   - Members listed publicly
   - Series LLC available
   - Operating agreement required
   - Publication requirement

4. **Ease of Filing**
   - Filing method category (API/Portal/PDF/Mail)
   - Quirks and special requirements
   - Registered agent complexity

5. **Compliance Burden**
   - Annual report requirements
   - Franchise tax
   - Other recurring obligations

**Step 3: Recommendation** — Based on the comparison, provide recommendations:
- **Cheapest to form**: [state]
- **Fastest to form**: [state]
- **Most privacy-friendly**: [state]
- **Lowest ongoing compliance**: [state]
- **Best for UMD to support first**: [state] (considering API availability, filing ease, user demand)

**Step 4: Save comparison** — Write to `specs/llc-states/COMPARISON_{STATE_CODES}.md`.
