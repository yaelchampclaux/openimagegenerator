# Generated migration for adding tags and categories
# you_image_generator/migrations/0004_add_tags_and_categories.py

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('you_image_generator', '0003_generatedimage_aspect_ratio_generatedimage_cfg_scale_and_more'),
    ]

    operations = [
        # Add tags field (JSON array)
        migrations.AddField(
            model_name='generatedimage',
            name='tags',
            field=models.JSONField(default=list, blank=True),
        ),
        
        # Add category field
        migrations.AddField(
            model_name='generatedimage',
            name='category',
            field=models.CharField(max_length=50, blank=True, default=''),
        ),
        
        # Add is_favorite field
        migrations.AddField(
            model_name='generatedimage',
            name='is_favorite',
            field=models.BooleanField(default=False),
        ),
        
        # Add favorite_date field
        migrations.AddField(
            model_name='generatedimage',
            name='favorite_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        
        # Add rating field
        migrations.AddField(
            model_name='generatedimage',
            name='rating',
            field=models.IntegerField(
                choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
                null=True,
                blank=True
            ),
        ),
        
        # Add style_preset field
        migrations.AddField(
            model_name='generatedimage',
            name='style_preset',
            field=models.CharField(max_length=50, blank=True, default=''),
        ),
        
        # Add is_upscaled field
        migrations.AddField(
            model_name='generatedimage',
            name='is_upscaled',
            field=models.BooleanField(default=False),
        ),
        
        # Add original_image field (for upscaled versions)
        migrations.AddField(
            model_name='generatedimage',
            name='original_image_id',
            field=models.IntegerField(null=True, blank=True),
        ),
        
        # Add index for tags (PostgreSQL GIN index)
        migrations.AddIndex(
            model_name='generatedimage',
            index=models.Index(fields=['tags'], name='you_image_g_tags_idx'),
        ),
        
        # Add index for category
        migrations.AddIndex(
            model_name='generatedimage',
            index=models.Index(fields=['category'], name='you_image_g_category_idx'),
        ),
        
        # Add index for favorites
        migrations.AddIndex(
            model_name='generatedimage',
            index=models.Index(fields=['is_favorite'], name='you_image_g_favorite_idx'),
        ),
        
        # Add index for style_preset
        migrations.AddIndex(
            model_name='generatedimage',
            index=models.Index(fields=['style_preset'], name='you_image_g_style_idx'),
        ),
    ]