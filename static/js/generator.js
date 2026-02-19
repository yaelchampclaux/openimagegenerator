let modelsConfig = {};
let currentGeneratedData = {};
let allImages = [];
const IMAGES_PER_PAGE = 20;
let currentPage = 1;

document.addEventListener('DOMContentLoaded', function() {
    // Charger les images depuis le script JSON
    const imagesDataElement = document.getElementById('images-data');
    if (imagesDataElement) {
        try {
            allImages = JSON.parse(imagesDataElement.textContent);
        } catch (e) {
            console.error('Error parsing images data:', e);
            allImages = [];
        }
    }

    loadModelsConfig().then(() => {
        const providerInput = document.getElementById('providerInput');
        updateAdvancedOptions(providerInput.value);
        if (allImages.length > 0) renderGallery();
    });
});

// Charger la configuration des modèles ET populer les sélecteurs
async function loadModelsConfig() {
    try {
        const response = await fetch(window.ALL_CONFIGS_URL);
        modelsConfig = await response.json();
        
        // Populer les sélecteurs de modèles
        populateModelSelectors();
    } catch (error) {
        console.error('Error loading models config:', error);
    }
}

// Populer les sélecteurs de modèles dynamiquement
function populateModelSelectors() {
    // Pollinations
    const pollinationsSelect = document.getElementById('pollinations_model');
    if (pollinationsSelect && modelsConfig.pollinations && modelsConfig.pollinations.models) {
        pollinationsSelect.innerHTML = '';
        Object.keys(modelsConfig.pollinations.models).forEach(modelKey => {
            const model = modelsConfig.pollinations.models[modelKey];
            const option = document.createElement('option');
            option.value = modelKey;
            option.textContent = model.name;
            if (modelKey === 'flux') option.selected = true;
            pollinationsSelect.appendChild(option);
        });
    }
    
    // HuggingFace
    const hfSelect = document.getElementById('hf_model');
    if (hfSelect && modelsConfig.huggingface && modelsConfig.huggingface.models) {
        hfSelect.innerHTML = '';
        Object.keys(modelsConfig.huggingface.models).forEach(modelKey => {
            const model = modelsConfig.huggingface.models[modelKey];
            const option = document.createElement('option');
            option.value = modelKey;
            option.textContent = model.name;
            if (modelKey === 'sdxl-lightning') option.selected = true;
            hfSelect.appendChild(option);
        });
    }
    
    // Subnp
    const subnpSelect = document.getElementById('subnp_model');
    if (subnpSelect && modelsConfig.subnp && modelsConfig.subnp.models) {
        subnpSelect.innerHTML = '';
        Object.keys(modelsConfig.subnp.models).forEach(modelKey => {
            const model = modelsConfig.subnp.models[modelKey];
            const option = document.createElement('option');
            option.value = modelKey;
            option.textContent = model.name;
            if (modelKey === 'magic') option.selected = true;
            subnpSelect.appendChild(option);
        });
    }
}

// Mettre à jour les options selon le modèle sélectionné
function updateAdvancedOptions(provider, modelKey = null) {
    let config = modelsConfig[provider] || modelsConfig['pollinations'];
    
    // Si provider a des modèles, utiliser la config du modèle spécifique
    if (config.models && modelKey) {
        config = config.models[modelKey] || config;
    } else if (config.models) {
        // Utiliser le premier modèle par défaut
        const firstModel = Object.keys(config.models)[0];
        config = config.models[firstModel] || config;
    }

    if (!config || !config.default_resolution) {
        console.warn('Invalid config for:', provider, modelKey);
        return;
    }

    // Mettre à jour les dimensions par défaut
    const widthInput = document.getElementById('width');
    const heightInput = document.getElementById('height');
    widthInput.value = config.default_resolution.width;
    heightInput.value = config.default_resolution.height;
    widthInput.max = config.max_resolution;
    heightInput.max = config.max_resolution;

    // Mettre à jour les aspect ratios
    const ratioSelect = document.getElementById('aspect_ratio');
    const parentConfig = modelsConfig[provider];
    const aspectRatios = parentConfig.aspect_ratios || ['1:1'];
    
    ratioSelect.innerHTML = '';
    aspectRatios.forEach(ratio => {
        const option = document.createElement('option');
        option.value = ratio;
        option.textContent = ratio + (ratio === '1:1' ? ' (Square)' : 
                                        ratio === '16:9' ? ' (Landscape)' :
                                        ratio === '9:16' ? ' (Portrait)' : '');
        if (ratio === '1:1') option.selected = true;
        ratioSelect.appendChild(option);
    });

    // Mettre à jour les formats
    const formatSelect = document.getElementById('output_format');
    const formats = parentConfig.formats || ['PNG'];
    formatSelect.innerHTML = '';
    formats.forEach(format => {
        const option = document.createElement('option');
        option.value = format;
        option.textContent = format;
        if (format === parentConfig.default_format) option.selected = true;
        formatSelect.appendChild(option);
    });

    // Afficher/masquer les options avancées selon support
    document.getElementById('seedGroup').style.display = parentConfig.supports_seed ? 'block' : 'none';
    document.getElementById('cfgGroup').style.display = parentConfig.supports_cfg_scale ? 'block' : 'none';
}

