"""
Premium ATS Resume Builder — Streamlit app
--------------------------------------------
Design language: "ink & brass" — deep navy/ink grounds, warm brass-gold
accents, a serif display face (Lora) for headings paired with Poppins for
body/UI text. Matches the wax-seal logo and editorial hero graphic in
logo.png / hero.png.

Features:
- Hero section: logo (left) + title/tagline + hero image (right)
- Choose a resume tier: Simple / Professional / Premium
    -> app randomly picks one of that tier's templates at generation time
    (Premium currently has 9 template variants; Simple/Professional have 5 each)
- Fill the resume manually OR upload an existing resume to auto-fill the form
- Generate a polished, ATS-friendly .docx and download it
- Check the ATS-friendliness score of the generated resume (0-100), shown
  as a brass gauge with a criterion-by-criterion breakdown

Run locally:
    streamlit run app.py

Deploy on Streamlit Community Cloud:
    1. Push this whole folder (app.py, resume_builder.py, resume_parser.py,
       ats_scorer.py, requirements.txt, logo.png, hero.png) to a GitHub repo.
    2. On share.streamlit.io, create a new app pointing at app.py.

Branding:
    Replace logo.png and hero.png with your own files any time — same
    filenames, any reasonable resolution. Re-run generate_assets.py if you
    ever want to regenerate the placeholders.
"""

import base64
import io
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from resume_builder import build_resume, TEMPLATES, pick_random_template
from resume_parser import parse_resume
from ats_scorer import score_resume
import auth

st.set_page_config(page_title="Résumé Studio — Premium ATS Resume Builder", page_icon="🖋️", layout="wide")

# Login/signup gate — nothing below this runs until someone is logged in.
if not auth.require_login():
    st.stop()

APP_DIR = os.path.dirname(__file__)


def _first_existing(*candidates):
    for c in candidates:
        if os.path.exists(c):
            return c
    return candidates[0]


LOGO_PATH = _first_existing(os.path.join(APP_DIR, "logo.png"), os.path.join(APP_DIR, "assets", "logo.png"))
HERO_PATH = _first_existing(os.path.join(APP_DIR, "hero.png"), os.path.join(APP_DIR, "assets", "hero.png"))

# ---------------------------------------------------------------- palette --
INK = "#0B0F1A"
NAVY = "#12203D"
NAVY_2 = "#1B2D52"
BRASS = "#C49B4A"
BRASS_LIGHT = "#E0BF76"
PAPER = "#F7F3EA"
PAPER_2 = "#FBF9F4"
INK_TEXT = "#23262B"
MUTED = "#6B6558"


