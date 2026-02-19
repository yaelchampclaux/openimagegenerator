"""
AI Clients - VERSION FINALE QUI MARCHE
Utilise les SDK et les clés API
"""
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
    """Represents the result of an image generation request."""
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
    """Abstract base class for AI image generation models."""
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.model_name = "Unknown Model"

    @abc.abstractmethod
    def generate_image(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> List[ImageResult]:
        pass


# === GRATUIT - Pollinations AVEC CLÉ API ===

class PollinationsClient(BaseImageGenerationModel):
    """
    Pollinations.ai - FREE, no API key needed
    Old endpoint works: https://image.pollinations.ai/prompt/
    """
    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self.base_url = "https://image.pollinations.ai/prompt"
        self.model_name = "Pollinations.ai"
        
        # Old endpoint doesn't support model parameter
        self.models = {
            "default": "default",
        }

    def generate_image(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> List[ImageResult]:
        if options is None:
            options = {}
            
        width = options.get('width', 512)
        height = options.get('height', 512)
        
        import urllib.parse
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"{self.base_url}/{encoded_prompt}"
        
        params = {
            'width': width,
            'height': height,
            'nologo': 'true',
        }
        
        # Cloudflare blocks curl - use browser headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://pollinations.ai/',
        }
        
        try:
            logger.info(f"Pollinations: size={width}x{height}, url={url}")
            response = requests.get(url, params=params, headers=headers, timeout=60)
            
            if response.status_code == 200 and len(response.content) > 5000:
                return [ImageResult(
                    image_data=response.content,
                    prompt=prompt,
                    model_used="Pollinations"
                )]
            elif response.status_code == 200:
                raise Exception(f"Pollinations returned invalid image ({len(response.content)} bytes) - server may be overloaded, retry later")
            else:
                error_text = response.text[:300]
                logger.error(f"Pollinations error {response.status_code}: {error_text}")
                raise Exception(f"API Error: {response.status_code} - {error_text}")
                
        except Exception as e:
            logger.error(f"Pollinations error: {e}")
            raise e

    def get_available_models(self):
        return [
            {"key": k, "name": k.replace('-', ' ').title()} 
            for k in self.models.keys()
        ]


# === GRATUIT - HuggingFace AVEC SDK ===

class HuggingFaceClient(BaseImageGenerationModel):
    """
    Hugging Face - Uses SDK for stability
    Requires: pip install huggingface_hub
    """
    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self.model_name = "Hugging Face (FREE)"
        
        # Check if SDK is available
        try:
            from huggingface_hub import InferenceClient
            self.client = InferenceClient(token=api_key) if api_key else InferenceClient()
            self.use_sdk = True
        except ImportError:
            logger.warning("huggingface_hub not installed, will try HTTP API")
            self.base_url = "https://api-inference.huggingface.co/models"
            self.use_sdk = False
        
        # FREE models - only confirmed working
        self.models = {
            "sdxl-lightning": "ByteDance/SDXL-Lightning",
        }

    def generate_image(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> List[ImageResult]:
        if options is None:
            options = {}
            
        model_key = options.get('model', 'sdxl-lightning')
        model_id = self.models.get(model_key, self.models['sdxl-lightning'])
        
        if self.use_sdk:
            # Use SDK (preferred)
            try:
                logger.info(f"HuggingFace SDK: model={model_id}")
                from huggingface_hub import InferenceClient
                from io import BytesIO
                
                image = self.client.text_to_image(prompt, model=model_id)
                
                # Convert PIL to bytes
                buffer = BytesIO()
                image.save(buffer, format='PNG')
                image_data = buffer.getvalue()
                
                return [ImageResult(
                    image_data=image_data,
                    prompt=prompt,
                    model_used=f"HuggingFace {model_key}"
                )]
            except Exception as e:
                logger.error(f"HuggingFace SDK error: {e}")
                raise e
        else:
            # Fallback to HTTP API
            url = f"{self.base_url}/{model_id}"
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            payload = {"inputs": prompt}
            
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=120)
                
                if response.status_code == 200:
                    return [ImageResult(
                        image_data=response.content,
                        prompt=prompt,
                        model_used=f"HuggingFace {model_key}"
                    )]
                elif response.status_code == 503:
                    raise Exception("Model loading. Wait 30-60s and retry.")
                else:
                    error_text = response.text[:300]
                    logger.error(f"HuggingFace HTTP error {response.status_code}: {error_text}")
                    raise Exception(f"API Error {response.status_code}. Install huggingface_hub: pip install huggingface_hub")
            except Exception as e:
                logger.error(f"HuggingFace error: {e}")
                raise e

    def get_available_models(self):
        return [
            {"key": k, "name": k.replace('-', ' ').title()} 
            for k in self.models.keys()
        ]


# === GRATUIT - Subnp (si leur serveur se répare) ===

class SubnpClient(BaseImageGenerationModel):
    """
    Subnp - FREE (streaming SSE API)
    """
    def __init__(self):
        super().__init__()
        self.base_url = "https://subnp.com/api/free/generate"
        self.model_name = "Subnp"
        self.models = {"magic": "magic"}  # flux and turbo broken server-side

    def generate_image(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> List[ImageResult]:
        if options is None:
            options = {}
        
        model = options.get('model', 'flux')
        
        try:
            payload = {"prompt": prompt, "model": model}
            
            logger.info(f"Subnp: Requesting model={model}, prompt={prompt[:50]}...")
            
            response = requests.post(
                self.base_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                stream=True,
                timeout=120
            )
            
            if response.status_code != 200:
                error_text = response.text[:500]
                logger.error(f"Subnp: HTTP {response.status_code}: {error_text}")
                raise Exception(f"API Error {response.status_code}: {error_text}")
            
            # Parse SSE selon leur doc
            image_url = None
            buffer = ""
            line_count = 0
            
            for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                if chunk:
                    buffer += chunk
                    lines = buffer.split('\n')
                    buffer = lines[-1]  # Keep incomplete line
                    
                    for line in lines[:-1]:
                        line = line.strip()
                        line_count += 1
                        
                        if line.startswith('data: '):
                            try:
                                data_json = line[6:]
                                data = json.loads(data_json)
                                
                                logger.info(f"Subnp: Line {line_count} status={data.get('status')}, model={model}")
                                
                                if data.get('status') == 'complete':
                                    image_url = data.get('imageUrl')
                                    if image_url:
                                        logger.info(f"Subnp: Image URL received for {model}: {image_url}")
                                        break
                                elif data.get('status') == 'error':
                                    error_msg = data.get('message', 'Unknown error')
                                    error_detail = data.get('error', '')
                                    logger.error(f"Subnp: Error status for {model}: {error_msg} - {error_detail}")
                                    raise Exception(f"Subnp: {error_msg}")
                            except json.JSONDecodeError as je:
                                logger.warning(f"Subnp: JSON decode error on line {line_count}: {data_json[:100]}")
                                continue
                    
                    if image_url:
                        break
            
            if not image_url:
                logger.error(f"Subnp: No image URL after {line_count} lines for model={model}")
                raise ValueError("No image URL from Subnp")
            
            # Download image
            logger.info(f"Subnp: Downloading image from {image_url}")
            img_response = requests.get(image_url, timeout=30)
            if img_response.status_code == 200:
                logger.info(f"Subnp: Downloaded {len(img_response.content)} bytes for {model}")
                return [ImageResult(
                    image_data=img_response.content,
                    prompt=prompt,
                    model_used=f"Subnp {model}"
                )]
            raise Exception(f"Download failed: {img_response.status_code}")
                
        except Exception as e:
            logger.error(f"Subnp error for model={model}: {e}")
            raise e

    def get_available_models(self):
        return [{"key": k, "name": f"Subnp {k.title()}"} for k in self.models.keys()]


# === GRATUIT - Gemini (si clé fournie) ===

class GeminiClient(BaseImageGenerationModel):
    """Google Gemini - Nécessite clé AI Studio"""
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.model_name = "Google Gemini"

    def generate_image(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> List[ImageResult]:
        if not self.api_key:
            raise ValueError("API key required for Gemini")
            
        if options is None:
            options = {}

        model = "gemini-2.5-flash-image-preview"
        url = f"{self.base_url}/{model}:generateContent"
        
        headers = {
            "x-goog-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
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
                                model_used="Gemini 2.5 Flash"
                            )]
                raise ValueError("No image in response")
            else:
                raise Exception(f"API Error: {response.text}")
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            raise e


# === GRATUIT - Placeholder ===

class PlaceholderClient(BaseImageGenerationModel):
    """Placeholder - test only"""
    def __init__(self):
        super().__init__()
        self.model_name = "Placeholder"

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
                    model_used="Placeholder"
                )]
            return []
        except Exception as e:
            logger.error(f"Placeholder error: {e}")
            return []


