from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import unittest

OUT = Path(__file__).resolve().parents[1] / '_site'
class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.ids=[]; self.links=[]; self.tags=[]; self.feed(text)
    def handle_starttag(self, tag, attrs):
        d=dict(attrs); self.tags.append(tag)
        if 'id' in d: self.ids.append(d['id'])
        if 'href' in d: self.links.append(d['href'])
class SiteTests(unittest.TestCase):
    def test_allowlist(self):
        self.assertEqual({p.name for p in OUT.iterdir()}, {'index.html','guidelines.html','checklist.html','style.css','.nojekyll'})
    def test_pages(self):
        for f in OUT.glob('*.html'):
            text=f.read_text(); page=Page(text)
            with self.subTest(page=f.name):
                self.assertIn('<html lang="ja">',text)
                self.assertEqual(page.tags.count('h1'),1)
                self.assertEqual(len(page.ids),len(set(page.ids)))
                self.assertNotIn('script',page.tags)
                self.assertIn('aria-current="page"',text)
                for link in page.links:
                    u=urlsplit(link)
                    if u.scheme: continue
                    target=OUT/unquote(u.path) if u.path else f
                    self.assertTrue(target.is_file(),link)
                    if u.fragment:
                        self.assertIn(unquote(u.fragment),Page(target.read_text()).ids,link)
    def test_markdown_features(self):
        t=(OUT/'guidelines.html').read_text()
        self.assertIn('<table>',t); self.assertIn('<pre><code',t)
        self.assertIn('Before',t)
        self.assertIn('確認項目：',(OUT/'checklist.html').read_text())
if __name__ == '__main__': unittest.main()
