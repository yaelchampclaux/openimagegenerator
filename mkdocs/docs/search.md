# 🔍 Search & Organization

Master OpenImage's powerful search and organization features to manage thousands of generated images efficiently.

---

## 🏷️ Tag System

### Automatic Tagging

OpenImage automatically assigns tags based on prompt content when images are generated.

#### Category Detection

```python
# Auto-tagging logic
def auto_tag_image(prompt):
    """Automatically generate tags from prompt"""
    tags = set()
    prompt_lower = prompt.lower()
    
    # Nature & Environment
    if any(word in prompt_lower for word in ['tree', 'forest', 'mountain', 'sea', 'ocean', 'beach', 'sky', 'cloud', 'river', 'lake', 'desert', 'jungle']):
        tags.add('nature')
    
    if any(word in prompt_lower for word in ['landscape', 'scenery', 'vista', 'panorama']):
        tags.add('landscape')
    
    # People & Characters
    if any(word in prompt_lower for word in ['person', 'people', 'human', 'man', 'woman', 'child', 'face', 'portrait']):
        tags.add('portrait')
    
    if any(word in prompt_lower for word in ['character', 'hero', 'villain', 'warrior', 'wizard', 'knight']):
        tags.add('character')
    
    # Objects & Products
    if any(word in prompt_lower for word in ['product', 'object', 'item', 'device', 'tool', 'furniture']):
        tags.add('product')
    
    if any(word in prompt_lower for word in ['car', 'vehicle', 'bike', 'boat', 'plane', 'train']):
        tags.add('vehicle')
    
    # Art Styles
    if any(word in prompt_lower for word in ['abstract', 'geometric', 'pattern', 'shapes']):
        tags.add('abstract')
    
    if any(word in prompt_lower for word in ['anime', 'manga', 'cartoon']):
        tags.add('anime')
    
    if any(word in prompt_lower for word in ['realistic', 'photorealistic', 'photo']):
        tags.add('realistic')
    
    # Architecture
    if any(word in prompt_lower for word in ['building', 'house', 'city', 'architecture', 'urban', 'skyscraper']):
        tags.add('architecture')
    
    # Animals
    if any(word in prompt_lower for word in ['cat', 'dog', 'bird', 'animal', 'wildlife', 'pet', 'creature']):
        tags.add('animal')
    
    # Food
    if any(word in prompt_lower for word in ['food', 'meal', 'dish', 'cuisine', 'restaurant', 'fruit', 'vegetable']):
        tags.add('food')
    
    # Fantasy & Sci-Fi
    if any(word in prompt_lower for word in ['fantasy', 'magic', 'dragon', 'elf', 'dwarf', 'wizard']):
        tags.add('fantasy')
    
    if any(word in prompt_lower for word in ['sci-fi', 'scifi', 'futuristic', 'robot', 'alien', 'space', 'cyberpunk']):
        tags.add('scifi')
    
    return list(tags)
```

### Available Tags

| Category | Tags | Description |
|----------|------|-------------|
| **Subject** | nature, portrait, product, vehicle, animal, food, architecture | Main subject matter |
| **Scene** | landscape, urban, interior, scene, environment | Scene type |
| **Character** | character, person, face, human | People-related |
| **Style** | realistic, anime, abstract, fantasy, scifi, vintage | Artistic style |
| **Quality** | professional, 8k, high-detail, photorealistic | Quality indicators |

### Manual Tagging

```python
# Add custom tags to an image
image = GeneratedImage.objects.get(id=123)
image.tags = ['custom_tag', 'project_name', 'client_work']
image.save()
```

```python
# Bulk tag assignment
images = GeneratedImage.objects.filter(provider='gemini')
for img in images:
    if 'portrait' not in img.tags:
        img.tags.append('portrait')
        img.save()
```

---

## 🔍 Search Methods

### 1. Basic Text Search

Search prompts and model names:

```python
# Search in prompts
def search_basic(query):
    return GeneratedImage.objects.filter(
        Q(prompt__icontains=query) |
        Q(model_used__icontains=query)
    ).order_by('-created_at')

# Example usage
results = search_basic("mountain landscape")
```

**Web Interface:**
```
Simply type: mountain landscape
Returns: All images with "mountain" or "landscape" in prompt
```

### 2. Tag-Based Search

Filter by one or multiple tags:

```python
# Single tag
def search_by_tag(tag):
    return GeneratedImage.objects.filter(
        tags__contains=[tag]
    ).order_by('-created_at')

# Multiple tags (AND logic)
def search_by_tags(tags):
    queryset = GeneratedImage.objects.all()
    for tag in tags:
        queryset = queryset.filter(tags__contains=[tag])
    return queryset.order_by('-created_at')

# Multiple tags (OR logic)
def search_by_any_tag(tags):
    from django.db.models import Q
    query = Q()
    for tag in tags:
        query |= Q(tags__contains=[tag])
    return GeneratedImage.objects.filter(query).order_by('-created_at')
```

**Web Interface:**
```
Click tags: [Nature] [Landscape] [8k]
Returns: Images with ALL selected tags
```

### 3. Advanced Search Operators

Use special operators for precise searches:

```python
def advanced_search(query):
    """Parse and execute advanced search"""
    
    # Provider filter: provider:gemini
    if query.startswith('provider:'):
        provider = query.split(':')[1]
        return GeneratedImage.objects.filter(provider=provider)
    
    # Date filter: date:2025-10-07
    elif query.startswith('date:'):
        date_str = query.split(':')[1]
        from datetime import datetime
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        return GeneratedImage.objects.filter(created_at__date=date)
    
    # Resolution filter: resolution:1024x1024
    elif query.startswith('resolution:'):
        resolution = query.split(':')[1]
        width, height = map(int, resolution.split('x'))
        return GeneratedImage.objects.filter(width=width, height=height)
    
    # Model filter: model:flux
    elif query.startswith('model:'):
        model = query.split(':')[1]
        return GeneratedImage.objects.filter(model_used__icontains=model)
    
    # Tag filter: tag:nature
    elif query.startswith('tag:'):
        tag = query.split(':')[1]
        return GeneratedImage.objects.filter(tags__contains=[tag])
    
    # Date range: after:2025-10-01
    elif query.startswith('after:'):
        date_str = query.split(':')[1]
        date = datetime.strptime(date_str, '%Y-%m-%d')
        return GeneratedImage.objects.filter(created_at__gte=date)
    
    # Before date: before:2025-10-31
    elif query.startswith('before:'):
        date_str = query.split(':')[1]
        date = datetime.strptime(date_str, '%Y-%m-%d')
        return GeneratedImage.objects.filter(created_at__lte=date)
    
    # Default: text search
    else:
        return GeneratedImage.objects.filter(
            Q(prompt__icontains=query) |
            Q(model_used__icontains=query)
        )
```

**Example Queries:**

| Query | Result |
|-------|--------|
| `provider:gemini` | All Gemini-generated images |
| `date:2025-10-07` | Images from October 7, 2025 |
| `resolution:1024x1024` | All 1024×1024 images |
| `model:flux` | Images using FLUX models |
| `tag:nature` | Images tagged with "nature" |
| `after:2025-10-01` | Images from October 2025 onwards |
| `before:2025-09-30` | Images before October 2025 |

### 4. Combined Searches

Combine multiple criteria:

```python
def combined_search(filters):
    """
    filters = {
        'text': 'mountain',
        'tags': ['nature', 'landscape'],
        'provider': 'gemini',
        'min_width': 1024,
        'date_from': '2025-10-01',
        'date_to': '2025-10-31'
    }
    """
    queryset = GeneratedImage.objects.all()
    
    if filters.get('text'):
        queryset = queryset.filter(prompt__icontains=filters['text'])
    
    if filters.get('tags'):
        for tag in filters['tags']:
            queryset = queryset.filter(tags__contains=[tag])
    
    if filters.get('provider'):
        queryset = queryset.filter(provider=filters['provider'])
    
    if filters.get('min_width'):
        queryset = queryset.filter(width__gte=filters['min_width'])
    
    if filters.get('date_from'):
        queryset = queryset.filter(created_at__gte=filters['date_from'])
    
    if filters.get('date_to'):
        queryset = queryset.filter(created_at__lte=filters['date_to'])
    
    return queryset.order_by('-created_at')
```

**Example:**
```python
results = combined_search({
    'text': 'portrait',
    'tags': ['realistic', 'professional'],
    'provider': 'gemini',
    'min_width': 1024,
    'date_from': '2025-10-01'
})
```

---

## 📊 Category System

### Predefined Categories

```python
CATEGORIES = {
    'nature': {
        'name': 'Nature & Landscape',
        'icon': '🌿',
        'keywords': ['tree', 'forest', 'mountain', 'sea', 'landscape']
    },
    'portrait': {
        'name': 'Portraits & People',
        'icon': '👤',
        'keywords': ['person', 'face', 'portrait', 'character']
    },
    'product': {
        'name': 'Products & Objects',
        'icon': '📦',
        'keywords': ['product', 'object', 'item']
    },
    'architecture': {
        'name': 'Architecture & Urban',
        'icon': '🏙️',
        'keywords': ['building', 'city', 'architecture', 'urban']
    },
    'animal': {
        'name': 'Animals & Wildlife',
        'icon': '🦁',
        'keywords': ['cat', 'dog', 'animal', 'wildlife']
    },
    'food': {
        'name': 'Food & Cuisine',
        'icon': '🍽️',
        'keywords': ['food', 'meal', 'dish', 'cuisine']
    },
    'fantasy': {
        'name': 'Fantasy & Magic',
        'icon': '✨',
        'keywords': ['fantasy', 'magic', 'dragon', 'wizard']
    },
    'scifi': {
        'name': 'Sci-Fi & Futuristic',
        'icon': '🚀',
        'keywords': ['sci-fi', 'futuristic', 'robot', 'space', 'cyberpunk']
    },
    'abstract': {
        'name': 'Abstract & Art',
        'icon': '🎨',
        'keywords': ['abstract', 'geometric', 'pattern', 'modern art']
    },
    'vehicle': {
        'name': 'Vehicles & Transport',
        'icon': '🚗',
        'keywords': ['car', 'vehicle', 'bike', 'boat', 'plane']
    }
}

# Auto-categorize on save
def auto_categorize(image):
    """Automatically assign category based on tags"""
    for category_key, category_data in CATEGORIES.items():
        for keyword in category_data['keywords']:
            if keyword in image.prompt.lower():
                image.category = category_key
                return
    
    image.category = 'other'
```

### Category Navigation

```python
def browse_by_category(category):
    """Get all images in a category"""
    return GeneratedImage.objects.filter(
        category=category
    ).order_by('-created_at')

def get_category_stats():
    """Get image count per category"""
    from django.db.models import Count
    
    return GeneratedImage.objects.values('category').annotate(
        count=Count('id')
    ).order_by('-count')
```

**Example Output:**
```json
[
    {"category": "nature", "count": 245},
    {"category": "portrait", "count": 187},
    {"category": "product", "count": 156},
    {"category": "architecture", "count": 98},
    {"category": "other", "count": 67}
]
```

---

## 🎯 Smart Filters

### Quick Filters

Pre-defined filter combinations for common use cases:

