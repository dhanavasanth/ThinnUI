# ThinnUI AI MVP Implementation Plan

## Scope

### In scope (v1.0)

- 21st.dev component crawling and indexing
- semantic retrieval over component embeddings
- prompt-to-sections parser
- layout composition for landing pages
- React + Tailwind code generation
- ZIP export of generated project
- basic email authentication
- dark/light mode toggle

### Out of scope (v1.0)

- drag-and-drop visual editing
- multi-registry ingestion
- enterprise private registry support
- custom fine-tuned model training
- Figma integration
- mobile app generation

## Functional requirements

| ID | Requirement | Priority |
| --- | --- | --- |
| FR1 | Crawl and store 21st.dev components | High |
| FR2 | Generate embeddings for components | High |
| FR3 | Semantic search using vector DB | High |
| FR4 | Prompt → section parser | High |
| FR5 | Layout composer | High |
| FR6 | Code export as ZIP | High |
| FR7 | Dark/light mode toggle | Medium |
| FR8 | Basic email authentication | Medium |

## Non-functional requirements

- Generation time under 10 seconds
- Support 500 concurrent users
- 99% availability target
- Weekly registry refresh
- Component code sanitization before generation

## Suggested service decomposition

### 1) Registry Ingestion Service

Responsibilities:
- crawl 21st.dev component pages
- extract metadata (name, URL, description, tags, props)
- persist raw source in object storage
- publish normalized component documents

Storage:
- MongoDB: structured metadata
- object storage: raw source snapshots

### 2) Embedding & Indexing Service

Responsibilities:
- convert component metadata + docs into embeddings
- upsert vectors into Qdrant
- maintain index versioning for refreshes

### 3) Prompt Understanding Service

Responsibilities:
- convert prompt into section list + style constraints
- normalize expected landing-page schema

Output example:

```json
{
  "theme": "dark",
  "sections": ["hero", "features", "pricing", "testimonials", "footer"]
}
```

### 4) Retrieval & Ranking Service

Responsibilities:
- query Qdrant per section
- return top-k candidate components
- rank by semantic relevance + compatibility filters

### 5) Layout & Code Generation Service

Responsibilities:
- select compatible components by section
- enforce consistent dark/light theme
- generate Next.js app structure and import graph
- emit install/run instructions

### 6) Export Service

Responsibilities:
- build downloadable ZIP artifacts
- track artifact IDs and expiry

## Data model sketch

### Component metadata (MongoDB)

```json
{
  "componentId": "21st-hero-001",
  "source": "21st.dev",
  "name": "Gradient SaaS Hero",
  "installUrl": "https://21st.dev/...",
  "description": "Dark hero with CTA",
  "props": [{"name": "title", "type": "string"}],
  "tags": ["hero", "saas", "dark"],
  "rawSourcePath": "s3://.../21st-hero-001.tsx",
  "updatedAt": "2026-02-01T00:00:00Z"
}
```

## Milestone plan

### Milestone 1: Registry + embeddings
- crawler MVP for 21st.dev subset
- metadata persistence
- vector index population

### Milestone 2: Prompt parsing + retrieval
- section parser
- per-section semantic search
- top-3 candidate ranking

### Milestone 3: Layout + code generation
- deterministic page skeleton
- component stitching with valid imports
- runnable project output validation

### Milestone 4: Export + auth + polish
- ZIP download endpoint
- basic email login
- dark/light toggle
- performance pass (<10 sec target)

## Acceptance criteria

- Prompt-to-export flow succeeds end-to-end.
- At least one generated project boots via `npm install && npm run dev`.
- Hallucinated import rate remains below 5% on test prompts.
- Generation latency average remains below 8 seconds for MVP benchmark prompts.
