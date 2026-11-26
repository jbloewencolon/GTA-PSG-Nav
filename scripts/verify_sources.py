#!/usr/bin/env python3
"""Check that every provision's quoted text appears word for word in its document's source text.

Run: python3 scripts/verify_sources.py data/stage1_inventory.json data/source_text
Source text files are named <doc_id>.txt (made with `pdftotext -layout <pdf> <doc_id>.txt`).
Before comparing, the check removes only what PDF printing adds: browser print headers and
footers, line breaks, and a line break after a hyphen ("AI-<newline>generated"). Wording,
punctuation and quotation marks must match exactly.
Exits 1 if any excerpt is missing from a document that has source text. Documents without
a source text file are listed, not failed.
"""
import json, os, re, sys

INV, SRC = sys.argv[1], sys.argv[2]
inv = json.load(open(INV, encoding='utf-8'))
HEADER = re.compile(r'^\f?\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2} [AP]M\s{2,}.*$', re.M)   # browser print header: date, time, page title
FOOTER = re.compile(r'^\f?https?://\S+\s+\d+/\d+\s*$', re.M)                              # browser print footer: URL, page n/N


def norm(t):
    return re.sub(r'\s+', ' ', t).strip()


def source(doc_id):
    path = os.path.join(SRC, doc_id + '.txt')
    if not os.path.exists(path): return None
    t = open(path, encoding='utf-8').read()
    t = FOOTER.sub('', HEADER.sub('', t))
    t = re.sub(r'(?<=\w)-[ \t]*\n\s*(?=\w)', '-', t)   # rejoin words broken after a hyphen
    return norm(t)


bad, no_text = [], []
for d in inv['documents']:
    s = source(d['doc_id'])
    provs = [p for p in inv['provisions'] if p['doc_id'] == d['doc_id']]
    if s is None:
        no_text.append(d['doc_id']); print(f"{d['doc_id']}: no source text ({len(provs)} provisions not checked)"); continue
    miss = [(p['id'], part) for p in provs for part in ('text_excerpt', 'lead_in_excerpt') if p[part] and norm(p[part]) not in s]
    bad += miss
    print(f"{d['doc_id']}: {len(provs)} provisions, {len(miss)} excerpts not found")
    for i, part in miss[:20]: print(f"  MISSING {i} {part}")
checked = len(inv['documents']) - len(no_text)
print(f"checked {checked} of {len(inv['documents'])} documents; {len(bad)} missing excerpts; without source text: {', '.join(no_text) or 'none'}")
sys.exit(1 if bad else 0)