```python
QUICK_FILTERS = {
    'recent': {
        'name': 'Recent Images',
        'filter': lambda: GeneratedImage.objects.all()[:50]
    },
    'high_res': {
        'name': 'High Resolution',
        'filter': lambda: GeneratedImage.objects.filter(width__gte=1024, height__gte=1024)
    },
    'favorites': {
        'name': 'Favorites',
        'filter': lambda: GeneratedImage.objects.filter(tags__contains=['favorite'])
    },
    'portraits': {
        'name': 'Portrait Photos',
        'filter': lambda: GeneratedImage.objects.filter(
            tags__contains=['portrait'],
            tags__contains=['realistic']
        )
    },
    'landscapes': {
        'name': 'Landscapes',
        'filter': lambda: GeneratedImage.objects.filter(
            Q(tags__contains=['nature']) | Q(tags__contains=['landscape'])
        )
    },
    'products': {
        'name': 'Product Photos',
        'filter': lambda: GeneratedImage.objects.filter(category='product')
    },
    'gemini_best': {
        'name': 'Best from Gemini',
        'filter': lambda: GeneratedImage.objects.filter(
            provider='gemini',
            width__gte=1024
        )
    },
    'this_week': {
        'name': 'This Week',
        'filter': lambda: GeneratedImage.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        )
    },
    'upscaled': {
        'name': 'Upscaled Images',
        'filter': lambda: GeneratedImage.objects.filter(
            model_used__icontains='esrgan'
        )
    }
}
```

---

## 📂 Collections & Albums

### Create Collections

Group related images together:

```python
class Collection(models.Model):
    """User-defined image collections"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    images = models.ManyToManyField(GeneratedImage)
    created_at = models.DateTimeField(auto_now_add=True)
    cover_image = models.ForeignKey(
        GeneratedImage, 
        on_delete=models.SET_NULL,
        null=True,
        related_name='collection_covers'
    )
    
    def __str__(self):
        return f"{self.name} ({self.images.count()} images)"

# Usage
collection = Collection.objects.create(
    name="Product Launch 2025",
    description="Images for Q4 product launch"
)

# Add images
images = GeneratedImage.objects.filter(tags__contains=['product'])
collection.images.add(*images)
```

### Smart Collections

Auto-updating collections based on rules:

```python
class SmartCollection(models.Model):
    """Auto-updating collections based on filters"""
    name = models.CharField(max_length=100)
    filter_rules = models.JSONField()
    
    def get_images(self):
        """Dynamically fetch images matching rules"""
        queryset = GeneratedImage.objects.all()
        
        for rule_type, rule_value in self.filter_rules.items():
            if rule_type == 'tags':
                for tag in rule_value:
                    queryset = queryset.filter(tags__contains=[tag])
            elif rule_type == 'provider':
                queryset = queryset.filter(provider=rule_value)
            elif rule_type == 'min_resolution':
                queryset = queryset.filter(
                    width__gte=rule_value,
                    height__gte=rule_value
                )
        
        return queryset

# Example smart collection
smart_col = SmartCollection.objects.create(
    name="High-Quality Nature Photos",
    filter_rules={
        'tags': ['nature', 'realistic'],
        'provider': 'gemini',
        'min_resolution': 1024
    }
)

# Always returns current matching images
images = smart_col.get_images()
```

---

## 🔖 Bookmarks & Favorites

### Favorite System

```python
# Add to models.py
class GeneratedImage(models.Model):
    # ... existing fields ...
    is_favorite = models.BooleanField(default=False)
    favorite_date = models.DateTimeField(null=True, blank=True)
    rating = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        null=True,
        blank=True
    )

# Mark as favorite
def mark_favorite(image_id):
    img = GeneratedImage.objects.get(id=image_id)
    img.is_favorite = True
    img.favorite_date = timezone.now()
    img.save()

# Get all favorites
favorites = GeneratedImage.objects.filter(is_favorite=True)

# Get by rating
top_rated = GeneratedImage.objects.filter(rating__gte=4)
```

---

## 📈 Search Analytics

### Track Popular Searches

