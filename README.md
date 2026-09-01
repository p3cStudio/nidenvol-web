# Nid'Envol — site statique (Astro)

Site de présentation de la micro-crèche **Nid'Envol**, reconstruit à partir du site
WordPress/Elementor d'origine en **HTML/CSS statique**, assemblé avec
[Astro](https://astro.build).

Le header et le footer sont **mutualisés** (écrits une seule fois) et injectés dans
chaque page **au moment du build** : le HTML livré est 100 % statique, avec le
header/footer écrits « en dur » dans chaque page → **SEO parfait**, aucun serveur,
hébergeable tel quel sur GitHub Pages / Netlify / Cloudflare Pages.

> C'est du **SSG** (génération statique), pas du SSR : rien ne tourne côté serveur
> en production, on ne sert que des fichiers.

## Structure

```
src/
  layouts/BaseLayout.astro     ← squelette commun (importe header + footer)
  fragments/
    header.html                ← HEADER MUTUALISÉ (à éditer 1 seule fois)
    footer.html                ← FOOTER MUTUALISÉ (à éditer 1 seule fois)
    home-head/-content/-scripts.html     ← contenu propre à l'accueil
    arleux-head/-content/-scripts.html   ← contenu propre à la page Arleux
  pages/
    index.astro                → /
    micro-creche-arleux.astro  → /micro-creche-arleux/
public/
  wp-content/, wp-includes/    ← images, CSS, JS, polices (URLs racine-relatives /wp-content/…)
  .nojekyll
dist/                          ← résultat du build (à publier) — non versionné
mirror.py                      ← script ayant servi à aspirer le site d'origine
```

## Développer

```bash
npm install          # une fois
npm run dev          # serveur local avec rechargement -> http://localhost:4321
```

## Construire le site à publier

```bash
npm run build        # génère le dossier dist/ (HTML statique)
npm run preview      # prévisualise le build
```

Le contenu de `dist/` est ce qu'on met en ligne.

## Modifier / ajouter du contenu

- **Changer le footer (ou le header) sur TOUTES les pages** : éditer
  `src/fragments/footer.html` (ou `header.html`) — une seule fois — puis `npm run build`.
- **Ajouter une page** (ex. Bugnicourt) : créer `src/pages/micro-creche-bugnicourt.astro`
  sur le modèle de `micro-creche-arleux.astro` avec ses fragments de contenu.
  Le routing est automatique (`/micro-creche-bugnicourt/`).

## Publier sur GitHub Pages

Le déploiement est **automatique** via GitHub Actions (`.github/workflows/deploy.yml`) :
à chaque push sur `main`, l'action build le site et le publie.

Mise en route (une seule fois) :

1. Le dépôt GitHub doit être **public** (obligatoire pour GitHub Pages en offre gratuite).
2. Sur GitHub : **Settings → Pages → Build and deployment → Source = "GitHub Actions"**.
3. Pousser sur `main` → l'action se lance → le site est en ligne sur
   **https://p3cstudio.github.io/nivenvol-web/**

Le workflow build avec `BASE_PATH=/nivenvol-web` (sous-dossier de l'URL github.io).

### Passer sur le domaine nidenvol.fr (plus tard)

1. Créer un fichier `public/CNAME` contenant `www.nidenvol.fr`.
2. Dans `.github/workflows/deploy.yml`, **supprimer la ligne `BASE_PATH: /nivenvol-web`**
   (le site sera alors généré pour la racine `/`).
3. Configurer le DNS du domaine vers GitHub Pages, puis renseigner le domaine dans
   **Settings → Pages → Custom domain**.

Rien d'autre à changer : la gestion du base path (`src/lib/withBase.js`) devient
automatiquement inactive à la racine.

## Points connus

- **Navigation** : le menu et le footer renvoient vers les ancres de l'accueil
  (`/#creche`, `/#offre`…). Le bouton « Pré-inscription » ouvre un Google Forms externe.
- **Carte** : iframe Google Maps standard (se charge en ligne).
- **« Mentions légales »** pointe encore vers le site d'origine — à recréer en page
  statique quand tu voudras.
