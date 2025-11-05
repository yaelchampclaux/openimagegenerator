# models_config.py
# Configuration centralisée des capacités de chaque modèle

MODELS_CONFIG = {
    'pollinations': {
        'name': 'Pollinations.ai',
        'max_resolution': 2048,
        'default_resolution': {'width': 1024, 'height': 1024},
        'aspect_ratios': ['1:1', '16:9', '9:16', '4:3', '3:4', '21:9', '9:21'],
        'formats': ['PNG'],
        'default_format': 'PNG',
        'supports_negative_prompt': False,
        'supports_cfg_scale': False,
        'supports_seed': False,
        'supports_style_preset': True,
    },
    'gemini': {
        'name': 'Google Gemini',
        'max_resolution': 2048,
        'default_resolution': {'width': 1024, 'height': 1024},
        'aspect_ratios': ['1:1', '3:4', '4:3', '9:16', '16:9'],
        'formats': ['PNG'],
        'default_format': 'PNG',
        'supports_negative_prompt': False,
        'supports_cfg_scale': False,
        'supports_seed': False,
        'supports_style_preset': True,
    },
    'huggingface': {
        'models': {
            'flux-schnell': {
                'name': 'FLUX.1 Schnell',
                'max_resolution': 1024,
                'default_resolution': {'width': 1024, 'height': 1024},
                'aspect_ratios': ['1:1'],
                'formats': ['PNG'],
                'default_format': 'PNG',
                'supports_negative_prompt': True,
                'supports_cfg_scale': True,
                'supports_seed': True,
                'supports_style_preset': True,
            },
            'stable-diffusion-xl': {
                'name': 'Stable Diffusion XL',
                'max_resolution': 1024,
                'default_resolution': {'width': 1024, 'height': 1024},
                'aspect_ratios': ['1:1', '3:4', '4:3'],
                'formats': ['PNG'],
                'default_format': 'PNG',
                'supports_negative_prompt': True,
                'supports_cfg_scale': True,
                'supports_seed': True,
                'supports_style_preset': True,
            },
            'stable-diffusion-3': {
                'name': 'Stable Diffusion 3',
                'max_resolution': 1024,
                'default_resolution': {'width': 1024, 'height': 1024},
                'aspect_ratios': ['1:1', '3:4', '4:3'],
                'formats': ['PNG'],
                'default_format': 'PNG',
                'supports_negative_prompt': True,
                'supports_cfg_scale': True,
                'supports_seed': True,
                'supports_style_preset': True,
            },
        }
    },
    'runware': {
        'name': 'Runware',
        'max_resolution': 2048,
        'default_resolution': {'width': 1024, 'height': 1024},
        'aspect_ratios': ['1:1', '16:9', '9:16', '4:3', '3:4'],
        'formats': ['PNG', 'JPEG', 'WEBP'],
        'default_format': 'PNG',
        'supports_negative_prompt': True,
        'supports_cfg_scale': True,
        'supports_seed': True,
        'supports_style_preset': True,
    },
    'replicate': {
        'name': 'Replicate',
        'max_resolution': 1024,
        'default_resolution': {'width': 1024, 'height': 1024},
        'aspect_ratios': ['1:1', '16:9', '9:16', '4:3', '3:4'],
        'formats': ['PNG', 'JPEG', 'WEBP'],
        'default_format': 'PNG',
        'supports_negative_prompt': True,
        'supports_cfg_scale': True,
        'supports_seed': True,
        'supports_style_preset': True,
    },
    'stability': {
        'name': 'Stability AI',
        'max_resolution': 2048,
        'default_resolution': {'width': 1024, 'height': 1024},
        'aspect_ratios': ['1:1', '16:9', '9:16', '4:3', '3:4', '21:9'],
        'formats': ['PNG', 'JPEG', 'WEBP'],
        'default_format': 'PNG',
        'supports_negative_prompt': True,
        'supports_cfg_scale': True,
        'supports_seed': True,
        'supports_style_preset': True,
    },
}

# Mapping des aspect ratios vers dimensions
ASPECT_RATIO_DIMENSIONS = {
    '1:1': lambda base: (base, base),
    '16:9': lambda base: (base, int(base * 9 / 16)),
    '9:16': lambda base: (int(base * 9 / 16), base),
    '4:3': lambda base: (base, int(base * 3 / 4)),
    '3:4': lambda base: (int(base * 3 / 4), base),
    '21:9': lambda base: (base, int(base * 9 / 21)),
    '9:21': lambda base: (int(base * 9 / 21), base),
}

def get_model_config(provider, hf_model=None):
    """
    Retourne la configuration d'un modèle spécifique
    """
    if provider == 'huggingface' and hf_model:
        return MODELS_CONFIG['huggingface']['models'].get(hf_model, 
                MODELS_CONFIG['huggingface']['models']['flux-schnell'])
    return MODELS_CONFIG.get(provider, MODELS_CONFIG['pollinations'])

def get_dimensions_from_ratio(aspect_ratio, base_resolution):
    """
    Calcule les dimensions à partir d'un aspect ratio
    """
    calculator = ASPECT_RATIO_DIMENSIONS.get(aspect_ratio)
    if calculator:
        return calculator(base_resolution)
    return (base_resolution, base_resolution)