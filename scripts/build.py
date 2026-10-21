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
<link rel="icon" href="assets/favicon.svg?v=m2" type="image/svg+xml">
<link rel="stylesheet" href="assets/style.css">
</head><body>
<a class="skip-link" href="#main">Skip to content</a>
<div class="site-shell">
<header class="site-header">
<a class="site-brand" href="https://mahdiar.org/"><svg class="brand-mark monogram-logo" viewBox="0 0 64 64" aria-hidden="true"><path d="M14 47V24 M14 34C14 20 32 20 32 34V47 M32 34C32 20 50 20 50 34V47" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg><span class="brand-name">Mahdiar Sadeghi</span></a>
<nav class="primary-nav" aria-label="Primary navigation"><a href="https://mahdiar.org/">Home</a><a href="./" aria-current="page">Publications</a></nav>
</header>
<main id="main" tabindex="-1">
<header class="page-heading"><p class="eyebrow">Research · Mahdiar Sadeghi</p><h1>Publications</h1>
<p>Research in quantitative pharmacology, mathematical modeling, control theory, and electromagnetic sensing.</p>
<p><a href="https://scholar.google.com/citations?user=WCOYDvkAAAAJ&amp;hl=en">Google Scholar</a> · <a href="https://orcid.org/0000-0002-8696-0912">ORCID</a></p></header>
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
        assert record['abstract'] and record['reference'] and record['pdf'], record['title']
        record_id = 'work-' + re.sub(r'[^a-z0-9]+', '-', record['title'].lower()).strip('-')
        assert record_id not in ids, record_id
        ids.add(record_id)
        parts.append(f'<li id="{record_id}"><span class="publication-year">{record["year"]}</span><div><h3>{escape(record["title"])}</h3><p class="publication-authors">{escape(record["authors_text"])}</p><p class="publication-venue">{escape(record["venue"])}</p>')
        pdf = record['pdf']
        url = pdf.get('path') or pdf['url']
        download = ''
        if pdf.get('path'):
            assert url in files, url
            download = ' download'
        links = [f'<a href="{escape(url, quote=True)}"{download}>{escape(pdf["label"])}</a>']
        reference = record['reference']
        links.append(f'<a href="{escape(reference["url"], quote=True)}" target="_blank" rel="noopener noreferrer">{escape(reference["label"])}</a>')
        if record.get('code'):
            code = record['code']
            assert code['url'] != reference['url']
            links.append(f'<a href="{escape(code["url"], quote=True)}" target="_blank" rel="noopener noreferrer">{escape(code["label"])}</a>')
        assert len(links) == (3 if record.get('code') else 2)
        parts.append('<p class="publication-links">' + ' · '.join(links) + '</p>')
        parts.append(f'<details class="publication-abstract"><summary>Abstract<span class="sr-only"> — {escape(record["title"])}</span></summary><div>')
        parts.extend(f'<p>{escape(paragraph)}</p>' for paragraph in record['abstract'])
        parts.append('</div></details></div></li>')
    parts.append('</ol></section>')
parts.append('''</main><footer class="site-footer"><span class="copyright">© 2026 Mahdiar Sadeghi</span></footer></div></body></html>''')
(ROOT / 'index.html').write_text('\n'.join(parts) + '\n')
print(f'Rendered {count} records; verified {len(files)} PDF files.')
