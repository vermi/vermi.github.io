"""Mirror a site syllabus (Tailwind HTML) into a Canvas course's Syllabus page, Tech Blue styling.

Usage: python3 syllabus_to_canvas.py fall|spring [--push]
The site syllabus stays the source of truth; rerun after editing it.
"""
import argparse, json, os, re, urllib.request
from html import escape
from html.parser import HTMLParser

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # academic/applied
SITE = 'https://lockboxsecurity.net/academic/applied'
TERMS = {'fall': (42477, 'fall-syllabus.html'), 'spring': (43904, 'spring-syllabus.html')}

NAVY, NAVY2, TEXT, MUTED, SILVER, PALE, LINK = '#0b2f5b', '#123e73', '#1f2933', '#5a6776', '#c5ccd6', '#eef2f7', '#0b57a4'
VOID = {'br', 'hr', 'img'}


class Converter(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.stack, self.in_body, self.skip = [], [], False, 0

    def emit(self, s):
        self.out.append(s)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get('class', '')
        if tag == 'body':
            self.in_body = True; return
        if not self.in_body or tag in ('script', 'style'):
            self.skip += tag in ('script', 'style'); self.stack.append(''); return
        close = f'</{tag}>'
        if tag == 'header':
            open_ = f'<div style="background: {NAVY}; border-radius: 6px; padding: 26px 28px; margin-bottom: 26px;">'; close = '</div>'
        elif tag == 'h1':
            open_ = '<h1 style="margin: 0 0 6px 0; font-size: 30px; line-height: 1.2; color: #ffffff;">'
        elif tag == 'p' and self.parent_is('header'):
            open_ = '<p style="margin: 0; font-size: 16px; color: #d6e0ec;">'
        elif tag == 'section':
            box = 'bg-gray-100' in cls
            open_ = (f'<div style="margin: 0 0 30px 0; background: {PALE}; border-radius: 6px; padding: 18px 22px;">' if box
                     else '<div style="margin: 0 0 30px 0;">'); close = '</div>'
        elif tag == 'h2':
            open_ = f'<h2 style="margin: 0 0 14px 0; font-size: 22px; color: {NAVY}; padding-bottom: 8px; border-bottom: 2px solid {SILVER};">'
        elif tag == 'h3':
            week = 'text-xl' in cls
            open_ = (f'<h3 style="margin: 0 0 8px 0; font-size: 18px; color: {NAVY2};">' if week
                     else f'<h3 style="margin: 12px 0 8px 0; font-size: 16px; color: {NAVY};">')
        elif tag == 'div' and 'grid' in cls:
            open_ = '<div style="display: flex; flex-wrap: wrap; gap: 8px 32px;">'; close = '</div>'
        elif tag == 'div' and 'border' in cls:
            open_ = f'<div style="border: 1px solid {SILVER}; border-radius: 6px; padding: 14px 18px; margin: 0 0 12px 0;">'; close = '</div>'
        elif tag == 'div' and self.parent_is_grid():
            open_ = '<div style="flex: 1 1 280px; min-width: 240px;">'; close = '</div>'
        elif tag == 'div' or tag == 'main':
            open_ = '<div>'; close = '</div>'
        elif tag == 'p' and 'text-sm' in cls:
            open_ = f'<p style="margin: 8px 0 0 0; display: inline-block; background: {PALE}; color: {NAVY}; font-weight: bold; font-size: 14px; padding: 4px 10px; border-radius: 4px;">'
        elif tag == 'p':
            open_ = f'<p style="margin: 0 0 8px 0; color: {TEXT};">'
        elif tag in ('ul', 'ol'):
            none = 'list-none' in cls
            open_ = f'<{tag} style="margin: 6px 0 10px 0; padding-left: {"0" if none else "22px"};{" list-style: none;" if none else ""}">'
        elif tag == 'li':
            open_ = f'<li style="margin: 0 0 4px 0; color: {TEXT};">'
        elif tag == 'a':
            href = a.get('href', '#')
            open_ = f'<a href="{escape(href)}" style="color: {LINK};"' + (' target="_blank" rel="noopener"' if href.startswith('http') else '') + '>'
        elif tag in ('strong', 'b', 'em', 'i', 'code', 'br', 'hr'):
            open_ = f'<{tag}>'
        else:
            open_, close = '', ''
        self.emit(open_)
        self.stack.append((tag, cls, close) if tag not in VOID else None)
        if tag in VOID:
            self.stack.pop()

    def parent_is(self, tag):
        return any(isinstance(s, tuple) and s[0] == tag for s in self.stack)

    def parent_is_grid(self):
        for s in reversed(self.stack):
            if isinstance(s, tuple) and s[0] == 'div':
                return 'grid' in s[1]
        return False

    def handle_endtag(self, tag):
        if tag == 'body' or not self.stack:
            return
        item = self.stack.pop()
        if item == '':
            if tag in ('script', 'style'): self.skip -= 1
            return
        if item:
            self.emit(item[2])

    def handle_data(self, data):
        if self.in_body and not self.skip:
            self.emit(escape(re.sub(r'\s+', ' ', data), quote=False))


def convert(src):
    # empty "Important:" labels in the schedule carry no information
    src = re.sub(r'<p class="[^"]*">\s*🎯 Important:\s*</p>', '', src)
    c = Converter(); c.feed(src)
    body = re.sub(r'>\s+<', '> <', ''.join(c.out)).strip()
    return body


def render(term):
    cid, fname = TERMS[term]
    body = convert(open(os.path.join(REPO, fname)).read())
    note = (f'<p style="margin: 0 0 18px 0; font-size: 14px; color: {MUTED};">This page mirrors the official course syllabus at '
            f'<a href="{SITE}/{fname}" target="_blank" rel="noopener" style="color: {LINK};">lockboxsecurity.net</a>. If the two ever differ, the website version is authoritative.</p>')
    return f'<div style="max-width: 900px; line-height: 1.55; color: {TEXT};">{note}{body}</div>'


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('term', choices=TERMS)
    ap.add_argument('--push', action='store_true')
    args = ap.parse_args()
    html = render(args.term)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', f'syllabus-{args.term}.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w').write(html)
    print('wrote', out, len(html), 'bytes')
    if args.push:
        cid = TERMS[args.term][0]
        tok = open(os.path.expanduser('~/.stuff/CANVAS_TOKEN')).readline().strip()
        req = urllib.request.Request(f'https://nmt.instructure.com/api/v1/courses/{cid}?include[]=syllabus_body',
                                     data=json.dumps({'course': {'syllabus_body': html}}).encode(), method='PUT',
                                     headers={'Authorization': 'Bearer ' + tok, 'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as r:
            c = json.load(r)
        print('pushed to course', cid, 'syllabus_body', len(c.get('syllabus_body') or ''), 'bytes')
