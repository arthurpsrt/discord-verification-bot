# TMK Moments — site vitrine

Site statique (un seul `index.html` + images dans `assets/img/`), sans build.

- Ouvrir `index.html` dans un navigateur pour le voir en local.
- Déploiement : glisser le dossier `tmk-moments/` sur Netlify, Vercel, GitHub Pages ou n'importe quel hébergeur statique.
- Les événements sont dans le tableau `EVENTS` du script en bas de `index.html` (catégorie, nom, lieu, date, image).
- Le formulaire ne nécessite pas de serveur : à l'envoi, il prépare un message WhatsApp (+33 7 85 73 96 07) ou un email (tmkmoments@tmkpsrt.com) déjà rédigé avec tous les détails.
- Animations : GSAP 3.12.5 (cdnjs). Elles se désactivent si l'utilisateur a choisi « réduire les animations ».
