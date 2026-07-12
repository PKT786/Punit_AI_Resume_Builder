"""
auth.py
--------
Login / signup gate for the app, matching the "ink & brass" premium look
(reuses logo.png and hero.png already in the repo).

What this gives you
--------------------
- Sign up with Name, Email (used as the user id), Mobile number, Password.
  If the email is already registered, the person is told so and pointed to
  Log In instead — no duplicate accounts.
- Log in with Email + Password.
- "Continue with Google" / "Continue with Facebook" — OAuth login that
  creates an account automatically on first use (no separate signup step),
  after verifying the identity with the provider.
- Every successful signup or login sends you (the app owner) an email and
  an SMS with the user's name, email, and mobile number.

Where things are stored
------------------------
User records live in a local SQLite file (`users.db`, created next to this
file the first time someone signs up). That's enough to make "don't let
someone sign up twice" and "log in later" work correctly. One honest
caveat: on hosts with an ephemeral filesystem (e.g. a fresh Streamlit
Community Cloud deploy after a restart), that file can be wiped and user
records lost. For anything beyond a demo/small deployment, point
`DB_PATH` below at a persistent disk, or swap `_get_conn()` to a hosted
database (Postgres/Supabase/etc.) — every other function in this file only
talks to `_get_conn()`, so that's the one place you'd need to change.

Required configuration (Streamlit secrets)
--------------------------------------------
None of this is hardcoded — you provide your own credentials via
`.streamlit/secrets.toml` (see secrets_example.toml). Anything not
configured is simply skipped (e.g. no Google secrets -> no Google button;
no SMTP secrets -> no admin email sent), so the app still runs without
every integration wired up.

    [smtp]
    host = "smtp.gmail.com"
    port = 587
    username = "you@gmail.com"
    app_password = "xxxx xxxx xxxx xxxx"   # Gmail App Password, not your normal password
    admin_email = "punitkr.786@gmail.com"

    [sms]
    twilio_account_sid = "..."
    twilio_auth_token = "..."
    twilio_from_number = "+1XXXXXXXXXX"
    admin_phone = "+919145480345"

    [google_oauth]
    client_id = "....apps.googleusercontent.com"
    client_secret = "..."
    redirect_uri = "https://your-deployed-app-url"

    [facebook_oauth]
    app_id = "..."
    app_secret = "..."
    redirect_uri = "https://your-deployed-app-url"

Usage in app.py
----------------
    import auth
    if not auth.require_login():
        st.stop()
    # ...rest of the app, only reached once someone is logged in...
    auth.render_logout_control()   # optional small "logged in as ..." + logout button
"""

import base64
import hashlib
import hmac
import os
import re
import secrets
import sqlite3
import time
from contextlib import closing

import requests
import streamlit as st

APP_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(APP_DIR, "users.db")

LOGO_PATH = os.path.join(APP_DIR, "logo.png")
HERO_PATH = os.path.join(APP_DIR, "hero.png")
PREVIEW_PATH = os.path.join(APP_DIR, "resume_preview.png")

# ---------------------------------------------------------------- palette --
# Mirrors app.py's "ink & brass" theme so the auth page matches the rest of
# the app. Duplicated here (rather than imported) so this file can be
# dropped into any project on its own.
INK = "#0B0F1A"
NAVY = "#12203D"
NAVY_2 = "#1B2D52"
BRASS = "#C49B4A"
BRASS_LIGHT = "#E0BF76"
PAPER = "#F7F3EA"
PAPER_2 = "#FBF9F4"
INK_TEXT = "#23262B"
MUTED = "#6B6558"

EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")
MOBILE_RE = re.compile(r"^\+?\d[\d\s-]{7,14}\d$")


# ============================================================ DATABASE ====
# Why this matters: on hosts with an ephemeral filesystem (this includes
# Streamlit Community Cloud whenever the app restarts/redeploys/sleeps),
# a plain local file gets wiped — which looks exactly like "it's asking me
# to sign up again" even though nothing in the signup logic is wrong; the
# user list itself just disappeared. Add a [postgres] section to your
# secrets (see secrets_example.toml) — a free instance from Supabase or
# Neon works fine — and accounts persist properly across restarts. Without
# it, everything still works, just backed by a local SQLite file instead.
try:
    _PG_URL = st.secrets.get("postgres", {}).get("url")
