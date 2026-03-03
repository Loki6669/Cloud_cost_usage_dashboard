# CLAUDE.md — Cloud Cost Usage Dashboard

This file provides context for AI assistants (Claude, Copilot, etc.) working in this repository. It describes the project purpose, planned architecture, development conventions, and workflow guidance.

---

## Project Overview

**Cloud_cost_usage_dashboard** is a web-based dashboard for monitoring, visualizing, and analyzing cloud infrastructure costs across one or more cloud providers (AWS, Azure, GCP). The goal is to give engineering and finance teams a unified view of cloud spending with breakdowns by service, team, environment, and time period.

### Core Features (Planned)

- Multi-cloud cost aggregation (AWS Cost Explorer, Azure Cost Management, GCP Billing)
- Time-series cost charts (daily, weekly, monthly)
- Cost breakdown by service, tag, account, and region
- Budget alerts and anomaly detection
- Forecasting / trend analysis
- Exportable reports (CSV, PDF)
- Role-based access control (RBAC)

---

## Repository State

> **Status: Early initialization** — No source code exists yet. This file is a forward-looking guide to establish conventions before development begins.

Current contents:
```
Cloud_cost_usage_dashboard/
├── CLAUDE.md        ← this file
└── README.md        ← project title only
```

---

## Planned Architecture

### Technology Stack (Recommended)

| Layer | Technology |
|---|---|
| Frontend | React 18 + TypeScript, Vite |
| UI Components | Shadcn/UI or Ant Design |
| Charts | Recharts or Chart.js |
| State Management | Zustand or React Query (TanStack Query) |
| Backend | Python (FastAPI) or Node.js (Express/Fastify) |
| Database | PostgreSQL (cost data cache, user config) |
| Auth | JWT + OAuth2 (Google/GitHub SSO) |
| Cloud SDKs | boto3 (AWS), azure-mgmt-costmanagement, google-cloud-billing |
| Containerization | Docker + docker-compose |
| CI/CD | GitHub Actions |

### Directory Layout (Target)

```
Cloud_cost_usage_dashboard/
├── frontend/                  # React TypeScript SPA
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   │   ├── charts/        # Chart wrappers (CostBarChart, TrendLine, etc.)
│   │   │   ├── layout/        # Shell, Sidebar, Header, etc.
│   │   │   └── ui/            # Generic primitives (Button, Card, etc.)
│   │   ├── pages/             # Route-level components (Dashboard, Reports, etc.)
│   │   ├── hooks/             # Custom React hooks (useCostData, useFilters, etc.)
│   │   ├── services/          # API client functions (api.ts, cloudProviders.ts)
│   │   ├── store/             # Global state (filters, date ranges, user prefs)
│   │   ├── types/             # Shared TypeScript types/interfaces
│   │   └── utils/             # Formatting helpers (currency, dates, percentages)
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── backend/                   # API server
│   ├── app/
│   │   ├── api/               # Route handlers / controllers
│   │   │   └── v1/            # Versioned API routes
│   │   ├── core/              # Config, settings, security
│   │   ├── models/            # Database ORM models
│   │   ├── schemas/           # Pydantic / Zod request+response schemas
│   │   ├── services/          # Business logic (cost aggregation, caching)
│   │   └── providers/         # Cloud provider SDK wrappers
│   │       ├── aws.py
│   │       ├── azure.py
│   │       └── gcp.py
│   ├── tests/
│   ├── requirements.txt
│   └── pyproject.toml
│
├── docker-compose.yml
├── .env.example
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── CLAUDE.md
└── README.md
```

---

## Development Workflows

### Local Setup (Once Implemented)

```bash
# Clone and enter the project
git clone <repo-url>
cd Cloud_cost_usage_dashboard

# Copy environment variables
cp .env.example .env
# Edit .env with your cloud credentials and database config

# Start all services
docker-compose up -d

# OR run individually:
# Backend
cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload

# Frontend
cd frontend && npm install && npm run dev
```

### Running Tests

```bash
# Backend tests
cd backend && pytest --cov=app tests/

# Frontend tests
cd frontend && npm run test

# Linting
cd frontend && npm run lint
cd backend && ruff check app/
```

### Common Commands

```bash
# Format code
cd frontend && npm run format      # Prettier
cd backend && ruff format app/     # Python formatter

# Type checking
cd frontend && npm run typecheck   # tsc --noEmit
cd backend && mypy app/            # Python type checking

# Database migrations (once ORM is set up)
cd backend && alembic upgrade head
cd backend && alembic revision --autogenerate -m "description"
```

---

## Code Conventions

### General

- Prefer explicit over clever code; readability is paramount
- Keep functions and components small and focused (single responsibility)
- Never commit secrets, API keys, or credentials — use `.env` files
- All environment variables must be documented in `.env.example` with placeholder values

### TypeScript / Frontend

