// Préfixe les URLs racine-relatives (/wp-content, /wp-includes, liens internes) par
// le "base path" du site, pour que tout fonctionne aussi bien à la racine d'un domaine
// (base = "/") que dans un sous-dossier GitHub Pages (base = "/nivenvol-web/").
//
// - À la racine (base === "/") : NO-OP, la fonction renvoie le HTML tel quel.
//   -> rien à retirer le jour où l'on passe sur le domaine nidenvol.fr.
// - En sous-dossier : réécrit /wp-content/... en /nivenvol-web/wp-content/..., etc.
//
// Les URLs absolues (https://www.nidenvol.fr/...) ne sont jamais touchées : la regex
// n'agit que sur un / précédé d'un délimiteur d'attribut ("=' ( , ou espace).
export function withBase(html) {
  let base = import.meta.env.BASE_URL; // "/", "/nivenvol-web" ou "/nivenvol-web/"
  if (base === '/' || base === '') return html;
  if (!base.endsWith('/')) base += '/'; // garantir le slash final
  return html
    // assets : src="/css/...", /js/..., /fonts/..., /img/..., srcset "..., /img/..."
    .replace(/([="'(,]\s*)\/(css|js|fonts|img|vendor)\//g, (_m, p, dir) => `${p}${base}${dir}/`)
    // liens internes
    .replaceAll('href="/"', `href="${base}"`)
    .replace(/href="\/(#|micro-creche-[a-z-]+\/)/g, `href="${base}$1`);
}