```python
class SearchQuery(models.Model):
    """Track search queries for analytics"""
    query = models.CharField(max_length=255)
    results_count = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    @classmethod
    def log_search(cls, query, results_count):
        cls.objects.create(
            query=query,
            results_count=results_count
        )
    
    @classmethod
    def get_popular_searches(cls, limit=10):
        """Get most common searches"""
        from django.db.models import Count
        
        return cls.objects.values('query').annotate(
            count=Count('id')
        ).order_by('-count')[:limit]

# Usage
results = search_basic("mountain")
SearchQuery.log_search("mountain", results.count())

# Get popular searches
popular = SearchQuery.get_popular_searches(10)
```

### Search Suggestions

```python
def get_search_suggestions(partial_query):
    """Autocomplete search suggestions"""
    suggestions = set()
    
    # From previous searches
    previous = SearchQuery.objects.filter(
        query__istartswith=partial_query
    ).values_list('query', flat=True)[:5]
    suggestions.update(previous)
    
    # From common tags
    common_tags = ['nature', 'portrait', 'product', 'realistic', 'anime']
    matching_tags = [tag for tag in common_tags if partial_query.lower() in tag]
    suggestions.update(matching_tags)
    
    # From recent prompts
    recent_prompts = GeneratedImage.objects.filter(
        prompt__icontains=partial_query
    ).values_list('prompt', flat=True)[:3]
    suggestions.update(recent_prompts)
    
    return list(suggestions)[:10]
```

---

## 🎨 Visual Search (Future Feature)

### Similar Image Search

```python
# Future implementation with embeddings
class ImageEmbedding(models.Model):
    """Store image embeddings for similarity search"""
    image = models.OneToOneField(GeneratedImage, on_delete=models.CASCADE)
    embedding = models.JSONField()  # Store vector embedding
    
    @classmethod
    def find_similar(cls, image_id, limit=10):
        """Find visually similar images"""
        source = cls.objects.get(image_id=image_id)
        source_embedding = np.array(source.embedding)
        
        # Calculate cosine similarity
        similar = []
        for other in cls.objects.exclude(image_id=image_id):
            other_embedding = np.array(other.embedding)
            similarity = cosine_similarity(source_embedding, other_embedding)
            similar.append((other.image, similarity))
        
        # Sort by similarity
        similar.sort(key=lambda x: x[1], reverse=True)
        return [img for img, score in similar[:limit]]
```

---

## 📊 Advanced Filtering UI

### Filter Panel Implementation

```html
<!-- In template -->
<div class="filter-panel">
    <!-- Provider Filter -->
    <div class="filter-group">
        <h4>Provider</h4>
        <label><input type="checkbox" name="provider" value="gemini"> Gemini</label>
        <label><input type="checkbox" name="provider" value="pollinations"> Pollinations</label>
        <label><input type="checkbox" name="provider" value="huggingface"> Hugging Face</label>
    </div>
    
    <!-- Tag Filter -->
    <div class="filter-group">
        <h4>Tags</h4>
        <div id="tag-cloud">
            {% for tag in popular_tags %}
            <span class="tag" data-tag="{{ tag }}">{{ tag }}</span>
            {% endfor %}
        </div>
    </div>
    
    <!-- Resolution Filter -->
    <div class="filter-group">
        <h4>Resolution</h4>
        <label><input type="radio" name="resolution" value="all" checked> All</label>
        <label><input type="radio" name="resolution" value="512"> 512×512</label>
        <label><input type="radio" name="resolution" value="1024"> 1024×1024</label>
        <label><input type="radio" name="resolution" value="2048"> 2048×2048</label>
    </div>
    
    <!-- Date Range -->
    <div class="filter-group">
        <h4>Date Range</h4>
        <input type="date" name="date_from" placeholder="From">
        <input type="date" name="date_to" placeholder="To">
    </div>
    
    <!-- Sort Order -->
    <div class="filter-group">
        <h4>Sort By</h4>
        <select name="sort">
            <option value="-created_at">Newest First</option>
            <option value="created_at">Oldest First</option>
            <option value="-width">Highest Resolution</option>
            <option value="prompt">Alphabetical</option>
        </select>
    </div>
</div>

<script>
// Live filter update
function updateFilters() {
    const filters = {
        providers: Array.from(document.querySelectorAll('input[name="provider"]:checked'))
            .map(el => el.value),
        tags: Array.from(document.querySelectorAll('.tag.active'))
            .map(el => el.dataset.tag),
        resolution: document.querySelector('input[name="resolution"]:checked').value,
        date_from: document.querySelector('input[name="date_from"]').value,
        date_to: document.querySelector('input[name="date_to"]').value,
        sort: document.querySelector('select[name="sort"]').value
    };
    
    // Fetch filtered results
    fetch('/api/search/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(filters)
    })
    .then(response => response.json())
    .then(data => updateGallery(data.images));
}

// Tag selection
document.querySelectorAll('.tag').forEach(tag => {
    tag.addEventListener('click', () => {
        tag.classList.toggle('active');
        updateFilters();
    });
});
</script>
```

