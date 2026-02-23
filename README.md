# ThinnUI AI

ThinnUI AI is an AI-powered UI generation project that converts prompts into grounded React + Tailwind landing-page scaffolds using real component metadata.

## What is implemented now

This repository includes an MVP pipeline prototype with both CLI and HTTP interfaces:

1. Parse prompt into sections and detect theme.
2. Retrieve ranked components from a seeded local registry.
3. Compose a deterministic landing-page layout.
4. Generate Next.js-style files (`app/page.tsx`, `app/layout.tsx`, `app/globals.css`).
5. Export the result as a ZIP artifact.

## Run locally (CLI)

```bash
python -m app.main "Create a dark SaaS landing page with hero pricing testimonials" --output demo.zip
```

## Run locally (HTTP API)

```bash
python -m app.server
```

Available endpoints:

- `GET /health`
- `POST /api/generate`
- `GET /api/export/{export_id}`

Generate request example:

```json
{
  "prompt": "Create a dark SaaS landing page with hero, pricing, testimonials",
  "theme": "dark"
}
```

## Tests

```bash
pytest -q
```

## Notes

- Registry seed data lives in `app/data/components.json`.
- Retrieval currently uses token-overlap scoring and will evolve to vector search (Qdrant) in upcoming milestones.
- Product roadmap details are documented in `docs/mvp-implementation-plan.md`.
