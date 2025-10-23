import os

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	EXASearchTool,
	ScrapeWebsiteTool,
	DallETool,
	BraveSearchTool
)
from ultimate_ai_powered_digital_empire___multi_platform_domination_with_voice_video_cloning.tools.elevenlabs_voice_tool import ElevenLabsVoiceTool
from ultimate_ai_powered_digital_empire___multi_platform_domination_with_voice_video_cloning.tools.runway_video_tool import RunwayVideoTool
from ultimate_ai_powered_digital_empire___multi_platform_domination_with_voice_video_cloning.tools.heygen_avatar_tool import HeyGenAvatarTool





@CrewBase
class UltimateAiPoweredDigitalEmpireMultiPlatformDominationWithVoiceVideoCloningCrew:
    """UltimateAiPoweredDigitalEmpireMultiPlatformDominationWithVoiceVideoCloning crew"""

    
    @agent
    def youtube_trend_research_specialist(self) -> Agent:

        
        return Agent(
            config=self.agents_config["youtube_trend_research_specialist"],
            
            
            tools=[
				EXASearchTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def content_script_writer(self) -> Agent:

        
        return Agent(
            config=self.agents_config["content_script_writer"],
            
            
            tools=[
				ScrapeWebsiteTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def youtube_seo_specialist(self) -> Agent:

        
        return Agent(
            config=self.agents_config["youtube_seo_specialist"],
            
            
            tools=[
				EXASearchTool(),
				BraveSearchTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def ai_video_producer(self) -> Agent:

        
        return Agent(
            config=self.agents_config["ai_video_producer"],
            
            
            tools=[
				DallETool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def youtube_publisher(self) -> Agent:

        
        return Agent(
            config=self.agents_config["youtube_publisher"],
            
            
            tools=[
				DallETool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def competitive_intelligence_analyst(self) -> Agent:

        
        return Agent(
            config=self.agents_config["competitive_intelligence_analyst"],
            
            
            tools=[
				EXASearchTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def viral_content_formula_engineer(self) -> Agent:

        
        return Agent(
            config=self.agents_config["viral_content_formula_engineer"],
            
            
            tools=[
				EXASearchTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def ai_trend_predictor(self) -> Agent:

        
        return Agent(
            config=self.agents_config["ai_trend_predictor"],
            
            
            tools=[
				EXASearchTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def youtube_algorithm_hacker(self) -> Agent:

        
        return Agent(
            config=self.agents_config["youtube_algorithm_hacker"],
            
            
            tools=[
				EXASearchTool(),
				BraveSearchTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def engagement_manipulation_specialist(self) -> Agent:

        
        return Agent(
            config=self.agents_config["engagement_manipulation_specialist"],
            
            
            tools=[
				EXASearchTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def medium_blog_domination_specialist(self) -> Agent:

        
        return Agent(
            config=self.agents_config["medium_blog_domination_specialist"],
            
            
            tools=[
				ScrapeWebsiteTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def multi_platform_content_strategist(self) -> Agent:

        
        return Agent(
            config=self.agents_config["multi_platform_content_strategist"],
            
            
            tools=[
				EXASearchTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def affiliate_monetization_strategist(self) -> Agent:

        
        return Agent(
            config=self.agents_config["affiliate_monetization_strategist"],
            
            
            tools=[
				EXASearchTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def email_list_building_automation_specialist(self) -> Agent:

        
        return Agent(
            config=self.agents_config["email_list_building_automation_specialist"],
            
            
            tools=[
				EXASearchTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def seo_search_domination_expert(self) -> Agent:

        
        return Agent(
            config=self.agents_config["seo_search_domination_expert"],
            
            
            tools=[
				EXASearchTool(),
				BraveSearchTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def audience_psychology_retention_master(self) -> Agent:

        
        return Agent(
            config=self.agents_config["audience_psychology_retention_master"],
            
            
            tools=[
				EXASearchTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def podcast_audio_content_domination_specialist(self) -> Agent:

        
        return Agent(
            config=self.agents_config["podcast_audio_content_domination_specialist"],
            
            
            tools=[
				EXASearchTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def market_intelligence_competitor_destroyer(self) -> Agent:

        
        return Agent(
            config=self.agents_config["market_intelligence_competitor_destroyer"],
            
            
            tools=[
				EXASearchTool(),
				BraveSearchTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def content_voice_specialist(self) -> Agent:

        
        return Agent(
            config=self.agents_config["content_voice_specialist"],
            
            
            tools=[
				ElevenLabsVoiceTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def visual_content_strategy_specialist(self) -> Agent:

        
        return Agent(
            config=self.agents_config["visual_content_strategy_specialist"],
            
            
            tools=[
				RunwayVideoTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def personal_branding_presentation_specialist(self) -> Agent:

        
        return Agent(
            config=self.agents_config["personal_branding_presentation_specialist"],
            
            
            tools=[
				HeyGenAvatarTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def cost_optimization_roi_manager(self) -> Agent:

        
        return Agent(
            config=self.agents_config["cost_optimization_roi_manager"],
            
            
            tools=[

            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    

    
    @task
    def competitive_intelligence_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["competitive_intelligence_analysis"],
            markdown=False,
            
            
        )
    
    @task
    def predict_future_viral_topics(self) -> Task:
        return Task(
            config=self.tasks_config["predict_future_viral_topics"],
            markdown=False,
            
            
        )
    
    @task
    def hack_youtube_algorithm(self) -> Task:
        return Task(
            config=self.tasks_config["hack_youtube_algorithm"],
            markdown=False,
            
            
        )
    
    @task
    def engineer_viral_content_formulas(self) -> Task:
        return Task(
            config=self.tasks_config["engineer_viral_content_formulas"],
            markdown=False,
            
            
        )
    
    @task
    def engineer_addictive_engagement(self) -> Task:
        return Task(
            config=self.tasks_config["engineer_addictive_engagement"],
            markdown=False,
            
            
        )
    
    @task
    def research_trending_topics(self) -> Task:
        return Task(
            config=self.tasks_config["research_trending_topics"],
            markdown=False,
            
            
        )
    
    @task
    def create_video_scripts(self) -> Task:
        return Task(
            config=self.tasks_config["create_video_scripts"],
            markdown=False,
            
            
        )
    
    @task
    def optimize_for_youtube_seo(self) -> Task:
        return Task(
            config=self.tasks_config["optimize_for_youtube_seo"],
            markdown=False,
            
            
        )
    
    @task
    def generate_video_content(self) -> Task:
        return Task(
            config=self.tasks_config["generate_video_content"],
            markdown=False,
            
            
        )
    
    @task
    def generate_ai_voiceovers(self) -> Task:
        return Task(
            config=self.tasks_config["generate_ai_voiceovers"],
            markdown=False,
            
            
        )
    
    @task
    def create_viral_medium_articles(self) -> Task:
        return Task(
            config=self.tasks_config["create_viral_medium_articles"],
            markdown=False,
            
            
        )
    
    @task
    def create_custom_thumbnails(self) -> Task:
        return Task(
            config=self.tasks_config["create_custom_thumbnails"],
            markdown=False,
            
            
        )
    
    @task
    def create_youtube_shorts(self) -> Task:
        return Task(
            config=self.tasks_config["create_youtube_shorts"],
            markdown=False,
            
            
        )
    
    @task
    def launch_viral_podcast_empire(self) -> Task:
        return Task(
            config=self.tasks_config["launch_viral_podcast_empire"],
            markdown=False,
            
            
        )
    
    @task
    def generate_ai_video_content(self) -> Task:
        return Task(
            config=self.tasks_config["generate_ai_video_content"],
            markdown=False,
            
            
        )
    
    @task
    def create_ai_avatar_videos(self) -> Task:
        return Task(
            config=self.tasks_config["create_ai_avatar_videos"],
            markdown=False,
            
            
        )
    
    @task
    def generate_multi_platform_content_packages(self) -> Task:
        return Task(
            config=self.tasks_config["generate_multi_platform_content_packages"],
            markdown=False,
            
            
        )
    
    @task
    def dominate_all_search_rankings(self) -> Task:
        return Task(
            config=self.tasks_config["dominate_all_search_rankings"],
            markdown=False,
            
            
        )
    
    @task
    def upload_to_youtube(self) -> Task:
        return Task(
            config=self.tasks_config["upload_to_youtube"],
            markdown=False,
            
            
        )
    
    @task
    def monitor_analytics_and_optimize(self) -> Task:
        return Task(
            config=self.tasks_config["monitor_analytics_and_optimize"],
            markdown=False,
            
            
        )
    
    @task
    def design_affiliate_monetization_strategy(self) -> Task:
        return Task(
            config=self.tasks_config["design_affiliate_monetization_strategy"],
            markdown=False,
            
            
        )
    
    @task
    def build_email_empire_automation_funnels(self) -> Task:
        return Task(
            config=self.tasks_config["build_email_empire_automation_funnels"],
            markdown=False,
            
            
        )
    
    @task
    def engineer_audience_addiction_loyalty_systems(self) -> Task:
        return Task(
            config=self.tasks_config["engineer_audience_addiction_loyalty_systems"],
            markdown=False,
            
            
        )
    
    @task
    def execute_total_market_domination_strategy(self) -> Task:
        return Task(
            config=self.tasks_config["execute_total_market_domination_strategy"],
            markdown=False,
            
            
        )
    
    @task
    def launch_total_digital_empire(self) -> Task:
        return Task(
            config=self.tasks_config["launch_total_digital_empire"],
            markdown=False,
            
            
        )
    
    @task
    def optimize_costs_roi_strategy(self) -> Task:
        return Task(
            config=self.tasks_config["optimize_costs_roi_strategy"],
            markdown=False,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the UltimateAiPoweredDigitalEmpireMultiPlatformDominationWithVoiceVideoCloning crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

    def _load_response_format(self, name):
        with open(os.path.join(self.base_directory, "config", f"{name}.json")) as f:
            json_schema = json.loads(f.read())

        return SchemaConverter.build(json_schema)