// Calculer dimensions depuis aspect ratio
function calculateDimensionsFromRatio() {
    const ratio = document.getElementById('aspect_ratio').value;
    const widthInput = document.getElementById('width');
    const heightInput = document.getElementById('height');
    const baseResolution = parseInt(widthInput.value);

    const ratioMap = {
        '1:1': [baseResolution, baseResolution],
        '16:9': [baseResolution, Math.floor(baseResolution * 9 / 16)],
        '9:16': [Math.floor(baseResolution * 9 / 16), baseResolution],
        '4:3': [baseResolution, Math.floor(baseResolution * 3 / 4)],
        '3:4': [Math.floor(baseResolution * 3 / 4), baseResolution],
        '21:9': [baseResolution, Math.floor(baseResolution * 9 / 21)],
        '9:21': [Math.floor(baseResolution * 9 / 21), baseResolution],
    };

    const [width, height] = ratioMap[ratio] || [baseResolution, baseResolution];
    widthInput.value = width;
    heightInput.value = height;
}

// Provider selection
const providerCards = document.querySelectorAll('.provider-card');
const providerInput = document.getElementById('providerInput');
const pollinationsModelSelector = document.getElementById('pollinationsModelSelector');
const pollinationsModelSelect = document.getElementById('pollinations_model');
const hfModelSelector = document.getElementById('hfModelSelector');
const hfModelSelect = document.getElementById('hf_model');
const subnpModelSelector = document.getElementById('subnpModelSelector');
const subnpModelSelect = document.getElementById('subnp_model');

const initialProvider = providerInput.value;
document.querySelector(`[data-provider="${initialProvider}"]`)?.classList.add('selected');

providerCards.forEach(card => {
    card.addEventListener('click', function() {
        providerCards.forEach(c => c.classList.remove('selected'));
        this.classList.add('selected');
        const provider = this.dataset.provider;
        providerInput.value = provider;
        
        // Masquer tous les sélecteurs
        pollinationsModelSelector.style.display = 'none';
        hfModelSelector.style.display = 'none';
        subnpModelSelector.style.display = 'none';
        
        // Afficher le bon sélecteur (sauf Pollinations qui n'a qu'un modèle)
        if (provider === 'huggingface') {
            hfModelSelector.style.display = 'block';
            updateAdvancedOptions(provider, hfModelSelect.value);
        } else if (provider === 'subnp') {
            subnpModelSelector.style.display = 'block';
            updateAdvancedOptions(provider, subnpModelSelect.value);
        } else {
            updateAdvancedOptions(provider);
        }
    });
});

// Changement de modèle Pollinations
if (pollinationsModelSelect) {
    pollinationsModelSelect.addEventListener('change', function() {
        updateAdvancedOptions('pollinations', this.value);
    });
}

// Changement de modèle HF
if (hfModelSelect) {
    hfModelSelect.addEventListener('change', function() {
        updateAdvancedOptions('huggingface', this.value);
    });
}

// Changement de modèle Subnp
if (subnpModelSelect) {
    subnpModelSelect.addEventListener('change', function() {
        updateAdvancedOptions('subnp', this.value);
    });
}

// Changement d'aspect ratio
document.getElementById('aspect_ratio').addEventListener('change', calculateDimensionsFromRatio);

function toggleAdvanced() {
    document.getElementById('advancedOptions').classList.toggle('active');
}

