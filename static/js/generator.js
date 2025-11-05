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
        updateAdvancedOptions(providerInput.value);
        if (allImages.length > 0) renderGallery();
    });
});

// Charger la configuration des modèles
async function loadModelsConfig() {
    try {
        const response = await fetch(window.ALL_CONFIGS_URL);//'{% url "you_image_generator:all_configs" %}'
        modelsConfig = await response.json();
    } catch (error) {
        console.error('Error loading models config:', error);
    }
}

// Mettre à jour les options selon le modèle sélectionné
function updateAdvancedOptions(provider, hfModel = null) {
    let config = modelsConfig[provider] || modelsConfig['pollinations'];
    
    // Si Hugging Face, utiliser la config du modèle spécifique
    if (provider === 'huggingface' && hfModel) {
        config = modelsConfig.huggingface.models[hfModel] || modelsConfig.huggingface.models['flux-schnell'];
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
    ratioSelect.innerHTML = '';
    config.aspect_ratios.forEach(ratio => {
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
    formatSelect.innerHTML = '';
    config.formats.forEach(format => {
        const option = document.createElement('option');
        option.value = format;
        option.textContent = format;
        if (format === config.default_format) option.selected = true;
        formatSelect.appendChild(option);
    });

    // Afficher/masquer les options avancées selon support
    document.getElementById('seedGroup').style.display = config.supports_seed ? 'block' : 'none';
    document.getElementById('cfgGroup').style.display = config.supports_cfg_scale ? 'block' : 'none';
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
const hfModelSelector = document.getElementById('hfModelSelector');
const hfModelSelect = document.getElementById('hf_model');

const initialProvider = providerInput.value;
document.querySelector(`[data-provider="${initialProvider}"]`)?.classList.add('selected');

providerCards.forEach(card => {
    card.addEventListener('click', function() {
        providerCards.forEach(c => c.classList.remove('selected'));
        this.classList.add('selected');
        const provider = this.dataset.provider;
        providerInput.value = provider;
        
        // Afficher sélecteur HF si nécessaire
        if (provider === 'huggingface') {
            hfModelSelector.style.display = 'block';
            updateAdvancedOptions(provider, hfModelSelect.value);
        } else {
            hfModelSelector.style.display = 'none';
            updateAdvancedOptions(provider);
        }
    });
});

// Changement de modèle HF
hfModelSelect.addEventListener('change', function() {
    updateAdvancedOptions('huggingface', this.value);
});

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
        const response = await fetch(window.GENERATE_API_URL, { //'{% url "you_image_generator:generate_api" %}'
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
            
            // Recharger la galerie
            location.reload();
        } else {
            errorMessage.textContent = data.error || 'An error occurred';
            if (data.help) errorMessage.textContent += ` - ${data.help}`;
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
    
    //console.log('allImages:', allImages);  
    //console.log('First image:', allImages[0]);  

    if (!gallery) return;
    const startIndex = (currentPage - 1) * IMAGES_PER_PAGE;
    const endIndex = startIndex + IMAGES_PER_PAGE;
    const pageImages = allImages.slice(startIndex, endIndex);
    gallery.innerHTML = '';
    
    pageImages.forEach(image => {
        //console.log('Processing image:', image);  
        const item = document.createElement('div');
        item.className = 'gallery-item';
        item.style.position = 'relative'; // Important pour l'étoile
        
        item.innerHTML = `
            <!-- Étoile favorite (en haut à droite) -->
            <span class="favorite-star" 
                data-image-id="${image.id}"
                style="position: absolute; top: 10px; right: 10px; 
                        font-size: 24px; cursor: pointer; z-index: 10;
                        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.8));"
                title="${image.is_favorite ? 'Remove from favorites' : 'Add to favorites'}">
                ${image.is_favorite ? '⭐' : '☆'}
            </span>
            
            <!-- Image -->
            <img src="data:image/png;base64,${image.image_data}" 
                alt="${image.prompt}"
                style="cursor: pointer;">
            
            <!-- Info existante -->
            <div class="gallery-item-info">
                <div class="gallery-item-prompt">
                    ${image.prompt.substring(0, 60)}${image.prompt.length > 60 ? '...' : ''}
                </div>
                <div class="gallery-item-model">${image.model_used}</div>
                
                <!-- NOUVEAU : Boutons d'action -->
                <div class="action-buttons" style="display: flex; gap: 5px; margin-top: 8px;">
                    <button class="btn-upscale" 
                            data-image-id="${image.id}"
                            style="flex: 1; padding: 6px 10px; background: #4CAF50; color: white; 
                                border: none; border-radius: 4px; cursor: pointer; 
                                font-size: 12px; font-weight: 600;">
                        🔍 Upscale
                    </button>
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
        
        // Event listener pour ouvrir la modal (sur l'image seulement)
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
        
        // Event listener pour l'étoile favorite
        const star = item.querySelector('.favorite-star');
        star.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleFavorite(image.id, star);
        });
        
        // Event listener pour le bouton upscale
        const btnUpscale = item.querySelector('.btn-upscale');
        btnUpscale.addEventListener('click', (e) => {
            e.stopPropagation();
            const imageId = parseInt(btnUpscale.dataset.imageId);  // <-- Utilisez btnUpscale au lieu de e.target
            //console.log('Upscale button clicked, imageId:', imageId);
            upscaleImage(imageId, btnUpscale);
        });
        
        // Event listener pour le bouton download
        const btnDownload = item.querySelector('.btn-download');
        btnDownload.addEventListener('click', (e) => {
            e.stopPropagation();
            // Créer un lien de téléchargement direct
            const link = document.createElement('a');
            link.href = `data:image/png;base64,${image.image_data}`;
            link.download = `openimage_${image.id}.png`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });
                        
        gallery.appendChild(item);
    });
        // Render pagination (votre code existant)
    const totalPages = Math.ceil(allImages.length / IMAGES_PER_PAGE);
    pagination.innerHTML = `
        <button class="pagination-btn" onclick="changePage(-1)" ${currentPage === 1 ? 'disabled' : ''}>← Previous</button>
        <span class="pagination-info">Page ${currentPage} of ${totalPages}</span>
        <button class="pagination-btn" onclick="changePage(1)" ${currentPage === totalPages ? 'disabled' : ''}>Next →</button>
    `;
}

// Fonction helper pour CSRF token
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

// Toggle Favorite
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
            // Mise à jour visuelle immédiate
            starElement.textContent = data.is_favorite ? '⭐' : '☆';
            starElement.title = data.is_favorite ? 'Remove from favorites' : 'Add to favorites';
            
            // Mettre à jour dans allImages pour persistance
            const imageIndex = allImages.findIndex(img => img.id === imageId);
            if (imageIndex !== -1) {
                allImages[imageIndex].is_favorite = data.is_favorite;
            }
        }
    } catch (error) {
        console.error('Error toggling favorite:', error);
        alert('❌ Error toggling favorite. Please try again.');
    }
}

async function upscaleImage(imageId, btnElement) {
    //console.log('upscaleImage called with imageId:', imageId); 
    
    if (!confirm('⏳ Upscale this image to 2x resolution?\n\nThis will take 10-15 seconds.\n\nNote: Requires Real-ESRGAN to be installed.')) {
        return;
    }

    const originalText = btnElement.textContent;
    btnElement.textContent = '⏳ Processing...';
    btnElement.disabled = true;
    btnElement.style.opacity = '0.6';

    try {
        const payload = { image_id: imageId, scale: 2 };
        //console.log('Sending payload:', payload); 
        
        const response = await fetch('/api/upscale/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(payload)
        });
    
        const data = await response.json();
        //console.log('Response data:', data);
    
        if (data.success) {
            alert(`✅ Upscaling Complete!\n\n` +
                `Original: ${data.original_resolution}\n` +
                `New: ${data.new_resolution}\n` +
                `Processing Time: ${data.processing_time}s\n\n` +
                `The page will reload to show the upscaled image.`);
        
            location.reload();
        } else {
            alert(`❌ Upscaling Failed:\n\n${data.error}\n\n` +
                `Note: If Real-ESRGAN is not installed, upscaling won't work.\n` +
                `Install with: docker-compose exec site pip install realesrgan basicsr torch`);
        
            btnElement.textContent = originalText;
            btnElement.disabled = false;
            btnElement.style.opacity = '1';
        }
    } catch (error) {
        console.error('Error upscaling:', error);
        alert(`❌ Error: ${error.message}`);
    
        btnElement.textContent = originalText;
        btnElement.disabled = false;
        btnElement.style.opacity = '1';
    }
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

// Download Image
function downloadImage(imageId, imageDataUrl) {
    const link = document.createElement('a');
    link.href = imageDataUrl;
    link.download = `openimage_${imageId}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function changePage(direction) {
    currentPage += direction;
    renderGallery();
    document.querySelector('.gallery').scrollIntoView({ behavior: 'smooth' });
}

// Modal functions
let currentModalData = {};

function openModal(imageSrc, data) {
    //console.log('openModal data:', data);  // ← AJOUTEZ CECI
    //console.log('style_preset value:', data.style_preset);  // ← AJOUTEZ CECI
    
    const modal = document.getElementById('imageModal');
    document.getElementById('modalImage').src = imageSrc;
    document.getElementById('modalPrompt').textContent = data.prompt;
    document.getElementById('modalModel').textContent = data.model;
    document.getElementById('modalResolution').textContent = `${data.width} × ${data.height} px`;
    document.getElementById('modalFormat').textContent = data.format;
    
    // Afficher le style preset
    const stylePresetRow = document.getElementById('modalStylePresetRow');
    const stylePresetElement = document.getElementById('modalStylePreset');
    
    //console.log('stylePresetRow:', stylePresetRow);  // ← AJOUTEZ CECI
    //console.log('Has style_preset?', data.style_preset && data.style_preset !== '');  // ← AJOUTEZ CECI
    
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

// Close modal on click outside
document.getElementById('imageModal').addEventListener('click', function(e) {
    if (e.target === this) closeModal();
});

// Keyboard navigation
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeModal();
});

// Initialize
loadModelsConfig().then(() => {
    updateAdvancedOptions(initialProvider);
    renderGallery();
});
