# Unlock My Dreams (UMD) — Business Plan

## 1. Vision

An AI-first SaaS (AIaaS) that takes someone from "I have a business idea" to "I have a registered LLC with a live website" in a single platform.

## 2. Problem

Starting a business today requires juggling multiple disconnected services:
- Research what's needed (scattered blog posts, Reddit threads)
- Build a website (Squarespace, Wix — manual setup, no business context)
- Register the company (LegalZoom, Stripe Atlas — separate flow, expensive)
- Track progress (spreadsheets, Notion — no structure)

Each step is a dropout point. Most aspiring entrepreneurs stall before they ever launch.

## 3. Solution

UMD is a single AI-guided platform with three core products:

### 3.1 AI Business Planner & Checklist
- User describes their business idea in plain language
- AI generates a structured business plan (market, revenue model, competitive landscape)
- Converts the plan into an actionable step-by-step checklist
- Checklist adapts based on business type, state, and industry
- Progress tracking with AI nudges to keep users moving

### 3.2 AI Website Builder
- Full multi-page site builder (landing, about, services, blog, store)
- AI generates all initial content from the business plan context
- Drag-and-drop editing with template system
- Custom domain support
- Built-in SEO optimization from AI
- Blog and basic e-commerce (product listings, Stripe checkout)

### 3.3 LLC Registration
- AI pre-fills all formation documents from the business plan
- Registered agent service included
- **Phase 1**: Partner API integration (evaluate Stripe Atlas, Northwest, Incfile APIs)
- **Phase 2**: Direct state filing for higher margins
- EIN application assistance
- Operating agreement generation
- Compliance calendar (annual reports, franchise tax reminders)

## 4. Target Market

### Primary
- First-time entrepreneurs in the US
- Side-hustle creators going legit
- Freelancers/solopreneurs formalizing their business

### Secondary (future)
- Small teams (2-5 people) launching together
- International founders forming US LLCs
- Existing businesses needing a website refresh

### Geography
- **Launch**: US-only (LLC formation across all 50 states)
- **Expand**: Canada, UK, EU entity types

## 5. Pricing Model — Tiered Subscription

| Tier | Price/mo | Features |
|------|----------|----------|
| **Starter** | Free | AI business plan, basic checklist (limited generations) |
| **Pro** | $29/mo | Full checklist, AI website builder (1 site), custom domain |
| **Business** | $79/mo | Everything in Pro + LLC registration*, compliance calendar, priority support |

*LLC registration includes a one-time state filing fee passed through at cost (varies by state, typically $50–$500).

### Revenue Streams
1. Monthly subscriptions (primary)
2. State filing fee pass-through (at cost or small markup)
3. Annual registered agent fee ($100–$150/yr, bundled into Business tier)
4. Premium templates and add-ons (future)

## 6. Tech Stack

### Frontend
- **Next.js** (React) — app router, server components
- **Tailwind CSS** — styling
- **Shadcn/ui** — component library
- Drag-and-drop: dnd-kit or similar for website builder

### Backend
- **Python (FastAPI)** — API server, business logic
- **Celery + Redis** — background jobs (LLC filing, AI generation)
- **PostgreSQL** — primary database
- **S3** — asset storage (user uploads, generated sites)

### AI Layer
- **Multi-model routing** — pick the best model per task:
  - Business plan generation & reasoning: Claude (Anthropic)
  - Content writing (website copy, blog posts): GPT (OpenAI)
  - Quick classifications & extractions: smaller/faster models
- **LangChain or custom orchestration** for prompt pipelines

### Infrastructure
- **Vercel** — Next.js hosting
- **AWS** — FastAPI (ECS/Lambda), PostgreSQL (RDS), Redis (ElastiCache), S3
- **Stripe** — payments, subscriptions
- **Auth**: NextAuth.js or Clerk

## 7. MVP Scope (4–6 Week Target)

### Week 1–2: Foundation
- [ ] Project scaffolding (Next.js + FastAPI monorepo)
- [ ] Auth system (sign up, login, OAuth)
- [ ] Database schema design
- [ ] Stripe subscription integration
- [ ] Basic dashboard UI

### Week 3–4: Core AI Features
- [ ] AI business plan generator (conversational flow)
- [ ] Checklist engine (generated from business plan, editable)
- [ ] Website builder v1 (template selection, AI content fill, page editor)
- [ ] Site preview and publish flow

### Week 5–6: LLC + Polish
- [ ] LLC registration flow (partner API integration)
- [ ] Document generation (operating agreement, EIN guidance)
- [ ] Compliance calendar
- [ ] Landing page / marketing site
- [ ] Beta testing and bug fixes

### Out of MVP (Post-Launch)
- E-commerce / store pages in website builder
- Blog editor with AI writing assistant
- Direct state filing (bypass partner API)
- Team accounts and collaboration
- International entity formation
- Mobile app

## 8. Competitive Landscape

| Competitor | What They Do | UMD Differentiator |
|-----------|-------------|-------------------|
| **Stripe Atlas** | LLC + bank account | No website, no business planning, $500 one-time |
| **LegalZoom** | Legal entity formation | Expensive, no AI, no website builder |
| **Squarespace/Wix** | Website builder | No business planning, no LLC formation |
| **ChatGPT/Claude** | General AI assistant | No execution — just generates text, user has to do everything |
| **Notion AI** | AI-enhanced docs | Not purpose-built for business launch |

**UMD's moat**: The only platform where AI understands your entire business context and uses it across planning, website, and legal formation — one continuous flow, not three separate products.

## 9. Key Metrics (Post-Launch)

- **Activation rate**: % of signups who complete a business plan
- **Conversion**: Free → Pro → Business tier upgrade rates
- **LLC completion rate**: % of Business tier users who complete formation
- **Site publish rate**: % of Pro+ users who publish a website
- **MRR**: Monthly recurring revenue
- **Churn**: Monthly subscriber churn rate
- **NPS**: Net promoter score

## 10. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| LLC partner API unreliable/expensive | Blocks core feature | Evaluate multiple partners, build abstraction layer |
| AI generates bad legal/business advice | Liability, trust loss | Clear disclaimers, human review option, limit scope to formation docs |
| Website builder too complex for MVP | Delays launch | Ship with templates + AI content only, add drag-and-drop in v2 |
| Low conversion from free tier | Revenue miss | Generous free tier to build trust, clear upgrade triggers |
| State filing rules change | Formation failures | Compliance monitoring, partner API handles updates |
