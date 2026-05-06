# Frontend UI Draft — Business Registration Flow

## Overview

The registration UI guides users from entity type selection through filing completion. Designed as a multi-step wizard with persistent progress tracking, auto-save, and inline validation.

---

## 1. Page Structure

```
/register                → State & entity type selection
/register/info           → Business information form
/register/details        → Entity-specific details (LLC vs sole prop)
/register/agent          → Registered agent / office selection
/register/review         → Review all information before filing
/register/payment        → Payment processing
/register/status         → Filing status & post-filing checklist
```

---

## 2. Screen-by-Screen Wireframes

### 2.1 State & Entity Type Selection (`/register`)

```
┌─────────────────────────────────────────────────────────────┐
│  ← Back to Dashboard                          Step 1 of 6  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Register Your Business                             │    │
│  │  We'll guide you through every step.                │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  Where will you register?                                   │
│                                                             │
│  ┌─────────────────────┐  ┌─────────────────────┐          │
│  │  🏛️ Massachusetts   │  │  🏛️ Pennsylvania    │          │
│  │                     │  │                     │          │
│  │  LLC: $500          │  │  LLC: $125          │          │
│  │  Annual report: $500│  │  No annual report   │          │
│  │  Processing: 1-2 day│  │  Processing: <1 day │          │
│  │                     │  │  ★ Recommended      │          │
│  └─────────────────────┘  └─────────────────────┘          │
│                                                             │
│  What type of business entity?                              │
│                                                             │
│  ┌─────────────────────┐  ┌─────────────────────┐          │
│  │  LLC                │  │  Sole Proprietorship │          │
│  │                     │  │                     │          │
│  │  • Limited liability│  │  • Simplest setup   │          │
│  │  • Tax flexibility  │  │  • No separate tax  │          │
│  │  • Professional     │  │  • Lower cost       │          │
│  │    credibility      │  │  • Personal liability│          │
│  └─────────────────────┘  └─────────────────────┘          │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  💡 Not sure? Our AI can recommend the best entity  │   │
│  │     type based on your business plan.    [Ask AI]   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│                                          [Continue →]       │
└─────────────────────────────────────────────────────────────┘
```

**Component breakdown:**
- `StateSelector` — clickable cards with fee comparison
- `EntityTypeSelector` — clickable cards with pros/cons
- `AIRecommendationBanner` — links to AI entity type advisor
- State comparison tooltip/modal on hover

### 2.2 Business Information (`/register/info`)

```
┌─────────────────────────────────────────────────────────────┐
│  ← Back                                       Step 2 of 6  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━░░░░░░░░░░░░  33%            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Business Name                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Acme Solutions                                     │    │
│  └─────────────────────────────────────────────────────┘    │
│  ✅ "Acme Solutions LLC" is available in Pennsylvania       │
│                                                             │
│  Alternate Name 1 (in case primary is taken)                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Acme Business Solutions                            │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  Alternate Name 2                                           │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Acme Consulting Group                              │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  Business Description                                       │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Technology consulting and software development     │    │
│  │  services for small businesses.                     │    │
│  │                                                     │    │
│  └─────────────────────────────────────────────────────┘    │
│  [✨ Generate from my business plan]                        │
│                                                             │
│  Industry                                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Technology / Software  ▼                           │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│                                 [← Back]  [Continue →]      │
└─────────────────────────────────────────────────────────────┘
```

**Key features:**
- **Real-time name availability check** — debounced API call as user types (500ms delay)
- **Auto-populate from business plan** — if user already created a plan in UMD, pre-fill fields
- **Auto-save** — every field change saved to draft (localStorage + server)

### 2.3 Entity-Specific Details (`/register/details`)

#### LLC View

```
┌─────────────────────────────────────────────────────────────┐
│  ← Back                                       Step 3 of 6  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━░░░░░  50%           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  LLC Structure                                              │
│                                                             │
│  Management Type                                            │
│  ○ Member-Managed (members run the business — most common)  │
│  ● Manager-Managed (designated managers run the business)   │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  ℹ️  Most single-owner LLCs choose Member-Managed.  │   │
│  │     Manager-Managed is better when you have          │   │
│  │     passive investors.                [Learn more]   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│  Members                                                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  👤 John Smith                                      │    │
│  │     123 Main St, Boston, MA 02101                   │    │
│  │     Ownership: 100%           [Edit] [Remove]       │    │
│  └─────────────────────────────────────────────────────┘    │
│  [+ Add Another Member]                                     │
│                                                             │
│  Organizer (person filing the paperwork)                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  ○ Same as member above                             │    │
│  │  ○ Different person:  ___________________________   │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  Effective Date                                             │
│  ○ Upon filing (immediately)                                │
│  ○ Specific date:  [  📅  ]                                │
│                                                             │
│                                 [← Back]  [Continue →]      │
└─────────────────────────────────────────────────────────────┘
```

