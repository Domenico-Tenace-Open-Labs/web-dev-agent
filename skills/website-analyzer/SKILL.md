---
name: website-analyzer
description: Analyzes a website from its URL (page structure, on-page SEO, technologies and CMS/framework, color palette and fonts, target audience), lists its strengths and weaknesses, proposes concrete fixes for the weak points, and saves a concise report to docs/ANALYSIS.md. Use this skill every time the user shares a link and asks to analyze, study, reverse-engineer, audit, review or "figure out how this site is built", even if they never mention the skill. Example requests (in any language) "analyze this website", "what is this site built with?", "what stack does it use?", "what colors and fonts does it use?", "who is it aimed at?", "what is good and bad about this site?", "how could it be improved?", "quick SEO audit", "competitor analysis", "website analysis", "tech stack", "site audit".
---

# Website Analyzer

Given URL, produces compact analysis in `docs/ANALYSIS.md` covering: structure + SEO, technologies, visual design, target audience. Closes with strengths, weaknesses, fixes.

Reader should grok site build, audience, next steps in minutes. File short, to the point: ten good lines beat fifty padded. Unverifiable → declared, not guessed.

## Workflow

### 1. Prepare the URL
If scheme missing, add `https://`. If no link given, ask for it.

### 2. Collect raw data with the script
```bash
python3 <skill-path>/scripts/fetch_site.py <url>
```
Script uses stdlib only, prints JSON with: HTTP headers, home page SEO (title, meta description, H1/H2, canonical, hreflang, Open Graph, JSON-LD, images without alt), internal links, robots.txt, sitemap, technology signals, most used colors, CSS variables, fonts. Use `--css-files N` to read more stylesheets (default 6).

If JSON contains `"error"`, network blocked from shell: switch to WebFetch to read pages (see step 3) and mark as "not verifiable" everything needing HTML source (framework versions, CSS classes, loaded scripts). Don't retry with curl or other commands — same filter blocks all.

### 3. Read the pages that matter
With WebFetch, open home page then 3-4 pages from internal links: about, services/products, contact, blog/pricing. Don't crawl everything. Look for:
- what site sells/offers, in one sentence
- tone of voice (formal, technical, ironic, institutional)
- main CTAs (quote, purchase, signup, booking)
- whether prices shown, language, geographic market, reviews/case studies

If page near-empty (`likely_client_rendered: true` in JSON), site is client-rendered: say so — affects SEO too.

### 4. Interpret, don't just list
Script gives clues, you draw conclusions. Criteria:

**Structure and SEO**
- Rebuild site map from `internal_paths` + sitemap: main sections, depth, rough page count.
- Check essentials: title (~50-60 chars), meta description (~120-160), single sensible H1, canonical, language, viewport, structured data, Open Graph, robots.txt + sitemap present, alt text on images.
- Flag only problems you see, with count ("12 of 14 images without alt").

**Technologies**
- Separate CMS, framework, CSS library, hosting/CDN, analytics, payments. Source the clue when non-obvious ("`/_next/` in scripts, so Next.js").
- Tech from single weak clue = "likely". Tailwind shows in utility classes, but minified build hides it.
- If page builder (Elementor, Divi) or well-known theme present, say so: explains look + perf.

**Visual design**
- Palette: from most frequent CSS colors + variables (`--primary` etc.), identify primary, secondary, accent, neutrals. Report hex values. Ignore colors from bundled libraries (plugins, widgets), not site's own design.
- Fonts: separate headings vs body if possible, note source (Google Fonts, Adobe Fonts, self-hosted).
- One line on overall style (minimal, corporate, editorial, playful), based on content + visuals, not generic adjectives.

**Target audience**
- Derive from content: who pays (B2B/B2C, industry, typical customer size), who uses it, arrival context. Consider vocabulary, prices, CTAs, language, market.
- One-two sharp sentences beat invented persona list. If signals weak, say so.

