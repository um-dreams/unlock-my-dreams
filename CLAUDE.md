# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Unlock My Dreams (UMD)** — AI-first SaaS (AIaaS) that helps entrepreneurs go from business idea to registered LLC with a live website. Part of the [UM Dreams](https://github.com/um-dreams) organization.

Three core products: AI Business Planner & Checklist, AI Website Builder (full multi-page), and LLC Registration (partner API first, direct filing later).

## Tech Stack

- **Frontend**: Next.js (app router, server components) + Tailwind + Shadcn/ui
- **Backend**: Python (FastAPI) + Celery + Redis
- **Database**: PostgreSQL
- **AI**: Multi-model routing — Claude for reasoning/planning, GPT for content generation
- **Payments**: Stripe (tiered subscriptions: Free / Pro $29 / Business $79)
- **Infrastructure**: Vercel (frontend), AWS (backend, RDS, ElastiCache, S3)

## Repository Structure

- `specs/` — Business plan, PRDs, and feature specifications

## Git Strategy

### Branching Model
```
feat/* → dev → staging → main (production)
```
- **feat/***: All new work starts here. Branch from `dev`, name as `feat/<short-description>`.
- **dev**: Integration branch. All feature branches merge here first.
- **staging**: Pre-production. Merges from `dev` for QA/testing before production.
- **main**: Production. Only promoted from `staging` after verification.

### Commit & Push Rules
- Commit and push after every completed task — do not batch multiple tasks into one commit.
- Do NOT add Claude or any AI co-author lines to commits.
- Write concise commit messages focused on the "why", not the "what".

### PR Flow
- Feature PRs target `dev`.
- Promotion PRs: `dev → staging`, `staging → main`.

## Key Specs

- `specs/BUSINESS_PLAN.md` — Full business plan with pricing, MVP timeline, competitive analysis
