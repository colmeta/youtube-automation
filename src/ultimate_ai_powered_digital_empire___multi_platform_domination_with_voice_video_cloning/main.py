#!/usr/bin/env python
"""CLI entry points for the agentic growth crew."""

from __future__ import annotations

import argparse
import json
from typing import Any, Dict

from ultimate_ai_powered_digital_empire___multi_platform_domination_with_voice_video_cloning.crew import (
    UltimateAiPoweredDigitalEmpireMultiPlatformDominationWithVoiceVideoCloningCrew,
)


def _build_default_inputs() -> Dict[str, Any]:
    return {
        "brand_name": "Popcorn Labs",
        "niche": "AI storyboard SaaS",
        "budget_level": "scrappy",
        "brand_voice": "bold, cinematic, human",
    }


def run(inputs: Dict[str, Any] | None = None) -> None:
    crew = UltimateAiPoweredDigitalEmpireMultiPlatformDominationWithVoiceVideoCloningCrew()
    result = crew.kickoff(inputs=inputs or _build_default_inputs())
    for task in result:
        print(f"\n=== {getattr(task, 'name', 'Task')} ===")
        output = getattr(task, "output", None)
        if output:
            print(output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Agentic Growth crew")
    parser.add_argument(
        "--inputs",
        type=str,
        help="JSON string with crew inputs (brand_name, niche, budget_level, etc.)",
    )

    args = parser.parse_args()
    payload = None
    if args.inputs:
        payload = json.loads(args.inputs)

    run(payload)


if __name__ == "__main__":
    main()
