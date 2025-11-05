# 🚀 Advanced Features

OpenImage provides professional-grade features for power users and production environments.

---

## 🔍 AI Image Upscaling

### Overview

OpenImage integrates **Real-ESRGAN**, a state-of-the-art AI upscaling technology that enhances image resolution while preserving and even improving quality.

### Supported Scale Factors

| Scale | Input | Output | Use Case |
|-------|-------|--------|----------|
| **2x** | 512×512 | 1024×1024 | Standard enhancement |
| **2x** | 1024×1024 | 2048×2048 | High-quality prints |
| **4x** | 512×512 | 2048×2048 | Maximum quality |
| **4x** | 256×256 | 1024×1024 | Thumbnail to full-size |

### How to Use

#### From Web Interface

1. Navigate to your image gallery
2. Click on an image thumbnail
3. Click the **"Upscale"** button
4. Select scale factor (2x or 4x)
5. Wait 5-15 seconds for processing
6. Both original and upscaled versions are saved

#### From Django Shell

```python
from you_image_generator.upscaler import upscale_image
from you_image_generator.models import GeneratedImage

# Get an image
img = GeneratedImage.objects.first()

# Upscale 2x
upscaled = upscale_image(img.image_data, scale=2)

# Save as new image
new_img = GeneratedImage.objects.create(
    prompt=f"{img.prompt} [Upscaled 2x]",
    image_data=upscaled,
    width=img.width * 2,
    height=img.height * 2,
    model_used=f"{img.model_used} + Real-ESRGAN"
)
```

#### Batch Upscaling

```python
# Upscale all images from a specific provider
images = GeneratedImage.objects.filter(provider='pollinations')

for img in images:
    if img.width < 1024:  # Only upscale smaller images
        upscaled = upscale_image(img.image_data, scale=2)
        # Save...
```

### Technical Details

- **Algorithm**: Real-ESRGAN (Enhanced Super-Resolution GAN)
- **Model**: RealESRGAN_x4plus
- **Processing Time**: 
  - 512×512 → 1024×1024: ~5 seconds
  - 1024×1024 → 2048×2048: ~15 seconds
  - 512×512 → 2048×2048: ~20 seconds
- **Memory Usage**: ~2GB RAM for 4x upscaling
- **Quality**: Preserves details, reduces artifacts

### Before/After Examples

=== "Product Photo"
    **Before (512×512)**
    - Slightly blurry edges
    - Visible compression artifacts
    - Limited print quality
    
    **After (2048×2048)**
    - Sharp edges and text
    - No visible artifacts
    - Print-ready quality

=== "Portrait"
    **Before (768×768)**
    - Soft facial features
    - Texture loss
    
    **After (1536×1536)**
    - Enhanced skin texture
    - Sharper eyes and hair
    - Professional quality

=== "Landscape"
    **Before (1024×512)**
    - Good overall quality
    - Detail loss in foliage
    
    **After (2048×1024)**
    - Enhanced leaf detail
    - Improved cloud texture
    - Ready for large displays

### Best Practices

!!! tip "When to Upscale"
    - ✅ Product photos for e-commerce
    - ✅ Images intended for print
    - ✅ Thumbnails that need full-size versions
    - ✅ Low-resolution generations that turned out well
    - ❌ Already high-resolution images (>2048px)
    - ❌ Images with fundamental quality issues

!!! warning "Limitations"
    - Cannot fix severely distorted images
    - Works best on images with good base quality
    - Processing time increases with resolution
    - Requires sufficient server RAM

---

## 🎨 Style Presets

### Available Styles

OpenImage provides 10 carefully crafted style presets that modify your prompt to achieve specific artistic looks.

#### 1. Realistic Photo

```yaml
Description: Professional photography style
Adds: "photorealistic, professional photography, studio lighting, 8k resolution, high detail, sharp focus"
Best for: Product shots, portraits, real-world scenes
Quality: ⭐⭐⭐⭐⭐
```