except Exception:
    _PG_URL = None

_USE_POSTGRES = bool(_PG_URL) and not _PG_URL.strip().lower().startswith("postgres://user:pass")
_PARAM = "%s" if _USE_POSTGRES else "?"


def _get_conn():
    if _USE_POSTGRES:
        import psycopg2
        conn = psycopg2.connect(_PG_URL)
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                mobile TEXT,
                password_hash TEXT,
                auth_provider TEXT NOT NULL DEFAULT 'password',
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()
        cur.close()
        return conn

    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            mobile TEXT,
            password_hash TEXT,
            auth_provider TEXT NOT NULL DEFAULT 'password',
            created_at TEXT NOT NULL
        )
        """
    )
    return conn


def _hash_password(password: str, salt: str = None) -> str:
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 200_000)
    return f"{salt}${digest.hex()}"


def _verify_password(password: str, stored: str) -> bool:
    try:
        salt, _ = stored.split("$", 1)
    except ValueError:
        return False
    return hmac.compare_digest(_hash_password(password, salt), stored)


def _public_user(user: dict) -> dict:
    """Strip the password hash before this dict lives in session state."""
    return {k: v for k, v in user.items() if k != "password_hash"}


def find_user_by_email(email: str):
    with closing(_get_conn()) as conn:
        cur = conn.cursor()
        cur.execute(
            f"SELECT id, name, email, mobile, password_hash, auth_provider FROM users WHERE email = {_PARAM}",
            (email.lower().strip(),),
        )
        row = cur.fetchone()
    if not row:
        return None
    return {
        "id": row[0], "name": row[1], "email": row[2],
        "mobile": row[3], "password_hash": row[4], "auth_provider": row[5],
    }


def create_user(name: str, email: str, mobile: str, password: str = None, provider: str = "password"):
    email = email.lower().strip()
    password_hash = _hash_password(password) if password else None
    with closing(_get_conn()) as conn:
        cur = conn.cursor()
        cur.execute(
            f"INSERT INTO users (name, email, mobile, password_hash, auth_provider, created_at) "
            f"VALUES ({_PARAM}, {_PARAM}, {_PARAM}, {_PARAM}, {_PARAM}, {_PARAM})",
            (name.strip(), email, mobile.strip(), password_hash, provider, time.strftime("%Y-%m-%d %H:%M:%S")),
        )
        conn.commit()
    return find_user_by_email(email)


# ======================================================== NOTIFICATIONS ====
def _secret(section, key, default=None):
    try:
        return st.secrets[section][key]
    except Exception:
        return default


def notify_admin(event: str, user: dict):
    """Best-effort email + SMS to the app owner. Never raises — a missing
    or wrong config should not block someone from logging in."""
    _send_admin_email(event, user)
    _send_admin_sms(event, user)


def _send_admin_email(event: str, user: dict):
    host = _secret("smtp", "host")
    username = _secret("smtp", "username")
    app_password = _secret("smtp", "app_password")
    admin_email = _secret("smtp", "admin_email", "punitkr.786@gmail.com")
    port = _secret("smtp", "port", 587)
    if not (host and username and app_password):
        return  # not configured — silently skip
    try:
        import smtplib
        from email.mime.text import MIMEText

        body = (
            f"Event: {event}\n"
            f"Name: {user.get('name', '')}\n"
            f"Email: {user.get('email', '')}\n"
            f"Mobile: {user.get('mobile', '')}\n"
            f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        msg = MIMEText(body)
        msg["Subject"] = f"[Resume Studio] {event}: {user.get('name', 'Unknown')}"
        msg["From"] = username
        msg["To"] = admin_email

        with smtplib.SMTP(host, int(port), timeout=10) as server:
            server.starttls()
            server.login(username, app_password)
            server.sendmail(username, [admin_email], msg.as_string())
    except Exception as e:
        st.session_state.setdefault("_notify_warnings", []).append(f"Email notification failed: {e}")


def _send_admin_sms(event: str, user: dict):
    sid = _secret("sms", "twilio_account_sid")
    token = _secret("sms", "twilio_auth_token")
    from_number = _secret("sms", "twilio_from_number")
    admin_phone = _secret("sms", "admin_phone", "+919145480345")
    if not (sid and token and from_number):
        return  # not configured — silently skip
    try:
        body = (
            f"{event}: {user.get('name','')} | {user.get('email','')} | {user.get('mobile','')}"
        )
        resp = requests.post(
            f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json",
            auth=(sid, token),
            data={"To": admin_phone, "From": from_number, "Body": body},
            timeout=10,
        )
        if resp.status_code >= 300:
            raise RuntimeError(f"Twilio returned {resp.status_code}: {resp.text[:200]}")
    except Exception as e:
        st.session_state.setdefault("_notify_warnings", []).append(f"SMS notification failed: {e}")


# ============================================================== OAUTH =====
def _looks_like_placeholder(value: str) -> bool:
    """
    Catches values copied straight from secrets_example.toml without being
    replaced (e.g. "xxxxxxxxxx.apps.googleusercontent.com", "your-deployed-app-url").
    This is what caused the Google 400 / Facebook "Invalid App ID" errors —
    the buttons rendered with placeholder text as real credentials. Now we
    just hide the button instead until real values are set.
    """
    if not value:
        return True
    v = str(value).strip().lower()
    return ("xxxx" in v) or v.startswith("your-") or "your-deployed-app" in v or v in ("", "changeme")


def _oauth_configured(provider: str) -> bool:
    if provider == "google":
        client_id = _secret("google_oauth", "client_id")
        redirect_uri = _secret("google_oauth", "redirect_uri")
        client_secret = _secret("google_oauth", "client_secret")
        return not any(_looks_like_placeholder(v) for v in [client_id, redirect_uri, client_secret])
    if provider == "facebook":
        app_id = _secret("facebook_oauth", "app_id")
        redirect_uri = _secret("facebook_oauth", "redirect_uri")
        app_secret = _secret("facebook_oauth", "app_secret")
        return not any(_looks_like_placeholder(v) for v in [app_id, redirect_uri, app_secret])
    return False


def _google_auth_url():
    client_id = _secret("google_oauth", "client_id")
    redirect_uri = _secret("google_oauth", "redirect_uri")
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "prompt": "select_account",
        "state": "google",
    }
    query = "&".join(f"{k}={requests.utils.quote(str(v))}" for k, v in params.items())
    return f"https://accounts.google.com/o/oauth2/v2/auth?{query}"


def _google_handle_callback(code: str):
    client_id = _secret("google_oauth", "client_id")
    client_secret = _secret("google_oauth", "client_secret")
    redirect_uri = _secret("google_oauth", "redirect_uri")
    token_resp = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code, "client_id": client_id, "client_secret": client_secret,
            "redirect_uri": redirect_uri, "grant_type": "authorization_code",
        },
        timeout=10,
    )
    token_resp.raise_for_status()
    access_token = token_resp.json()["access_token"]

    info_resp = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=10,
    )
    info_resp.raise_for_status()
    info = info_resp.json()

    # "Validate the user is genuine": require the provider to confirm the
    # email is verified before we trust it. Google can return this as a
    # real bool or as the string "true"/"false" depending on token type,
    # so normalize it explicitly rather than doing `if not info.get(...)`.
    verified = info.get("email_verified", False)
    if isinstance(verified, str):
        verified = verified.lower() == "true"
    if not verified:
        raise ValueError("Google account email is not verified.")

    return {
        "name": info.get("name") or info.get("email", "").split("@")[0],
        "email": info["email"],
        "mobile": "",
    }


def _facebook_auth_url():
    app_id = _secret("facebook_oauth", "app_id")
    redirect_uri = _secret("facebook_oauth", "redirect_uri")
    params = {
        "client_id": app_id, "redirect_uri": redirect_uri,
        "scope": "email public_profile", "state": "facebook",
    }
    query = "&".join(f"{k}={requests.utils.quote(str(v))}" for k, v in params.items())
    return f"https://www.facebook.com/v19.0/dialog/oauth?{query}"


def _facebook_handle_callback(code: str):
    app_id = _secret("facebook_oauth", "app_id")
    app_secret = _secret("facebook_oauth", "app_secret")
    redirect_uri = _secret("facebook_oauth", "redirect_uri")

    token_resp = requests.get(
        "https://graph.facebook.com/v19.0/oauth/access_token",
        params={
            "client_id": app_id, "client_secret": app_secret,
            "redirect_uri": redirect_uri, "code": code,
        },
        timeout=10,
    )
    token_resp.raise_for_status()
    access_token = token_resp.json()["access_token"]

    # A successful Graph API call with this token IS the identity check —
    # Facebook only issues it after the person authenticated on facebook.com.
    info_resp = requests.get(
        "https://graph.facebook.com/me",
        params={"fields": "id,name,email", "access_token": access_token},
        timeout=10,
    )
    info_resp.raise_for_status()
    info = info_resp.json()

    if not info.get("email"):
        raise ValueError("Facebook account has no verified email to sign in with.")

    return {"name": info.get("name", ""), "email": info["email"], "mobile": ""}


def _handle_oauth_redirect():
    """Runs on every page load; if we're coming back from a provider
    redirect (?code=...&state=google|facebook), complete the login."""
    params = st.query_params
    code = params.get("code")
    state = params.get("state")
    if not code or not state:
        return

    try:
        if state == "google":
            profile = _google_handle_callback(code)
        elif state == "facebook":
            profile = _facebook_handle_callback(code)
        else:
            return

        user = find_user_by_email(profile["email"])
        if user is None:
            user = create_user(
                name=profile["name"], email=profile["email"],
                mobile=profile.get("mobile", ""), password=None, provider=state,
            )
            notify_admin(f"New signup via {state.title()}", user)
        else:
            notify_admin(f"Login via {state.title()}", user)

        st.session_state["auth_user"] = _public_user(user)
        st.query_params.clear()
        st.rerun()
    except Exception as e:
        st.query_params.clear()
        st.session_state["_auth_error"] = f"{state.title()} sign-in failed: {e}"


# =============================================================== CSS/UI ====
def _img_b64(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def _inject_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,500;0,600;0,700;1,500&family=Poppins:wght@300;400;500;600;700&display=swap');
        html, body, [class*="css"] {{ font-family: 'Poppins', sans-serif; }}
        .stApp {{ background: {PAPER}; }}
        h1, h2, h3, h4 {{ font-family: 'Lora', serif !important; color: {INK_TEXT} !important; }}
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header[data-testid="stHeader"] {{background: transparent;}}
        .block-container {{ padding-top: 1.6rem; padding-left: 3rem; padding-right: 3rem; max-width: 1300px; }}
        @media (max-width: 900px) {{
            .block-container {{ padding-left: 1.2rem; padding-right: 1.2rem; }}
        }}

        div[data-testid="stButton"] button, div[data-testid="stFormSubmitButton"] button {{
            border-radius: 999px;
            border: 1.5px solid rgba(18,32,61,0.15);
            background: {PAPER_2};
            color: {NAVY};
            font-weight: 600;
            padding: 0.5rem 1.1rem;
            transition: all 0.15s ease;
        }}
        div[data-testid="stButton"] button:hover, div[data-testid="stFormSubmitButton"] button:hover {{
            border-color: {BRASS}; color: {INK}; transform: translateY(-1px);
            box-shadow: 0 6px 14px rgba(196,155,74,0.25);
        }}
        div[data-testid="stFormSubmitButton"] button {{
            background: linear-gradient(135deg, {BRASS_LIGHT} 0%, {BRASS} 100%);
            color: {INK}; border: none; font-weight: 700; width: 100%;
        }}
        div[data-testid="stTextInput"] input {{
            border-radius: 10px !important;
            border: 1.4px solid rgba(18,32,61,0.14) !important;
            background: {PAPER_2} !important;
        }}
        div[data-testid="stTextInput"] input:focus {{
            border-color: {BRASS} !important;
            box-shadow: 0 0 0 3px rgba(196,155,74,0.18) !important;
        }}
        .auth-hero {{
            position: relative;
            background: radial-gradient(circle at 85% 15%, rgba(196,155,74,0.16) 0%, transparent 45%),
                        linear-gradient(135deg, {NAVY_2} 0%, {NAVY} 55%, {INK} 100%);
            border-radius: 22px; padding: 30px 34px; margin-bottom: 24px;
            box-shadow: 0 16px 40px rgba(11,15,26,0.35); overflow: hidden;
            text-align: center;
        }}
        .auth-logo img {{ width: 64px; height: 64px; border-radius: 50%; margin-bottom: 10px; }}
        .auth-title {{ color: #fff; font-family:'Lora',serif; font-size: 26px; font-weight: 700; margin: 4px 0; }}
        .auth-sub {{ color: #C7CEDB; font-size: 13px; max-width: 420px; margin: 6px auto 0; }}
        .auth-hero-img img {{ width: 100%; max-width: 260px; border-radius: 14px; margin-top: 16px;
            box-shadow: 0 14px 32px rgba(0,0,0,0.5); }}
        .oauth-note {{ font-size: 11.5px; color: {MUTED}; text-align: center; margin-top: 4px; }}

        /* ---------- split hero (left) / login card (right) layout ---------- */
        .auth-left-panel {{
            position: relative;
            height: 100%;
            min-height: 480px;
            background: radial-gradient(circle at 80% 10%, rgba(196,155,74,0.18) 0%, transparent 45%),
                        linear-gradient(160deg, {NAVY_2} 0%, {NAVY} 55%, {INK} 100%);
            border-radius: 22px;
            padding: 38px 34px;
            box-shadow: 0 16px 40px rgba(11,15,26,0.35);
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            text-align: center;
        }}
        .auth-left-panel .auth-logo img {{ width: 68px; height: 68px; margin-bottom: 14px; }}
        .auth-left-panel .auth-title {{ font-size: 28px; }}
        .auth-left-panel .auth-sub {{ max-width: 320px; }}
        .auth-left-panel .auth-hero-img img {{ max-width: 300px; margin-top: 26px; }}
        .login-card-heading {{
            font-family: 'Lora', serif; font-size: 21px; font-weight: 700; color: {INK_TEXT};
            text-align: center; margin-bottom: 4px;
        }}
        .login-card-sub {{
            font-size: 12.5px; color: {MUTED}; text-align: center; margin-bottom: 14px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_hero_banner():
    logo_b64 = _img_b64(LOGO_PATH)
    hero_b64 = _img_b64(HERO_PATH)
    logo_html = f'<div class="auth-logo"><img src="data:image/png;base64,{logo_b64}"/></div>' if logo_b64 else ""
    hero_html = f'<div class="auth-hero-img"><img src="data:image/png;base64,{hero_b64}"/></div>' if hero_b64 else ""
    st.markdown(
        f"""
        <div class="auth-hero">
          {logo_html}
          <div class="auth-title">Welcome to Résumé Studio</div>
          <p class="auth-sub">Sign in to build a polished, ATS-friendly resume in minutes.</p>
          {hero_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_hero_left():
    """Left-column version of the hero, used in the split login layout —
    logo, title, tagline, and the hero image stacked in a tall navy panel
    that sits beside the login/signup card instead of above it."""
    logo_b64 = _img_b64(LOGO_PATH)
    hero_b64 = _img_b64(HERO_PATH)
    logo_html = f'<div class="auth-logo"><img src="data:image/png;base64,{logo_b64}"/></div>' if logo_b64 else ""
    hero_html = f'<div class="auth-hero-img"><img src="data:image/png;base64,{hero_b64}"/></div>' if hero_b64 else ""
    st.markdown(
        f"""
        <div class="auth-left-panel">
          {logo_html}
          <div class="auth-title">Welcome to Résumé Studio</div>
          <p class="auth-sub">Sign in to build a polished, ATS-friendly resume in minutes —
          upload what you have, or start fresh.</p>
          {hero_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_features():
    """
    The 'what is this site and why should I care' section — sits below the
    login/signup card so new visitors can scroll down and learn more before
    committing, without it crowding the actual sign-in action up top.
    """
    preview_b64 = _img_b64(PREVIEW_PATH)

    st.markdown(
        f"""
        <style>
        .features-heading {{
            text-align: center; font-family: 'Lora', serif; font-size: 22px;
            font-weight: 700; color: {INK_TEXT}; margin: 8px 0 4px;
        }}
        .stats-strip {{
            display: flex; justify-content: center; gap: 0; margin: 4px 0 26px;
            background: {PAPER_2}; border: 1px solid rgba(18,32,61,0.08);
            border-radius: 16px; overflow: hidden;
            box-shadow: 0 3px 14px rgba(18,32,61,0.05);
        }}
        .stat-item {{
            flex: 1; text-align: center; padding: 16px 8px;
            border-right: 1px solid rgba(18,32,61,0.08);
        }}
        .stat-item:last-child {{ border-right: none; }}
        .stat-num {{
            font-family: 'Lora', serif; font-size: 24px; font-weight: 700; color: {NAVY};
        }}
        .stat-label {{ font-size: 10.5px; color: {MUTED}; text-transform: uppercase; letter-spacing: 1px; margin-top: 2px; }}

        .lede {{
            text-align: center; max-width: 620px; margin: 0 auto 28px;
            color: {INK_TEXT}; font-size: 15px; line-height: 1.7;
        }}
        .lede b {{ color: {NAVY}; }}

        .feature-grid {{
            display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px;
            margin-bottom: 30px;
        }}
        @media (max-width: 700px) {{ .feature-grid {{ grid-template-columns: 1fr; }} }}
        .feature-card {{
            background: {PAPER_2}; border: 1px solid rgba(18,32,61,0.08);
            border-radius: 14px; padding: 18px 16px; box-shadow: 0 3px 12px rgba(18,32,61,0.05);
            transition: all 0.15s ease;
        }}
        .feature-card:hover {{
            border-color: {BRASS}; box-shadow: 0 8px 20px rgba(196,155,74,0.18); transform: translateY(-2px);
        }}
        .feature-icon {{ font-size: 22px; margin-bottom: 8px; }}
        .feature-title {{
            font-family: 'Lora', serif; font-weight: 700; font-size: 14.5px; color: {INK_TEXT}; margin-bottom: 4px;
        }}
        .feature-desc {{ font-size: 12px; color: {MUTED}; line-height: 1.5; }}

        .preview-wrap {{
            display: flex; align-items: center; gap: 30px; margin-bottom: 24px; flex-wrap: wrap;
        }}
        .preview-img-col {{ flex: 1; min-width: 260px; text-align: center; }}
        .preview-img-col img {{ max-width: 100%; }}
        .preview-text-col {{ flex: 1; min-width: 240px; }}
        .preview-eyebrow {{
            color: {BRASS}; font-size: 11px; font-weight: 700; letter-spacing: 2px;
            text-transform: uppercase; margin-bottom: 6px;
        }}
        .preview-heading {{ font-family: 'Lora', serif; font-size: 21px; font-weight: 700; color: {INK_TEXT}; margin-bottom: 10px; }}
        .preview-list {{ font-size: 13px; color: {INK_TEXT}; line-height: 2; }}
        .preview-list li::marker {{ color: {BRASS}; }}

        .steps-row {{ display: flex; gap: 14px; margin-bottom: 26px; flex-wrap: wrap; }}
        .step-item {{ flex: 1; min-width: 180px; text-align: center; }}
        .step-num {{
            width: 34px; height: 34px; border-radius: 50%; margin: 0 auto 8px;
            background: linear-gradient(135deg, {BRASS_LIGHT}, {BRASS});
            color: {INK}; font-family:'Lora',serif; font-weight: 700; font-size: 15px;
            display: flex; align-items: center; justify-content: center;
        }}
        .step-title {{ font-family:'Lora',serif; font-weight: 700; font-size: 13.5px; color: {INK_TEXT}; margin-bottom: 3px; }}
        .step-desc {{ font-size: 11.5px; color: {MUTED}; line-height: 1.5; }}
        </style>

        <div class="features-heading">Why Résumé Studio?</div>
        <div class="lede">
            <b>Résumé Studio</b> turns a messy resume — or a blank page — into a polished,
            recruiter-ready document. Upload what you already have and we'll pull the details
            out automatically, or start fresh. Either way, you pick a style, we build a
            single-column, ATS-safe .docx, and you can check exactly how well it will score
            before you send it anywhere.
        </div>

        <div class="stats-strip">
            <div class="stat-item"><div class="stat-num">23</div><div class="stat-label">Templates</div></div>
            <div class="stat-item"><div class="stat-num">3</div><div class="stat-label">Style Tiers</div></div>
            <div class="stat-item"><div class="stat-num">0–100</div><div class="stat-label">ATS Score</div></div>
            <div class="stat-item"><div class="stat-num">100%</div><div class="stat-label">Table-Free Layout</div></div>
        </div>

        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">📤</div>
                <div class="feature-title">Upload &amp; Auto-Fill</div>
                <div class="feature-desc">Drop in your existing resume (.pdf or .docx) and we pre-fill the form —
                contact info, skills, jobs, and education — so you only fix what needs fixing.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎨</div>
                <div class="feature-title">Simple, Professional &amp; Premium</div>
                <div class="feature-desc">23 templates across three styles. Every generation picks a fresh
                template from your chosen tier — you won't get the same look twice in a row.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔎</div>
                <div class="feature-title">ATS Score Check</div>
                <div class="feature-desc">One click scores your resume 0–100 across 8 criteria — contact
                completeness, action verbs, quantified results, and more — with tips to improve it.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">✍️</div>
                <div class="feature-title">Fill In Manually</div>
                <div class="feature-desc">Prefer to start clean? Build every section — summary, skills,
                experience, education — from scratch with a guided form.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🧭</div>
                <div class="feature-title">Single-Column, ATS-Safe</div>
                <div class="feature-desc">No tables, no text boxes, no multi-column layouts that scramble an
                applicant tracking system's reading order — just clean, parseable text.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">⬇️</div>
                <div class="feature-title">Instant .docx Download</div>
                <div class="feature-desc">Get a ready-to-send Word document in seconds, styled and formatted —
                no manual cleanup needed.</div>
            </div>
        </div>

        <div class="steps-row">
            <div class="step-item"><div class="step-num">1</div>
                <div class="step-title">Upload or Fill In</div>
                <div class="step-desc">Start from an existing resume or a blank form.</div></div>
            <div class="step-item"><div class="step-num">2</div>
                <div class="step-title">Pick a Style</div>
                <div class="step-desc">Simple, Professional, or Premium — your choice.</div></div>
            <div class="step-item"><div class="step-num">3</div>
                <div class="step-title">Generate</div>
                <div class="step-desc">We build a polished, ATS-safe .docx in seconds.</div></div>
            <div class="step-item"><div class="step-num">4</div>
                <div class="step-title">Check &amp; Download</div>
                <div class="step-desc">Run the ATS score, then download and apply.</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if preview_b64:
        st.markdown(
            f"""
            <div class="preview-wrap">
              <div class="preview-img-col">
                <img src="data:image/png;base64,{preview_b64}"/>
              </div>
              <div class="preview-text-col">
                <div class="preview-eyebrow">See it in action</div>
                <div class="preview-heading">A resume that actually looks premium</div>
                <ul class="preview-list">
                  <li>Full-bleed color header banners &amp; refined typography</li>
                  <li>Consistent, professional structure recruiters recognize</li>
                  <li>Every template stays single-column and ATS-parseable</li>
                  <li>Generated from your real details — not a generic mockup</li>
                </ul>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()


def _oauth_buttons():
    google_ok = _oauth_configured("google")
    fb_ok = _oauth_configured("facebook")
    if not (google_ok or fb_ok):
        return
    st.markdown(
        f"<div style='text-align:center;color:{MUTED};font-size:12.5px;margin:14px 0 8px;'>— or continue with —</div>",
        unsafe_allow_html=True,
    )
    cols = st.columns(2) if (google_ok and fb_ok) else st.columns(1)
    i = 0
    if google_ok:
        with cols[i]:
            st.link_button("🔵 Continue with Google", _google_auth_url(), use_container_width=True)
        i += 1
    if fb_ok:
        with cols[i]:
            st.link_button("🔷 Continue with Facebook", _facebook_auth_url(), use_container_width=True)
    st.markdown(
        "<div class='oauth-note'>We only use your provider account to verify who you are — "
        "no separate signup needed.</div>",
        unsafe_allow_html=True,
    )


def _login_form():
    with st.form("login_form"):
        email = st.text_input("Email (used as your user id)")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log In")
    if submitted:
        if not EMAIL_RE.match(email.strip()):
            st.error("Please enter a valid email address.")
            return
        user = find_user_by_email(email)
        if user is None:
            st.error("No account found with this email. Please sign up first.")
            return
        if user["auth_provider"] != "password" or not user["password_hash"]:
            st.error(f"This email is registered via {user['auth_provider'].title()}. Use that button below instead.")
            return
        if not _verify_password(password, user["password_hash"]):
            st.error("Incorrect password.")
            return
        notify_admin("Login", user)
        st.session_state["auth_user"] = _public_user(user)
        st.rerun()

    _oauth_buttons()


def _signup_form():
    with st.form("signup_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email (this will be your user id)")
        mobile = st.text_input("Mobile Number")
        password = st.text_input("Create a Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Sign Up")
    if submitted:
        if not name.strip():
            st.error("Please enter your name.")
            return
        if not EMAIL_RE.match(email.strip()):
            st.error("Please enter a valid email address.")
            return
        if not MOBILE_RE.match(mobile.strip()):
            st.error("Please enter a valid mobile number.")
            return
        if len(password) < 6:
            st.error("Password must be at least 6 characters.")
            return
        if password != confirm:
            st.error("Passwords don't match.")
            return

        existing = find_user_by_email(email)
        if existing is not None:
            st.warning(
                f"You have already signed up with this email ({email}). "
                "Please use the **Log In** tab instead."
            )
            return

        user = create_user(name=name, email=email, mobile=mobile, password=password, provider="password")
        notify_admin("New signup", user)
        st.success("Account created! You're now logged in.")
        st.session_state["auth_user"] = _public_user(user)
        st.rerun()

    _oauth_buttons()


def render_auth_page():
    _inject_css()

    if st.session_state.get("_auth_error"):
        st.error(st.session_state.pop("_auth_error"))
    for w in st.session_state.pop("_notify_warnings", []):
        st.caption(f"⚠️ {w}")  # non-blocking — visible but doesn't stop login

    # Split layout: hero image + branding on the left, login/signup card on
    # the right — instead of a centered stack with wasted space either side.
    hero_col, form_col = st.columns([1.1, 1], gap="large")
    with hero_col:
        _render_hero_left()
    with form_col:
        with st.container(border=True):
            st.markdown('<div class="login-card-heading">Get Started</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="login-card-sub">Log in to your account, or sign up in a few seconds.</div>',
                unsafe_allow_html=True,
            )
            tab_login, tab_signup = st.tabs(["Log In", "Sign Up"])
            with tab_login:
                _login_form()
            with tab_signup:
                _signup_form()

    st.write("")
    _render_features()


def render_logout_control():
    """Small 'logged in as ...' strip with a logout button. Call this from
    app.py once the person is past the login gate, wherever you'd like it
    to show up (e.g. right under the hero section)."""
    user = st.session_state.get("auth_user")
    if not user:
        return
    c1, c2 = st.columns([5, 1])
    with c1:
        st.caption(f"Logged in as **{user['name']}** ({user['email']})")
    with c2:
        if st.button("Log out", key="auth_logout_btn"):
            st.session_state.pop("auth_user", None)
            st.rerun()


def require_login() -> bool:
    """
    Call this at the very top of app.py. Returns True if the person is
    logged in (safe to continue rendering the app); otherwise renders the
    login/signup page and returns False (caller should st.stop()).
    """
    _handle_oauth_redirect()
    if st.session_state.get("auth_user"):
        return True
    render_auth_page()
    return False
