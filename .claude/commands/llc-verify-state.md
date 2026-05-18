# LLC State Requirements Verification

Verify and refresh existing LLC requirement data for a specific state.

## Instructions

Verify LLC requirements for: **$ARGUMENTS**

If no state is provided, check `specs/llc-states/` and verify the state with the oldest `last_updated` date.

If the argument is `stale`, find and verify all states with `last_updated` older than 90 days or `confidence: low`.

### Process

**Step 1: Read existing data** — Load the state file from `specs/llc-states/{STATE_CODE}.md`.

**Step 2: Identify verification targets** — Focus on:
- Fields marked `[UNVERIFIED]` or `[needs spot-check]`
- Fee amounts (change frequently)
- Processing times (change seasonally)
- Any field with `confidence: low` or `confidence: medium`

**Step 3: Re-research** — Use web search and aggregator sites to find current data. Follow the same IP protection rules:
- NEVER visit state SOS portals directly
- Search aggregator sites (Northwest, Nolo, ZenBusiness, HarborCompliance)
- Use web search for specific data points

**Step 4: Compare and update** — For each field:
- If new data matches existing: mark as verified, update `last_updated`
- If new data differs: update the field, add a note about what changed
- If still unverifiable: keep the `[UNVERIFIED]` marker

**Step 5: Update metadata** — Update the frontmatter:
- `last_updated`: today's date
- `confidence`: upgrade if more data found, downgrade if sources conflict
- `needs_spot_check`: set to `no` if all critical fields verified
- `sources`: add any new sources used

**Step 6: Report changes** — Output a summary:
```
## Verification Report: [State]
- Fields verified: [count]
- Fields updated: [list with old → new values]
- Fields still unverified: [list]
- Confidence: [old] → [new]
- Recommendation: [ready for use / needs spot-check / needs manual research]
```

### Change Log
When updating a state file, append to the Notes section:
```
### Change Log
- [YYYY-MM-DD]: [what changed and why]
```
