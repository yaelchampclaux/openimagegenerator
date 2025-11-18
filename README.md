# 🎨 OpenImage - Multi-Provider AI Image Generator

Professional Django application for AI image generation with support for 7 providers (3 free, 4 paid).

## ✨ Features

- **7 AI Providers**: Pollinations, Gemini, Hugging Face (3 models), DeepAI, Runware, Replicate, Stability AI
- **Style Presets**: 15+ artistic styles (realistic, anime, oil painting, cyberpunk, etc.)
- **Advanced Options**: Negative prompts, CFG scale, seeds, custom dimensions
- **Image Gallery**: Download, upscale (2x/4x), search, and filter past generations
- **Adaptive UI**: Form fields adapt to selected provider capabilities
- **Docker Ready**: Fully containerized with PostgreSQL

## 🚀 Quick Start

### 1. Clone and Install

```bash
git clone <your-repo>
cd oi_v2

# Using Docker (recommended)
docker-compose up -d

# Or manual installation
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 2. Configure API Keys

Create `.env` file:

```bash
# Free APIs (recommended)
GEMINI_API_KEY=your_key          # Get at: https://aistudio.google.com/app/apikey
HUGGINGFACE_API_KEY=optional     # Optional for HF models

# Paid APIs (optional)
DEEPAI_API_KEY=your_key
RUNWARE_API_KEY=your_key
REPLICATE_API_KEY=your_key
STABILITY_AI_API_KEY=your_key

# Django
SECRET_KEY=your_django_secret
DEBUG=True
DATABASE_URL=postgres://user:pass@db:5432/openimage_db
```

### 3. Initialize Database

```bash
# With Docker
docker-compose exec site python manage.py migrate
docker-compose exec site python manage.py makemigrations
docker-compose exec site python manage.py migrate

# Manual
python manage.py migrate
```

### 4. Run Application

```bash
# Docker
docker-compose up

# Manual
python manage.py runserver
```

Open http://localhost:8000

## 📊 Provider Comparison

| Provider | Free | API Key | Quality | Speed | Limits |
|----------|------|---------|---------|-------|--------|
| **Pollinations** | ✅ | ❌ | ⭐⭐⭐ | ⚡⚡⚡ | Unlimited |
| **Gemini** | ✅ | ✅ | ⭐⭐⭐⭐⭐ | ⚡⚡ | 1500/day |
| **Hugging Face** | ✅ | Optional | ⭐⭐⭐⭐ | ⚡ | Moderate |
| **DeepAI** | ❌ | ✅ | ⭐⭐⭐ | ⚡⚡ | $5/500 imgs |
| **Runware** | ❌ | ✅ | ⭐⭐⭐⭐ | ⚡⚡ | $0.002/img |
| **Replicate** | ❌ | ✅ | ⭐⭐⭐⭐⭐ | ⚡ | $0.003/img |
| **Stability AI** | ❌ | ✅ | ⭐⭐⭐⭐⭐ | ⚡⚡ | $0.01-0.04/img |

## 💡 Usage Tips

### Writing Better Prompts

```
❌ Bad:  "a cat"
✅ Good: "A fluffy orange tabby cat sitting on a windowsill, 
         soft natural lighting, photorealistic, 8k, detailed fur"
```

### Negative Prompts (when supported)

```
"blurry, distorted, low quality, watermark, deformed, ugly"
```

### Style Presets

- **Realistic Photo**: Professional photography
- **Anime/Manga**: Japanese animation style
- **Oil Painting**: Classical art with brush strokes
- **Cyberpunk**: Neon-lit futuristic scenes
- **Fantasy Art**: Epic magical illustrations

## 🔧 Key Features Explained

### Adaptive Form Fields

The UI automatically shows/hides options based on provider capabilities:
- Negative prompt (only for SD models)
- CFG Scale (Stable Diffusion only)
- Seed (SD models only)
- Resolution limits (per provider)
- Aspect ratios (provider-specific)

### Image Gallery

Each gallery item shows:
- Generated image preview
- Prompt and settings used
- Style preset applied
- Generation metadata

**Gallery Actions:**
- 🔍 Click to view full details
- 📥 Download image
- 🔼 Upscale 2x (requires Real-ESRGAN)
- 📋 Copy prompt to generator

### Upscaling

Requires Real-ESRGAN installation:

```bash
# With Docker
docker-compose exec site pip install realesrgan basicsr torch torchvision

