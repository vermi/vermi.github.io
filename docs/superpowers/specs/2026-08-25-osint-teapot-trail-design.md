# The Teapot Trail — OSINT Mini-Lab Design

**Course:** CYBS 0189, Applied Cybersecurity I (bonus module)
**Replaces:** the PYPL/VS Code chain in `academic/applied/slides/osint.html`
**Date:** 2026-08-25

## Why the old lab was replaced

The original three-stage lab anchored Stage 1 on the PYPL IDE popularity index — a
live leaderboard that reshuffles monthly. Its answer key said "VS Code is #2."
As of August 2026 PYPL ranks Cursor #2 and VS Code #5, and because Cursor is
closed-source the Stage 2 instruction ("find its open source project") dead-ends.
Stage 2 was independently stale: VS Code published no iteration plan issues after
March 2026, so "the current sprint planner" had no answer. Only Stage 3 (an IANA
registry record) still resolved.

**Root cause:** every stage chained off volatile live data. The replacement anchors
only on append-only or archived sources.

## Constraints

- All tooling browser-based. No installs, no CLI.
- Solvable by a novice high-school-level student.
- 15–20 minutes total, ~5 minutes per stage.
- Four students, working individually. No team framing.
- Keep the existing click-to-reveal clue buttons.

## The chain

Hook: a server replies `418 I'm a teapot`. Real standard, or a joke?

### Stage 1 — Frozen registries
Find the body that officially assigns HTTP status codes, and what it says about 418.

- Start: <https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml>
- **Flag 1: `(Unused)`**
- Bridge: the Reference column cites RFC 9110 §15.5.19, which states 418 "has been
  deployed as a joke often enough for the code to be unusable for any future use,"
  and points to RFC 2324 (1 April 1998, author L. Masinter).

### Stage 2 — Wayback Machine
RFC 2324 §10 "Author's Address" lists `masinter@parc.xerox.com`. That domain no
longer resolves, so the archive is the only way to view it.

- Start: <https://www.rfc-editor.org/rfc/rfc2324.txt> → §10
- Pinned snapshot: <http://web.archive.org/web/20041231090129/http://www.parc.xerox.com/>
- **Flag 2: `Palo Alto Research Center`**
- Lesson: the organization, the domain, and the site are all gone; the content is
  still readable. Deleting does not delete.

### Stage 3 — Document metadata
Masinter's own site hosts his talk on the history of HTTP. Inspect its properties.

- Target: <https://larrymasinter.net/071203-HTTPbis.pdf>
- Backup: Wayback mirror, snapshot 2024-03-15
- Verified metadata:
  - Title: `HTTP: how we got here and where we should go`
  - Author: `Larry Masinter`
  - Creator: `Acrobat PDFMaker 8.1 for PowerPoint`
  - Producer: `Acrobat Distiller 8.1.0 (Windows)`
  - Created: 2007-12-03
- **Flag 3: `Acrobat Distiller 8.1.0 (Windows)`**
- Payoff: the file was built from a PowerPoint, names the operating system, and
  carries a 2007 version number that is one search away from a published CVE list.
  This is version disclosure, tying directly to the reconnaissance objectives.

## Tooling

| Stage | Tool | Notes |
|-------|------|-------|
| 1 | iana.org | Plain web page |
| 2 | rfc-editor.org, web.archive.org | Plain web pages |
| 3 | extractmetadata.com | Accepts a remote URL; no download/upload step |

Stage 3 documents two independent paths, deliberately:

1. **Primary (browser-agnostic):** <https://extractmetadata.com/> — paste the PDF
   URL into the "Or enter a URL:" field. Works in any browser.
2. **Fallback (no third party):** Firefox's built-in PDF viewer → Document
   Properties. Chrome and Edge have no Document Properties dialog at all, so
   Firefox is the only native-browser option.

Two paths because a third-party tool going offline is exactly the failure mode that
killed the previous version of this lab. Either path can die without breaking Stage 3.

**Unverified:** extractmetadata.com renders results via JavaScript polling, so its
output could not be confirmed from the command line — only that it is reachable,
exposes a `userfile_url` field, and lists PDF support. Click through it once with
the Stage 3 URL before teaching.

## Durability

IANA registries and RFCs are append-only and never rewritten. Wayback snapshots are
immutable. Stage 3 has an archived mirror if `larrymasinter.net` goes offline. No
stage depends on a ranking, a search result, or an active project's current state.

## Ethics posture

The chain terminates on a software version string rather than an individual's
contact details. Every artifact used is a published professional record — a
standards document, a defunct corporate homepage, a conference talk the author put
online himself. Pairs with the existing ethics module.

## Instructor notes

- **Do not let students search Wayback for `parc.xerox.com` unaided.** The
  2001-03-04 snapshot is polluted: it archived a page reading "Family.com:
  Styrofoam Fish." Pin the 2004-12-31 URL in the slide. Optionally surface the bad
  snapshot afterward as a discussion of source verification.
- At ~5 minutes per stage, give each stage its exact starting URL. This is a
  guided trail, not open-ended searching.
- RFC 2324 also cites the Carnegie Mellon coke machine history at
  `cse.ucsd.edu/users/bsy/coke.history.txt` — usable as a bonus thread.

## Deliverable

One self-contained file: `academic/applied/slides/osint.html`. Same structural
pattern as the existing decks (Tailwind CDN, dark theme, keyboard-navigable slides,
click-to-reveal clues). Replaces the current file. Deploys to `jump_host:~/public_html`
via the existing rsync path.
