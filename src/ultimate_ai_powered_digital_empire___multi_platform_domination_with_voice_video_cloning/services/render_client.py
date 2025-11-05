"""Client utilities for interacting with the Render MCP Stable Diffusion service."""

from __future__ import annotations

import asyncio
import os
from typing import Any, Dict, List, Optional

import httpx
from pydantic import BaseModel, Field, HttpUrl, validator


class RenderStoryboardFrame(BaseModel):
    """Single frame definition for the storyboard request."""

    prompt: str = Field(..., description="Prompt for this frame")
    negative_prompt: Optional[str] = Field(None, description="Negative prompt for this frame")
    seed: Optional[int] = Field(None, description="Optional per-frame seed to stabilize outputs")
    guidance_scale: Optional[float] = Field(None, description="Optional per-frame CFG override")
    steps: Optional[int] = Field(None, description="Optional per-frame inference steps override")


class RenderStoryboardRequest(BaseModel):
    """Payload describing a storyboard generation job."""

    project_name: str = Field(..., description="Human-friendly project label")
    reference_images: List[HttpUrl] = Field(..., description="HTTP-accessible reference image URLs")
    frames: List[RenderStoryboardFrame] = Field(..., description="Sequence of storyboard frames")
    cfg_scale: float = Field(5.0, ge=0.0, le=20.0, description="Default CFG scale")
    steps: int = Field(28, ge=1, le=150, description="Default inference steps")
    width: int = Field(768, ge=256, le=1536, description="Output width in pixels")
    height: int = Field(1024, ge=256, le=1536, description="Output height in pixels")
    scheduler: str = Field("dpmpp_2m", description="Scheduler to use on the remote service")
    seed: Optional[int] = Field(None, description="Global seed to anchor the run")
    extras: Dict[str, Any] = Field(default_factory=dict, description="Additional provider-specific options")

    @validator("frames")
    def validate_frames(cls, value: List[RenderStoryboardFrame]) -> List[RenderStoryboardFrame]:
        if not value:
            raise ValueError("At least one frame must be provided")
        if len(value) > 12:
            raise ValueError("A maximum of 12 frames per storyboard is supported")
        return value


class RenderMCPError(RuntimeError):
    """Raised when the Render MCP service returns an error."""


class RenderMCPClient:
    """Thin client for the Render MCP Stable Diffusion orchestration layer."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        token: Optional[str] = None,
        timeout: float = 60.0,
        poll_interval: float = 5.0,
        max_poll_time: float = 300.0,
    ) -> None:
        self.base_url = base_url or os.getenv("RENDER_MCP_URL", "https://mcp.render.com/mcp")
        self.token = token or os.getenv("RENDER_MCP_TOKEN")
        if not self.token:
            raise ValueError(
                "Render MCP token not provided. Set RENDER_MCP_TOKEN env variable or pass token explicitly."
            )
        self.timeout = timeout
        self.poll_interval = poll_interval
        self.max_poll_time = max_poll_time

    @property
    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def generate_storyboard(self, request: RenderStoryboardRequest) -> Dict[str, Any]:
        """Trigger storyboard generation and return the completed job payload."""

        payload: Dict[str, Any] = {
            "action": "storyboard.generate",
            "project": request.project_name,
            "reference_images": list(request.reference_images),
            "frames": [frame.dict(exclude_none=True) for frame in request.frames],
            "parameters": {
                "cfg_scale": request.cfg_scale,
                "steps": request.steps,
                "width": request.width,
                "height": request.height,
                "scheduler": request.scheduler,
                **request.extras,
            },
        }
        if request.seed is not None:
            payload["parameters"]["seed"] = request.seed

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                self.base_url,
                json=payload,
                headers=self._headers,
            )

            if response.status_code in (200, 201):
                data = response.json()
                self._ensure_success(data)
                return data

            if response.status_code == 202:
                data = response.json()
                status_url = data.get("status_url")
                job_id = data.get("job_id")
                if not status_url and job_id:
                    status_url = self._infer_status_url(job_id)
                if not status_url:
                    raise RenderMCPError(
                        "Render MCP returned 202 but did not provide status_url or job_id"
                    )
                return await self._poll_until_complete(client, status_url)

            self._raise_http_error(response)

        raise RenderMCPError("Unexpected flow in Render MCP client")

    async def _poll_until_complete(self, client: httpx.AsyncClient, status_url: str) -> Dict[str, Any]:
        """Poll the status endpoint until completion or timeout."""

        loop = asyncio.get_running_loop()
        start = loop.time()
        while True:
            if loop.time() - start > self.max_poll_time:
                raise RenderMCPError("Timed out waiting for Render MCP job to complete")

            response = await client.get(status_url, headers=self._headers)

            if response.status_code not in (200, 202):
                self._raise_http_error(response)

            data = response.json()
            status = data.get("status", "unknown").lower()
            if status in {"succeeded", "completed", "ready"}:
                self._ensure_success(data)
                return data
            if status in {"failed", "error"}:
                message = data.get("error") or data.get("message") or "Render MCP reported failure"
                raise RenderMCPError(message)

            await asyncio.sleep(self.poll_interval)

    def _infer_status_url(self, job_id: str) -> str:
        if self.base_url.endswith("/"):
            base = self.base_url[:-1]
        else:
            base = self.base_url
        return f"{base}/jobs/{job_id}"

    def _ensure_success(self, data: Dict[str, Any]) -> None:
        if not data:
            raise RenderMCPError("Empty response from Render MCP")
        if data.get("status") in {"failed", "error"}:
            raise RenderMCPError(data.get("error") or "Render MCP reported failure")

    def _raise_http_error(self, response: httpx.Response) -> None:
        try:
            details = response.json()
        except Exception:
            details = {"body": response.text}
        raise RenderMCPError(
            f"Render MCP request failed with status {response.status_code}: {details}"
        )
