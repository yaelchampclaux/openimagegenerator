from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, JsonResponse
from django.views.decorators.http import require_http_methods
from .models import GeneratedImage
# Import the new multi-API client system
from .ai_clients import get_api_client, AVAILABLE_PROVIDERS, ImageResult
from django.conf import settings
from typing import List
import base64
import logging
import json

logger = logging.getLogger(__name__)

# --- Main page view ---
def image_generator_view(request):
    generated_images = GeneratedImage.objects.all() 
    
    # Sérialiser les images pour JavaScript
    images_data = []
    for img in generated_images:
        images_data.append({
            'id': img.id,
            'image_data': base64.b64encode(img.image_data).decode('utf-8') if img.image_data else '',
            'prompt': img.prompt,
            'negative_prompt': img.negative_prompt or '',
            'model_used': img.model_used or 'Unknown',
            'provider': img.provider or 'unknown',
            'width': img.width,
            'height': img.height,
            'aspect_ratio': img.aspect_ratio,
            'output_format': img.output_format,
            'style_preset': img.style_preset or '',
            'seed': img.seed,
            'cfg_scale': img.cfg_scale,
        })
    
    context = {
        'generated_images': generated_images,
        'images_json': json.dumps(images_data),  # Ajouter ceci
        'available_providers': AVAILABLE_PROVIDERS,
        'default_provider': 'huggingface'
    }
    return render(request, 'you_image_generator/generator.html', context)

