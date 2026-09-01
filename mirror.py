#!/usr/bin/env python3
"""Mirror www.nidenvol.fr (one-page Elementor site) into a static, relative-path site."""
import os, re, sys, urllib.request, urllib.parse, posixpath

HOST = "www.nidenvol.fr"
BASE = "https://" + HOST
ROOT = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"

downloaded = {}   # url(no query) -> local relative path
to_process_css = []

def url_to_local(url):
    """Map an absolute nidenvol URL to a local relative path (strip query)."""
    p = urllib.parse.urlparse(url)
    path = p.path
    if path.endswith("/") or path == "":
        path = path + "index.html"
    return path.lstrip("/")

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

def download(url):
    """Download a nidenvol asset. Return local relative path, or None."""
    clean = url.split("#")[0]
    key = clean.split("?")[0]
    if key in downloaded:
        return downloaded[key]
    local = url_to_local(clean)
    dest = os.path.join(ROOT, local)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if not os.path.exists(dest):
        try:
            data = fetch(clean)
        except Exception as e:
            print("  FAIL", clean, e)
            return None
        with open(dest, "wb") as f:
            f.write(data)
        print("  ok", local)
    downloaded[key] = local
    if local.endswith(".css"):
        to_process_css.append((clean, local))
    return local

def is_local_url(u):
    u = u.strip().strip('"').strip("'")
    if u.startswith("data:") or u.startswith("#"):
        return False
    if u.startswith("//"):
        u = "https:" + u
    if u.startswith("http"):
        return HOST in urllib.parse.urlparse(u).netloc
    return False  # only rewrite absolute nidenvol urls in this pass

def abs_url(u):
    u = u.strip()
    if u.startswith("//"):
        return "https:" + u
    return u

# ---- collect asset urls from a blob of HTML/CSS ----
ASSET_RE = re.compile(r'https?://' + re.escape(HOST) + r'/[^\s"\'\)]+')

def collect_urls(text):
    return set(m.group(0) for m in ASSET_RE.finditer(text))

def main():
    # 1. homepage
    html = fetch(BASE + "/").decode("utf-8", "replace")
    # find all asset urls (css/js/img/fonts) that are files (have an extension) or wp-content
    urls = collect_urls(html)
    asset_ext = (".css",".js",".webp",".png",".jpg",".jpeg",".gif",".svg",".woff",".woff2",".ttf",".eot",".ico",".mp4",".webm")
    for u in sorted(urls):
        cu = u.split("?")[0].split("#")[0]
        if cu.lower().endswith(asset_ext):
            download(u)
    # 2. recursively process css for url()/@import
    i = 0
    while i < len(to_process_css):
        css_url, css_local = to_process_css[i]
        i += 1
        dest = os.path.join(ROOT, css_local)
        with open(dest, "r", encoding="utf-8", errors="replace") as f:
            css = f.read()
        for u in collect_urls(css):
            cu = u.split("?")[0].split("#")[0]
            if cu.lower().endswith(asset_ext):
                download(u)
    print("Downloaded", len(downloaded), "assets")

    # 3. rewrite all downloaded css + homepage with relative paths
    def rewrite(text, from_local):
        from_dir = posixpath.dirname(from_local)
        def repl(m):
            u = m.group(0)
            key = u.split("?")[0].split("#")[0]
            if key in downloaded:
                target = downloaded[key]
                rel = posixpath.relpath(target, from_dir if from_dir else ".")
                return rel
            # nidenvol url we didn't download (e.g. internal page link) -> leave host-less relative
            return u
        return ASSET_RE.sub(repl, text)

    # homepage
    html_out = rewrite(html, "index.html")
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_out)
    print("wrote index.html")
    # css files
    for css_url, css_local in to_process_css:
        dest = os.path.join(ROOT, css_local)
        with open(dest, "r", encoding="utf-8", errors="replace") as f:
            css = f.read()
        css2 = rewrite(css, css_local)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(css2)
    print("rewrote", len(to_process_css), "css files")

if __name__ == "__main__":
    main()