# Manual
pip install realesrgan basicsr torch torchvision
```

Note: Upscaling adds 10-15 seconds per image.

## 🏗️ Project Structure

```
oi_v2/
├── you_image_generator/
│   ├── ai_clients.py          # 7 AI provider clients
│   ├── models.py              # GeneratedImage model
│   ├── models_config.py       # Provider capabilities config
│   ├── views.py               # Main generation logic
│   ├── views_advanced.py      # Upscale, search, stats
│   ├── styles.py              # 15+ style presets
│   ├── upscaler.py            # Real-ESRGAN integration
│   └── templates/
│       └── you_image_generator/
│           └── generator.html # Main UI
├── openimage/
│   ├── settings.py            # Django configuration
│   └── urls.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## 🛠️ Technical Details

### Supported Features by Provider

| Feature | Pollinations | Gemini | HF FLUX | HF SDXL | DeepAI | Runware | Replicate | Stability |
|---------|-------------|--------|---------|---------|--------|---------|-----------|-----------|
| Negative Prompt | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| CFG Scale | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Seed | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Style Presets | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Max Resolution | 2048 | 2048 | 1024 | 1024 | 1024 | 2048 | 1024 | 2048 |
| Custom Ratios | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |

### Output Formats

Currently, all providers return **PNG** format images. This is because:
- PNG is lossless and maintains quality
- All AI models natively output PNG
- Better for archival and editing
- Transparency support (when applicable)

### Gemini Special Ratios

Gemini supports two additional HD ratios:
- **HD**: 1920×1080 (landscape)
- **mobileHD**: 1080×1920 (portrait)

## 🐛 Troubleshooting

### "API Key not configured"
Check your `.env` file and restart the server.

### "Model is loading" (Hugging Face)
First-time use takes 30-60 seconds. Wait and retry.

### Download Not Working
Ensure browser allows downloads and check console for errors.

### Upscale Fails
Install Real-ESRGAN dependencies:
```bash
docker-compose exec site pip install realesrgan basicsr torch
```

### Images Low Quality
1. Use more detailed prompts
2. Try different providers (Gemini/Replicate for best quality)
3. Increase resolution
4. Add negative prompts
5. Apply appropriate style presets

## 📈 Cost Estimation

### Monthly Usage Scenarios

**Hobbyist (100 images/month)**
- Free tier: $0 (Pollinations + Gemini)
- Paid: $0.20 (Runware)

**Content Creator (1000 images/month)**
- Free tier: $0 (mixed providers)
- Paid: $2-5 (Runware + occasional Replicate)

**Professional (10,000 images/month)**
- Recommended: Runware ($20) + Gemini free tier
- Premium: Mix of Replicate/Stability ($30-100)

## 🔒 Security Notes

- Never commit `.env` file
- Use strong SECRET_KEY in production
- Set DEBUG=False in production
- Use environment variables for API keys
- Implement rate limiting for production

## 🚀 Deployment

### Production Checklist

1. Set `DEBUG=False`
2. Configure `ALLOWED_HOSTS`
3. Use strong `SECRET_KEY`
4. Set up proper PostgreSQL
5. Configure static files (whitenoise)
6. Set up SSL/HTTPS
7. Implement user authentication
8. Add rate limiting
9. Set up monitoring
10. Configure backups

### Docker Production

```bash
# Build production image
docker-compose -f docker-compose.prod.yml build

# Run with production settings
docker-compose -f docker-compose.prod.yml up -d
```

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 Changelog

### v1.1.0 (Current)
- ✅ Added DeepAI provider
- ✅ Fixed download functionality
- ✅ Fixed upscale with proper image_id
- ✅ Added style_preset to database
- ✅ Adaptive form fields per provider
- ✅ Added HD/mobileHD ratios for Gemini
- ✅ Fixed width/height display in modal
- ✅ Style presets now work correctly
- ✅ All formats confirmed as PNG

### v1.0.0
- Initial release with 6 providers
- Style preset system
- Gallery with search
- Basic upscaling

## 📄 License

MIT License - See LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini team
- Pollinations.ai for free API
- Hugging Face community
- All open-source contributors

---

**⭐ Star this project if you find it useful!**

For issues and feature requests, please use GitHub Issues.