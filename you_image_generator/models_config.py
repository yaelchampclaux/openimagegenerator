# models_config.py - FUSION VERSION
# Configuration centralisée des capacités de chaque modèle

MODELS_CONFIG = {
    'cloudflare': {
        'name': 'Cloudflare AI',
        'max_resolution': 1024,
        'default_resolution': {'width': 1024, 'height': 1024},
        'aspect_ratios': ['1:1', '16:9', '9:16'],
        'formats': ['PNG'],
        'default_format': 'PNG',
        'supports_negative_prompt': False,
        'supports_cfg_scale': False,
        'supports_seed': False,
        'supports_style_preset': False,
        'models': {
            'sdxl': {
                'name': 'Stable Diffusion XL',
                'max_resolution': 1024,
                'default_resolution': {'width': 1024, 'height': 1024},
            },
            'dreamshaper': {
                'name': 'DreamShaper 8 LCM',
                'max_resolution': 1024,
                'default_resolution': {'width': 512, 'height': 512},
            },
            'stable-diffusion': {
                'name': 'Stable Diffusion 1.5',
                'max_resolution': 512,
                'default_resolution': {'width': 512, 'height': 512},
            },
        }
    },
    'aihorde': {
        'name': 'AI Horde',
        'max_resolution': 1024,
        'default_resolution': {'width': 512, 'height': 512},
        'aspect_ratios': ['1:1', '16:9', '9:16', '4:3', '3:4'],
        'formats': ['PNG'],
        'default_format': 'PNG',
        'supports_negative_prompt': False,
        'supports_cfg_scale': True,
        'supports_seed': False,
        'supports_style_preset': False,
        'models': {
            'sdxl': {
                'name': 'Stable Diffusion XL',
                'max_resolution': 1024,
                'default_resolution': {'width': 512, 'height': 512},
            },
            'deliberate': {
                'name': 'Deliberate',
                'max_resolution': 1024,
                'default_resolution': {'width': 512, 'height': 512},
            },
            'dreamshaper': {
                'name': 'DreamShaper',
                'max_resolution': 1024,
                'default_resolution': {'width': 512, 'height': 512},
            },
        }
    },
    'segmind': {
        'name': 'Segmind',
        'max_resolution': 1024,
        'default_resolution': {'width': 1024, 'height': 1024},
        'aspect_ratios': ['1:1', '16:9', '9:16', '4:3', '3:4'],
        'formats': ['PNG'],
        'default_format': 'PNG',
        'supports_negative_prompt': True,
        'supports_cfg_scale': True,
        'supports_seed': True,
        'supports_style_preset': False,
        'models': {
            'sdxl': {
                'name': 'SDXL 1.0',
                'max_resolution': 1024,
                'default_resolution': {'width': 1024, 'height': 1024},
            },
            'sd-1.5': {
                'name': 'Stable Diffusion 1.5',
                'max_resolution': 512,
                'default_resolution': {'width': 512, 'height': 512},
            },
            'kandinsky': {
                'name': 'Kandinsky 2.2',
                'max_resolution': 1024,
                'default_resolution': {'width': 1024, 'height': 1024},
            },
        }
    },
    'prodia': {
        'name': 'Prodia',
        'max_resolution': 1024,
        'default_resolution': {'width': 512, 'height': 512},
        'aspect_ratios': ['1:1', '16:9', '9:16'],
        'formats': ['PNG'],
        'default_format': 'PNG',
        'supports_negative_prompt': True,
        'supports_cfg_scale': True,
        'supports_seed': True,
        'supports_style_preset': False,
        'models': {
            'sdxl': {
                'name': 'SDXL',
                'max_resolution': 1024,
                'default_resolution': {'width': 512, 'height': 512},
            },
            'dreamshaper': {
                'name': 'DreamShaper 8',
                'max_resolution': 1024,
                'default_resolution': {'width': 512, 'height': 512},
            },
            'realistic-vision': {
                'name': 'Realistic Vision V5.1',
                'max_resolution': 1024,
                'default_resolution': {'width': 512, 'height': 512},
            },
        }
    },
    'pollinations': {
        'name': 'Pollinations.ai',
        'max_resolution': 1024,
        'default_resolution': {'width': 512, 'height': 512},
        'aspect_ratios': ['1:1', '16:9', '9:16', '4:3', '3:4'],
        'formats': ['PNG'],
        'default_format': 'PNG',
        'supports_negative_prompt': False,
        'supports_cfg_scale': False,
        'supports_seed': False,
        'supports_style_preset': False,
        'models': {
            'default': {
                'name': 'Pollinations (no model selection)',
                'max_resolution': 1024,
                'default_resolution': {'width': 512, 'height': 512},
            },
        }
    },
    'huggingface': {
        'name': 'Hugging Face',
        'max_resolution': 1024,
        'default_resolution': {'width': 1024, 'height': 1024},
        'aspect_ratios': ['1:1'],
        'formats': ['PNG'],
        'default_format': 'PNG',
        'supports_negative_prompt': True,
        'supports_cfg_scale': True,
        'supports_seed': True,
        'supports_style_preset': True,
        'models': {
            'sdxl-lightning': {
                'name': 'SDXL Lightning',
                'max_resolution': 1024,
                'default_resolution': {'width': 1024, 'height': 1024},
                'free': True,
            },
        }
    },
    'subnp': {
        'name': 'Subnp',
        'max_resolution': 1024,
        'default_resolution': {'width': 1024, 'height': 1024},
        'aspect_ratios': ['1:1'],
        'formats': ['PNG'],
        'default_format': 'PNG',
        'supports_negative_prompt': False,
        'supports_cfg_scale': False,
        'supports_seed': False,
        'supports_style_preset': False,
        'models': {
            'magic': {
                'name': 'Subnp Magic',
                'max_resolution': 1024,
                'default_resolution': {'width': 1024, 'height': 1024},
                'aspect_ratios': ['1:1'],
                'formats': ['PNG'],
                'default_format': 'PNG',
                'supports_negative_prompt': False,
                'supports_cfg_scale': False,
                'supports_seed': False,
                'supports_style_preset': False,
            },
        }
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
    'deepai': {
        'name': 'DeepAI',
        'max_resolution': 512,
        'default_resolution': {'width': 512, 'height': 512},
        'aspect_ratios': ['1:1'],
        'formats': ['PNG', 'JPEG'],
        'default_format': 'PNG',
        'supports_negative_prompt': True,
        'supports_cfg_scale': False,
        'supports_seed': False,
        'supports_style_preset': False,
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
    """Retourne la configuration d'un modèle spécifique"""
    if provider == 'huggingface':
        if hf_model and 'models' in MODELS_CONFIG['huggingface']:
            # Retourne la config du modèle spécifique
            return MODELS_CONFIG['huggingface']['models'].get(
                hf_model, 
                MODELS_CONFIG['huggingface']['models']['flux-schnell']
            )
        # Retourne la config générale si pas de modèle spécifique
        return MODELS_CONFIG['huggingface']
    elif provider == 'subnp':
        if hf_model and 'models' in MODELS_CONFIG['subnp']:
            return MODELS_CONFIG['subnp']['models'].get(
                hf_model,
                MODELS_CONFIG['subnp']['models']['magic']
            )
        return MODELS_CONFIG['subnp']
    elif provider == 'pollinations':
        if hf_model and 'models' in MODELS_CONFIG['pollinations']:
            return MODELS_CONFIG['pollinations']['models'].get(
                hf_model,
                MODELS_CONFIG['pollinations']['models']['flux']
            )
        return MODELS_CONFIG['pollinations']
    return MODELS_CONFIG.get(provider, MODELS_CONFIG.get('pollinations', {}))

def get_dimensions_from_ratio(aspect_ratio, base_resolution):
    """Calcule les dimensions à partir d'un aspect ratio"""
    calculator = ASPECT_RATIO_DIMENSIONS.get(aspect_ratio)
    if calculator:
        return calculator(base_resolution)
    return (base_resolution, base_resolution)
