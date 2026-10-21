#!/usr/bin/env python3
"""Validate the bibliography and original PDFs, then render the static site."""
from pathlib import Path
import hashlib
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
escape = html.escape
data = json.loads((ROOT / 'data/publications.json').read_text())
manifest = json.loads((ROOT / 'data/pdf-manifest.json').read_text())
files = {entry['file']: entry for entry in manifest}
for name, entry in files.items():
    content = (ROOT / name).read_bytes()
    assert content.startswith(b'%PDF-'), name
    assert len(content) == entry['bytes'], name
    assert hashlib.sha256(content).hexdigest() == entry['sha256'], name

parts = ['''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Publications — Mahdiar Sadeghi</title>
<meta name="description" content="Publications by Mahdiar Sadeghi, with abstracts and downloadable PDFs: quantitative pharmacology, mathematical modeling, control theory, and electromagnetic sensing.">
<link rel="canonical" href="https://azelys.github.io/publications/">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/style.css">
</head><body>
<a class="skip-link" href="#main">Skip to content</a>
<div class="site-shell">
<header class="site-header">
<a class="site-brand" href="https://mahdiar.org/"><span class="brand-mark">M<span class="brand-dot">.</span></span><span class="brand-name">Mahdiar Sadeghi</span></a>
<nav class="primary-nav" aria-label="Primary navigation"><a href="https://mahdiar.org/">Home</a><a href="https://azelys.github.io/H/en/">Weblog</a><a href="./" aria-current="page">Publications</a></nav>
</header>
<main id="main" tabindex="-1">
<header class="page-heading"><p class="eyebrow">Research · Mahdiar Sadeghi</p><h1>Publications</h1>
<p>Research in quantitative pharmacology, mathematical modeling, control theory, and electromagnetic sensing.</p>
<p><a href="https://scholar.google.com/citations?user=WCOYDvkAAAAJ&amp;hl=en">Google Scholar</a> · <a href="https://orcid.org/0000-0002-8696-0912">ORCID</a> · <a href="https://github.com/azelys/publications">Repository &amp; PDFs</a></p></header>
<nav class="publication-index" aria-label="Publication types">''']
ids = set()
for group in data['groups']:
    assert group['id'] not in ids
    ids.add(group['id'])
    parts.append(f'<a href="#{escape(group["id"])}">{escape(group["title"])}</a>')
parts.append('</nav>')
count = 0
for group in data['groups']:
    parts.append(f'<section class="publication-group" aria-labelledby="{escape(group["id"])}"><h2 id="{escape(group["id"])}">{escape(group["title"])}</h2><ol class="publication-records">')
    for record in group['records']:
        count += 1
        assert record['abstract'] and record['links'], record['title']
        record_id = 'work-' + re.sub(r'[^a-z0-9]+', '-', record['title'].lower()).strip('-')
        assert record_id not in ids, record_id
        ids.add(record_id)
        parts.append(f'<li id="{record_id}"><span class="publication-year">{record["year"]}</span><div><h3>{escape(record["title"])}</h3><p class="publication-authors">{escape(record["authors_text"])}</p><p class="publication-venue">{escape(record["venue"])}</p>')
        links = []
        pdf = record.get('pdf')
        if pdf:
            url = pdf.get('path') or pdf['url']
            if pdf.get('path'):
                assert url in files, url
            links.append(f'<a href="{escape(url, quote=True)}">{escape(pdf["label"])}</a>')
            if pdf.get('path'):
                links.append(f'<a href="{escape(url, quote=True)}" download aria-label="Download PDF: {escape(record["title"], quote=True)}">Download</a>')
        for link in record['links']:
            links.append(f'<a href="{escape(link["url"], quote=True)}">{escape(link["label"])}</a>')
        if record.get('license'):
            license = record['license']
            links.append(f'<a href="{escape(license["url"], quote=True)}" rel="license">{escape(license["label"])}</a>')
        parts.append('<p class="publication-links">' + ' · '.join(links) + '</p>')
        parts.append(f'<details class="publication-abstract"><summary>Abstract<span class="sr-only"> — {escape(record["title"])}</span></summary><div>')
        parts.extend(f'<p>{escape(paragraph)}</p>' for paragraph in record['abstract'])
        parts.append('</div></details></div></li>')
    parts.append('</ol></section>')
parts.append('''</main><footer class="site-footer"><span class="copyright">© 2026 Mahdiar Sadeghi</span></footer></div></body></html>''')
(ROOT / 'index.html').write_text('\n'.join(parts) + '\n')
print(f'Rendered {count} records; verified {len(files)} original PDFs.')
