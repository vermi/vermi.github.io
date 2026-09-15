"""Generate the Canvas course home page (Tech Blue theme) and push it as a page.

Usage:
  python3 course_home.py fall            # render to out/course-home-fall.html
  python3 course_home.py spring --push   # render and create/update "Course Home (Draft)" in Canvas

Everything term-specific lives in COURSES. The page is static for the whole term;
students get live due dates from Canvas's own To Do list and Calendar.
"""
import argparse, json, os, urllib.request
from datetime import date, timedelta
from html import escape as e

HOST = 'https://nmt.instructure.com'
TOKEN = os.path.expanduser('~/.stuff/CANVAS_TOKEN')

SHARED = {
    'code': 'CYBS 0189 & 0189L',
    'meets': 'Mon–Thu, 2:00–2:50 PM, live on Zoom',
    'zoom': 'https://nmt-edu.zoom.us/j/3736260872',
    'site': 'https://lockboxsecurity.net/academic/applied/',
    'instructor': 'Justin Vermillion',
    'email': 'justin.vermillion@student.nmt.edu',
    'office_hours': 'Tue & Thu, 7:00–8:00 PM on Zoom, or by appointment',
    'email_rule': 'Put CYBS 0189 and your section in every email subject. High school students: CC your local instructor. Replies within 48 hours on business days.',
    'help': [
        ('Canvas or Zoom trouble', 'NMT IT Help Desk', None),
        ('Accommodations', 'Office for Student Access Services', 'https://nmt.edu/ds/for_students.php'),
        ('Tutoring and writing help', 'Office of Student Learning', 'https://www.nmt.edu/osl/'),
        ('Counseling, incl. 24/7 crisis line', 'Counseling and Disability Services', 'https://www.nmt.edu/cds/'),
    ],
}

COURSES = {
    'fall': {
        'canvas_id': 42477,
        'title': 'Applied Cybersecurity I',
        'term': 'Fall 2026',
        'tagline': 'Foundations of information security, with preparation for CompTIA Security+ (SY0-701).',
        'week1_monday': date(2026, 8, 17),
        # (module number, title, weeks after week 1); breaks are gaps in the offsets
        'modules': [
            (1, "Today's Security Professional", 0), (2, 'Cybersecurity Threat Landscape', 1), (3, 'Malicious Code', 2),
            (4, 'Social Engineering and Password Attacks', 3), (5, 'Security Assessment and Testing', 4),
            (6, 'Application Security', 5), (7, 'Cryptography and the PKI', 6), (8, 'Midterm Review and Exam', 7),
            (9, 'Resilience and Physical Security', 8), (10, 'Cloud and Virtualization Security', 9),
            (11, 'Endpoint Security', 10), (12, 'Network Security', 11), (13, 'Wireless and Mobile Security', 12),
            (14, 'Security Architecture and Design', 13), (15, 'Course Review', 15), (16, 'Final Exam', 16),
        ],
        'breaks': [('Thanksgiving Break', date(2026, 11, 23), date(2026, 11, 27))],
        'steps': [
            ('Read', 'Start the chapter listed at the top of the module.'),
            ('Attend', 'Join lecture and lab live on Zoom, Mon–Thu. Slides are posted in every module.'),
            ('Lab', 'Complete the module’s ACI Skill Labs and LEXX labs.'),
            ('Quiz', 'Take the module quiz. Unless noted, work is due Sunday at 11:59 PM.'),
        ],
    },
    'spring': {
        'canvas_id': 43904,
        'title': 'Applied Cybersecurity II',
        'term': 'Spring 2027',
        'tagline': 'Security operations, incident response, and security program management, continuing preparation for CompTIA Security+ (SY0-701).',
        'week1_monday': date(2027, 1, 18),  # MLK Day; classes begin Tue Jan 19
        'modules': [
            (1, 'Identity and Access Management I', 0), (2, 'Identity and Access Management II', 1),
            (3, 'Monitoring and Incident Response', 2), (4, 'Digital Forensics', 3),
            (5, 'Security Governance and Compliance', 4), (6, 'Risk Management and Privacy', 5),
            (7, 'Social Engineering and the Psychology of Security', 6), (8, 'Midterm Review and Exam', 7),
            (9, 'Cybersecurity Ethics', 9), (10, 'Cybersecurity Law', 10),
            (11, 'Malware Analysis and Reverse Engineering', 11), (12, 'Securing LLMs', 12),
            (13, 'Using LLMs for Security', 13), (14, 'Comprehensive Security+ Review Part 1', 14),
            (15, 'Comprehensive Security+ Review Part 2 and Final Exam', 15),
        ],
        'breaks': [('Spring Break', date(2027, 3, 15), date(2027, 3, 19))],
        'steps': [
            ('Read', 'Start the reading listed at the top of the module.'),
            ('Attend', 'Join lecture and lab live on Zoom, Mon–Thu. Slides are posted in modules that have them.'),
            ('Practice', 'Complete the module’s labs and activities.'),
            ('Quiz', 'Take the module quiz when one is assigned. Unless noted, work is due Sunday at 11:59 PM.'),
        ],
    },
}

