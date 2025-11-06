"""Agentic growth crew orchestrator for the Ultimate AI Powered Digital Empire."""

from __future__ import annotations

import os
from typing import List, Optional

from crewai import Agent, Crew, LLM, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import BraveSearchTool, EXASearchTool, ScrapeWebsiteTool

from ultimate_ai_powered_digital_empire___multi_platform_domination_with_voice_video_cloning.tools import (
    CloudStoryboardTool,
)


def _build_llm(model: Optional[str] = None, temperature: float = 0.4) -> LLM:
    """Create an LLM instance with Groq-first fallbacks."""

    groq_api_key = os.getenv("GROQ_API_KEY")
    if groq_api_key:
        return LLM(
            model=model or os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile"),
            api_key=groq_api_key,
            api_base=os.getenv("GROQ_API_BASE", "https://api.groq.com/openai/v1"),
            temperature=temperature,
        )

    return LLM(
        model=model or os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=temperature,
    )


def _default_agent_kwargs() -> dict:
    return {
        "reasoning": False,
        "max_iter": 18,
        "allow_delegation": False,
        "inject_date": True,
    }


@CrewBase
class UltimateAiPoweredDigitalEmpireMultiPlatformDominationWithVoiceVideoCloningCrew:
    """Agentic growth operating system for unstoppable digital dominance."""

    budget_modes = {"scrappy", "balanced", "premium"}

    # --- Agents -----------------------------------------------------------------

    @agent
    def growth_signal_hunter(self) -> Agent:
        tools = [EXASearchTool(), BraveSearchTool()]
        return Agent(
            config=self.agents_config["growth_signal_hunter"],
            tools=tools,
            llm=_build_llm(),
            **_default_agent_kwargs(),
        )

    @agent
    def audience_intelligence_analyst(self) -> Agent:
        tools = [ScrapeWebsiteTool(), EXASearchTool()]
        return Agent(
            config=self.agents_config["audience_intelligence_analyst"],
            tools=tools,
            llm=_build_llm(),
            **_default_agent_kwargs(),
        )

    @agent
    def social_content_architect(self) -> Agent:
        return Agent(
            config=self.agents_config["social_content_architect"],
            tools=[ScrapeWebsiteTool()],
            llm=_build_llm(),
            **_default_agent_kwargs(),
        )

    @agent
    def visual_storyboard_director(self) -> Agent:
        storyboard_tool = CloudStoryboardTool()
        return Agent(
            config=self.agents_config["visual_storyboard_director"],
            tools=[storyboard_tool],
            llm=_build_llm(temperature=0.2),
            **_default_agent_kwargs(),
        )

    @agent
    def human_tone_editor(self) -> Agent:
        return Agent(
            config=self.agents_config["human_tone_editor"],
            tools=[],
            llm=_build_llm(temperature=0.3),
            **_default_agent_kwargs(),
        )

    @agent
    def distribution_field_commander(self) -> Agent:
        tools = [BraveSearchTool(), EXASearchTool()]
        return Agent(
            config=self.agents_config["distribution_field_commander"],
            tools=tools,
            llm=_build_llm(),
            **_default_agent_kwargs(),
        )

    @agent
    def performance_oracle(self) -> Agent:
        return Agent(
            config=self.agents_config["performance_oracle"],
            tools=[ScrapeWebsiteTool()],
            llm=_build_llm(temperature=0.25),
            **_default_agent_kwargs(),
        )

    # --- Tasks ------------------------------------------------------------------

    @task
    def scan_growth_opportunities(self) -> Task:
        return Task(
            config=self.tasks_config["scan_growth_opportunities"],
            markdown=True,
        )

    @task
    def synthesize_audience_intelligence(self) -> Task:
        return Task(
            config=self.tasks_config["synthesize_audience_intelligence"],
            markdown=True,
        )

    @task
    def architect_campaign_system(self) -> Task:
        return Task(
            config=self.tasks_config["architect_campaign_system"],
            markdown=True,
        )

    @task
    def craft_storyboard_brief(self) -> Task:
        return Task(
            config=self.tasks_config["craft_storyboard_brief"],
            markdown=True,
        )

    @task
    def render_storyboard_sequences(self) -> Task:
        return Task(
            config=self.tasks_config["render_storyboard_sequences"],
            markdown=True,
        )

    @task
    def polish_human_copy(self) -> Task:
        return Task(
            config=self.tasks_config["polish_human_copy"],
            markdown=True,
        )

    @task
    def deploy_distribution_playbook(self) -> Task:
        return Task(
            config=self.tasks_config["deploy_distribution_playbook"],
            markdown=True,
        )

    @task
    def analyze_performance_feedback(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_performance_feedback"],
            markdown=True,
        )

    # --- Crew -------------------------------------------------------------------

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=os.getenv("CREW_VERBOSE", "true").lower() == "true",
        )

    # --- Utilities --------------------------------------------------------------

    @staticmethod
    def validate_inputs(inputs: dict) -> dict:
        """Normalize and validate runtime inputs before kickoff."""

        inputs = dict(inputs or {})
        budget = inputs.get("budget_level", "scrappy").lower()
        if budget not in UltimateAiPoweredDigitalEmpireMultiPlatformDominationWithVoiceVideoCloningCrew.budget_modes:
            budget = "scrappy"
        inputs["budget_level"] = budget
        inputs.setdefault("brand_name", inputs.get("niche", "Next-Gen Brand"))
        inputs.setdefault("offer_name", inputs.get("brand_name"))
        inputs.setdefault("brand_voice", "confident, human, future-forward")
        return inputs

    def kickoff(self, inputs: Optional[dict] = None) -> List[Task]:
        """Helper to run the crew with safe defaults."""

        sanitized = self.validate_inputs(inputs or {})
        return self.crew().kickoff(inputs=sanitized)
