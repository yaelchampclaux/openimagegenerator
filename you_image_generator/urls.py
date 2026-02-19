"""
URL configuration for OpenImage
Includes routes for generation, upscaling, search, styles, and more
"""

from django.urls import path
from . import views
from . import views_advanced

app_name = 'you_image_generator'

urlpatterns = [
    # ============================================
    # Main Views
    # ============================================
    path('', views.image_generator_view, name='generator'),
    
    # ============================================
    # Generation APIs
    # ============================================
    path('generate/', views.generate_image_api, name='generate_api'),
    path('api/model-config/', views.get_model_configuration, name='model_config'),
    path('api/all-configs/', views.get_all_configurations, name='all_configs'),
    
    # ============================================
    # Upscaling APIs
    # ============================================
    path('api/upscale/', views_advanced.upscale_image_view, name='upscale'),
    path('api/batch-upscale/', views_advanced.batch_upscale_view, name='batch_upscale'),
    
    # ============================================
    # Search & Filter APIs
    # ============================================
    path('api/search/', views_advanced.advanced_search_view, name='advanced_search'),
    path('api/search/suggestions/', views_advanced.search_suggestions_view, name='search_suggestions'),
    
    # ============================================
    # Style Preset APIs
    # ============================================
    path('api/styles/', views_advanced.get_style_presets_view, name='get_styles'),
    path('api/styles/apply/', views_advanced.apply_style_view, name='apply_style'),
    path('api/styles/suggest/', views_advanced.suggest_style_view, name='suggest_style'),
    
    # ============================================
    # Favorites & Rating APIs
    # ============================================
    path('api/favorites/toggle/', views_advanced.toggle_favorite_view, name='toggle_favorite'),
    path('api/rate/', views_advanced.rate_image_view, name='rate_image'),
    
    # ============================================
    # Statistics & Export APIs
    # ============================================
    path('api/stats/', views_advanced.get_statistics_view, name='statistics'),
    path('api/export/', views_advanced.export_images_view, name='export_images'),
    
    # ============================================
    # Health Check APIs
    # ============================================
    path('api/health/', views.api_health_check, name='api_health_check'),
    path('api/providers/working/', views.get_working_providers, name='working_providers'),
    path('api/test-free/', views.test_free_apis, name='test_free_apis'),
]