# 📘 Guide : Ajouter un nouveau Provider

Ce guide explique comment ajouter un nouveau provider d'IA pour la génération d'images.

## 📋 Prérequis

- Documentation de l'API du provider
- Clé API (si nécessaire)
- Connaître les capacités du provider (formats, résolutions, options)

---

## 🔧 Étapes d'implémentation

### 1. Créer la classe client dans `ai_clients.py`

```python
class MonNouveauClient(BaseImageGenerationModel):
    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self.base_url = "https://api.monprovider.com"
        self.model_name = "Mon Provider"

    def generate_image(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> List[ImageResult]:
        if not self.api_key:
            raise ValueError("API key required for Mon Provider")
            
        if options is None:
            options = {}

        # Préparer la requête
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "prompt": prompt,
            "width": options.get('width', 512),
            "height": options.get('height', 512)
        }
        
        # Ajouter negative prompt si supporté
        if options.get('negative_prompt'):
            payload["negative_prompt"] = options['negative_prompt']

        try:
            # Appel API
            response = requests.post(
                f"{self.base_url}/generate",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                # Récupérer l'image
                image_data = response.content  # ou response.json()['image']
                
                return [ImageResult(
                    image_data=image_data,
                    prompt=prompt,
                    model_used="Mon Provider Model"
                )]
            else:
                raise requests.exceptions.RequestException(f"API Error: {response.text}")
                
        except Exception as e:
            logger.error(f"Error with Mon Provider: {e}")
            raise e
```

### 2. Ajouter au factory `get_api_client()`

Dans la fonction `get_api_client()` :

```python
def get_api_client(provider: str, api_key: str = None):
    clients = {
        # ... providers existants ...
        'monprovider': lambda: MonNouveauClient(api_key) if api_key else None,
    }
    # ... reste du code
```

### 3. Ajouter à `AVAILABLE_PROVIDERS`

```python
AVAILABLE_PROVIDERS = {
    # ... providers existants ...
    'monprovider': {
        'name': 'Mon Provider',
        'description': 'Description courte (prix, qualité)',
        'free': False,  # ou True
        'requires_api_key': True,  # ou False
        'quality': 4  # 1-5
    }
}
```

### 4. Configurer dans `models_config.py`

```python
MODELS_CONFIG = {
    # ... configs existantes ...
    'monprovider': {
        'name': 'Mon Provider',
        'max_resolution': 2048,
        'default_resolution': {'width': 1024, 'height': 1024},
        'aspect_ratios': ['1:1', '16:9', '9:16', '4:3'],
        'formats': ['PNG', 'JPEG'],
        'default_format': 'PNG',
        'supports_negative_prompt': True,
        'supports_cfg_scale': False,
        'supports_seed': True,
        'supports_style_preset': True,
    },
}
```

### 5. Ajouter configuration JavaScript

Dans `static/js/form-handler.js`, ajoutez à `PROVIDER_CONFIGS` :

```javascript
const PROVIDER_CONFIGS = {
    // ... configs existantes ...
    'monprovider': {
        supports_negative_prompt: true,
        supports_cfg_scale: false,
        supports_seed: true,
        supports_style_preset: true
    }
};
```

### 6. Ajouter la clé API dans `.env`

```bash
MONPROVIDER_API_KEY=votre_cle_api
```

### 7. Charger la clé dans `settings.py`

```python
MONPROVIDER_API_KEY = config('MONPROVIDER_API_KEY', default='')
```

### 8. Gérer la clé dans `views.py`

Dans la fonction `generate_image_api()`, ajoutez :

```python
elif provider == 'monprovider':
    api_key = settings.MONPROVIDER_API_KEY
    if not api_key:
        return JsonResponse({'error': 'Mon Provider API Key not configured'}, status=500)
```

---

## ✅ Checklist de validation

Avant de considérer le provider comme fonctionnel :

- [ ] La classe client hérite de `BaseImageGenerationModel`
- [ ] `generate_image()` retourne `List[ImageResult]`
- [ ] Gestion d'erreurs appropriée (try/except)
- [ ] Provider ajouté à `get_api_client()`
- [ ] Provider ajouté à `AVAILABLE_PROVIDERS`
- [ ] Configuration dans `models_config.py`
- [ ] Configuration JavaScript dans `form-handler.js`
- [ ] Clé API dans `.env` et `settings.py`
- [ ] Gestion de la clé dans `views.py`
- [ ] Test manuel de génération d'image
- [ ] Les champs adaptatifs fonctionnent
- [ ] Logs appropriés avec `logger.info()` et `logger.error()`

---

## 🧪 Tester le nouveau provider

```bash
# 1. Redémarrer
docker-compose restart site

# 2. Tester la génération
# Via l'interface web : sélectionner le provider et générer une image

# 3. Vérifier les logs
docker-compose logs site | grep "monprovider"
```

---

## 📝 Exemple complet : Provider fictif "QuickAI"

```python
# Dans ai_clients.py
class QuickAIClient(BaseImageGenerationModel):
    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self.base_url = "https://api.quickai.com/v1"
        self.model_name = "QuickAI"

    def generate_image(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> List[ImageResult]:
        if options is None:
            options = {}
            
        headers = {"X-API-Key": self.api_key}
        payload = {
            "text": prompt,
            "size": f"{options.get('width', 512)}x{options.get('height', 512)}"
        }
        
        response = requests.post(
            f"{self.base_url}/generate",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            image_url = data['image_url']
            
            # Télécharger l'image
            img_response = requests.get(image_url)
            
            return [ImageResult(
                image_data=img_response.content,
                image_url=image_url,
                prompt=prompt,
                model_used="QuickAI-v1"
            )]
        else:
            raise Exception(f"QuickAI Error: {response.text}")
```

---

## ⚠️ Points d'attention

1. **Timeouts** : Ajustez le timeout selon le provider (60-120s)
2. **Rate limits** : Certains providers ont des limites de requêtes
3. **Formats d'image** : Certains retournent des URLs, d'autres du base64
4. **Erreurs** : Capturez les codes d'erreur spécifiques du provider
5. **Logs** : Loguez les erreurs pour faciliter le débogage

---

## 🔗 Ressources

- [Documentation BaseImageGenerationModel](#)
- [Liste des providers supportés](#)
- [Tests unitaires](#)