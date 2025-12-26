# 🤖 Configuration Ollama pour ShadowScan

## ✨ Pourquoi Ollama ?

**Ollama** permet d'exécuter des modèles LLM **localement** et **gratuitement** sur votre machine !

### Avantages :
- ✅ **100% Gratuit** - Aucun abonnement API requis
- ✅ **Privé** - Vos données ne quittent jamais votre machine
- ✅ **Rapide** - Pas de latence réseau
- ✅ **Hors-ligne** - Fonctionne sans internet (après téléchargement)
- ✅ **Open Source** - Modèles transparents et vérifiables

### Modèles Utilisés :
- **Llama 3.1 8B** → Analyse de code (~4.7GB)
- **LLaVA 13B** → Analyse de diagrammes (~7.4GB)
- **Codellama 13B** → Alternative pour le code (~7.4GB)

---

## 📦 Installation Rapide

### Option 1 : Docker (Recommandé)

**Tout est déjà configuré !** Les modèles seront téléchargés automatiquement.

```bash
# Démarrer ShadowScan avec Ollama
docker-compose up -d

# Initialiser Ollama et télécharger les modèles
docker-compose exec ollama sh -c "
  ollama pull llama3.1:8b &&
  ollama pull llava:13b
"

# Vérifier que les modèles sont prêts
docker-compose exec ollama ollama list
```

**Temps estimé :** 15-30 minutes (selon votre connexion)

---

### Option 2 : Installation Locale (Sans Docker)

#### 1. Installer Ollama

**Linux :**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**macOS :**
```bash
brew install ollama
```

**Windows :**
Téléchargez depuis [ollama.com/download](https://ollama.com/download)

#### 2. Démarrer Ollama

```bash
ollama serve
```

#### 3. Télécharger les Modèles

```bash
# Modèle pour l'analyse de code
ollama pull llama3.1:8b

# Modèle pour les diagrammes
ollama pull llava:13b

# (Optionnel) Modèle alternatif pour le code
ollama pull codellama:13b
```

#### 4. Configurer ShadowScan

Mettez à jour votre `.env` :

```bash
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL_CODE=llama3.1:8b
OLLAMA_MODEL_VISION=llava:13b
```

---

## ⚙️ Configuration Avancée

### Changer de Modèle

Vous pouvez utiliser d'autres modèles Ollama :

```bash
# Modèles disponibles sur ollama.com/library

# Petits modèles (rapides, moins précis)
OLLAMA_MODEL_CODE=llama3.1:8b
OLLAMA_MODEL_CODE=codellama:7b
OLLAMA_MODEL_CODE=mistral:7b

# Grands modèles (lents, très précis)
OLLAMA_MODEL_CODE=llama3.1:70b
OLLAMA_MODEL_CODE=codellama:34b
OLLAMA_MODEL_CODE=mixtral:8x7b

# Vision models
OLLAMA_MODEL_VISION=llava:13b
OLLAMA_MODEL_VISION=llava:34b
OLLAMA_MODEL_VISION=bakllava
```

### Support GPU

Pour utiliser votre GPU NVIDIA et accélérer l'analyse :

1. **Installez NVIDIA Container Toolkit :**
```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

2. **Le docker-compose.yml est déjà configuré !**

Le service Ollama détectera automatiquement votre GPU.

### Optimisation Mémoire

Les modèles nécessitent de la RAM :

| Modèle | RAM CPU | VRAM GPU |
|--------|---------|----------|
| llama3.1:8b | 8 GB | 6 GB |
| llava:13b | 16 GB | 10 GB |
| codellama:13b | 16 GB | 10 GB |
| mixtral:8x7b | 48 GB | 40 GB |

**Astuce :** Si vous avez peu de RAM, utilisez des modèles plus petits :

```bash
OLLAMA_MODEL_CODE=llama3.1:8b  # Au lieu de 70b
OLLAMA_MODEL_VISION=llava:7b   # Au lieu de 13b
```

---

## 🧪 Tester Ollama

### Test Manuel

```bash
# Tester le modèle de code
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.1:8b",
  "prompt": "Analyze this Python code for SQL injection: cursor.execute(\"SELECT * FROM users WHERE id = \" + user_id)"
}'