// Form submission
document.getElementById('generateForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const generateBtn = document.getElementById('generateBtn');
    const loading = document.getElementById('loading');
    const resultContainer = document.getElementById('resultContainer');
    const errorMessage = document.getElementById('errorMessage');

    resultContainer.classList.remove('active');
    errorMessage.classList.remove('active');
    loading.classList.add('active');
    generateBtn.disabled = true;

    try {
        const response = await fetch(window.GENERATE_API_URL, {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': formData.get('csrfmiddlewaretoken') }
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById('generatedImage').src = `data:${data.content_type};base64,${data.image_base64}`;
            document.getElementById('resultPrompt').textContent = data.prompt;
            document.getElementById('resultModel').textContent = data.model_used;
            document.getElementById('resultProvider').textContent = data.provider;
            
            // Stocker les données pour le modal
            currentGeneratedData = {
                prompt: data.prompt,
                model: data.model_used,
                width: formData.get('width'),
                height: formData.get('height'),
                format: formData.get('output_format') || 'PNG',
                imageData: `data:${data.content_type};base64,${data.image_base64}`
            };

            resultContainer.classList.add('active');
            resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

            if (data.id) {
                const newImage = {
                    id: data.id,
                    image_data: data.image_base64,
                    prompt: data.prompt,
                    model_used: data.model_used,
                    width: formData.get('width'),
                    height: formData.get('height'),
                    output_format: formData.get('output_format') || 'PNG',
                    style_preset: formData.get('style_preset') || '',
                    is_favorite: false
                };
                
                allImages.unshift(newImage);
                currentPage = 1;
                renderGallery();
                
                setTimeout(() => {
                    document.querySelector('.gallery')?.scrollIntoView({ 
                        behavior: 'smooth', 
                        block: 'start' 
                    });
                }, 500);
            }
        } else {
            errorMessage.textContent = data.error || 'An error occurred';
            errorMessage.classList.add('active');
        }
    } catch (error) {
        errorMessage.textContent = 'Network error. Please try again.';
        errorMessage.classList.add('active');
    } finally {
        loading.classList.remove('active');
        generateBtn.disabled = false;
    }
});

function generateAnother() {
    document.getElementById('resultContainer').classList.remove('active');
    document.getElementById('prompt').focus();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Gallery with pagination
function renderGallery() {
    const gallery = document.getElementById('galleryGrid');
    const pagination = document.getElementById('pagination');

    if (!gallery) return;
    const startIndex = (currentPage - 1) * IMAGES_PER_PAGE;
    const endIndex = startIndex + IMAGES_PER_PAGE;
    const pageImages = allImages.slice(startIndex, endIndex);
    gallery.innerHTML = '';
    
    pageImages.forEach(image => {
        const item = document.createElement('div');
        item.className = 'gallery-item';
        item.style.position = 'relative';
        
        item.innerHTML = `
            <span class="favorite-star" 
                data-image-id="${image.id}"
                style="position: absolute; top: 10px; right: 10px; 
                        font-size: 24px; cursor: pointer; z-index: 10;
                        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.8));"
                title="${image.is_favorite ? 'Remove from favorites' : 'Add to favorites'}">
                ${image.is_favorite ? '⭐' : '☆'}
            </span>
            
            <img src="data:image/png;base64,${image.image_data}" 
                alt="${image.prompt}"
                style="cursor: pointer;">
            
            <div class="gallery-item-info">
                <div class="gallery-item-prompt">
                    ${image.prompt.substring(0, 60)}${image.prompt.length > 60 ? '...' : ''}
                </div>
                <div class="gallery-item-model">${image.model_used}</div>
                
                <div class="action-buttons" style="display: flex; gap: 5px; margin-top: 8px;">
                    <button class="btn-download"
                            data-image-id="${image.id}"
                            style="flex: 1; padding: 6px 10px; background: #2196F3; color: white; 
                                border: none; border-radius: 4px; cursor: pointer; 
                                font-size: 12px; font-weight: 600;">
                        ⬇️ Download
                    </button>
                </div>
            </div>
        `;
        
        const imgElement = item.querySelector('img');
        imgElement.addEventListener('click', () => {
            openModal(`data:image/png;base64,${image.image_data}`, {
                prompt: image.prompt,
                model: image.model_used,
                width: image.width || 'Unknown',
                height: image.height || 'Unknown',
                format: image.output_format || 'PNG',
                style_preset: image.style_preset || '',
                imageData: `data:image/png;base64,${image.image_data}`
            });
        });
        
        const star = item.querySelector('.favorite-star');
        star.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleFavorite(image.id, star);
        });
        
        const btnDownload = item.querySelector('.btn-download');
        btnDownload.addEventListener('click', (e) => {
            e.stopPropagation();
            const link = document.createElement('a');
            link.href = `data:image/png;base64,${image.image_data}`;
            link.download = `openimage_${image.id}.png`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });
                        
        gallery.appendChild(item);
    });
    
    const totalPages = Math.ceil(allImages.length / IMAGES_PER_PAGE);
    pagination.innerHTML = `
        <button class="pagination-btn" onclick="changePage(-1)" ${currentPage === 1 ? 'disabled' : ''}>← Previous</button>
        <span class="pagination-info">Page ${currentPage} of ${totalPages}</span>
        <button class="pagination-btn" onclick="changePage(1)" ${currentPage === totalPages ? 'disabled' : ''}>Next →</button>
    `;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function toggleFavorite(imageId, starElement) {
    try {
        const response = await fetch('/api/favorites/toggle/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ image_id: imageId })
        });
        
        const data = await response.json();
        
        if (data.success) {
            starElement.textContent = data.is_favorite ? '⭐' : '☆';
            starElement.title = data.is_favorite ? 'Remove from favorites' : 'Add to favorites';
            
            const imageIndex = allImages.findIndex(img => img.id === imageId);
            if (imageIndex !== -1) {
                allImages[imageIndex].is_favorite = data.is_favorite;
            }
        }
    } catch (error) {
        console.error('Error toggling favorite:', error);
    }
}