- Use TypeScript strict mode (`"strict": true` in tsconfig)
- Name components and files in PascalCase: `CostBarChart.tsx`, `DashboardPage.tsx`
- Name hooks with `use` prefix: `useCostData`, `useFilters`
- Name utility functions in camelCase: `formatCurrency`, `parseISODate`
- Co-locate component styles, types, and tests with the component file
- Prefer named exports over default exports for components (except pages)
- Avoid `any` — define proper types in `src/types/`
- Use React Query for all server state; use Zustand only for pure client-side state

### Python / Backend

- Follow PEP 8; use `ruff` for linting and formatting
- Use type hints everywhere (`from __future__ import annotations`)
- Name files and modules in snake_case: `cost_aggregation.py`, `aws_provider.py`
- Name classes in PascalCase: `CostRecord`, `AWSProvider`
- Use Pydantic models for all request/response validation
- Keep route handlers thin — delegate logic to service layer
- Never call cloud provider APIs directly from route handlers; always use the provider abstraction layer

### API Design

- All API routes are prefixed `/api/v1/`
- Use nouns for resources: `/api/v1/costs`, `/api/v1/budgets`, `/api/v1/providers`
- Use standard HTTP verbs: GET (read), POST (create), PUT/PATCH (update), DELETE (delete)
- Return consistent JSON envelopes:
  ```json
  { "data": {...}, "meta": { "page": 1, "total": 100 } }
  ```
- Errors follow RFC 7807 Problem Details format:
  ```json
  { "type": "...", "title": "Not Found", "status": 404, "detail": "..." }
  ```

### Git Conventions

- Branch naming: `feature/<short-description>`, `fix/<issue-id>-description`, `chore/<task>`
- Commit messages follow Conventional Commits:
  - `feat: add AWS Cost Explorer integration`
  - `fix: correct currency rounding in cost aggregation`
  - `chore: update dependencies`
  - `docs: add setup instructions to README`
  - `test: add unit tests for cost aggregation service`
- Keep commits atomic — one logical change per commit
- Open a PR for every change; no direct commits to `main`/`master`

---

## Environment Variables

Document all required environment variables here as the project grows. The `.env.example` file must stay up to date.

### Expected Variables (Planned)

```bash
# App
APP_ENV=development          # development | staging | production
SECRET_KEY=changeme          # JWT signing secret

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/cloud_costs

# AWS
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=us-east-1

# Azure
AZURE_SUBSCRIPTION_ID=
AZURE_CLIENT_ID=
AZURE_CLIENT_SECRET=
AZURE_TENANT_ID=

# GCP
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
GCP_PROJECT_ID=

# Frontend
VITE_API_BASE_URL=http://localhost:8000
```

---

## Key Domain Concepts

Understanding these terms is important when reading or writing code:

| Term | Meaning |
|---|---|
| **Cost record** | A single billing line item from a cloud provider (service, amount, date, tags) |
| **Provider** | A cloud platform: AWS, Azure, or GCP |
| **Account / Subscription / Project** | Provider-specific grouping of resources (AWS account, Azure subscription, GCP project) |
| **Tag** | A key-value label attached to cloud resources, used for cost allocation |
| **Granularity** | Time resolution of cost data: `DAILY`, `MONTHLY` |
| **Budget** | A user-defined spending limit that triggers alerts when approached/exceeded |
| **Anomaly** | An unusual spike or drop in costs, detected by statistical comparison |
| **Forecast** | Predicted future spend based on historical trends |

---

## Testing Strategy

- **Unit tests**: Test pure functions, service logic, data transformations in isolation
- **Integration tests**: Test API endpoints against a test database
- **Component tests**: Test React components with React Testing Library
- **E2E tests (optional)**: Playwright for critical user flows (login, view dashboard, export report)
- Aim for >80% coverage on backend service and provider layers
- Mock all external cloud API calls in tests using fixtures/stubs

---

## Security Considerations

- Never log raw cloud credentials or API keys
- Rotate credentials regularly; use IAM roles with least-privilege for cloud access
- All API endpoints must require authentication except `/health` and `/docs`
- Validate and sanitize all user inputs before passing to cloud SDKs or queries
- Use parameterized queries for all database operations (no raw SQL string interpolation)
- CORS must be explicitly configured; do not use wildcard (`*`) in production

---

## For AI Assistants

When contributing to this repository, follow these guidelines:

1. **Read before writing** — Always read existing files before editing them
2. **Stay minimal** — Only change what is necessary; do not refactor unrelated code
3. **Match existing style** — Follow the conventions in whichever language/framework is already in use
4. **Test your changes** — Run the relevant test suite and fix failures before committing
5. **Update this file** — If you add a major component, new env variable, or change a workflow, update CLAUDE.md accordingly
6. **No hardcoded secrets** — Use environment variables; update `.env.example` if you add new ones
7. **Commit on the right branch** — Always check `git branch` before committing; the active branch should match the task's designated branch
8. **Keep commits focused** — One logical change per commit with a Conventional Commits message