---

## 🚀 Performance Optimization

### Search Index

```python
# Add search indexes
class GeneratedImage(models.Model):
    # ... fields ...
    
    class Meta:
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['provider']),
            models.Index(fields=['category']),
            models.Index(fields=['width', 'height']),
            GinIndex(fields=['tags']),  # PostgreSQL GIN index for JSON
        ]

# Full-text search with PostgreSQL
from django.contrib.postgres.search import SearchVector, SearchQuery

def fulltext_search(query):
    """Use PostgreSQL full-text search"""
    search_vector = SearchVector('prompt', 'model_used')
    search_query = SearchQuery(query)
    
    return GeneratedImage.objects.annotate(
        search=search_vector
    ).filter(search=search_query)
```

### Caching Search Results

```python
from django.core.cache import cache

def cached_search(query, cache_time=300):
    """Cache search results for 5 minutes"""
    cache_key = f"search:{query}"
    
    results = cache.get(cache_key)
    if results is None:
        results = list(search_basic(query))
        cache.set(cache_key, results, cache_time)
    
    return results
```

---

## 📱 Mobile Search Experience

### Mobile-Optimized Search

```html
<!-- Mobile search bar -->
<div class="mobile-search">
    <input type="search" 
           placeholder="Search images..." 
           id="mobile-search"
           autocomplete="off">
    <button id="filter-toggle">
        <i class="icon-filter"></i>
    </button>
</div>

<!-- Slide-out filter panel -->
<div class="mobile-filters" id="mobile-filters">
    <div class="filter-header">
        <h3>Filters</h3>
        <button id="close-filters">✕</button>
    </div>
    
    <!-- Quick tag selection -->
    <div class="quick-tags">
        <span class="quick-tag" data-tag="nature">🌿 Nature</span>
        <span class="quick-tag" data-tag="portrait">👤 Portrait</span>
        <span class="quick-tag" data-tag="product">📦 Product</span>
        <span class="quick-tag" data-tag="realistic">📷 Realistic</span>
    </div>
    
    <!-- Provider chips -->
    <div class="provider-chips">
        <span class="chip" data-provider="gemini">Gemini</span>
        <span class="chip" data-provider="pollinations">Pollinations</span>
    </div>
</div>

<style>
.mobile-search {
    display: flex;
    gap: 10px;
    padding: 10px;
    position: sticky;
    top: 0;
    background: white;
    z-index: 100;
}

.mobile-filters {
    position: fixed;
    top: 0;
    right: -100%;
    width: 80%;
    height: 100vh;
    background: white;
    transition: right 0.3s;
    z-index: 1000;
}

.mobile-filters.open {
    right: 0;
}

.quick-tag, .chip {
    display: inline-block;
    padding: 8px 16px;
    margin: 4px;
    border-radius: 20px;
    background: #f0f0f0;
    cursor: pointer;
}

.quick-tag.active, .chip.active {
    background: #4A90E2;
    color: white;
}
</style>
```

