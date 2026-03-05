# Unlock My Dreams — Architecture Documentation

Visual documentation of UMD's system architecture, user flows, data model, and AI routing. All diagrams use [Mermaid](https://mermaid.js.org/) syntax and render on GitHub natively.

---

## 1. System Architecture

High-level view of all components, boundaries, and external services.

```mermaid
graph TB
    subgraph Client["Browser"]
        UI["Next.js App<br/>(React + Tailwind + Shadcn/ui)"]
    end

    subgraph Vercel["Vercel"]
        SSR["Next.js Server<br/>(App Router, Server Components)"]
        AUTH["Auth Provider<br/>(NextAuth.js / Clerk)"]
    end

    subgraph AWS["AWS"]
        subgraph Compute["Compute"]
            API["FastAPI<br/>(ECS / Lambda)"]
            WORKER["Celery Workers<br/>(ECS)"]
        end

        subgraph Data["Data Stores"]
            PG["PostgreSQL<br/>(RDS)"]
            REDIS["Redis<br/>(ElastiCache)"]
            S3["S3<br/>(Uploads, Generated Sites)"]
        end
    end

    subgraph AI["AI Layer"]
        ROUTER["AI Router /<br/>Orchestration"]
        CLAUDE["Claude API<br/>(Anthropic)"]
        GPT["GPT API<br/>(OpenAI)"]
        SMALL["Smaller Models<br/>(Classification)"]
    end

    subgraph External["External Services"]
        STRIPE["Stripe<br/>(Subscriptions + Payments)"]
        LLC_API["LLC Partner API<br/>(Stripe Atlas / Northwest / Incfile)"]
    end

    UI -->|HTTPS| SSR
    SSR -->|REST API| API
    SSR --> AUTH
    API --> PG
    API --> REDIS
    API --> S3
    API -->|Enqueue Jobs| REDIS
    REDIS -->|Consume Jobs| WORKER
    WORKER --> PG
    WORKER --> S3
    API --> ROUTER
    WORKER --> ROUTER
    ROUTER --> CLAUDE
    ROUTER --> GPT
    ROUTER --> SMALL
    API --> STRIPE
    API --> LLC_API
```

---

## 2. User Journey Flow

End-to-end user experience across all three products with tier gating.

```mermaid
flowchart TD
    START([User Visits UMD]) --> SIGNUP[Sign Up / Login]
    SIGNUP --> DASHBOARD[Dashboard]

    DASHBOARD --> IDEA[Describe Business Idea]
    IDEA --> AI_PLAN["AI Generates Business Plan<br/>(Claude)"]
    AI_PLAN --> REVIEW[Review & Edit Plan]

    REVIEW --> CHECKLIST["AI Generates Checklist<br/>from Plan"]
    CHECKLIST --> TRACK[Track Progress<br/>with AI Nudges]

    REVIEW --> GATE_PRO{Pro Tier?}
    GATE_PRO -- No --> UPGRADE_PRO[Upgrade Prompt<br/>$29/mo]
    GATE_PRO -- Yes --> BUILDER[AI Website Builder]

    BUILDER --> TEMPLATE[Select Template]
    TEMPLATE --> AI_CONTENT["AI Fills Content<br/>from Business Plan<br/>(GPT)"]
    AI_CONTENT --> EDIT[Drag-and-Drop Edit<br/>Pages & Sections]
    EDIT --> DOMAIN[Connect Custom Domain]
    DOMAIN --> PUBLISH[Publish Site]

    REVIEW --> GATE_BIZ{Business Tier?}
    GATE_BIZ -- No --> UPGRADE_BIZ[Upgrade Prompt<br/>$79/mo]
    GATE_BIZ -- Yes --> LLC[LLC Registration]

    LLC --> PREFILL["AI Pre-fills Formation Docs<br/>from Business Plan"]
    PREFILL --> DOC_GEN["Generate Documents<br/>(Operating Agreement, EIN)"]
    DOC_GEN --> FILE["File via Partner API<br/>(State Filing Fee at Cost)"]
    FILE --> COMPLIANCE["Compliance Calendar<br/>(Annual Reports, Tax Reminders)"]

    style START fill:#4ade80,color:#000
    style PUBLISH fill:#60a5fa,color:#000
    style COMPLIANCE fill:#60a5fa,color:#000
    style UPGRADE_PRO fill:#fbbf24,color:#000
    style UPGRADE_BIZ fill:#fbbf24,color:#000
```

---

## 3. Data Model (ER Diagram)

Core entities and their relationships.

