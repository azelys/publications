# Publications — Mahdiar Sadeghi

Research bibliography, abstracts, and downloadable original PDFs.

- **Website:** https://azelys.github.io/publications/
- **PDF collection:** [pdfs/](pdfs/)
- **Bibliography:** [data/publications.json](data/publications.json)
- **PDF provenance and checksums:** [data/pdf-manifest.json](data/pdf-manifest.json)

## Updating the collection

Add or edit a record in `data/publications.json`. Store an authorized PDF in
`pdfs/` and add its source URL, version, byte size, and SHA-256 checksum to
`data/pdf-manifest.json`. Each record's `pdf.path` points to its local PDF;
`pdf.url` is used for a PDF hosted elsewhere.

Run `python3 scripts/build.py` to verify the original files and regenerate
`index.html`. Push to `main` to publish through GitHub Pages.

## Versions and rights

The bibliography distinguishes journal articles, conference papers, conference
abstracts and posters, preprints, and the dissertation. A preprint PDF is labeled
as a preprint even when a journal version exists.

PDFs are stored unchanged. Copyright and licenses remain with the respective
authors and publishers; this repository does not grant a blanket license to the
papers. Font license information is retained in `fonts/`.

Each publication has one download and one external reference. A GitHub link is
included only when a matching code repository has been identified. Conference
abstract exports are labeled as abstracts rather than full papers or posters.

The collection currently contains 17 records and 23 locally hosted PDF files,
including historical versions in `pdfs/author-archive/` and three abstract
exports in `pdfs/abstracts/`. One article's download links to its author's PDF
server. This is not an exhaustive archive of all works.
