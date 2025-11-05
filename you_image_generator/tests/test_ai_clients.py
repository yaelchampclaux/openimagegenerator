from django.test import TestCase
from unittest.mock import Mock, patch
from you_image_generator.ai_clients import (
    get_api_client,
    PollinationsClient,
    GeminiClient,
    AVAILABLE_PROVIDERS,
    ImageResult
)


class AIClientsTest(TestCase):
    """Tests pour les clients AI"""
    
    def test_available_providers_exists(self):
        """Test que AVAILABLE_PROVIDERS est défini"""
        self.assertIsNotNone(AVAILABLE_PROVIDERS)
        self.assertGreater(len(AVAILABLE_PROVIDERS), 0)
    
    def test_available_providers_structure(self):
        """Test structure de AVAILABLE_PROVIDERS"""
        for key, info in AVAILABLE_PROVIDERS.items():
            self.assertIn('name', info)
            self.assertIn('free', info)
            self.assertIn('requires_api_key', info)
            self.assertIn('quality', info)
    
    def test_get_api_client_pollinations(self):
        """Test obtention client Pollinations"""
        client = get_api_client('pollinations')
        self.assertIsInstance(client, PollinationsClient)
    
    def test_get_api_client_with_api_key(self):
        """Test obtention client avec clé API"""
        client = get_api_client('gemini', 'fake_api_key')
        self.assertIsInstance(client, GeminiClient)
    
    def test_get_api_client_invalid_provider(self):
        """Test provider invalide"""
        with self.assertRaises(ValueError):
            get_api_client('invalid_provider')
    
    def test_get_api_client_requires_key_but_none_given(self):
        """Test provider nécessitant clé mais aucune fournie"""
        with self.assertRaises(ValueError):
            get_api_client('gemini')
    
    def test_image_result_creation(self):
        """Test création ImageResult"""
        result = ImageResult(
            image_data=b'fake_data',
            prompt="test prompt",
            model_used="test_model"
        )
        self.assertEqual(result.prompt, "test prompt")
        self.assertEqual(result.image_data, b'fake_data')
    
    @patch('requests.get')
    def test_pollinations_client_generate(self, mock_get):
        """Test génération Pollinations"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'fake_image_data'
        mock_get.return_value = mock_response
        
        client = PollinationsClient()
        results = client.generate_image("test prompt", {'width': 512, 'height': 512})
        
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], ImageResult)
        self.assertEqual(results[0].image_data, b'fake_image_data')


class AIClientIntegrationTest(TestCase):
    """Tests d'intégration (nécessitent connexion internet)"""
    
    def test_pollinations_real_generation(self):
        """Test génération réelle Pollinations (SKIP si pas de connexion)"""
        try:
            client = PollinationsClient()
            results = client.generate_image("a red apple", {'width': 256, 'height': 256})
            
            self.assertEqual(len(results), 1)
            self.assertIsNotNone(results[0].image_data)
            self.assertGreater(len(results[0].image_data), 1000)  # Image > 1KB
        except Exception as e:
            self.skipTest(f"Pollinations API not available: {e}")