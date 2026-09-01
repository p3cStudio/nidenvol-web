import { defineConfig } from 'astro/config';

// Site statique (SSG) : `astro build` génère du HTML pur dans dist/, hébergeable
// tel quel sur GitHub Pages. Header/footer sont mutualisés via des composants,
// mais écrits « en dur » dans chaque page au build → SEO parfait, aucun serveur.
// base : piloté par la variable d'env BASE_PATH.
//   - non définie -> "/"  (racine : pour le domaine nidenvol.fr)
//   - "/nivenvol-web" -> sous-dossier (URL de test p3cstudio.github.io/nivenvol-web/)
// La GitHub Action passe BASE_PATH=/nivenvol-web pour le déploiement de test.
export default defineConfig({
  site: 'https://www.nidenvol.fr',
  base: process.env.BASE_PATH || '/',
  build: {
    format: 'directory', // /micro-creche-arleux/ -> dist/micro-creche-arleux/index.html
  },
});
