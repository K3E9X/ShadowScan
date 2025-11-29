# 🚀 Guide de Déploiement ShadowScan

Ce guide vous explique comment déployer **ShadowScan** gratuitement en quelques clics.

## ✨ Déploiement Rapide (Gratuit)

### Option 1 : Vercel + Railway (Recommandé)

#### 1️⃣ Déployer le Frontend sur Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/K3E9X/New-project&project-name=shadowscan&repository-name=shadowscan&root-directory=frontend)

**OU manuellement :**

1. Allez sur [vercel.com](https://vercel.com)
2. Cliquez sur "Add New" → "Project"
3. Importez votre repo GitHub : `K3E9X/New-project`
4. Configurez :
   - **Framework Preset** : Next.js
   - **Root Directory** : `frontend`
   - **Build Command** : `npm run build`
   - **Output Directory** : `.next`
5. Ajoutez les variables d'environnement :
   ```
   NEXT_PUBLIC_API_URL=https://votre-backend.railway.app
   ```
6. Cliquez sur "Deploy"

✅ Votre frontend sera disponible sur : `https://shadowscan.vercel.app`

#### 2️⃣ Déployer le Backend sur Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/K3E9X/New-project)

**OU manuellement :**

1. Allez sur [railway.app](https://railway.app)
2. Cliquez sur "New Project"
3. Sélectionnez "Deploy from GitHub repo"
4. Choisissez `K3E9X/New-project`
5. Ajoutez PostgreSQL et Redis :
   - Cliquez sur "+ New" → "Database" → "Add PostgreSQL"
   - Cliquez sur "+ New" → "Database" → "Add Redis"
6. Configurez les variables d'environnement :
   ```
   ANTHROPIC_API_KEY=votre_clé_anthropic
   SECRET_KEY=votre_clé_secrète_32_caractères
   CORS_ORIGINS=https://shadowscan.vercel.app
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   REDIS_URL=${{Redis.REDIS_URL}}
   ```
7. Dans Settings → Deploy :
   - **Root Directory** : `backend`
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
8. Déployez !

✅ Votre backend sera disponible sur : `https://shadowscan-production.up.railway.app`

#### 3️⃣ Connecter Frontend et Backend

1. **Dans Vercel**, mettez à jour la variable :
   ```
   NEXT_PUBLIC_API_URL=https://shadowscan-production.up.railway.app
   ```
2. **Dans Railway**, ajoutez le domaine Vercel au CORS :
   ```
   CORS_ORIGINS=https://shadowscan.vercel.app
   ```

---

### Option 2 : Render (Tout-en-un)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/K3E9X/New-project)

1. Cliquez sur le bouton ci-dessus
2. Connectez votre compte GitHub
3. Render va automatiquement :
   - Déployer le backend
   - Déployer le frontend
   - Créer PostgreSQL
   - Créer Redis
4. Ajoutez votre `ANTHROPIC_API_KEY` dans les variables d'environnement

✅ Votre app sera disponible sur : `https://shadowscan.onrender.com`

---

### Option 3 : Netlify + Supabase

#### Frontend sur Netlify

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/K3E9X/New-project)

#### Backend sur Supabase Edge Functions

1. Installez Supabase CLI : `npm install -g supabase`
2. Créez un projet sur [supabase.com](https://supabase.com)
3. Déployez le backend comme Edge Function
4. Connectez PostgreSQL de Supabase

---

## 🔧 Configuration Post-Déploiement

### Mise à Jour du README

Mettez à jour les badges dans votre `README.md` :

```markdown
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/K3E9X/New-project)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/K3E9X/New-project)

🌐 **Live Demo** : [https://shadowscan.vercel.app](https://shadowscan.vercel.app)
```

### Variables d'Environnement Requises

**Backend (Railway/Render) :**
```env
ANTHROPIC_API_KEY=sk-ant-xxxxx          # Obligatoire
SECRET_KEY=minimum-32-caractères         # Obligatoire
DATABASE_URL=postgresql://...            # Auto (Railway/Render)
REDIS_URL=redis://...                    # Auto (Railway/Render)
CORS_ORIGINS=https://shadowscan.vercel.app
ENVIRONMENT=production
DEBUG=false
```

**Frontend (Vercel) :**
```env
NEXT_PUBLIC_API_URL=https://votre-backend.railway.app
```

---

## 📊 Tableau de Comparaison

| Plateforme | Frontend | Backend | Database | Prix | Limite |
|------------|----------|---------|----------|------|--------|
| **Vercel + Railway** | ✅ | ✅ | ✅ | Gratuit | 500h/mois |
| **Render** | ✅ | ✅ | ✅ | Gratuit | 750h/mois |
| **Netlify + Supabase** | ✅ | ⚠️ | ✅ | Gratuit | 100GB/mois |
| **Fly.io** | ✅ | ✅ | ⚠️ | Gratuit | 3 apps |

---

## 🎯 Recommandation

Pour ShadowScan, je recommande **Vercel + Railway** car :

✅ Déploiement automatique à chaque push
✅ HTTPS gratuit
✅ PostgreSQL + Redis inclus
✅ Logs et monitoring
✅ Scaling automatique
✅ 99.9% uptime

---

## 🔄 Déploiement Continu (Automatique)

Avec la configuration actuelle, **chaque fois que vous pushez sur GitHub** :

1. ✅ GitHub Actions exécute les tests
2. ✅ Les images Docker sont buildées
3. ✅ Vercel déploie automatiquement le frontend
4. ✅ Railway déploie automatiquement le backend

**Aucune action manuelle nécessaire !**

---

## 🆘 Dépannage

### Le backend ne démarre pas
- Vérifiez que `ANTHROPIC_API_KEY` est définie
- Vérifiez que `DATABASE_URL` et `REDIS_URL` sont correctes
- Consultez les logs : `railway logs` ou dans le dashboard Render

### Le frontend ne se connecte pas au backend
- Vérifiez `NEXT_PUBLIC_API_URL` dans Vercel
- Vérifiez `CORS_ORIGINS` dans Railway/Render
- Testez l'API : `curl https://votre-backend/health`

### Erreur de base de données
- Railway/Render créent automatiquement la DB
- Assurez-vous que les migrations sont exécutées

---

## 📞 Support

Des questions ? Ouvrez une [issue GitHub](https://github.com/K3E9X/New-project/issues) !

---

**🚀 Bon déploiement !**
