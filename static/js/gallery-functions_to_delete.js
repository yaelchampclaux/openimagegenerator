// Fix download - gère le format correctement
function downloadImage(imageId) {
    const imageData = window.generatedImages.find(img => img.id === imageId);
    if (!imageData) {
        alert('Image not found');
        return;
    }
    
    const format = imageData.output_format || 'PNG';
    const extension = format.toLowerCase();
    const filename = `image_${imageId}.${extension}`;
    
    const byteCharacters = atob(imageData.image_data);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], { type: `image/${extension}` });
    
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
}

// Fix upscale - envoie l'image_id correctement
async function upscaleImage(imageId) {
    if (!confirm('Upscale this image to 2x resolution? This will take 10-15 seconds.')) {
        return;
    }
    
    try {
        const response = await fetch('/api/upscale/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                image_id: imageId,
                scale: 2
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            alert('Image upscaled successfully!');
            window.location.reload();
        } else {
            alert('Upscaling failed: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        alert('Upscaling failed: ' + error.message);
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