# --- API endpoint for generation ---
@require_http_methods(["POST"])
def generate_image_api(request):
    """
    API endpoint to receive a prompt, generate image(s), and save them.
    Returns a JSON response with details of the generated image(s).
    """
    if request.method == 'POST':
        try:
            # Get form data
            prompt = request.POST.get('prompt')
            if not prompt or len(prompt.strip()) < 3:
                return JsonResponse({'error': 'Prompt must be at least 3 characters long'}, status=400)

            # Get provider selection
            provider = request.POST.get('provider', 'huggingface')
            hf_model = request.POST.get('hf_model', 'sdxl-lightning')
            subnp_model = request.POST.get('subnp_model', 'magic')
            pollinations_model = request.POST.get('pollinations_model', 'default')
            segmind_model = request.POST.get('segmind_model', 'sdxl')
            prodia_model = request.POST.get('prodia_model', 'sdxl')
            cloudflare_model = request.POST.get('cloudflare_model', 'sdxl')
            aihorde_model = request.POST.get('aihorde_model', 'sdxl')
            if provider not in AVAILABLE_PROVIDERS:
                return JsonResponse({'error': f'Unknown provider: {provider}'}, status=400)

            # Get other parameters
            negative_prompt = request.POST.get('negative_prompt', '')
            width = int(request.POST.get('width', 512))
            height = int(request.POST.get('height', 512))
            
            # Validate dimensions (limit to reasonable sizes)
            width = min(max(width, 256), 1024)
            height = min(max(height, 256), 1024)

            style_preset = request.POST.get('style_preset', '')

            logger.info(f"Generating image with provider: {provider}, prompt: {prompt[:50]}...")

            # Get API key based on provider
            api_key = None
            if provider == 'stability':
                api_key = settings.STABILITY_AI_API_KEY
                if not api_key:
                    return JsonResponse({'error': 'Stability AI API Key not configured'}, status=500)
            elif provider == 'gemini':
                api_key = settings.GEMINI_API_KEY
                if not api_key:
                    return JsonResponse({'error': 'Gemini API Key not configured. Get one at https://aistudio.google.com/app/apikey'}, status=500)
            elif provider == 'runware':
                api_key = settings.RUNWARE_API_KEY
                if not api_key:
                    return JsonResponse({'error': 'Runware API Key not configured'}, status=500)
            elif provider == 'replicate':
                api_key = settings.REPLICATE_API_KEY
                if not api_key:
                    return JsonResponse({'error': 'Replicate API Key not configured'}, status=500)
            elif provider == 'huggingface':
                api_key = getattr(settings, 'HUGGINGFACE_API_KEY', None)
            elif provider == 'cloudflare':
                api_key = getattr(settings, 'CLOUDFLARE_API_KEY', None)
                account_id = getattr(settings, 'CLOUDFLARE_ACCOUNT_ID', None)
            elif provider == 'aihorde':
                api_key = getattr(settings, 'AIHORDE_API_KEY', None) or "0000000000"  # Public key
            elif provider == 'segmind':
                api_key = getattr(settings, 'SEGMIND_API_KEY', None)
            elif provider == 'pollinations':
                api_key = getattr(settings, 'POLLINATION_API_KEY', None)
            elif provider == 'deepai':
                api_key = getattr(settings, 'DEEPAI_API_KEY', None)
            # subnp, prodia and placeholder don't need API keys

            # Initialize the AI client
            try:
                if provider == 'cloudflare':
                    ai_client = get_api_client(provider, api_key, account_id=account_id)
                else:
                    ai_client = get_api_client(provider, api_key)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)

            # Prepare options for generation
            generation_options = {
                'prompt': prompt,
                'negative_prompt': negative_prompt if negative_prompt else None,
                'width': width,
                'height': height,
            }
            
            # Provider-specific options
            if provider == 'stability':
                generation_options.update({
                    'engine': 'ultra',  # Use better quality
                    'cfg_scale': 7,
                    'steps': 20,  # Lower steps to save credits
                })

            # Assign model for each provider
            if provider == 'huggingface':
                generation_options['model'] = hf_model
            if provider == 'subnp':
                generation_options['model'] = subnp_model
            if provider == 'pollinations':
                generation_options['model'] = pollinations_model
            if provider == 'segmind':
                generation_options['model'] = segmind_model
            if provider == 'prodia':
                generation_options['model'] = prodia_model
            if provider == 'cloudflare':
                generation_options['model'] = cloudflare_model
            if provider == 'aihorde':
                generation_options['model'] = aihorde_model
            
            # Filter out None values
            generation_options = {k: v for k, v in generation_options.items() if v is not None}

            # Call the AI model
            try:
                image_results: List[ImageResult] = ai_client.generate_image(
                    prompt=prompt, 
                    options=generation_options
                )
            except Exception as e:
                logger.error(f"Error calling {provider} client: {e}")
                error_msg = str(e)
                # Provide helpful error messages
                if provider == 'stability' and '400' in error_msg:
                    error_msg = "Stability AI request failed. You might be out of credits or the prompt might be filtered."
                elif provider == 'huggingface' and 'loading' in error_msg.lower():
                    error_msg = "Hugging Face model is loading. Please try again in a few seconds."
                
                return JsonResponse({'error': f'Failed to generate image: {error_msg}'}, status=500)

            if not image_results:
                return JsonResponse({'error': 'No images were generated.'}, status=500)

            # Save the first generated image to database
            img_result = image_results[0]
            try:
                # Extraire toutes les métadonnées du formulaire
                width = int(request.POST.get('width', 1024))
                height = int(request.POST.get('height', 1024))
                aspect_ratio = request.POST.get('aspect_ratio', '1:1')
                output_format = request.POST.get('output_format', 'PNG')
                negative_prompt = request.POST.get('negative_prompt', '')
                seed = request.POST.get('seed', None)
                cfg_scale = request.POST.get('cfg_scale', None)
                
                # Convertir seed et cfg_scale en nombres si fournis
                if seed and seed.strip():
                    try:
                        seed = int(seed)
                    except ValueError:
                        seed = None
                else:
                    seed = None
                    
                if cfg_scale and cfg_scale.strip():
                    try:
                        cfg_scale = float(cfg_scale)
                    except ValueError:
                        cfg_scale = None
                else:
                    cfg_scale = None

                # Créer l'objet avec toutes les métadonnées
                new_db_image = GeneratedImage(
                    prompt=img_result.prompt,
                    negative_prompt=negative_prompt if negative_prompt else None,
                    model_used=img_result.model_used,
                    provider=provider,
                    image_data=img_result.image_data,
                    width=width,
                    height=height,
                    aspect_ratio=aspect_ratio,
                    output_format=output_format,
                    seed=seed,
                    cfg_scale=cfg_scale,
                    style_preset=style_preset if style_preset else None,
                )
                new_db_image.save()
                
                logger.info(f"Successfully saved image to database (ID: {new_db_image.id})")

                # Préparer la réponse avec toutes les métadonnées
                response_data = {
                    'id': new_db_image.id,
                    'prompt': new_db_image.prompt,
                    'model_used': new_db_image.model_used,
                    'provider': provider,
                    'width': width,
                    'height': height,
                    'aspect_ratio': aspect_ratio,
                    'output_format': output_format,
                    'image_base64': base64.b64encode(new_db_image.image_data).decode('utf-8'),
                    'content_type': f'image/{output_format.lower()}',
                    'created_at': new_db_image.created_at.isoformat(),
                }
                
                return JsonResponse(response_data, status=200)

            except Exception as e:
                logger.error(f"Error saving image to database: {e}")
                # Toujours retourner l'image même si la sauvegarde échoue
                response_data = {
                    'prompt': img_result.prompt,
                    'model_used': img_result.model_used,
                    'provider': provider,
                    'image_base64': base64.b64encode(img_result.image_data).decode('utf-8'),
                    'content_type': 'image/png',
                    'warning': 'Image generated but not saved to database'
                }
                return JsonResponse(response_data, status=200)

        except ValueError as e:
            logger.error(f"ValueError in generate_image_api: {e}")
            return JsonResponse({'error': f'Invalid input: {str(e)}'}, status=400)
        except Exception as e:
            # Catch any unexpected errors
            logger.error(f"Unexpected error in generate_image_api: {e}")
            return JsonResponse({'error': 'An internal server error occurred. Please try again.'}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@require_http_methods(["GET"])
def get_model_configuration(request):
    """API endpoint pour récupérer la configuration d'un modèle"""
    from .models_config import get_model_config
    
    provider = request.GET.get('provider', 'huggingface')
    hf_model = request.GET.get('hf_model', None)
    config = get_model_config(provider, hf_model)
    return JsonResponse(config)

@require_http_methods(["GET"])
def get_all_configurations(request):
    """Retourne toutes les configurations de modèles"""
    from .models_config import MODELS_CONFIG
    return JsonResponse(MODELS_CONFIG, safe=False)

# ===== Health Check Views (Added by repair script) =====
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from .ai_clients import check_all_providers, AVAILABLE_PROVIDERS
import logging

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def api_health_check(request):
    """
    API endpoint to check health of all providers
    
    GET /api/health/
    GET /api/health/?provider=gemini
    
    Returns:
    {
        "providers": {
            "pollinations": {
                "is_healthy": true,
                "message": "API working",
                "response_time": 1.23,
                "info": {...}
            },
            ...
        },
        "summary": {
            "total": 4,
            "working": 3,
            "broken": 1
        }
    }
    """
    try:
        # Get filter parameter
        provider_filter = request.GET.get('provider')
        
        # Gather API keys from settings
        api_keys = {
            'gemini': settings.GEMINI_API_KEY if hasattr(settings, 'GEMINI_API_KEY') else None,
            'huggingface': settings.HUGGINGFACE_API_KEY if hasattr(settings, 'HUGGINGFACE_API_KEY') else None,
            'pollinations': settings.POLLINATION_API_KEY if hasattr(settings, 'POLLINATION_API_KEY') else None,
            'deepai': settings.DEEPAI_API_KEY if hasattr(settings, 'DEEPAI_API_KEY') else None,
            'runware': settings.RUNWARE_API_KEY if hasattr(settings, 'RUNWARE_API_KEY') else None,
            'replicate': settings.REPLICATE_API_KEY if hasattr(settings, 'REPLICATE_API_KEY') else None,
            'stability': settings.STABILITY_AI_API_KEY if hasattr(settings, 'STABILITY_AI_API_KEY') else None,
        }
        
        # Perform health checks
        health_results = check_all_providers(api_keys)
        
        # Build response
        providers = {}
        working_count = 0
        broken_count = 0
        
        for provider_key, health in health_results.items():
            # Apply filter if specified
            if provider_filter and provider_key != provider_filter:
                continue
            
            provider_info = AVAILABLE_PROVIDERS.get(provider_key, {})
            
            providers[provider_key] = {
                'is_healthy': health.is_healthy,
                'message': health.message,
                'response_time': health.response_time,
                'last_checked': health.last_checked.isoformat(),
                'info': {
                    'name': provider_info.get('name', provider_key),
                    'description': provider_info.get('description', ''),
                    'free': provider_info.get('free', False),
                    'requires_api_key': provider_info.get('requires_api_key', False),
                    'quality': provider_info.get('quality', 0),
                    'speed': provider_info.get('speed', 'unknown'),
                    'has_api_key': bool(api_keys.get(provider_key))
                }
            }
            
            if health.is_healthy:
                working_count += 1
            else:
                broken_count += 1
        
        return JsonResponse({
            'success': True,
            'providers': providers,
            'summary': {
                'total': working_count + broken_count,
                'working': working_count,
                'broken': broken_count
            },
            'recommendations': get_health_recommendations(providers)
        }, status=200)
        
    except Exception as e:
        logger.error(f"Error in api_health_check: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def get_health_recommendations(providers: dict) -> list:
    """Generate recommendations based on health status"""
    recommendations = []
    
    # Check if any providers are working
    working_providers = [k for k, v in providers.items() if v['is_healthy']]
    
    if not working_providers:
        recommendations.append({
            'priority': 'high',
            'message': 'No providers are currently working. Start with Pollinations (no setup required).',
            'action': 'Select Pollinations in the provider dropdown'
        })
    
    # Check for broken providers with specific issues
    for provider_key, data in providers.items():
        if data['is_healthy']:
            continue
            
        message = data['message']
        provider_name = data['info']['name']
        
        if 'No API key' in message or 'API key required' in message:
            if provider_key == 'gemini':
                recommendations.append({
                    'priority': 'medium',
                    'provider': provider_key,
                    'message': f'{provider_name} requires FREE API key',
                    'action': 'Get FREE key from https://aistudio.google.com/apikey',
                    'steps': [
                        'Go to AI Studio (not Google Cloud)',
                        'Create API key',
                        'Add to .env: GEMINI_API_KEY=your_key'
                    ]
                })
        
        elif 'quota exceeded' in message.lower():
            recommendations.append({
                'priority': 'low',
                'provider': provider_key,
                'message': f'{provider_name} quota exceeded',
                'action': 'Wait until tomorrow or use Pollinations (unlimited)'
            })
        
        elif 'Invalid API key' in message:
            if provider_key == 'gemini':
                recommendations.append({
                    'priority': 'high',
                    'provider': provider_key,
                    'message': f'{provider_name} API key is invalid',
                    'action': 'Use AI Studio key (FREE), not Google Cloud key',
                    'fix_url': 'https://aistudio.google.com/apikey'
                })
    
    # Recommend setting up more providers if only one works
    if len(working_providers) == 1:
        recommendations.append({
            'priority': 'low',
            'message': 'You have only one working provider',
            'action': 'Consider setting up Gemini (FREE) as backup'
        })
    
    return recommendations


@require_http_methods(["GET"])
def get_working_providers(request):
    """
    Quick endpoint to get list of working providers
    
    GET /api/providers/working/
    
    Returns:
    {
        "working_providers": ["pollinations", "gemini"],
        "recommended": "pollinations"
    }
    """
    try:
        # Gather API keys
        api_keys = {
            'gemini': settings.GEMINI_API_KEY if hasattr(settings, 'GEMINI_API_KEY') else None,
            'huggingface': settings.HUGGINGFACE_API_KEY if hasattr(settings, 'HUGGINGFACE_API_KEY') else None,
            'pollinations': settings.POLLINATION_API_KEY if hasattr(settings, 'POLLINATION_API_KEY') else None,
        }
        
        # Quick health check
        health_results = check_all_providers(api_keys)
        
        # Get working providers
        working = [
            provider for provider, health in health_results.items()
            if health.is_healthy
        ]
        
        # Recommend the best one
        if 'pollinations' in working:
            recommended = 'pollinations'  # Fast and always works
        elif 'gemini' in working:
            recommended = 'gemini'  # High quality
        elif working:
            recommended = working[0]
        else:
            recommended = 'pollinations'  # Fallback even if check failed
        
        return JsonResponse({
            'success': True,
            'working_providers': working,
            'recommended': recommended,
            'count': len(working)
        }, status=200)
        
    except Exception as e:
        logger.error(f"Error in get_working_providers: {e}")
        # Return safe defaults
        return JsonResponse({
            'success': True,
            'working_providers': ['pollinations'],  # Safe fallback
            'recommended': 'pollinations',
            'count': 1,
            'note': 'Returned fallback due to error'
        }, status=200)


import time
import requests as http_requests

@require_http_methods(["GET"])
def test_free_apis(request):
    """
    Test all free APIs and return status + working models.
    GET /api/test-free/
    """
    results = {}
    
    # --- Test Pollinations (old endpoint, no key needed) ---
    try:
        start = time.time()
        # Cloudflare blocks curl - use browser headers
        headers_poll = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'image/*',
        }
        r = http_requests.get(
            "https://image.pollinations.ai/prompt/test",
            params={"width": 64, "height": 64, "nologo": "true"},
            headers=headers_poll,
            timeout=15
        )
        elapsed = round(time.time() - start, 1)
        
        if r.status_code == 200 and len(r.content) > 1000:
            results['pollinations'] = {
                'status': 'ok',
                'message': f'Working ({elapsed}s)',
                'models': ['default (no model selection)']
            }
        else:
            results['pollinations'] = {
                'status': 'error',
                'message': f'HTTP {r.status_code}, size {len(r.content)}',
                'models': []
            }
    except Exception as e:
        results['pollinations'] = {'status': 'error', 'message': str(e)[:100], 'models': []}
    
    # --- Test HuggingFace ---
    hf_key = getattr(settings, 'HUGGINGFACE_API_KEY', None)
    working_hf_models = []
    
    try:
        headers = {"Authorization": f"Bearer {hf_key}"} if hf_key else {}
        r = http_requests.post(
            "https://api-inference.huggingface.co/models/ByteDance/SDXL-Lightning",
            headers=headers,
            json={"inputs": "test"},
            timeout=30
        )
        if r.status_code == 200:
            working_hf_models.append('sdxl-lightning')
    except:
        pass
    
    # Fallback SDK
    if not working_hf_models and hf_key:
        try:
            from huggingface_hub import InferenceClient
            client = InferenceClient(token=hf_key)
            img = client.text_to_image("test", model="ByteDance/SDXL-Lightning")
            if img:
                working_hf_models.append('sdxl-lightning')
        except:
            pass
    
    results['huggingface'] = {
        'status': 'ok' if working_hf_models else 'error',
        'message': f'{len(working_hf_models)} model(s) working' if working_hf_models else 'No models working',
        'models': working_hf_models
    }
    
    # --- Test Subnp ---
    try:
        r = http_requests.post(
            "https://subnp.com/api/free/generate",
            json={"prompt": "test", "model": "magic"},
            headers={"Content-Type": "application/json"},
            stream=True,
            timeout=30
        )
        
        working_subnp = []
        if r.status_code == 200:
            import json as json_lib
            for line in r.iter_lines(decode_unicode=True):
                if line.startswith('data: '):
                    try:
                        data = json_lib.loads(line[6:])
                        if data.get('status') == 'complete' and data.get('imageUrl'):
                            working_subnp.append('magic')
                            break
                        elif data.get('status') == 'error':
                            break
                    except:
                        continue
        
        results['subnp'] = {
            'status': 'ok' if working_subnp else 'error',
            'message': 'magic working' if working_subnp else 'No models working',
            'models': working_subnp
        }
    except Exception as e:
        results['subnp'] = {'status': 'error', 'message': str(e)[:100], 'models': []}
    
    # --- Test Cloudflare AI ---
    cf_key = getattr(settings, 'CLOUDFLARE_API_KEY', None)
    cf_account = getattr(settings, 'CLOUDFLARE_ACCOUNT_ID', None)
    
    if cf_key and cf_account:
        try:
            headers_cf = {
                "Authorization": f"Bearer {cf_key}",
                "Content-Type": "application/json"
            }
            r = http_requests.post(
                f"https://api.cloudflare.com/client/v4/accounts/{cf_account}/ai/run/@cf/stabilityai/stable-diffusion-xl-base-1.0",
                headers=headers_cf,
                json={"prompt": "test"},
                timeout=30
            )
            if r.status_code == 200:
                results['cloudflare'] = {
                    'status': 'ok',
                    'message': 'Working (20-30 images/day)',
                    'models': ['sdxl', 'dreamshaper', 'stable-diffusion']
                }
            else:
                results['cloudflare'] = {
                    'status': 'error',
                    'message': f'HTTP {r.status_code}',
                    'models': []
                }
        except Exception as e:
            results['cloudflare'] = {'status': 'error', 'message': str(e)[:100], 'models': []}
    else:
        results['cloudflare'] = {'status': 'skipped', 'message': 'API key or Account ID not configured', 'models': []}
    
    # --- Test AI Horde ---
    try:
        headers_horde = {
            "apikey": "0000000000",
            "Content-Type": "application/json"
        }
        r = http_requests.post(
            "https://stablehorde.net/api/v2/generate/async",
            headers=headers_horde,
            json={
                "prompt": "test",
                "params": {"steps": 10, "width": 64, "height": 64},
                "models": ["stable_diffusion_xl"],
            },
            timeout=15
        )
        if r.status_code == 202:
            results['aihorde'] = {
                'status': 'ok',
                'message': 'Working (community powered, slow)',
                'models': ['sdxl', 'deliberate', 'dreamshaper']
            }
        else:
            results['aihorde'] = {
                'status': 'error',
                'message': f'HTTP {r.status_code}',
                'models': []
            }
    except Exception as e:
        results['aihorde'] = {'status': 'error', 'message': str(e)[:100], 'models': []}
    
    return JsonResponse({'results': results})