**Example Prompts:**
```
Input: "red sports car"
Output: "red sports car, photorealistic, professional photography, 
         studio lighting, 8k resolution, high detail, sharp focus"
```

#### 2. Anime/Manga

```yaml
Description: Japanese animation style
Adds: "anime style, manga art, vibrant colors, cel-shaded, clean lines, digital art"
Best for: Character illustrations, scenes, fan art
Quality: ⭐⭐⭐⭐⭐
```

**Example Prompts:**
```
Input: "magical girl character"
Output: "magical girl character, anime style, manga art, vibrant colors, 
         cel-shaded, clean lines, digital art"
```

#### 3. Oil Painting

```yaml
Description: Classical oil painting technique
Adds: "oil painting, canvas texture, brush strokes, impressionist, rich colors, artistic"
Best for: Portraits, landscapes, artistic interpretations
Quality: ⭐⭐⭐⭐
```

#### 4. Watercolor

```yaml
Description: Soft watercolor painting
Adds: "watercolor painting, soft edges, pastel colors, paper texture, artistic, flowing"
Best for: Gentle scenes, nature, illustrations
Quality: ⭐⭐⭐⭐
```

#### 5. Cyberpunk

```yaml
Description: Futuristic dystopian aesthetic
Adds: "cyberpunk style, neon lights, dark atmosphere, futuristic, dystopian, high tech"
Best for: Sci-fi scenes, urban environments, tech concepts
Quality: ⭐⭐⭐⭐
```

#### 6. Fantasy Art

```yaml
Description: Epic fantasy illustration
Adds: "fantasy art, epic, magical, detailed, concept art, dramatic lighting"
Best for: Characters, creatures, magical scenes
Quality: ⭐⭐⭐⭐⭐
```

#### 7. Minimalist

```yaml
Description: Clean, simple design
Adds: "minimalist, clean lines, simple, modern, flat design, minimal details"
Best for: Logos, icons, modern designs
Quality: ⭐⭐⭐⭐
```

#### 8. Vintage Film

```yaml
Description: Retro photography style
Adds: "vintage photo, film grain, faded colors, retro, nostalgic, analog photography"
Best for: Retro scenes, nostalgic themes
Quality: ⭐⭐⭐⭐
```

#### 9. Comic Book

```yaml
Description: American comic book style
Adds: "comic book style, bold lines, halftone dots, vibrant colors, action-packed"
Best for: Superhero scenes, action sequences
Quality: ⭐⭐⭐⭐
```

#### 10. Abstract

```yaml
Description: Modern abstract art
Adds: "abstract art, geometric shapes, colorful, modern art, non-representational"
Best for: Artistic expression, backgrounds
Quality: ⭐⭐⭐⭐
```

### Style Compatibility Matrix

| Style | Gemini | FLUX.1 | SD XL | Pollinations |
|-------|---------|---------|-------|--------------|
| Realistic | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Anime | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Oil Painting | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Watercolor | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Cyberpunk | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Fantasy | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Minimalist | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Vintage | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Comic Book | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Abstract | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

### Creating Custom Styles

```python
# In you_image_generator/styles.py

STYLE_PRESETS = {
    'your_custom_style': {
        'name': 'Your Custom Style',
        'description': 'Your description',
        'suffix': 'your, custom, keywords',
        'negative': 'things, to, avoid',  # Optional
        'recommended_providers': ['gemini', 'flux'],
        'quality_rating': 4
    }
}
```

---

## 📦 Batch Operations

### Batch Generation

Generate multiple variations of the same prompt:

```python
from you_image_generator.ai_clients import get_api_client
from django.conf import settings

client = get_api_client('gemini', settings.GEMINI_API_KEY)

base_prompt = "a red apple on white background"
variations = [
    f"{base_prompt}, photorealistic",
    f"{base_prompt}, watercolor painting",
    f"{base_prompt}, anime style",
    f"{base_prompt}, minimalist",
]

for prompt in variations:
    result = client.generate_image(prompt)
    # Save to database...
```

