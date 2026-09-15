# Canvas page generators

Scripts that build the Canvas-side pages for CYBS 0189 from this site, so both semesters share one look (Tech Blue) and the Canvas copies never drift from the website.

Both read the Canvas API token from `~/.stuff/CANVAS_TOKEN` (never commit a token) and write rendered HTML to `out/` (git-ignored).

| Script | What it does |
| --- | --- |
| `course_home.py fall\|spring [--push]` | Renders the course home page from the settings in `COURSES`. `--push` creates or updates the course's "Course Home (Draft)" page. |
| `syllabus_to_canvas.py fall\|spring [--push]` | Converts `../fall-syllabus.html` or `../spring-syllabus.html` into Canvas-safe HTML. `--push` replaces the course's built-in Syllabus page. |

## New term checklist

1. Update the syllabus HTML on the site, then run `python3 syllabus_to_canvas.py <term> --push`.
2. In `course_home.py`, copy the previous term's `COURSES` entry and change the Canvas course ID, term, week 1 Monday, modules, and breaks. Then run `python3 course_home.py <term> --push`.
3. In Canvas, publish the page and set it as the front page (Pages → ⋮ → Use as Front Page), then set the course Home to "Pages Front Page".

Canvas strips `<style>`, scripts, shadows, letter-spacing, uppercase transforms and opacity from pages, so everything here uses inline styles with flexbox.
