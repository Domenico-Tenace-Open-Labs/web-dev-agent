#!/usr/bin/env python3
"""Collects raw data about a website and prints it as JSON.

Usage:
    python3 fetch_site.py <url> [--css-files N]

Standard library only. It fetches the home page, the HTTP headers, robots.txt,
the sitemap and the first N stylesheets, then extracts:
  - on-page SEO (title, meta, headings, canonical, hreflang, Open Graph, JSON-LD)
  - technology signals (CMS, frameworks, CSS/JS libraries, analytics, hosting)
  - color palette and fonts
  - internal links (to rebuild the site structure)

If the network is not reachable from the shell, the script prints a JSON with
an "error" key: in that case read the pages with WebFetch instead.
"""
import collections
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

UA = "Mozilla/5.0 (compatible; website-analyzer/1.0)"
TIMEOUT = 15


def get(url, max_bytes=2_000_000):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": UA, "Accept": "*/*", "Accept-Language": "en,it;q=0.8"},
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            body = r.read(max_bytes)
            charset = r.headers.get_content_charset() or "utf-8"
            return {
                "url": r.geturl(),
                "status": r.status,
                "headers": {k.lower(): v for k, v in r.headers.items()},
                "text": body.decode(charset, errors="replace"),
            }
    except urllib.error.HTTPError as e:
        return {"url": url, "status": e.code, "headers": {}, "text": "", "error": str(e)}
    except Exception as e:  # blocked network, DNS, timeout, TLS
        return {"url": url, "status": None, "headers": {}, "text": "", "error": str(e)}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self._in_title = False
        self.lang = None
        self.meta = {}
        self.links = []          # (rel, href, extra)
        self.scripts = []
        self.inline_scripts = 0
        self.anchors = []
        self.headings = collections.defaultdict(list)
        self._head_tag = None
        self._head_buf = []
        self.imgs_total = 0
        self.imgs_no_alt = 0
        self.jsonld = 0
        self.inline_css = []
        self._in_style = False
        self.classes = collections.Counter()
        self.forms = 0
        self.has_viewport = False
        self.body_text_len = 0
        self._in_body = False
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            key = a.get("name") or a.get("property") or a.get("http-equiv")
            if key:
                self.meta[key.lower()] = a.get("content", "")
        elif tag == "link":
            self.links.append((a.get("rel", ""), a.get("href", ""), a))
        elif tag == "script":
            if a.get("src"):
                self.scripts.append(a["src"])
            else:
                self.inline_scripts += 1
            if a.get("type") == "application/ld+json":
                self.jsonld += 1
            self._skip += 1
        elif tag == "style":
            self._in_style = True
            self._skip += 1
        elif tag == "a" and a.get("href"):
            self.anchors.append(a["href"])
        elif tag in ("h1", "h2", "h3"):
            self._head_tag = tag
            self._head_buf = []
        elif tag == "img":
            self.imgs_total += 1
            if not (a.get("alt") or "").strip():
                self.imgs_no_alt += 1
        elif tag == "form":
            self.forms += 1
        elif tag == "body":
            self._in_body = True
        if a.get("style"):
            self.inline_css.append(a["style"])
        if a.get("class"):
            for c in a["class"].split():
                self.classes[c] += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "style":
            self._in_style = False
            self._skip = max(0, self._skip - 1)
        elif tag == "script":
            self._skip = max(0, self._skip - 1)
        elif tag in ("h1", "h2", "h3") and self._head_tag == tag:
            text = " ".join("".join(self._head_buf).split())
            if text:
                self.headings[tag].append(text[:120])
            self._head_tag = None

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_style:
            self.inline_css.append(data)
        if self._head_tag:
            self._head_buf.append(data)
        if self._in_body and not self._skip:
            self.body_text_len += len(data.strip())


TECH_RULES = [
    # (name, category, pattern matched on html + script src + link href)
    ("WordPress", "CMS", r"wp-content|wp-includes|wp-json"),
    ("Shopify", "E-commerce", r"cdn\.shopify\.com|Shopify\.theme"),
    ("WooCommerce", "E-commerce", r"woocommerce"),
    ("Wix", "Site builder", r"static\.wixstatic\.com|wix\.com/_api|X-Wix"),
    ("Squarespace", "Site builder", r"squarespace\.com|static1\.squarespace"),
    ("Webflow", "Site builder", r"webflow\.com|data-wf-page|w-nav"),
    ("Framer", "Site builder", r"framerusercontent|framer\.com"),
    ("Joomla", "CMS", r"/media/jui/|Joomla!"),
    ("Drupal", "CMS", r"Drupal|/sites/default/files"),
    ("PrestaShop", "E-commerce", r"prestashop"),
    ("Magento", "E-commerce", r"Magento|/static/version"),
    ("Next.js", "JS framework", r"/_next/|__NEXT_DATA__"),
    ("Nuxt", "JS framework", r"/_nuxt/|__NUXT__"),
    ("Gatsby", "JS framework", r"/___gatsby|gatsby-"),
    ("Astro", "JS framework", r"astro-island|/_astro/"),
    ("SvelteKit", "JS framework", r"/_app/immutable|sveltekit"),
    ("Remix", "JS framework", r"__remixContext"),
    ("React", "JS library", r"data-reactroot|react(\.production|-dom)|__reactFiber|id=\"root\""),
    ("Vue", "JS library", r"vue(\.runtime)?(\.min)?\.js|data-v-[0-9a-f]{6,}|id=\"app\""),
    ("Angular", "JS framework", r"ng-version|ng-app|angular(\.min)?\.js"),
    ("jQuery", "JS library", r"jquery"),
    ("Alpine.js", "JS library", r"x-data=|alpinejs"),
    ("htmx", "JS library", r"htmx"),
    ("Tailwind CSS", "CSS", r"tailwind"),
    ("Bootstrap", "CSS", r"bootstrap"),
    ("Elementor", "Page builder", r"elementor"),
    ("Divi", "Page builder", r"et_pb_|et-boc"),
    ("WPBakery", "Page builder", r"vc_row|wpb_"),
    ("Cloudflare", "CDN/Hosting", r"cdnjs\.cloudflare|cf-ray|__cf_bm"),
    ("Vercel", "CDN/Hosting", r"vercel"),
    ("Netlify", "CDN/Hosting", r"netlify"),
    ("Google Tag Manager", "Analytics", r"googletagmanager\.com/gtm\.js|GTM-[A-Z0-9]+"),
    ("Google Analytics", "Analytics", r"google-analytics\.com|gtag/js|G-[A-Z0-9]{6,}|UA-\d+"),
    ("Meta Pixel", "Analytics", r"connect\.facebook\.net|fbq\("),
    ("Hotjar", "Analytics", r"hotjar"),
    ("Plausible", "Analytics", r"plausible\.io"),
    ("Matomo", "Analytics", r"matomo|piwik"),
    ("Iubenda", "Privacy/Cookie consent", r"iubenda"),
    ("Cookiebot", "Privacy/Cookie consent", r"cookiebot"),
    ("reCAPTCHA", "Security", r"recaptcha"),
    ("Stripe", "Payments", r"js\.stripe\.com"),
    ("PayPal", "Payments", r"paypal\.com/sdk|paypalobjects"),
    ("Font Awesome", "Icons", r"font-?awesome|fontawesome"),
    ("Google Fonts", "Font", r"fonts\.googleapis\.com|fonts\.gstatic\.com"),
    ("Adobe Fonts", "Font", r"use\.typekit\.net"),
]

HEADER_HINTS = ["server", "x-powered-by", "x-generator", "via", "x-vercel-id",
                "x-nf-request-id", "cf-ray", "x-shopify-stage", "x-wix-request-id",
                "content-security-policy", "strict-transport-security",
                "x-frame-options", "content-encoding", "cache-control"]

HEX = re.compile(r"#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
FONT_FAMILY = re.compile(r"font-family\s*:\s*([^;}{]+)", re.I)
FONT_FACE = re.compile(r"@font-face\s*{[^}]*?font-family\s*:\s*['\"]?([^;'\"]+)", re.I | re.S)
CSS_VAR = re.compile(r"(--[\w-]*(?:color|primary|secondary|accent|brand|bg|background|foreground|text)[\w-]*)\s*:\s*([^;}{]+)", re.I)
GENERIC_FONTS = {"inherit", "initial", "sans-serif", "serif", "monospace", "system-ui",
                 "-apple-system", "blinkmacsystemfont", "cursive", "fantasy", "ui-sans-serif",
                 "ui-serif", "ui-monospace", "unset"}


def normalize_hex(h):
    h = h.lower()
    if len(h) == 4:
        h = "#" + "".join(c * 2 for c in h[1:])
    return h


def clean_family(raw):
    out = []
    for part in raw.split(","):
        name = part.strip().strip("'\"").strip()
        if name and name.lower() not in GENERIC_FONTS and not name.startswith("var("):
            out.append(name)
    return out


def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: fetch_site.py <url> [--css-files N]", file=sys.stderr)
        sys.exit(2)
    url = args[0]
    css_limit = 6
    if "--css-files" in args:
        css_limit = int(args[args.index("--css-files") + 1])
    if not re.match(r"^https?://", url):
        url = "https://" + url

    home = get(url)
    result = {"requested_url": url, "final_url": home["url"], "status": home["status"]}
    if home.get("error") and not home["text"]:
        result["error"] = home["error"]
        result["hint"] = "Network not reachable from the shell. Use WebFetch to read the pages."
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    html = home["text"]
    base = home["url"]
    host = urllib.parse.urlparse(base).netloc.lower().removeprefix("www.")

    p = PageParser()
    try:
        p.feed(html)
    except Exception as e:
        result["parse_warning"] = str(e)

    # --- headers
    result["headers"] = {k: v[:200] for k, v in home["headers"].items() if k in HEADER_HINTS}

    # --- SEO on page
    canonical = next((h for rel, h, _ in p.links if "canonical" in rel), None)
    hreflang = [a.get("hreflang") for rel, _, a in p.links if "alternate" in rel and a.get("hreflang")]
    og = {k: v[:160] for k, v in p.meta.items() if k.startswith("og:") or k.startswith("twitter:")}
    result["seo"] = {
        "title": " ".join(p.title.split()),
        "title_length": len(" ".join(p.title.split())),
        "meta_description": p.meta.get("description", ""),
        "meta_description_length": len(p.meta.get("description", "")),
        "robots_meta": p.meta.get("robots"),
        "canonical": canonical,
        "lang": p.lang,
        "viewport": "viewport" in p.meta,
        "hreflang": hreflang,
        "open_graph_twitter": og,
        "json_ld_blocks": p.jsonld,
        "h1": p.headings.get("h1", []),
        "h2": p.headings.get("h2", [])[:12],
        "h3_count": len(p.headings.get("h3", [])),
        "images_total": p.imgs_total,
        "images_without_alt": p.imgs_no_alt,
        "visible_text_chars": p.body_text_len,
        "forms": p.forms,
    }

    # --- internal links
    internal = collections.OrderedDict()
    external = set()
    for href in p.anchors:
        if href.startswith(("mailto:", "tel:", "javascript:", "#")):
            continue
        full = urllib.parse.urljoin(base, href)
        pu = urllib.parse.urlparse(full)
        h = pu.netloc.lower().removeprefix("www.")
        if h == host:
            path = pu.path or "/"
            internal.setdefault(path, 0)
            internal[path] += 1
        else:
            external.add(h)
    result["links"] = {
        "internal_unique": len(internal),
        "internal_paths": list(internal.keys())[:60],
        "external_domains": sorted(external)[:25],
        "mailto_or_tel": any(a.startswith(("mailto:", "tel:")) for a in p.anchors),
    }

    # --- robots and sitemap
    origin = "{0.scheme}://{0.netloc}".format(urllib.parse.urlparse(base))
    robots = get(origin + "/robots.txt", 100_000)
    sitemaps = []
    if robots["status"] == 200:
        sitemaps = re.findall(r"(?im)^sitemap:\s*(\S+)", robots["text"])
        result["robots_txt"] = robots["text"][:800]
    else:
        result["robots_txt"] = None
    if not sitemaps:
        sitemaps = [origin + "/sitemap.xml"]
    sm_info = []
    for sm in sitemaps[:2]:
        r = get(sm, 600_000)
        if r["status"] == 200 and r["text"]:
            locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", r["text"])
            is_index = "<sitemapindex" in r["text"]
            info = {"url": sm, "is_index": is_index, "entries": len(locs), "sample": locs[:12]}
            if is_index and locs:
                sub = get(locs[0], 600_000)
                if sub["status"] == 200:
                    sublocs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", sub["text"])
                    info["first_child"] = {"url": locs[0], "entries": len(sublocs), "sample": sublocs[:8]}
            sm_info.append(info)
    result["sitemaps"] = sm_info

    # --- technologies
    blob = html[:600_000] + "\n" + "\n".join(p.scripts) + "\n" + "\n".join(h for _, h, _ in p.links)
    blob += "\n" + "\n".join(f"{k}: {v}" for k, v in home["headers"].items())
    generator = p.meta.get("generator")
    found = {}
    for name, cat, pat in TECH_RULES:
        if re.search(pat, blob, re.I):
            found[name] = cat
    # more precise signal based on utility classes
    cls = p.classes
    tw_hits = sum(v for c, v in cls.items() if re.match(r"^(?:[a-z]+:)*(?:flex|grid|px-\d|py-\d|mt-\d|mb-\d|text-(?:xs|sm|base|lg|xl|\dxl)|bg-[a-z]+-\d{2,3}|rounded(?:-\w+)?|gap-\d)$", c))
    if tw_hits > 25:
        found["Tailwind CSS"] = "CSS (inferred from utility classes)"
    if "react" in blob.lower() and "Next.js" in found:
        found.pop("React", None)
        found["React (via Next.js)"] = "JS library"
    result["technologies"] = {
        "generator_meta": generator,
        "detected": found,
        "scripts_count": len(p.scripts),
        "inline_scripts": p.inline_scripts,
        "script_hosts": sorted({urllib.parse.urlparse(urllib.parse.urljoin(base, s)).netloc for s in p.scripts})[:20],
        "likely_client_rendered": p.body_text_len < 400 and len(p.scripts) > 0,
        "top_classes": [c for c, _ in cls.most_common(15)],
    }

    # --- CSS: colors and fonts
    css_text = "\n".join(p.inline_css)
    css_urls = []
    for rel, href, _ in p.links:
        if "stylesheet" in rel and href:
            css_urls.append(urllib.parse.urljoin(base, href))
    fetched_css = []
    for cu in css_urls[:css_limit]:
        r = get(cu, 800_000)
        if r["status"] == 200:
            css_text += "\n" + r["text"]
            fetched_css.append(cu)

    colors = collections.Counter(normalize_hex(c) for c in HEX.findall(css_text))
    # leave pure white/black out of the brand colors, but report them separately
    neutral = {"#ffffff", "#000000"}
    brand = [(c, n) for c, n in colors.most_common(40) if c not in neutral]
    css_vars = {}
    for name, val in CSS_VAR.findall(css_text):
        if name not in css_vars and len(css_vars) < 25:
            css_vars[name] = val.strip()[:60]

    fonts = collections.Counter()
    for raw in FONT_FAMILY.findall(css_text):
        for f in clean_family(raw):
            fonts[f] += 1
    face = sorted({f.strip() for f in FONT_FACE.findall(css_text) if f.strip()})[:15]
    gfonts = []
    for rel, href, _ in p.links:
        if href and "fonts.googleapis.com" in href:
            for fam in re.findall(r"family=([^&:]+)", urllib.parse.unquote(href)):
                gfonts.append(fam.replace("+", " "))
    theme_color = p.meta.get("theme-color")

    result["design"] = {
        "css_files_fetched": fetched_css,
        "css_files_total": len(css_urls),
        "theme_color_meta": theme_color,
        "top_colors": brand[:14],
        "white_black_usage": {c: colors[c] for c in neutral if c in colors},
        "css_variables": css_vars,
        "font_families_by_usage": fonts.most_common(10),
        "font_face_declared": face,
        "google_fonts": sorted(set(gfonts)),
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
