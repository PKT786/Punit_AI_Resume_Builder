"""
resume_parser.py
-----------------
Best-effort extraction of structured resume data from an uploaded .pdf or
.docx file, so the Streamlit form can be pre-filled and the user only needs
to correct/complete it rather than retype everything from scratch.

This is intentionally heuristic (regex + keyword based) — resumes come in
too many formats to parse perfectly. Always show the results in an editable
form after parsing.
"""

import re
import io
import docx
import pdfplumber

SECTION_ALIASES = {
    "summary": ["summary", "professional summary", "profile", "objective", "about"],
    "skills": ["technical skills", "skills", "core competencies", "key skills"],
    "experience": ["experience", "professional experience", "work experience", "employment history"],
    "certifications": ["certifications", "certificates", "certification"],
    "awards": ["awards", "achievements", "awards & achievements", "honors"],
    "education": ["education", "academic background", "qualifications"],
}

DATE_RANGE_RE = re.compile(
    r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s*\d{4}|\d{4})\s*[-–—to]{1,3}\s*"
    r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s*\d{4}|\d{4}|Present|Current)",
    re.IGNORECASE,
)
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"(\+?\d[\d\-\s()]{8,}\d)")
LINKEDIN_RE = re.compile(r"(https?://)?(www\.)?linkedin\.com/[^\s|,]+", re.IGNORECASE)


# ------------------------------------------------------------------ readers
def extract_text(uploaded_file) -> str:
    """uploaded_file: a Streamlit UploadedFile (has .name and read())."""
    name = uploaded_file.name.lower()
    data = uploaded_file.read()

    if name.endswith(".pdf"):
        text_parts = []
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            for page in pdf.pages:
                t = page.extract_text() or ""
                text_parts.append(t)
        return "\n".join(text_parts)

    if name.endswith(".docx"):
        d = docx.Document(io.BytesIO(data))
        return "\n".join(p.text for p in d.paragraphs)

    # fallback: try to decode as plain text
    try:
        return data.decode("utf-8", errors="ignore")
    except Exception:
        return ""


# -------------------------------------------------------------- section split
def _find_section_spans(lines):
    """Return {section_key: (start_idx, end_idx)} based on heading keyword matches."""
    spans = {}
    hits = []  # (line_idx, section_key)
    for i, line in enumerate(lines):
        clean = line.strip().strip(":").lower()
        if not clean or len(clean) > 40:
            continue
        for key, aliases in SECTION_ALIASES.items():
            if clean in aliases or any(clean == a for a in aliases):
                hits.append((i, key))
                break
    for idx, (line_idx, key) in enumerate(hits):
        end = hits[idx + 1][0] if idx + 1 < len(hits) else len(lines)
        spans[key] = (line_idx + 1, end)
    return spans


# ------------------------------------------------------------------- fields
def _guess_name(lines):
    for line in lines[:6]:
        clean = line.strip()
        if not clean:
            continue
        if EMAIL_RE.search(clean) or PHONE_RE.search(clean):
            continue
        if len(clean.split()) <= 5 and not any(ch.isdigit() for ch in clean):
            return clean.title() if clean.isupper() else clean
    return ""


def _guess_title(lines, name_line_idx):
    for line in lines[name_line_idx + 1:name_line_idx + 4]:
        clean = line.strip()
        if not clean or EMAIL_RE.search(clean) or PHONE_RE.search(clean):
            continue
        if len(clean) < 100:
            return clean
    return ""


def _parse_skills_block(block_lines):
    skills = []
    for line in block_lines:
        raw = line.strip(" -•")
        if not raw.strip():
            continue
        if "\t" in raw:
            label, value = raw.split("\t", 1)
            skills.append({"label": label.strip(), "value": value.strip()})
        elif ":" in raw:
            label, value = raw.split(":", 1)
            skills.append({"label": label.strip(), "value": value.strip()})
        else:
            skills.append({"label": "Skills", "value": raw.strip()})
    return skills


def _split_role_company(header_text: str):
    """
    Splits a job-header string into (role, company). Tries separators in
    order of how unambiguous they are, so we don't accidentally split on a
    hyphen that's part of a company name (e.g. "Coca-Cola").
    """
    header_text = header_text.strip(" \t")
    for sep in ["|", "—", " – ", " - "]:
        if sep in header_text:
            left, right = header_text.split(sep, 1)
            left, right = left.strip(), right.strip()
            if left:
                return left, right
    return header_text, ""


def _parse_experience_block(block_lines):
    """
    Groups lines into jobs. A new job starts at a line containing a date range.
    Everything between one job-header and the next is treated as bullets,
    with the first non-bullet line kept as a 'project' hint.
    """
    jobs = []
    current = None
    for raw in block_lines:
        line = raw.strip()
        if not line:
            continue
        m = DATE_RANGE_RE.search(line)
        if m:
            if current:
                jobs.append(current)
            header_text = line[:m.start()].strip(" \t|-–—")
            role, company = _split_role_company(header_text)
            current = {
                "role": role or header_text,
                "company": company,
                "dates": m.group(0).strip(),
                "project": "",
                "bullets": [],
            }
        else:
            if current is None:
                continue
            bullet_text = line.lstrip("•-*\t ").strip()
            if bullet_text.lower().startswith("project"):
                current["project"] = bullet_text.split(":", 1)[-1].strip()
            elif bullet_text:
                current["bullets"].append(bullet_text)
    if current:
        jobs.append(current)
    return jobs


def _parse_bullet_list(block_lines):
    items = []
    for line in block_lines:
        clean = line.strip(" -•\t")
        if clean:
            items.append(clean)
    return items


def _parse_education_block(block_lines):
    entries = []
    current = {}
    for line in block_lines:
        clean = line.strip()
        if not clean:
            continue
        if not current.get("degree"):
            current["degree"] = clean
        elif not current.get("school"):
            current["school"] = clean
        else:
            current["details"] = (current.get("details", "") + " " + clean).strip()
    if current:
        entries.append(current)
    return entries


# --------------------------------------------------------------------- main
def parse_resume(uploaded_file) -> dict:
    text = extract_text(uploaded_file)
    lines = [l for l in text.split("\n")]
    non_empty = [l for l in lines if l.strip()]

    name = _guess_name(non_empty)
    name_idx = 0
    for i, l in enumerate(lines):
        if name and name.lower() in l.lower():
            name_idx = i
            break
    title = _guess_title(lines, name_idx)

    email_match = EMAIL_RE.search(text)
    phone_match = PHONE_RE.search(text)
    linkedin_match = LINKEDIN_RE.search(text)

    spans = _find_section_spans(lines)

    def block(key):
        if key not in spans:
            return []
        start, end = spans[key]
        return lines[start:end]

    summary_lines = block("summary")
    summary = " ".join(l.strip() for l in summary_lines if l.strip())

    data = {
        "name": name,
        "title": title,
        "location": "",
        "phone": phone_match.group(0).strip() if phone_match else "",
        "email": email_match.group(0).strip() if email_match else "",
        "linkedin": linkedin_match.group(0).strip() if linkedin_match else "",
        "summary": summary,
        "skills": _parse_skills_block(block("skills")),
        "experience": _parse_experience_block(block("experience")),
        "certifications": _parse_bullet_list(block("certifications")),
        "awards": _parse_bullet_list(block("awards")),
        "education": _parse_education_block(block("education")),
    }
    return data