### Batch Upscaling

Upscale multiple images:

```python
from you_image_generator.models import GeneratedImage
from you_image_generator.upscaler import upscale_image

# Get all low-res images
images = GeneratedImage.objects.filter(width__lt=1024)

for img in images:
    upscaled = upscale_image(img.image_data, scale=2)
    GeneratedImage.objects.create(
        prompt=f"{img.prompt} [Upscaled]",
        image_data=upscaled,
        width=img.width * 2,
        height=img.height * 2,
        provider=img.provider,
        model_used=f"{img.model_used} + Real-ESRGAN"
    )
```

### Batch Export

Export multiple images as ZIP:

```python
import zipfile
from io import BytesIO

def export_images_zip(image_ids):
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for img_id in image_ids:
            img = GeneratedImage.objects.get(id=img_id)
            filename = f"{img.id}_{img.prompt[:30]}.png"
            zip_file.writestr(filename, img.image_data)
    
    return zip_buffer.getvalue()
```

### Scheduled Generation

Using Django management command:

```python
# management/commands/generate_daily.py

from django.core.management.base import BaseCommand
from you_image_generator.ai_clients import get_api_client

class Command(BaseCommand):
    def handle(self, *args, **options):
        prompts = self.load_prompts_from_file()
        client = get_api_client('gemini', api_key)
        
        for prompt in prompts:
            result = client.generate_image(prompt)
            # Save...
```

```bash
# Add to crontab
0 2 * * * cd /app && python manage.py generate_daily
```

---

## 🔍 Advanced Search Features

### Tag System

Images are automatically tagged based on content:

```python
# Auto-tagging on save
def auto_tag_image(prompt):
    tags = []
    
    # Nature tags
    if any(word in prompt.lower() for word in ['tree', 'forest', 'mountain', 'sea']):
        tags.append('nature')
    
    # Portrait tags
    if any(word in prompt.lower() for word in ['person', 'face', 'portrait', 'character']):
        tags.append('portrait')
    
    # ... more logic
    
    return tags
```

### Search Operators

```python
# In views.py
def search_images(query):
    # Tag search
    if query.startswith('tag:'):
        tag = query.split(':')[1]
        return GeneratedImage.objects.filter(tags__contains=tag)
    
    # Provider search
    elif query.startswith('provider:'):
        provider = query.split(':')[1]
        return GeneratedImage.objects.filter(provider=provider)
    
    # Date search
    elif query.startswith('date:'):
        date = query.split(':')[1]
        return GeneratedImage.objects.filter(created_at__date=date)
    
    # Full-text search
    else:
        return GeneratedImage.objects.filter(prompt__icontains=query)
```

### Filter Combinations

```python
# Complex filtering
images = GeneratedImage.objects.filter(
    tags__contains='nature',
    provider='gemini',
    width__gte=1024,
    created_at__gte=timezone.now() - timedelta(days=7)
).order_by('-created_at')
```

---

## 📊 Metadata Management

### Full Metadata Tracking

Each generated image stores:

```python
class GeneratedImage(models.Model):
    # Core data
    prompt = models.TextField()
    negative_prompt = models.TextField(blank=True, null=True)
    model_used = models.CharField(max_length=100)
    provider = models.CharField(max_length=50)
    
    # Image data
    image_data = models.BinaryField()
    image_url = models.URLField(blank=True, null=True)
    
    # Dimensions
    width = models.IntegerField(default=1024)
    height = models.IntegerField(default=1024)
    aspect_ratio = models.CharField(max_length=10, default='1:1')
    
    # Parameters
    seed = models.BigIntegerField(blank=True, null=True)
    cfg_scale = models.FloatField(blank=True, null=True)
    output_format = models.CharField(max_length=10, default='PNG')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Organization
    tags = models.JSONField(default=list)
    category = models.CharField(max_length=50, blank=True)
```

### Exporting Metadata