# Tester le modèle vision
curl http://localhost:11434/api/generate -d '{
  "model": "llava:13b",
  "prompt": "Describe the security issues in this architecture diagram",
  "images": ["base64_encoded_image_here"]
}'
```

### Test via ShadowScan

1. Démarrez ShadowScan : `docker-compose up -d`
2. Allez sur http://localhost:3000
3. Analysez du code ou un diagramme
4. Vérifiez les logs : `docker-compose logs backend`

---

## 🚀 Performance

### Temps d'Analyse Typiques (CPU)

| Tâche | Modèle | Temps |
|-------|--------|-------|
| Code court (< 100 lignes) | llama3.1:8b | 10-30s |
| Code moyen (100-500 lignes) | llama3.1:8b | 30-60s |
| Code long (> 500 lignes) | llama3.1:8b | 1-3min |
| Diagramme simple | llava:13b | 20-40s |
| Diagramme complexe | llava:13b | 40-90s |

### Avec GPU (NVIDIA RTX 3080)

| Tâche | Modèle | Temps |
|-------|--------|-------|
| Code court | llama3.1:8b | 2-5s |
| Code moyen | llama3.1:8b | 5-15s |
| Code long | llama3.1:8b | 15-40s |
| Diagramme | llava:13b | 5-15s |

---

## 🔧 Dépannage

### Problème : Ollama ne démarre pas

```bash
# Vérifier les logs
docker-compose logs ollama

# Redémarrer Ollama
docker-compose restart ollama
```

### Problème : Modèles non trouvés

```bash
# Lister les modèles téléchargés
docker-compose exec ollama ollama list

# Re-télécharger un modèle
docker-compose exec ollama ollama pull llama3.1:8b
```

### Problème : Erreur de mémoire

```bash
# Utiliser un modèle plus petit
OLLAMA_MODEL_CODE=llama3.1:8b  # Au lieu de 70b

# Ou augmenter la RAM Docker
# Dans Docker Desktop → Settings → Resources → Memory
```

### Problème : Analyse trop lente

```bash
# Option 1: Utiliser un modèle plus petit
OLLAMA_MODEL_CODE=llama3.1:8b  # Au lieu de 13b/70b

# Option 2: Activer le GPU (voir section Support GPU)

# Option 3: Augmenter les ressources CPU
# Dans docker-compose.yml, pour le service ollama:
deploy:
  resources:
    limits:
      cpus: '8'  # Augmentez selon vos cores disponibles
```

---

## 📊 Comparaison : Ollama vs APIs Payantes

| Critère | Ollama | Claude/GPT |
|---------|--------|------------|
| **Coût** | 0€ | ~$0.01-0.10 par analyse |
| **Vitesse (CPU)** | 30s | 5s |
| **Vitesse (GPU)** | 5s | 5s |
| **Confidentialité** | ✅ 100% local | ❌ Données envoyées |
| **Hors-ligne** | ✅ Oui | ❌ Non |
| **Qualité** | 85-90% | 95-98% |
| **Setup** | 15 min | 2 min |

**Verdict :** Ollama est parfait pour :
- ✅ Usage personnel/apprentissage
- ✅ Données sensibles
- ✅ Pas de budget API
- ✅ Utilisation intensive

APIs payantes sont mieux pour :
- ✅ Maximum de précision
- ✅ Setup rapide
- ✅ Pas de hardware puissant

---

## 🆘 Support

Des questions sur Ollama ?

- 📖 [Documentation Ollama](https://github.com/ollama/ollama)
- 💬 [Discord Ollama](https://discord.gg/ollama)
- 🐛 [Issues ShadowScan](https://github.com/K3E9X/ShadowScan/issues)

---

**🎉 Ollama est maintenant configuré ! Profitez de l'IA gratuite et locale !**