---

## 🎓 Search Tips & Best Practices

### Effective Search Strategies

=== "For Specific Images"
    ```
    1. Use exact phrases: "red sports car"
    2. Add context: "red sports car mountain road"
    3. Include style: "red sports car photorealistic"
    ```

=== "For Similar Images"
    ```
    1. Use tags: tag:nature tag:landscape
    2. Filter by provider: provider:gemini
    3. Set resolution: resolution:1024x1024
    ```

=== "For Recent Work"
    ```
    1. Date filter: after:2025-10-01
    2. This week: Quick filter → "This Week"
    3. Sort by newest: Default sorting
    ```

=== "For Quality Images"
    ```
    1. High-res filter: Quick filter → "High Resolution"
    2. Specific provider: provider:gemini
    3. Tagged quality: tag:8k tag:professional
    ```

### Common Search Patterns

```python
# Pattern: Find all high-quality portraits from last month
images = GeneratedImage.objects.filter(
    category='portrait',
    width__gte=1024,
    created_at__gte=timezone.now() - timedelta(days=30)
).order_by('-created_at')

# Pattern: Get product photos ready for use
products = GeneratedImage.objects.filter(
    tags__contains=['product'],
    tags__contains=['realistic'],
    width__gte=1024,
    output_format='PNG'
)

# Pattern: Find similar style images
reference = GeneratedImage.objects.get(id=123)
similar = GeneratedImage.objects.filter(
    provider=reference.provider,
    tags__overlap=reference.tags
).exclude(id=reference.id)[:10]
```

---

## 📊 Search Statistics Dashboard

### View Search Analytics

```python
def search_dashboard():
    """Generate search analytics dashboard"""
    from django.db.models import Count, Avg
    from datetime import timedelta
    
    last_30_days = timezone.now() - timedelta(days=30)
    
    stats = {
        # Total searches
        'total_searches': SearchQuery.objects.filter(
            timestamp__gte=last_30_days
        ).count(),
        
        # Popular searches
        'popular_searches': SearchQuery.get_popular_searches(10),
        
        # Average results per search
        'avg_results': SearchQuery.objects.filter(
            timestamp__gte=last_30_days
        ).aggregate(Avg('results_count'))['results_count__avg'],
        
        # Most searched tags
        'popular_tags': GeneratedImage.objects.values('tags').annotate(
            count=Count('id')
        ).order_by('-count')[:10],
        
        # Search trends
        'daily_searches': SearchQuery.objects.filter(
            timestamp__gte=last_30_days
        ).extra({'date': 'date(timestamp)'}).values('date').annotate(
            count=Count('id')
        ).order_by('date')
    }
    
    return stats
```

---

## 🔗 Integration with External Tools

### Export Search Results

```python
def export_search_csv(queryset, filename='search_results.csv'):
    """Export search results to CSV"""
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Prompt', 'Provider', 'Model', 'Resolution', 'Created'])
    
    for img in queryset:
        writer.writerow([
            img.id,
            img.prompt,
            img.provider,
            img.model_used,
            f"{img.width}x{img.height}",
            img.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    return response
```

### API Search Endpoint

```python
# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST'])
def search_api(request):
    """API endpoint for searching images"""
    if request.method == 'GET':
        query = request.GET.get('q', '')
        results = search_basic(query)
    else:
        filters = request.data
        results = combined_search(filters)
    
    # Serialize results
    data = [{
        'id': img.id,
        'prompt': img.prompt,
        'provider': img.provider,
        'width': img.width,
        'height': img.height,
        'tags': img.tags,
        'created_at': img.created_at.isoformat()
    } for img in results[:100]]  # Limit to 100 results
    
    return Response({
        'count': len(data),
        'results': data
    })
```

---

<div align="center">

**Master your image library with powerful search and organization tools!**

[← Back to Features](features.md) | [Next: API Reference →](api-reference.md)

</div>