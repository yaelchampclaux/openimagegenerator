import abc
import requests
import base64
import json
from typing import Dict, Any, Optional, List
import logging
import io
import time

logger = logging.getLogger(__name__)

# --- Data Structures ---

class ImageResult:
    """
    Represents the result of an image generation request.
    """
    def __init__(self, image_data: bytes = None, image_url: str = None, prompt: str = None, model_used: str = None):
        self.image_data = image_data
        self.image_url = image_url
        self.prompt = prompt
        self.model_used = model_used

    def __str__(self):
        if self.image_url:
            return f"Image generated for '{self.prompt[:30]}...' via {self.model_used}. URL: {self.image_url}"
        elif self.image_data:
            return f"Image generated for '{self.prompt[:30]}...' via {self.model_used}. Data: {len(self.image_data)} bytes"
        else:
            return f"No image generated for '{self.prompt[:30]}...' via {self.model_used}."

# --- Abstract Base Class ---

class BaseImageGenerationModel(abc.ABC):
    """
    Abstract base class for AI image generation models.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.model_name = "Unknown Model"

    @abc.abstractmethod
    def generate_image(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> List[ImageResult]:
        pass

# --- Google Gemini Client (FREE tier available) ---

class GeminiClient(BaseImageGenerationModel):
    """
    Client for Google Gemini (Nano Banana) - FREE tier with generous limits
    1500 requests/day free, requires API key
    """
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.model_name = "Google Gemini (FREE)"

    def generate_image(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> List[ImageResult]:
        if not self.api_key:
            raise ValueError("API key required for Google Gemini")
            
        if options is None:
            options = {}

        model = "gemini-2.5-flash-image-preview"
        url = f"{self.base_url}/{model}:generateContent"
        
        headers = {
            "x-goog-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt}
                ]
            }]
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'candidates' in data and len(data['candidates']) > 0:
                    parts = data['candidates'][0].get('content', {}).get('parts', [])
                    
                    for part in parts:
                        if 'inlineData' in part:
                            image_b64 = part['inlineData']['data']
                            image_data = base64.b64decode(image_b64)
                            
                            return [ImageResult(
                                image_data=image_data,
                                prompt=prompt,
                                model_used="Google Gemini 2.0 Flash"
                            )]
                
                raise ValueError("No image data in response")
            elif response.status_code == 429:
                raise Exception(
                    "Gemini quota exceeded. You've reached your daily limit (1500 free requests/day). "
                    "Wait until tomorrow or use Pollinations.ai (unlimited free) as alternative. "
                    "Check quotas: https://aistudio.google.com/app/apikey"
                )
            else:
                logger.error(f"Gemini API error: {response.status_code} - {response.text}")
                raise requests.exceptions.RequestException(f"API Error: {response.text}")

        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower() or "RESOURCE_EXHAUSTED" in error_msg:
                raise Exception(
                    "Gemini quota exceeded (1500/day free limit). "
                    "Use Pollinations.ai instead (unlimited free). "
                    "Or wait and check: https://aistudio.google.com/app/apikey"
                )
            logger.error(f"Error with Gemini API: {e}")
            raise e

# --- Hugging Face Client (FREE) - Updated with working models ---

class HuggingFaceClient(BaseImageGenerationModel):
    """
    Client for Hugging Face Inference API - FREE tier available
    Multiple models available, may be slow on first request (model loading)
    """
    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self.base_url = "https://api-inference.huggingface.co/models"
        # Updated with models that actually work
        self.models = {
            "flux-schnell": "black-forest-labs/FLUX.1-schnell",
            "stable-diffusion-xl": "stabilityai/stable-diffusion-xl-base-1.0",
            "stable-diffusion-3": "stabilityai/stable-diffusion-3-medium-diffusers",
        }
        self.model_name = "Hugging Face (FREE)"

    def generate_image(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> List[ImageResult]:
        if options is None:
            options = {}
            
        # Use FLUX schnell by default (fast and good quality)
        model_key = options.get('model', 'flux-schnell')
        model_id = self.models.get(model_key, self.models['flux-schnell'])
        
        url = f"{self.base_url}/{model_id}"
        
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        payload = {"inputs": prompt}
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=120)
            
            if response.status_code == 200:
                image_data = response.content
                return [ImageResult(
                    image_data=image_data,
                    prompt=prompt,
                    model_used=f"Hugging Face - {model_id.split('/')[-1]}"
                )]
            elif response.status_code == 503:
                raise Exception(
                    "Hugging Face model is loading (cold start). "
                    "This takes 30-60 seconds. Please wait and try again. "
                    "Or use Pollinations.ai for instant generation."
                )
            else:
                logger.error(f"Hugging Face API error: {response.status_code} - {response.text}")
                raise requests.exceptions.RequestException(
                    f"Hugging Face API Error. Model may not exist or be unavailable. "
                    f"Try Pollinations.ai or Gemini instead."
                )
                
        except Exception as e:
            error_msg = str(e)
            if "503" in error_msg or "loading" in error_msg.lower():
                raise Exception(
                    "Model is loading (first use). Wait 30-60s and retry. "
                    "Or use Pollinations (instant) or Gemini instead."
                )
            logger.error(f"Error with Hugging Face API: {e}")
            raise e

# --- Pollinations Client (FREE) ---

class PollinationsClient(BaseImageGenerationModel):
    """
    Client for Pollinations.ai - Completely FREE and unlimited
    No API key required, instant generation
    """
    def __init__(self):
        super().__init__()
        self.base_url = "https://image.pollinations.ai/prompt"
        self.model_name = "Pollinations.ai (FREE)"

    def generate_image(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> List[ImageResult]:
        if options is None:
            options = {}
            
        width = options.get('width', 1024)
        height = options.get('height', 1024)
        
        clean_prompt = prompt.replace(' ', '%20')
        url = f"{self.base_url}/{clean_prompt}"
        params = {
            'width': width,
            'height': height,
            'nologo': 'true',
            'enhance': 'true'
        }
        
        try:
            response = requests.get(url, params=params, timeout=60)
            
            if response.status_code == 200:
                return [ImageResult(
                    image_data=response.content,
                    prompt=prompt,
                    model_used="Pollinations.ai"
                )]
            else:
                raise requests.exceptions.RequestException(f"API Error: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error with Pollinations API: {e}")
            raise e

    def get_available_models(self):
        """Return list of available models"""
        return [
            {"key": k, "name": v.split('/')[-1]} 
            for k, v in self.models.items()
        ]

# --- Placeholder Image Client (ALWAYS WORKS) ---

class PlaceholderClient(BaseImageGenerationModel):
    """
    Generates placeholder images - for testing only
    """
    def __init__(self):
        super().__init__()
        self.model_name = "Placeholder (DEMO)"

    def generate_image(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> List[ImageResult]:
        if options is None:
            options = {}
            
        width = min(options.get('width', 512), 800)
        height = min(options.get('height', 512), 800)
        
        url = f"https://via.placeholder.com/{width}x{height}/4A90E2/FFFFFF.png"
        params = {'text': f"Generated: {prompt[:15]}"}
        
        try:
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                return [ImageResult(
                    image_data=response.content,
                    prompt=prompt,
                    model_used="Placeholder Service"
                )]
            else:
                logger.warning(f"Placeholder service failed: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error with placeholder: {e}")
            return []

# --- Runware Client (PAID but cheap) ---

class RunwareClient(BaseImageGenerationModel):
    """
    Client for Runware - Very affordable ($0.002/image)
    Best price/quality ratio for paid services
    """
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://api.runware.ai/v1"
        self.model_name = "Runware (PAID)"

    def generate_image(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> List[ImageResult]:
        if not self.api_key:
            raise ValueError("API key required for Runware")
            
        if options is None:
            options = {}

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "positivePrompt": prompt,
            "model": options.get('model', 'civitai:4384@128713'),
            "numberResults": 1,
            "height": options.get('height', 512),
            "width": options.get('width', 512),
            "outputFormat": "PNG"
        }
        
        if options.get('negative_prompt'):
            payload["negativePrompt"] = options['negative_prompt']

        try:
            response = requests.post(
                f"{self.base_url}/inference/generate",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if 'data' in data and len(data['data']) > 0:
                    image_url = data['data'][0].get('imageURL')
                    
                    if image_url:
                        img_response = requests.get(image_url, timeout=30)
                        if img_response.status_code == 200:
                            return [ImageResult(
                                image_data=img_response.content,
                                image_url=image_url,
                                prompt=prompt,
                                model_used="Runware SDXL"
                            )]
                
                raise ValueError("No image data in response")
            else:
                logger.error(f"Runware API error: {response.text}")
                raise requests.exceptions.RequestException(f"API Error: {response.text}")

        except Exception as e:
            logger.error(f"Error with Runware API: {e}")
            raise e

# --- Replicate Client (PAID - Pay per use) ---

class ReplicateClient(BaseImageGenerationModel):
    """
    Client for Replicate - Access to FLUX.1 and other top models
    Pay per use, excellent quality
    """
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://api.replicate.com/v1"
        self.model_name = "Replicate (PAID)"

    def generate_image(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> List[ImageResult]:
        if not self.api_key:
            raise ValueError("API key required for Replicate")
            
        if options is None:
            options = {}

        headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }
        
        model_version = options.get('model', 'black-forest-labs/flux-schnell')
        
        payload = {
            "version": model_version,
            "input": {
                "prompt": prompt,
                "width": options.get('width', 512),
                "height": options.get('height', 512),
                "num_outputs": 1
            }
        }

        try:
            response = requests.post(
                f"{self.base_url}/predictions",
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 201:
                prediction = response.json()
                prediction_url = prediction['urls']['get']
                
                max_attempts = 30
                for attempt in range(max_attempts):
                    time.sleep(2)
                    
                    status_response = requests.get(prediction_url, headers=headers)
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        
                        if status_data['status'] == 'succeeded':
                            output = status_data.get('output')
                            if output and len(output) > 0:
                                image_url = output[0] if isinstance(output, list) else output
                                
                                img_response = requests.get(image_url, timeout=30)
                                if img_response.status_code == 200:
                                    return [ImageResult(
                                        image_data=img_response.content,
                                        image_url=image_url,
                                        prompt=prompt,
                                        model_used="Replicate FLUX.1"
                                    )]
                        
                        elif status_data['status'] == 'failed':
                            raise ValueError(f"Generation failed: {status_data.get('error')}")
                
                raise TimeoutError("Image generation timed out")
            else:
                logger.error(f"Replicate API error: {response.text}")
                raise requests.exceptions.RequestException(f"API Error: {response.text}")

        except Exception as e:
            logger.error(f"Error with Replicate API: {e}")
            raise e

# --- Stability AI Client (PAID) ---

class StabilityAiClient(BaseImageGenerationModel):
    """
    Client for Stability AI - Premium service
    High quality but more expensive than alternatives
    """
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://api.stability.ai/v2beta"
        self.model_name = "Stability AI (PAID)"

    def generate_image(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> List[ImageResult]:
        if not self.api_key:
            raise ValueError("API key required for Stability AI")
            
        if options is None:
            options = {}

        endpoint_url = f"{self.base_url}/stable-image/generate/core"

        payload = {
            "prompt": prompt,
            "output_format": "png",
            "aspect_ratio": "1:1"
        }
        
        negative_prompt = options.get('negative_prompt')
        if negative_prompt:
            payload["negative_prompt"] = negative_prompt

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "image/*"
        }

        try:
            response = requests.post(endpoint_url, headers=headers, data=payload, timeout=60)
            
            if response.status_code == 200:
                return [ImageResult(
                    image_data=response.content,
                    prompt=prompt,
                    model_used="Stability AI Core"
                )]
            else:
                logger.error(f"Stability AI API error: {response.status_code} - {response.text}")
                raise requests.exceptions.RequestException(f"API Error {response.status_code}: {response.text}")

        except Exception as e:
            logger.error(f"Error with Stability AI: {e}")
            raise e

# --- DeepAI Client (PAID) ---

class DeepAIClient(BaseImageGenerationModel):
    """
    Client for DeepAI - PAID with no API key required initially
    """
    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self.base_url = "https://api.deepai.org/api/text2img"
        self.model_name = "DeepAI (PAID)"

    def generate_image(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> List[ImageResult]:
        if options is None:
            options = {}
            
        headers = {}
        if self.api_key:
            headers["api-key"] = self.api_key
        
        data = {
            'text': prompt,
            'grid_size': options.get('grid_size', '1'),
            'width': options.get('width', 512),
            'height': options.get('height', 512)
        }
        
        try:
            response = requests.post(self.base_url, data=data, headers=headers, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                image_url = result.get('output_url')
                
                if image_url:
                    # Download the image
                    img_response = requests.get(image_url, timeout=30)
                    if img_response.status_code == 200:
                        return [ImageResult(
                            image_data=img_response.content,
                            image_url=image_url,
                            prompt=prompt,
                            model_used="DeepAI"
                        )]
                
                raise ValueError("No image URL in response")
            else:
                logger.error(f"DeepAI API error: {response.text}")
                raise requests.exceptions.RequestException(f"API Error: {response.text}")
                
        except Exception as e:
            logger.error(f"Error with DeepAI API: {e}")
            raise e

# --- API Factory ---

def get_api_client(provider: str, api_key: str = None):
    """Factory function to get the appropriate API client"""
    clients = {
        'placeholder': lambda: PlaceholderClient(),
        'pollinations': lambda: PollinationsClient(),
        'huggingface': lambda: HuggingFaceClient(api_key),
        'gemini': lambda: GeminiClient(api_key) if api_key else None,
        'runware': lambda: RunwareClient(api_key) if api_key else None,
        'replicate': lambda: ReplicateClient(api_key) if api_key else None,
        'stability': lambda: StabilityAiClient(api_key) if api_key else None,
        'deepai': lambda: DeepAIClient(api_key) if api_key else None,
    }
    
    client_factory = clients.get(provider)
    if client_factory:
        client = client_factory()
        if client:
            return client
        else:
            raise ValueError(f"API key required for {provider}")
    else:
        raise ValueError(f"Unknown provider: {provider}")

# List of available providers - UPDATED
AVAILABLE_PROVIDERS = {
    # 'placeholder': {
    #     'name': 'Placeholder (Demo)',
    #     'description': 'Simple placeholder images for testing only',
    #     'free': True,
    #     'requires_api_key': False,
    #     'quality': 1
    # },
    'pollinations': {
        'name': 'Pollinations.ai',
        'description': 'Unlimited free AI images, no API key needed',
        'free': True,
        'requires_api_key': False,
        'quality': 3
    },
    'huggingface': {
        'name': 'Hugging Face',
        'description': 'Free FLUX & Stable Diffusion models, optional API key',
        'free': True,
        'requires_api_key': False,
        'quality': 4
    },
    'gemini': {
        'name': 'Google Gemini (Nano Banana)',
        'description': 'High quality, 1500 free requests/day, requires API key',
        'free': True,
        'requires_api_key': True,
        'quality': 5
    },
    'runware': {
        'name': 'Runware',
        'description': 'Very affordable ($0.002/image), multiple models',
        'free': False,
        'requires_api_key': True,
        'quality': 4
    },
    'replicate': {
        'name': 'Replicate (FLUX.1)',
        'description': 'Pay per use (~$0.003/image), top quality',
        'free': False,
        'requires_api_key': True,
        'quality': 5
    },
    'stability': {
        'name': 'Stability AI',
        'description': 'Premium quality ($0.01-0.04/image)',
        'free': False,
        'requires_api_key': True,
        'quality': 5
    },
    'deepai': {
        'name': 'DeepAI',
        'description': 'Paid service ($5/500 images)',
        'free': False,
        'requires_api_key': True,
        'quality': 3
    }
}