# === PAYANT - Runware ===

class RunwareClient(BaseImageGenerationModel):
    """Runware - PAID"""
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://api.runware.ai/v1"
        self.model_name = "Runware"

    def generate_image(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> List[ImageResult]:
        if not self.api_key:
            raise ValueError("API key required")
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
                                prompt=prompt,
                                model_used="Runware"
                            )]
                raise ValueError("No image in response")
            else:
                raise Exception(f"API Error: {response.text}")
        except Exception as e:
            logger.error(f"Runware error: {e}")
            raise e


# === PAYANT - Replicate ===

class ReplicateClient(BaseImageGenerationModel):
    """Replicate - PAID"""
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://api.replicate.com/v1"
        self.model_name = "Replicate"

    def generate_image(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> List[ImageResult]:
        if not self.api_key:
            raise ValueError("API key required")
        if options is None:
            options = {}

        headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "version": options.get('model', 'black-forest-labs/flux-schnell'),
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
                
                for _ in range(30):
                    time.sleep(2)
                    status_response = requests.get(prediction_url, headers=headers)
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        if status_data['status'] == 'succeeded':
                            output = status_data.get('output')
                            if output:
                                image_url = output[0] if isinstance(output, list) else output
                                img_response = requests.get(image_url, timeout=30)
                                if img_response.status_code == 200:
                                    return [ImageResult(
                                        image_data=img_response.content,
                                        prompt=prompt,
                                        model_used="Replicate"
                                    )]
                        elif status_data['status'] == 'failed':
                            raise ValueError(f"Failed: {status_data.get('error')}")
                raise TimeoutError("Timed out")
            else:
                raise Exception(f"API Error: {response.text}")
        except Exception as e:
            logger.error(f"Replicate error: {e}")
            raise e


# === PAYANT - Stability AI ===

class StabilityAiClient(BaseImageGenerationModel):
    """Stability AI - PAID"""
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.base_url = "https://api.stability.ai/v2beta"
        self.model_name = "Stability AI"

    def generate_image(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> List[ImageResult]:
        if not self.api_key:
            raise ValueError("API key required")
        if options is None:
            options = {}

        endpoint_url = f"{self.base_url}/stable-image/generate/core"
        payload = {
            "prompt": prompt,
            "output_format": "png",
            "aspect_ratio": "1:1"
        }
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
                    model_used="Stability AI"
                )]
            else:
                raise Exception(f"API Error: {response.text}")
        except Exception as e:
            logger.error(f"Stability error: {e}")
            raise e