```mermaid
erDiagram
    User {
        uuid id PK
        string email
        string name
        string auth_provider
        timestamp created_at
    }

    Subscription {
        uuid id PK
        uuid user_id FK
        string tier "free | pro | business"
        string stripe_customer_id
        string stripe_subscription_id
        string status "active | canceled | past_due"
        timestamp current_period_end
    }

    BusinessPlan {
        uuid id PK
        uuid user_id FK
        string title
        text idea_description
        jsonb plan_content
        string status "draft | complete"
        timestamp created_at
        timestamp updated_at
    }

    Checklist {
        uuid id PK
        uuid business_plan_id FK
        string status "active | completed"
        timestamp created_at
    }

    ChecklistItem {
        uuid id PK
        uuid checklist_id FK
        string title
        text description
        int sort_order
        boolean completed
        timestamp completed_at
    }

    Website {
        uuid id PK
        uuid user_id FK
        uuid business_plan_id FK
        uuid template_id FK
        string name
        string subdomain
        string status "draft | published"
        timestamp published_at
    }

    Page {
        uuid id PK
        uuid website_id FK
        string title
        string slug
        string page_type "landing | about | services | blog | store"
        jsonb content
        int sort_order
    }

    Template {
        uuid id PK
        string name
        string category
        jsonb layout_config
        boolean is_premium
    }

    Domain {
        uuid id PK
        uuid website_id FK
        string domain_name
        string verification_status "pending | verified | failed"
        jsonb dns_records
    }

    LLCRegistration {
        uuid id PK
        uuid user_id FK
        uuid business_plan_id FK
        string state
        string entity_name
        string status "draft | submitted | approved | rejected"
        string partner_reference_id
        decimal filing_fee
        timestamp filed_at
    }

    Document {
        uuid id PK
        uuid llc_registration_id FK
        string doc_type "operating_agreement | ein_application | articles"
        string s3_key
        string status "draft | final"
        timestamp generated_at
    }

    ComplianceEvent {
        uuid id PK
        uuid llc_registration_id FK
        string event_type "annual_report | franchise_tax | agent_renewal"
        string title
        date due_date
        boolean completed
    }

    User ||--o| Subscription : "has"
    User ||--o{ BusinessPlan : "creates"
    BusinessPlan ||--o| Checklist : "generates"
    Checklist ||--o{ ChecklistItem : "contains"
    User ||--o{ Website : "owns"
    BusinessPlan ||--o{ Website : "informs"
    Website ||--o{ Page : "has"
    Website }o--|| Template : "uses"
    Website ||--o| Domain : "has"
    User ||--o{ LLCRegistration : "files"
    BusinessPlan ||--o| LLCRegistration : "pre-fills"
    LLCRegistration ||--o{ Document : "generates"
    LLCRegistration ||--o{ ComplianceEvent : "schedules"
```

---

## 4. AI Routing Diagram

How incoming AI tasks are classified and routed to the appropriate model.

```mermaid
flowchart LR
    REQ([AI Request]) --> ROUTER{AI Router}

    ROUTER -->|"Reasoning &<br/>Planning"| CLAUDE_TASKS
    ROUTER -->|"Content<br/>Generation"| GPT_TASKS
    ROUTER -->|"Quick<br/>Classification"| SMALL_TASKS

    subgraph CLAUDE_TASKS["Claude (Anthropic)"]
        C1[Business Plan Generation]
        C2[Checklist Creation & Adaptation]
        C3[LLC Document Reasoning]
        C4[Compliance Analysis]
    end

    subgraph GPT_TASKS["GPT (OpenAI)"]
        G1[Website Copy & Headlines]
        G2[Blog Post Generation]
        G3[SEO Meta Descriptions]
        G4[Product Descriptions]
    end

    subgraph SMALL_TASKS["Smaller / Faster Models"]
        S1[Business Type Classification]
        S2[State Requirement Extraction]
        S3[Sentiment & Intent Detection]
        S4[Content Moderation]
    end

    CLAUDE_TASKS --> CONTEXT[(Business Plan<br/>Context Store)]
    GPT_TASKS --> CONTEXT
    SMALL_TASKS --> PIPE

    subgraph PIPE["Prompt Pipeline (LangChain / Custom)"]
        P1[Context Injection]
        P2[Prompt Templates]
        P3[Output Parsing]
        P4[Quality Validation]
    end

    CONTEXT --> PIPE
    PIPE --> RESP([Response to User])

    style CLAUDE_TASKS fill:#d4a0ff,color:#000
    style GPT_TASKS fill:#a0d4ff,color:#000
    style SMALL_TASKS fill:#a0ffb8,color:#000
    style CONTEXT fill:#fff3b0,color:#000
```

---

## Diagram Rendering

These diagrams render natively on GitHub. For local viewing:

- **VS Code**: Install the [Markdown Preview Mermaid Support](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid) extension
- **CLI**: Use `mmdc` from [mermaid-cli](https://github.com/mermaid-js/mermaid-cli) to export to PNG/SVG
- **Web**: Paste into [mermaid.live](https://mermaid.live) for interactive editing