# Tech Blue palette
NAVY, NAVY2, TEXT, MUTED, SILVER, PALE, LINK, HAIR = '#0b2f5b', '#123e73', '#1f2933', '#5a6776', '#c5ccd6', '#eef2f7', '#0b57a4', '#e3e7ed'


def token():
    return open(TOKEN).readline().strip()


def api(method, path, data=None):
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(HOST + '/api/v1' + path, data=body, method=method,
                                 headers={'Authorization': 'Bearer ' + token(), 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def span(d0, d1):
    return f"{d0:%b %-d}–{d1:%-d}" if d0.month == d1.month else f"{d0:%b %-d}–{d1:%b %-d}"


def render(c):
    cid = c['canvas_id']
    mod_ids = {int(m['name'].split(':')[0].split()[1]): m['id'] for m in api('GET', f'/courses/{cid}/modules?per_page=100') if m['name'].startswith('Module ')}
    modules_url = f'{HOST}/courses/{cid}/modules'
    calendar_url = f'{HOST}/calendar'
    links = [
        ('Syllabus', 'Policies, grading, schedule', f'{HOST}/courses/{cid}/assignments/syllabus'),
        ('Modules', 'Every week, in order', modules_url),
        ('Grades', 'Check your progress', f'{HOST}/courses/{cid}/grades'),
        ('Calendar', 'All due dates', calendar_url),
        ('Course website', 'Interactive slides', c['site']),
        ('Office hours', 'Tue & Thu, 7–8 PM', c['zoom']),
    ]
    h2 = lambda t: f'<h2 style="margin: 0 0 14px 0; font-size: 21px; color: {NAVY}; padding-bottom: 8px; border-bottom: 2px solid {SILVER};">{e(t)}</h2>'

    band = (f'<div style="background: {NAVY}; border-radius: 6px; padding: 28px 30px;">'
            f'<p style="margin: 0 0 6px 0; font-size: 14px; color: #b9c9de;">{e(c["code"])} · {e(c["term"])} · New Mexico Tech</p>'
            f'<h1 style="margin: 0 0 8px 0; font-size: 34px; line-height: 1.15; color: #ffffff;">{e(c["title"])}</h1>'
            f'<p style="margin: 0 0 20px 0; font-size: 16px; color: #d6e0ec; max-width: 640px;">{e(c["tagline"])}</p>'
            f'<div style="display: flex; flex-wrap: wrap; gap: 10px; align-items: center;">'
            f'<a href="{e(c["zoom"])}" style="text-decoration: none; background: #ffffff; color: {NAVY}; font-weight: bold; padding: 10px 20px; border-radius: 4px;">Join class on Zoom</a>'
            f'<a href="{modules_url}" style="text-decoration: none; border: 1px solid #8fa9c9; color: #ffffff; font-weight: bold; padding: 9px 19px; border-radius: 4px;">View modules</a>'
            f'<span style="color: #b9c9de; font-size: 14px;">{e(c["meets"])}</span></div></div>')

    steps = ''.join(
        f'<div style="flex: 1 1 160px; min-width: 150px; padding: 4px 0;">'
        f'<p style="margin: 0 0 6px 0;"><span style="display: inline-block; width: 30px; height: 30px; line-height: 30px; text-align: center; border-radius: 999px; background: {NAVY2}; color: #ffffff; font-weight: bold;">{i}</span>'
        f' <strong style="color: {NAVY}; font-size: 17px; vertical-align: middle;">{e(h)}</strong></p><p style="margin: 0; font-size: 14px;">{e(b)}</p></div>'
        for i, (h, b) in enumerate(c['steps'], 1))
    week = (f'<div>{h2("How each week works")}<div style="display: flex; flex-wrap: wrap; gap: 20px;">{steps}</div>'
            f'<p style="margin: 16px 0 0 0; background: {PALE}; padding: 12px 16px; border-radius: 4px;"><strong style="color: {NAVY};">Looking for due dates?</strong> '
            f'Check your To Do list on the right side of this page (or the To Do tab in the Canvas Student app) and the <a href="{calendar_url}" style="color: {LINK};">Calendar</a>.</p></div>')

    tiles = ''.join(
        f'<a href="{e(h)}" style="flex: 1 1 28%; min-width: 150px; text-decoration: none; background: #ffffff; border: 1px solid {SILVER}; border-radius: 6px; padding: 14px 16px;">'
        f'<span style="display: block; font-weight: bold; color: {LINK};">{e(t)}</span><span style="display: block; font-size: 13px; color: {MUTED};">{e(s)}</span></a>'
        for t, s, h in links)
    quick = f'<div>{h2("Quick links")}<div style="display: flex; flex-wrap: wrap; gap: 10px;">{tiles}</div></div>'

    road, pending = '', list(c['breaks'])
    for n, title, off in c['modules']:
        start = c['week1_monday'] + timedelta(weeks=off)
        for b in list(pending):
            if b[1] < start:
                road += f'<tr><td colspan="3" style="padding: 8px 12px; background: {PALE}; color: {NAVY}; font-weight: bold;">{e(b[0])} · {span(b[1], b[2])}</td></tr>'
                pending.remove(b)
        href = f'{modules_url}#module_{mod_ids[n]}' if n in mod_ids else modules_url
        road += (f'<tr><td style="padding: 8px 12px; border-bottom: 1px solid {HAIR}; color: {MUTED}; white-space: nowrap; width: 90px;">Module {n}</td>'
                 f'<td style="padding: 8px 12px; border-bottom: 1px solid {HAIR};"><a href="{e(href)}" style="color: {LINK}; text-decoration: none;">{e(title)}</a></td>'
                 f'<td style="padding: 8px 12px; border-bottom: 1px solid {HAIR}; text-align: right; color: {MUTED}; white-space: nowrap;">{span(start, start + timedelta(days=6))}</td></tr>')
    roadmap = f'<div>{h2("Course schedule")}<div style="overflow-x: auto;"><table style="width: 100%; border-collapse: collapse; font-size: 15px;">{road}</table></div></div>'

    helps = ''.join(f'<li style="margin-bottom: 4px;">{e(a)}: ' + (f'<a href="{e(u)}" style="color: {LINK};">{e(b)}</a>' if u else e(b)) + '</li>' for a, b, u in c['help'])
    people = (f'<div style="display: flex; flex-wrap: wrap; gap: 28px;">'
              f'<div style="flex: 1 1 280px;">{h2("Instructor")}<p style="margin: 0 0 4px 0; font-size: 17px; font-weight: bold; color: {NAVY};">{e(c["instructor"])}</p>'
              f'<p style="margin: 0 0 10px 0;"><a href="mailto:{e(c["email"])}" style="color: {LINK};">{e(c["email"])}</a><br>{e(c["office_hours"])}</p>'
              f'<p style="margin: 0; font-size: 13px; color: {MUTED};">{e(c["email_rule"])}</p></div>'
              f'<div style="flex: 1 1 280px;">{h2("Student support")}<ul style="margin: 0; padding-left: 18px;">{helps}</ul></div></div>')

    gap = '<div style="height: 30px;"></div>'
    return f'<div style="max-width: 980px; margin: 0 auto; color: {TEXT}; line-height: 1.5;">' + gap.join([band, week, quick, roadmap, people]) + '</div>'


def push(c, html, title='Course Home (Draft)'):
    cid = c['canvas_id']
    existing = {p['title']: p['url'] for p in api('GET', f'/courses/{cid}/pages?per_page=100')}
    payload = {'wiki_page': {'title': title, 'body': html, 'editing_roles': 'teachers'}}
    if title in existing:
        return api('PUT', f'/courses/{cid}/pages/{existing[title]}', payload)
    payload['wiki_page']['published'] = False
    return api('POST', f'/courses/{cid}/pages', payload)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('term', choices=COURSES)
    ap.add_argument('--push', action='store_true', help='create or update the "Course Home (Draft)" page in Canvas')
    args = ap.parse_args()
    course = {**SHARED, **COURSES[args.term]}
    html = render(course)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', f'course-home-{args.term}.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w').write(html)
    print('wrote', out, len(html), 'bytes')
    if args.push:
        p = push(course, html)
        print('page', p['html_url'], 'published' if p['published'] else 'unpublished', '| front page' if p['front_page'] else '')