function changePage(direction) {
    currentPage += direction;
    renderGallery();
    document.querySelector('.gallery').scrollIntoView({ behavior: 'smooth' });
}

// Modal functions
let currentModalData = {};

function openModal(imageSrc, data) {
    const modal = document.getElementById('imageModal');
    document.getElementById('modalImage').src = imageSrc;
    document.getElementById('modalPrompt').textContent = data.prompt;
    document.getElementById('modalModel').textContent = data.model;
    document.getElementById('modalResolution').textContent = `${data.width} × ${data.height} px`;
    document.getElementById('modalFormat').textContent = data.format;
    
    const stylePresetRow = document.getElementById('modalStylePresetRow');
    const stylePresetElement = document.getElementById('modalStylePreset');
    
    if (data.style_preset && data.style_preset !== '') {
        stylePresetElement.textContent = data.style_preset;
        stylePresetRow.style.display = 'flex';
    } else {
        stylePresetRow.style.display = 'none';
    }
    
    currentModalData = data;
    modal.classList.add('active');
}

function closeModal() {
    document.getElementById('imageModal').classList.remove('active');
}

function copyPrompt() {
    navigator.clipboard.writeText(currentModalData.prompt).then(() => {
        alert('Prompt copied to clipboard!');
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

function downloadImage() {
    const link = document.createElement('a');
    link.href = currentModalData.imageData;
    link.download = `ai-generated-${Date.now()}.${currentModalData.format.toLowerCase()}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

document.getElementById('imageModal').addEventListener('click', function(e) {
    if (e.target === this) closeModal();
});

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeModal();
});

// Test Free APIs button
async function testFreeAPIs() {
    const btn = document.getElementById('testApisBtn');
    const resultDiv = document.getElementById('testApisResult');
    
    btn.textContent = '⏳ Testing...';
    btn.disabled = true;
    resultDiv.style.display = 'block';
    resultDiv.innerHTML = '⏳ Testing all free APIs (may take 30s)...';
    
    try {
        const response = await fetch(window.TEST_FREE_APIS_URL);
        const data = await response.json();
        
        let html = '<strong>🔍 Free API Status:</strong><br><br>';
        
        for (const [provider, info] of Object.entries(data.results)) {
            const icon = info.status === 'ok' ? '✅' : '❌';
            const color = info.status === 'ok' ? '#16a34a' : '#dc2626';
            const name = provider.charAt(0).toUpperCase() + provider.slice(1);
            
            html += `<div style="margin-bottom:8px;">`;
            html += `<strong style="color:${color}">${icon} ${name}</strong>: ${info.message}`;
            
            if (info.models.length > 0) {
                html += `<br><span style="color:#666; font-size:12px;">Models: ${info.models.join(', ')}</span>`;
            }
            html += `</div>`;
        }
        
        resultDiv.innerHTML = html;
        
    } catch(e) {
        resultDiv.innerHTML = `❌ Test failed: ${e.message}`;
    } finally {
        btn.textContent = '🔍 Test Free APIs';
        btn.disabled = false;
    }
}

// Initialize
loadModelsConfig().then(() => {
    updateAdvancedOptions(initialProvider);
    renderGallery();
});