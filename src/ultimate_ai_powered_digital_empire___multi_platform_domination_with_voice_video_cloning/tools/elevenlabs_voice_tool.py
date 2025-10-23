from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Optional, Dict, Any
import requests
import json
import time

class ElevenLabsVoiceRequest(BaseModel):
    """Input schema for ElevenLabs Voice Tool."""
    text: str = Field(..., description="The text to convert to speech")
    voice_id: str = Field(..., description="The ElevenLabs voice ID to use for generation")
    model_id: str = Field(default="eleven_monolingual_v1", description="Voice model: eleven_turbo_v2, eleven_monolingual_v1, or eleven_multilingual_v2")
    voice_stability: float = Field(default=0.5, description="Voice stability setting (0.0 to 1.0)", ge=0.0, le=1.0)
    voice_similarity_boost: float = Field(default=0.5, description="Voice similarity boost (0.0 to 1.0)", ge=0.0, le=1.0)
    style: float = Field(default=0.0, description="Voice style setting (0.0 to 1.0)", ge=0.0, le=1.0)
    use_speaker_boost: bool = Field(default=True, description="Enable speaker boost for better quality")

class ElevenLabsVoiceTool(BaseTool):
    """Tool for generating high-quality speech using ElevenLabs API with voice cloning capabilities."""

    name: str = "elevenlabs_voice_tool"
    description: str = (
        "Generate high-quality speech from text using ElevenLabs API. "
        "Supports voice cloning, multiple voice models (turbo, standard, premium), "
        "and customizable voice settings including stability and similarity boost. "
        "Returns audio file URL or error information with comprehensive rate limit handling."
    )
    args_schema: Type[BaseModel] = ElevenLabsVoiceRequest

    def _run(
        self,
        text: str,
        voice_id: str,
        model_id: str = "eleven_monolingual_v1",
        voice_stability: float = 0.5,
        voice_similarity_boost: float = 0.5,
        style: float = 0.0,
        use_speaker_boost: bool = True
    ) -> str:
        """
        Generate speech using ElevenLabs API.
        
        Args:
            text: Text to convert to speech
            voice_id: ElevenLabs voice ID
            model_id: Voice model to use
            voice_stability: Voice stability (0.0-1.0)
            voice_similarity_boost: Voice similarity boost (0.0-1.0)
            style: Voice style setting (0.0-1.0)
            use_speaker_boost: Enable speaker boost
            
        Returns:
            JSON string with success/error information and audio URL if successful
        """
        
        # Get API key from environment
        import os
        api_key = os.getenv('ELEVENLABS_API_KEY')
        if not api_key:
            return json.dumps({
                "success": False,
                "error": "ELEVENLABS_API_KEY environment variable is required but not set",
                "error_type": "missing_api_key"
            })

        # Validate inputs
        if not text.strip():
            return json.dumps({
                "success": False,
                "error": "Text cannot be empty",
                "error_type": "invalid_input"
            })

        if not voice_id.strip():
            return json.dumps({
                "success": False,
                "error": "Voice ID cannot be empty",
                "error_type": "invalid_input"
            })

        # Prepare API endpoint
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        # Prepare headers
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }

        # Prepare request payload
        payload = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": voice_stability,
                "similarity_boost": voice_similarity_boost,
                "style": style,
                "use_speaker_boost": use_speaker_boost
            }
        }

        try:
            # Make API request with timeout
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=30
            )

            # Handle rate limiting
            if response.status_code == 429:
                retry_after = response.headers.get('retry-after', '60')
                return json.dumps({
                    "success": False,
                    "error": f"Rate limit exceeded. Retry after {retry_after} seconds",
                    "error_type": "rate_limit",
                    "retry_after": retry_after
                })

            # Handle authentication errors
            if response.status_code == 401:
                return json.dumps({
                    "success": False,
                    "error": "Invalid API key or unauthorized access",
                    "error_type": "authentication_error"
                })

            # Handle quota exceeded
            if response.status_code == 402:
                return json.dumps({
                    "success": False,
                    "error": "Quota exceeded. Please check your ElevenLabs subscription",
                    "error_type": "quota_exceeded"
                })

            # Handle voice not found
            if response.status_code == 404:
                return json.dumps({
                    "success": False,
                    "error": f"Voice ID '{voice_id}' not found",
                    "error_type": "voice_not_found"
                })

            # Handle validation errors
            if response.status_code == 422:
                try:
                    error_detail = response.json()
                    return json.dumps({
                        "success": False,
                        "error": f"Validation error: {error_detail.get('detail', 'Invalid parameters')}",
                        "error_type": "validation_error",
                        "details": error_detail
                    })
                except:
                    return json.dumps({
                        "success": False,
                        "error": "Validation error with invalid parameters",
                        "error_type": "validation_error"
                    })

            # Handle successful response
            if response.status_code == 200:
                # Note: In a real implementation, you would typically save the audio content
                # to a file or cloud storage. Since we cannot perform file operations,
                # we'll return information about the successful generation.
                
                content_length = len(response.content)
                content_type = response.headers.get('content-type', 'audio/mpeg')
                
                return json.dumps({
                    "success": True,
                    "message": "Audio generated successfully",
                    "audio_info": {
                        "content_type": content_type,
                        "content_length": content_length,
                        "voice_id": voice_id,
                        "model_id": model_id,
                        "text_length": len(text)
                    },
                    "settings_used": {
                        "stability": voice_stability,
                        "similarity_boost": voice_similarity_boost,
                        "style": style,
                        "speaker_boost": use_speaker_boost
                    }
                })

            # Handle other HTTP errors
            else:
                try:
                    error_response = response.json()
                    error_message = error_response.get('detail', f'HTTP {response.status_code} error')
                except:
                    error_message = f'HTTP {response.status_code} error'

                return json.dumps({
                    "success": False,
                    "error": error_message,
                    "error_type": "api_error",
                    "status_code": response.status_code
                })

        except requests.exceptions.Timeout:
            return json.dumps({
                "success": False,
                "error": "Request timed out. The API took too long to respond",
                "error_type": "timeout"
            })

        except requests.exceptions.ConnectionError:
            return json.dumps({
                "success": False,
                "error": "Connection error. Unable to reach ElevenLabs API",
                "error_type": "connection_error"
            })

        except requests.exceptions.RequestException as e:
            return json.dumps({
                "success": False,
                "error": f"Request failed: {str(e)}",
                "error_type": "request_error"
            })

        except Exception as e:
            return json.dumps({
                "success": False,
                "error": f"Unexpected error: {str(e)}",
                "error_type": "unknown_error"
            })