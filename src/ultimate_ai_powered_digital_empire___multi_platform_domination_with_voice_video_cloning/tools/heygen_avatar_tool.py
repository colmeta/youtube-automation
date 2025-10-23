from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Dict, Any, List, Optional
import requests
import json
import time
import os

class HeyGenAvatarInput(BaseModel):
    """Input schema for HeyGen Avatar Tool."""
    action: str = Field(
        description="Action to perform: 'generate_video', 'create_avatar', 'get_avatars', 'check_status', 'get_voices', or 'estimate_cost'"
    )
    text: Optional[str] = Field(
        None,
        description="Text script for the avatar to speak (required for generate_video)"
    )
    avatar_id: Optional[str] = Field(
        None,
        description="ID of the avatar to use (required for generate_video, optional for others)"
    )
    voice_id: Optional[str] = Field(
        None,
        description="ID of the voice to use (optional, defaults to avatar's default voice)"
    )
    background: Optional[str] = Field(
        "office",
        description="Background style: 'office', 'white', 'green_screen', 'custom', etc."
    )
    video_quality: Optional[str] = Field(
        "720p",
        description="Video quality: '480p', '720p', '1080p'"
    )
    language: Optional[str] = Field(
        "en",
        description="Language code (e.g., 'en', 'es', 'fr', 'de', 'zh')"
    )
    avatar_name: Optional[str] = Field(
        None,
        description="Name for new custom avatar (required for create_avatar)"
    )
    photo_url: Optional[str] = Field(
        None,
        description="URL of photo for custom avatar creation (required for create_avatar)"
    )
    job_id: Optional[str] = Field(
        None,
        description="Job ID for status checking (required for check_status)"
    )
    custom_background_url: Optional[str] = Field(
        None,
        description="URL for custom background image"
    )

