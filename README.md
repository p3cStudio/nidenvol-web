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

Deux options :

1. **Build local + push du dossier `dist/`** sur une branche `gh-pages`.
2. **GitHub Actions** (recommandé) : à chaque push, une action lance `npm run build`
   et publie `dist/`. Astro fournit un workflow prêt à l'emploi
   (`withastro/action`). Je peux le mettre en place sur demande.

Pour le domaine `nidenvol.fr` : ajouter un fichier `public/CNAME` contenant
`www.nidenvol.fr` (les chemins sont racine-relatifs, donc pensés pour un domaine à la racine).

## Points connus

- **Navigation** : le menu et le footer renvoient vers les ancres de l'accueil
  (`/#creche`, `/#offre`…). Le bouton « Pré-inscription » ouvre un Google Forms externe.
- **Carte** : iframe Google Maps standard (se charge en ligne).
- **« Mentions légales »** pointe encore vers le site d'origine — à recréer en page
  statique quand tu voudras.
