from django.test import TestCase, Client
from django.urls import reverse
from you_image_generator.models import GeneratedImage
from unittest.mock import patch, Mock
import json


class ViewsTest(TestCase):
    """Tests pour les vues"""
    
    def setUp(self):
        """Setup test client"""
        self.client = Client()
        self.test_image = GeneratedImage.objects.create(
            prompt="Test image",
            image_data=b'fake_data',
            width=512,
            height=512,
            provider="test"
        )
    
    def test_image_generator_view_loads(self):
        """Test page principale charge"""
        response = self.client.get(reverse('you_image_generator:generator'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'OpenImage')
    
    def test_image_generator_view_contains_images(self):
        """Test page contient les images"""
        response = self.client.get(reverse('you_image_generator:generator'))
        self.assertContains(response, 'Test image')
    
    def test_model_configuration_endpoint(self):
        """Test endpoint configuration modèle"""
        response = self.client.get(
            reverse('you_image_generator:model_config'),
            {'provider': 'pollinations'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('max_resolution', data)
    
    def test_all_configurations_endpoint(self):
        """Test endpoint toutes configurations"""
        response = self.client.get(reverse('you_image_generator:all_configs'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('pollinations', data)
    
    @patch('you_image_generator.views.get_api_client')
    def test_generate_image_api_success(self, mock_get_client):
        """Test génération d'image réussie"""
        # Mock du client AI
        mock_client = Mock()
        mock_result = Mock()
        mock_result.prompt = "test"
        mock_result.model_used = "test_model"
        mock_result.image_data = b'fake_image'
        mock_client.generate_image.return_value = [mock_result]
        mock_get_client.return_value = mock_client
        
        response = self.client.post(
            reverse('you_image_generator:generate_api'),
            {
                'prompt': 'a red apple',
                'provider': 'pollinations',
                'width': 512,
                'height': 512,
                'aspect_ratio': '1:1',
                'output_format': 'PNG'
            }
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('image_base64', data)
    
    def test_generate_image_api_missing_prompt(self):
        """Test génération sans prompt"""
        response = self.client.post(
            reverse('you_image_generator:generate_api'),
            {'provider': 'pollinations'}
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)
    
    def test_generate_image_api_invalid_provider(self):
        """Test génération avec provider invalide"""
        response = self.client.post(
            reverse('you_image_generator:generate_api'),
            {
                'prompt': 'test',
                'provider': 'invalid_provider'
            }
        )
        self.assertEqual(response.status_code, 400)


class AdvancedViewsTest(TestCase):
    """Tests pour views_advanced"""
    
    def setUp(self):
        self.client = Client()
        self.image = GeneratedImage.objects.create(
            prompt="Test",
            image_data=b'data',
            width=512,
            height=512,
            tags=[]
        )
    
    def test_upscale_view_missing_image_id(self):
        """Test upscale sans image_id"""
        response = self.client.post(
            '/api/upscale/',
            json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_toggle_favorite(self):
        """Test toggle favorite"""
        response = self.client.post(
            '/api/favorites/toggle/',
            json.dumps({'image_id': self.image.id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)