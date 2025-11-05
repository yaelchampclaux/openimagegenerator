# you_image_generator/upscaler.py
"""
AI Image Upscaling using Real-ESRGAN
Enhances image resolution while preserving and improving quality
"""

import logging
from typing import Optional
from io import BytesIO
from PIL import Image
import numpy as np

logger = logging.getLogger(__name__)

try:
    from basicsr.archs.rrdbnet_arch import RRDBNet
    from realesrgan import RealESRGANer
    REALESRGAN_AVAILABLE = True
except ImportError as e:
    REALESRGAN_AVAILABLE = False
    logger.warning(
        "Real-ESRGAN not installed. Install with: "
        "pip install realesrgan basicsr"
    )
    logger.warning(f"Real-ESRGAN import failed: {e}")


class ImageUpscaler:
    """
    AI-powered image upscaling using Real-ESRGAN
    
    Supports 2x and 4x upscaling with high quality results.
    """
    
    def __init__(self, model_name='RealESRGAN_x4plus', device='cpu'):
        """
        Initialize the upscaler
        
        Args:
            model_name: Model to use ('RealESRGAN_x4plus', 'RealESRGAN_x2plus')
            device: 'cpu' or 'cuda' for GPU acceleration
        """
        if not REALESRGAN_AVAILABLE:
            raise ImportError(
                "Real-ESRGAN is not installed. "
                "Install with: pip install realesrgan basicsr"
            )
        
        self.model_name = model_name
        self.device = device
        self.upsampler = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Load the Real-ESRGAN model"""
        try:
            import os
            import urllib.request
            
            # Déterminer le scale
            if 'x4' in self.model_name.lower():
                scale = 4
            elif 'x2' in self.model_name.lower():
                scale = 2
            else:
                scale = 4
            
            # Créer le dossier weights s'il n'existe pas
            weights_dir = 'weights'
            os.makedirs(weights_dir, exist_ok=True)
            
            # Chemin du modèle
            model_path = f'{weights_dir}/RealESRGAN_x4plus.pth'
            
            # Télécharger le modèle s'il n'existe pas
            if not os.path.exists(model_path):
                logger.info("Downloading RealESRGAN model...")
                url = 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth'
                urllib.request.urlretrieve(url, model_path)
                logger.info("Model downloaded successfully")
            
            # Créer le modèle
            model = RRDBNet(
                num_in_ch=3,
                num_out_ch=3,
                num_feat=64,
                num_block=23,
                num_grow_ch=32,
                scale=scale
            )
            
            # Initialiser l'upsampler
            self.upsampler = RealESRGANer(
                scale=scale,
                model_path=model_path,
                model=model,
                tile=400,
                tile_pad=10,
                pre_pad=0,
                half=False,
                device=self.device
            )
            
            logger.info(f"Real-ESRGAN model loaded: {self.model_name}")
            
        except Exception as e:
            logger.error(f"Failed to load Real-ESRGAN model: {e}")
            raise
    
    def upscale(
        self, 
        image_data: bytes, 
        scale: int = 2,
        output_format: str = 'PNG'
    ) -> bytes:
        """
        Upscale an image
        
        Args:
            image_data: Input image as bytes
            scale: Upscaling factor (2 or 4)
            output_format: Output format ('PNG', 'JPEG', 'WEBP')
        
        Returns:
            Upscaled image as bytes
        """
        if not self.upsampler:
            raise RuntimeError("Upscaler not initialized")
        
        try:
            # Load image from bytes
            img = Image.open(BytesIO(image_data))
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Convert to numpy array
            img_array = np.array(img)
            
            # Upscale
            logger.info(f"Upscaling image from {img.size} by {scale}x...")
            output, _ = self.upsampler.enhance(img_array, outscale=scale)
            
            # Convert back to PIL Image
            output_img = Image.fromarray(output)
            
            # Save to bytes
            output_buffer = BytesIO()
            output_img.save(
                output_buffer, 
                format=output_format,
                quality=95 if output_format == 'JPEG' else None
            )
            
            logger.info(
                f"Upscaling complete: {img.size} → {output_img.size}"
            )
            
            return output_buffer.getvalue()
            
        except Exception as e:
            logger.error(f"Upscaling failed: {e}")
            raise


# Global upscaler instance
_upscaler = None


def get_upscaler(device='cpu'):
    """
    Get or create global upscaler instance
    
    Args:
        device: 'cpu' or 'cuda'
    
    Returns:
        ImageUpscaler instance
    """
    global _upscaler
    
    if _upscaler is None:
        _upscaler = ImageUpscaler(device=device)
    
    return _upscaler


def upscale_image(
    image_data: bytes,
    scale: int = 2,
    output_format: str = 'PNG'
) -> bytes:
    """
    Convenience function to upscale an image
    
    Args:
        image_data: Input image as bytes
        scale: Upscaling factor (2 or 4)
        output_format: Output format ('PNG', 'JPEG', 'WEBP')
    
    Returns:
        Upscaled image as bytes
    
    Example:
        >>> from you_image_generator.models import GeneratedImage
        >>> img = GeneratedImage.objects.first()
        >>> upscaled = upscale_image(img.image_data, scale=2)
        >>> # Save upscaled version
        >>> new_img = GeneratedImage.objects.create(
        ...     prompt=f"{img.prompt} [Upscaled 2x]",
        ...     image_data=upscaled,
        ...     width=img.width * 2,
        ...     height=img.height * 2
        ... )
    """
    if not REALESRGAN_AVAILABLE:
        raise ImportError(
            "Real-ESRGAN is not installed. "
            "Install with: pip install realesrgan basicsr"
        )
    
    upscaler = get_upscaler()
    return upscaler.upscale(image_data, scale, output_format)


def batch_upscale(
    image_ids: list,
    scale: int = 2,
    save_to_db: bool = True
) -> list:
    """
    Batch upscale multiple images
    
    Args:
        image_ids: List of GeneratedImage IDs
        scale: Upscaling factor (2 or 4)
        save_to_db: Whether to save upscaled images to database
    
    Returns:
        List of upscaled GeneratedImage objects (if save_to_db=True)
        or list of upscaled image bytes (if save_to_db=False)
    """
    from .models import GeneratedImage
    
    results = []
    upscaler = get_upscaler()
    
    for img_id in image_ids:
        try:
            img = GeneratedImage.objects.get(id=img_id)
            
            logger.info(f"Upscaling image {img_id}...")
            upscaled_data = upscaler.upscale(
                img.image_data,
                scale=scale,
                output_format=img.output_format
            )
            
            if save_to_db:
                # Create new database entry
                new_img = GeneratedImage.objects.create(
                    prompt=f"{img.prompt} [Upscaled {scale}x]",
                    negative_prompt=img.negative_prompt,
                    model_used=f"{img.model_used} + Real-ESRGAN",
                    provider=img.provider,
                    image_data=upscaled_data,
                    width=img.width * scale,
                    height=img.height * scale,
                    aspect_ratio=img.aspect_ratio,
                    output_format=img.output_format,
                    seed=img.seed,
                    cfg_scale=img.cfg_scale,
                    tags=img.tags + ['upscaled']
                )
                results.append(new_img)
                logger.info(f"Saved upscaled image as ID {new_img.id}")
            else:
                results.append(upscaled_data)
                
        except Exception as e:
            logger.error(f"Failed to upscale image {img_id}: {e}")
            results.append(None)
    
    return results


def estimate_upscale_time(width: int, height: int, scale: int = 2) -> float:
    """
    Estimate upscaling time in seconds
    
    Args:
        width: Original image width
        height: Original image height
        scale: Upscaling factor
    
    Returns:
        Estimated time in seconds
    """
    # Rough estimates based on testing
    # These will vary based on hardware
    pixels = width * height
    output_pixels = pixels * (scale ** 2)
    
    # Base time + pixel processing time
    base_time = 2.0  # Model loading overhead
    pixel_time = output_pixels / 1000000  # ~1 second per megapixel
    
    return base_time + pixel_time


# Alternative: Simple PIL-based upscaling (fallback)
def simple_upscale(
    image_data: bytes,
    scale: int = 2,
    output_format: str = 'PNG',
    resample=Image.LANCZOS
) -> bytes:
    """
    Simple upscaling using PIL (no AI)
    
    Use this as a fallback when Real-ESRGAN is not available.
    Quality is lower but much faster.
    
    Args:
        image_data: Input image as bytes
        scale: Upscaling factor
        output_format: Output format
        resample: PIL resampling filter
    
    Returns:
        Upscaled image as bytes
    """
    img = Image.open(BytesIO(image_data))
    
    new_size = (img.width * scale, img.height * scale)
    upscaled = img.resize(new_size, resample=resample)
    
    output_buffer = BytesIO()
    upscaled.save(
        output_buffer,
        format=output_format,
        quality=95 if output_format == 'JPEG' else None
    )
    
    return output_buffer.getvalue()


# Django management command helper
def upscale_all_low_res_images(min_width: int = 512, scale: int = 2):
    """
    Upscale all images below a certain resolution
    
    Useful for bulk upgrading your image library.
    
    Args:
        min_width: Minimum width to trigger upscaling
        scale: Upscaling factor
    
    Example:
        >>> # In Django management command
        >>> upscale_all_low_res_images(min_width=1024, scale=2)
    """
    from .models import GeneratedImage
    
    low_res = GeneratedImage.objects.filter(width__lt=min_width)
    total = low_res.count()
    
    logger.info(f"Found {total} images to upscale")
    
    for i, img in enumerate(low_res, 1):
        try:
            logger.info(f"Processing {i}/{total}: Image {img.id}")
            upscaled = upscale_image(img.image_data, scale=scale)
            
            # Create new upscaled version
            GeneratedImage.objects.create(
                prompt=f"{img.prompt} [Upscaled {scale}x]",
                negative_prompt=img.negative_prompt,
                model_used=f"{img.model_used} + Real-ESRGAN",
                provider=img.provider,
                image_data=upscaled,
                width=img.width * scale,
                height=img.height * scale,
                aspect_ratio=img.aspect_ratio,
                output_format=img.output_format,
                tags=img.tags + ['upscaled', 'batch_upscaled']
            )
            
        except Exception as e:
            logger.error(f"Failed to upscale image {img.id}: {e}")
            continue
    
    logger.info("Batch upscaling complete!")


# Performance monitoring
class UpscaleMetrics:
    """Track upscaling performance metrics"""
    
    def __init__(self):
        self.total_upscales = 0
        self.total_time = 0
        self.failures = 0
    
    def record_upscale(self, time_taken: float, success: bool = True):
        """Record an upscaling operation"""
        self.total_upscales += 1
        self.total_time += time_taken
        if not success:
            self.failures += 1
    
    def get_average_time(self) -> float:
        """Get average upscaling time"""
        if self.total_upscales == 0:
            return 0
        return self.total_time / self.total_upscales
    
    def get_success_rate(self) -> float:
        """Get success rate as percentage"""
        if self.total_upscales == 0:
            return 0
        return ((self.total_upscales - self.failures) / self.total_upscales) * 100


# Global metrics instance
_metrics = UpscaleMetrics()


def get_upscale_metrics():
    """Get current upscaling metrics"""
    return _metrics


# API view helper
def upscale_image_api(image_id: int, scale: int = 2) -> dict:
    """
    API helper to upscale an image and return metadata
    
    Args:
        image_id: ID of image to upscale
        scale: Upscaling factor
    
    Returns:
        Dictionary with upscaled image info
    """
    from .models import GeneratedImage
    import time
    
    start_time = time.time()
    
    try:
        # Get original image
        original = GeneratedImage.objects.get(id=image_id)
        
        # Upscale
        upscaled_data = upscale_image(
            original.image_data,
            scale=scale,
            output_format=original.output_format
        )
        
        # Save to database
        upscaled = GeneratedImage.objects.create(
            prompt=f"{original.prompt} [Upscaled {scale}x]",
            negative_prompt=original.negative_prompt,
            model_used=f"{original.model_used} + Real-ESRGAN",
            provider=original.provider,
            image_data=upscaled_data,
            width=original.width * scale,
            height=original.height * scale,
            aspect_ratio=original.aspect_ratio,
            output_format=original.output_format,
            seed=original.seed,
            cfg_scale=original.cfg_scale,
            tags=original.tags + ['upscaled']
        )
        
        elapsed_time = time.time() - start_time
        _metrics.record_upscale(elapsed_time, success=True)
        
        return {
            'success': True,
            'original_id': image_id,
            'upscaled_id': upscaled.id,
            'original_resolution': f"{original.width}x{original.height}",
            'new_resolution': f"{upscaled.width}x{upscaled.height}",
            'scale': scale,
            'processing_time': round(elapsed_time, 2),
            'model': 'Real-ESRGAN',
        }
        
    except Exception as e:
        elapsed_time = time.time() - start_time
        _metrics.record_upscale(elapsed_time, success=False)
        
        return {
            'success': False,
            'error': str(e),
            'processing_time': round(elapsed_time, 2),
        }