# === PAYANT - DeepAI ===

class DeepAIClient(BaseImageGenerationModel):
    """DeepAI - PAID"""
    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self.base_url = "https://api.deepai.org/api/text2img"
        self.model_name = "DeepAI"

    def generate_image(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> List[ImageResult]:
        if options is None:
            options = {}
        headers = {}
        if self.api_key:
            headers["api-key"] = self.api_key
        data = {'text': prompt}
        
        try:
            response = requests.post(self.base_url, data=data, headers=headers, timeout=60)
            if response.status_code == 200:
                result = response.json()
                image_url = result.get('output_url')
                if image_url:
                    img_response = requests.get(image_url, timeout=30)
                    if img_response.status_code == 200:
                        return [ImageResult(
                            image_data=img_response.content,
                            prompt=prompt,
                            model_used="DeepAI"
                        )]
                raise ValueError("No image URL")
            else:
                raise Exception(f"API Error: {response.text}")
        except Exception as e:
            logger.error(f"DeepAI error: {e}")
            raise e


# === FACTORY ===

def get_api_client(provider: str, api_key: str = None):
    """Factory function"""
    clients = {
        'placeholder': lambda: PlaceholderClient(),
        'segmind': lambda: SegmindClient(api_key) if api_key else None,
        'prodia': lambda: ProdiaClient(),
        'pollinations': lambda: PollinationsClient(api_key),
        'huggingface': lambda: HuggingFaceClient(api_key),
        'subnp': lambda: SubnpClient(),
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
        raise ValueError(f"API key required for {provider}")
    raise ValueError(f"Unknown provider: {provider}")


def check_all_providers(api_keys: dict = None):
    """Check health of all providers"""
    if api_keys is None:
        api_keys = {}
    
    results = {}
    
    for provider_name in AVAILABLE_PROVIDERS.keys():
        try:
            api_key = api_keys.get(provider_name)
            provider_info = AVAILABLE_PROVIDERS[provider_name]
            
            if provider_info.get('requires_api_key') and not api_key:
                results[provider_name] = {
                    'status': 'skipped',
                    'message': 'API key required',
                    'healthy': False
                }
                continue
            
            client = get_api_client(provider_name, api_key)
            results[provider_name] = {
                'status': 'available',
                'message': 'Client initialized',
                'healthy': True
            }
            
        except Exception as e:
            results[provider_name] = {
                'status': 'error',
                'message': str(e),
                'healthy': False
            }
    
    return results




class SegmindClient(BaseImageGenerationModel):
    """
    Segmind.com - FREE tier: 100 images/day
    Official API, stable, multiple models
    """
    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self.base_url = "https://api.segmind.com/v1"
        self.model_name = "Segmind"
        
        # Free tier models
        self.models = {
            "sdxl": "sdxl1.0-txt2img",
            "sd-1.5": "sd1.5-txt2img",
            "kandinsky": "kandinsky-2.2-txt2img",
        }

    def generate_image(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> List[ImageResult]:
        if options is None:
            options = {}
            
        width = options.get('width', 1024)
        height = options.get('height', 1024)
        model_key = options.get('model', 'sdxl')
        model_endpoint = self.models.get(model_key, self.models['sdxl'])
        
        url = f"{self.base_url}/{model_endpoint}"
        
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "negative_prompt": options.get('negative_prompt', ''),
            "samples": 1,
            "scheduler": "UniPC",
            "num_inference_steps": 25,
            "guidance_scale": options.get('cfg_scale', 7.5),
            "seed": options.get('seed', -1),
            "img_width": width,
            "img_height": height,
            "base64": False
        }
        
        try:
            logger.info(f"Segmind: model={model_key}, size={width}x{height}")
            response = requests.post(url, json=payload, headers=headers, timeout=120)
            
            if response.status_code == 200:
                return [ImageResult(
                    image_data=response.content,
                    prompt=prompt,
                    model_used=f"Segmind {model_key}"
                )]
            else:
                error_text = response.text[:300]
                logger.error(f"Segmind error {response.status_code}: {error_text}")
                raise Exception(f"Segmind API Error: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Segmind error: {e}")
            raise e

    def get_available_models(self):
        return [
            {"key": k, "name": k.upper().replace('-', ' ')} 
            for k in self.models.keys()
        ]


class ProdiaClient(BaseImageGenerationModel):
    """
    Prodia.com - Completely FREE (no key needed)
    Slower but unlimited and stable
    """
    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self.base_url = "https://api.prodia.com/v1"
        self.model_name = "Prodia"
        
        # Free models
        self.models = {
            "sdxl": "sdxl",
            "dreamshaper": "dreamshaper_8",
            "realistic-vision": "realisticVisionV51_v51VAE",
        }

    def generate_image(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> List[ImageResult]:
        if options is None:
            options = {}
            
        model_key = options.get('model', 'sdxl')
        model_id = self.models.get(model_key, self.models['sdxl'])
        
        # Step 1: Submit generation job
        url = f"{self.base_url}/sd/generate"
        
        payload = {
            "prompt": prompt,
            "model": model_id,
            "negative_prompt": options.get('negative_prompt', ''),
            "steps": 25,
            "cfg_scale": options.get('cfg_scale', 7),
            "seed": options.get('seed', -1),
            "sampler": "DPM++ 2M Karras",
        }
        
        try:
            logger.info(f"Prodia: Submitting job, model={model_key}")
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code != 200:
                raise Exception(f"Failed to submit job: {response.status_code}")
            
            data = response.json()
            job_id = data.get('job')
            
            if not job_id:
                raise Exception("No job ID returned")
            
            # Step 2: Poll for completion
            status_url = f"{self.base_url}/job/{job_id}"
            max_wait = 120  # 2 minutes max
            waited = 0
            
            while waited < max_wait:
                time.sleep(5)
                waited += 5
                
                status_response = requests.get(status_url, timeout=10)
                status_data = status_response.json()
                
                status = status_data.get('status')
                logger.info(f"Prodia: Job {job_id} status={status}, waited={waited}s")
                
                if status == 'succeeded':
                    image_url = status_data.get('imageUrl')
                    if not image_url:
                        raise Exception("No image URL in response")
                    
                    # Download image
                    img_response = requests.get(image_url, timeout=30)
                    return [ImageResult(
                        image_data=img_response.content,
                        prompt=prompt,
                        model_used=f"Prodia {model_key}"
                    )]
                elif status == 'failed':
                    raise Exception("Generation failed")
            
            raise Exception("Timeout waiting for generation")
            
        except Exception as e:
            logger.error(f"Prodia error: {e}")
            raise e

    def get_available_models(self):
        return [
            {"key": k, "name": k.replace('-', ' ').title()} 
            for k in self.models.keys()
        ]


# AVAILABLE_PROVIDERS
AVAILABLE_PROVIDERS = {
    'huggingface': {
        'name': 'Hugging Face',
        'description': 'FREE with API key - SDXL Lightning',
        'free': True,
        'requires_api_key': True,
        'quality': 4,
        'speed': 'medium'
    },
    'subnp': {
        'name': 'Subnp',
        'description': 'FREE - Magic model',
        'free': True,
        'requires_api_key': False,
        'quality': 3,
        'speed': 'medium'
    },
    'pollinations': {
        'name': 'Pollinations.ai',
        'description': 'FREE (currently unstable)',
        'free': True,
        'requires_api_key': False,
        'quality': 4,
        'speed': 'fast'
    },
    'segmind': {
        'name': 'Segmind',
        'description': 'FREE tier ended - needs credits',
        'free': False,
        'requires_api_key': True,
        'quality': 4,
        'speed': 'fast'
    },
    'prodia': {
        'name': 'Prodia',
        'description': 'API changed - currently broken',
        'free': False,
        'requires_api_key': False,
        'quality': 3,
        'speed': 'slow'
    },
    'gemini': {
        'name': 'Google Gemini',
        'description': 'PAID - AI Studio key',
        'free': False,
        'requires_api_key': True,
        'quality': 5,
        'speed': 'fast'
    },
    'runware': {
        'name': 'Runware',
        'description': 'PAID ($0.002/image)',
        'free': False,
        'requires_api_key': True,
        'quality': 4,
        'speed': 'fast'
    },
    'replicate': {
        'name': 'Replicate',
        'description': 'PAID (~$0.003/image)',
        'free': False,
        'requires_api_key': True,
        'quality': 5,
        'speed': 'medium'
    },
    'stability': {
        'name': 'Stability AI',
        'description': 'PAID ($0.01-0.04/image)',
        'free': False,
        'requires_api_key': True,
        'quality': 5,
        'speed': 'fast'
    },
    'deepai': {
        'name': 'DeepAI',
        'description': 'PAID ($5/500 images)',
        'free': False,
        'requires_api_key': True,
        'quality': 3,
        'speed': 'fast'
    },
}
