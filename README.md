# Discord Verification Bot 🤖

Un bot Discord pour vérifier les utilisateurs via des réactions et attribuer des rôles automatiquement.

## ✨ Fonctionnalités

- ✅ Embed des règles avec réaction
- ✅ Attribution automatique du rôle "MEMBER"
- ✅ Accès aux salons réservés après vérification
- ✅ Fonctionne 24/7 sur Railway

## 🚀 Déploiement sur Railway (5 minutes)

### Étape 1 : Créer un repo GitHub

1. Va sur https://github.com/new
2. Donne un nom : `discord-verification-bot`
3. Clique sur "Create repository"

### Étape 2 : Ajouter les fichiers

1. Clique sur "uploading an existing file"
2. Ajoute les 3 fichiers :
   - `main.py`
   - `requirements.txt`
   - `Procfile` (contenu : `worker: python main.py`)

3. Clique sur "Commit changes"

### Étape 3 : Déployer sur Railway

1. Va sur https://railway.app
2. Clique sur "New Project"
3. Sélectionne "Deploy from GitHub"
4. Connecte ton GitHub et choisis le repo
5. Clique sur "Deploy"

### Étape 4 : Ajouter le Token Discord

1. Sur Railway, va dans "Variables"
2. Ajoute une variable :
   - **Key** : `DISCORD_TOKEN`
   - **Value** : [TON NOUVEAU TOKEN]
3. Clique sur "Save"

🎉 **C'est bon ! Ton bot fonctionne 24/7 !**

## 📋 Configuration du serveur Discord

### Créer les salons

- `#bienvenue` - Accessible à tous (règles + réaction)
- `#roles` - Accessible qu'aux MEMBER après vérification
- Autres salons - Masqués sauf pour MEMBER

### Poster les règles

1. Va dans le salon `#bienvenue`
2. Tape : `!setup_rules`
3. Le bot poste automatiquement l'embed avec ✅

### Configurer les permissions

Pour chaque salon (sauf `#bienvenue`) :
1. Clique sur les paramètres ⚙️
2. Va dans "Permissions"
3. Ajoute une permission pour `@everyone` : **Voir les salons** = ❌
4. Ajoute une permission pour le rôle `MEMBER` : **Voir les salons** = ✅

## 🔧 Variables d'environnement

| Variable | Valeur |
|----------|--------|
| `DISCORD_TOKEN` | Ton token Discord (ne le partage JAMAIS en public !) |

## ⚠️ Sécurité

- **NE PARTAGE JAMAIS TON TOKEN !**
- Si tu l'as accidentellement partagé, va dans Discord Developer Portal et clique sur "Reset Token"
- Le token doit TOUJOURS rester privé

## 🆘 Troubleshooting

**Le bot ne démarre pas ?**
- Vérifie que le `DISCORD_TOKEN` est bien configuré dans Railway
- Regarde les logs dans Railway ("Logs" tab)

**Le bot démarre mais ne répond pas ?**
- Attends quelques secondes après le déploiement
- Redémarre le bot dans Railway (icône refresh)

**Les permissions ne fonctionnent pas ?**
- Attends quelques secondes après avoir donné le rôle
- Vérifie que le rôle du bot est AU-DESSUS du rôle MEMBER dans l'ordre des rôles

## 📞 Besoin d'aide ?

Si quelque chose ne fonctionne pas :
1. Regarde les logs dans Railway
2. Vérifie que le token est correct
3. Assure-toi que le bot a les permissions nécessaires

---

**Fait avec ❤️ pour ton serveur Discord**
