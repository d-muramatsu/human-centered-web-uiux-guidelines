"""Build only the three explicitly selected documents; never publish the repo root."""
from pathlib import Path
import html
import re
import shutil
import markdown

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_site'
PAGES = {'README.md': ('index.html', 'はじめに'), 'GUIDELINES.md': ('guidelines.html', 'ガイドライン'), 'REVIEW-CHECKLIST.md': ('checklist.html', 'チェックリスト')}

def build():
    OUT.mkdir(exist_ok=True)
    for filename, (dest, label) in PAGES.items():
        md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'], extension_configs={'toc': {'toc_depth': '2-3'}})
        body = md.convert((ROOT / filename).read_text(encoding='utf-8'))
        for source, (target, _) in PAGES.items():
            body = body.replace(f'href="{source}"', f'href="{target}"')
        # Markdown checkboxes are intentionally static: no state or storage.
        body = re.sub(r'\[ \]', '<span aria-hidden="true">☐</span><span class="sr-only">確認項目：</span>', body)
        nav = ''.join(f'<a href="{target}"'+ (' aria-current="page"' if target == dest else '') + f'>{name}</a>' for target, name in PAGES.values())
        toc = '<aside aria-label="ページ内目次"><h2>このページの目次</h2>'+md.toc+'</aside>' if filename != 'README.md' else ''
        page = f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light"><title>{html.escape(label)} | Web UI/UX ガイドライン</title><meta name="description" content="画一的なAI臭さを減らし、利用者と目的に根ざしたWeb UI/UXを作る実践ガイド。"><link rel="stylesheet" href="style.css"></head>
<body><a class="skip" href="#content">本文へ移動</a><header><a class="brand" href="index.html">Web UI/UX ガイドライン</a><nav aria-label="主なページ">{nav}</nav></header><div class="layout">{toc}<main id="content">{body}</main></div><footer><p>Markdownを正本として自動生成。チェック欄は印刷・レビュー用の静的表示です。</p><a href="https://github.com/d-muramatsu/human-centered-web-uiux-guidelines">GitHubで原文を見る</a></footer></body></html>'''
        (OUT / dest).write_text(page, encoding='utf-8')
    shutil.copyfile(ROOT / 'site/style.css', OUT / 'style.css')
    (OUT / '.nojekyll').touch()

if __name__ == '__main__':
    build()
