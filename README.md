# Nid'Envol — site statique

Copie statique fidèle du site de présentation de la micro-crèche **Nid'Envol**
(site one-page à l'origine sous WordPress / Elementor), reconstruite en
HTML/CSS/JS purs pour un hébergement simple (GitHub Pages, Netlify, Cloudflare
Pages, OVH, etc.). Aucune base de données, aucun PHP.

## Contenu

- `index.html` — la page d'accueil (one-page avec navigation par ancres).
- `micro-creche-arleux/index.html` — page « Micro-crèche proche d'Arleux »
  (URL propre `/micro-creche-arleux/`). Liée depuis le footer de l'accueil via
  le terme « crèche Arleux ». Son menu renvoie vers les ancres de l'accueil.
- `wp-content/` — tous les CSS, JS, images et polices, chemins **relatifs**
  (le site fonctionne à la racine d'un domaine comme dans un sous-dossier).
- `.nojekyll` — évite tout traitement Jekyll sur GitHub Pages.
- `mirror.py` — script ayant servi à télécharger le site (utile pour re-synchroniser
  si le site d'origine change ; non nécessaire à l'hébergement).

## Tester en local

```bash
python3 -m http.server 8000
# puis ouvrir http://localhost:8000
```

(Ouvrir `index.html` directement en `file://` marche aussi, mais un serveur local
reproduit mieux le comportement réel.)

## Publier sur GitHub Pages

1. Créer un dépôt et y pousser ce dossier.
2. Repo → **Settings → Pages** → *Source: Deploy from a branch* → branche `main`, dossier `/ (root)`.
3. Le site sera en ligne sous `https://<utilisateur>.github.io/<repo>/`.
4. Pour utiliser le domaine `nidenvol.fr` : ajouter le domaine dans *Pages → Custom domain*
   et créer un fichier `CNAME` contenant `www.nidenvol.fr`.

## Points à noter

- **Navigation** : le menu utilise des ancres (`#creche`, `#offre`, `#equipe`, …) — tout est sur la page.
- **Bouton « Pré-inscription »** : pointe vers un formulaire Google Forms externe (inchangé).
- **Carte** : iframe Google Maps standard (se charge en ligne, nécessite une connexion).
- **Lien « Mentions légales »** : pointe encore vers la page du site d'origine
  (`nidenvol.fr/mentions-legales/`) — à recréer en page statique quand les
  pages de contenu seront prêtes.
- Quelques balises `<link>` de métadonnées (flux RSS, `wp-json`) subsistent dans
  le `<head>` : sans effet sur l'affichage.
