# Ultimate Agentic Growth Platform

An end-to-end, budget-aware growth factory that blends Groq-powered reasoning, Human+AI content playbooks, and cloud Stable Diffusion storyboards. Ship cinematic content systems, social distribution, and measurement loops in minutes—not months.

## Highlight Reel

- **Visual Storyboard Factory** – Cloud Stable Diffusion (Render MCP endpoint) orbits Popcorn-style briefs with IP-Adapter consistency.
- **Human+AI Social Studio** – Human_content prompts upgraded into modular campaigns with built-in human-touch checkpoints.
- **Growth Intelligence Crew** – A lean crewAI stack that scouts prospects, architects distribution, polishes copy, and instruments feedback loops.
- **Full-stack interface** – FastAPI backend + actionable React-lite UI (served at `/app`) so teams and clients can queue jobs instantly.

## Architecture

```
├─ src/ultimate_ai_powered_digital_empire___.../
│  ├─ api/                # FastAPI application (server.py exposes app)
│  ├─ crew.py             # 7-agent crew aligned to three suites
│  ├─ config/
│  │  ├─ agents.yaml      # Growth Signal Hunter → Performance Oracle
│  │  └─ tasks.yaml       # Scan → Synthesize → Architect → Render → Deploy → Analyze
│  ├─ frontend/           # Static UI (served under /app)
│  ├─ services/           # Render MCP Stable Diffusion client
│  └─ tools/              # Cloud storyboard tool + legacy helpers
├─ Human_content          # Human+AI prompt playbooks (ideation → optimization)
├─ Popcorn                # Field notes on Popcorn + multi-frame consistency
└─ README.md              # You are here
```

## Prerequisites

- Python 3.10 – 3.13
- Optional: [uv](https://docs.astral.sh/uv/) for fast dependency installs
- Cloud GPU endpoint compatible with the provided Render MCP token
- Optional Groq account for low-cost LLM inference

## Quickstart

```bash
# 1. Install dependencies
uv pip install -e .
# or
pip install -e .

# 2. Export credentials
export RENDER_MCP_TOKEN="<rnd_...>"
export GROQ_API_KEY="your_groq_key"        # optional (falls back to OPENAI_API_KEY)
# Optional overrides
# export GROQ_MODEL="llama-3.1-70b-versatile"
# export RENDER_MCP_URL="https://mcp.render.com/mcp"

# 3. Launch the API + UI
uvicorn ultimate_ai_powered_digital_empire___multi_platform_domination_with_voice_video_cloning.api.server:app --reload

# 4. Open the command center
open http://localhost:8000/app
```

### CLI runner

```bash
python -m ultimate_ai_powered_digital_empire___multi_platform_domination_with_voice_video_cloning.main \
  --inputs '{"brand_name": "Popcorn Labs", "niche": "AI storyboard SaaS", "budget_level": "scrappy"}'
```

## API Surface

- `POST /api/storyboards` – Trigger Stable Diffusion storyboard generation. Provide `project_name`, `reference_images`, and `frames` (prompt list). Returns Render MCP job result.
- `POST /api/launch` – Queue the full agentic campaign asynchronously.
- `POST /api/launch/sync` – Run the crew synchronously and return aggregated outputs.
- `GET /api/health` – Liveness check.

## Budget Controls & Providers

- **Groq-first LLMs**: Set `GROQ_API_KEY` to route all reasoning through Groq’s OpenAI-compatible endpoint. Falls back to `OPENAI_API_KEY` if absent.
- **Stable Diffusion**: Supply `RENDER_MCP_TOKEN`. The `CloudStoryboardTool` uses the Render MCP API to hit a cloud SDXL deployment, keeping on-device compute at zero.
- **Budget Modes**: Inputs accept `budget_level` (`scrappy`, `balanced`, `premium`). Agents adapt distribution and tooling choices automatically.

## Customisation

- **Agents / tasks** – Edit `config/agents.yaml` and `config/tasks.yaml` to rewire roles or outputs.
- **Tooling** – Extend `services/` with additional providers (e.g., self-hosted ComfyUI) and register via `tools/__init__.py`.
- **Frontend** – `frontend/index.html`, `main.js`, `styles.css` are lightweight and can be swapped for a heavier SPA if needed.

## Deployment Notes

- Ready for Render, Fly.io, or Docker—`uvicorn` entrypoint expects module path `ultimate_ai_powered_digital_empire___multi_platform_domination_with_voice_video_cloning.api.server:app`.
- Keep the provided Render MCP token in a secure secret store; never commit.
- Groq model + base URL are overridable for future-proofing (`GROQ_MODEL`, `GROQ_API_BASE`).

## Roadmap Ideas

- Add async job persistence (Redis + background workers) for large batches.
- Wire analytics outputs into a Supabase dashboard or Notion export.
- Integrate optional voice/video renderers (ElevenLabs, Runway) behind premium toggles.

## Support

This stack ships with best-effort defaults but expects experimentation. For help:

- crewAI docs – https://docs.crewai.com
- Render MCP – https://render.com/
- Groq – https://console.groq.com/

Unleash it, iterate, and keep the budgets ruthless. Fortune 59-ready. Presidents approved.
