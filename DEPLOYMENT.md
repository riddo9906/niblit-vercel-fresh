# Niblit — Vercel Deployment Guide

This guide explains how to deploy Niblit to [Vercel](https://vercel.com) as a serverless web application.

---

## Prerequisites

- A [Vercel account](https://vercel.com/signup) (free tier is sufficient)
- The Niblit repository forked or accessible on GitHub
- A [Hugging Face](https://huggingface.co) account with an API token

---

## Step 1 — Set Up Environment Variables

Niblit requires the following environment variables to run in production.

| Variable | Required | Description |
|---|---|---|
| `HF_TOKEN` | **Yes** | Hugging Face API token for LLM inference |
| `NIBLIT_API_KEY` | No | Optional API key that protects `/chat` and `/memory` endpoints |

Copy `.env.example` to `.env` for local development:

```bash
cp .env.example .env
# Edit .env and fill in your values
```

On Vercel, set these variables via **Project → Settings → Environment Variables**.

---

## Step 2 — Project Layout for Vercel

Niblit is deployed as a **Python serverless function** — there is no frontend build step.

Key files Vercel uses:

| File | Purpose |
|---|---|
| `vercel.json` | Declares routes and function settings |
| `app.py` | The Flask WSGI application — handles `/`, `/health`, `/ping`, `/chat`, `/memory` |
| `api/boot.py` | Serverless entry point for `/api/boot` |
| `api/suggest.py` | Serverless entry point for `/api/suggest` |
| `api/threads.py` | Serverless entry point for `/api/threads` |
| `api/commands.py` | Serverless entry point for `/api/commands` |
| `api/status.py` | Serverless entry point for `/api/status` |
| `api/search.py` | Serverless entry point for `/api/search` |
| `requirements.txt` | Python dependencies — auto-installed by `@vercel/python` during build |
| `public/index.html` | Static landing page served before the Flask function fully loads |

The `@vercel/python` builder reads `requirements.txt` automatically; **no manual `buildCommand` is required**. Root routes (`/`, `/health`, `/ping`, `/chat`, `/memory`) are handled by `app.py`. Each `/api/*` route is served by its own dedicated serverless function in the `api/` directory, all of which import the shared Flask app from `app.py`.

---

## Step 3 — Connect Repository to Vercel

1. Log in to the [Vercel Dashboard](https://vercel.com/dashboard).
2. Click **Add New Project**.
3. Import your GitHub repository (your fork of Niblit, e.g. `your-username/Niblit`).
4. Vercel will detect the `vercel.json` configuration automatically.
5. Before clicking **Deploy**, add the required environment variables (see Step 1).
6. Click **Deploy**.

---

## Step 4 — Verify the Deployment

Once deployed, visit your Vercel URL and check the following endpoints:

| Endpoint | Method | Expected Response |
|---|---|---|
| `/` | GET | Niblit Dashboard UI |
| `/health` | GET | `{"status": "ok", "service": "niblit"}` |
| `/ping` | GET | `{"status": "ok", "personality": {...}}` |
| `/chat` | POST | `{"reply": "..."}` |
| `/memory` | GET | `{"facts": [...]}` |
| `/api/boot` | GET | `{"messages": [...], "ready": true}` |
| `/api/suggest?q=<term>` | GET | `{"suggestions": [...]}` |
| `/api/threads` | GET | `{"threads": [...]}` |
| `/api/commands` | GET | `{"commands": [...], "count": N}` |
| `/api/status` | GET | `{"online": true, "service": "niblit"}` |
| `/api/search?q=<term>` | GET | `{"query": "...", "result": "..."}` |

### Quick health check

```bash
# Lightweight liveness probe (no AI init needed)
curl https://<your-vercel-url>/health

# Full status including personality data
curl https://<your-vercel-url>/ping
```

---

## Step 5 — Cold Starts

Vercel serverless functions may experience a cold start on the first request after a period of inactivity. Niblit handles this gracefully:

- `NiblitCore` is loaded lazily on first request, not at import time.
- If `NiblitCore` fails to initialise, endpoints return structured error responses instead of crashing.
- The `/ping` endpoint is safe to use as a warm-up probe.

---

## Troubleshooting

### `Missing public directory` build error

This error occurs when `vercel.json` includes a top-level `buildCommand` that does not produce any static output. For a pure Python serverless deployment, **do not add a `buildCommand`** — the `@vercel/python` builder handles dependency installation automatically. Remove `buildCommand` from `vercel.json` to resolve this error.

### `{"error": "core failed"}` on `/chat`

The `NiblitCore` failed to initialise. Check:
- That `HF_TOKEN` is set correctly in the Vercel environment variables.
- Vercel function logs under **Project → Deployments → Functions → Logs**.

### `{"error": "unauthorized"}` on `/chat` or `/memory`

`NIBLIT_API_KEY` is set but the request did not include the `X-API-Key` header.
Either unset the variable or add the header to your request:

```bash
curl -H "X-API-Key: <your-key>" https://<your-vercel-url>/chat \
  -X POST -H "Content-Type: application/json" \
  -d '{"text": "hello"}'
```

### `{"error": "rate limit reached"}`

The simple in-memory rate limiter allows 10 requests per 60 seconds per IP. Reduce request frequency or increase `RATE_LIMIT` / `RATE_WINDOW` in `app.py` if needed.

### Build size exceeds 50 MB

Ensure unnecessary large files are excluded via `.vercelignore`. The project already excludes `*_full.py`, database files, and logs by default.

---

## Local Development

```bash
pip install -r requirements.txt
cp .env.example .env   # fill in values
python app.py
# Open http://localhost:5000
```

To simulate the Vercel environment locally, install the Vercel CLI:

```bash
npm i -g vercel
vercel dev
```
