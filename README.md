# ShadowScan - AI-Powered Security Analysis Platform

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![100% Free AI](https://img.shields.io/badge/AI-100%25%20Free%20(Ollama)-brightgreen.svg)](docs/OLLAMA_SETUP.md)
[![Security Rating](https://img.shields.io/badge/security-A+-green.svg)](https://shadowscan.dev)

> 🎉 **100% GRATUIT** avec Ollama - Aucune API payante requise !
> 🌐 **[LIVE DEMO](https://shadowscan.vercel.app)** | 🤖 **[Guide Ollama](docs/OLLAMA_SETUP.md)** | 🚀 **[Déploiement Cloud](DEPLOY.md)**

**ShadowScan** est une plateforme d'analyse de sécurité alimentée par l'IA qui utilise **Ollama** (gratuit et local) pour analyser votre code et vos diagrammes d'architecture sans aucun coût !

---

## ✨ Pourquoi ShadowScan ?

- ✅ **100% Gratuit** - Utilise Ollama (modèles AI locaux)
- ✅ **Privé** - Vos données ne quittent jamais votre machine
- ✅ **Multi-langages** - Python, JS, TS, Java, Go, Rust, C/C++, PHP, Ruby...
- ✅ **Analyse Complète** - OWASP Top 10 2025, CWE Top 25, secrets, dépendances
- ✅ **Architecture** - Analyse de diagrammes avec recommandations Zero Trust
- ✅ **Conformité** - ISO 27001:2022, NIS2, CIS Benchmarks

---

## 🚀 Démarrage Rapide (5 minutes)

### Prérequis

- **Docker** et **Docker Compose** installés
- **8GB RAM minimum** (16GB recommandé)
- **20GB d'espace disque** pour les modèles AI

### Étape 1️⃣ : Cloner le Projet

```bash
git clone https://github.com/K3E9X/ShadowScan.git
cd ShadowScan
```

### Étape 2️⃣ : Démarrer les Services

```bash
# Démarrer tous les services (Ollama, Backend, Frontend, DB)
docker-compose up -d

# Voir les logs
docker-compose logs -f
```

⏳ **Attendez ~2 minutes** que tous les services démarrent.

### Étape 3️⃣ : Télécharger les Modèles AI (IMPORTANT)

```bash
# Modèle pour l'analyse de code (~4.7GB)
docker-compose exec ollama ollama pull llama3.1:8b

# Modèle pour l'analyse de diagrammes (~7.4GB)
docker-compose exec ollama ollama pull llava:13b
```

⏳ **Temps de téléchargement :** 10-20 minutes (selon votre connexion)

💡 **Astuce :** Ces modèles ne se téléchargent qu'une seule fois !

### Étape 4️⃣ : Vérifier que Tout Fonctionne

```bash
# Lister les modèles téléchargés
docker-compose exec ollama ollama list

# Vérifier les services
docker-compose ps
```

Vous devriez voir tous les services **"Up"** :
```
✅ shadowscan-ollama    (port 11434)
✅ shadowscan-backend   (port 8000)
✅ shadowscan-frontend  (port 3000)
✅ shadowscan-postgres  (port 5432)
✅ shadowscan-redis     (port 6379)
```

### Étape 5️⃣ : Ouvrir ShadowScan

🌐 **Frontend** : http://localhost:3000
📚 **API Docs** : http://localhost:8000/api/docs
💚 **Health Check** : http://localhost:8000/health

---

## 🧪 Tester ShadowScan

### Test 1 : Analyse de Code

1. Allez sur **http://localhost:3000**
2. Cliquez sur **"Start Analysis"**
3. Sélectionnez **"Code Analysis"**
4. Collez ce code vulnérable :

```python
import sqlite3

def get_user(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # DANGER: SQL Injection!
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)
    return cursor.fetchone()
```

5. Sélectionnez **"Python"** comme langage
6. Cliquez sur **"Analyze Code"**
7. ⏳ Attendez **20-40 secondes** (première analyse plus longue)
8. 🎉 Regardez les vulnérabilités détectées !

**Résultat attendu :**
- ❌ **SQL Injection** détectée (CWE-89)
- ⚠️ Niveau de sévérité : **CRITICAL**
- 💡 Suggestions de correction avec code sécurisé

### Test 2 : Analyse de Diagramme

1. Allez dans **"Diagram Analysis"**
2. Téléchargez une image de votre architecture (PNG/JPG/SVG)
3. Cliquez sur **"Analyze Diagram"**
4. ⏳ Attendez **30-60 secondes**
5. 🎉 Consultez les recommandations Zero Trust !

---

## 📊 Modèles AI Utilisés (Ollama)

| Modèle | Usage | Taille | Performance CPU |
|--------|-------|--------|-----------------|
| **llama3.1:8b** | Analyse de code | 4.7 GB | 10-60s |
| **llava:13b** | Analyse de diagrammes | 7.4 GB | 20-90s |

### Modèles Alternatifs (Optionnels)

```bash
# Meilleure précision pour le code (plus lent)
docker-compose exec ollama ollama pull codellama:13b

# Modèle plus puissant (nécessite 48GB RAM)
docker-compose exec ollama ollama pull mixtral:8x7b

# Vision alternative
docker-compose exec ollama ollama pull bakllava
```

**Changer de modèle :** Éditez `docker-compose.yml` :
```yaml
environment:
  - OLLAMA_MODEL_CODE=codellama:13b  # Au lieu de llama3.1:8b
```

---

## ⚡ Optimisation Performance

### Option 1 : GPU NVIDIA (Recommandé)

Si vous avez une carte NVIDIA, décommentez dans `docker-compose.yml` (lignes 61-67) :

```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: all
          capabilities: [gpu]
```

Puis redémarrez :
```bash
docker-compose down
docker-compose up -d
```

**Performance avec GPU (RTX 3080) :**
- ⚡ Code : **2-15s** (au lieu de 10-60s)
- ⚡ Diagramme : **5-15s** (au lieu de 20-90s)

### Option 2 : Plus de RAM

Dans Docker Desktop → **Settings** → **Resources** :
- **Memory** : Minimum 8GB, Recommandé 16GB
- **CPU** : 4+ cores

---

## 🔧 Commandes Utiles

### Gestion des Services

```bash
# Démarrer
docker-compose up -d

# Arrêter
docker-compose down

# Redémarrer
docker-compose restart

# Voir les logs en temps réel
docker-compose logs -f backend

# Voir l'état des services
docker-compose ps
```

### Gestion des Modèles Ollama

```bash
# Lister les modèles installés
docker-compose exec ollama ollama list

# Télécharger un nouveau modèle
docker-compose exec ollama ollama pull <model-name>

# Supprimer un modèle (libérer de l'espace)
docker-compose exec ollama ollama rm <model-name>

# Tester Ollama directement
docker-compose exec ollama ollama run llama3.1:8b "Analyse ce code Python..."
```

### Nettoyage

```bash
# Arrêter et supprimer tout (ATTENTION: supprime les données)
docker-compose down -v

# Supprimer les images Docker
docker-compose down --rmi all

# Rebuild après changement de code
docker-compose up -d --build
```

---

## 🎯 Fonctionnalités

### Analyse de Code
- ✅ Support de **14+ langages** (Python, JS, TS, Java, Go, Rust, C/C++, PHP, Ruby, Swift, Kotlin...)
- ✅ Détection **OWASP Top 10 2025**
- ✅ Détection **CWE Top 25 2025**
- ✅ Détection de **secrets** (API keys, mots de passe, tokens)
- ✅ Vulnérabilités de **dépendances**
- ✅ Génération de **code sécurisé**
- ✅ Recommandations de **remédiation**

### Analyse de Diagrammes
- ✅ Support **PNG, JPG, SVG**
- ✅ Identification automatique des **composants**
- ✅ Évaluation de la **posture de sécurité**
- ✅ Recommandations **Zero Trust**
- ✅ Propositions **Secure-by-Design**
- ✅ Analyse de **conformité** (ISO 27001, NIS2, CIS)

---

## 🏗️ Architecture Technique

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Next.js   │─────▶│   FastAPI    │─────▶│   Ollama    │
│  Frontend   │      │   Backend    │      │  (AI Local) │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                     ┌──────┴──────┐
                     │             │
                ┌────▼────┐   ┌───▼────┐
                │PostgreSQL│   │ Redis  │
                └──────────┘   └────────┘
```

**Stack Technique :**
- **Frontend** : Next.js 15, React Server Components, Tailwind CSS
- **Backend** : Python 3.12, FastAPI, SQLAlchemy, Pydantic
- **AI** : Ollama (Llama 3.1, LLaVA)
- **Database** : PostgreSQL 16, Redis 7
- **Infra** : Docker, Kubernetes, Terraform

📖 [Documentation Architecture Complète](docs/ARCHITECTURE.md)

---

## 💰 Comparaison : Ollama vs APIs Payantes

| Critère | Ollama (ShadowScan) | Claude/GPT APIs |
|---------|---------------------|-----------------|
| **Coût** | **0€** ✅ | ~$5-15/mois |
| **Setup** | 15 min | 2 min |
| **Vitesse (CPU)** | 30s | 5s |
| **Vitesse (GPU)** | 5s | 5s |
| **Confidentialité** | **100% local** ✅ | Données envoyées |
| **Hors-ligne** | **Oui** ✅ | Non |
| **Limites** | **Aucune** ✅ | Quotas |
| **Qualité** | 85-90% | 95-98% |

**💡 Verdict :** Ollama est **parfait** pour usage personnel, apprentissage et données sensibles !

---

## 🚀 Déploiement en Production

### Option 1 : Vercel + Railway (Gratuit)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/K3E9X/ShadowScan)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/K3E9X/ShadowScan)

📖 **[Guide Complet de Déploiement](DEPLOY.md)**

### Option 2 : Local avec HTTPS

```bash
# Installer Caddy pour HTTPS automatique
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🆘 Problèmes Courants

### ❌ "Cannot connect to Ollama"

```bash
# Vérifier que Ollama est démarré
docker-compose ps ollama

# Redémarrer Ollama
docker-compose restart ollama

# Voir les logs
docker-compose logs ollama
```

### ❌ "Model not found"

```bash
# Re-télécharger le modèle
docker-compose exec ollama ollama pull llama3.1:8b
```

### ❌ "Out of memory"

```bash
# Solution 1: Augmenter la RAM Docker (Settings → Resources)
# Solution 2: Utiliser un modèle plus petit
OLLAMA_MODEL_CODE=llama3.1:8b  # Au lieu de 70b
```

### ❌ "Analysis timeout"

```bash
# C'est normal la première fois (Ollama charge le modèle)
# Attendez 1-2 minutes pour la première analyse
# Les suivantes seront plus rapides (10-30s)
```

### ❌ "Cannot access localhost:3000"

```bash
# Vérifier que les ports ne sont pas utilisés
lsof -i :3000
lsof -i :8000

# Changer les ports dans docker-compose.yml si besoin
```

---

## 📚 Documentation

- 🤖 **[Guide Ollama (FR)](docs/OLLAMA_SETUP.md)** - Configuration AI locale
- 🏗️ **[Architecture](docs/ARCHITECTURE.md)** - Architecture système complète
- 🚀 **[Déploiement Cloud](DEPLOY.md)** - Vercel, Railway, Render
- 🤝 **[Contributing](CONTRIBUTING.md)** - Guide de contribution
- 📖 **[API Docs](http://localhost:8000/api/docs)** - Documentation API interactive

---

## 🤝 Contributing

Les contributions sont les bienvenues !

1. Fork le projet
2. Créez votre branche (`git checkout -b feature/amazing-feature`)
3. Commit vos changements (`git commit -m 'feat: add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrez une Pull Request

📖 Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour plus de détails.

---

## 🔒 Sécurité & Conformité

### Standards Implémentés

- ✅ **OWASP Top 10 2025**
- ✅ **CWE Top 25 2025**
- ✅ **NIST 800-218 SSDF**
- ✅ **ISO 27001:2022**
- ✅ **NIS2 Directive**
- ✅ **CIS Benchmarks**
- ✅ **GDPR Compliance**

### Signaler une Vulnérabilité

🔐 **Email** : security@shadowscan.dev
⚠️ **Ne pas** ouvrir d'issue publique pour les vulnérabilités

---

## 📄 License

Ce projet est sous licence **MIT** - voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🙏 Remerciements

- **Ollama** - Pour les modèles AI locaux gratuits
- **Meta AI** - Pour Llama 3.1
- **OWASP** - Pour les frameworks de sécurité
- **MITRE** - Pour la base CWE
- **La communauté open source** ❤️

---

## 📞 Support

- 💬 **[GitHub Discussions](https://github.com/K3E9X/ShadowScan/discussions)**
- 🐛 **[Issues](https://github.com/K3E9X/ShadowScan/issues)**
- 📧 **Email** : support@shadowscan.dev

---

## ⭐ Star History

Si ShadowScan vous aide, **donnez une ⭐ sur GitHub** !

---

**Construit avec ❤️ pour la communauté de sécurité**

*ShadowScan - Sécurisez votre code gratuitement avec l'IA locale*