```python
import json

def export_metadata(image_id):
    img = GeneratedImage.objects.get(id=image_id)
    
    metadata = {
        'prompt': img.prompt,
        'negative_prompt': img.negative_prompt,
        'model': img.model_used,
        'provider': img.provider,
        'dimensions': f"{img.width}x{img.height}",
        'aspect_ratio': img.aspect_ratio,
        'seed': img.seed,
        'cfg_scale': img.cfg_scale,
        'format': img.output_format,
        'created': img.created_at.isoformat(),
        'tags': img.tags,
    }
    
    return json.dumps(metadata, indent=2)
```

---

## 🎯 Performance Optimization

### Caching

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# views.py
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def gallery_view(request):
    images = GeneratedImage.objects.all()[:50]
    return render(request, 'gallery.html', {'images': images})
```

### Lazy Loading

```javascript
// In template
<img data-src="{{ image.url }}" class="lazy" alt="{{ image.prompt }}">

<script>
document.addEventListener("DOMContentLoaded", function() {
    const lazyImages = document.querySelectorAll('.lazy');
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    lazyImages.forEach(img => imageObserver.observe(img));
});
</script>
```

### Database Indexing

```python
# models.py
class GeneratedImage(models.Model):
    # ... fields ...
    
    class Meta:
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['provider']),
            models.Index(fields=['width', 'height']),
            models.Index(fields=['tags']),
        ]
        ordering = ['-created_at']
```

### Pagination

```python
from django.core.paginator import Paginator

def gallery_view(request):
    images = GeneratedImage.objects.all()
    paginator = Paginator(images, 50)  # 50 images per page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'gallery.html', {'page_obj': page_obj})
```

---

## 🔐 API Access

### REST Endpoints

```python
# urls.py
urlpatterns = [
    path('api/generate/', generate_api, name='generate_api'),
    path('api/upscale/', upscale_api, name='upscale_api'),
    path('api/search/', search_api, name='search_api'),
    path('api/metadata/<int:id>/', metadata_api, name='metadata_api'),
]

# Example API call
POST /api/generate/
{
    "prompt": "a red apple",
    "provider": "gemini",
    "style_preset": "realistic",
    "width": 1024,
    "height": 1024,
    "negative_prompt": "blurry, low quality"
}

Response:
{
    "id": 123,
    "image_base64": "iVBORw0KGgoAAAANSUhEUg...",
    "prompt": "a red apple, photorealistic...",
    "model_used": "Gemini 2.0 Flash",
    "width": 1024,
    "height": 1024,
    "created_at": "2025-10-07T12:00:00Z"
}
```

### Python Client Library

```python
import requests
import base64

class OpenImageClient:
    def __init__(self, base_url='http://localhost:9510'):
        self.base_url = base_url
    
    def generate(self, prompt, provider='gemini', **kwargs):
        url = f"{self.base_url}/api/generate/"
        data = {
            'prompt': prompt,
            'provider': provider,
            **kwargs
        }
        response = requests.post(url, data=data)
        return response.json()
    
    def upscale(self, image_id, scale=2):
        url = f"{self.base_url}/api/upscale/"
        data = {'image_id': image_id, 'scale': scale}
        response = requests.post(url, data=data)
        return response.json()
    
    def search(self, query):
        url = f"{self.base_url}/api/search/"
        response = requests.get(url, params={'q': query})
        return response.json()

# Usage
client = OpenImageClient()
result = client.generate("a cute cat", provider="gemini")
image_data = base64.b64decode(result['image_base64'])
with open('cat.png', 'wb') as f:
    f.write(image_data)
