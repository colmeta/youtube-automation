"""FastAPI application powering the agentic growth platform."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import AnyHttpUrl, BaseModel, Field

from ultimate_ai_powered_digital_empire___multi_platform_domination_with_voice_video_cloning.crew import (
    UltimateAiPoweredDigitalEmpireMultiPlatformDominationWithVoiceVideoCloningCrew,
)
from ultimate_ai_powered_digital_empire___multi_platform_domination_with_voice_video_cloning.services import (
    RenderMCPClient,
    RenderMCPError,
    RenderStoryboardFrame,
    RenderStoryboardRequest,
)


class StoryboardFrameInput(BaseModel):
    prompt: str = Field(..., description="Frame prompt")
    negative_prompt: Optional[str] = Field(None, description="Optional negative prompt")
    seed: Optional[int] = None
    guidance_scale: Optional[float] = Field(None, ge=0.0, le=20.0)
    steps: Optional[int] = Field(None, ge=1, le=150)


class StoryboardGenerationRequest(BaseModel):
    project_name: str
    reference_images: List[AnyHttpUrl]
    frames: List[StoryboardFrameInput]
    cfg_scale: float = Field(5.0, ge=0.0, le=20.0)
    steps: int = Field(28, ge=1, le=150)
    width: int = Field(768, ge=256, le=1536)
    height: int = Field(1024, ge=256, le=1536)
    scheduler: str = Field("dpmpp_2m")
    seed: Optional[int] = None
    extras: Dict[str, Any] = Field(default_factory=dict)


class LaunchRequest(BaseModel):
    brand_name: Optional[str] = None
    niche: Optional[str] = None
    offer_name: Optional[str] = None
    brand_voice: Optional[str] = None
    budget_level: Optional[str] = None
    audience_profile: Optional[str] = None
    objective: str = Field(
        "Launch omni-channel growth campaign",
        description="Primary campaign objective",
    )


app = FastAPI(title="Ultimate Agentic Growth Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health() -> Dict[str, Any]:
    return {"status": "ok"}


@app.post("/api/storyboards")
async def generate_storyboards(payload: StoryboardGenerationRequest) -> Dict[str, Any]:
    client = RenderMCPClient()
    frames = [RenderStoryboardFrame(**frame.dict(exclude_none=True)) for frame in payload.frames]

    request = RenderStoryboardRequest(
        project_name=payload.project_name,
        reference_images=[str(url) for url in payload.reference_images],
        frames=frames,
        cfg_scale=payload.cfg_scale,
        steps=payload.steps,
        width=payload.width,
        height=payload.height,
        scheduler=payload.scheduler,
        seed=payload.seed,
        extras=payload.extras,
    )

    try:
        result = await client.generate_storyboard(request)
    except RenderMCPError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return {"status": "success", "result": result}


def _run_crew(payload: LaunchRequest) -> None:
    crew = UltimateAiPoweredDigitalEmpireMultiPlatformDominationWithVoiceVideoCloningCrew()
    crew.kickoff(inputs=payload.dict(exclude_none=True))


@app.post("/api/launch")
async def launch_campaign(request: LaunchRequest, background_tasks: BackgroundTasks) -> Dict[str, Any]:
    background_tasks.add_task(_run_crew, request)
    return {"status": "queued"}


@app.post("/api/launch/sync")
async def launch_campaign_sync(request: LaunchRequest) -> Dict[str, Any]:
    crew = UltimateAiPoweredDigitalEmpireMultiPlatformDominationWithVoiceVideoCloningCrew()
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, crew.kickoff, request.dict(exclude_none=True))

    outputs: List[Dict[str, Any]] = []
    for task in result:
        outputs.append(
            {
                "name": getattr(task, "name", "task"),
                "status": getattr(task, "status", "completed"),
                "output": getattr(task, "output", None),
            }
        )

    return {"status": "completed", "result": outputs}


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    return HTMLResponse("""<html><body><h1>Agentic Growth API</h1><p>Visit /app/ for UI.</p></body></html>""")


FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/app", StaticFiles(directory=FRONTEND_DIR, html=True), name="app")
