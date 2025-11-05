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
        'default_provider': 'pollinations'
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
            provider = request.POST.get('provider', 'pollinations')
            hf_model = request.POST.get('hf_model', 'flux-schnell')
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
            elif provider == 'deepai':
                api_key = getattr(settings, 'DEEPAI_API_KEY', None)
            # pollinations and placeholder don't need API keys

            # Initialize the AI client
            try:
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

            if provider == 'huggingface':
                generation_options['model'] = hf_model
            
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
    
    provider = request.GET.get('provider', 'pollinations')
    hf_model = request.GET.get('hf_model', None)
    config = get_model_config(provider, hf_model)
    return JsonResponse(config)

@require_http_methods(["GET"])
def get_all_configurations(request):
    """Retourne toutes les configurations de modèles"""
    from .models_config import MODELS_CONFIG
    return JsonResponse(MODELS_CONFIG, safe=False)