```

---

## 🎨 Custom Workflows

### E-Commerce Product Pipeline

```python
def ecommerce_pipeline(product_name, angles=['front', 'side', 'top']):
    """Generate multiple product views"""
    client = get_api_client('gemini', api_key)
    results = []
    
    for angle in angles:
        prompt = f"{product_name}, {angle} view, white background, studio lighting, product photography, 8k"
        result = client.generate_image(
            prompt=prompt,
            options={
                'width': 1024,
                'height': 1024,
                'style_preset': 'realistic',
            }
        )
        
        # Save original
        img = save_to_database(result[0])
        
        # Upscale for print
        upscaled = upscale_image(img.image_data, scale=2)
        img_hq = save_to_database(upscaled, suffix='_HQ')
        
        results.append({
            'angle': angle,
            'standard': img,
            'high_quality': img_hq
        })
    
    return results
```

### Social Media Content Creator

```python
def social_media_batch(theme, count=10):
    """Generate social media post images"""
    client = get_api_client('pollinations')  # Fast and free
    
    prompts = [
        f"{theme}, trending on instagram, vibrant colors, eye-catching",
        f"{theme}, minimalist design, clean, modern",
        f"{theme}, vintage aesthetic, retro, nostalgic",
        # ... more variations
    ]
    
    for prompt in prompts[:count]:
        result = client.generate_image(
            prompt=prompt,
            options={
                'width': 1024,
                'height': 1024,
                'aspect_ratio': '1:1'
            }
        )
        save_to_database(result[0], tags=['social_media', theme])
```

### Blog Illustration Pipeline

```python
def blog_illustration(article_title, article_summary):
    """Generate blog header image"""
    # Use GPT to create image prompt from article
    prompt = generate_prompt_from_text(article_title, article_summary)
    
    # Generate with FLUX.1 for quality
    client = get_api_client('huggingface', api_key)
    result = client.generate_image(
        prompt=prompt,
        options={
            'model': 'flux-schnell',
            'width': 1820,
            'height': 1024,
            'aspect_ratio': '16:9'
        }
    )
    
    return save_to_database(result[0], category='blog_header')
```

---

## 📱 Mobile Optimization

### Responsive Image Serving

```python
def get_responsive_image(image_id, size='medium'):
    """Serve appropriately sized image for device"""
    img = GeneratedImage.objects.get(id=image_id)
    
    sizes = {
        'thumbnail': (256, 256),
        'small': (512, 512),
        'medium': (1024, 1024),
        'large': (2048, 2048)
    }
    
    target_size = sizes.get(size, sizes['medium'])
    
    # Check if we have cached version
    cache_key = f"image_{image_id}_{size}"
    cached = cache.get(cache_key)
    if cached:
        return cached
    
    # Resize if needed
    if img.width > target_size[0]:
        resized = resize_image(img.image_data, target_size)
        cache.set(cache_key, resized, timeout=3600)
        return resized
    
    return img.image_data
```

---

## 🔄 Webhook Integration

### Setup Webhooks

```python
# settings.py
WEBHOOK_ENDPOINTS = [
    'https://your-app.com/webhooks/image-generated',
    'https://slack.com/webhooks/...',
]

# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests

@receiver(post_save, sender=GeneratedImage)
def notify_webhooks(sender, instance, created, **kwargs):
    if created:
        payload = {
            'event': 'image.generated',
            'image_id': instance.id,
            'prompt': instance.prompt,
            'provider': instance.provider,
            'timestamp': instance.created_at.isoformat()
        }
        
        for endpoint in settings.WEBHOOK_ENDPOINTS:
            try:
                requests.post(endpoint, json=payload, timeout=5)
            except:
                pass  # Handle errors appropriately
```

---

## 📊 Analytics & Monitoring

### Usage Statistics

```python
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import timedelta

def get_usage_stats(days=30):
    """Get generation statistics"""
    start_date = timezone.now() - timedelta(days=days)
    
    stats = {
        'total_images': GeneratedImage.objects.filter(
            created_at__gte=start_date
        ).count(),
        
        'by_provider': GeneratedImage.objects.filter(
            created_at__gte=start_date
        ).values('provider').annotate(count=Count('id')),
        
        'by_style': GeneratedImage.objects.filter(
            created_at__gte=start_date
        ).values('tags').annotate(count=Count('id')),
        
        'avg_resolution': GeneratedImage.objects.filter(
            created_at__gte=start_date
        ).aggregate(
            avg_width=Avg('width'),
            avg_height=Avg('height')
        ),
        
        'popular_prompts': GeneratedImage.objects.filter(
            created_at__gte=start_date
        ).values('prompt')[:10]
    }
    
    return stats