#### Sole Proprietorship View

```
┌─────────────────────────────────────────────────────────────┐
│  ← Back                                       Step 3 of 6  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━░░░░░  50%           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Owner Information                                          │
│                                                             │
│  Full Legal Name                                            │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Jane Doe                                           │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  Home Address                                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  456 Oak Ave                                        │    │
│  │  Philadelphia, PA 19103                             │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  Business Address                                           │
│  ☐ Same as home address                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  789 Market St, Suite 200                           │    │
│  │  Philadelphia, PA 19103                             │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  Business Start Date                                        │
│  ○ Starting now                                             │
│  ○ Already started:  [  📅  ]                              │
│  ○ Future date:  [  📅  ]                                  │
│                                                             │
│                                 [← Back]  [Continue →]      │
└─────────────────────────────────────────────────────────────┘
```

### 2.4 Registered Agent / Office (`/register/agent`)

```
┌─────────────────────────────────────────────────────────────┐
│  ← Back                                       Step 4 of 6  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━░░  67%          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Registered Agent / Office                                  │
│                                                             │
│  Your LLC needs a registered agent (MA) or registered       │
│  office (PA) to receive legal documents on your behalf.     │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  ★ Use UMD's Registered Agent Service               │    │
│  │                                                     │    │
│  │  • Professional registered agent in [state]         │    │
│  │  • Included with your Business plan ($79/mo)        │    │
│  │  • Mail forwarding & document scanning              │    │
│  │  • Compliance alerts                                │    │
│  │                                                     │    │
│  │  ● Select this option                               │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Use My Own Registered Agent                        │    │
│  │                                                     │    │
│  │  Agent Name:  ___________________________________   │    │
│  │  Street Address:  _______________________________   │    │
│  │  City:  __________  State: [MA/PA]  Zip: _______   │    │
│  │                                                     │    │
│  │  ○ Select this option                               │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│                                 [← Back]  [Continue →]      │
└─────────────────────────────────────────────────────────────┘
```

### 2.5 Review (`/register/review`)

```
┌─────────────────────────────────────────────────────────────┐
│  ← Back                                       Step 5 of 6  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━░░  83%     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Review Your Filing                                         │
│                                                             │
│  Please review all information carefully. Once submitted,   │
│  changes may require an amendment filing.                   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Filing Details                            [Edit ✏️]│    │
│  │  State: Pennsylvania                                │    │
│  │  Entity: LLC                                        │    │
│  │  Name: Acme Solutions LLC                           │    │
│  │  Purpose: Technology consulting and software...     │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Structure                                 [Edit ✏️]│    │
│  │  Management: Member-Managed                         │    │
│  │  Members: John Smith (100%)                         │    │
│  │  Organizer: John Smith                              │    │
│  │  Effective Date: Upon filing                        │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Registered Office                         [Edit ✏️]│    │
│  │  UMD Registered Agent Service                       │    │
│  │  123 Business Ave, Philadelphia, PA 19103           │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Cost Summary                                       │    │
│  │  State filing fee (PA LLC):         $125.00         │    │
│  │  UMD service fee:                     $0.00         │    │
│  │  (included in Business plan)                        │    │
│  │  ──────────────────────────────────────────         │    │
│  │  Total due today:                   $125.00         │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  ☐ I confirm all information is accurate and I authorize    │
│    UMD to file on my behalf.                                │
│                                                             │
│                                 [← Back]  [Submit & Pay →]  │
└─────────────────────────────────────────────────────────────┘
```

### 2.6 Payment (`/register/payment`)

