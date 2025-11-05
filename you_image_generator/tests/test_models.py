from django.test import TestCase
from you_image_generator.models import GeneratedImage
from django.utils import timezone
import base64


class GeneratedImageModelTest(TestCase):
    """Tests pour le modèle GeneratedImage"""
    
    def setUp(self):
        """Créer des données de test"""
        self.test_image_data = b'fake_image_data'
        self.image = GeneratedImage.objects.create(
            prompt="A test image",
            negative_prompt="blurry",
            model_used="Test Model",
            provider="test_provider",
            image_data=self.test_image_data,
            width=1024,
            height=1024,
            aspect_ratio="1:1",
            output_format="PNG",
            style_preset="realistic",
            seed=12345,
            cfg_scale=7.5,
            tags=["test", "sample"]
        )
    
    def test_image_creation(self):
        """Test création d'image"""
        self.assertEqual(self.image.prompt, "A test image")
        self.assertEqual(self.image.width, 1024)
        self.assertEqual(self.image.height, 1024)
        self.assertEqual(self.image.provider, "test_provider")
    
    def test_image_str_representation(self):
        """Test représentation string"""
        str_repr = str(self.image)
        self.assertIn("A test image", str_repr)
        self.assertIn("Test Model", str_repr)
    
    def test_resolution_property(self):
        """Test propriété resolution"""
        self.assertEqual(self.image.resolution, "1024x1024")
    
    def test_optional_fields_null(self):
        """Test champs optionnels à null"""
        minimal_image = GeneratedImage.objects.create(
            prompt="Minimal test",
            image_data=b'data',
            width=512,
            height=512
        )
        self.assertIsNone(minimal_image.negative_prompt)
        self.assertIsNone(minimal_image.style_preset)
        self.assertIsNone(minimal_image.seed)
    
    def test_timestamps(self):
        """Test timestamps auto"""
        self.assertIsNotNone(self.image.created_at)
        self.assertIsNotNone(self.image.updated_at)
        self.assertLessEqual(self.image.created_at, timezone.now())
    
    def test_tags_field(self):
        """Test champ tags JSON"""
        self.assertEqual(self.image.tags, ["test", "sample"])
        self.image.tags.append("new_tag")
        self.image.save()
        self.assertEqual(len(self.image.tags), 3)
    
    def test_image_ordering(self):
        """Test ordre par défaut (créé récemment en premier)"""
        older_image = GeneratedImage.objects.create(
            prompt="Older",
            image_data=b'data',
            width=512,
            height=512
        )
        newer_image = GeneratedImage.objects.create(
            prompt="Newer",
            image_data=b'data',
            width=512,
            height=512
        )
        
        images = GeneratedImage.objects.all()
        self.assertEqual(images[0].id, newer_image.id)
        self.assertEqual(images[1].id, older_image.id)