```

### Cost Tracking

```python
def calculate_costs(start_date, end_date):
    """Calculate generation costs"""
    images = GeneratedImage.objects.filter(
        created_at__range=[start_date, end_date]
    )
    
    cost_per_provider = {
        'pollinations': 0.0,
        'gemini': 0.0,  # Free tier
        'huggingface': 0.0,  # Free tier
        'deepai': 0.0,
        'runware': 0.002,
        'replicate': 0.004,
        'stability': 0.02,
    }
    
    total_cost = 0
    breakdown = {}
    
    for provider, cost in cost_per_provider.items():
        count = images.filter(provider=provider).count()
        provider_cost = count * cost
        total_cost += provider_cost
        breakdown[provider] = {
            'count': count,
            'cost': provider_cost
        }
    
    return {
        'total_cost': total_cost,
        'breakdown': breakdown,
        'period': f"{start_date} to {end_date}"
    }
```

---

## 🛠️ Maintenance Tasks

### Database Cleanup

```python
# management/commands/cleanup_old_images.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from you_image_generator.models import GeneratedImage

class Command(BaseCommand):
    help = 'Delete images older than specified days'
    
    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, default=90)
        parser.add_argument('--dry-run', action='store_true')
    
    def handle(self, *args, **options):
        cutoff_date = timezone.now() - timedelta(days=options['days'])
        old_images = GeneratedImage.objects.filter(created_at__lt=cutoff_date)
        
        count = old_images.count()
        
        if options['dry_run']:
            self.stdout.write(f"Would delete {count} images")
        else:
            old_images.delete()
            self.stdout.write(self.style.SUCCESS(f"Deleted {count} images"))
```

```bash
# Run cleanup
python manage.py cleanup_old_images --days=90
python manage.py cleanup_old_images --days=30 --dry-run
```

### Image Optimization

```python
from PIL import Image
from io import BytesIO

def optimize_image(image_data, quality=85):
    """Compress image to reduce storage"""
    img = Image.open(BytesIO(image_data))
    
    # Convert RGBA to RGB if needed
    if img.mode == 'RGBA':
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background
    
    # Save with optimization
    output = BytesIO()
    img.save(output, format='JPEG', quality=quality, optimize=True)
    
    return output.getvalue()

# Batch optimize all images
def optimize_all_images():
    images = GeneratedImage.objects.filter(output_format='PNG')
    
    for img in images:
        optimized = optimize_image(img.image_data)
        
        # Only save if significantly smaller
        if len(optimized) < len(img.image_data) * 0.7:
            img.image_data = optimized
            img.output_format = 'JPEG'
            img.save()
```

---

## 🎓 Tips & Best Practices

### Prompt Engineering

!!! tip "Write Better Prompts"
    **Good prompt structure:**
    ```
    [Subject] + [Style] + [Quality modifiers] + [Lighting] + [Composition]
    
    Example:
    "A red sports car, photorealistic, 8k resolution, golden hour lighting, 
     centered composition, professional photography"
    ```

### Provider Selection Guide

```python
def choose_provider(use_case):
    """Recommend provider based on use case"""
    recommendations = {
        'rapid_prototyping': 'pollinations',  # Fast & free
        'high_quality_free': 'gemini',  # Best free quality
        'specific_models': 'huggingface',  # Model variety
        'production_volume': 'runware',  # Cheap at scale
        'maximum_quality': 'replicate',  # Top quality
        'enterprise': 'stability',  # Official enterprise
    }
    
    return recommendations.get(use_case, 'gemini')
