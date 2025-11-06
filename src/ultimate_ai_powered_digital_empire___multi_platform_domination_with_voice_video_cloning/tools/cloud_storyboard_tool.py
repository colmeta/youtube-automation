"""Stable Diffusion storyboard tool backed by the Render MCP service."""

from __future__ import annotations

import asyncio
import json
from typing import Any, Dict, List, Optional

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from ultimate_ai_powered_digital_empire___multi_platform_domination_with_voice_video_cloning.services import (
    RenderMCPClient,
    RenderStoryboardFrame,
    RenderStoryboardRequest,
    RenderMCPError,
)


class CloudStoryboardToolInput(BaseModel):
    """Schema for Render-backed storyboard generation."""

    project_name: str = Field(..., description="Name of the storyboard project")
    reference_images: List[str] = Field(
        ..., description="List of reference image URLs accessible to the Render service"
    )
    prompts: List[str] = Field(..., description="Ordered list of frame prompts")
    negative_prompts: Optional[List[str]] = Field(
        None,
        description="Optional negative prompts aligned by index with the prompts list",
    )
    cfg_scale: float = Field(5.0, ge=0.0, le=20.0, description="Classifier-free guidance scale")
    steps: int = Field(28, ge=1, le=150, description="Diffusion steps")
    width: int = Field(768, ge=256, le=1536, description="Output width in pixels")
    height: int = Field(1024, ge=256, le=1536, description="Output height in pixels")
    scheduler: str = Field("dpmpp_2m", description="Sampler to use on the remote service")
    seed: Optional[int] = Field(None, description="Optional global seed")
    extras: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional provider-specific options (e.g., ip_adapter_strength)",
    )


class CloudStoryboardTool(BaseTool):
    """Tool that generates consistent storyboards using a remote SDXL deployment."""

    name: str = "cloud_storyboard_generator"
    description: str = (
        "Generate multi-frame visual storyboards with Stable Diffusion XL running on the Render MCP cloud. "
        "Supports up to 12 frames per request with shared character consistency via IP-Adapter references."
    )
    args_schema: type[BaseModel] = CloudStoryboardToolInput

    def _run(
        self,
        project_name: str,
        reference_images: List[str],
        prompts: List[str],
        negative_prompts: Optional[List[str]] = None,
        cfg_scale: float = 5.0,
        steps: int = 28,
        width: int = 768,
        height: int = 1024,
        scheduler: str = "dpmpp_2m",
        seed: Optional[int] = None,
        extras: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Synchronously trigger the remote storyboard generation."""

        payload = CloudStoryboardToolInput(
            project_name=project_name,
            reference_images=reference_images,
            prompts=prompts,
            negative_prompts=negative_prompts,
            cfg_scale=cfg_scale,
            steps=steps,
            width=width,
            height=height,
            scheduler=scheduler,
            seed=seed,
            extras=extras or {},
        )

        async def _execute() -> Dict[str, Any]:
            client = RenderMCPClient()
            frames: List[RenderStoryboardFrame] = []
            neg_prompts = payload.negative_prompts or []
            for idx, prompt in enumerate(payload.prompts):
                frame_kwargs: Dict[str, Any] = {
                    "prompt": prompt,
                }
                if idx < len(neg_prompts) and neg_prompts[idx]:
                    frame_kwargs["negative_prompt"] = neg_prompts[idx]
                frames.append(RenderStoryboardFrame(**frame_kwargs))

            request = RenderStoryboardRequest(
                project_name=payload.project_name,
                reference_images=payload.reference_images,
                frames=frames,
                cfg_scale=payload.cfg_scale,
                steps=payload.steps,
                width=payload.width,
                height=payload.height,
                scheduler=payload.scheduler,
                seed=payload.seed,
                extras=payload.extras,
            )

            return await client.generate_storyboard(request)

        try:
            result = asyncio.run(_execute())
        except RenderMCPError as exc:  # pragma: no cover - network dependency
            return json.dumps({
                "success": False,
                "error": str(exc),
            })
        except RuntimeError:
            # asyncio.run cannot be called from within a running loop; create a dedicated loop.
            new_loop = asyncio.new_event_loop()
            try:
                asyncio.set_event_loop(new_loop)
                result = new_loop.run_until_complete(_execute())
            finally:
                new_loop.close()
                asyncio.set_event_loop(None)
        except Exception as exc:  # pragma: no cover - defensive branch
            return json.dumps({
                "success": False,
                "error": f"Unexpected error: {exc}",
            })

        return json.dumps({
            "success": True,
            "data": result,
        })
