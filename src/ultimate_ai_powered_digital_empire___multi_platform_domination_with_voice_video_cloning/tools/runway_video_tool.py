from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Optional, Dict, Any, List
import requests
import json
import time

class RunwayVideoRequest(BaseModel):
    """Input schema for Runway Video Tool."""
    prompt: str = Field(..., description="Text prompt describing the video content to generate")
    image_url: Optional[str] = Field(None, description="URL of input image for image-to-video generation (optional)")
    duration: int = Field(default=5, description="Video duration in seconds (5 or 10)")
    quality: str = Field(default="standard", description="Video quality: 'standard' or 'high'")
    aspect_ratio: str = Field(default="16:9", description="Video aspect ratio: '16:9', '9:16', or '1:1'")
    seed: Optional[int] = Field(None, description="Random seed for reproducible results (optional)")

class RunwayVideoTool(BaseTool):
    """Tool for generating AI videos using Runway ML Gen-3 Alpha API.
    
    This tool provides comprehensive video generation capabilities including:
    - Text-to-video generation
    - Image-to-video generation  
    - Customizable duration and quality settings
    - Generation status monitoring
    - Cost estimation and rate limit handling
    """

    name: str = "runway_video_tool"
    description: str = (
        "Generate AI videos using Runway ML Gen-3 Alpha API. Supports text-to-video and "
        "image-to-video generation with various quality settings, durations (5-10 seconds), "
        "and aspect ratios. Returns generation status, download URLs, and cost information."
    )
    args_schema: Type[BaseModel] = RunwayVideoRequest

    def _run(self, prompt: str, image_url: Optional[str] = None, duration: int = 5, 
             quality: str = "standard", aspect_ratio: str = "16:9", seed: Optional[int] = None) -> str:
        """Generate AI video using Runway ML API."""
        
        try:
            # Get API key from environment
            import os
            api_key = os.getenv('RUNWAYML_API_KEY')
            if not api_key:
                return json.dumps({
                    "success": False,
                    "error": "RUNWAYML_API_KEY environment variable is required but not found",
                    "suggestion": "Please set your Runway ML API key in the RUNWAYML_API_KEY environment variable"
                })

            # Validate inputs
            if duration not in [5, 10]:
                return json.dumps({
                    "success": False,
                    "error": "Invalid duration. Must be 5 or 10 seconds",
                    "provided_duration": duration
                })

            if quality not in ["standard", "high"]:
                return json.dumps({
                    "success": False,
                    "error": "Invalid quality. Must be 'standard' or 'high'",
                    "provided_quality": quality
                })

            if aspect_ratio not in ["16:9", "9:16", "1:1"]:
                return json.dumps({
                    "success": False,
                    "error": "Invalid aspect ratio. Must be '16:9', '9:16', or '1:1'",
                    "provided_aspect_ratio": aspect_ratio
                })

            # Prepare API request
            base_url = "https://api.runwayml.com/v1"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "X-Runway-Version": "2024-09-13"
            }

            # Build request payload
            payload = {
                "model": "gen3a_turbo",
                "prompt": prompt,
                "duration": duration,
                "aspect_ratio": aspect_ratio,
                "watermark": False
            }

            # Add image input if provided
            if image_url:
                payload["image"] = image_url
                payload["mode"] = "image_to_video"
            else:
                payload["mode"] = "text_to_video"

            # Add seed if provided
            if seed is not None:
                payload["seed"] = seed

            # Add quality settings
            if quality == "high":
                payload["upscale"] = True

            # Submit generation request
            generate_url = f"{base_url}/image_generations"
            
            response = requests.post(generate_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 429:
                return json.dumps({
                    "success": False,
                    "error": "Rate limit exceeded",
                    "retry_after": response.headers.get("Retry-After", "60"),
                    "suggestion": "Please wait before making another request"
                })

            if response.status_code == 402:
                return json.dumps({
                    "success": False,
                    "error": "Insufficient credits",
                    "suggestion": "Please add credits to your Runway ML account"
                })

            if response.status_code != 200:
                error_detail = "Unknown error"
                try:
                    error_data = response.json()
                    error_detail = error_data.get("detail", error_data.get("error", str(error_data)))
                except:
                    error_detail = f"HTTP {response.status_code}: {response.text[:200]}"
                
                return json.dumps({
                    "success": False,
                    "error": f"API request failed: {error_detail}",
                    "status_code": response.status_code
                })

            generation_data = response.json()
            generation_id = generation_data.get("id")
            
            if not generation_id:
                return json.dumps({
                    "success": False,
                    "error": "No generation ID received from API",
                    "response": generation_data
                })

            # Monitor generation progress
            status_url = f"{base_url}/tasks/{generation_id}"
            max_attempts = 60  # 5 minutes max wait time
            attempt = 0
            
            while attempt < max_attempts:
                try:
                    status_response = requests.get(status_url, headers=headers, timeout=10)
                    
                    if status_response.status_code != 200:
                        attempt += 1
                        time.sleep(5)
                        continue

                    status_data = status_response.json()
                    status = status_data.get("status", "unknown")
                    
                    if status == "SUCCEEDED":
                        # Generation completed successfully
                        video_url = status_data.get("output", {}).get("url") if isinstance(status_data.get("output"), dict) else status_data.get("output")
                        
                        # Calculate estimated cost
                        base_cost = 0.05 if duration == 5 else 0.10  # Example pricing
                        quality_multiplier = 1.5 if quality == "high" else 1.0
                        estimated_cost = base_cost * quality_multiplier

                        return json.dumps({
                            "success": True,
                            "generation_id": generation_id,
                            "video_url": video_url,
                            "status": "completed",
                            "duration": duration,
                            "quality": quality,
                            "aspect_ratio": aspect_ratio,
                            "estimated_cost": estimated_cost,
                            "generation_time": attempt * 5,
                            "prompt": prompt,
                            "mode": "image_to_video" if image_url else "text_to_video"
                        })
                    
                    elif status == "FAILED":
                        error_msg = status_data.get("failure_reason", "Generation failed")
                        return json.dumps({
                            "success": False,
                            "error": f"Video generation failed: {error_msg}",
                            "generation_id": generation_id,
                            "status": status
                        })
                    
                    elif status in ["PENDING", "RUNNING"]:
                        # Still processing
                        progress = status_data.get("progress", 0)
                        if attempt % 6 == 0:  # Log every 30 seconds
                            print(f"Generation in progress: {progress}% complete...")
                        
                        attempt += 1
                        time.sleep(5)
                        continue
                    
                    else:
                        # Unknown status
                        attempt += 1
                        time.sleep(5)
                        continue

                except requests.exceptions.RequestException as e:
                    attempt += 1
                    if attempt >= max_attempts:
                        return json.dumps({
                            "success": False,
                            "error": f"Failed to check generation status: {str(e)}",
                            "generation_id": generation_id
                        })
                    time.sleep(5)
                    continue

            # Timeout reached
            return json.dumps({
                "success": False,
                "error": "Generation timeout - video is still processing",
                "generation_id": generation_id,
                "status": "timeout",
                "suggestion": "Check generation status later using the generation_id"
            })

        except requests.exceptions.ConnectionError:
            return json.dumps({
                "success": False,
                "error": "Failed to connect to Runway ML API",
                "suggestion": "Please check your internet connection and try again"
            })
        
        except requests.exceptions.Timeout:
            return json.dumps({
                "success": False,
                "error": "Request timeout",
                "suggestion": "The API request timed out. Please try again"
            })
        
        except Exception as e:
            return json.dumps({
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "type": type(e).__name__
            })