import { defineConfig } from 'astro/config';

// Site statique (SSG) : `astro build` génère du HTML pur dans dist/, hébergeable
// tel quel sur GitHub Pages. Header/footer sont mutualisés via des composants,
// mais écrits « en dur » dans chaque page au build → SEO parfait, aucun serveur.
export default defineConfig({
  site: 'https://www.nidenvol.fr',
  build: {
    format: 'directory', // /micro-creche-arleux/ -> dist/micro-creche-arleux/index.html
  },
});