class HeyGenAvatarTool(BaseTool):
    """Tool for creating AI avatar videos using HeyGen API.
    
    This tool provides comprehensive functionality for:
    - Generating videos with AI avatars speaking provided text
    - Creating custom avatars from user photos
    - Managing avatar libraries and voice options
    - Handling video generation workflows with status tracking
    - Supporting multiple languages and customization options
    
    Workflows:
    1. Avatar Video Generation: Use 'generate_video' action with text and avatar_id
    2. Custom Avatar Creation: Use 'create_avatar' with photo_url and avatar_name
    3. Status Monitoring: Use 'check_status' with job_id to track progress
    4. Resource Discovery: Use 'get_avatars' or 'get_voices' to explore options
    5. Cost Planning: Use 'estimate_cost' to calculate generation costs
    """

    name: str = "heygen_avatar_tool"
    description: str = (
        "Generate AI avatar videos, create custom avatars from photos, and manage HeyGen avatar workflows. "
        "Supports multiple languages, voices, backgrounds, and video customization options with comprehensive status tracking."
    )
    args_schema: Type[BaseModel] = HeyGenAvatarInput

    def _run(
        self,
        action: str,
        text: Optional[str] = None,
        avatar_id: Optional[str] = None,
        voice_id: Optional[str] = None,
        background: Optional[str] = "office",
        video_quality: Optional[str] = "720p",
        language: Optional[str] = "en",
        avatar_name: Optional[str] = None,
        photo_url: Optional[str] = None,
        job_id: Optional[str] = None,
        custom_background_url: Optional[str] = None,
    ) -> str:
        """Execute HeyGen avatar operations based on the specified action."""
        
        try:
            api_key = os.getenv("HEYGEN_API_KEY")
            if not api_key:
                return "Error: HEYGEN_API_KEY environment variable is required"

            base_url = "https://api.heygen.com/v2"
            headers = {
                "X-API-KEY": api_key,
                "Content-Type": "application/json"
            }

            if action == "generate_video":
                return self._generate_video(
                    base_url, headers, text, avatar_id, voice_id, 
                    background, video_quality, language, custom_background_url
                )
            
            elif action == "create_avatar":
                return self._create_avatar(base_url, headers, avatar_name, photo_url)
            
            elif action == "get_avatars":
                return self._get_avatars(base_url, headers)
            
            elif action == "get_voices":
                return self._get_voices(base_url, headers, language)
            
            elif action == "check_status":
                return self._check_status(base_url, headers, job_id)
            
            elif action == "estimate_cost":
                return self._estimate_cost(text, video_quality, avatar_id)
            
            else:
                return f"Error: Unknown action '{action}'. Available actions: generate_video, create_avatar, get_avatars, get_voices, check_status, estimate_cost"

        except Exception as e:
            return f"Error executing HeyGen avatar tool: {str(e)}"

    def _generate_video(
        self, base_url: str, headers: dict, text: str, avatar_id: str,
        voice_id: Optional[str], background: str, video_quality: str,
        language: str, custom_background_url: Optional[str]
    ) -> str:
        """Generate an AI avatar video."""
        if not text or not avatar_id:
            return "Error: Both 'text' and 'avatar_id' are required for video generation"

        # Prepare video generation payload
        video_inputs = [{
            "character": {
                "type": "avatar",
                "avatar_id": avatar_id,
                "avatar_style": "normal"
            },
            "voice": {
                "type": "text",
                "input_text": text,
                "voice_id": voice_id if voice_id else "default",
                "language": language
            },
            "background": {
                "type": background,
                "url": custom_background_url if background == "custom" and custom_background_url else None
            }
        }]

        payload = {
            "video_inputs": video_inputs,
            "dimension": {
                "width": 1920 if video_quality == "1080p" else (1280 if video_quality == "720p" else 854),
                "height": 1080 if video_quality == "1080p" else (720 if video_quality == "720p" else 480)
            },
            "aspect_ratio": "16:9",
            "callback_id": f"video_{int(time.time())}"
        }

        try:
            response = requests.post(
                f"{base_url}/video/generate",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                job_id = result.get('job_id', 'unknown')
                
                return json.dumps({
                    "status": "success",
                    "message": "Video generation started successfully",
                    "job_id": job_id,
                    "video_id": result.get('video_id'),
                    "estimated_duration": result.get('estimated_duration', 'unknown'),
                    "cost_estimate": result.get('cost_estimate'),
                    "next_step": f"Use check_status action with job_id '{job_id}' to monitor progress"
                }, indent=2)
            else:
                error_detail = response.json() if response.content else {"error": "Unknown error"}
                return f"Error generating video: {response.status_code} - {error_detail}"

        except requests.exceptions.RequestException as e:
            return f"Error making video generation request: {str(e)}"

    def _create_avatar(self, base_url: str, headers: dict, avatar_name: str, photo_url: str) -> str:
        """Create a custom avatar from a photo."""
        if not avatar_name or not photo_url:
            return "Error: Both 'avatar_name' and 'photo_url' are required for avatar creation"

        payload = {
            "avatar_name": avatar_name,
            "image_url": photo_url,
            "voice_id": "default"
        }

        try:
            response = requests.post(
                f"{base_url}/avatars/create",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return json.dumps({
                    "status": "success",
                    "message": "Avatar creation started successfully",
                    "avatar_id": result.get('avatar_id'),
                    "job_id": result.get('job_id'),
                    "estimated_processing_time": "5-10 minutes",
                    "next_step": f"Use check_status action with job_id '{result.get('job_id')}' to monitor training progress"
                }, indent=2)
            else:
                error_detail = response.json() if response.content else {"error": "Unknown error"}
                return f"Error creating avatar: {response.status_code} - {error_detail}"

        except requests.exceptions.RequestException as e:
            return f"Error making avatar creation request: {str(e)}"

    def _get_avatars(self, base_url: str, headers: dict) -> str:
        """Get list of available avatars."""
        try:
            response = requests.get(
                f"{base_url}/avatars",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                avatars = result.get('data', [])
                
                formatted_avatars = []
                for avatar in avatars[:20]:  # Limit to first 20 for readability
                    formatted_avatars.append({
                        "avatar_id": avatar.get('avatar_id'),
                        "name": avatar.get('name'),
                        "gender": avatar.get('gender'),
                        "language": avatar.get('language'),
                        "preview_image": avatar.get('preview_image_url'),
                        "avatar_type": avatar.get('avatar_type', 'standard')
                    })
                
                return json.dumps({
                    "status": "success",
                    "total_avatars": len(avatars),
                    "showing": len(formatted_avatars),
                    "avatars": formatted_avatars
                }, indent=2)
            else:
                return f"Error fetching avatars: {response.status_code}"

        except requests.exceptions.RequestException as e:
            return f"Error fetching avatars: {str(e)}"

    def _get_voices(self, base_url: str, headers: dict, language: str) -> str:
        """Get list of available voices for a language."""
        try:
            params = {"language": language} if language != "en" else {}
            response = requests.get(
                f"{base_url}/voices",
                headers=headers,
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                voices = result.get('data', [])
                
                formatted_voices = []
                for voice in voices[:15]:  # Limit for readability
                    formatted_voices.append({
                        "voice_id": voice.get('voice_id'),
                        "name": voice.get('name'),
                        "gender": voice.get('gender'),
                        "language": voice.get('language'),
                        "accent": voice.get('accent'),
                        "preview_audio": voice.get('preview_audio_url')
                    })
                
                return json.dumps({
                    "status": "success",
                    "language": language,
                    "total_voices": len(voices),
                    "showing": len(formatted_voices),
                    "voices": formatted_voices
                }, indent=2)
            else:
                return f"Error fetching voices: {response.status_code}"

        except requests.exceptions.RequestException as e:
            return f"Error fetching voices: {str(e)}"

    def _check_status(self, base_url: str, headers: dict, job_id: str) -> str:
        """Check the status of a video generation or avatar creation job."""
        if not job_id:
            return "Error: 'job_id' is required for status checking"

        try:
            response = requests.get(
                f"{base_url}/jobs/{job_id}",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                status = result.get('status', 'unknown')
                
                status_info = {
                    "job_id": job_id,
                    "status": status,
                    "progress": result.get('progress', 0),
                    "created_at": result.get('created_at'),
                    "updated_at": result.get('updated_at')
                }

                if status == "completed":
                    status_info.update({
                        "video_url": result.get('video_url'),
                        "download_url": result.get('download_url'),
                        "duration": result.get('duration'),
                        "file_size": result.get('file_size'),
                        "message": "Job completed successfully! Video is ready for download."
                    })
                elif status == "processing":
                    status_info["message"] = "Job is currently processing. Please check again in a few minutes."
                    status_info["estimated_completion"] = result.get('estimated_completion')
                elif status == "failed":
                    status_info["error_message"] = result.get('error_message')
                    status_info["message"] = "Job failed. Please check error_message for details."
                else:
                    status_info["message"] = f"Job status: {status}"

                return json.dumps(status_info, indent=2)
            else:
                return f"Error checking job status: {response.status_code}"

        except requests.exceptions.RequestException as e:
            return f"Error checking job status: {str(e)}"

    def _estimate_cost(self, text: Optional[str], video_quality: str, avatar_id: Optional[str]) -> str:
        """Estimate the cost of video generation."""
        try:
            # Basic cost estimation logic (actual costs may vary)
            base_cost = 0.10  # Base cost per request
            
            # Text length cost (approximate)
            text_length = len(text) if text else 0
            text_cost = (text_length / 100) * 0.05  # $0.05 per 100 characters
            
            # Quality multiplier
            quality_multipliers = {"480p": 1.0, "720p": 1.5, "1080p": 2.0}
            quality_multiplier = quality_multipliers.get(video_quality, 1.5)
            
            # Avatar type cost (estimated)
            avatar_cost = 0.15 if avatar_id and "custom" in avatar_id.lower() else 0.05
            
            total_estimated_cost = (base_cost + text_cost + avatar_cost) * quality_multiplier
            
            estimation = {
                "cost_breakdown": {
                    "base_cost": base_cost,
                    "text_processing_cost": round(text_cost, 3),
                    "avatar_cost": avatar_cost,
                    "quality_multiplier": quality_multiplier,
                    "total_estimated_cost": round(total_estimated_cost, 3)
                },
                "text_length": text_length,
                "video_quality": video_quality,
                "currency": "USD",
                "note": "This is an estimate. Actual costs may vary based on HeyGen's current pricing."
            }
            
            return json.dumps(estimation, indent=2)

        except Exception as e:
            return f"Error calculating cost estimate: {str(e)}"