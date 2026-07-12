# Résumé Studio — Premium ATS Resume Builder (Streamlit)

A resume builder with a premium "ink & brass" visual identity:
- Hero section with a wax-seal monogram logo and an editorial hero graphic
- 3 resume tiers — **Simple (5 templates) / Professional (5 templates) /
  Premium (9 templates)** — 19 templates total. Pick a tier; the app
  randomly selects one of its templates each time you generate.
- Two ways to start: **upload an existing resume** (auto-parsed into an
  editable form) or **fill in manually**
- One-click **ATS Score Check** (0–100) shown as a brass gauge, with a
  criterion-by-criterion breakdown

## Design system
"Ink & brass": deep navy/ink grounds (`#0B0F1A`, `#12203D`), warm brass-gold
accents (`#C49B4A`), an ivory "paper" background for the form (`#F7F3EA`),
Lora (serif) for headings paired with Poppins (sans) for body/UI text. The
palette and wax-seal/document motifs are chosen because the product itself
is a resume/document tool — the visual language leans on stationery, foil
stamping, and letterpress typography rather than a generic tech gradient.

## Files
- `app.py` — Streamlit UI: hero section, tier picker, form, generate, ATS
  score gauge, and all custom CSS
- `resume_builder.py` — the template engine (`python-docx`), 19 templates
  across 3 tiers, all single-column and ATS-safe (no tables/images/text
  boxes in the generated resume itself)
- `resume_parser.py` — heuristic parser for uploaded resumes (pdf/docx)
- `ats_scorer.py` — heuristic ATS-friendliness scoring (see note below)
- `generate_assets.py` — regenerates `logo.png` and `hero.png` if you ever
  want new placeholders
- `logo.png`, `hero.png` — hero section brand images (replace with your own
  — same filenames)
- `requirements.txt` — dependencies

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
Open the local URL Streamlit prints (usually http://localhost:8501).

## Deploy on Streamlit Community Cloud
1. Push this whole folder (including `logo.png` and `hero.png`) to a
   GitHub repo.
2. Go to https://share.streamlit.io → **New app**.
3. Point it at your repo/branch, main file `app.py`.
4. Deploy — Streamlit installs `requirements.txt` automatically.

## Branding
Replace `logo.png` with your real logo and `hero.png` with your own hero
image any time — just keep the same filenames (any reasonable resolution
works; the CSS scales them). Run `python3 generate_assets.py` if you want
to regenerate the placeholder wax-seal logo / document hero graphic.

## Customizing templates
Each of the 19 templates is a small dict in `TEMPLATES` inside
`resume_builder.py` (colors, fonts, header style). Add, remove, or restyle
templates by editing that dict — no need to touch the rendering logic. To
add a whole new tier or header treatment, extend `ResumeBuilder.add_header`
in the same file.

## Customizing the app's look
All UI styling lives in `inject_global_css()` and `render_hero()` near the
top of `app.py` — colors are defined as constants (`INK`, `NAVY`, `BRASS`,
`PAPER`, etc.) at the top of the file, so re-theming is a matter of editing
those hex values in one place.

## About the ATS score
There is no public API for "the" ATS score — every company's applicant
tracking system parses differently. `ats_scorer.py` instead checks the
things that are consistently known to matter across systems: parseable
contact info, standard section headings, bullet-based experience with a
sane bullet count, quantified achievements, action verbs, adequate content
length, and a single-column/table-free/image-free format (guaranteed by
the generator itself). Treat the score as directional coaching, not a
guarantee any specific employer's ATS will score it identically.
