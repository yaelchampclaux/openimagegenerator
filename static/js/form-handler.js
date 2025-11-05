// Configuration des providers (doit correspondre à models_config.py)
const PROVIDER_CONFIGS = {
    'pollinations': {
        supports_negative_prompt: false,
        supports_cfg_scale: false,
        supports_seed: false,
        supports_style_preset: false
    },
    'gemini': {
        supports_negative_prompt: false,
        supports_cfg_scale: false,
        supports_seed: false,
        supports_style_preset: true
    },
    'huggingface': {
        'flux-schnell': {
            supports_negative_prompt: false,
            supports_cfg_scale: false,
            supports_seed: false,
            supports_style_preset: true
        },
        'stable-diffusion-xl': {
            supports_negative_prompt: true,
            supports_cfg_scale: true,
            supports_seed: true,
            supports_style_preset: true
        },
        'stable-diffusion-3': {
            supports_negative_prompt: true,
            supports_cfg_scale: true,
            supports_seed: true,
            supports_style_preset: true
        }
    },
    'deepai': {
        supports_negative_prompt: true,
        supports_cfg_scale: false,
        supports_seed: false,
        supports_style_preset: true
    },
    'runware': {
        supports_negative_prompt: true,
        supports_cfg_scale: true,
        supports_seed: true,
        supports_style_preset: true
    },
    'replicate': {
        supports_negative_prompt: true,
        supports_cfg_scale: true,
        supports_seed: true,
        supports_style_preset: true
    },
    'stability': {
        supports_negative_prompt: true,
        supports_cfg_scale: true,
        supports_seed: true,
        supports_style_preset: true
    }
};

function getCurrentConfig() {
    const providerInput = document.getElementById('providerInput');  // ← Changé
    const hfModel = document.getElementById('hf_model');
    
    if (!providerInput) {
        console.warn('Provider input not found');
        return PROVIDER_CONFIGS.pollinations;
    }
    
    const providerValue = providerInput.value;
    const hfModelValue = hfModel ? hfModel.value : null;
    
    if (providerValue === 'huggingface' && hfModelValue) {
        return PROVIDER_CONFIGS.huggingface[hfModelValue] || PROVIDER_CONFIGS.huggingface['flux-schnell'];
    }
    
    return PROVIDER_CONFIGS[providerValue] || PROVIDER_CONFIGS.pollinations;
}

function updateFormFields() {
    const config = getCurrentConfig();
    const providerInput = document.getElementById('providerInput');  
    if (!providerInput) return;
    
    const provider = providerInput.value;
    
    //console.log('Provider:', provider, 'Config:', config);  // Debug
    
    // Afficher/masquer HF model select
    const hfModelGroup = document.getElementById('hf_model_group');
    if (hfModelGroup) {
        hfModelGroup.style.display = provider === 'huggingface' ? 'block' : 'none';
    }
    
    // Afficher/masquer negative prompt
    const negativePromptInput = document.getElementById('negative_prompt');
    if (negativePromptInput) {
        const negativePromptGroup = negativePromptInput.closest('.form-group');
        if (negativePromptGroup) {
            negativePromptGroup.style.display = config.supports_negative_prompt ? 'block' : 'none';
        }
    }
    
    // Afficher/masquer seed
    const seedGroup = document.getElementById('seedGroup');
    if (seedGroup) {
        seedGroup.style.display = config.supports_seed ? 'block' : 'none';
    }
    
    // Afficher/masquer CFG scale
    const cfgGroup = document.getElementById('cfgGroup');
    if (cfgGroup) {
        cfgGroup.style.display = config.supports_cfg_scale ? 'block' : 'none';
    }
    
    // Avertissement pour style preset
    const stylePreset = document.getElementById('style_preset');
    const stylePresetParent = stylePreset ? stylePreset.closest('.form-group') : null;
    
    if (stylePreset && stylePresetParent) {
        let warningEl = stylePresetParent.querySelector('.style-warning');
        
        if (!config.supports_style_preset) {
            if (!warningEl) {
                warningEl = document.createElement('small');
                warningEl.className = 'style-warning';
                warningEl.style.color = '#f59e0b';
                warningEl.style.display = 'block';
                warningEl.style.marginTop = '5px';
                warningEl.textContent = '⚠️ Style presets may not work well with this provider';
                stylePresetParent.appendChild(warningEl);
            }
        } else {
            if (warningEl) {
                warningEl.remove();
            }
        }
    }
}

function initializeFormHandler() {
    const providerInput = document.getElementById('providerInput');  // ← Changé
    const hfModelSelect = document.getElementById('hf_model');
    
    // Écouter les clics sur les cartes provider
    const providerCards = document.querySelectorAll('.provider-card');
    providerCards.forEach(card => {
        card.addEventListener('click', function() {
            const selectedProvider = this.dataset.provider;
            if (providerInput) {
                providerInput.value = selectedProvider;
            }
            
            // Retirer la classe active de toutes les cartes
            providerCards.forEach(c => c.classList.remove('active'));
            // Ajouter la classe active à la carte cliquée
            this.classList.add('active');
            
            // Mettre à jour les champs
            updateFormFields();
        });
    });
    
    if (hfModelSelect) {
        hfModelSelect.addEventListener('change', updateFormFields);
    }
    
    // Initialiser l'affichage
    updateFormFields();
    
    //console.log('Form handler initialized');
}

// Initialiser au chargement
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeFormHandler);
} else {
    initializeFormHandler();
}