```
┌─────────────────────────────────────────────────────────────┐
│                                                Step 6 of 6  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━░  95% │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Payment                                                    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │         Stripe Payment Element              │    │    │
│  │  │                                             │    │    │
│  │  │  Card Number                                │    │    │
│  │  │  ┌──────────────────────────────────────┐   │    │    │
│  │  │  │  4242 4242 4242 4242                 │   │    │    │
│  │  │  └──────────────────────────────────────┘   │    │    │
│  │  │                                             │    │    │
│  │  │  Exp        CVC         ZIP                 │    │    │
│  │  │  ┌────────┐ ┌────────┐ ┌────────┐          │    │    │
│  │  │  │ 12/28  │ │  123   │ │ 19103  │          │    │    │
│  │  │  └────────┘ └────────┘ └────────┘          │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  │                                                     │    │
│  │  Total: $125.00                                     │    │
│  │                                                     │    │
│  │              [Pay $125.00 & Submit Filing →]         │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  🔒 Secured by Stripe. UMD never stores your card details. │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.7 Filing Status (`/register/status`)

```
┌─────────────────────────────────────────────────────────────┐
│  ← Dashboard                                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🎉 Filing Submitted!                                       │
│                                                             │
│  Acme Solutions LLC — Pennsylvania                          │
│  Submitted: May 6, 2026 at 2:34 PM                         │
│  Status: ● Processing                                       │
│  Confirmation #: PA-2026-0506-78432                         │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Filing Progress                                    │    │
│  │                                                     │    │
│  │  ✅ Payment received                                │    │
│  │  ✅ Filing submitted to PA Dept. of State           │    │
│  │  🔄 State review in progress (est. 1-3 days)       │    │
│  │  ○  Certificate of Organization issued              │    │
│  │  ○  Documents available for download                │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  Next Steps (do these while you wait)                       │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  ☐ Apply for EIN (Federal Tax ID)      [Start →]   │    │
│  │  ☐ Open a business bank account        [Guide →]   │    │
│  │  ☐ Register with PA Revenue Dept       [Start →]   │    │
│  │  ☐ Get business insurance              [Guide →]   │    │
│  │  ☐ Set up your business website        [Build →]   │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                             │
│  📧 We'll email you at john@example.com when your          │
│     filing is approved.                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Component Architecture

```
src/
├── app/
│   └── register/
│       ├── page.tsx                    # State & entity type selection
│       ├── info/page.tsx              # Business info form
│       ├── details/page.tsx           # Entity-specific details
│       ├── agent/page.tsx             # Registered agent selection
│       ├── review/page.tsx            # Review summary
│       ├── payment/page.tsx           # Stripe payment
│       ├── status/page.tsx            # Filing status tracker
│       └── layout.tsx                 # Shared wizard layout with progress bar
│
├── components/
│   └── registration/
│       ├── state-selector.tsx         # State comparison cards
│       ├── entity-type-selector.tsx   # LLC vs sole prop cards
│       ├── name-checker.tsx           # Real-time name availability
│       ├── member-manager.tsx         # Add/remove LLC members
│       ├── agent-selector.tsx         # RA service vs own agent
│       ├── review-section.tsx         # Collapsible review card
│       ├── filing-status.tsx          # Status timeline
│       ├── cost-summary.tsx           # Running cost calculation
│       └── progress-bar.tsx           # Step progress indicator
│
├── hooks/
│   └── registration/
│       ├── use-registration-form.ts   # Form state management
│       ├── use-name-check.ts          # Debounced name availability
│       ├── use-auto-save.ts           # Auto-save to localStorage + API
│       └── use-filing-status.ts       # Polling for filing updates
│
└── lib/
    └── registration/
        ├── schemas.ts                 # Zod validation schemas
        ├── types.ts                   # TypeScript types
        └── constants.ts               # State fees, entity types, etc.
```

---

## 4. Data Collection Points (Analytics & Feedback)

Every interaction is tracked for product improvement:

| Event | Data Captured | Purpose |
|-------|--------------|---------|
| `state_selected` | state, timestamp, time_on_page | Which states are popular |
| `entity_type_selected` | type, changed_from, ai_recommended | Are users following AI advice? |
| `name_search` | query, available (bool), attempt_number | Name availability pain points |
| `form_field_focus` | field_name, step, timestamp | Where users hesitate |
| `form_field_blur` | field_name, time_spent, value_length | Time per field |
| `form_field_error` | field_name, error_type, value_sanitized | Validation friction |
| `step_completed` | step_number, time_on_step, fields_changed | Step-level completion |
| `step_abandoned` | step_number, last_field_focused, time_on_step | Where users drop off |
| `ai_recommendation_clicked` | feature, context | AI feature engagement |
| `auto_save_triggered` | step, fields_saved | Draft persistence |
| `review_edit_clicked` | section_name | What users change at review |
| `payment_initiated` | amount, entity_type, state | Conversion tracking |
| `payment_completed` | amount, payment_method_type | Revenue tracking |
| `filing_status_checked` | filing_id, times_checked, time_since_submit | User anxiety levels |
| `post_filing_task_clicked` | task_name | Post-filing engagement |

---

## 5. Responsive Design Notes

- Mobile-first layout — wizard works on phone screens
- Cards stack vertically on small screens
- Progress bar collapses to "Step 3/6" text on mobile
- Form fields are full-width on mobile, 2-column on desktop
- Sticky bottom nav with Back/Continue buttons on mobile

---

## 6. Accessibility

- All form fields have proper labels and `aria-describedby` for help text
- Error messages announced via `aria-live="polite"`
- Keyboard navigation through all wizard steps
- Color contrast meets WCAG 2.1 AA
- Focus management on step transitions