```

### Style Preset Combinations

```python
# Some styles work well together
def combine_styles(base_style, modifiers):
    """Combine multiple style elements"""
    combinations = {
        'realistic': {
            'lighting': ['studio', 'natural', 'golden hour', 'dramatic'],
            'quality': ['8k', '4k', 'high detail', 'sharp focus'],
            'composition': ['centered', 'rule of thirds', 'close-up']
        },
        'anime': {
            'substyles': ['shonen', 'shojo', 'seinen', 'mecha'],
            'artists': ['Makoto Shinkai', 'Studio Ghibli', 'CLAMP'],
            'quality': ['detailed', 'vibrant', 'dynamic']
        }
    }
    
    return combinations.get(base_style, {})
```

---

## 🐛 Debugging Tools

### Image Generation Logger

```python
import logging

logger = logging.getLogger('image_generation')

def generate_with_logging(prompt, provider):
    """Generate image with detailed logging"""
    logger.info(f"Starting generation: {provider}")
    logger.debug(f"Prompt: {prompt}")
    
    start_time = time.time()
    
    try:
        result = client.generate_image(prompt)
        duration = time.time() - start_time
        
        logger.info(f"Success in {duration:.2f}s")
        logger.debug(f"Image size: {len(result[0].image_data)} bytes")
        
        return result
    except Exception as e:
        logger.error(f"Generation failed: {str(e)}")
        logger.exception("Full traceback:")
        raise
```

### Performance Profiling

```python
from django.core.cache import cache
import time

def profile_generation(prompt, provider):
    """Profile generation performance"""
    timings = {
        'api_call': 0,
        'save_to_db': 0,
        'upscale': 0,
        'total': 0
    }
    
    start = time.time()
    
    # API call timing
    api_start = time.time()
    result = client.generate_image(prompt)
    timings['api_call'] = time.time() - api_start
    
    # Database save timing
    db_start = time.time()
    img = save_to_database(result[0])
    timings['save_to_db'] = time.time() - db_start
    
    # Upscale timing (optional)
    if should_upscale:
        upscale_start = time.time()
        upscaled = upscale_image(img.image_data)
        timings['upscale'] = time.time() - upscale_start
    
    timings['total'] = time.time() - start
    
    # Log or store metrics
    logger.info(f"Performance metrics: {timings}")
    
    return img, timings
```

---

## 🔗 Integration Examples

### WordPress Plugin

```php
<?php
// OpenImage WordPress integration
function openimage_generate($prompt, $provider = 'gemini') {
    $url = 'http://localhost:9510/api/generate/';
    
    $response = wp_remote_post($url, array(
        'body' => array(
            'prompt' => $prompt,
            'provider' => $provider
        )
    ));
    
    if (is_wp_error($response)) {
        return false;
    }
    
    $data = json_decode(wp_remote_retrieve_body($response), true);
    
    // Upload to WordPress media library
    $upload = wp_upload_bits(
        'generated-' . time() . '.png',
        null,
        base64_decode($data['image_base64'])
    );
    
    return $upload['url'];
}
```

### Zapier Integration

```javascript
// Zapier custom action
const options = {
  url: 'http://your-server.com:9510/api/generate/',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: {
    prompt: inputData.prompt,
    provider: inputData.provider || 'gemini',
    width: 1024,
    height: 1024
  }
};

return z.request(options)
  .then(response => response.json())
  .then(data => {
    return {
      id: data.id,
      imageUrl: `http://your-server.com:9510/image/${data.id}/`,
      prompt: data.prompt
    };
  });
```

---

## 📚 Further Reading

- [Prompt Engineering Guide](prompt-engineering.md)
- [Provider Comparison](provider-comparison.md)
- [Performance Tuning](performance.md)
- [Security Best Practices](security.md)
- [API Reference](api-reference.md)

---

<div align="center">

**Need help?** Check our [Troubleshooting Guide](troubleshooting.md) or [open an issue](https://github.com/yourusername/openimage/issues)

[← Back to Home](index.md) | [Next: Search Guide →](search.md)

</div>