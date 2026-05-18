# LLC Batch State Requirements Check

Research and document LLC requirements for multiple states in one session.

## Instructions

Batch-check LLC requirements for: **$ARGUMENTS**

Accepted arguments:
- `tier1` — Delaware, Wyoming, Nevada, Florida, Texas (launch states)
- `tier2` — California, New York, Illinois, Georgia, North Carolina, Virginia, Colorado, Washington
- `all` — All 50 states + DC (runs in parallel agents where possible)
- `remaining` — States not yet documented in `specs/llc-states/`
- A comma-separated list of state codes: `CA,NY,TX`

If no argument is provided, default to `remaining` (only research states not yet documented).

### Process

**Step 1: Inventory** — Read `specs/llc-states/` to see which states are already documented.

**Step 2: Build work list** — Determine which states need research based on the argument.

**Step 3: Parallel research** — Launch parallel agents (one per state or small batches) to run `/llc-check-state` for each state. Use the Agent tool with parallel invocations for efficiency.

Each agent MUST follow the IP protection rules:
- NEVER visit state SOS portals directly
- Use aggregator sites and web search only
- Mark unverifiable items for spot-check

**Step 4: Update index** — After all states complete, rebuild `specs/llc-states/STATE_MATRIX.md` with a summary table.

### STATE_MATRIX.md Format

```markdown
# LLC State Filing Matrix

> Last updated: [date]
> States documented: [X] / 51

| State | Code | Fee | Processing | E-Filing | API | Category | Confidence | Quirks |
|-------|------|-----|-----------|----------|-----|----------|------------|--------|
| [Name] | [XX] | $[fee] | [time] | [Y/N] | [Y/N/U] | [A/B/C/D] | [H/M/L] | [notes] |
```

### Progress Tracking
After each state completes, report progress: `[X/total] states documented`.

### Rate Limiting
Even though we're using web search (not state portals), be respectful:
- Don't launch more than 5 parallel agents at once
- Space web search queries naturally
- If a web search tool rate-limits, back off and retry
