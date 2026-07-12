"""
ats_scorer.py
--------------
Heuristic ATS-friendliness score (0-100) for a resume, based on the
structured `data` dict used to build it (see resume_builder.build_resume).

This is NOT a connection to any real ATS vendor — no such public API
exists — it's a checklist-based approximation of what ATS parsers and
recruiters commonly screen for: parseable contact info, standard section
headings, bullet-based experience, quantified achievements, action verbs,
adequate (not sparse, not bloated) content, and a clean single-column
format free of tables/images (guaranteed by resume_builder itself).
"""

import re

ACTION_VERBS = {
    "led", "built", "created", "developed", "designed", "managed", "delivered",
    "improved", "increased", "reduced", "optimized", "implemented", "launched",
    "coordinated", "drove", "achieved", "streamlined", "automated", "resolved",
    "supported", "performed", "executed", "analyzed", "collaborated", "mentored",
    "migrated", "deployed", "architected", "spearheaded", "negotiated", "trained",
    "prepared", "delivered", "enhanced", "maintained", "monitored", "configured",
    "administered", "engineered", "produced", "generated", "owned", "scaled",
}

NUMBER_RE = re.compile(r"\d")


def _score_contact(data):
    fields = ["name", "email", "phone", "location", "linkedin"]
    present = sum(1 for f in fields if data.get(f, "").strip())
    score = round((present / len(fields)) * 15)
    detail = f"{present}/{len(fields)} contact fields present (name, email, phone, location, LinkedIn)"
    return score, 15, detail


def _score_sections(data):
    checks = {
        "Professional Summary": bool(data.get("summary", "").strip()),
        "Skills": bool(data.get("skills")),
        "Experience": bool(data.get("experience")),
        "Education": bool(data.get("education")),
    }
    present = sum(checks.values())
    score = round((present / len(checks)) * 20)
    missing = [k for k, v in checks.items() if not v]
    detail = "All core sections present" if not missing else f"Missing: {', '.join(missing)}"
    return score, 20, detail


def _score_bullets(data):
    jobs = data.get("experience", [])
    if not jobs:
        return 0, 15, "No experience entries found"
    good_jobs = 0
    for job in jobs:
        n = len([b for b in job.get("bullets", []) if b.strip()])
        if 3 <= n <= 7:
            good_jobs += 1
    ratio = good_jobs / len(jobs)
    score = round(ratio * 15)
    detail = f"{good_jobs}/{len(jobs)} roles have an ideal bullet count (3–7)"
    return score, 15, detail


def _score_quantified(data):
    jobs = data.get("experience", [])
    all_bullets = [b for job in jobs for b in job.get("bullets", []) if b.strip()]
    if not all_bullets:
        return 0, 10, "No bullet points to evaluate"
    quantified = sum(1 for b in all_bullets if NUMBER_RE.search(b))
    ratio = quantified / len(all_bullets)
    score = round(ratio * 10)
    detail = f"{quantified}/{len(all_bullets)} bullets include a number or metric"
    return score, 10, detail


def _score_action_verbs(data):
    jobs = data.get("experience", [])
    all_bullets = [b for job in jobs for b in job.get("bullets", []) if b.strip()]
    if not all_bullets:
        return 0, 10, "No bullet points to evaluate"
    starts_with_verb = 0
    for b in all_bullets:
        first_word = re.sub(r"[^a-zA-Z]", "", b.strip().split()[0]).lower() if b.strip().split() else ""
        if first_word in ACTION_VERBS:
            starts_with_verb += 1
    ratio = starts_with_verb / len(all_bullets)
    score = round(ratio * 10)
    detail = f"{starts_with_verb}/{len(all_bullets)} bullets start with a strong action verb"
    return score, 10, detail


def _score_skills(data):
    skills = data.get("skills", [])
    total_terms = 0
    for s in skills:
        total_terms += len([v for v in s.get("value", "").split(",") if v.strip()])
    score = 10 if total_terms >= 8 else round((total_terms / 8) * 10)
    detail = f"{total_terms} distinct skill keywords listed"
    return score, 10, detail


def _score_length(data):
    all_text = " ".join([
        data.get("summary", ""),
        " ".join(b for job in data.get("experience", []) for b in job.get("bullets", [])),
    ])
    word_count = len(all_text.split())
    if 150 <= word_count <= 700:
        score = 10
    elif word_count < 150:
        score = round((word_count / 150) * 10)
    else:
        score = max(0, 10 - round((word_count - 700) / 100))
    detail = f"~{word_count} words of content (ideal: 150–700)"
    return score, 10, detail


def _score_format():
    # Guaranteed by resume_builder.py: single column, real text only,
    # no tables, no images/icons, no text boxes, standard fonts.
    return 10, 10, "Single-column, table-free, image-free layout with standard fonts"


def score_resume(data: dict) -> dict:
    """Returns {'total': int, 'max': 100, 'breakdown': [ (label, score, max, detail), ... ]}"""
    checks = [
        ("Contact Information", _score_contact(data)),
        ("Standard Sections", _score_sections(data)),
        ("Bullet Structure", _score_bullets(data)),
        ("Quantified Achievements", _score_quantified(data)),
        ("Action Verbs", _score_action_verbs(data)),
        ("Skills Keywords", _score_skills(data)),
        ("Content Length", _score_length(data)),
        ("ATS-Safe Formatting", _score_format()),
    ]
    total = sum(c[1][0] for c in checks)
    breakdown = [(label, s, m, d) for label, (s, m, d) in checks]
    return {"total": total, "max": 100, "breakdown": breakdown}