# ================================================================ GLOBAL CSS
def inject_global_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,500;0,600;0,700;1,500&family=Poppins:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"]  {{
            font-family: 'Poppins', sans-serif;
        }}

        .stApp {{
            background: {PAPER};
            background-image:
                radial-gradient(circle at 15% 0%, rgba(196,155,74,0.06) 0%, transparent 45%),
                radial-gradient(circle at 100% 10%, rgba(18,32,61,0.05) 0%, transparent 40%);
        }}

        /* headings use the serif display face */
        h1, h2, h3, h4 {{
            font-family: 'Lora', serif !important;
            color: {INK_TEXT} !important;
            letter-spacing: 0.2px;
        }}

        /* section subheaders get a slim brass rule + eyebrow-style number look */
        .stApp h3 {{
            border-bottom: 1.5px solid rgba(196,155,74,0.35);
            padding-bottom: 8px;
            margin-top: 6px !important;
        }}

        /* hide default streamlit chrome for a cleaner look */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header[data-testid="stHeader"] {{background: transparent;}}

        .block-container {{
            padding-top: 1.6rem;
            padding-left: 3.5rem;
            padding-right: 3.5rem;
            max-width: 100%;
        }}

        @media (max-width: 900px) {{
            .block-container {{ padding-left: 1.2rem; padding-right: 1.2rem; }}
        }}

        /* ---------------- buttons ---------------- */
        div[data-testid="stButton"] button, div[data-testid="stDownloadButton"] button {{
            border-radius: 999px;
            border: 1.5px solid rgba(18,32,61,0.15);
            background: {PAPER_2};
            color: {NAVY};
            font-weight: 600;
            padding: 0.5rem 1.1rem;
            transition: all 0.15s ease;
            box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        }}
        div[data-testid="stButton"] button:hover, div[data-testid="stDownloadButton"] button:hover {{
            border-color: {BRASS};
            color: {INK};
            transform: translateY(-1px);
            box-shadow: 0 6px 14px rgba(196,155,74,0.25);
        }}
        div[data-testid="stButton"] button[kind="primary"], div[data-testid="stDownloadButton"] button {{
            background: linear-gradient(135deg, {BRASS_LIGHT} 0%, {BRASS} 100%);
            color: {INK};
            border: none;
            font-weight: 700;
        }}
        div[data-testid="stButton"] button[kind="primary"]:hover, div[data-testid="stDownloadButton"] button:hover {{
            box-shadow: 0 8px 20px rgba(196,155,74,0.45);
            transform: translateY(-2px);
        }}

        /* ---------------- inputs ---------------- */
        div[data-testid="stTextInput"] input,
        div[data-testid="stTextArea"] textarea {{
            border-radius: 10px !important;
            border: 1.4px solid rgba(18,32,61,0.14) !important;
            background: {PAPER_2} !important;
            color: {INK_TEXT} !important;
        }}
        div[data-testid="stTextInput"] input:focus,
        div[data-testid="stTextArea"] textarea:focus {{
            border-color: {BRASS} !important;
            box-shadow: 0 0 0 3px rgba(196,155,74,0.18) !important;
        }}

        /* ---------------- bordered containers -> paper cards ---------------- */
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background: {PAPER_2};
            border-radius: 14px !important;
            border: 1px solid rgba(18,32,61,0.08) !important;
            box-shadow: 0 3px 14px rgba(18,32,61,0.06);
            padding: 4px 2px;
        }}

        /* ---------------- progress bars ---------------- */
        div[data-testid="stProgress"] div[role="progressbar"] > div {{
            background: linear-gradient(90deg, {BRASS} 0%, {BRASS_LIGHT} 100%) !important;
        }}

        /* ---------------- divider ---------------- */
        hr {{
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(196,155,74,0.55), transparent);
            margin: 1.6rem 0;
        }}

        /* ---------------- radio (mode picker) as pill segmented control ---------------- */
        div[data-testid="stRadio"] > div {{
            gap: 8px;
        }}
        div[data-testid="stRadio"] label {{
            background: {PAPER_2};
            border: 1.4px solid rgba(18,32,61,0.12);
            border-radius: 999px;
            padding: 6px 16px !important;
            margin-right: 4px;
        }}

        /* captions */
        .stCaption, [data-testid="stCaptionContainer"] {{
            color: {MUTED} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_global_css()


# ============================================================ HERO SECTION ==
def _img_b64(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def render_hero():
    logo_b64 = _img_b64(LOGO_PATH)
    hero_b64 = _img_b64(HERO_PATH)

    st.markdown(
        f"""
        <style>
        .hero-wrap {{
            position: relative;
            background:
                radial-gradient(circle at 85% 15%, rgba(196,155,74,0.16) 0%, transparent 45%),
                linear-gradient(135deg, {NAVY_2} 0%, {NAVY} 55%, {INK} 100%);
            border-radius: 26px;
            padding: 56px 64px;
            margin-bottom: 34px;
            box-shadow: 0 20px 48px rgba(11,15,26,0.35);
            overflow: hidden;
        }}
        .hero-wrap::before {{
            content: "";
            position: absolute;
            top: -40%;
            right: -10%;
            width: 460px;
            height: 460px;
            border-radius: 50%;
            border: 1px solid rgba(196,155,74,0.25);
        }}
        .hero-row {{
            position: relative;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 36px;
            flex-wrap: wrap;
        }}
        .hero-logo img {{
            width: 100px;
            height: 100px;
            border-radius: 50%;
            box-shadow: 0 8px 22px rgba(0,0,0,0.45);
        }}
        .hero-text {{
            flex: 1;
            min-width: 280px;
            text-align: center;
        }}
        .hero-eyebrow {{
            color: {BRASS_LIGHT};
            font-family: 'Poppins', sans-serif;
            font-size: 13px;
            font-weight: 600;
            letter-spacing: 3.5px;
            text-transform: uppercase;
            margin-bottom: 10px;
        }}
        .hero-title {{
            color: #FFFFFF;
            font-size: 48px;
            font-weight: 700;
            letter-spacing: 0.3px;
            margin: 0;
            font-family: 'Lora', serif;
            line-height: 1.15;
        }}
        .hero-sub {{
            color: #C7CEDB;
            font-size: 16px;
            margin-top: 16px;
            max-width: 580px;
            margin-left: auto;
            margin-right: auto;
            line-height: 1.6;
        }}
        .hero-image img {{
            width: 280px;
            border-radius: 18px;
            box-shadow: 0 18px 40px rgba(0,0,0,0.5);
        }}
        @media (max-width: 700px) {{
            .hero-row {{ flex-direction: column; text-align: center; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    logo_html = f'<div class="hero-logo"><img src="data:image/png;base64,{logo_b64}"/></div>' if logo_b64 else '<div class="hero-logo">🖋️</div>'
    hero_html = f'<div class="hero-image"><img src="data:image/png;base64,{hero_b64}"/></div>' if hero_b64 else ""

    st.markdown(
        f"""
        <div class="hero-wrap">
          <div class="hero-row">
            {logo_html}
            <div class="hero-text">
              <div class="hero-eyebrow">Résumé Studio</div>
              <p class="hero-title">Premium ATS Resume Builder</p>
              <p class="hero-sub">
                Fill in your details or upload an existing resume — get a polished,
                recruiter-ready .docx crafted to pass ATS screening, in a template
                that actually looks premium.
              </p>
            </div>
            {hero_html}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


render_hero()
auth.render_logout_control()



# ================================================================ STATE ====
def init_state():
    defaults = {
        "name": "", "title": "", "location": "", "phone": "", "email": "", "linkedin": "",
        "summary": "",
        "skills": [{"label": "", "value": ""}],
        "experience": [{"role": "", "company": "", "dates": "", "project": "", "bullets": [""]}],
        "certifications": [""],
        "awards": [""],
        "education": [{"degree": "", "school": "", "details": ""}],
        "resume_tier": "premium",
        "generated_docx": None,
        "generated_template": None,
        "generated_data": None,
        "used_template_ids_by_tier": {},  # tier -> [template_id, ...] most-recent-last
        "form_version": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def load_parsed_into_state(parsed: dict):
    # Bumping this changes every dynamic widget's key below, so Streamlit
    # treats them as brand-new widgets and actually uses the new values —
    # without this, a field that was ever rendered blank (e.g. the very
    # first skill/job/education row, before any upload) keeps showing blank
    # forever, because Streamlit's widget state for that key takes priority
    # over the `value=` argument on every future rerun. This was the cause
    # of "Category 1 / Job 1 / Education never fill in after upload."
    st.session_state["form_version"] = st.session_state.get("form_version", 0) + 1

    for key in ["name", "title", "location", "phone", "email", "linkedin", "summary"]:
        if parsed.get(key):
            st.session_state[key] = parsed[key]
    if parsed.get("skills"):
        st.session_state["skills"] = parsed["skills"]
    if parsed.get("experience"):
        for job in parsed["experience"]:
            job.setdefault("bullets", [])
            if not job["bullets"]:
                job["bullets"] = [""]
        st.session_state["experience"] = parsed["experience"]
    if parsed.get("certifications"):
        st.session_state["certifications"] = parsed["certifications"]
    if parsed.get("awards"):
        st.session_state["awards"] = parsed["awards"]
    if parsed.get("education"):
        st.session_state["education"] = parsed["education"]


init_state()

def _vk(base: str) -> str:
    """Versioned widget key — see the comment in load_parsed_into_state()
    for why this is needed."""
    return f"{base}_v{st.session_state['form_version']}"


# ============================================================ TIER PICKER ==
st.subheader("I. Choose a resume style")

TIER_INFO = {
    "simple": {
        "label": "Simple", "roman": "I",
        "desc": "Clean, minimal, maximum ATS safety — for conservative applicant tracking systems.",
    },
    "professional": {
        "label": "Professional", "roman": "II",
        "desc": "Confident color accents and structured headers — a step up for corporate roles.",
    },
    "premium": {
        "label": "Premium", "roman": "III",
        "desc": "A full-bleed color header banner and refined typography for a standout, high-end look.",
    },
}

tier_cols = st.columns(3)
for col, (key, info) in zip(tier_cols, TIER_INFO.items()):
    with col:
        selected = st.session_state["resume_tier"] == key
        border_color = BRASS if selected else "rgba(18,32,61,0.10)"
        bg = f"linear-gradient(160deg, {PAPER_2} 0%, #F1E7D2 100%)" if selected else PAPER_2
        st.markdown(
            f"""
            <div style="
                border: 1.6px solid {border_color};
                background: {bg};
                border-radius: 14px;
                padding: 16px 14px 10px 14px;
                text-align: center;
                box-shadow: {'0 8px 20px rgba(196,155,74,0.25)' if selected else '0 2px 8px rgba(18,32,61,0.05)'};
                margin-bottom: 8px;
                min-height: 132px;
            ">
              <div style="
                  font-family:'Lora',serif; font-size:13px; color:{BRASS if selected else MUTED};
                  letter-spacing:2px; font-weight:600; margin-bottom:4px;">
                {info['roman']}
              </div>
              <div style="font-family:'Lora',serif; font-size:18px; font-weight:700; color:{INK_TEXT};">
                {info['label']}
              </div>
              <div style="font-size:11.5px; color:{MUTED}; margin-top:6px; line-height:1.4;">
                {info['desc']}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            "Selected ✓" if selected else "Select",
            key=f"tier_btn_{key}",
            use_container_width=True,
            type="primary" if selected else "secondary",
        ):
            st.session_state["resume_tier"] = key
            st.rerun()
        st.caption(f"{len(TEMPLATES[key])} template variants")

st.divider()

# ------------------------------------------------------------- mode picker
st.subheader("II. Start with an upload or fill manually")
mode = st.radio(
    "How would you like to start?",
    ["Upload an existing resume", "Fill in manually"],
    horizontal=True,
    label_visibility="collapsed",
)

if mode == "Upload an existing resume":
    uploaded = st.file_uploader("Upload your resume (.pdf or .docx)", type=["pdf", "docx"])
    if uploaded is not None:
        if st.button("Parse resume and pre-fill form"):
            with st.spinner("Reading and parsing your resume..."):
                parsed = parse_resume(uploaded)
            load_parsed_into_state(parsed)
            st.success("Parsed! Review and correct the fields below — auto-parsing isn't perfect.")

st.divider()

# ------------------------------------------------------------------ FORM UI
st.subheader("III. Your Details")

st.markdown("**Contact Details**")
c1, c2 = st.columns(2)
with c1:
    st.session_state["name"] = st.text_input("Full Name", st.session_state["name"], key=_vk("contact_name"))
    st.session_state["location"] = st.text_input("Location (City, State/Country)", st.session_state["location"], key=_vk("contact_location"))
    st.session_state["email"] = st.text_input("Email", st.session_state["email"], key=_vk("contact_email"))
with c2:
    st.session_state["title"] = st.text_input("Headline / Target Job Title", st.session_state["title"], key=_vk("contact_title"))
    st.session_state["phone"] = st.text_input("Phone", st.session_state["phone"], key=_vk("contact_phone"))
    st.session_state["linkedin"] = st.text_input("LinkedIn URL (optional)", st.session_state["linkedin"], key=_vk("contact_linkedin"))

st.markdown("**Professional Summary**")
st.session_state["summary"] = st.text_area("Summary", st.session_state["summary"], height=120, label_visibility="collapsed", key=_vk("contact_summary"))

st.markdown("**Technical / Core Skills**")
for i, s in enumerate(st.session_state["skills"]):
    col1, col2, col3 = st.columns([2, 4, 0.5])
    s["label"] = col1.text_input(f"Category {i+1}", s.get("label", ""), key=_vk(f"skill_label_{i}"))
    s["value"] = col2.text_input(f"Skills {i+1}", s.get("value", ""), key=_vk(f"skill_value_{i}"))
    if col3.button("✕", key=_vk(f"skill_del_{i}")) and len(st.session_state["skills"]) > 1:
        st.session_state["skills"].pop(i)
        st.session_state["form_version"] += 1
        st.rerun()
if st.button("+ Add skill category"):
    st.session_state["skills"].append({"label": "", "value": ""})
    st.rerun()

st.markdown("**Professional Experience**")
for i, job in enumerate(st.session_state["experience"]):
    with st.container(border=True):
        st.markdown(f"Job {i+1}")
        jc1, jc2 = st.columns(2)
        job["role"] = jc1.text_input("Job Title", job.get("role", ""), key=_vk(f"job_role_{i}"))
        job["company"] = jc2.text_input("Company", job.get("company", ""), key=_vk(f"job_company_{i}"))
        jc3, jc4 = st.columns(2)
        job["dates"] = jc3.text_input("Dates (e.g. Jan 2022 – Present)", job.get("dates", ""), key=_vk(f"job_dates_{i}"))
        job["project"] = jc4.text_input("Project (optional)", job.get("project", ""), key=_vk(f"job_project_{i}"))

        st.caption("Bullet points (start with an action verb, add numbers where possible)")
        for bi, bullet in enumerate(job["bullets"]):
            bc1, bc2 = st.columns([6, 0.5])
            job["bullets"][bi] = bc1.text_input(
                f"Bullet {bi+1}", bullet, key=_vk(f"job_{i}_bullet_{bi}"), label_visibility="collapsed"
            )
            if bc2.button("✕", key=_vk(f"job_{i}_bullet_del_{bi}")) and len(job["bullets"]) > 1:
                job["bullets"].pop(bi)
                st.session_state["form_version"] += 1
                st.rerun()
        if st.button("+ Add bullet", key=_vk(f"job_{i}_add_bullet")):
            job["bullets"].append("")
            st.rerun()

        if st.button("Remove this job", key=_vk(f"job_del_{i}")) and len(st.session_state["experience"]) > 1:
            st.session_state["experience"].pop(i)
            st.session_state["form_version"] += 1
            st.rerun()
if st.button("+ Add another job"):
    st.session_state["experience"].append({"role": "", "company": "", "dates": "", "project": "", "bullets": [""]})
    st.rerun()

st.markdown("**Certifications**")
for i, cert in enumerate(st.session_state["certifications"]):
    cc1, cc2 = st.columns([6, 0.5])
    st.session_state["certifications"][i] = cc1.text_input(
        f"Certification {i+1}", cert, key=_vk(f"cert_{i}"), label_visibility="collapsed"
    )
    if cc2.button("✕", key=_vk(f"cert_del_{i}")) and len(st.session_state["certifications"]) > 1:
        st.session_state["certifications"].pop(i)
        st.session_state["form_version"] += 1
        st.rerun()
if st.button("+ Add certification"):
    st.session_state["certifications"].append("")
    st.rerun()

st.markdown("**Awards & Achievements**")
for i, award in enumerate(st.session_state["awards"]):
    ac1, ac2 = st.columns([6, 0.5])
    st.session_state["awards"][i] = ac1.text_input(
        f"Award {i+1}", award, key=_vk(f"award_{i}"), label_visibility="collapsed"
    )
    if ac2.button("✕", key=_vk(f"award_del_{i}")) and len(st.session_state["awards"]) > 1:
        st.session_state["awards"].pop(i)
        st.session_state["form_version"] += 1
        st.rerun()
if st.button("+ Add award"):
    st.session_state["awards"].append("")
    st.rerun()

st.markdown("**Education**")
for i, edu in enumerate(st.session_state["education"]):
    with st.container(border=True):
        edu["degree"] = st.text_input("Degree", edu.get("degree", ""), key=_vk(f"edu_degree_{i}"))
        edu["school"] = st.text_input("School / University", edu.get("school", ""), key=_vk(f"edu_school_{i}"))
        edu["details"] = st.text_input("Year / Grade / Extra details", edu.get("details", ""), key=_vk(f"edu_details_{i}"))
        if st.button("Remove this education entry", key=_vk(f"edu_del_{i}")) and len(st.session_state["education"]) > 1:
            st.session_state["education"].pop(i)
            st.session_state["form_version"] += 1
            st.rerun()
if st.button("+ Add education entry"):
    st.session_state["education"].append({"degree": "", "school": "", "details": ""})
    st.rerun()

st.divider()


# --------------------------------------------------------------- generate
def _has_job_content(job):
    """A job entry counts as 'filled' if it has any real content at all —
    not just role/company. Previously an entry with only bullets/dates/
    project (e.g. because role/company weren't typed in yet, or an upload
    parse missed them) was silently dropped from the download. Now it's
    kept, so nothing the user entered ever disappears."""
    if job.get("role", "").strip() or job.get("company", "").strip():
        return True
    if job.get("dates", "").strip() or job.get("project", "").strip():
        return True
    if any(b.strip() for b in job.get("bullets", [])):
        return True
    return False


def _has_edu_content(edu):
    return bool(
        edu.get("degree", "").strip()
        or edu.get("school", "").strip()
        or edu.get("details", "").strip()
    )


def _collect_data():
    return {
        "name": st.session_state["name"],
        "title": st.session_state["title"],
        "location": st.session_state["location"],
        "phone": st.session_state["phone"],
        "email": st.session_state["email"],
        "linkedin": st.session_state["linkedin"],
        "summary": st.session_state["summary"],
        "skills": [s for s in st.session_state["skills"] if s.get("label") or s.get("value")],
        "experience": [
            {**job, "bullets": [b for b in job["bullets"] if b.strip()]}
            for job in st.session_state["experience"]
            if _has_job_content(job)
        ],
        "certifications": [c for c in st.session_state["certifications"] if c.strip()],
        "awards": [a for a in st.session_state["awards"] if a.strip()],
        "education": [e for e in st.session_state["education"] if _has_edu_content(e)],
    }


st.subheader("IV. Generate")
tier = st.session_state["resume_tier"]
st.caption(f"Selected style: **{TIER_INFO[tier]['label']}** — a random template from this tier will be used.")

if st.button("🖋️  Generate Resume", type="primary"):
    if not st.session_state["name"].strip():
        st.error("Please enter at least your name before generating.")
    else:
        data = _collect_data()

        # "Shuffle bag": avoid repeating a template within this tier until
        # every other variant in that tier has been shown at least once.
        used_map = st.session_state["used_template_ids_by_tier"]
        used_for_tier = used_map.get(tier, [])
        template = pick_random_template(tier, exclude_ids=used_for_tier)

        used_for_tier.append(template["id"])
        if len(used_for_tier) >= len(TEMPLATES[tier]):
            used_for_tier = [template["id"]]  # start a fresh cycle, keep this one so it isn't repeated next time
        used_map[tier] = used_for_tier
        st.session_state["used_template_ids_by_tier"] = used_map

        with st.spinner(f"Building your {TIER_INFO[tier]['label']} resume ({template['name']} template)..."):
            docx_bytes = build_resume(data, template=template)

        st.session_state["generated_docx"] = docx_bytes
        st.session_state["generated_template"] = template
        st.session_state["generated_data"] = data
        st.success(f"Your resume is ready! Template used: **{template['name']}** ({TIER_INFO[tier]['label']} tier)")

if st.session_state.get("generated_docx"):
    data = st.session_state["generated_data"]
    file_name = f"{(data['name'] or 'Resume').replace(' ', '_')}_Resume.docx"
    dcol1, dcol2 = st.columns(2)
    with dcol1:
        st.download_button(
            "⬇️  Download Resume (.docx)",
            data=st.session_state["generated_docx"],
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )
    with dcol2:
        check_ats = st.button("🔎  Check ATS Score", use_container_width=True)

    if check_ats:
        result = score_resume(data)
        total = result["total"]

        if total >= 90:
            gauge_color = "#2E7D4F"
            verdict = "Excellent — highly likely to pass ATS screening."
        elif total >= 75:
            gauge_color = BRASS
            verdict = "Good — a few improvements would push this into the top tier."
        else:
            gauge_color = "#B3453A"
            verdict = "Needs work — add more detail before applying."

        # ---- brass-themed donut gauge ----
        fig, ax = plt.subplots(figsize=(3.6, 3.6), subplot_kw={"aspect": "equal"})
        fig.patch.set_alpha(0)
        ax.set_facecolor("none")

        theta = np.linspace(0.5 * np.pi, 0.5 * np.pi - 2 * np.pi * (total / 100), 200)
        track_theta = np.linspace(0, 2 * np.pi, 200)

        ax.plot(np.cos(track_theta), np.sin(track_theta), linewidth=14, color="#E7DEC8", solid_capstyle="round")
        ax.plot(np.cos(theta), np.sin(theta), linewidth=14, color=gauge_color, solid_capstyle="round")

        ax.text(0, 0.08, f"{total}", ha="center", va="center", fontsize=42, fontweight="bold",
                color=INK_TEXT, family="serif")
        ax.text(0, -0.28, "/ 100", ha="center", va="center", fontsize=13, color=MUTED)

        ax.set_xlim(-1.3, 1.3)
        ax.set_ylim(-1.3, 1.3)
        ax.axis("off")

        buf = io.BytesIO()
        fig.savefig(buf, format="png", transparent=True, dpi=180, bbox_inches="tight")
        plt.close(fig)
        buf.seek(0)

        gcol1, gcol2 = st.columns([1, 1.4])
        with gcol1:
            st.image(buf, use_container_width=True)
        with gcol2:
            st.markdown(
                f"""
                <div style="padding-top: 22px;">
                  <div style="font-family:'Lora',serif; font-size:20px; font-weight:700; color:{gauge_color};">
                    {"Excellent" if total>=90 else "Good" if total>=75 else "Needs Work"}
                  </div>
                  <div style="font-size:13.5px; color:{MUTED}; margin-top:6px; line-height:1.5;">
                    {verdict}
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("**Score breakdown**")
        for label, s, m, detail in result["breakdown"]:
            pct = s / m if m else 0
            st.write(f"**{label}** — {s}/{m}")
            st.progress(pct)
            st.caption(detail)

        if total < 90:
            st.info(
                "Tip: add numbers/metrics to your bullet points (e.g. \"reduced costs by 20%\"), "
                "start each bullet with an action verb, and make sure every section above has content — "
                "these are the biggest score drivers."
            )

