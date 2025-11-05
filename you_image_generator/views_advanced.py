# you_image_generator/views_advanced.py
"""
Advanced views for upscaling, search, and style presets
"""

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.utils import timezone
from .models import GeneratedImage
from .upscaler import upscale_image, upscale_image_api, REALESRGAN_AVAILABLE
from .styles import (
    get_style_preset,
    apply_style_to_prompt,
    get_styles_for_template,
    suggest_style_for_prompt
)
import logging
import json
import base64

logger = logging.getLogger(__name__)


# ============================================
# Upscaling Views
# ============================================

@require_http_methods(["POST"])
def upscale_image_view(request):
    """
    API endpoint to upscale an image
    
    POST /upscale/
    {
        "image_id": 123,
        "scale": 2
    }
    """
    try:
        data = json.loads(request.body)
        image_id = data.get('image_id')
        scale = int(data.get('scale', 2))
        
        if not image_id:
            return JsonResponse({'error': 'image_id is required'}, status=400)
        
        if scale not in [2, 4]:
            return JsonResponse({'error': 'scale must be 2 or 4'}, status=400)
        
        if not REALESRGAN_AVAILABLE:
            return JsonResponse({
                'error': 'Real-ESRGAN is not installed. Please install with: pip install realesrgan basicsr'
            }, status=500)
        
        # Perform upscaling
        result = upscale_image_api(image_id, scale)
        
        if result['success']:
            return JsonResponse(result, status=200)
        else:
            return JsonResponse(result, status=500)
            
    except Exception as e:
        logger.error(f"Error in upscale_image_view: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def batch_upscale_view(request):
    """
    Batch upscale multiple images
    
    POST /batch-upscale/
    {
        "image_ids": [1, 2, 3],
        "scale": 2
    }
    """
    try:
        data = json.loads(request.body)
        image_ids = data.get('image_ids', [])
        scale = int(data.get('scale', 2))
        
        if not image_ids:
            return JsonResponse({'error': 'image_ids is required'}, status=400)
        
        if not REALESRGAN_AVAILABLE:
            return JsonResponse({
                'error': 'Real-ESRGAN is not installed'
            }, status=500)
        
        from .upscaler import batch_upscale
        
        results = batch_upscale(image_ids, scale=scale, save_to_db=True)
        
        successful = [r for r in results if r is not None]
        
        return JsonResponse({
            'success': True,
            'total': len(image_ids),
            'successful': len(successful),
            'failed': len(image_ids) - len(successful),
            'upscaled_ids': [img.id for img in successful if img]
        }, status=200)
        
    except Exception as e:
        logger.error(f"Error in batch_upscale_view: {e}")
        return JsonResponse({'error': str(e)}, status=500)


# ============================================
# Search Views
# ============================================

@require_http_methods(["GET", "POST"])
def advanced_search_view(request):
    """
    Advanced search with filters
    
    GET/POST /search/
    Parameters:
    - q: text query
    - tags: comma-separated tags
    - provider: provider name
    - category: category name
    - min_width: minimum width
    - max_width: maximum width
    - date_from: start date
    - date_to: end date
    - is_favorite: boolean
    - style_preset: style preset key
    - page: page number
    - limit: results per page
    """
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
        else:
            data = request.GET.dict()
        
        # Build query
        queryset = GeneratedImage.objects.all()
        
        # Text search
        q = data.get('q', '').strip()
        if q:
            queryset = queryset.filter(
                Q(prompt__icontains=q) |
                Q(model_used__icontains=q) |
                Q(provider__icontains=q)
            )
        
        # Tag filter
        tags = data.get('tags', '')
        if tags:
            tag_list = [t.strip() for t in tags.split(',') if t.strip()]
            for tag in tag_list:
                queryset = queryset.filter(tags__contains=[tag])
        
        # Provider filter
        provider = data.get('provider')
        if provider:
            queryset = queryset.filter(provider=provider)
        
        # Category filter
        category = data.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Resolution filters
        min_width = data.get('min_width')
        if min_width:
            queryset = queryset.filter(width__gte=int(min_width))
        
        max_width = data.get('max_width')
        if max_width:
            queryset = queryset.filter(width__lte=int(max_width))
        
        # Date filters
        date_from = data.get('date_from')
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        
        date_to = data.get('date_to')
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)
        
        # Favorite filter
        is_favorite = data.get('is_favorite')
        if is_favorite:
            queryset = queryset.filter(is_favorite=True)
        
        # Style preset filter
        style_preset = data.get('style_preset')
        if style_preset:
            queryset = queryset.filter(style_preset=style_preset)
        
        # Sort
        sort_by = data.get('sort', '-created_at')
        queryset = queryset.order_by(sort_by)
        
        # Pagination
        page = int(data.get('page', 1))
        limit = int(data.get('limit', 50))
        paginator = Paginator(queryset, limit)
        page_obj = paginator.get_page(page)
        
        # Serialize results
        results = []
        for img in page_obj:
            results.append({
                'id': img.id,
                'prompt': img.prompt,
                'provider': img.provider,
                'model_used': img.model_used,
                'width': img.width,
                'height': img.height,
                'tags': img.tags,
                'category': img.category,
                'style_preset': img.style_preset,
                'is_favorite': img.is_favorite,
                'rating': img.rating,
                'created_at': img.created_at.isoformat(),
                'image_url': f'/image/{img.id}/',
            })
        
        return JsonResponse({
            'success': True,
            'count': paginator.count,
            'page': page,
            'total_pages': paginator.num_pages,
            'results': results
        }, status=200)
        
    except Exception as e:
        logger.error(f"Error in advanced_search_view: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def search_suggestions_view(request):
    """
    Get search suggestions based on partial query
    
    GET /search/suggestions/?q=cat
    """
    try:
        query = request.GET.get('q', '').strip()
        
        if not query or len(query) < 2:
            return JsonResponse({'suggestions': []}, status=200)
        
        # Get tag suggestions
        tag_suggestions = GeneratedImage.objects.values_list('tags', flat=True)
        all_tags = set()
        for tag_list in tag_suggestions:
            if tag_list:
                all_tags.update(tag_list)
        
        matching_tags = [
            tag for tag in all_tags
            if query.lower() in tag.lower()
        ][:5]
        
        # Get prompt suggestions
        prompt_suggestions = GeneratedImage.objects.filter(
            prompt__icontains=query
        ).values_list('prompt', flat=True)[:5]
        
        # Combine suggestions
        suggestions = list(matching_tags) + list(prompt_suggestions)
        
        return JsonResponse({
            'suggestions': suggestions[:10]
        }, status=200)
        
    except Exception as e:
        logger.error(f"Error in search_suggestions_view: {e}")
        return JsonResponse({'error': str(e)}, status=500)


# ============================================
# Style Preset Views
# ============================================

@require_http_methods(["GET"])
def get_style_presets_view(request):
    """
    Get all available style presets
    
    GET /styles/
    """
    try:
        styles = get_styles_for_template()
        return JsonResponse({
            'success': True,
            'styles': styles
        }, status=200)
        
    except Exception as e:
        logger.error(f"Error in get_style_presets_view: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def apply_style_view(request):
    """
    Apply a style preset to a prompt
    
    POST /styles/apply/
    {
        "prompt": "a red apple",
        "style": "realistic"
    }
    """
    try:
        data = json.loads(request.body)
        prompt = data.get('prompt', '')
        style_key = data.get('style', '')
        
        if not prompt:
            return JsonResponse({'error': 'prompt is required'}, status=400)
        
        if not style_key:
            return JsonResponse({'error': 'style is required'}, status=400)
        
        result = apply_style_to_prompt(prompt, style_key)
        
        return JsonResponse({
            'success': True,
            **result
        }, status=200)
        
    except Exception as e:
        logger.error(f"Error in apply_style_view: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def suggest_style_view(request):
    """
    Suggest a style based on prompt content
    
    POST /styles/suggest/
    {
        "prompt": "portrait of a person"
    }
    """
    try:
        data = json.loads(request.body)
        prompt = data.get('prompt', '')
        
        if not prompt:
            return JsonResponse({'error': 'prompt is required'}, status=400)
        
        suggested_style = suggest_style_for_prompt(prompt)
        
        return JsonResponse({
            'success': True,
            'suggested_style': suggested_style
        }, status=200)
        
    except Exception as e:
        logger.error(f"Error in suggest_style_view: {e}")
        return JsonResponse({'error': str(e)}, status=500)


# ============================================
# Favorites & Rating Views
# ============================================

@require_http_methods(["POST"])
def toggle_favorite_view(request):
    """
    Toggle favorite status of an image
    
    POST /favorites/toggle/
    {
        "image_id": 123
    }
    """
    try:
        data = json.loads(request.body)
        image_id = data.get('image_id')
        
        if not image_id:
            return JsonResponse({'error': 'image_id is required'}, status=400)
        
        img = get_object_or_404(GeneratedImage, id=image_id)
        img.is_favorite = not img.is_favorite
        
        if img.is_favorite:
            img.favorite_date = timezone.now()
        else:
            img.favorite_date = None
        
        img.save()
        
        return JsonResponse({
            'success': True,
            'is_favorite': img.is_favorite
        }, status=200)
        
    except Exception as e:
        logger.error(f"Error in toggle_favorite_view: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def rate_image_view(request):
    """
    Rate an image (1-5 stars)
    
    POST /rate/
    {
        "image_id": 123,
        "rating": 5
    }
    """
    try:
        data = json.loads(request.body)
        image_id = data.get('image_id')
        rating = data.get('rating')
        
        if not image_id:
            return JsonResponse({'error': 'image_id is required'}, status=400)
        
        if rating is None or rating not in [1, 2, 3, 4, 5]:
            return JsonResponse({'error': 'rating must be 1-5'}, status=400)
        
        img = get_object_or_404(GeneratedImage, id=image_id)
        img.rating = rating
        img.save()
        
        return JsonResponse({
            'success': True,
            'rating': rating
        }, status=200)
        
    except Exception as e:
        logger.error(f"Error in rate_image_view: {e}")
        return JsonResponse({'error': str(e)}, status=500)


# ============================================
# Statistics Views
# ============================================

@require_http_methods(["GET"])
def get_statistics_view(request):
    """
    Get usage statistics
    
    GET /stats/
    """
    try:
        from datetime import timedelta
        from django.db.models import Avg, Count
        
        # Time ranges
        now = timezone.now()
        last_7_days = now - timedelta(days=7)
        last_30_days = now - timedelta(days=30)
        
        stats = {
            'total_images': GeneratedImage.objects.count(),
            'last_7_days': GeneratedImage.objects.filter(
                created_at__gte=last_7_days
            ).count(),
            'last_30_days': GeneratedImage.objects.filter(
                created_at__gte=last_30_days
            ).count(),
            
            # By provider
            'by_provider': list(GeneratedImage.objects.values('provider').annotate(
                count=Count('id')
            ).order_by('-count')),
            
            # By category
            'by_category': list(GeneratedImage.objects.values('category').annotate(
                count=Count('id')
            ).order_by('-count')),
            
            # By style
            'by_style': list(GeneratedImage.objects.values('style_preset').annotate(
                count=Count('id')
            ).order_by('-count')),
            
            # Favorites
            'favorites_count': GeneratedImage.objects.filter(is_favorite=True).count(),
            
            # Average rating
            'average_rating': GeneratedImage.objects.filter(
                rating__isnull=False
            ).aggregate(Avg('rating'))['rating__avg'],
            
            # Resolution distribution
            'resolution_distribution': {
                '512x512': GeneratedImage.objects.filter(width=512, height=512).count(),
                '1024x1024': GeneratedImage.objects.filter(width=1024, height=1024).count(),
                '2048x2048': GeneratedImage.objects.filter(width=2048, height=2048).count(),
            }
        }
        
        return JsonResponse({
            'success': True,
            'stats': stats
        }, status=200)
        
    except Exception as e:
        logger.error(f"Error in get_statistics_view: {e}")
        return JsonResponse({'error': str(e)}, status=500)


# ============================================
# Export Views
# ============================================

@require_http_methods(["POST"])
def export_images_view(request):
    """
    Export multiple images as ZIP
    
    POST /export/
    {
        "image_ids": [1, 2, 3]
    }
    """
    try:
        import zipfile
        from io import BytesIO
        
        data = json.loads(request.body)
        image_ids = data.get('image_ids', [])
        
        if not image_ids:
            return JsonResponse({'error': 'image_ids is required'}, status=400)
        
        # Create ZIP file in memory
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for img_id in image_ids:
                try:
                    img = GeneratedImage.objects.get(id=img_id)
                    
                    # Create filename
                    filename = f"{img.id}_{img.prompt[:30].replace(' ', '_')}.{img.output_format.lower()}"
                    
                    # Add image to ZIP
                    zip_file.writestr(filename, img.image_data)
                    
                except GeneratedImage.DoesNotExist:
                    logger.warning(f"Image {img_id} not found")
                    continue
        
        # Prepare response
        response = HttpResponse(
            zip_buffer.getvalue(),
            content_type='application/zip'
        )
        response['Content-Disposition'] = 'attachment; filename="openimage_export.zip"'
        
        return response
        
    except Exception as e:
        logger.error(f"Error in export_images_view: {e}")
        return JsonResponse({'error': str(e)}, status=500)