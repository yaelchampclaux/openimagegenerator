# you_image_generator/styles.py
"""
Style Presets for AI Image Generation

Provides predefined style modifiers that can be applied to prompts
to achieve specific artistic looks consistently across providers.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class StylePreset:
    """
    Represents a style preset configuration
    
    Attributes:
        key: Unique identifier for the style
        name: Display name
        description: Human-readable description
        suffix: Text to append to prompt
        negative: Negative prompt additions (optional)
        recommended_providers: List of best providers for this style
        quality_rating: 1-5 rating of typical quality
        icon: Emoji or icon for UI
        category: Style category (artistic, realistic, etc.)
    """
    key: str
    name: str
    description: str
    suffix: str
    negative: str = ""
    recommended_providers: List[str] = None
    quality_rating: int = 4
    icon: str = "🎨"
    category: str = "general"


# Define all available style presets
STYLE_PRESETS = {
    'realistic': StylePreset(
        key='realistic',
        name='Realistic Photo',
        description='Professional photography style with photorealistic quality',
        suffix='photorealistic, professional photography, studio lighting, 8k resolution, high detail, sharp focus, natural colors',
        negative='anime, cartoon, painting, drawing, illustration, low quality, blurry, distorted',
        recommended_providers=['gemini', 'replicate', 'stability'],
        quality_rating=5,
        icon='📷',
        category='realistic'
    ),
    
    'anime': StylePreset(
        key='anime',
        name='Anime/Manga',
        description='Japanese animation and manga art style',
        suffix='anime style, manga art, vibrant colors, cel-shaded, clean lines, digital art, anime aesthetic',
        negative='photorealistic, 3d render, western cartoon, photograph',
        recommended_providers=['huggingface', 'gemini', 'replicate'],
        quality_rating=5,
        icon='🎌',
        category='artistic'
    ),
    
    'oil_painting': StylePreset(
        key='oil_painting',
        name='Oil Painting',
        description='Classical oil painting technique with visible brush strokes',
        suffix='oil painting, canvas texture, visible brush strokes, impressionist style, rich colors, artistic, painted masterpiece',
        negative='photograph, digital art, 3d render, flat colors',
        recommended_providers=['stability', 'huggingface', 'gemini'],
        quality_rating=4,
        icon='🖼️',
        category='artistic'
    ),
    
    'watercolor': StylePreset(
        key='watercolor',
        name='Watercolor',
        description='Soft watercolor painting with flowing colors',
        suffix='watercolor painting, soft edges, pastel colors, paper texture, artistic, flowing, delicate, hand-painted',
        negative='harsh lines, digital, photograph, 3d',
        recommended_providers=['stability', 'gemini', 'huggingface'],
        quality_rating=4,
        icon='🎨',
        category='artistic'
    ),
    
    'cyberpunk': StylePreset(
        key='cyberpunk',
        name='Cyberpunk',
        description='Futuristic dystopian aesthetic with neon lights',
        suffix='cyberpunk style, neon lights, dark atmosphere, futuristic, dystopian, high tech, sci-fi, dramatic lighting, cinematic',
        negative='bright, cheerful, natural, historical, vintage',
        recommended_providers=['gemini', 'replicate', 'pollinations'],
        quality_rating=5,
        icon='🌃',
        category='scifi'
    ),
    
    'fantasy': StylePreset(
        key='fantasy',
        name='Fantasy Art',
        description='Epic fantasy illustration style',
        suffix='fantasy art, epic, magical, detailed, concept art, dramatic lighting, mystical, enchanted, adventure',
        negative='modern, realistic photography, mundane, everyday',
        recommended_providers=['gemini', 'stability', 'replicate'],
        quality_rating=5,
        icon='✨',
        category='fantasy'
    ),
    
    'minimalist': StylePreset(
        key='minimalist',
        name='Minimalist',
        description='Clean, simple, modern design',
        suffix='minimalist, clean lines, simple, modern, flat design, minimal details, geometric, elegant, uncluttered',
        negative='complex, detailed, ornate, busy, cluttered',
        recommended_providers=['pollinations', 'huggingface', 'gemini'],
        quality_rating=4,
        icon='⬜',
        category='modern'
    ),
    
    'vintage': StylePreset(
        key='vintage',
        name='Vintage Film',
        description='Retro photography with film grain and faded colors',
        suffix='vintage photo, film grain, faded colors, retro, nostalgic, analog photography, 1970s aesthetic, aged photograph',
        negative='modern, digital, sharp, vibrant, contemporary',
        recommended_providers=['stability', 'huggingface', 'gemini'],
        quality_rating=4,
        icon='📸',
        category='retro'
    ),
    
    'comic': StylePreset(
        key='comic',
        name='Comic Book',
        description='American comic book and graphic novel style',
        suffix='comic book style, bold lines, halftone dots, vibrant colors, action-packed, graphic novel, ink drawing, pop art',
        negative='photograph, realistic, 3d, subtle, muted',
        recommended_providers=['huggingface', 'replicate', 'pollinations'],
        quality_rating=4,
        icon='💥',
        category='artistic'
    ),
    
    'abstract': StylePreset(
        key='abstract',
        name='Abstract Art',
        description='Modern abstract and geometric art',
        suffix='abstract art, geometric shapes, colorful, modern art, non-representational, contemporary, artistic expression',
        negative='realistic, photograph, detailed, representational',
        recommended_providers=['pollinations', 'stability', 'gemini'],
        quality_rating=4,
        icon='🔷',
        category='artistic'
    ),
    
    'sketch': StylePreset(
        key='sketch',
        name='Pencil Sketch',
        description='Hand-drawn pencil or charcoal sketch',
        suffix='pencil sketch, hand-drawn, graphite, detailed linework, sketch art, black and white, artistic drawing',
        negative='color, photograph, digital, painting',
        recommended_providers=['huggingface', 'stability'],
        quality_rating=3,
        icon='✏️',
        category='artistic'
    ),
    
    'pixel_art': StylePreset(
        key='pixel_art',
        name='Pixel Art',
        description='Retro video game pixel art style',
        suffix='pixel art, 8-bit, retro gaming, pixelated, sprite art, retro game graphics, low resolution aesthetic',
        negative='high resolution, smooth, realistic, photograph',
        recommended_providers=['pollinations', 'huggingface'],
        quality_rating=3,
        icon='👾',
        category='retro'
    ),
    
    'steampunk': StylePreset(
        key='steampunk',
        name='Steampunk',
        description='Victorian-era science fiction with mechanical elements',
        suffix='steampunk style, Victorian era, brass and copper, gears and cogs, mechanical, industrial, retro-futuristic',
        negative='modern, digital, minimalist, futuristic',
        recommended_providers=['stability', 'gemini', 'replicate'],
        quality_rating=4,
        icon='⚙️',
        category='scifi'
    ),
    
    'impressionist': StylePreset(
        key='impressionist',
        name='Impressionist',
        description='Impressionist painting style like Monet',
        suffix='impressionist painting, loose brushwork, emphasis on light, Claude Monet style, plein air, color theory',
        negative='photograph, detailed, sharp, hyperrealistic',
        recommended_providers=['stability', 'gemini'],
        quality_rating=4,
        icon='🌅',
        category='artistic'
    ),
    
    'gothic': StylePreset(
        key='gothic',
        name='Gothic Dark',
        description='Dark gothic aesthetic with dramatic atmosphere',
        suffix='gothic style, dark atmosphere, dramatic shadows, mysterious, Victorian gothic, ornate details, haunting',
        negative='bright, cheerful, minimalist, modern',
        recommended_providers=['stability', 'gemini', 'replicate'],
        quality_rating=4,
        icon='🦇',
        category='dark'
    ),
}


def get_style_preset(key: str) -> Optional[StylePreset]:
    """
    Get a style preset by its key
    
    Args:
        key: Style preset identifier
    
    Returns:
        StylePreset object or None if not found
    """
    return STYLE_PRESETS.get(key)


def get_all_style_presets() -> Dict[str, StylePreset]:
    """Get all available style presets"""
    return STYLE_PRESETS


def get_all_style_presets() -> Dict[str, StylePreset]:
    """Get all available style presets"""
    return STYLE_PRESETS


def get_styles_by_category(category: str) -> Dict[str, StylePreset]:
    """
    Get all styles in a specific category
    
    Args:
        category: Category name (artistic, realistic, scifi, etc.)
    
    Returns:
        Dictionary of matching style presets
    """
    return {
        key: preset
        for key, preset in STYLE_PRESETS.items()
        if preset.category == category
    }


def get_style_categories() -> List[str]:
    """Get list of all style categories"""
    categories = set(preset.category for preset in STYLE_PRESETS.values())
    return sorted(categories)


def apply_style_to_prompt(
    prompt: str,
    style_key: str,
    include_negative: bool = True
) -> Dict[str, str]:
    """
    Apply a style preset to a prompt
    
    Args:
        prompt: Original user prompt
        style_key: Style preset key
        include_negative: Whether to include negative prompt
    
    Returns:
        Dictionary with 'prompt' and optionally 'negative_prompt'
    
    Example:
        >>> result = apply_style_to_prompt("a red apple", "realistic")
        >>> print(result['prompt'])
        'a red apple, photorealistic, professional photography...'
    """
    style = get_style_preset(style_key)
    
    if not style:
        return {'prompt': prompt}
    
    # Combine original prompt with style suffix
    enhanced_prompt = f"{prompt}, {style.suffix}"
    
    result = {'prompt': enhanced_prompt}
    
    if include_negative and style.negative:
        result['negative_prompt'] = style.negative
    
    return result


def get_recommended_providers_for_style(style_key: str) -> List[str]:
    """
    Get recommended providers for a specific style
    
    Args:
        style_key: Style preset key
    
    Returns:
        List of recommended provider names
    """
    style = get_style_preset(style_key)
    
    if style and style.recommended_providers:
        return style.recommended_providers
    
    # Default recommendations if none specified
    return ['gemini', 'pollinations', 'huggingface']


def get_style_compatibility_matrix() -> Dict[str, Dict[str, int]]:
    """
    Get compatibility scores between styles and providers
    
    Returns:
        Nested dict: {style_key: {provider: score}}
        Score: 1-5 (5 = excellent, 1 = poor)
    """
    matrix = {}
    
    for style_key, preset in STYLE_PRESETS.items():
        matrix[style_key] = {}
        
        # Assign scores based on recommendations
        for provider in ['gemini', 'pollinations', 'huggingface', 
                        'deepai', 'runware', 'replicate', 'stability']:
            if preset.recommended_providers and provider in preset.recommended_providers:
                matrix[style_key][provider] = 5
            else:
                # Default scores for non-recommended
                matrix[style_key][provider] = 3
    
    return matrix


def suggest_style_for_prompt(prompt: str) -> Optional[str]:
    """
    Suggest a style based on prompt content
    
    Args:
        prompt: User's prompt text
    
    Returns:
        Suggested style key or None
    
    Example:
        >>> suggest_style_for_prompt("portrait of a person")
        'realistic'
        >>> suggest_style_for_prompt("fantasy dragon")
        'fantasy'
    """
    prompt_lower = prompt.lower()
    
    # Keywords for each style
    style_keywords = {
        'realistic': ['photo', 'photograph', 'portrait', 'realistic', 'real'],
        'anime': ['anime', 'manga', 'cartoon', 'animated'],
        'fantasy': ['fantasy', 'magic', 'dragon', 'wizard', 'medieval'],
        'cyberpunk': ['cyberpunk', 'neon', 'futuristic', 'dystopia'],
        'minimalist': ['simple', 'minimal', 'clean', 'modern'],
        'vintage': ['vintage', 'retro', 'old', 'nostalgic', '70s', '80s'],
        'abstract': ['abstract', 'geometric', 'pattern'],
    }
    
    # Check for keyword matches
    for style_key, keywords in style_keywords.items():
        if any(keyword in prompt_lower for keyword in keywords):
            return style_key
    
    return None


# Export for templates
def get_styles_for_template():
    """
    Get styles formatted for Django template
    
    Returns:
        List of dictionaries suitable for template rendering
    """
    return [
        {
            'key': preset.key,
            'name': preset.name,
            'description': preset.description,
            'icon': preset.icon,
            'category': preset.category,
            'quality': preset.quality_rating,
        }
        for preset in STYLE_PRESETS.values()
    ]


# Style mixing (experimental)
def mix_styles(style_keys: List[str], weights: Optional[List[float]] = None) -> Dict[str, str]:
    """
    Experimental: Mix multiple style presets
    
    Args:
        style_keys: List of style keys to mix
        weights: Optional weights for each style (must sum to 1.0)
    
    Returns:
        Dictionary with combined prompts
    """
    if not style_keys:
        return {}
    
    if weights is None:
        weights = [1.0 / len(style_keys)] * len(style_keys)
    
    # Combine suffixes
    combined_suffix = ", ".join([
        STYLE_PRESETS[key].suffix
        for key in style_keys
        if key in STYLE_PRESETS
    ])
    
    # Combine negative prompts
    combined_negative = ", ".join([
        STYLE_PRESETS[key].negative
        for key in style_keys
        if key in STYLE_PRESETS and STYLE_PRESETS[key].negative
    ])
    
    return {
        'suffix': combined_suffix,
        'negative': combined_negative
    }