### 5. Strengths, weaknesses and fixes
Only use findings from above. Every point needs evidence, every weakness needs fix.

**Strengths:** 3-5 real differentiators (clear value prop, fast/clean stack, solid SEO basics, coherent branding, strong CTAs), not generic praise.

**Weaknesses:** gaps + risks observed, ordered by impact (traffic, conversions, trust, maintainability). Look for: missing/weak SEO elements, accessibility (alt text, contrast, skip links), client-side rendering hiding content from crawlers, heavy page builders or too many third-party scripts, unclear/buried CTAs, missing privacy/cookie handling, inconsistent branding, thin content, missing social proof. Don't pad: two real problems → write two.

**Solutions:** one concrete fix per weakness. Says what to do + with what, tailored to detected stack (WordPress → plugin/setting, Next.js → metadata/rendering option, Webflow → built-in setting). Avoid generic advice ("improve your SEO"). Per fix: effort (low/medium/high) + priority (high/medium/low). Keep realistic for site size + audience. Mark "to verify" any suggestion depending on data you can't see from outside (traffic, conversion rate, real perf scores).

### 6. Write `docs/ANALYSIS.md`
- Create `docs/` folder in working dir if needed.
- If `docs/ANALYSIS.md` exists, rename to `docs/ANALYSIS.prev.md` before writing.
- Use template below. Keep sections, drop rows with no data.

## ANALYSIS.md template

```markdown
# Analysis of <domain>

**URL:** <final url>  
**Analysis date:** <YYYY-MM-DD>  
**In one sentence:** <what the site is and what it offers>

## Structure and SEO

**Main pages:** <home, sections, depth, rough number of pages>

| Element | Status |
|---|---|
| Title | <short text> (<n> chars) |
| Meta description | ok / missing / too long |
| H1 | <text> |
| Canonical / language / viewport | ... |
| Sitemap and robots.txt | ... |
| Structured data and Open Graph | ... |
| Image alt text | <x of y without alt> |

**Worth noting:** <at most 3 points, only the ones that matter>

## Technologies

| Area | Detected | Confidence |
|---|---|---|
| CMS / framework | ... | certain / likely |
| CSS / UI | ... | ... |
| Hosting / CDN | ... | ... |
| Analytics and marketing | ... | ... |
| Other (payments, cookies, etc.) | ... | ... |

**Rendering:** <static, server-side, client-side>. <One line on the impact on SEO and performance if relevant.>

## Visual design

**Palette**

| Role | Color |
|---|---|
| Primary | #xxxxxx |
| Secondary | #xxxxxx |
| Accent | #xxxxxx |
| Background / text | #xxxxxx / #xxxxxx |

**Fonts:** headings <font>, body <font> (<source>)  
**Style:** <one or two lines>

## Target audience

**Audience:** <who, industry, B2B/B2C, market>  
**Tone and proposition:** <how it speaks and what it promises>  
**Main CTAs:** <short list>

## Strengths

- <3-5 points, each with the evidence behind it>

## Weaknesses and how to fix them

| Weakness | Evidence | Proposed fix | Priority | Effort |
|---|---|---|---|---|
| <what is wrong> | <what you saw> | <concrete action, adapted to the detected stack> | high / medium / low | low / medium / high |

## Key takeaways

- <3-5 points: what a hurried reader must take away, including the limits of the analysis>
```

## Style rules for the file

- English, short direct sentences, colleague-over-coffee tone, not press release.
- No em dashes or en dashes: use commas, colons, parentheses.
- No buzzwords or corporate speak ("end-to-end solution", "best-in-class").
- Weaknesses listed with evidence, always paired with fix. Never problem without fix, never fix without problem.
- Every claim rests on something seen. What can't be known from outside (traffic, conversions, backend, exact versions) written as "not detectable".
- If site in another language, report stays English, quoted text left in original.

## Wrapping up

When file ready, reply with two-three sentences: file path + most interesting finding. Don't repeat report content in chat.