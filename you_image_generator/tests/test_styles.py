from django.test import TestCase
from you_image_generator.styles import (
    get_style_preset,
    apply_style_to_prompt,
    get_all_style_presets,
    suggest_style_for_prompt,
    STYLE_PRESETS
)


class StylePresetsTest(TestCase):
    """Tests pour les style presets"""
    
    def test_style_presets_exists(self):
        """Test que STYLE_PRESETS est défini"""
        self.assertIsNotNone(STYLE_PRESETS)
        self.assertGreater(len(STYLE_PRESETS), 0)
    
    def test_get_style_preset_valid(self):
        """Test récupération preset valide"""
        preset = get_style_preset('realistic')
        self.assertIsNotNone(preset)
        self.assertEqual(preset.key, 'realistic')
    
    def test_get_style_preset_invalid(self):
        """Test récupération preset invalide"""
        preset = get_style_preset('nonexistent')
        self.assertIsNone(preset)
    
    def test_get_all_style_presets(self):
        """Test récupération tous les presets"""
        presets = get_all_style_presets()
        self.assertIsInstance(presets, dict)
        self.assertIn('realistic', presets)
        self.assertIn('anime', presets)
    
    def test_apply_style_to_prompt(self):
        """Test application style au prompt"""
        result = apply_style_to_prompt("a red apple", "realistic")
        
        self.assertIn('prompt', result)
        self.assertIn('a red apple', result['prompt'])
        self.assertIn('photorealistic', result['prompt'].lower())
    
    def test_apply_style_includes_negative(self):
        """Test inclusion negative prompt"""
        result = apply_style_to_prompt("a cat", "realistic", include_negative=True)
        
        self.assertIn('negative_prompt', result)
        self.assertIsNotNone(result['negative_prompt'])
    
    def test_apply_style_without_negative(self):
        """Test sans negative prompt"""
        result = apply_style_to_prompt("a cat", "realistic", include_negative=False)
        
        self.assertNotIn('negative_prompt', result)
    
    def test_suggest_style_realistic(self):
        """Test suggestion style réaliste"""
        style = suggest_style_for_prompt("portrait of a person")
        self.assertEqual(style, 'realistic')
    
    def test_suggest_style_fantasy(self):
        """Test suggestion style fantasy"""
        style = suggest_style_for_prompt("magic dragon wizard")
        self.assertEqual(style, 'fantasy')
    
    def test_suggest_style_anime(self):
        """Test suggestion style anime"""
        style = suggest_style_for_prompt("anime girl character")
        self.assertEqual(style, 'anime')
    
    def test_suggest_style_no_match(self):
        """Test suggestion sans correspondance"""
        style = suggest_style_for_prompt("random words test")
        self.assertIsNone(style)
    
    def test_all_presets_have_required_fields(self):
        """Test que tous les presets ont les champs requis"""
        for key, preset in STYLE_PRESETS.items():
            self.assertEqual(preset.key, key)
            self.assertIsNotNone(preset.name)
            self.assertIsNotNone(preset.description)
            self.assertIsNotNone(preset.suffix)
            self.assertGreater(preset.quality_rating, 0)
            self.assertLessEqual(preset.quality_rating, 5)