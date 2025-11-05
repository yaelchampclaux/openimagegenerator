from django.db import models

class GeneratedImage(models.Model):
    """
    Model to store information about generated images with full metadata.
    """
    # Texte et modèle
    prompt = models.TextField()
    negative_prompt = models.TextField(blank=True, null=True)
    model_used = models.CharField(max_length=100, blank=True, null=True)
    provider = models.CharField(max_length=50, blank=True, null=True)
    tags = models.JSONField(default=list, blank=True)
    
    # Image data
    image_url = models.URLField(blank=True, null=True)
    image_data = models.BinaryField(blank=True, null=True)
    
    # Métadonnées de génération
    width = models.IntegerField(default=1024)
    height = models.IntegerField(default=1024)
    aspect_ratio = models.CharField(max_length=10, default='1:1')
    output_format = models.CharField(max_length=10, default='PNG')
    
    # Style preset
    style_preset = models.CharField(max_length=50, blank=True, null=True)
    
    # Paramètres avancés
    seed = models.BigIntegerField(blank=True, null=True)
    cfg_scale = models.FloatField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Generated Image"
        verbose_name_plural = "Generated Images"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['provider']),
        ]

    def __str__(self):
        prompt_preview = self.prompt[:50] + '...' if len(self.prompt) > 50 else self.prompt
        model_name = self.model_used if self.model_used else "Unknown Model"
        return f"'{prompt_preview}' ({model_name}) - {self.width}x{self.height}"
    
    @property
    def resolution(self):
        """Retourne la résolution formatée"""
        return f"{self.width}x{self.height}"