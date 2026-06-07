import streamlit as st
import json
import random
from datetime import datetime

st.set_page_config(
    page_title="UAE Health Insurance Training Academy",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── UI theme state ────────────────────────────────────────────────────────────
if "ui_theme" not in st.session_state:
    st.session_state.ui_theme = "Dark"
if "light_mode_switch" not in st.session_state:
    st.session_state.light_mode_switch = False

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
  --bg: #0d0f14;
  --surface: rgba(255,255,255,0.04);
  --surface-2: rgba(255,255,255,0.07);
  --border: rgba(255,255,255,0.09);
  --border-2: rgba(255,255,255,0.14);
  --text-1: #f0f2f8;
  --text-2: #9aa3b8;
  --text-3: #5c6480;
  --accent-blue: #4f9cf9;
  --accent-cyan: #22d3c5;
  --accent-coral: #ff6b6b;
  --accent-violet: #a78bfa;
  --accent-pink: #f472b6;
  --accent-amber: #fbbf24;
  --accent-green: #34d399;
  --radius-lg: 16px;
  --radius-md: 10px;
  --radius-sm: 6px;
}

html, body, [class*="css"] {
  font-family: 'Inter', 'DM Sans', sans-serif;
  background: var(--bg) !important;
  color: var(--text-1) !important;
}

.stApp { background: var(--bg) !important; }


/* App shell */
[data-testid="stHeader"] {
  background: rgba(13,15,20,0.96) !important;
  border-bottom: 1px solid rgba(255,255,255,0.04) !important;
}
[data-testid="stToolbar"] { right: 0.8rem !important; }
.block-container {
  max-width: 1320px !important;
  padding-top: 3.6rem !important;
  padding-bottom: 3rem !important;
}
[data-testid="stSidebarContent"] { padding-top: 1.35rem !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] label {
  border-radius: 8px;
  padding: 0.18rem 0.42rem;
  transition: background 0.15s ease, transform 0.15s ease;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
  background: rgba(79,156,249,0.08);
  transform: translateX(2px);
}

/* Hero typography */
.hero-kicker {
  font-size: 0.72rem; color: #75b7ff; font-weight: 700;
  letter-spacing: 0.14em; text-transform: uppercase; margin-bottom: 10px;
}
.hero-title { font-size: 2.45rem; font-weight: 800; line-height: 1.14; margin-bottom: 12px; letter-spacing: -0.035em; }
.hero-gradient {
  background: linear-gradient(90deg,#62a9ff,#38dfd1);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-copy { font-size: 0.96rem; color: #a9b3c7; max-width: 720px; line-height: 1.7; }
.hero-chip-row { display:flex; gap:8px; flex-wrap:wrap; margin-top:18px; }
.hero-chip {
  display:inline-flex; align-items:center; gap:6px; padding:5px 10px;
  border-radius:999px; font-size:0.72rem; font-weight:600; color:#b9c5d8;
  background:rgba(255,255,255,0.055); border:1px solid rgba(255,255,255,0.09);
}

/* Learning module cards */
.module-card {
  display:flex; align-items:center; gap:16px; padding:1rem 1.2rem;
  background:linear-gradient(135deg, rgba(255,255,255,0.045), rgba(255,255,255,0.025));
}
.module-icon {
  width:42px; height:42px; border-radius:12px; display:flex; align-items:center;
  justify-content:center; font-size:1.25rem; background:rgba(79,156,249,0.08);
  border:1px solid rgba(79,156,249,0.12);
}
.module-title { font-weight:650; font-size:0.94rem; }
.module-desc { font-size:0.78rem; color:#9aa3b8; margin-top:3px; }
.module-status { font-size:0.74rem; font-weight:650; white-space:nowrap; }

@media (max-width: 860px) {
  .block-container { padding-top: 3.2rem !important; padding-left: 1rem !important; padding-right: 1rem !important; }
  .hero-card { padding: 1.45rem 1.35rem !important; }
  .hero-title { font-size: 1.95rem; }
  .hero-copy { font-size: 0.9rem; }
  .module-card { gap: 11px; padding: 0.9rem 0.95rem; }
  .module-icon { width: 36px; height: 36px; }
}

/* Orb background */
.bg-orbs {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  pointer-events: none; z-index: 0; overflow: hidden;
}
.orb {
  position: absolute; border-radius: 50%;
  filter: blur(80px); opacity: 0.12;
  animation: orb-drift 20s ease-in-out infinite alternate;
}
.orb-1 { width:500px; height:500px; background:#4f9cf9; top:-100px; left:-100px; animation-duration:18s; }
.orb-2 { width:400px; height:400px; background:#a78bfa; top:30%; right:-80px; animation-duration:22s; animation-delay:-5s; }
.orb-3 { width:350px; height:350px; background:#22d3c5; bottom:10%; left:25%; animation-duration:25s; animation-delay:-10s; }
.orb-4 { width:300px; height:300px; background:#f472b6; top:60%; right:30%; animation-duration:20s; animation-delay:-8s; }
@keyframes orb-drift { 0%{transform:translate(0,0) scale(1);} 100%{transform:translate(40px,30px) scale(1.08);} }

/* Sidebar */
[data-testid="stSidebar"] {
  background: rgba(13,15,20,0.92) !important;
  border-right: 1px solid var(--border) !important;
  backdrop-filter: blur(20px) !important;
}
[data-testid="stSidebar"] * { color: var(--text-1) !important; }

/* Cards */
.glass-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.4rem 1.6rem;
  backdrop-filter: blur(12px);
  transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
  margin-bottom: 1rem;
}
.glass-card:hover {
  transform: translateY(-2px);
  border-color: var(--border-2);
  box-shadow: 0 8px 32px rgba(0,0,0,0.35);
}

/* Hero card */
.hero-card {
  position: relative; overflow: hidden;
  background: linear-gradient(135deg, rgba(79,156,249,0.15) 0%, rgba(167,139,250,0.10) 52%, rgba(34,211,197,0.09) 100%);
  border: 1px solid rgba(99,169,255,0.24);
  border-radius: 22px;
  padding: 2.25rem 2.55rem;
  margin-bottom: 1.25rem;
  box-shadow: 0 18px 45px rgba(0,0,0,0.18);
}
.hero-card::after {
  content: ""; position:absolute; width:260px; height:260px; right:-85px; top:-105px;
  border-radius:50%; background:radial-gradient(circle, rgba(34,211,197,0.20), transparent 68%);
  pointer-events:none;
}

/* Metric cards */
.metric-row { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 1.2rem; }
.metric-card {
  background: linear-gradient(145deg, rgba(255,255,255,0.072), rgba(255,255,255,0.04));
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.05rem 1.2rem;
  min-width: 130px; flex: 1;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.025);
  transition: transform 0.15s ease, border-color 0.15s ease;
}
.metric-card:hover { transform: translateY(-2px); border-color: rgba(79,156,249,0.22); }
.metric-val { font-size: 1.75rem; font-weight: 700; line-height: 1.1; }
.metric-lbl { font-size: 0.72rem; color: var(--text-2); text-transform: uppercase; letter-spacing: 0.06em; margin-top: 4px; }

/* Badges */
.badge {
  display: inline-block; padding: 2px 10px; border-radius: 20px;
  font-size: 0.72rem; font-weight: 600; letter-spacing: 0.04em;
}
.badge-blue { background: rgba(79,156,249,0.15); color: #7bb9fb; border: 1px solid rgba(79,156,249,0.25); }
.badge-cyan { background: rgba(34,211,197,0.12); color: #22d3c5; border: 1px solid rgba(34,211,197,0.2); }
.badge-coral { background: rgba(255,107,107,0.12); color: #ff8080; border: 1px solid rgba(255,107,107,0.2); }
.badge-violet { background: rgba(167,139,250,0.12); color: #c4b5fd; border: 1px solid rgba(167,139,250,0.2); }
.badge-amber { background: rgba(251,191,36,0.12); color: #fcd34d; border: 1px solid rgba(251,191,36,0.2); }
.badge-green { background: rgba(52,211,153,0.12); color: #6ee7b7; border: 1px solid rgba(52,211,153,0.2); }

/* Section headings */
.section-title {
  font-size: 1.5rem; font-weight: 700;
  background: linear-gradient(90deg, #f0f2f8 0%, #9aa3b8 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  margin-bottom: 0.25rem;
}
.section-sub { font-size: 0.9rem; color: var(--text-2); margin-bottom: 1.5rem; }

/* Tables */
.styled-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
.styled-table th {
  background: rgba(79,156,249,0.1); color: #7bb9fb;
  padding: 10px 14px; text-align: left; border-bottom: 1px solid rgba(79,156,249,0.2);
  font-weight: 600; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em;
}
.styled-table td { padding: 9px 14px; border-bottom: 1px solid var(--border); color: var(--text-1); vertical-align: top; }
.styled-table tr:hover td { background: var(--surface); }

/* Disclaimer box */
.disclaimer {
  background: rgba(251,191,36,0.06);
  border: 1px solid rgba(251,191,36,0.2);
  border-left: 3px solid var(--accent-amber);
  border-radius: var(--radius-md);
  padding: 0.9rem 1.2rem;
  font-size: 0.82rem; color: #d4a843;
  margin-bottom: 1rem;
}

/* Progress bar */
.prog-bar-bg {
  background: var(--surface-2); border-radius: 8px; height: 6px;
  overflow: hidden; margin-top: 6px;
}
.prog-bar-fill {
  height: 100%; border-radius: 8px;
  background: linear-gradient(90deg, #4f9cf9, #22d3c5);
  transition: width 0.4s ease;
}

/* Tabs override */
.stTabs [data-baseweb="tab-list"] {
  background: var(--surface) !important;
  border-radius: var(--radius-md) !important;
  border: 1px solid var(--border) !important;
  gap: 4px; padding: 4px;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text-2) !important;
  font-size: 0.84rem !important;
}
.stTabs [aria-selected="true"] {
  background: rgba(79,156,249,0.18) !important;
  color: #7bb9fb !important;
}

/* Expander */
[data-testid="stExpander"] {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-md) !important;
}

/* Buttons */
.stButton > button {
  background: rgba(79,156,249,0.12) !important;
  border: 1px solid rgba(79,156,249,0.3) !important;
  color: #7bb9fb !important;
  border-radius: var(--radius-sm) !important;
  font-weight: 500 !important;
  transition: transform 0.12s ease, background 0.15s ease !important;
}
.stButton > button:hover {
  background: rgba(79,156,249,0.22) !important;
  transform: translateY(-1px) !important;
}
.stButton > button:active { transform: scale(0.97) !important; }

/* Radio */
.stRadio [data-testid="stMarkdownContainer"] p { color: var(--text-1) !important; }

/* Input fields */
.stTextInput input, .stSelectbox select {
  background: var(--surface-2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--text-1) !important;
}

/* Streamlit default elements dark override */
p, li, span { color: var(--text-1); }
h1,h2,h3,h4 { color: var(--text-1) !important; }
.stMarkdown { color: var(--text-1) !important; }

/* Alert boxes */
.info-box {
  background: rgba(79,156,249,0.08);
  border: 1px solid rgba(79,156,249,0.18);
  border-left: 3px solid var(--accent-blue);
  border-radius: var(--radius-md);
  padding: 0.9rem 1.2rem; margin-bottom: 1rem;
  font-size: 0.875rem;
}
.warning-box {
  background: rgba(255,107,107,0.08);
  border: 1px solid rgba(255,107,107,0.18);
  border-left: 3px solid var(--accent-coral);
  border-radius: var(--radius-md);
  padding: 0.9rem 1.2rem; margin-bottom: 1rem;
  font-size: 0.875rem;
}
.success-box {
  background: rgba(52,211,153,0.08);
  border: 1px solid rgba(52,211,153,0.18);
  border-left: 3px solid var(--accent-green);
  border-radius: var(--radius-md);
  padding: 0.9rem 1.2rem; margin-bottom: 1rem;
  font-size: 0.875rem;
}

/* Timeline */
.timeline-item {
  display: flex; gap: 14px; margin-bottom: 1rem; align-items: flex-start;
}
.timeline-dot {
  width: 28px; height: 28px; border-radius: 50%; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.75rem; font-weight: 700; margin-top: 2px;
}

@media (prefers-reduced-motion: reduce) {
  .orb, .glass-card, .metric-card, .stButton > button { animation: none !important; transition: none !important; }
}


/* Branded shell, navigation links and microinteractions */
.brand-card {
  display:flex; align-items:center; gap:10px; padding:10px 10px 12px;
  border-radius:16px; margin:0 0 10px;
  background:linear-gradient(135deg, rgba(79,156,249,.12), rgba(244,114,182,.07), rgba(34,211,197,.08));
  border:1px solid rgba(125,170,255,.16);
  box-shadow: inset 0 1px 0 rgba(255,255,255,.05);
}
.brand-logo {
  width:42px; height:42px; border-radius:15px; display:flex; align-items:center; justify-content:center;
  background:linear-gradient(135deg,#4f9cf9 0%,#22d3c5 52%,#f472b6 100%);
  box-shadow:0 8px 24px rgba(79,156,249,.22), inset 0 1px 0 rgba(255,255,255,.42);
  position:relative; flex:0 0 auto;
}
.brand-logo::before { content:"✚"; color:white; font-size:1.18rem; font-weight:800; text-shadow:0 2px 6px rgba(0,0,0,.18); }
.brand-logo::after { content:""; position:absolute; inset:7px; border:1px solid rgba(255,255,255,.56); border-radius:10px; }
.brand-name {font-size:.95rem;font-weight:780;letter-spacing:-.02em;line-height:1.05;}
.brand-by {font-size:.69rem;color:var(--text-3);margin-top:4px;}
.brand-email {font-size:.66rem;color:var(--text-2);margin-top:3px;}
.brand-email a {color:var(--accent-blue)!important;text-decoration:none;}
.module-link { text-decoration:none!important; display:block; color:inherit!important; }
.module-link .module-card { cursor:pointer; position:relative; overflow:hidden; }
.module-link .module-card::after {
  content:"Open →"; position:absolute; right:18px; bottom:11px; opacity:0;
  color:var(--page-accent, #4f9cf9); font-size:.68rem; font-weight:700;
  transform:translateX(-8px); transition:opacity .18s ease, transform .18s ease;
}
.module-link:hover .module-card::after { opacity:1; transform:translateX(0); }
.module-link:hover .module-card { transform:translateY(-4px) scale(1.004); }
.page-accent-bar {height:3px;border-radius:99px;margin:-.5rem 0 1.1rem;background:linear-gradient(90deg,var(--page-accent),transparent 78%);opacity:.82;}
.card-title {font-size:1rem;font-weight:750;margin-bottom:.8rem;letter-spacing:-.012em;}
.source-note {font-size:.74rem;color:var(--text-3);line-height:1.55;margin-top:.75rem;}
.source-note a {color:var(--accent-blue)!important;text-decoration:none;}
[data-testid="stSidebar"] [data-testid="stToggle"] {margin:.15rem 0 .85rem;}

/* Light glass theme inspired by the pastel interface mock-up. Dark stays the default. */
html[data-app-theme="light"], html[data-app-theme="light"] body { background:#f4f7fc!important; }
.light-ui .stApp {
  background:
    radial-gradient(circle at 16% 13%, rgba(34,211,197,.16), transparent 24%),
    radial-gradient(circle at 82% 12%, rgba(244,114,182,.15), transparent 26%),
    radial-gradient(circle at 62% 88%, rgba(167,139,250,.16), transparent 28%),
    linear-gradient(135deg,#f7fbff 0%,#f8f5ff 50%,#fff9f5 100%)!important;
}
.light-ui [data-testid="stHeader"] {background:rgba(255,255,255,.68)!important;border-bottom:1px solid rgba(80,100,145,.1)!important;backdrop-filter:blur(24px)!important;}
.light-ui [data-testid="stSidebar"] {background:rgba(255,255,255,.62)!important;border-right:1px solid rgba(83,102,145,.13)!important;backdrop-filter:blur(28px)!important;}
.light-ui [data-testid="stSidebar"] * {color:#22304a!important;}
.light-ui .glass-card, .light-ui .metric-card, .light-ui .hero-card {
  background:linear-gradient(135deg,rgba(255,255,255,.72),rgba(255,255,255,.44))!important;
  border-color:rgba(91,111,155,.16)!important;
  box-shadow:0 14px 40px rgba(78,101,148,.10), inset 0 1px 0 rgba(255,255,255,.78)!important;
}
.light-ui .hero-card {background:linear-gradient(135deg,rgba(255,255,255,.8),rgba(237,245,255,.66),rgba(255,244,250,.62))!important;}
.light-ui p, .light-ui li, .light-ui span, .light-ui h1, .light-ui h2, .light-ui h3, .light-ui h4, .light-ui .stMarkdown {color:#1f2b43!important;}
.light-ui .section-sub, .light-ui .module-desc, .light-ui .hero-copy, .light-ui .source-note {color:#66738c!important;}
.light-ui .styled-table td {color:#27344d!important;border-bottom-color:rgba(80,103,146,.12)!important;}
.light-ui .styled-table th {border-bottom-color:rgba(80,103,146,.16)!important;}
.light-ui .info-box {background:rgba(79,156,249,.08)!important;color:#29496f!important;}
.light-ui .warning-box {background:rgba(255,107,107,.08)!important;color:#6a3342!important;}
.light-ui .success-box {background:rgba(52,211,153,.09)!important;color:#245d4d!important;}
.light-ui .disclaimer {background:rgba(251,191,36,.10)!important;color:#76591b!important;}
.light-ui .hero-chip {background:rgba(255,255,255,.62)!important;border-color:rgba(88,108,150,.13)!important;color:#4e5f7d!important;}
.light-ui .orb {opacity:.16!important;filter:blur(95px)!important;}
.light-ui .stTabs [data-baseweb="tab-list"] {background:rgba(255,255,255,.54)!important;border-color:rgba(80,103,146,.14)!important;}
.light-ui .stTabs [aria-selected="true"] {background:rgba(79,156,249,.13)!important;color:#236ab1!important;}
.light-ui .stTextInput input, .light-ui .stSelectbox select {background:rgba(255,255,255,.7)!important;color:#24324b!important;border-color:rgba(80,103,146,.16)!important;}
.light-ui .brand-card {background:linear-gradient(135deg,rgba(255,255,255,.78),rgba(238,247,255,.62),rgba(255,242,249,.55));border-color:rgba(91,111,155,.14);}

</style>

<div class="bg-orbs">
  <div class="orb orb-1"></div>
  <div class="orb orb-2"></div>
  <div class="orb orb-3"></div>
  <div class="orb orb-4"></div>
</div>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "progress" not in st.session_state:
    st.session_state.progress = {
        "foundations": False, "exclusions": False, "claims": False,
        "coding": False, "preex": False, "inpatient": False,
        "audit": False, "specialty": False, "cases": False,
        "quiz": False
    }
if "quiz_scores" not in st.session_state:
    st.session_state.quiz_scores = {}
if "disclaimer_accepted" not in st.session_state:
    st.session_state.disclaimer_accepted = False

completed = sum(1 for v in st.session_state.progress.values() if v)

# ── Sidebar, routes and visual mode ───────────────────────────────────────────
NAV_OPTIONS = [
    "🏠  Home & Dashboard",
    "🌍  UAE Insurance Landscape",
    "🚫  Exclusions Reference",
    "📋  Claims Processing",
    "🔢  Medical Coding",
    "🔍  Pre-existing Conditions",
    "🏥  Inpatient & Emergency",
    "🔎  Internal Audit",
    "💊  Specialty Rules",
    "🎯  Case Studies",
    "📝  Knowledge Quiz",
    "📚  Resources",
    "🩺  Procedures, Dental & Vaccines",
]
SLUG_TO_NAV = {
    "home": NAV_OPTIONS[0], "landscape": NAV_OPTIONS[1], "exclusions": NAV_OPTIONS[2],
    "claims": NAV_OPTIONS[3], "coding": NAV_OPTIONS[4], "preex": NAV_OPTIONS[5],
    "inpatient": NAV_OPTIONS[6], "audit": NAV_OPTIONS[7], "specialty": NAV_OPTIONS[8],
    "cases": NAV_OPTIONS[9], "quiz": NAV_OPTIONS[10], "resources": NAV_OPTIONS[11],
    "procedures": NAV_OPTIONS[12],
}
NAV_TO_SLUG = {label: slug for slug, label in SLUG_TO_NAV.items()}
requested_slug = st.query_params.get("page", "home")
if isinstance(requested_slug, list):
    requested_slug = requested_slug[0]
requested_slug = requested_slug if requested_slug in SLUG_TO_NAV else "home"
if "nav_choice" not in st.session_state:
    st.session_state.nav_choice = SLUG_TO_NAV[requested_slug]
if st.session_state.get("_last_route") != requested_slug:
    st.session_state.nav_choice = SLUG_TO_NAV[requested_slug]
    st.session_state._last_route = requested_slug

with st.sidebar:
    st.markdown("""
    <div class="brand-card">
      <div class="brand-logo"></div>
      <div>
        <div class="brand-name">UAE Insurance Academy</div>
        <div class="brand-by">Designed & curated by Rana Musab Bin Tariq</div>
        <div class="brand-email">PharmD · MSc Digital Health<br/>Deggendorf Institute of Technology</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    light_mode = st.toggle("☀️ Light glass interface", key="light_mode_switch")
    desired_theme = "Light" if light_mode else "Dark"
    if st.session_state.ui_theme != desired_theme:
        st.session_state.ui_theme = desired_theme
        st.rerun()

    pct = int(completed / len(st.session_state.progress) * 100)
    st.markdown(f"""
    <div style="margin-bottom:1.2rem;">
      <div style="display:flex;justify-content:space-between;font-size:0.78rem;color:#9aa3b8;margin-bottom:4px;">
        <span>Overall Progress</span><span style="color:#4f9cf9;font-weight:600;">{pct}%</span>
      </div>
      <div class="prog-bar-bg"><div class="prog-bar-fill" style="width:{pct}%"></div></div>
    </div>
    """, unsafe_allow_html=True)

    nav = st.radio("", NAV_OPTIONS, key="nav_choice", label_visibility="collapsed")

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.72rem;color:#5c6480;line-height:1.7;">
      <a href="https://www.linkedin.com/in/rana-musab-bin-tariq-a70982152/" target="_blank" style="color:#4f9cf9;text-decoration:none;">🔗 LinkedIn Profile</a><br/>
      <a href="https://github.com/RanaMusabBinTariq" target="_blank" style="color:#4f9cf9;text-decoration:none;">💻 GitHub</a>
    </div>
    """, unsafe_allow_html=True)

current_slug = NAV_TO_SLUG.get(nav, "home")
if st.query_params.get("page", "home") != current_slug:
    st.query_params["page"] = current_slug
    st.session_state._last_route = current_slug

PAGE_ACCENTS = {
    "home": ("#4f9cf9", "rgba(79,156,249,.13)"), "landscape": ("#22d3c5", "rgba(34,211,197,.13)"),
    "exclusions": ("#ff6b6b", "rgba(255,107,107,.13)"), "claims": ("#fbbf24", "rgba(251,191,36,.13)"),
    "coding": ("#a78bfa", "rgba(167,139,250,.14)"), "preex": ("#f472b6", "rgba(244,114,182,.13)"),
    "inpatient": ("#34d399", "rgba(52,211,153,.13)"), "audit": ("#fb923c", "rgba(251,146,60,.13)"),
    "specialty": ("#ec4899", "rgba(236,72,153,.13)"), "cases": ("#06b6d4", "rgba(6,182,212,.13)"),
    "quiz": ("#8b5cf6", "rgba(139,92,246,.13)"), "resources": ("#0ea5e9", "rgba(14,165,233,.13)"),
    "procedures": ("#14b8a6", "rgba(20,184,166,.13)"),
}
page_accent, page_accent_soft = PAGE_ACCENTS[current_slug]
light_theme_css = """
<style>
:root {
  --bg:#f4f7fc; --surface:rgba(255,255,255,.66); --surface-2:rgba(255,255,255,.78);
  --border:rgba(86,106,148,.15); --border-2:rgba(86,106,148,.24);
  --text-1:#1f2b43; --text-2:#66738c; --text-3:#7c879c;
}
html, body, [class*="css"] { background:#f4f7fc!important; color:#1f2b43!important; }
.stApp {
  background:
    radial-gradient(circle at 16% 13%, rgba(34,211,197,.16), transparent 24%),
    radial-gradient(circle at 82% 12%, rgba(244,114,182,.15), transparent 26%),
    radial-gradient(circle at 62% 88%, rgba(167,139,250,.16), transparent 28%),
    linear-gradient(135deg,#f7fbff 0%,#f8f5ff 50%,#fff9f5 100%)!important;
}
[data-testid="stHeader"] {background:rgba(255,255,255,.68)!important;border-bottom:1px solid rgba(80,100,145,.1)!important;backdrop-filter:blur(24px)!important;}
[data-testid="stSidebar"] {background:rgba(255,255,255,.62)!important;border-right:1px solid rgba(83,102,145,.13)!important;backdrop-filter:blur(28px)!important;}
[data-testid="stSidebar"] * {color:#22304a!important;}
.glass-card, .metric-card, .hero-card {
  background:linear-gradient(135deg,rgba(255,255,255,.72),rgba(255,255,255,.44))!important;
  border-color:rgba(91,111,155,.16)!important;
  box-shadow:0 14px 40px rgba(78,101,148,.10), inset 0 1px 0 rgba(255,255,255,.78)!important;
}
.hero-card {background:linear-gradient(135deg,rgba(255,255,255,.8),rgba(237,245,255,.66),rgba(255,244,250,.62))!important;}
p, li, span, h1, h2, h3, h4, .stMarkdown {color:#1f2b43!important;}
.section-sub, .module-desc, .hero-copy, .source-note {color:#66738c!important;}
.styled-table td {color:#27344d!important;border-bottom-color:rgba(80,103,146,.12)!important;}
.styled-table th {border-bottom-color:rgba(80,103,146,.16)!important;}
.info-box {background:rgba(79,156,249,.08)!important;color:#29496f!important;}
.warning-box {background:rgba(255,107,107,.08)!important;color:#6a3342!important;}
.success-box {background:rgba(52,211,153,.09)!important;color:#245d4d!important;}
.disclaimer {background:rgba(251,191,36,.10)!important;color:#76591b!important;}
.hero-chip {background:rgba(255,255,255,.62)!important;border-color:rgba(88,108,150,.13)!important;color:#4e5f7d!important;}
.orb {opacity:.16!important;filter:blur(95px)!important;}
.stTabs [data-baseweb="tab-list"] {background:rgba(255,255,255,.54)!important;border-color:rgba(80,103,146,.14)!important;}
.stTabs [aria-selected="true"] {background:rgba(79,156,249,.13)!important;color:#236ab1!important;}
.stTextInput input, .stSelectbox select {background:rgba(255,255,255,.7)!important;color:#24324b!important;border-color:rgba(80,103,146,.16)!important;}
.brand-card {background:linear-gradient(135deg,rgba(255,255,255,.78),rgba(238,247,255,.62),rgba(255,242,249,.55))!important;border-color:rgba(91,111,155,.14)!important;}
</style>
""" if st.session_state.ui_theme == "Light" else ""
st.markdown(light_theme_css, unsafe_allow_html=True)
st.markdown(f"""
<style>
:root {{ --page-accent:{page_accent}; --page-accent-soft:{page_accent_soft}; }}
.section-title {{ background:linear-gradient(90deg,var(--page-accent),var(--text-1)); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }}
.styled-table th {{ background:var(--page-accent-soft)!important; color:var(--page-accent)!important; }}
.glass-card:hover {{ border-color:var(--page-accent)!important; box-shadow:0 15px 42px {page_accent_soft}; }}
.module-icon {{ background:var(--page-accent-soft); border-color:var(--page-accent-soft); }}
</style>
<div class="page-accent-bar"></div>
""", unsafe_allow_html=True)

# ── Disclaimer modal ──────────────────────────────────────────────────────────
if not st.session_state.disclaimer_accepted:
    st.markdown("""
    <div style="max-width:680px;margin:3rem auto;">
      <div class="glass-card" style="border-color:rgba(251,191,36,0.3);padding:2rem;">
        <div style="font-size:1.3rem;font-weight:700;margin-bottom:0.5rem;">⚠️ Important Disclaimer</div>
    """, unsafe_allow_html=True)
    st.markdown("""
**This application is a training and educational resource only.**

- All content is provided for learning purposes and does not constitute medical, legal, or insurance advice.
- Clinical and coverage decisions must always be based on the treating physician's medical judgment, the patient's complete medical file, and the applicable policy terms and conditions (TOB).
- DHA, HAAD/DOH, MOH, and other regulatory rules referenced are generalised summaries. Always verify with the current official circulars before applying in practice.
- No insurance company names or proprietary internal documents are disclosed or reproduced. Content derived from professional experience and publicly available regulatory frameworks.
- The creator assumes no liability for decisions made based on content presented in this app.

**By continuing, you acknowledge this is a training tool and not a clinical or legal decision-making system.**
    """)
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("✅ I Understand — Continue", use_container_width=True):
            st.session_state.disclaimer_accepted = True
            st.rerun()
    st.stop()

# ── Compact branded masthead ──────────────────────────────────────────────────
st.markdown("""
<div style="display:flex;align-items:center;gap:10px;margin:0 0 1rem;">
  <div class="brand-logo" style="width:36px;height:36px;border-radius:13px;"></div>
  <div>
    <div style="font-size:.76rem;font-weight:800;letter-spacing:.12em;color:var(--page-accent);text-transform:uppercase;">UAE Insurance Academy</div>
    <div style="font-size:.69rem;color:var(--text-3);">Educational app by Rana Musab Bin Tariq · PharmD · MSc Digital Health, Deggendorf Institute of Technology</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — HOME
# ══════════════════════════════════════════════════════════════════════════════
if nav == "🏠  Home & Dashboard":
    st.markdown("""
    <div class="hero-card">
      <div class="hero-kicker">UAE HEALTH INSURANCE TRAINING ACADEMY</div>
      <div class="hero-title">
        Explore UAE Health Insurance<br/>
        <span class="hero-gradient">Through Practical Learning</span>
      </div>
      <div class="hero-copy">
        A structured educational resource for doctors, pharmacists, physiotherapists, and healthcare
        professionals who want to build familiarity with common UAE health insurance concepts,
        workflows, terminology, and reference material.
      </div>
      <div class="hero-chip-row">
        <span class="hero-chip">📘 Educational resource</span>
        <span class="hero-chip">🧭 12 learning modules</span>
        <span class="hero-chip">🇦🇪 UAE context</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer">
      ⚠️ <strong>Training Tool Only.</strong> Content is educational. All coverage and clinical decisions
      must be based on the patient's complete medical file, applicable policy TOB, and the judgment of
      a qualified medical professional. Always verify with official DHA/HAAD/MOH circulars.
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-val" style="color:#4f9cf9;">{completed}</div>
          <div class="metric-lbl">Modules Completed</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-val" style="color:#22d3c5;">{pct}%</div>
          <div class="metric-lbl">Learning Progress</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        score_avg = int(sum(st.session_state.quiz_scores.values()) / max(len(st.session_state.quiz_scores), 1))
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-val" style="color:#a78bfa;">{score_avg}%</div>
          <div class="metric-lbl">Avg Quiz Score</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-val" style="color:#f472b6;">12</div>
          <div class="metric-lbl">Learning Modules</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("### 🧭 Learning Modules")
    modules = [
        ("🌍", "UAE Insurance Landscape", "Regulators, TPA, DHA, DOH/HAAD, reinsurance", "foundations", "landscape"),
        ("🚫", "Exclusions Reference", "DHA, DOH/HAAD and MOH exclusion summaries", "exclusions", "exclusions"),
        ("📋", "Claims Processing", "OP/IP workflow, denial codes, prior authorisation", "claims", "claims"),
        ("🔢", "Medical Coding", "CPT, ICD-10, HCPCS, DRG and HCC concepts", "coding", "coding"),
        ("🔍", "Pre-existing Conditions", "UNPEC, underwriting and file-audit learning", "preex", "preex"),
        ("🏥", "Inpatient & Emergency", "IP rules, notification, LoS and DRG grouping", "inpatient", "inpatient"),
        ("🔎", "Internal Audit", "Risk-based audit, FWA and documentation", "audit", "audit"),
        ("💊", "Specialty Rules", "Physiotherapy, dental, maternity and pharmacy", "specialty", "specialty"),
        ("🎯", "Case Studies", "Scenario-based educational practice", "cases", "cases"),
        ("📝", "Knowledge Quiz", "Module checks and knowledge review", "quiz", "quiz"),
        ("📚", "Resources", "Official reference links and glossary", "resources", "resources"),
        ("🩺", "Procedures, Dental & Vaccines", "First-line review prompts, procedures and vaccination notes", "procedures", "procedures"),
    ]
    for icon, title, desc, key, slug in modules:
        done = st.session_state.progress.get(key, False)
        status = "✅ Completed" if done else "○ Not started"
        status_col = "#34d399" if done else "#5c6480"
        st.markdown(f"""
        <a class="module-link" href="?page={slug}" target="_self">
          <div class="glass-card module-card">
            <div class="module-icon">{icon}</div>
            <div style="flex:1;">
              <div class="module-title">{title}</div>
              <div class="module-desc">{desc}</div>
            </div>
            <div class="module-status" style="color:{status_col};">{status}</div>
          </div>
        </a>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.8rem;color:#5c6480;text-align:center;padding:1rem 0;">
      Created by <strong style="color:#9aa3b8;">Rana Musab Bin Tariq</strong> — PharmD, MSc Digital Health, Deggendorf Institute of Technology |
      <a href="https://www.linkedin.com/in/rana-musab-bin-tariq-a70982152/" target="_blank"
         style="color:#4f9cf9;text-decoration:none;">LinkedIn</a> |
      <a href="https://github.com/RanaMusabBinTariq" target="_blank"
         style="color:#4f9cf9;text-decoration:none;">GitHub</a>
      <br/>Educational summaries informed by publicly available UAE regulatory materials and professional experience.
      For training purposes only — not a clinical decision tool.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — UAE INSURANCE LANDSCAPE
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "🌍  UAE Insurance Landscape":
    st.session_state.progress["foundations"] = True
    st.markdown('<div class="section-title">UAE Insurance Landscape</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Regulators, policy types, TPA roles, insurance vs reinsurance — the full ecosystem</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🏛️ Regulators", "📄 Policy Types", "🔄 TPA & Payers", "🌐 Insurance vs Reinsurance"])

    with tab1:
        st.markdown("""
        <div class="glass-card">
          <div style="font-weight:700;font-size:1rem;margin-bottom:1rem;">UAE Health Insurance Regulatory Bodies</div>
          <table class="styled-table">
            <tr><th>Body</th><th>Jurisdiction</th><th>What It Controls</th><th>Key Framework</th></tr>
            <tr>
              <td><span class="badge badge-blue">DHA</span> Dubai Health Authority</td>
              <td>Dubai Emirate</td>
              <td>Mandatory health insurance for all employees & dependents in Dubai. Sets minimum benefit (EBP). Licenses providers & insurers.</td>
              <td>Dubai Law No. 11 of 2013</td>
            </tr>
            <tr>
              <td><span class="badge badge-cyan">DOH / HAAD</span> Dept of Health Abu Dhabi</td>
              <td>Abu Dhabi, Al Ain, Al Gharbia</td>
              <td>Mandatory coverage since 2006. Thiqa for UAE nationals (ADNOC/govt), DAMAN for expats. Sets SHCA standard plan.</td>
              <td>Law No. 23 of 2005 (AUH)</td>
            </tr>
            <tr>
              <td><span class="badge badge-violet">MOH</span> Ministry of Health & Prevention</td>
              <td>Northern Emirates (SHJ, AJM, UAQ, RAK, FUJ)</td>
              <td>Regulates health insurance in Northern Emirates. Mandatory insurance active. Less standardised than DHA/HAAD.</td>
              <td>Federal Law No. 7 of 2019</td>
            </tr>
            <tr>
              <td><span class="badge badge-amber">IA</span> Insurance Authority (now CBUAE)</td>
              <td>Federal</td>
              <td>Licenses insurance & reinsurance companies federally. Merged into Central Bank UAE (CBUAE) in 2020.</td>
              <td>Federal Law No. 6 of 2007</td>
            </tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box">
          <strong>Key difference:</strong> DHA and HAAD/DOH operate independently. A DHA policy follows DHA exclusions; a HAAD policy follows HAAD/DOH exclusions.
          A member working in Dubai but living in Abu Dhabi may have either — always check the policy issuing authority (check the TOB header or regulator field).
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="glass-card">
          <div style="font-weight:700;font-size:1rem;margin-bottom:1rem;">Policy Plan Tiers — Dubai (DHA) Example</div>
          <table class="styled-table">
            <tr><th>Tier</th><th>Also Called</th><th>Who Has It</th><th>Key Characteristics</th></tr>
            <tr>
              <td><span class="badge badge-coral">EBP</span></td>
              <td>Essential Benefits Plan / Basic</td>
              <td>Low-income workers, domestic helpers</td>
              <td>Minimum DHA-mandated cover. Limited network. 6-month waiting period on pre-existing. No specialist without GP referral (except paeds/OB-GYN). Capped at AED 150,000/year.</td>
            </tr>
            <tr>
              <td><span class="badge badge-amber">Silk Road / Watania Basic</span></td>
              <td>Near-EBP plans</td>
              <td>Small employers, budget groups</td>
              <td>Similar to EBP. Restricted OP network. Hospital access only at night (10pm–8am) or emergency. Max 3 physio sessions per request.</td>
            </tr>
            <tr>
              <td><span class="badge badge-blue">Standard / Enhanced</span></td>
              <td>Corporate group plans</td>
              <td>Mid-size companies, professionals</td>
              <td>Broader network. May include dental, optical, maternity package. No GP referral requirement. Standard 5 physio sessions per request.</td>
            </tr>
            <tr>
              <td><span class="badge badge-cyan">Gold / Premium / International</span></td>
              <td>Executive, VIP plans</td>
              <td>Senior management, expat families</td>
              <td>Wide network including private hospitals. Maternity covered. Mental health emergency. Higher sub-limits. Reinsured with international carriers.</td>
            </tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card">
          <div style="font-weight:700;font-size:1rem;margin-bottom:0.8rem;">Abu Dhabi (DOH/HAAD) Plan Types</div>
          <table class="styled-table">
            <tr><th>Plan</th><th>Population</th><th>Features</th></tr>
            <tr><td><span class="badge badge-cyan">Thiqa</span></td><td>UAE Nationals in Abu Dhabi</td><td>ADNOC employees, government workers. Comprehensive cover. DAMAN administers. No co-pay for nationals.</td></tr>
            <tr><td><span class="badge badge-blue">DAMAN Standard</span></td><td>Expat workers in Abu Dhabi</td><td>Mandatory minimum plan. AED 250,000 annual limit. SHCA basic benefits apply.</td></tr>
            <tr><td><span class="badge badge-violet">DAMAN Enhanced</span></td><td>Higher-income expats / families</td><td>Extended network, dental, optical, maternity top-up. DOH exclusions still apply.</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class="glass-card">
          <div style="font-weight:700;font-size:1rem;margin-bottom:0.8rem;">How the Claims Ecosystem Works</div>
          <p style="font-size:0.88rem;color:#9aa3b8;line-height:1.7;">
            <strong style="color:#f0f2f8;">Member</strong> → visits provider →
            <strong style="color:#f0f2f8;">Provider</strong> submits claim/PA →
            <strong style="color:#f0f2f8;">TPA</strong> (Third Party Administrator) adjudicates →
            <strong style="color:#f0f2f8;">Insurance Company (Payer/PIC)</strong> holds risk →
            <strong style="color:#f0f2f8;">Reinsurer</strong> absorbs excess risk above retention
          </p>
          <table class="styled-table" style="margin-top:0.8rem;">
            <tr><th>Role</th><th>What They Do</th><th>Example in UAE</th></tr>
            <tr>
              <td><strong>PIC</strong> (Primary Insurance Company)</td>
              <td>Sells the policy, holds the risk, sets the TOB. Final decision maker on exclusions and escalations.</td>
              <td>Orient Insurance, Dubai Insurance, Watania, AIAW, Daman, Generali</td>
            </tr>
            <tr>
              <td><strong>TPA</strong> (Third Party Administrator)</td>
              <td>Processes claims and prior authorisations on behalf of the PIC. Does not hold the risk. Earns a per-member-per-month fee.</td>
              <td>MedNet, Neuron, HealthPoint, NAS, Nextcare</td>
            </tr>
            <tr>
              <td><strong>Provider</strong></td>
              <td>Hospital, clinic, pharmacy, diagnostic centre. Submits requests and claims to TPA system.</td>
              <td>Mediclinic, Aster, Prime, Al Zahra, NMC</td>
            </tr>
            <tr>
              <td><strong>Network</strong></td>
              <td>The contracted list of providers where the member has direct billing coverage. Out-of-network = reimbursement or denial.</td>
              <td>DHA-licensed providers contracted by TPA/PIC</td>
            </tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

    with tab4:
        st.markdown("""
        <div class="glass-card">
          <div style="font-weight:700;font-size:1rem;margin-bottom:1rem;">Insurance vs Reinsurance — Key Concepts</div>
          <table class="styled-table">
            <tr><th>Concept</th><th>Insurance</th><th>Reinsurance</th></tr>
            <tr><td><strong>Definition</strong></td><td>Contract between insurer and member. Covers medical expenses as per policy terms.</td><td>Contract between insurer and reinsurer. Insurer transfers part of its risk to the reinsurer.</td></tr>
            <tr><td><strong>Parties</strong></td><td>PIC ↔ Employer/Member</td><td>PIC (cedant) ↔ Reinsurer</td></tr>
            <tr><td><strong>Claim trigger</strong></td><td>Member's medical event</td><td>PIC's aggregate/individual loss exceeds retention limit</td></tr>
            <tr><td><strong>Types</strong></td><td>Group health, individual health, maternity add-on</td><td>Proportional (quota share), Non-proportional (excess of loss, stop loss)</td></tr>
            <tr><td><strong>UAE Example</strong></td><td>Orient Insurance selling a group health policy to a company of 200 employees</td><td>Orient cedes 60% of risk to Munich Re (which owns MedNet as its TPA arm)</td></tr>
            <tr><td><strong>Member awareness</strong></td><td>Member has a policy card, TOB, network list</td><td>Member is unaware of reinsurance arrangement — no impact on their benefits</td></tr>
          </table>
        </div>
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.6rem;">🔑 Key Terms for Day-One Work</div>
          <table class="styled-table">
            <tr><th>Term</th><th>Meaning</th></tr>
            <tr><td>TOB</td><td>Table of Benefits — the master document listing covered and excluded services, limits, co-pays, networks</td></tr>
            <tr><td>MAF</td><td>Medical Application Form — completed at policy inception for individual/small-group underwriting</td></tr>
            <tr><td>Declaration Form</td><td>Lists pre-existing conditions declared by the member at enrollment</td></tr>
            <tr><td>Prior Authorization (PA)</td><td>Pre-approval required before a service is rendered — most elective procedures, specialist referrals, high-cost diagnostics</td></tr>
            <tr><td>Co-pay / Deductible</td><td>Member's share of cost. Co-pay = fixed amount per visit. Deductible = amount member pays before insurance kicks in.</td></tr>
            <tr><td>Sub-limit</td><td>A cap within the annual limit for a specific category (e.g. dental AED 3,000 within overall AED 150,000 limit)</td></tr>
            <tr><td>Waiting Period</td><td>Period after enrollment during which certain conditions are not covered. Standard = 6 months for pre-existing/chronic in EBP.</td></tr>
            <tr><td>Direct Billing (DB)</td><td>Provider bills TPA/PIC directly. Member pays only co-pay. Available only for network providers.</td></tr>
            <tr><td>Reimbursement</td><td>Member pays out-of-pocket then submits claim to TPA/PIC for refund. Used for out-of-network or non-approved services.</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — EXCLUSIONS
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "🚫  Exclusions Reference":
    st.session_state.progress["exclusions"] = True
    st.markdown('<div class="section-title">Exclusions Reference</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Official DHA, HAAD/DOH, and Northern Emirates exclusion clauses — searchable, annotated</div>', unsafe_allow_html=True)

    st.markdown("""<div class="disclaimer">
      These exclusions are derived from DHA Mandatory Health Insurance Scheme (Dubai Law No.11/2013) and HAAD
      Standard Health Insurance Regulations. Always verify against the current official circular before applying to any claim.
      A condition may be excluded under the basic policy but covered under an enhanced TOB — always check the member's specific TOB.
    </div>""", unsafe_allow_html=True)

    search = st.text_input("🔍 Search exclusions...", placeholder="e.g. dental, obesity, maternity, HIV...")
    tab1, tab2, tab3, tab4 = st.tabs(["🔵 DHA Exclusions", "🟢 HAAD Exclusions", "🟡 Northern Emirates", "⚖️ Key Differences"])

    dha_exclusions = [
        (1, "Not medically necessary", "Services that are not clinically indicated per accepted medical guidelines. One of the most commonly cited denial reasons. Requires medical justification for all investigations and procedures.", "badge-coral"),
        (2, "Dental treatment", "All dental expenses including treatment, prostheses, and orthodontics. Covered only if dental benefit is explicitly added in TOB.", "badge-coral"),
        (3, "Travel care", "Care obtained solely for the purpose of travelling or convenience.", "badge-amber"),
        (4, "Custodial care", "Non-medical services or services that do not change the patient's medical condition. Includes long-term nursing home care.", "badge-amber"),
        (5, "Non-specialist care", "Services not requiring continuous administration by specialised medical personnel.", "badge-amber"),
        (6, "Personal comfort items", "TV, barber, beauty, guest services in hospital.", "badge-amber"),
        (7, "Cosmetic services", "All cosmetic procedures. Exception: cosmetic surgery related to injury/disease where primary purpose is functional restoration. Breast reconstruction post-mastectomy IS covered.", "badge-coral"),
        (8, "Obesity treatment", "Surgical and non-surgical obesity treatments including bariatric surgery, weight loss programs, medications.", "badge-coral"),
        (9, "Experimental services", "Research, medically non-approved experimental treatments, investigational drugs.", "badge-amber"),
        (10, "Unauthorised providers", "Services not by DHA-licensed healthcare providers. Emergency exception applies.", "badge-coral"),
        (11, "Alopecia/hair loss", "Treatment for baldness, alopecia, dandruff, wigs.", "badge-amber"),
        (12, "Smoking cessation", "Programs and medications for nicotine addiction.", "badge-amber"),
        (13, "Contraception", "All contraceptive services and devices.", "badge-coral"),
        (14, "Sex transformation/infertility", "Sterilisation (unless medically indicated), infertility treatment, IVF, sexual dysfunction.", "badge-coral"),
        (15, "External prosthetics", "External prosthetic devices and medical equipment (wheelchairs, crutches, etc.) unless in TOB.", "badge-amber"),
        (16, "Professional sports injuries", "Injuries from professional sports activities. Amateur/recreational sports ARE covered under DHA (updated circular). List includes aerial flight, power races, water sports, mountaineering, martial arts, bungee jumping.", "badge-coral"),
        (17, "Growth hormone therapy", "Unless medically necessary and documented.", "badge-amber"),
        (18, "Hearing/vision aids", "Hearing tests, prosthetic devices, vision aids, corrective lenses.", "badge-amber"),
        (19, "Mental health", "Both inpatient and outpatient mental health unless it is an emergency psychiatric condition.", "badge-coral"),
        (20, "Patient treatment supplies", "Bandages, gauze, syringes, diabetic strips, non-prescription drugs. Exception: required during emergency treatment.", "badge-amber"),
        (21, "Allergy testing", "Allergy testing and desensitisation. Exception: testing for allergy to medications being used in treatment.", "badge-coral"),
        (22, "Relative provider", "Services by a provider who is a first-degree relative of the patient.", "badge-amber"),
        (23, "Enteral feeding", "Tube feeding and nutritional supplements unless medically necessary during inpatient treatment.", "badge-amber"),
        (24, "Spinal manipulation", "Adjustment of spinal subluxation by any means.", "badge-amber"),
        (25, "Alternative medicine", "Acupuncture, acupressure, hypnotism, massage therapy, aromatherapy, ozone therapy, homeopathy.", "badge-coral"),
        (26, "IVF/embryo transfer", "All in-vitro fertilisation, embryo transfer, ovum/sperm transfer.", "badge-coral"),
        (27, "Elective vision correction", "Elective diagnostic services and treatment for refractive errors (LASIK, Pentacam unless medical need shown).", "badge-amber"),
        (28, "Nasal septum/concha", "Nasal septum deviation (surgery). OP investigations/scans for DNS are covered. Nasal concha resection.", "badge-coral"),
        (29, "Chronic dialysis", "Haemodialysis and peritoneal dialysis for chronic conditions and all related tests/procedures.", "badge-coral"),
        (30, "Hepatitis exclusion", "Viral hepatitis — Hepatitis B covered under DHA. Hepatitis C covered under DHA. Hepatitis A always covered.", "badge-cyan"),
        (31, "Congenital/birth defects", "Unless left untreated will develop into an emergency.", "badge-amber"),
        (32, "Senile dementia/Alzheimer's", "Healthcare services for dementia and Alzheimer's disease.", "badge-coral"),
        (33, "Medical evacuation", "Air or terrestrial evacuation and unauthorised transport. Emergency evacuation has exceptions.", "badge-amber"),
        (34, "IP without prior approval", "Inpatient treatment without pre-authorisation. Emergency not notified within 24 hours where possible.", "badge-coral"),
        (35, "IP doable as OP", "Any treatment, test, or procedure that can be carried out on outpatient basis without risk to health.", "badge-coral"),
        (36, "Non-medical testing", "Employment, travel, licensing, or insurance-related tests.", "badge-amber"),
        (37, "Non-medical supplies", "Mouthwash, toothpaste, antiseptics, food supplements, skin care, shampoos, multivitamins (unless replacement therapy for known deficiency), air conditioners, exercise equipment.", "badge-amber"),
        (38, "Multiple specialist visits", "More than one consultation with a medical specialist in a single day unless referred by treating physician.", "badge-amber"),
        (39, "Organ transplants", "All organ and tissue transplants (donor and recipient). Follow-up and complications excluded unless emergency.", "badge-coral"),
        (40, "Immunomodulators", "Unless medically necessary.", "badge-amber"),
        (41, "Sleep disorders", "All treatment for sleep-related disorders.", "badge-amber"),
        (42, "Disabilities/special education", "Services and educational programs for people of determination. Disability-related services.", "badge-amber"),
    ]

    with tab1:
        filtered_dha = dha_exclusions
        if search:
            filtered_dha = [e for e in dha_exclusions if search.lower() in e[1].lower() or search.lower() in e[2].lower()]

        st.markdown(f"""
        <div class="glass-card" style="padding:1rem 1.4rem;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.8rem;">
            <div style="font-weight:700;">DHA Exclusions — Dubai Health Authority</div>
            <span class="badge badge-blue">{len(filtered_dha)} clauses</span>
          </div>
          <table class="styled-table">
            <tr><th>#</th><th>Exclusion</th><th>Detail & Notes</th></tr>
            {''.join(f'<tr><td style="color:#5c6480;font-size:0.78rem;">{e[0]}</td><td><span class="badge {e[3]}">{e[1]}</span></td><td style="font-size:0.82rem;color:#9aa3b8;">{e[2]}</td></tr>' for e in filtered_dha)}
          </table>
        </div>
        """, unsafe_allow_html=True)

    haad_exclusions = [
        (1, "Not medically necessary", "Same as DHA. Services not clinically indicated per good medical practice.", "badge-coral"),
        (2, "Dental treatment", "All dental treatment, prostheses, orthodontics.", "badge-coral"),
        (3, "Domiciliary / travel care", "Home care, private nursing, travel-related care.", "badge-amber"),
        (4, "Custodial care", "Non-medical services that don't change the patient's condition.", "badge-amber"),
        (5, "Non-specialist services", "Services not requiring specialised continuous medical care.", "badge-amber"),
        (6, "Personal comfort items", "TV, barber, beauty, guest services.", "badge-amber"),
        (7, "Cosmetic procedures", "Cosmetic surgery for aesthetics. Functional restoration and post-mastectomy breast reconstruction are covered.", "badge-coral"),
        (8, "Obesity treatment", "Surgical and non-surgical obesity and weight control programs.", "badge-coral"),
        (9, "Experimental treatments", "Medically non-approved, investigational, research-phase treatments.", "badge-amber"),
        (10, "Unauthorised providers", "Except in medical emergency.", "badge-coral"),
        (11, "Alopecia/hair loss", "Alopecia, baldness, dandruff, wigs.", "badge-amber"),
        (12, "Smoking cessation", "Programs and medications for nicotine addiction.", "badge-amber"),
        (13, "Non-medical amniocentesis", "Non-medically necessary amniocentesis.", "badge-amber"),
        (14, "Sex transformation/sterility", "Sex change, sterilisation, sterility treatment.", "badge-coral"),
        (15, "Contraception", "All contraception services and treatments.", "badge-coral"),
        (16, "Fertility/sexual dysfunction", "Infertility treatment, varicocele, PCOS, hormonal disturbances, sexual dysfunction — all covered under DHA but excluded under HAAD.", "badge-coral"),
        (17, "Prosthetics", "Prosthetic devices and consumed medical equipment unless approved by insurer.", "badge-amber"),
        (18, "Hazardous activities", "Injuries from hazardous activities — aerial flight, power races, water sports, horse riding, mountaineering, martial arts, bungee jumping, professional sports. NOTE: Under DHA, only professional sports excluded; HAAD is broader.", "badge-coral"),
        (19, "Growth hormone therapy", "Standard exclusion under HAAD.", "badge-amber"),
        (20, "Hearing/vision aids", "Hearing tests, vision corrections, prosthetics, aids.", "badge-amber"),
        (21, "Mental health", "Inpatient and outpatient unless transient disorder or acute reaction to stress.", "badge-coral"),
        (22, "Patient treatment supplies", "Elastic stockings, bandages, syringes, diabetic strips, non-prescription drugs.", "badge-amber"),
        (23, "Preventive / vaccinations", "Preventive services, vaccinations, immunisations, allergy testing and desensitisation, physicals and screening exams.", "badge-coral"),
        (24, "Relative provider", "Services by a relative of the patient.", "badge-amber"),
        (25, "Enteral feeding", "Nutritional supplements unless medically necessary during treatment.", "badge-amber"),
        (26, "Spinal subluxation", "Chiropractic-style spinal adjustments.", "badge-amber"),
        (27, "Alternative medicine", "Acupuncture, acupressure, hypnotism, rolfing, massage, aromatherapy, homeopathy.", "badge-coral"),
        (28, "IVF/embryo transfer", "All IVF and related reproductive technology.", "badge-coral"),
        (29, "Elective vision correction", "Elective correction of refractive errors.", "badge-amber"),
        (30, "Nasal septum/concha", "Nasal septum deviation surgery and nasal concha resection.", "badge-coral"),
        (31, "Chronic dialysis", "All chronic dialysis and related treatments.", "badge-coral"),
        (32, "Viral hepatitis", "Hepatitis B and C excluded. Hepatitis A always covered under HAAD.", "badge-coral"),
        (33, "Birth defects", "Congenital diseases, birth defects, deformities unless life-threatening.", "badge-amber"),
        (34, "Dementia/Alzheimer's", "Senile dementia and Alzheimer's disease.", "badge-coral"),
        (35, "Medical evacuation", "Air/terrestrial evacuation except emergency cases.", "badge-amber"),
        (36, "Circumcision", "Circumcision services — excluded under HAAD. Covered under DHA for newborns and medically necessary cases.", "badge-coral"),
        (37, "IP without prior approval", "Inpatient without authorisation; emergency not notified within 24 hours.", "badge-coral"),
        (38, "IP doable as OP", "Any IP treatment that could safely be done as OP.", "badge-coral"),
        (39, "Non-medical testing", "Employment, travel, licensing, insurance testing.", "badge-amber"),
        (40, "Non-medical supplies", "Mouthwash, toothpaste, food supplements, skin care, shampoos, multivitamins, equipment not primarily for medical improvement.", "badge-amber"),
        (41, "Multiple specialist visits/day", "More than one specialist visit per day without referral.", "badge-amber"),
        (42, "Organ transplants", "All organ and tissue transplants (donor and recipient).", "badge-coral"),
        (43, "Handicap education", "Services and educational programs for handicaps.", "badge-amber"),
        (44, "Military injuries", "Injuries from military operations.", "badge-amber"),
        (45, "War/terrorism injuries", "Injuries from wars or acts of terror.", "badge-amber"),
        (46, "Nuclear/chemical contamination", "Healthcare for nuclear or chemical contamination injuries.", "badge-amber"),
        (47, "Natural disasters", "Injuries from earthquakes, tornados, natural disasters.", "badge-amber"),
        (48, "Criminal acts", "Injuries from criminal acts or resisting authority.", "badge-amber"),
        (49, "HIV/AIDS", "Healthcare for AIDS and its complications — excluded under HAAD. Under DHA: HIV is excluded per basic. Check TOB.", "badge-coral"),
        (50, "Work injuries", "Work-related illnesses and injuries (Workmen's Compensation, Federal Law No. 8/1980).", "badge-coral"),
        (51, "Alcohol/drug use", "Conditions resulting from alcohol, drugs, hallucinatory substances.", "badge-coral"),
        (52, "Non-prescribed treatment", "Any test or treatment not prescribed by a doctor.", "badge-amber"),
        (53, "Suicide/self-harm", "Injuries from attempted suicide or self-inflicted injuries.", "badge-coral"),
        (54, "Complications of excluded conditions", "Diagnosis and treatment for complications of excluded illnesses.", "badge-coral"),
        (55, "Epidemics", "Internationally and locally recognised epidemics (e.g., COVID-19 under HAAD handled separately by DOH Circular 38).", "badge-coral"),
        (56, "Sexually transmitted diseases", "Venereal and sexually transmitted diseases. Note: STDs are excluded under HAAD but HPV is covered under DHA per medical necessity.", "badge-coral"),
    ]

    with tab2:
        filtered_haad = haad_exclusions
        if search:
            filtered_haad = [e for e in haad_exclusions if search.lower() in e[1].lower() or search.lower() in e[2].lower()]
        st.markdown(f"""
        <div class="glass-card">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.8rem;">
            <div style="font-weight:700;">HAAD/DOH Exclusions — Abu Dhabi Health Authority</div>
            <span class="badge badge-cyan">{len(filtered_haad)} clauses</span>
          </div>
          <table class="styled-table">
            <tr><th>#</th><th>Exclusion</th><th>Detail & Notes</th></tr>
            {chr(10).join('<tr><td style="color:#5c6480;font-size:0.78rem;">'+str(e[0])+'</td><td><span class="badge '+e[3]+'">'+str(e[1])+'</span></td><td style="font-size:0.82rem;color:#9aa3b8;">'+str(e[2])+'</td></tr>' for e in filtered_haad)}
          </table>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">Northern Emirates (Non-DHA / Non-HAAD) — Key Exclusions</div>
          <p style="font-size:0.85rem;color:#9aa3b8;margin-bottom:1rem;">
            For Sharjah, Ajman, Ras Al Khaimah, Umm Al Quwain, Fujairah policies regulated under MOH.
            Less standardised — always check the specific TOB. Common exclusion categories:
          </p>
          <table class="styled-table">
            <tr><th>Category</th><th>Exclusion Detail</th></tr>
            <tr><td>Hazardous sports</td><td>Broader than DHA — includes winter sports, water sports, horse riding, martial arts, power vehicles, aerial flight, mountaineering, bungee jumping</td></tr>
            <tr><td>Mental/psychiatric</td><td>Psychiatric, psychological disorders generally excluded</td></tr>
            <tr><td>Chronic diseases (specific)</td><td>Dementia, Alzheimer's, osteoporosis, menopause excluded</td></tr>
            <tr><td>Eating disorders</td><td>Bulimia, anorexia nervosa and similar excluded</td></tr>
            <tr><td>STDs</td><td>All STDs including Hepatitis B, HIV/AIDS excluded</td></tr>
            <tr><td>Fertility</td><td>Infertility, IVF, sexual dysfunction, birth control excluded</td></tr>
            <tr><td>Skin conditions</td><td>Warts, keloid, acne, molluscum contagiosum, moles/nevi</td></tr>
            <tr><td>Circumcision</td><td>Excluded unless medically necessary</td></tr>
            <tr><td>Hormone replacement therapy (HRT)</td><td>Excluded</td></tr>
            <tr><td>Deviated nasal septum</td><td>Excluded (broader than DHA which allows OP investigations)</td></tr>
            <tr><td>Road traffic accidents</td><td>Excluded — covered by Motor Third-Party Liability</td></tr>
            <tr><td>Preventive / vaccinations</td><td>Vaccinations, screening, general check-ups excluded</td></tr>
          </table>
          <div style="margin-top:1rem;font-size:0.82rem;color:#5c6480;">
            <strong style="color:#fbbf24;">Pharmaceutical exclusions (common):</strong>
            Vitamins & minerals (unless with antibiotics), vaccinations, contraceptives, psychiatric medications,
            cosmetic preparations, antiseptic solutions, baby formula, contact lens products, bandages/braces/supports,
            glucostrips, hearing aids, HRT medications, acne medications.
          </div>
        </div>
        """, unsafe_allow_html=True)

    with tab4:
        st.markdown("""
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">⚖️ DHA vs HAAD — Critical Differences at a Glance</div>
          <table class="styled-table">
            <tr><th>Topic</th><th>DHA (Dubai)</th><th>HAAD/DOH (Abu Dhabi)</th></tr>
            <tr><td><strong>Hepatitis</strong></td><td>Hep A ✅ Hep B ✅ Hep C ✅ (covered)</td><td>Hep A ✅ only. Hep B/C excluded</td></tr>
            <tr><td><strong>STDs/HPV</strong></td><td>HPV covered per medical necessity (not standard exclusion)</td><td>All STDs/venereal diseases excluded</td></tr>
            <tr><td><strong>Hazardous sports</strong></td><td>Only <em>professional</em> sports excluded. Amateur/recreational covered.</td><td>Broad exclusion including water sports, horse riding, martial arts regardless of professional status</td></tr>
            <tr><td><strong>Mental health</strong></td><td>Emergency psychiatric condition covered</td><td>Transient disorder or acute stress reaction covered only</td></tr>
            <tr><td><strong>Circumcision</strong></td><td>Covered for newborns (0–2 yrs) and medical necessity. Some policies cover ritual.</td><td>Excluded</td></tr>
            <tr><td><strong>Fertility treatment</strong></td><td>Infertility/IVF excluded but some enhanced plans add it</td><td>Fertility, varicocele, PCOS, hormonal disturbances all specifically excluded</td></tr>
            <tr><td><strong>COVID testing</strong></td><td>Pre-operative COVID PCR covered (DHA circular). Symptomatic testing covered.</td><td>Covered by Activity-Based Funded Mandates/DAMAN — NOT through insurance</td></tr>
            <tr><td><strong>HIV/AIDS</strong></td><td>Excluded in basic plan; may be covered in some enhanced TOBs. Check Integra Global — not excluded.</td><td>Explicitly excluded</td></tr>
            <tr><td><strong>Congenital diseases</strong></td><td>Covered if left untreated would become emergency</td><td>Excluded unless life-threatening for newborn</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — CLAIMS PROCESSING
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "📋  Claims Processing":
    st.session_state.progress["claims"] = True
    st.markdown('<div class="section-title">Claims Processing</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Prior authorisation, adjudication workflow, denial codes, and procedure decision trees</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🔄 Workflow", "🚫 Denial Codes", "🌳 Decision Trees", "📋 Procedure Rules"])

    with tab1:
        st.markdown("""
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:1rem;">Prior Authorisation (PA) Process Flow</div>
          <div class="timeline-item">
            <div class="timeline-dot" style="background:rgba(79,156,249,0.2);color:#4f9cf9;">1</div>
            <div><strong>Provider submits PA request</strong> — via TPA portal with CPT code, ICD-10 diagnosis, member card number, clinical notes. Cost must be included in service line.</div>
          </div>
          <div class="timeline-item">
            <div class="timeline-dot" style="background:rgba(34,211,197,0.2);color:#22d3c5;">2</div>
            <div><strong>TPA receives & checks eligibility</strong> — Is member active? Is provider in-network? Is service in TOB? Waiting period? Sub-limit remaining? Annual limit remaining?</div>
          </div>
          <div class="timeline-item">
            <div class="timeline-dot" style="background:rgba(167,139,250,0.2);color:#a78bfa;">3</div>
            <div><strong>Medical adjudication</strong> — Is service medically necessary? First-line or requires prior conservative management? Any exclusion clause? Documentation adequate?</div>
          </div>
          <div class="timeline-item">
            <div class="timeline-dot" style="background:rgba(251,191,36,0.2);color:#fbbf24;">4</div>
            <div><strong>Decision</strong> — Approve (with reference code) / Deny (with denial code + template) / Query (Request for Information) / Escalate to PIC (high-value or UNPEC)</div>
          </div>
          <div class="timeline-item">
            <div class="timeline-dot" style="background:rgba(52,211,153,0.2);color:#34d399;">5</div>
            <div><strong>Provider notified</strong> — Approval reference sent. Service rendered. Claim submitted post-service for payment settlement.</div>
          </div>
        </div>

        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">What Always Requires Prior Authorisation</div>
          <table class="styled-table">
            <tr><th>Service Category</th><th>PA Required?</th><th>Notes</th></tr>
            <tr><td>All inpatient admissions (elective)</td><td><span class="badge badge-coral">Always</span></td><td>Must be approved before admission. No PA = denial (except emergency notified within 24hrs)</td></tr>
            <tr><td>Surgical procedures (OP and IP)</td><td><span class="badge badge-coral">Always</span></td><td>PA must be obtained before surgery regardless of setting</td></tr>
            <tr><td>MRI / CT / PET scans</td><td><span class="badge badge-coral">Always</span></td><td>High-value imaging. Clinical justification required. First-line tests must precede in most cases.</td></tr>
            <tr><td>Specialist referral (EBP)</td><td><span class="badge badge-amber">Usually</span></td><td>EBP members need GP referral to see specialist (except paeds/OB-GYN)</td></tr>
            <tr><td>Physiotherapy sessions</td><td><span class="badge badge-amber">Yes</span></td><td>Max 5 sessions per request (3 for EBP). Progress report after each batch.</td></tr>
            <tr><td>Outpatient procedures (colonoscopy, endoscopy)</td><td><span class="badge badge-coral">Yes</span></td><td>Requires clinical criteria to be met before approval</td></tr>
            <tr><td>OP GP consultation</td><td><span class="badge badge-green">No PA</span></td><td>Generally direct access for standard plans</td></tr>
            <tr><td>Emergency (life-threatening)</td><td><span class="badge badge-green">Treat first</span></td><td>Approve until stabilisation. Notify insurer within 24 hours post-admission.</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        denial_codes = [
            ("Auth-001", "Prior approval not obtained", "badge-coral", "Service rendered without prior authorisation. Standard rejection unless verbal approval exists in medical file (emergency ER only)."),
            ("AUTH-011", "Waiting period on pre-existing / chronic conditions", "badge-amber", "6-month standard waiting period for chronic/pre-existing. Check both group AND individual custom fields before applying."),
            ("AUTH-012", "Request for Information (RFI)", "badge-blue", "Incomplete documentation. Specify exactly what is needed: onset date, conservative management history, investigations, physiotherapy progress notes."),
            ("BENX-005", "Annual limit / sub-limit exceeded", "badge-amber", "Member has exhausted their benefit for the current policy year. State which benefit and the amount."),
            ("CLAI-007", "Work-related injury", "badge-coral", "Condition related to workplace injury. Covered by Workmen's Compensation, not health insurance. For EBP: cover only to point of emergency stabilisation."),
            ("CLAI-012", "Provider not in member's network", "badge-coral", "Requesting provider is not contracted in the member's specific network tier. Direct billing not available — reimbursement only."),
            ("CLAI-017", "Service only on reimbursement", "badge-amber", "Service is covered but only through reimbursement (not direct billing). Advise member to pay and submit claim."),
            ("DUPL-001", "Duplicate claim / approval", "badge-amber", "Service was already approved or claimed. Cite the previous approval reference code."),
            ("ELIG-007", "Non-network provider", "badge-coral", "Provider not in network. Member may proceed on reimbursement basis if covered under TOB."),
            ("MNEC-003", "Not clinically indicated", "badge-coral", "Service not medically necessary per clinical guidelines. Must cite specific reason (e.g., normal radiology findings, insufficient conservative management, too short duration of symptoms)."),
            ("MNEC-005", "Service too frequent", "badge-amber", "Service was already recently approved and repeating within a short interval is not medically justified. Cite previous approval date."),
            ("NCOV-001", "Diagnosis not covered", "badge-coral", "The ICD-10 diagnosis code submitted is an excluded condition. State the applicable exclusion clause number."),
            ("NCOV-002", "Pre-existing condition not covered", "badge-coral", "Undeclared pre-existing condition. The onset predates policy effective date and was not declared. State onset vs enrollment date."),
            ("NCOV-003", "Service not covered", "badge-coral", "Specific service/CPT is a standard exclusion. State the exclusion clause number."),
            ("WRNG-001", "Wrong submission / system issue", "badge-amber", "Miscellaneous technical rejections: request not in system, wrong CPT submitted, missing cost, wrong network. Use specific template for each case."),
        ]
        denial_rows = "".join(
            '<tr><td><span class="badge ' + d[2] + '" style="font-family:monospace;">' + d[0] + '</span></td>'
            + '<td><strong>' + d[1] + '</strong></td>'
            + '<td style="font-size:0.8rem;color:#9aa3b8;">' + d[3] + '</td></tr>'
            for d in denial_codes
        )
        st.markdown(
            '<div class="glass-card"><div style="font-weight:700;margin-bottom:0.8rem;">Standard Denial &amp; Response Codes</div>'
            + '<table class="styled-table"><tr><th>Code</th><th>Reason</th><th>Key Action</th></tr>'
            + denial_rows + '</table></div>',
            unsafe_allow_html=True
        )

    with tab3:
        st.markdown('<div style="font-weight:700;margin-bottom:1rem;">🌳 MRI Authorisation Decision Tree</div>', unsafe_allow_html=True)
        body_part = st.selectbox("Select body part/indication:", ["Brain", "Spine/Orthopaedic", "Breast", "Abdomen/Pelvis"])
        if body_part == "Spine/Orthopaedic":
            st.markdown("""<div class="glass-card">
              <div style="font-weight:600;margin-bottom:0.8rem;">MRI Spine / Orthopaedic Decision</div>
              <div class="timeline-item"><div class="timeline-dot" style="background:rgba(251,191,36,0.2);color:#fbbf24;">Q1</div><div>Is there an X-ray attached?</div></div>
              <div style="padding-left:42px;margin-bottom:1rem;">
                <div class="success-box"><strong>X-ray shows abnormality + no prior physio:</strong> ✅ Approve MRI</div>
                <div class="success-box"><strong>X-ray shows abnormality + prior physio:</strong> Ask for physiotherapy progress notes first, then approve if PT inadequate</div>
                <div class="warning-box"><strong>X-ray normal + no conservative management:</strong> ❌ Deny. Request conservative management first (physio, analgesics).</div>
                <div class="info-box"><strong>No X-ray attached:</strong> Query (AUTH-012): Request X-ray, conservative management history, initial investigations.</div>
              </div>
            </div>""", unsafe_allow_html=True)
        elif body_part == "Brain":
            st.markdown("""<div class="glass-card">
              <div style="font-weight:600;margin-bottom:0.8rem;">MRI Brain Decision</div>
              <div class="info-box">MRI brain is generally case-by-case based on neurological indication. Standard criteria:</div>
              <div class="success-box">✅ Approve if: Seizures (EEG done first), MS evaluation, neurological deficit, head trauma with clinical finding, ophthalmologist/neurologist/ENT opinion provided</div>
              <div class="warning-box">⚠️ Query if: First presentation of headache only — ask for conservative management history, neurological signs/symptoms, ENT and ophthalmology opinions, preliminary investigations</div>
              <div class="warning-box">❌ Deny if: Purely headache without clinical neurological signs and no conservative management attempted</div>
            </div>""", unsafe_allow_html=True)
        elif body_part == "Breast":
            st.markdown("""<div class="glass-card">
              <div style="font-weight:600;margin-bottom:0.8rem;">Breast Imaging — Age-Based Decision</div>
              <table class="styled-table">
                <tr><th>Age</th><th>First-Line Modality</th><th>Second Modality</th></tr>
                <tr><td>&lt; 40 years</td><td><span class="badge badge-cyan">Ultrasound</span></td><td>Mammogram if ultrasound shows finding</td></tr>
                <tr><td>≥ 40 years</td><td><span class="badge badge-blue">Mammography</span></td><td>Ultrasound if mammogram shows abnormality</td></tr>
              </table>
              <div class="info-box" style="margin-top:0.8rem;">Note: Ultrasound cannot detect microcalcifications. Mammography cannot adequately evaluate superficial lumps in dense breast tissue. They are complementary, not interchangeable.</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div class="glass-card">
              <div class="info-box">MRI abdomen/pelvis: Evaluate based on clinical diagnosis, prior ultrasound findings, and specific indication. Ultrasound is first-line for most abdominal indications.</div>
            </div>""", unsafe_allow_html=True)

    with tab4:
        st.markdown("""
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">Procedure-Specific Coverage Rules</div>
          <table class="styled-table">
            <tr><th>Procedure</th><th>First-Line?</th><th>Conditions for Approval</th></tr>
            <tr><td>Physiotherapy</td><td><span class="badge badge-green">Yes</span></td><td>Referral required. No preliminary reports needed (unless individual policy). Max 5 sessions per request.</td></tr>
            <tr><td>Ultrasound</td><td><span class="badge badge-green">Yes</span></td><td>First-line for most indications. Not first-line for UTI (urine test first). First-line for varicose veins, TMJ.</td></tr>
            <tr><td>EEG</td><td><span class="badge badge-green">Yes</span></td><td>First-line for epilepsy/seizure evaluation.</td></tr>
            <tr><td>NCS/Nerve Conduction</td><td><span class="badge badge-green">Yes</span></td><td>First-line for carpal tunnel syndrome, neuropathy.</td></tr>
            <tr><td>X-Ray</td><td><span class="badge badge-green">Yes</span></td><td>First-line for most orthopaedic, chest, and structural assessments.</td></tr>
            <tr><td>ECG</td><td><span class="badge badge-green">Yes</span></td><td>First-line. No prerequisites.</td></tr>
            <tr><td>Echocardiogram</td><td><span class="badge badge-amber">Not always</span></td><td>Not indicated for chest pain without structural cardiac signs (ECG changes, cardiac murmur). Require ECG, TMT, and cardiac enzymes first.</td></tr>
            <tr><td>Colonoscopy</td><td><span class="badge badge-coral">No</span></td><td>Requires: chronic GI history, calprotectin/investigations, prior colonoscopy reports, or emergency (bleeding PR with Hb drop).</td></tr>
            <tr><td>Upper GIT Endoscopy</td><td><span class="badge badge-coral">No</span></td><td>Requires: 4–8 weeks of GERD treatment, H. pylori/urea breath test, prior endoscopy report, or emergency (haematemesis).</td></tr>
            <tr><td>Vitamin D test</td><td><span class="badge badge-coral">No</span></td><td>High-risk groups only. Must have prior test result + supplementation history. Annual repeat only if deficiency confirmed.</td></tr>
            <tr><td>Allergy testing</td><td><span class="badge badge-coral">Excluded</span></td><td>Standard exclusion for all. Covered under Generali upon medical necessity. TPA/Futtaim: approve.</td></tr>
            <tr><td>DEXA scan</td><td><span class="badge badge-amber">Conditional</span></td><td>Osteoporosis: check if X-rays show osteopenia. Approve if osteopenia confirmed, deny otherwise.</td></tr>
            <tr><td>Liver elastography</td><td><span class="badge badge-coral">No</span></td><td>Not first-line. Requires: medical report with history, liver function profile, ultrasound, viral hepatic labs.</td></tr>
            <tr><td>Ureteroscopy</td><td><span class="badge badge-amber">Conditional</span></td><td>Stone &lt;0.5cm: conservative management. 0.5–1cm: ESWL or URS if hydronephrosis. &gt;1cm: URS + ESWL. Must have radiology confirmation + urine analysis.</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — MEDICAL CODING
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "🔢  Medical Coding":
    st.session_state.progress["coding"] = True
    st.markdown('<div class="section-title">Medical Coding</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">CPT, HCPCS, ICD-10, DRG, HCC — what each system does and how they interact in UAE insurance</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📘 CPT vs HCPCS vs ICD-10", "🔢 CPT Deep Dive", "🏥 DRG & Inpatient", "🌍 UAE vs US Coding"])

    with tab1:
        st.markdown("""
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">The Three Coding Systems — Overview</div>
          <table class="styled-table">
            <tr><th>System</th><th>Full Name</th><th>Maintained By</th><th>What It Codes</th><th>Format</th></tr>
            <tr>
              <td><span class="badge badge-blue">ICD-10</span></td>
              <td>International Classification of Diseases, 10th Revision</td>
              <td>WHO (ICD-10) / CMS USA (ICD-10-CM)</td>
              <td>Diagnoses, diseases, conditions, reasons for encounter. WHY the patient is being treated.</td>
              <td>Alphanumeric: A00.0 – Z99.9</td>
            </tr>
            <tr>
              <td><span class="badge badge-cyan">CPT</span></td>
              <td>Current Procedural Terminology</td>
              <td>American Medical Association (AMA)</td>
              <td>Procedures, services, treatments. WHAT was done to the patient.</td>
              <td>5-digit numeric: 00100 – 99499</td>
            </tr>
            <tr>
              <td><span class="badge badge-violet">HCPCS</span></td>
              <td>Healthcare Common Procedure Coding System</td>
              <td>CMS (USA). Level I = CPT. Level II = Supplies/DME.</td>
              <td>Level II: supplies, equipment, drugs, ambulance, orthotics, prosthetics — things CPT doesn't cover.</td>
              <td>1 letter + 4 digits: A0000–V9999</td>
            </tr>
            <tr>
              <td><span class="badge badge-amber">DRG</span></td>
              <td>Diagnosis Related Group</td>
              <td>CMS (USA) / adapted by UAE hospitals</td>
              <td>Groups inpatient stays into categories based on primary diagnosis + procedures + complications. Used for inpatient payment.</td>
              <td>3-digit numeric group</td>
            </tr>
          </table>
        </div>
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">How They Work Together in a Claim</div>
          <div style="font-size:0.88rem;color:#9aa3b8;line-height:1.8;">
            A claim requires BOTH a diagnosis code (ICD-10) AND a procedure code (CPT/HCPCS).<br/>
            <strong style="color:#f0f2f8;">Example:</strong> Patient with acute appendicitis (ICD-10: K35.8) undergoes laparoscopic appendectomy (CPT: 44950).<br/>
            The insurer adjudicates: Is the diagnosis valid? Is the procedure medically necessary for that diagnosis? Is this covered under the TOB? Is there a sub-limit?<br/>
            In inpatient, the DRG groups this encounter for bundled payment calculation.
          </div>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">CPT Code Structure</div>
          <table class="styled-table">
            <tr><th>Range</th><th>Category</th><th>Examples</th></tr>
            <tr><td>00100–01999</td><td>Anaesthesia</td><td>00400 – anaesthesia for procedures on integumentary system</td></tr>
            <tr><td>10000–19999</td><td>Integumentary (skin/breast)</td><td>11400 – excision benign lesion. 19120 – breast lesion excision</td></tr>
            <tr><td>20000–29999</td><td>Musculoskeletal</td><td>27447 – total knee replacement. 23430 – shoulder repair</td></tr>
            <tr><td>30000–39999</td><td>Respiratory, Cardiovascular</td><td>31620 – bronchoscopy. 33510 – CABG</td></tr>
            <tr><td>40000–49999</td><td>Digestive System</td><td>43239 – upper GI endoscopy with biopsy. 44950 – appendectomy</td></tr>
            <tr><td>50000–59999</td><td>Urinary, Genital, Maternity</td><td>52352 – ureteroscopy. 59400 – vaginal delivery including antepartum care</td></tr>
            <tr><td>60000–69999</td><td>Endocrine, Nervous, Eye, Ear</td><td>66984 – cataract extraction. 63030 – lumbar disc surgery</td></tr>
            <tr><td>70000–79999</td><td>Radiology</td><td>70553 – MRI brain w/wo contrast. 73721 – MRI joint lower extremity</td></tr>
            <tr><td>80000–89999</td><td>Pathology & Laboratory</td><td>80048 – basic metabolic panel. 82040 – albumin</td></tr>
            <tr><td>90000–99999</td><td>Medicine / E&M</td><td>99213 – OP visit est patient low complexity. 97110 – therapeutic exercise (physio)</td></tr>
          </table>
        </div>
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">Physiotherapy CPT Codes (High-Use in UAE Claims)</div>
          <table class="styled-table">
            <tr><th>CPT</th><th>Description</th><th>Unit</th><th>UAE Usage Note</th></tr>
            <tr><td>97001</td><td>PT evaluation (initial assessment)</td><td>1 unit per session</td><td>Only on first session per condition. Not on follow-up sessions.</td></tr>
            <tr><td>97110</td><td>Therapeutic exercises</td><td>Per 15 min</td><td>Standard physio exercise component. Often 1–3 units per session.</td></tr>
            <tr><td>97140</td><td>Manual therapy techniques</td><td>Per 15 min</td><td>Increases to 2 units from 2nd–4th session in Mediclinic protocol.</td></tr>
            <tr><td>97530</td><td>Therapeutic activities</td><td>Per 15 min</td><td>Used for functional activity-based rehab</td></tr>
            <tr><td>97035</td><td>Ultrasound therapy</td><td>Per 15 min</td><td>Less common; requires specific indication</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class="glass-card">
          <div class="card-title">DRG — Diagnosis Related Groups for Inpatient</div>
          <p style="font-size:0.88rem;color:#9aa3b8;line-height:1.7;">
            A DRG groups an inpatient stay with clinically similar cases that are expected to use a similar level of hospital resources.
            The exact grouper, tariff, edits and payment rules depend on the applicable market and payer arrangement. In general,
            DRG-based payment is a case-based reimbursement method rather than a simple total of every line item.
          </p>
          <table class="styled-table">
            <tr><th>Element</th><th>How It Influences Grouping</th><th>Reviewer Prompt</th></tr>
            <tr><td>Principal diagnosis</td><td>Main condition established after study as chiefly responsible for the admission.</td><td>Does the discharge summary support the selected principal diagnosis?</td></tr>
            <tr><td>Secondary diagnoses</td><td>Relevant comorbidities or complications may affect severity. In MS-DRG terminology, some diagnoses are CCs or MCCs.</td><td>Was the condition clinically evaluated, monitored, treated or relevant to care?</td></tr>
            <tr><td>Procedures</td><td>Qualifying procedures may move a case into a surgical or procedure-based group.</td><td>Are procedure codes supported by the operative record and dates?</td></tr>
            <tr><td>Demographics and discharge status</td><td>Age, sex and discharge disposition can influence grouper logic in some systems.</td><td>Is the discharge status accurate: home, transfer, death, or against-medical-advice?</td></tr>
            <tr><td>Relative weight</td><td>Represents the relative resources associated with a group. A higher relative weight generally means a higher case-based payment before local adjustments.</td><td>Is the higher-weight group supported, or did documentation change after a query?</td></tr>
            <tr><td>Local tariff and adjustments</td><td>Local base rates, outliers, high-cost devices and payer rules may adjust the final reimbursement.</td><td>Apply the current DOH, DHA or payer-specific methodology; do not assume CMS payment rules apply locally.</td></tr>
          </table>
        </div>
        <div class="glass-card">
          <div class="card-title">A Practical DRG Grouping Walkthrough</div>
          <div class="timeline-item"><div class="timeline-dot" style="background:rgba(79,156,249,.18);color:#4f9cf9;">1</div><div><strong>Confirm the encounter:</strong> inpatient admission, dates, discharge status and complete clinical documentation.</div></div>
          <div class="timeline-item"><div class="timeline-dot" style="background:rgba(34,211,197,.18);color:#22d3c5;">2</div><div><strong>Validate diagnosis coding:</strong> identify the principal diagnosis after study, then review documented secondary diagnoses.</div></div>
          <div class="timeline-item"><div class="timeline-dot" style="background:rgba(167,139,250,.18);color:#a78bfa;">3</div><div><strong>Validate procedures:</strong> match procedure codes to operative notes, discharge summary and dates of service.</div></div>
          <div class="timeline-item"><div class="timeline-dot" style="background:rgba(251,191,36,.18);color:#fbbf24;">4</div><div><strong>Run the applicable grouper:</strong> the output is a DRG with severity logic and a relative weight. Use the local version required by the payer or authority.</div></div>
          <div class="timeline-item"><div class="timeline-dot" style="background:rgba(52,211,153,.18);color:#34d399;">5</div><div><strong>Review payment adjustments:</strong> base rate, outlier rules, eligible add-ons, high-cost devices and any contracted edits.</div></div>
          <div class="warning-box"><strong>Audit focus:</strong> Look for unsupported CC/MCC diagnoses, principal-diagnosis shifts without clinical basis, procedure-code mismatches, discharge-status errors, unbundling and unsupported outlier claims.</div>
          <div class="source-note">Reference starting points: <a href="https://www.doh.gov.ae/shafafiya/prices" target="_blank">DOH Shafafiya prices and methodologies</a>, <a href="https://www.doh.gov.ae/-/media/Feature/shafifya/standards/coding/DOH-Coding-Manual-CSv2021.ashx" target="_blank">DOH Coding Manual</a>, and <a href="https://www.cms.gov/medicare/payment/prospective-payment-systems/acute-inpatient-pps/ms-drg-classifications-and-software" target="_blank">CMS MS-DRG classifications and software</a>. Use UAE and payer requirements for live work.</div>
        </div>
        """, unsafe_allow_html=True)

    with tab4:
        st.markdown("""
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">UAE vs US Health Insurance — Key Differences</div>
          <table class="styled-table">
            <tr><th>Dimension</th><th>UAE System</th><th>US System</th></tr>
            <tr><td>Mandatory coverage</td><td>Yes — employer must provide. DHA/HAAD mandated.</td><td>Affordable Care Act (ACA) mandated but enforcement varies. Employer-sponsored is most common.</td></tr>
            <tr><td>Public safety net</td><td>Government hospitals for UAE nationals (Thiqa). Expats must have private insurance.</td><td>Medicare (65+), Medicaid (low income). Private for majority.</td></tr>
            <tr><td>Coding system</td><td>ICD-10 for diagnoses. CPT used widely. DRG for inpatient. No HCPCS Level II formal mandate — supply codes vary by TPA.</td><td>ICD-10-CM/PCS, CPT, HCPCS Level I & II, DRGs for CMS/Medicare. Highly standardised.</td></tr>
            <tr><td>Pre-authorisation</td><td>Very common — almost all imaging, procedures, IP require PA. Done through TPA portal in real-time.</td><td>Common but varies by payer. Prior auth has been a major debate (gold-carding, etc.).</td></tr>
            <tr><td>Network model</td><td>In-network direct billing. Out-of-network usually reimbursement or denied. Networks set by TPA contract.</td><td>HMO (referral needed), PPO (flexible, higher OOP out-of-network), EPO (strict network).</td></tr>
            <tr><td>Risk adjustment</td><td>Limited formal risk adjustment. Some reinsurance uses basic morbidity models.</td><td>ACA risk adjustment, Medicare Advantage HCC risk adjustment (RAF scores). Sophisticated CRC coding industry.</td></tr>
            <tr><td>Mental health parity</td><td>Mental health largely excluded in UAE basic plans. Emergency only.</td><td>Mental Health Parity and Addiction Equity Act (MHPAEA) requires equal coverage with medical.</td></tr>
            <tr><td>Claims currency</td><td>AED (UAE Dirham). Sub-limits and deductibles in AED.</td><td>USD. PMPM, deductibles in USD. Actuarial tables in USD.</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">HCC & Risk Adjustment Coding (AAPC CRC)</div>
          <p style="font-size:0.88rem;color:#9aa3b8;line-height:1.7;">
            Hierarchical Condition Categories (HCC) are used in risk-adjusted payment models — primarily US Medicare Advantage and ACA plans.
            The AAPC Certified Risk Adjustment Coder (CRC) credential focuses on this. Increasingly relevant in UAE as international reinsurers apply risk models.
          </p>
          <table class="styled-table">
            <tr><th>Concept</th><th>Explanation</th></tr>
            <tr><td>HCC Model</td><td>Groups ICD-10 diagnosis codes into approximately 70–80 HCC categories. Chronic, high-cost conditions each carry a relative factor.</td></tr>
            <tr><td>RAF Score</td><td>Risk Adjustment Factor. Sum of all HCC weights + demographic factors. Higher RAF = higher expected cost = higher capitation payment to insurer.</td></tr>
            <tr><td>Hierarchical</td><td>When a patient has related conditions of different severity (e.g., diabetic nephropathy), only the most severe/specific HCC counts. More specific coding = more accurate RAF.</td></tr>
            <tr><td>Suspect diagnosis</td><td>A condition suspected but not confirmed. Cannot be coded as confirmed (HCC missed). Physicians must document confirmed diagnoses to capture HCC credit.</td></tr>
            <tr><td>CRC audit focus</td><td>Ensuring all chronic conditions that were evaluated and treated during the year are coded at the highest specificity. Under-coding loses RAF. Over-coding is fraud.</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — PRE-EXISTING CONDITIONS
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "🔍  Pre-existing Conditions":
    st.session_state.progress["preex"] = True
    st.markdown('<div class="section-title">Pre-existing Conditions & Underwriting</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">How to identify, investigate, and handle undeclared pre-existing conditions (UNPEC) — the most complex area in UAE health insurance</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📖 Concepts & Rules", "🔬 UNPEC Investigation", "📂 File Audit"])

    with tab1:
        st.markdown("""
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">Key Definitions</div>
          <table class="styled-table">
            <tr><th>Term</th><th>Definition</th></tr>
            <tr><td><strong>Pre-existing condition (PEC)</strong></td><td>Any illness, disease, or injury for which the member received medical advice, diagnosis, care, or treatment before the policy effective date.</td></tr>
            <tr><td><strong>Declared PEC</strong></td><td>A pre-existing condition that was disclosed in the Medical Application Form (MAF) or declaration form at the time of enrollment. May be covered, excluded, or subject to loading.</td></tr>
            <tr><td><strong>Undeclared PEC (UNPEC)</strong></td><td>A pre-existing condition that existed before the policy but was NOT disclosed at enrollment. Grounds for claim denial under NCOV-002.</td></tr>
            <tr><td><strong>Waiting period</strong></td><td>A defined period (typically 6 months for EBP) after enrollment during which pre-existing or chronic conditions are not covered. After waiting period, declared PECs may become covered.</td></tr>
            <tr><td><strong>MAF</strong></td><td>Medical Application Form — individual/small group health declaration. Lists known conditions, medications, hospitalisations. Basis for underwriting decisions.</td></tr>
          </table>
        </div>
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">DHA 5-Year Rule</div>
          <div class="info-box">
            <strong>DHA Regulation:</strong> A pre-existing condition CANNOT be established if the last complaint, treatment, or documented investigation related to that condition was more than 5 years before the current policy effective date — AND there are no captured reports or treatment within the past 5 years.
            <br/><br/>This means: even if a patient had hypertension 8 years ago but has no records or treatment in the past 5 years, you cannot deny the current claim as UNPEC.
          </div>
        </div>
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">Waiting Period Rules</div>
          <table class="styled-table">
            <tr><th>Policy Type</th><th>Waiting Period</th><th>Notes</th></tr>
            <tr><td>EBP / Basic (standard)</td><td>6 months — pre-existing and chronic</td><td>Applies from member enrollment date. Check BOTH group and individual custom fields.</td></tr>
            <tr><td>EBP with zero waiting period flag</td><td>None</td><td>If member custom fields show zero waiting period and no MAF — pre-existing conditions are fully covered from day 1.</td></tr>
            <tr><td>Standard/Enhanced group</td><td>Usually none for group plans (>10 members)</td><td>Large groups typically waive waiting periods as part of group underwriting. Check TOB.</td></tr>
            <tr><td>Individual / small group (&lt;10)</td><td>Varies — check MAF and declaration</td><td>Individual policies always have underwriting. Second-year renewals: check if any new conditions arose during policy year.</td></tr>
            <tr><td>Late addition members</td><td>Depends on policy notes</td><td>Members joining after inception may be subject to underwriting. Check if policy notes specify late additions + confirm if this specific member is flagged.</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">UNPEC Detection — Investigation Workflow</div>
          <div class="timeline-item">
            <div class="timeline-dot" style="background:rgba(255,107,107,0.2);color:#ff6b6b;">1</div>
            <div><strong>Suspicion triggered</strong> — New member with chronic/complex condition shortly after enrollment. Provider reports long-standing condition. Patient history suggests onset before policy date.</div>
          </div>
          <div class="timeline-item">
            <div class="timeline-dot" style="background:rgba(251,191,36,0.2);color:#fbbf24;">2</div>
            <div><strong>Query onset</strong> — Send AUTH-012 requesting: exact date of onset, duration of condition, prior visits to any facility, previous investigations, current medications, history of treatment.</div>
          </div>
          <div class="timeline-item">
            <div class="timeline-dot" style="background:rgba(167,139,250,0.2);color:#a78bfa;">3</div>
            <div><strong>Evaluate response</strong> — Does onset predate policy effective date? Compare to enrollment date, check declaration form/MAF for this condition. Check custom fields.</div>
          </div>
          <div class="timeline-item">
            <div class="timeline-dot" style="background:rgba(79,156,249,0.2);color:#4f9cf9;">4</div>
            <div><strong>Payer-specific rules apply</strong> — Some PICs require escalation. Evidence thresholds differ (see table below).</div>
          </div>
          <div class="timeline-item">
            <div class="timeline-dot" style="background:rgba(52,211,153,0.2);color:#34d399;">5</div>
            <div><strong>Document and act</strong> — Update medical file. Raise UNPEC sheet. Deny with NCOV-002 or approve if investigation clears. For ambiguous cases: give benefit of doubt for initial investigations.</div>
          </div>
        </div>
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">Payer-Specific UNPEC Rules</div>
          <table class="styled-table">
            <tr><th>Payer Type</th><th>Denial Basis</th><th>Escalation Required?</th><th>Notes</th></tr>
            <tr><td>Watania / AIAW / Orient</td><td>Signed & stamped medical reports with specific date of onset. Diagnosis-based (not S&S alone). Grey zone cases escalated.</td><td>Yes — mandatory PIC escalation</td><td>Cannot deny on symptoms alone. Must have documented diagnosis + date.</td></tr>
            <tr><td>Dubai Insurance / DNIRC</td><td>Extremely strict. Even signs & symptoms sufficient. Slightest evidence of pre-existing = full support for denial.</td><td>No escalation needed</td><td>Most aggressive payer for UNPEC denials.</td></tr>
            <tr><td>Generali / Integra Global (GGH)</td><td>Standard evidence required. All UNPEC must be escalated.</td><td>Yes — escalate to GGH</td><td>HIV, Hep B/C are not excluded under IG — don't deny those.</td></tr>
            <tr><td>Salama / National Takaful (Watania)</td><td>Standard — escalate before denial.</td><td>Yes</td><td>Follow same protocol as Orient.</td></tr>
            <tr><td>All other payers</td><td>Can deny based on S&S alone if signed & stamped report confirms pre-existing nature.</td><td>No escalation needed</td><td>Document thoroughly. Update medical file.</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">File Audit Workflow</div>
          <div class="info-box">File audits are triggered when a case is suspected to be UNPEC, when there is a discrepancy in onset history, or when the claim value warrants deeper review.</div>
          <table class="styled-table">
            <tr><th>Trigger</th><th>Threshold / Condition</th></tr>
            <tr><td>High-value claim</td><td>Generally cases above AED 4,000–5,000. Confirm internal threshold with TPA policy.</td></tr>
            <tr><td>UNPEC suspicion</td><td>When onset investigation reveals possible pre-existing condition and documentation supports it.</td></tr>
            <tr><td>Onset discrepancy</td><td>Member and provider give conflicting accounts of onset date or treatment history.</td></tr>
            <tr><td>Suspected fraud</td><td>Unusual billing patterns, duplicate requests, provider-member collusion signs.</td></tr>
            <tr><td>Recently enrolled with complex chronic condition</td><td>New member presenting with long-standing condition (e.g., advanced DM with nephropathy on first visit).</td></tr>
          </table>
          <div style="margin-top:1rem;font-weight:600;margin-bottom:0.6rem;">File Audit Process</div>
          <div class="timeline-item"><div class="timeline-dot" style="background:rgba(79,156,249,0.2);color:#4f9cf9;">1</div><div>Ensure provider has specified exact onset date before raising FA ticket. No FA ticket without onset information.</div></div>
          <div class="timeline-item"><div class="timeline-dot" style="background:rgba(167,139,250,0.2);color:#a78bfa;">2</div><div>Fill FA form. Attach all received medical reports. Raise ticket to Medical Investigation Unit (MIU).</div></div>
          <div class="timeline-item"><div class="timeline-dot" style="background:rgba(34,211,197,0.2);color:#22d3c5;">3</div><div>Email subject format: <code>FILE AUDIT FOR [Member Name] – [Card No.] – [Insurance Company]</code></div></div>
          <div class="timeline-item"><div class="timeline-dot" style="background:rgba(251,191,36,0.2);color:#fbbf24;">4</div><div>Pending FA: update medical file with "request pending provider for onset documentation." Approve initial diagnostic investigations while investigation is ongoing.</div></div>
          <div class="timeline-item"><div class="timeline-dot" style="background:rgba(52,211,153,0.2);color:#34d399;">5</div><div>FA outcome: If UNPEC confirmed → update UNPEC sheet → deny related claims with NCOV-002. If cleared → approve ongoing treatment.</div></div>
          <div class="warning-box" style="margin-top:0.8rem;">Avoid multiple denials asking for information. One query → case management → FA if needed. Do not raise FA for cases below AED 5,000 unless fraud suspicion or discrepancy exists.</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 7 — INPATIENT & EMERGENCY
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "🏥  Inpatient & Emergency":
    st.session_state.progress["inpatient"] = True
    st.markdown('<div class="section-title">Inpatient & Emergency Rules</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">IP authorisation, the 24-hour rule, DRG grouping, length of stay, and emergency stabilisation requirements</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🏥 IP Authorisation", "🚨 Emergency Rules", "💰 DRG & Payment"])

    with tab1:
        st.markdown("""
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">Inpatient (IP) Prior Authorisation Rules</div>
          <div class="warning-box"><strong>Critical Rule:</strong> Inpatient treatment without prior authorisation will be denied — NCOV-003 / Auth-001. No exceptions except genuine emergency cases notified within 24 hours.</div>
          <table class="styled-table" style="margin-top:0.8rem;">
            <tr><th>Step</th><th>Action</th><th>Responsible</th></tr>
            <tr><td>1</td><td>Provider submits IP PA request with admitting diagnosis (ICD-10), proposed procedure (CPT), estimated LoS, estimated cost, clinical notes</td><td>Hospital admissions/billing team</td></tr>
            <tr><td>2</td><td>TPA checks: eligibility, network, IP coverage (not all plans have IP), annual limit remaining, waiting period, exclusions</td><td>TPA adjudicator</td></tr>
            <tr><td>3</td><td>Medical review: Is admission medically necessary? Can treatment safely be done as OP? Is LoS appropriate?</td><td>TPA medical reviewer</td></tr>
            <tr><td>4</td><td>High-value cases (above payer escalation matrix threshold): escalate to PIC for approval</td><td>TPA → PIC</td></tr>
            <tr><td>5</td><td>Approval issued with reference code, authorised LoS, and any conditions (e.g., concurrent review at 48hrs)</td><td>TPA</td></tr>
            <tr><td>6</td><td>Patient admitted. Any extension of stay requires re-authorisation. Discharge coding determines DRG.</td><td>Hospital + TPA</td></tr>
          </table>
        </div>
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">Length of Stay (LoS) Guidelines</div>
          <p style="font-size:0.88rem;color:#9aa3b8;line-height:1.7;">
            TPAs use clinical LoS benchmarks (Milliman, MCG, or internally defined) to assess whether a requested admission length is appropriate.
            An LoS longer than the benchmark requires clinical justification (complications, comorbidities, post-op concerns).
          </p>
          <div class="info-box">Any treatment that can safely be done on an outpatient basis must NOT be admitted as inpatient. This is both a DHA/HAAD exclusion and a standard denial reason (CLAI-012 type). Example: minor procedures, simple injections, observations without active treatment.</div>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">Emergency Rules — UAE Standard</div>
          <div class="success-box"><strong>Principle:</strong> Any genuine emergency must be stabilised regardless of network, coverage, or exclusions. Cost of emergency stabilisation is always covered to the point of stabilisation.</div>
          <table class="styled-table" style="margin-top:0.8rem;">
            <tr><th>Triage Level</th><th>Category</th><th>Insurance Action</th></tr>
            <tr><td>Triage 1</td><td>Immediate — life-threatening</td><td>Cover until stabilisation. No PA required. Notify insurer within 24 hours.</td></tr>
            <tr><td>Triage 2</td><td>Emergent — urgent</td><td>Cover until stabilisation. Notify within 24 hours. Reassess for ongoing coverage.</td></tr>
            <tr><td>Triage 3</td><td>Urgent</td><td>Borderline — assess clinical notes. Generally considered emergency.</td></tr>
            <tr><td>Triage 4–5</td><td>Less urgent / Non-urgent</td><td>Not emergency. Requires PA. EBP members should have visited clinic first.</td></tr>
          </table>
          <div class="warning-box" style="margin-top:0.8rem;"><strong>24-Hour Notification Rule:</strong> For emergency admissions, the hospital or member must notify the TPA/insurer within 24 hours of admission where possible. Failure to notify does not void emergency coverage but may complicate PA for ongoing stay.</div>
        </div>
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">EBP Emergency Access Rules</div>
          <table class="styled-table">
            <tr><th>Situation</th><th>EBP Rule</th></tr>
            <tr><td>Consultation at hospital — night hours (10pm–8am)</td><td>Allowed if GP consultation and member has IP coverage at that facility</td></tr>
            <tr><td>Life-threatening emergency (any hour)</td><td>Allowed — cover to point of stabilisation</td></tr>
            <tr><td>Consultation with referral from EBP OP clinic</td><td>Allowed at IP facility if member has IP coverage there</td></tr>
            <tr><td>Work-related injury (EBP)</td><td>Emergency only to stabilisation. Elective WRI: deny immediately.</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class="glass-card">
          <div class="card-title">DRG — Inpatient Payment Logic</div>
          <p style="font-size:0.88rem;color:#9aa3b8;line-height:1.7;">
            Diagnosis Related Groups are case-based categories for inpatient reimbursement. A grouper processes the coded encounter
            and returns a DRG. The payment calculation then applies the relevant local tariff, relative weight, contract terms and any eligible adjustments.
          </p>
          <table class="styled-table">
            <tr><th>Review Layer</th><th>What to Validate</th><th>Common Risk</th></tr>
            <tr><td>Clinical</td><td>Reason for admission, inpatient necessity, course of treatment, LoS and discharge plan</td><td>Admission that could safely be outpatient; unsupported extension of stay</td></tr>
            <tr><td>Coding</td><td>Principal diagnosis, secondary diagnoses, procedures, dates and discharge status</td><td>Unsupported CC/MCC, incorrect sequencing, missing or mismatched procedure code</td></tr>
            <tr><td>Grouping</td><td>Correct local grouper version and expected DRG result</td><td>Using the wrong grouper version or overlooking a material edit</td></tr>
            <tr><td>Payment</td><td>Relative weight, base rate, outlier logic, high-cost device rules and contracted adjustments</td><td>Unsupported add-on, incorrect outlier, unbundled line items</td></tr>
            <tr><td>Audit trail</td><td>Discharge summary, operative report, lab/radiology evidence and coding-query history</td><td>Post-discharge documentation changes without a clear clinical basis</td></tr>
          </table>
          <div class="warning-box" style="margin-top:0.8rem;"><strong>Do not use this page as a tariff calculator.</strong> Current DOH, DHA and payer rules, grouper versions and contracts must be checked for live adjudication.</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 8 — INTERNAL AUDIT
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "🔎  Internal Audit":
    st.session_state.progress["audit"] = True
    st.markdown('<div class="section-title">Internal Audit in Health Insurance</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Risk-based auditing, FWA detection, DRG audit, coding compliance, and documentation standards</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔎 Audit Fundamentals", "⚠️ Fraud, Waste & Abuse", "📋 Audit Documentation"])

    with tab1:
        st.markdown("""
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">Types of Health Insurance Audit</div>
          <table class="styled-table">
            <tr><th>Type</th><th>When Done</th><th>Focus</th></tr>
            <tr><td><span class="badge badge-blue">Desk / Retrospective Review</span></td><td>Post-claim payment — random or triggered</td><td>Review of paid claims for coding accuracy, medical necessity, correct DRG assignment, UNPEC</td></tr>
            <tr><td><span class="badge badge-cyan">Concurrent Review</span></td><td>During active inpatient admission</td><td>Ongoing LoS appropriateness, continued stay necessity, discharge planning</td></tr>
            <tr><td><span class="badge badge-violet">Prospective Review</span></td><td>Before service — PA process</td><td>Is the requested service medically necessary and appropriate before approval?</td></tr>
            <tr><td><span class="badge badge-amber">File Audit (FA)</span></td><td>Triggered by UNPEC suspicion or high value</td><td>Deep review of member's complete medical file for undeclared conditions, onset verification</td></tr>
            <tr><td><span class="badge badge-coral">Provider Audit</span></td><td>Periodic or triggered by anomaly</td><td>Provider billing patterns, upcoding, unbundling, phantom services, outlier utilisation</td></tr>
          </table>
        </div>
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">Risk-Based Audit — High-Risk Indicators</div>
          <p style="font-size:0.88rem;color:#9aa3b8;margin-bottom:0.8rem;">Audit resources are limited — risk-based approach focuses on highest-probability issues:</p>
          <table class="styled-table">
            <tr><th>Risk Indicator</th><th>Why It Matters</th><th>Audit Action</th></tr>
            <tr><td>New member with chronic condition</td><td>High UNPEC probability</td><td>Trigger onset investigation. Cross-check with declaration form.</td></tr>
            <tr><td>Frequent high-value imaging requests</td><td>Possible overutilisation or kickback arrangement</td><td>Review clinical justification trend for same member/provider</td></tr>
            <tr><td>Same diagnosis repeated quickly</td><td>May indicate chronic/UNPEC or duplicate billing</td><td>Check approval history, DUPL-001 risk, MNEC-005</td></tr>
            <tr><td>Outlier LoS vs DRG benchmark</td><td>Possible inappropriate admission or DRG upcoding</td><td>Concurrent review. Clinical documentation audit.</td></tr>
            <tr><td>Provider billing pattern anomaly</td><td>Upcoding, unbundling, modifiers abuse</td><td>Comparative analysis vs peer providers. E&M level distribution review.</td></tr>
            <tr><td>Multiple claims same day from different providers</td><td>Possible coordination of care issues or duplicate</td><td>Cross-claim review. DUPL-001 check.</td></tr>
            <tr><td>High OP-to-IP conversion rate at single provider</td><td>Possible admissions manipulation for DRG revenue</td><td>Medical necessity review of admissions from that provider</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">Fraud, Waste & Abuse (FWA) — Definitions</div>
          <table class="styled-table">
            <tr><th>Category</th><th>Definition</th><th>Example</th></tr>
            <tr><td><span class="badge badge-coral">Fraud</span></td><td>Intentional deception for financial gain. Criminal act.</td><td>Billing for services never rendered. Forging clinical notes. UNPEC concealment.</td></tr>
            <tr><td><span class="badge badge-amber">Waste</span></td><td>Overutilisation or misuse without intentional deception. No criminal intent.</td><td>Ordering unnecessary tests. Admitting patients who could be managed OP.</td></tr>
            <tr><td><span class="badge badge-blue">Abuse</span></td><td>Practices inconsistent with sound medical/billing practices. May involve deception.</td><td>Upcoding E&M levels. Unbundling procedures that should be bundled.</td></tr>
          </table>
        </div>
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">Common FWA Schemes in UAE Health Insurance</div>
          <table class="styled-table">
            <tr><th>Scheme</th><th>Description</th><th>Detection Method</th></tr>
            <tr><td>Upcoding</td><td>Billing a more complex/expensive CPT or DRG than actually performed. E.g., billing E&M 99215 (complex) for a routine 99213 visit.</td><td>E&M distribution analysis. DRG CC/MCC rate outlier.</td></tr>
            <tr><td>Unbundling</td><td>Billing components of a procedure separately when a comprehensive code exists that should cover all components. E.g., billing for each component of a panel test separately.</td><td>CCI (Correct Coding Initiative) edits review. Column 1/2 code analysis.</td></tr>
            <tr><td>Phantom billing</td><td>Billing for services never rendered. Patient did not attend; no service given.</td><td>Member confirmation calls. Visit log cross-check. GPS verification.</td></tr>
            <tr><td>Duplicate billing</td><td>Submitting the same claim multiple times to collect double payment.</td><td>DUPL-001 flags. Same date/same CPT/same provider cross-check.</td></tr>
            <tr><td>Kickbacks</td><td>Provider receives financial incentive to refer to a specific facility or prescribe specific drugs.</td><td>Referral pattern analysis. Provider relationship investigation.</td></tr>
            <tr><td>Unnecessary admissions</td><td>Admitting patient as IP for revenue when OP management is appropriate and safe.</td><td>LoS benchmarking. OP-to-IP rate analysis. Clinical review.</td></tr>
            <tr><td>Modifier abuse</td><td>Using modifiers (like -25, -59) inappropriately to bypass bundling rules and get paid for additional procedures.</td><td>Modifier utilisation rate review. Supporting documentation audit.</td></tr>
            <tr><td>UNPEC concealment</td><td>Member or provider deliberately conceals pre-existing condition to obtain coverage.</td><td>File audit. Onset investigation. Cross-facility medical history.</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">Audit Documentation Standards</div>
          <p style="font-size:0.88rem;color:#9aa3b8;margin-bottom:0.8rem;">A well-documented audit finding must include all of the following to be actionable and defensible:</p>
          <table class="styled-table">
            <tr><th>Element</th><th>What to Include</th></tr>
            <tr><td>Member identification</td><td>Member name, card number, policy number, insurer, TPA reference</td></tr>
            <tr><td>Claim details</td><td>Date(s) of service, claim reference, provider name, CPT/ICD-10 codes billed</td></tr>
            <tr><td>Finding description</td><td>Specific issue identified — what was billed, what should have been billed, or what documentation is missing</td></tr>
            <tr><td>Evidence</td><td>Clinical notes reviewed, reports received, date of onset evidence, billing records</td></tr>
            <tr><td>Applicable standard</td><td>Which exclusion clause, coding guideline, medical necessity standard, or policy term was violated</td></tr>
            <tr><td>Financial impact</td><td>Amount paid vs amount that should have been paid. Recovery amount if applicable.</td></tr>
            <tr><td>Recommendation</td><td>Deny / Recoup / Education / Refer to compliance / Escalate to PIC</td></tr>
            <tr><td>Audit trail</td><td>Who reviewed, date of review, approval chain for findings</td></tr>
          </table>
          <div class="info-box" style="margin-top:0.8rem;">
            <strong>File Audit email format:</strong><br/>
            To: MIU (Medical Investigation Unit) / Dr. Priyanka<br/>
            CC: MCU, MedNet Approvals, Compliance Lead<br/>
            Subject: <code>FILE AUDIT FOR [Member Name] – [Card No.] – [Insurance Company Name]</code>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 9 — SPECIALTY RULES
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "💊  Specialty Rules":
    st.session_state.progress["specialty"] = True
    st.markdown('<div class="section-title">Specialty Rules</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Physiotherapy, pharmacy/Rx, maternity, dental — the rules that vary most between policies</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🦴 Physiotherapy", "💊 Pharmacy & Rx", "🤱 Maternity", "🦷 Dental"])

    with tab1:
        st.markdown("""
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">Physiotherapy Rules by Policy Type</div>
          <table class="styled-table">
            <tr><th>Policy Type</th><th>Max Sessions / Request</th><th>Progress Report</th><th>Notes</th></tr>
            <tr><td>Standard/Enhanced plans</td><td>5 sessions</td><td>After every 5 sessions</td><td>Progress report with pain scale, functional improvement, treatment plan. Update medical file.</td></tr>
            <tr><td>EBP / Basic / Silk Road</td><td>3 sessions (from 6-session limit)</td><td>After every 3 sessions</td><td>Check TOB for session limit first. Most EBP plans have 6-session total limit.</td></tr>
            <tr><td>Generali (sessions limit)</td><td>5 sessions</td><td>After every 5</td><td>If limit in AED not sessions — approve up to the AED limit.</td></tr>
            <tr><td>Expacare</td><td>7 sessions per complaint/site</td><td>After 7, send Expacare template</td><td>After 7 sessions, fill Expacare template → email to provider → escalate to PIC for approval.</td></tr>
            <tr><td>TPA / Futtaim (Al Futtaim)</td><td>5 sessions (no progress report needed)</td><td>Not required</td><td>Futtaim has flexible rules. Check network (HealthHub providers only).</td></tr>
          </table>
          <div class="warning-box" style="margin-top:0.8rem;"><strong>Rehab vs Treatment:</strong> Physiotherapy after surgery is NOT rehab — it's treatment and proceeds normally. Physiotherapy after stroke, amputation, or brain injury = rehab. Check TOB for rehab benefit separately.</div>
        </div>
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">Mediclinic Physiotherapy CPT Protocol</div>
          <table class="styled-table">
            <tr><th>Session</th><th>CPT 97001</th><th>CPT 97140</th><th>CPT 97110</th></tr>
            <tr><td>1st session</td><td>1 unit ✅</td><td>1 unit</td><td>1 unit</td></tr>
            <tr><td>2nd–4th sessions</td><td>Not included ❌</td><td>2 units</td><td>1 unit</td></tr>
            <tr><td>5th session</td><td>Not included ❌</td><td>2 units</td><td>Denied ❌ (included in session)</td></tr>
            <tr><td>6th session onwards</td><td colspan="3" style="text-align:center;">Deny with "approved up to 5 sessions"</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">Pharmacy & Prescription Drug Rules</div>
          <table class="styled-table">
            <tr><th>Category</th><th>Coverage Status</th><th>Notes</th></tr>
            <tr><td>Prescription medications (generic)</td><td><span class="badge badge-green">Generally covered</span></td><td>Must be prescribed by licensed physician. Related to covered diagnosis.</td></tr>
            <tr><td>Brand vs generic</td><td><span class="badge badge-amber">Plan-dependent</span></td><td>Many policies cover generic only, or require step therapy (generic first). Check formulary tier.</td></tr>
            <tr><td>Vitamins / minerals</td><td><span class="badge badge-coral">Excluded</span></td><td>Unless prescribed alongside antibiotics or as replacement therapy for documented deficiency.</td></tr>
            <tr><td>Contraceptives</td><td><span class="badge badge-coral">Excluded</span></td><td>Standard exclusion across all plan types.</td></tr>
            <tr><td>Psychiatric medications</td><td><span class="badge badge-coral">Excluded</span></td><td>Standard pharmaceutical exclusion (Northern Emirates/non-DHA). Under DHA/HAAD check TOB for mental health emergency coverage.</td></tr>
            <tr><td>Hormonal replacement therapy (HRT)</td><td><span class="badge badge-coral">Excluded</span></td><td>Standard exclusion.</td></tr>
            <tr><td>Acne medications</td><td><span class="badge badge-coral">Excluded</span></td><td>Cosmetic exclusion — included in pharmaceutical exclusion list.</td></tr>
            <tr><td>Durable medical equipment (DME)</td><td><span class="badge badge-amber">TOB-dependent</span></td><td>Glucometers, nebulizers, blood pressure monitors. Check TOB for DME coverage. Some policies list as "Prescribed Medical Aids."</td></tr>
          </table>
        </div>
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">Vitamin D — Special Rules</div>
          <div class="info-box">
            Vitamin D testing is considered screening for reinsured and individual policies.<br/>
            <strong>Criteria for approval:</strong><br/>
            1. High-risk group (elderly, veiled, chronic malabsorption, osteoporosis) — evaluate for deficiency<br/>
            2. Previous test showing insufficiency/deficiency + supplementation history required<br/>
            3. Retesting: annual only if deficiency confirmed. Not approved if proper supplementation was not taken.<br/>
            4. Denial if: no prior test, no supplementation history, or test within less than 12 months without new clinical reason.
          </div>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">Maternity Coverage Rules — UAE</div>
          <table class="styled-table">
            <tr><th>Service</th><th>Rule</th></tr>
            <tr><td>Maternity package (IP)</td><td>Some policies offer a bundled maternity package (e.g., normal delivery package AED X). Member must apply for this package specifically — not itemised billing.</td></tr>
            <tr><td>NT scan (Nuchal Translucency)</td><td>Covered only between <strong>11–13 weeks gestation</strong>. Outside this window: deny with NCOV-003 citing DHA maternity protocol.</td></tr>
            <tr><td>Anomaly scan</td><td>Covered only between <strong>18–20 weeks gestation</strong>. Require ultrasound report showing gestational age + LMP to verify timing.</td></tr>
            <tr><td>Routine antenatal consultations</td><td>Covered if maternity benefit is included in TOB. EBP may have limited antenatal visits.</td></tr>
            <tr><td>C-section</td><td>Higher package/itemised cost. Medical necessity must be documented. Elective C-section may require additional justification.</td></tr>
            <tr><td>Maternity for EBP members</td><td>Check TOB carefully. Basic EBP may cover only medically necessary maternity or emergency. Some exclude elective maternity entirely.</td></tr>
            <tr><td>Gestational diabetes / hypertension</td><td>Generally covered as new medical conditions arising during pregnancy, subject to maternity benefit and TOB.</td></tr>
          </table>
          <div class="warning-box" style="margin-top:0.8rem;">Always request: ultrasound report with gestational age + LMP date before approving any maternity-timed scan. Without this, you cannot verify the coverage window.</div>
        </div>
        """, unsafe_allow_html=True)

    with tab4:
        st.markdown("""
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">Dental Coverage Rules</div>
          <table class="styled-table">
            <tr><th>Check</th><th>What to Do</th></tr>
            <tr><td>1. Dental benefit in TOB?</td><td>Check custom fields for dental coverage. Check dental network access. Dental is a standard exclusion unless explicitly added in TOB.</td></tr>
            <tr><td>2. Requesting provider in dental network?</td><td>Verify against dental network list (not applicable for Generali, Integra Global, Expacare who have open dental networks).</td></tr>
            <tr><td>3. Sub-limit remaining?</td><td>Dental sub-limits are typically separate from annual medical limit (e.g., AED 3,000 dental per year).</td></tr>
            <tr><td>4. Scope of coverage</td><td>Basic dental typically covers: consultation, extraction, simple fillings. Cosmetic dentistry, implants, orthodontics, dental prostheses are almost universally excluded.</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 10 — CASE STUDIES
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "🎯  Case Studies":
    st.session_state.progress["cases"] = True
    st.markdown('<div class="section-title">Case Study Simulator</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">10 real-world scenarios. Read the case, decide: Approve / Deny / Query / Escalate</div>', unsafe_allow_html=True)

    st.markdown("""<div class="disclaimer">
      These cases are fictional training scenarios inspired by common real-world patterns. They do not represent any real member or claim.
      Decisions in practice must be based on the member's specific TOB, medical file, and applicable regulatory framework.
    </div>""", unsafe_allow_html=True)

    cases = [
        {
            "id": 1, "title": "MRI Lumbar Spine — EBP Member",
            "scenario": """
**Member:** 34-year-old male, EBP policy, enrolled 2 months ago.
**Provider request:** MRI lumbar spine (CPT 72148), cost AED 950.
**Diagnosis:** M54.5 — Low back pain.
**Attachments:** Referral from GP. No X-ray. No physiotherapy records. Doctor notes: "Patient complains of low back pain x 3 weeks."
""",
            "options": ["✅ Approve — GP referred and it's medically necessary", "❌ Deny — Not medically justified", "📋 Query — Request X-ray and conservative management history", "📤 Escalate to PIC"],
            "answer": 2,
            "explanation": "MRI spine is NOT first-line. X-ray must precede, and conservative management (physiotherapy, analgesics) must be documented. 3 weeks of symptoms without prior management is insufficient. Send AUTH-012 requesting: X-ray report, details of conservative management (duration, response), and physiotherapy history if any. Also note: EBP member, only 2 months enrolled — check waiting period for any chronic spine condition."
        },
        {
            "id": 2, "title": "Echocardiogram — Chest Pain",
            "scenario": """
**Member:** 55-year-old female, standard group plan, Dubai (DHA policy).
**Provider request:** Echocardiogram (CPT 93306), cost AED 1,200.
**Diagnosis:** R07.9 — Chest pain, unspecified.
**Attachments:** None provided.
""",
            "options": ["✅ Approve — Echo is standard cardiac workup", "❌ Deny — Not medically necessary", "📋 Query — Request ECG, TMT, and cardiac enzyme results", "📤 Escalate"],
            "answer": 2,
            "explanation": "Echo is NOT first-line for chest pain without structural cardiac evidence. Protocol requires ECG, TMT (treadmill test), and cardiac enzymes first. If these show abnormalities (ST changes, positive troponin, pathological ECG), then echo is justified. Send AUTH-012 requesting: ECG report, TMT results, cardiac enzyme results, and details of chest pain (onset, character, radiation)."
        },
        {
            "id": 3, "title": "Physiotherapy — Progress Report Needed",
            "scenario": """
**Member:** 28-year-old female, standard plan, non-EBP.
**Provider request:** 5 physiotherapy sessions (CPT 97110 x5), cost AED 750. Diagnosis: M75.1 — Rotator cuff syndrome.
**Attachments:** Referral letter from orthopaedic surgeon. Medical file shows: 5 physiotherapy sessions already approved 4 weeks ago for same condition.
""",
            "options": ["✅ Approve — Referral attached and condition ongoing", "❌ Deny — Already approved 5 sessions", "📋 Query — Request physiotherapy progress report from previous sessions", "📤 Escalate — High-value case"],
            "answer": 2,
            "explanation": "A progress report is mandatory before approving the next batch of sessions when a previous batch has been given. The progress report should show: current pain scale (VAS score), functional improvement, treatment plan for next sessions, and whether goals have been met. Approve next 5 sessions only after reviewing the progress report confirming continued need and measurable improvement."
        },
        {
            "id": 4, "title": "UNPEC Suspicion — New Member with DM",
            "scenario": """
**Member:** 45-year-old male, enrolled 6 weeks ago, enhanced plan (no waiting period stated in TOB).
**Provider request:** Follow-up consultation for Type 2 Diabetes Mellitus (E11.9) + renewal of medications (Metformin, Sitagliptin), cost AED 650.
**Attachments:** Doctor note mentions patient has been on diabetic medications "for several years."
""",
            "options": ["✅ Approve — No waiting period on this plan", "❌ Deny — Pre-existing condition", "📋 Query — Request onset date, declaration form review, previous records", "📤 Escalate to PIC immediately"],
            "answer": 2,
            "explanation": "Even with no waiting period, an UNDECLARED pre-existing condition can be denied (NCOV-002). The phrase 'on medications for several years' is a red flag. You must: (1) Check the MAF/declaration form for DM declaration. (2) Query onset: when was DM first diagnosed? Who prescribed the medications? Any prior hospitalisation? (3) If DM onset predates enrollment and was not declared, this is UNPEC. Check policy payer — if Orient/AIAW/Watania, escalate to PIC before denying. Approve initial investigations while investigating."
        },
        {
            "id": 5, "title": "Vitamin D Test — Annual Repeat",
            "scenario": """
**Member:** 32-year-old female, individual reinsured policy, Dubai.
**Provider request:** Vitamin D 25-OH test (CPT 82306), cost AED 185. Doctor note: "Patient requests vitamin D check."
**Attachments:** Previous test from 8 months ago (result: 42 nmol/L — insufficient).
""",
            "options": ["✅ Approve — Patient had deficiency last time", "❌ Deny — Vitamin D tested within 12 months", "📋 Query — Request supplementation history before deciding", "📤 Escalate"],
            "answer": 2,
            "explanation": "Vitamin D retesting is denied if: (a) less than 12 months since last test, AND (b) adequate supplementation has not been demonstrated. 8 months is less than the annual repeat interval. Send AUTH-012: 'Regret to inform you that the test is denied in view of absence of proper vitamin D supplementation AND test done within 12 months. Please provide supplementation history and previous prescriptions.' If supplementation history is provided and the period is appropriate, reassess."
        },
        {
            "id": 6, "title": "Emergency — Out-of-Network Hospital",
            "scenario": """
**Member:** 40-year-old male, EBP policy. Was involved in a fall with head injury.
**Provider request:** Emergency admission at a hospital NOT in the member's EBP network. CT brain requested + 24-hour observation. Total cost AED 7,800.
**Triage level:** Triage 2 (Emergent).
""",
            "options": ["✅ Approve in full — Emergency overrides network restrictions", "❌ Deny — Out of network", "📋 Approve to stabilisation point only, then transfer to network", "📤 Escalate to PIC for high value"],
            "answer": 2,
            "explanation": "Emergency care must be covered regardless of network — this is a DHA/HAAD regulatory requirement. Approve to stabilisation. CT brain with head injury + Triage 2 = genuine emergency. Stabilisation = once medically stable (head CT reviewed, no surgical intervention needed, observation period for monitoring). Once stabilised: advise transfer to network facility for ongoing care if needed. EBP rule: emergency covered to stabilisation even out-of-network. Mark approval with emergency reference. Notify PIC given value (AED 7,800 triggers escalation matrix)."
        },
        {
            "id": 7, "title": "Circumcision — HAAD Policy",
            "scenario": """
**Member:** 8-year-old child, HAAD (Abu Dhabi) policy.
**Provider request:** Circumcision (CPT 54161), elective/ritual, cost AED 2,200.
**Attachments:** Parent consent form. No medical indication documented.
""",
            "options": ["✅ Approve — Child is under 18", "❌ Deny — Standard HAAD exclusion", "📋 Query — Request medical necessity documentation", "📤 Escalate to PIC"],
            "answer": 1,
            "explanation": "Circumcision is a STANDARD EXCLUSION under HAAD policies — Exclusion clause 36. This applies regardless of age. Under DHA policies: covered 0–2 years, and medically necessary cases beyond 2 years. This is a HAAD policy — deny with NCOV-003 citing: 'Excluded under HAAD Exclusion Clause 36: Circumcision healthcare services.' If the provider claims medical necessity (phimosis, recurrent infections), query for documentation, but the standard HAAD position remains exclusion without medical indication documented by a urologist/surgeon."
        },
        {
            "id": 8, "title": "STD Coverage — DHA vs HAAD",
            "scenario": """
**Scenario A:** Member with DHA policy presents with HPV infection. Provider requests consultation + treatment, AED 850.
**Scenario B:** Member with HAAD policy presents with HPV infection. Same request, AED 850.
""",
            "options": ["Approve both — STD coverage is the same across UAE", "Approve DHA, Deny HAAD — Different exclusion rules", "Deny both — STDs excluded everywhere", "Query both — Need more clinical detail"],
            "answer": 1,
            "explanation": "This is one of the most important DHA vs HAAD differences. Under DHA: HPV infection is covered as per medical necessity — it is NOT a standard exclusion (updated DHA guidance). Under HAAD: all sexually transmitted diseases/venereal diseases are a standard exclusion (Clause 56). Therefore: Approve DHA member. Deny HAAD member with NCOV-001: 'Excluded under HAAD Exclusion Clause 56: Venereal/sexually transmitted diseases.'"
        },
        {
            "id": 9, "title": "Colonoscopy — Without Adequate Criteria",
            "scenario": """
**Member:** 38-year-old male, standard plan. No prior GI history in medical file.
**Provider request:** Colonoscopy (CPT 45378), cost AED 3,500.
**Diagnosis:** K57.30 — Diverticulosis. Doctor note: "Patient complains of occasional bloating and gas for 1 month."
**Attachments:** None.
""",
            "options": ["✅ Approve — Colonoscopy appropriate for diverticulosis", "❌ Deny — Not medically necessary", "📋 Query — Request prior investigations and clinical history", "📤 Escalate — High value over AED 3,000"],
            "answer": 2,
            "explanation": "Colonoscopy requires significant clinical justification. 1 month of bloating and gas WITHOUT: prior GI investigations (calprotectin, FOB, H. pylori test), history of chronic GI condition, or emergency indication (bleeding PR with Hb drop) is insufficient. Send AUTH-012 requesting: history of any prior GI conditions, previous prescriptions/medications for GI complaints, results of calprotectin/stool tests/FOB, duration and exact nature of symptoms, any previous colonoscopy reports. A 38-year-old with non-specific symptoms for 1 month should have conservative management and baseline labs first."
        },
        {
            "id": 10, "title": "Internal Audit — DRG Upcoding",
            "scenario": """
**Audit finding:** Retrospective review of 50 paid IP claims from Hospital X shows:
- 85% of claims have MCC (Major Complication/Comorbidity) codes
- Peer benchmark for similar hospital: 35% MCC rate
- Medical records reviewed: several MCC diagnoses (e.g., malnutrition, pressure ulcer stage 3) found in billing codes but NOT documented in clinical notes
""",
            "options": ["No action needed — hospital may just have sicker patients", "Flag for provider education only", "Initiate formal provider audit — possible DRG upcoding/fraud", "Automatically recoup all claims with MCC"],
            "answer": 2,
            "explanation": "An MCC rate of 85% vs 35% benchmark is a major statistical outlier. Combined with MCC codes appearing in billing without supporting clinical documentation, this is a textbook DRG upcoding red flag. Initiate formal provider audit: (1) Pull complete medical records for 20% of MCC claims. (2) Verify each MCC diagnosis against clinical notes — is it documented, was it treated, does it meet coding criteria? (3) If confirmed upcoding: recoup overpaid DRG weight differential, issue findings report, consider referral to regulatory authority. Never automatically recoup all claims — audit must be individual and evidence-based."
        }
    ]

    if "case_answers" not in st.session_state:
        st.session_state.case_answers = {}

    case_num = st.selectbox("Select Case:", [f"Case {c['id']}: {c['title']}" for c in cases])
    case_idx = int(case_num.split(":")[0].replace("Case ", "")) - 1
    case = cases[case_idx]

    st.markdown(f"""
    <div class="glass-card">
      <div style="font-weight:700;font-size:1rem;margin-bottom:0.8rem;">
        📋 Case {case['id']}: {case['title']}
      </div>
    """, unsafe_allow_html=True)
    st.markdown(case["scenario"])
    st.markdown("</div>", unsafe_allow_html=True)

    choice = st.radio("Your decision:", case["options"], key=f"case_{case['id']}")
    chosen_idx = case["options"].index(choice)

    if st.button("Submit Decision", key=f"submit_{case['id']}"):
        st.session_state.case_answers[case['id']] = chosen_idx
        if chosen_idx == case["answer"]:
            st.markdown(f'<div class="success-box">✅ <strong>Correct!</strong><br/>{case["explanation"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="warning-box">❌ <strong>Incorrect.</strong> Correct answer: <strong>{case["options"][case["answer"]]}</strong><br/><br/>{case["explanation"]}</div>', unsafe_allow_html=True)

    correct = sum(1 for cid, ans in st.session_state.case_answers.items()
                  if ans == cases[cid-1]["answer"])
    st.markdown(f"""
    <div class="metric-card" style="margin-top:1rem;">
      <div class="metric-val" style="color:#22d3c5;">{correct}/{len(st.session_state.case_answers)}</div>
      <div class="metric-lbl">Cases Correct So Far</div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 11 — QUIZ
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "📝  Knowledge Quiz":
    st.session_state.progress["quiz"] = True
    st.markdown('<div class="section-title">Knowledge Quiz</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Test your understanding across all modules. 80% required to pass each section.</div>', unsafe_allow_html=True)

    all_questions = [
        {"q": "Under DHA regulations, what is the maximum number of years after which a pre-existing condition CANNOT be established?", "opts": ["3 years", "5 years", "7 years", "10 years"], "a": 1, "module": "Pre-existing"},
        {"q": "Which denial code is used when a service was already approved and performed recently, making a repeat not medically justified?", "opts": ["Auth-001", "DUPL-001", "MNEC-005", "NCOV-002"], "a": 2, "module": "Claims"},
        {"q": "An EBP member visits a specialist at a hospital at 11pm without a GP referral. The complaint is a routine follow-up for a chronic condition. What is the correct action?", "opts": ["Approve — it's after 10pm so hospital access is allowed", "Deny — specialist access requires GP referral regardless of time", "Approve if they have IP coverage at that facility and the consultation is with a GP", "Escalate to PIC"], "a": 2, "module": "Policy"},
        {"q": "HPV infection treatment: under which regulatory framework is it covered?", "opts": ["Both DHA and HAAD", "HAAD only", "DHA only — not an exclusion per updated DHA guidance", "Neither — STDs are universally excluded in UAE"], "a": 2, "module": "Exclusions"},
        {"q": "What does DRG stand for and what does it primarily determine?", "opts": ["Drug Reimbursement Group — medication payment", "Diagnosis Related Group — inpatient payment bundle", "Diagnostic Review Guide — outpatient necessity", "Document Review Guidelines — audit framework"], "a": 1, "module": "Coding"},
        {"q": "For an MRI spine request with no X-ray attached and 3 weeks of symptoms, the correct action is:", "opts": ["Approve — MRI is first-line for back pain", "Deny — patient not eligible", "Query AUTH-012: request X-ray and conservative management history", "Escalate to PIC"], "a": 2, "module": "Claims"},
        {"q": "Under HAAD regulations, which hepatitis types are covered?", "opts": ["Hepatitis A, B, and C all covered", "Hepatitis A only", "Hepatitis B and C only", "All excluded"], "a": 1, "module": "Exclusions"},
        {"q": "What is the maximum number of physiotherapy sessions per request for a standard (non-EBP) plan?", "opts": ["3", "5", "7", "10"], "a": 1, "module": "Specialty"},
        {"q": "CPT codes 97001, 97110, and 97140 are all associated with:", "opts": ["Cardiology procedures", "Physiotherapy and rehabilitation", "Radiology imaging", "Laboratory tests"], "a": 1, "module": "Coding"},
        {"q": "A TPA (Third Party Administrator) in UAE health insurance:", "opts": ["Holds the insurance risk and sets the premium", "Processes claims on behalf of the PIC but does not hold the risk", "Is the same as the insurance company (PIC)", "Only handles dental and optical claims"], "a": 1, "module": "Foundations"},
        {"q": "An UNPEC (Undeclared Pre-existing Condition) case for an Orient Insurance member should:", "opts": ["Be denied immediately with NCOV-002", "Be approved as there is a benefit of doubt", "Be escalated to Orient PIC before final denial", "Be escalated to MOH for regulatory review"], "a": 2, "module": "Pre-existing"},
        {"q": "The NT scan (Nuchal Translucency) is only covered between:", "opts": ["8–10 weeks gestation", "11–13 weeks gestation", "16–18 weeks gestation", "18–20 weeks gestation"], "a": 1, "module": "Specialty"},
        {"q": "Which of the following is a standard exclusion under BOTH DHA and HAAD?", "opts": ["Hepatitis C treatment", "Circumcision for newborns", "IVF and embryo transfer", "HPV infection treatment"], "a": 2, "module": "Exclusions"},
        {"q": "Upcoding in the context of DRG billing means:", "opts": ["Coding a less complex diagnosis to reduce payment", "Adding CC/MCC diagnosis codes without clinical documentation to increase DRG payment", "Failing to code secondary diagnoses", "Using outdated ICD-9 codes instead of ICD-10"], "a": 1, "module": "Audit"},
        {"q": "For a file audit (FA) ticket to be raised, which of these must be confirmed FIRST?", "opts": ["The claim must exceed AED 10,000", "The provider must have specified the exact onset date of the condition", "The member must have been enrolled for less than 1 year", "The PIC must pre-approve the audit"], "a": 1, "module": "Pre-existing"},
        {"q": "Under hazardous sports exclusion, DHA and HAAD differ how?", "opts": ["DHA excludes all sports; HAAD only excludes professional sports", "DHA only excludes professional sports; HAAD has a broader exclusion including recreational hazardous activities", "Both have identical hazardous sports exclusions", "Neither covers sports injuries"], "a": 1, "module": "Exclusions"},
        {"q": "Which coding system is used for diagnosis coding in both UAE and international insurance?", "opts": ["CPT", "HCPCS Level II", "ICD-10", "DRG"], "a": 2, "module": "Coding"},
        {"q": "Emergency treatment in UAE health insurance is covered up to:", "opts": ["The first AED 5,000 regardless of outcome", "The point of stabilisation, regardless of network", "24 hours of admission only", "Whatever is in the TOB sub-limit for emergency"], "a": 1, "module": "Inpatient"},
        {"q": "What is the standard waiting period for pre-existing and chronic conditions under an EBP policy?", "opts": ["3 months", "6 months", "12 months", "24 months"], "a": 1, "module": "Pre-existing"},
        {"q": "RAF score in HCC risk adjustment models is:", "opts": ["A quality score for healthcare providers", "A risk adjustment factor reflecting a member's predicted healthcare cost based on diagnoses", "A reimbursement formula for pharmacy claims", "A fraud detection algorithm"], "a": 1, "module": "Coding"},
    ]

    module_filter = st.selectbox("Filter by module:", ["All Modules", "Foundations", "Exclusions", "Claims", "Coding", "Pre-existing", "Specialty", "Inpatient", "Audit"])
    if module_filter != "All Modules":
        filtered_q = [q for q in all_questions if q["module"].lower() in module_filter.lower()]
    else:
        filtered_q = all_questions

    if "quiz_state" not in st.session_state:
        st.session_state.quiz_state = {"current": 0, "score": 0, "answers": {}, "started": False}

    if not st.session_state.quiz_state["started"]:
        st.markdown(f"""
        <div class="glass-card">
          <div style="font-weight:700;">Quiz: {module_filter}</div>
          <div style="color:#9aa3b8;margin-top:0.5rem;">{len(filtered_q)} questions | Pass mark: 80%</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Quiz", use_container_width=True):
            st.session_state.quiz_state = {"current": 0, "score": 0, "answers": {}, "started": True, "questions": filtered_q}
            st.rerun()
    else:
        qs = st.session_state.quiz_state.get("questions", filtered_q)
        idx = st.session_state.quiz_state["current"]

        if idx < len(qs):
            q = qs[idx]
            progress_pct = int(idx / len(qs) * 100)
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;font-size:0.8rem;color:#9aa3b8;margin-bottom:4px;">
              <span>Question {idx+1} of {len(qs)}</span>
              <span class="badge badge-blue">{q['module']}</span>
            </div>
            <div class="prog-bar-bg" style="margin-bottom:1.2rem;">
              <div class="prog-bar-fill" style="width:{progress_pct}%"></div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f'<div class="glass-card"><div style="font-size:1rem;font-weight:600;margin-bottom:1rem;">{q["q"]}</div></div>', unsafe_allow_html=True)
            answer = st.radio("Choose answer:", q["opts"], key=f"q_{idx}")

            if st.button("Next →", use_container_width=True):
                chosen = q["opts"].index(answer)
                st.session_state.quiz_state["answers"][idx] = chosen
                if chosen == q["a"]:
                    st.session_state.quiz_state["score"] += 1
                st.session_state.quiz_state["current"] += 1
                st.rerun()
        else:
            score = st.session_state.quiz_state["score"]
            total = len(qs)
            pct_score = int(score / total * 100)
            passed = pct_score >= 80
            color = "#34d399" if passed else "#ff6b6b"
            status = "PASSED ✅" if passed else "NEEDS REVIEW ❌"
            st.session_state.quiz_scores[module_filter] = pct_score

            st.markdown(f"""
            <div class="glass-card" style="text-align:center;padding:2rem;">
              <div style="font-size:3rem;font-weight:800;color:{color};">{pct_score}%</div>
              <div style="font-size:1.1rem;font-weight:600;color:{color};margin:0.5rem 0;">{status}</div>
              <div style="color:#9aa3b8;">{score} correct out of {total} questions</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("**Review — Questions & Correct Answers:**")
            for i, q in enumerate(qs):
                user_ans = st.session_state.quiz_state["answers"].get(i, -1)
                correct_ans = q["a"]
                icon = "✅" if user_ans == correct_ans else "❌"
                bg = "rgba(52,211,153,0.06)" if user_ans == correct_ans else "rgba(255,107,107,0.06)"
                st.markdown(f"""
                <div style="background:{bg};border:1px solid var(--border);border-radius:var(--radius-md);padding:0.8rem 1rem;margin-bottom:0.5rem;font-size:0.85rem;">
                  {icon} <strong>Q{i+1}:</strong> {q['q']}<br/>
                  <span style="color:#34d399;">✓ {q['opts'][correct_ans]}</span>
                  {f'<br/><span style="color:#ff6b6b;">✗ Your answer: {q["opts"][user_ans]}</span>' if user_ans != correct_ans and user_ans >= 0 else ''}
                </div>
                """, unsafe_allow_html=True)

            if st.button("Retake Quiz", use_container_width=True):
                st.session_state.quiz_state = {"current": 0, "score": 0, "answers": {}, "started": False}
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 12 — RESOURCES
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "📚  Resources":
    st.markdown('<div class="section-title">Resources</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Official references and glossary</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📖 Official References", "📚 Glossary"])

    with tab1:
        st.markdown("""
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.8rem;">Official Regulatory Sources</div>
          <table class="styled-table">
            <tr><th>Source</th><th>Topic</th><th>Link</th></tr>
            <tr><td>DHA — Dubai Health Authority</td><td>DHA health insurance regulations, exclusions, circulars</td><td><a href="https://www.dha.gov.ae" target="_blank" style="color:#4f9cf9;">dha.gov.ae</a></td></tr>
            <tr><td>DOH — Dept of Health Abu Dhabi</td><td>HAAD/DOH health insurance framework, SHCA, DAMAN</td><td><a href="https://www.doh.gov.ae" target="_blank" style="color:#4f9cf9;">doh.gov.ae</a></td></tr>
            <tr><td>MOH — Ministry of Health UAE</td><td>Federal health regulations, Northern Emirates framework</td><td><a href="https://www.mohap.gov.ae" target="_blank" style="color:#4f9cf9;">mohap.gov.ae</a></td></tr>
            <tr><td>CBUAE — Central Bank UAE</td><td>Insurance licensing, reinsurance, IA functions</td><td><a href="https://www.centralbank.ae" target="_blank" style="color:#4f9cf9;">centralbank.ae</a></td></tr>
            <tr><td>AMA — CPT Codes</td><td>CPT code lookup and coding guidelines</td><td><a href="https://www.ama-assn.org/practice-management/cpt" target="_blank" style="color:#4f9cf9;">ama-assn.org</a></td></tr>
            <tr><td>WHO — ICD-10 / ICD-11</td><td>International Classification of Diseases</td><td><a href="https://icd.who.int" target="_blank" style="color:#4f9cf9;">icd.who.int</a></td></tr>
            <tr><td>CMS — DRG grouper & HCPCS</td><td>DRG weights, HCPCS Level II, coding edits</td><td><a href="https://www.cms.gov/Medicare/Coding" target="_blank" style="color:#4f9cf9;">cms.gov</a></td></tr>
            <tr><td>DOH Shafafiya — Prices & Methodologies</td><td>Abu Dhabi prices, adjudication rules, coding and DRG-related methodologies</td><td><a href="https://www.doh.gov.ae/shafafiya/prices" target="_blank" style="color:#4f9cf9;">doh.gov.ae/shafafiya/prices</a></td></tr>
            <tr><td>DOH Coding Manual</td><td>Department of Health coding guidelines and standards</td><td><a href="https://www.doh.gov.ae/-/media/Feature/shafifya/standards/coding/DOH-Coding-Manual-CSv2021.ashx" target="_blank" style="color:#4f9cf9;">DOH coding manual</a></td></tr>
            <tr><td>CMS — MS-DRG Classifications & Software</td><td>Official MS-DRG reference software and relative-weight explanation</td><td><a href="https://www.cms.gov/medicare/payment/prospective-payment-systems/acute-inpatient-pps/ms-drg-classifications-and-software" target="_blank" style="color:#4f9cf9;">CMS MS-DRG</a></td></tr>
            <tr><td>ACR Appropriateness Criteria</td><td>Evidence-based imaging appropriateness reference library</td><td><a href="https://acsearch.acr.org/list" target="_blank" style="color:#4f9cf9;">acsearch.acr.org</a></td></tr>
            <tr><td>AAPC — CRC Certification</td><td>Risk adjustment coding, HCC, CRC credential</td><td><a href="https://www.aapc.com/certification/crc" target="_blank" style="color:#4f9cf9;">aapc.com</a></td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        glossary = [
            ("AED", "Arab Emirate Dirham — currency of UAE"),
            ("AAPC CRC", "Certified Risk Adjustment Coder — AAPC credential focused on HCC and risk adjustment coding"),
            ("CC/MCC", "Complication/Comorbidity and Major Complication/Comorbidity — ICD-10 secondary diagnoses that increase DRG payment weight"),
            ("CPT", "Current Procedural Terminology — AMA-maintained code set for medical procedures and services"),
            ("CBUAE", "Central Bank of the UAE — regulates insurance companies federally (absorbed IA in 2020)"),
            ("Co-pay", "Fixed amount paid by member per visit/service. E.g. AED 20 per GP visit."),
            ("DHA", "Dubai Health Authority — regulates health insurance in Dubai emirate"),
            ("DMAN / DAMAN", "Abu Dhabi National Health Insurance Company — administers HAAD/DOH health plans"),
            ("DOH", "Department of Health Abu Dhabi — successor to HAAD"),
            ("DRG", "Diagnosis Related Group — inpatient payment grouping system"),
            ("EBP", "Essential Benefits Plan — minimum mandatory DHA health coverage plan"),
            ("FA", "File Audit — deep review of member medical file to verify onset and UNPEC"),
            ("FWA", "Fraud, Waste and Abuse — improper billing or utilisation practices"),
            ("HAAD", "Health Authority Abu Dhabi — predecessor to DOH, rules still referred to as HAAD regulations"),
            ("HCC", "Hierarchical Condition Category — ICD-10 code groupings used in risk adjustment models"),
            ("HCPCS", "Healthcare Common Procedure Coding System — Level I = CPT, Level II = supplies/equipment codes"),
            ("ICD-10", "International Classification of Diseases 10th Revision — diagnosis coding standard"),
            ("IP", "Inpatient — admission to hospital for at least one overnight stay"),
            ("LoS", "Length of Stay — number of days in hospital"),
            ("MAF", "Medical Application Form — health declaration form for underwriting"),
            ("MCC", "Major Complication/Comorbidity — serious secondary diagnosis increasing DRG weight"),
            ("MCU", "Medical Clinical Unit — internal team managing complex case reviews"),
            ("MIU", "Medical Investigation Unit — handles file audit and UNPEC investigation"),
            ("MOH", "Ministry of Health and Prevention UAE — federal health authority"),
            ("OP", "Outpatient — medical services without hospital admission"),
            ("PA", "Prior Authorisation — pre-approval required before service"),
            ("PEC", "Pre-existing Condition — illness present before policy start date"),
            ("PIC", "Primary Insurance Company — the insurance company that issues the policy and holds the risk"),
            ("PMPM", "Per Member Per Month — insurance cost unit"),
            ("RAF", "Risk Adjustment Factor — score reflecting predicted healthcare costs based on diagnosis profile"),
            ("SLA", "Service Level Agreement — turnaround time standards for claim/PA processing"),
            ("SHCA", "Standard Health Coverage Agreement — Abu Dhabi minimum benefit framework"),
            ("TOB", "Table of Benefits — policy document listing coverage, exclusions, limits"),
            ("TPA", "Third Party Administrator — processes claims on behalf of insurer without holding the risk"),
            ("UNPEC", "Undeclared Pre-existing Condition — condition present before policy but not disclosed at enrollment"),
        ]
        search_gloss = st.text_input("Search glossary...", placeholder="e.g. DRG, PA, UNPEC...")
        filtered_gloss = [(k, v) for k, v in glossary if not search_gloss or search_gloss.lower() in k.lower() or search_gloss.lower() in v.lower()]
        gloss_rows = "".join(
            "<tr><td><strong>" + k + "</strong></td><td style=\'font-size:0.83rem;color:#9aa3b8;\'>" + v + "</td></tr>"
            for k, v in filtered_gloss
        )
        st.markdown(
            "<div class=\"glass-card\"><table class=\"styled-table\"><tr><th>Term</th><th>Definition</th></tr>"
            + gloss_rows + "</table></div>",
            unsafe_allow_html=True
        )

    # Certificate tab intentionally removed.

    st.markdown("""
    <div style="font-size:0.78rem;color:#5c6480;text-align:center;padding:1.5rem 0 0.5rem;">
      <strong style="color:#9aa3b8;">Legal Disclaimer:</strong> This application is an educational training tool created by Rana Musab Bin Tariq.
      All content is for learning purposes only and does not constitute medical, legal, or insurance advice.
      Coverage and clinical decisions must always be based on the member complete medical file, specific TOB, and applicable regulatory framework.
      No internal company documents, proprietary data, or confidential information are disclosed. Regulatory content is derived from publicly available
      DHA, HAAD/DOH, and MOH frameworks. The creator assumes no liability for decisions made based on content in this application.
    </div>
    """, unsafe_allow_html=True)

# 
# PAGE  PROCEDURES, DENTAL & VACCINES
# 
elif nav == "🩺  Procedures, Dental & Vaccines":
    st.session_state.progress["cases"] = True
    st.markdown('<div class="section-title">Procedures, Dental & Vaccines</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">First-line investigations  What to request when something isn\'t first-line  Dental terms & rules  UAE vaccination coverage  High-value escalation</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="disclaimer">
      These pathways are educational review prompts, not automatic approval or denial rules.
      The treating clinician's judgment, red flags, current official guidance, your TPA's internal protocol,
      and the member's specific TOB always take precedence. Verify live cases against current sources.
    </div>
    """, unsafe_allow_html=True)

    t1, t5, t2, t3, t4 = st.tabs(["🧪 First-Line & Procedures", "🧭 Common Indications", "🦷 Dental Rules", "💉 Vaccinations UAE", "📈 Escalation & High-Value"])

    #  TAB 1: FIRST LINE 
    with t1:
        st.markdown("""
        <div class="glass-card">
          <div class="card-title">What "First-Line" Means in Claims Adjudication</div>
          <p style="font-size:.87rem;color:#9aa3b8;line-height:1.7;">
            A <strong style="color:#f0f2f8;">first-line investigation</strong> is one that is clinically appropriate as the
            initial step in evaluating a condition  no prior tests or conservative management are required before approving it.
            A <strong style="color:#f0f2f8;">non-first-line investigation</strong> requires you to confirm that earlier,
            simpler steps have already been taken before the more advanced test is justified.
            This is the heart of medical necessity assessment.
          </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card">
          <div class="card-title"> Investigations That Are Always First-Line  No Prerequisites Needed</div>
          <p style="font-size:.84rem;color:#9aa3b8;margin-bottom:.8rem;">
            These can be approved based on clinical diagnosis alone  no prior imaging, no management history required:
          </p>
          <table class="styled-table">
            <tr><th>Investigation</th><th>Common Indications</th><th>Notes</th></tr>
            <tr><td><strong>X-Ray</strong></td><td>Orthopaedic pain, chest symptoms, fracture query, dental</td><td>First-line for almost all structural and chest assessments. No prerequisites.</td></tr>
            <tr><td><strong>ECG</strong></td><td>Chest pain, palpitations, pre-op, cardiac symptoms</td><td>Always first-line. Must be done before echo in most cardiac workups.</td></tr>
            <tr><td><strong>Ultrasound (most indications)</strong></td><td>Abdomen, pelvis, thyroid, varicose veins, TMJ, soft tissue masses</td><td>First-line for most soft-tissue and abdominal queries. Exception: UTI (urine test first).</td></tr>
            <tr><td><strong>Mammography (age 40)</strong></td><td>Breast lump, screening in symptomatic women 40</td><td>First-line modality for women 40 and above.</td></tr>
            <tr><td><strong>Breast Ultrasound (age &lt;40)</strong></td><td>Palpable breast lump in women under 40</td><td>First-line for under-40. Dense breast tissue makes mammogram less effective in this age group.</td></tr>
            <tr><td><strong>EEG</strong></td><td>Seizure, epilepsy workup</td><td>First-line for all seizure investigations. No prerequisites.</td></tr>
            <tr><td><strong>Nerve Conduction Study (NCS) / EMG</strong></td><td>Carpal tunnel syndrome, peripheral neuropathy, radiculopathy</td><td>First-line for nerve-related symptoms. No X-ray or physio required first.</td></tr>
            <tr><td><strong>Doppler (vascular)</strong></td><td>Deep vein thrombosis, peripheral arterial disease, varicose veins</td><td>First-line vascular assessment. No prerequisites.</td></tr>
            <tr><td><strong>TMT (Treadmill Test)</strong></td><td>Chest pain, ischaemic heart disease workup</td><td>First-line functional cardiac test. Required before echo in most non-emergency cardiac workups.</td></tr>
            <tr><td><strong>MCV / FBC (Full Blood Count)</strong></td><td>Anaemia, infection, general workup</td><td>First-line haematology. No prerequisites.</td></tr>
            <tr><td><strong>Physiotherapy</strong></td><td>Most musculoskeletal conditions</td><td>Considered first-line for MSK. Referral letter required. No imaging prerequisite for standard plans.</td></tr>
            <tr><td><strong>MRI  Multiple Sclerosis</strong></td><td>Clinical MS workup</td><td>MRI brain and spine is first-line in suspected MS. Neurologist referral confirms indication.</td></tr>
            <tr><td><strong>MRI  TMJ</strong></td><td>Temporomandibular joint disorder</td><td>MRI is first-line for TMJ. CT also acceptable for TMJ. X-ray can complement.</td></tr>
            <tr><td><strong>CT Brain  Head Trauma</strong></td><td>Fall with head injury, GCS change, focal neurology</td><td>CT brain is first-line for acute trauma (faster than MRI for detecting acute bleeds). Approve if documented fall/trauma.</td></tr>
            <tr><td><strong>USG Kidney / Urinary tract</strong></td><td>Kidney stones, hydronephrosis, renal colic</td><td>First-line for urinary tract. CT KUB is second-line to confirm stone size and location.</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card">
          <div class="card-title"> Non-First-Line Investigations  What to Request Before Approving</div>
          <table class="styled-table">
            <tr><th>Investigation</th><th>Condition</th><th>What Must Come First</th><th>Decision Logic</th></tr>
            <tr>
              <td><strong>MRI Spine / Joint</strong></td><td>Back pain, joint pain, orthopaedic</td>
              <td>X-ray + conservative management (physiotherapy, analgesics)</td>
              <td>
                <strong>A.</strong> X-ray attached + shows abnormality + no physio history ' <span style="color:#34d399;">Approve MRI</span><br/>
                <strong>B.</strong> X-ray attached + shows abnormality + physio done ' Request physio progress notes ' approve if physio insufficient<br/>
                <strong>C.</strong> X-ray attached + normal + no conservative management ' <span style="color:#ff6b6b;">Deny / request conservative management first</span><br/>
                <strong>D.</strong> No X-ray attached ' <span style="color:#fbbf24;">Query: request X-ray, conservative management history, initial investigations</span>
              </td>
            </tr>
            <tr>
              <td><strong>MRI Brain</strong></td><td>Headache, neurological symptoms</td>
              <td>Clinical neurological assessment; ENT, ophthalmology opinion for chronic headache</td>
              <td>
                Approve if: seizures (EEG done first), MS workup, focal neurological deficit, trauma with clinical signs.<br/>
                Query if: headache only, no neurological signs, no conservative management.<br/>
                Always ask: duration of symptoms, any neurological signs, preliminary investigations done, what condition is being ruled out.
              </td>
            </tr>
            <tr>
              <td><strong>MRI Brain  Seizures</strong></td><td>Epilepsy, first seizure</td>
              <td>EEG must be done first</td>
              <td>EEG is the first-line investigation for seizures. Once EEG is done and raises concern for structural cause, MRI brain is then justified.</td>
            </tr>
            <tr>
              <td><strong>MRI Breast</strong></td><td>Breast mass or abnormality</td>
              <td>Ultrasound (under 40) or Mammogram (40+) must come first</td>
              <td>MRI breast is only justified after primary modality shows an abnormality that needs further characterisation. Not a screening tool in standard insurance context.</td>
            </tr>
            <tr>
              <td><strong>MRI for Haemorrhoids</strong></td><td>Haemorrhoidal disease</td>
              <td>Clinical examination, basic investigations</td>
              <td>MRI is only justified to rule out malignancy in complicated or atypical presentations. Simple haemorrhoids do not warrant MRI.</td>
            </tr>
            <tr>
              <td><strong>Echocardiogram</strong></td><td>Chest pain, palpitations, cardiac workup</td>
              <td>ECG + TMT + cardiac enzymes (troponin)</td>
              <td>
                Echo is not first-line for non-specific chest pain.<br/>
                Approve only if: structural evidence on ECG, positive troponin, audible murmur, or confirmed cardiac structural diagnosis.<br/>
                Do not approve for chest pain with normal ECG and no enzymes.
              </td>
            </tr>
            <tr>
              <td><strong>CT PNS (Sinuses)</strong></td><td>Sinusitis, nasal symptoms</td>
              <td>X-ray PNS or nasal endoscopy must be done first</td>
              <td>CT is not first-line for sinus symptoms. X-ray or endoscopy first. If findings are inconclusive and CT is needed for surgical planning, then approve.</td>
            </tr>
            <tr>
              <td><strong>Colonoscopy</strong></td><td>GI symptoms, colorectal query</td>
              <td>Calprotectin / FOB / H. pylori test / stool analysis; conservative management documented</td>
              <td>
                Approve if: chronic GI history documented + baseline labs done, or emergency indication (PR bleeding with Hb drop).<br/>
                Always ask: onset and duration of symptoms, prior GI investigations, prior medications, any alarm symptoms (weight loss, rectal bleeding, family history colorectal cancer).
              </td>
            </tr>
            <tr>
              <td><strong>Upper GIT Endoscopy</strong></td><td>GERD, dyspepsia, epigastric pain</td>
              <td>48 weeks of conservative medical management (PPI therapy); H. pylori / urea breath test</td>
              <td>
                Approve if: failed conservative management documented, H. pylori positive, prior endoscopy history with progression, or emergency (haematemesis).<br/>
                Always ask: duration of symptoms, medications tried and duration, H. pylori test result, previous endoscopy reports.
              </td>
            </tr>
            <tr>
              <td><strong>Ultrasound  UTI</strong></td><td>Urinary tract infection</td>
              <td>Urine analysis / urine culture must be done first</td>
              <td>Ultrasound is not first-line for simple UTI. Urine analysis is the first step. Ultrasound is appropriate if there is suspected complication (abscess, structural anomaly, recurrent UTI).</td>
            </tr>
            <tr>
              <td><strong>Vitamin D Test</strong></td><td>Vitamin D deficiency screening</td>
              <td>Prior test result + supplementation history</td>
              <td>
                Not a routine first-line test for all members. Approve for high-risk groups (elderly, chronic malabsorption, veiled women, osteoporosis).<br/>
                For repeat: require supplementation history (36 months minimum) and minimum 12-month interval from last test.<br/>
                Deny if: no prior deficiency, no supplementation, or repeat within 12 months without clinical change.
              </td>
            </tr>
            <tr>
              <td><strong>DEXA Scan</strong></td><td>Osteoporosis</td>
              <td>X-ray showing osteopenia</td>
              <td>Approve if X-ray reports confirm osteopenia or bone loss. Deny if X-ray is normal or not attached. DEXA is a quantification tool  it requires prior clinical suspicion from imaging.</td>
            </tr>
            <tr>
              <td><strong>Liver Elastography (Fibroscan)</strong></td><td>Liver fibrosis, hepatic disease</td>
              <td>Liver function profile + ultrasound abdomen + viral hepatitis labs</td>
              <td>Not first-line. Requires: detailed medical history with management plan, LFTs, ultrasound abdomen, hepatitis viral serology (HBsAg, HCV Ab), future treatment plan.</td>
            </tr>
            <tr>
              <td><strong>Arthrocentesis</strong></td><td>Joint aspiration / injection</td>
              <td>X-ray of affected joint + MRI if available + conservative management history</td>
              <td>Not first-line. Must confirm joint pathology on imaging and document failed conservative management before proceeding to joint aspiration or injection.</td>
            </tr>
            <tr>
              <td><strong>Sclerotherapy</strong></td><td>Varicose veins</td>
              <td>Doppler scan of affected vessels + conservative management (compression stockings) documented</td>
              <td>Doppler confirms venous reflux and suitability for sclerotherapy. Conservative management (compression) must have been tried. Document indication clearly.</td>
            </tr>
            <tr>
              <td><strong>Photochemotherapy (PUVA/UVB)</strong></td><td>Skin conditions (psoriasis, vitiligo, eczema)</td>
              <td>Previous topical treatments tried and failed; duration of disease and prior management documented</td>
              <td>Ask for: duration of condition, all previous topical treatments tried, duration and response to each, current clinical severity. Phototherapy is typically a second or third-line option.</td>
            </tr>
            <tr>
              <td><strong>Ureteroscopy (URS)</strong></td><td>Kidney / ureteric stones</td>
              <td>Radiology confirmation (CT KUB) of stone size + urine analysis</td>
              <td>
                Stone &lt;0.5 cm ' Conservative management (hydration, analgesia, alpha-blockers) first.<br/>
                Stone 0.51 cm ' ESWL or URS if hydronephrosis or back-pressure present.<br/>
                Stone &gt;1 cm ' URS + ESWL appropriate. Confirm with radiology report + urine analysis (haematuria, infection).
              </td>
            </tr>
            <tr>
              <td><strong>Circumcision (DHA policies)</strong></td><td>Phimosis, recurrent balanitis, religious/ritual</td>
              <td>Age and medical indication determine coverage</td>
              <td>
                <strong>DHA:</strong> Age 02 years ' covered (newborn circumcision). Over 2 years ' medical necessity must be documented by surgeon (phimosis, recurrent infection).<br/>
                <strong>HAAD:</strong> Standard exclusion regardless of age and indication.<br/>
                Always check if the TOB has specific wording.
              </td>
            </tr>
            <tr>
              <td><strong>Dramatic Falls  Alcohol Query</strong></td><td>Injury following a fall</td>
              <td>Clarify circumstances of fall</td>
              <td>
                Always ask: When did the fall happen? Where? How did it happen?<br/>
                If there is any clinical indication or documentation that the member was under the influence of alcohol or substances at the time of the fall ' deny (alcohol/substance exclusion).<br/>
                If the doctor confirms the member was NOT intoxicated and the fall was accidental ' approve.
              </td>
            </tr>
            <tr>
              <td><strong>Audiometry</strong></td><td>Hearing assessment</td>
              <td>N/A  it is a standard exclusion</td>
              <td>Standard exclusion under DHA, HAAD, and Northern Emirates. Covered only if the TOB explicitly includes hearing tests or hearing aids as a benefit. Always check TOB first before denying.</td>
            </tr>
            <tr>
              <td><strong>Allergy Testing</strong></td><td>Allergic conditions</td>
              <td>N/A  standard exclusion for most</td>
              <td>Standard exclusion for most policies. Exception: allergy testing specifically to determine allergy to a medication being used in treatment may be approved. Some international plans cover it upon medical necessity  check TOB.</td>
            </tr>
            <tr>
              <td><strong>Keratoconus workup (Pentacam)</strong></td><td>Keratoconus / refractive error</td>
              <td>N/A  classified as refractive error</td>
              <td>Keratoconus investigations and management fall under refractive error correction  standard exclusion for outpatient. Only covered if TOB explicitly includes vision correction or keratoconus as a named benefit.</td>
            </tr>
            <tr>
              <td><strong>Deviated Nasal Septum (DNS)</strong></td><td>Nasal obstruction</td>
              <td>Depends on service type</td>
              <td>
                <strong>OP investigations</strong> (scans, X-rays for DNS) ' Covered under DHA and most standard plans.<br/>
                <strong>Septoplasty (surgical correction)</strong> ' Standard exclusion under most policies unless TOB specifically covers it. Always check TOB before approving surgical DNS correction.
              </td>
            </tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card">
          <div class="card-title">Preoperative & Infectious Disease Testing Rules</div>
          <table class="styled-table">
            <tr><th>Test</th><th>Indication</th><th>Coverage Rule</th></tr>
            <tr><td>COVID-19 PCR  Pre-operative</td><td>Before any elective surgery</td><td><strong>DHA policies only:</strong> covered as mandatory pre-op screening per DHA circular. Not covered for HAAD or Northern Emirates policies through insurance.</td></tr>
            <tr><td>Hepatitis B, C / HIV  Pre-op (non-dialysis)</td><td>Before elective surgery</td><td>Coverage varies by payer and TOB. Some plans include, many exclude. Always check TOB. Hepatitis A is not an exclusion unless TOB states otherwise.</td></tr>
            <tr><td>Hepatitis B, C / HIV  Pre-dialysis</td><td>Before starting haemodialysis</td><td>Generally covered for Mediclinic group. For other providers: check TOB. Hepatitis A not excluded.</td></tr>
            <tr><td>Cryo / Electro sessions (dermatology)</td><td>Skin lesion treatment</td><td>Cryotherapy: typically up to 2 sessions. Electrocautery: up to 5 sessions. Beyond this, query for clinical justification and progress.</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)


    #  TAB 1B: COMMON INDICATION REVIEW PROMPTS
    with t5:
        st.markdown("""
        <div class="glass-card">
          <div class="card-title">Common Indications — Educational Review Prompts</div>
          <div class="warning-box"><strong>Use as a learning checklist, not an automatic approval rule.</strong> The treating clinician's judgment, red flags, age, pregnancy status, comorbidities, official guidelines, the member's TOB and your current TPA protocol take precedence.</div>
          <table class="styled-table">
            <tr><th>Presentation</th><th>Common Initial Work-up Considerations</th><th>When a More Advanced Test May Need Review</th><th>Useful Notes to Request</th></tr>
            <tr><td><strong>Low-back pain</strong></td><td>Clinical assessment; consider conservative management when there are no red flags. Imaging choice depends on the scenario.</td><td>MRI may be appropriate for red flags, suspected serious pathology, or persistent/progressive symptoms when intervention is being considered.</td><td>Duration, neurological deficit, trauma, fever, cancer history, bladder/bowel symptoms, prior management and specialist plan.</td></tr>
            <tr><td><strong>Acute head injury</strong></td><td>Clinical assessment and red-flag review. CT is commonly used when acute intracranial injury is suspected.</td><td>MRI may be considered for selected neurological questions after initial assessment.</td><td>Mechanism, loss of consciousness, GCS, vomiting, anticoagulants, focal deficit and clinician rationale.</td></tr>
            <tr><td><strong>Headache</strong></td><td>History and neurological examination. Identify thunderclap onset, focal deficit, fever, pregnancy, cancer or other red flags.</td><td>Advanced imaging depends on red flags and suspected pathology; headache alone does not establish a single pathway.</td><td>Onset, pattern, severity, red flags, neurological findings, prior treatment and specialist assessment.</td></tr>
            <tr><td><strong>Breast lump or symptoms</strong></td><td>Clinical examination and age-appropriate breast imaging. Ultrasound and mammography can be complementary.</td><td>Additional imaging or biopsy depends on imaging findings and specialist recommendation.</td><td>Age, symptoms, examination, pregnancy/lactation status, prior imaging and family history.</td></tr>
            <tr><td><strong>Abdominal pain</strong></td><td>Clinical assessment, targeted labs and ultrasound where clinically appropriate.</td><td>CT or MRI depends on location, suspected diagnosis, severity, red flags and initial results.</td><td>Location, onset, fever, vomiting, pregnancy status, surgical history, labs and ultrasound findings.</td></tr>
            <tr><td><strong>Suspected renal colic</strong></td><td>Urinalysis, renal function and imaging selected by clinical context. Ultrasound may be useful; CT KUB is often considered when clarification is needed.</td><td>Advanced imaging depends on severity, uncertainty, obstruction, infection risk and local pathway.</td><td>Stone history, fever, renal function, urinalysis, hydronephrosis, pain severity and previous imaging.</td></tr>
            <tr><td><strong>Chest pain</strong></td><td>Urgent clinical triage, ECG and biomarkers as clinically indicated. Emergency pathways supersede routine authorisation logic.</td><td>Echo, stress testing, coronary imaging or CT pulmonary angiography depend on the suspected diagnosis.</td><td>Vital signs, ECG, troponin, risk factors, dyspnoea, hypoxia, D-dimer where relevant and physician impression.</td></tr>
            <tr><td><strong>Suspected DVT</strong></td><td>Clinical risk assessment and venous Doppler ultrasound when indicated.</td><td>Additional imaging depends on initial result and specialist assessment.</td><td>Laterality, swelling, pain, recent travel/surgery, pregnancy, cancer and prior thrombosis.</td></tr>
            <tr><td><strong>Dyspepsia or GERD symptoms</strong></td><td>Clinical assessment, medication history and testing strategy based on age, alarm symptoms and guideline context.</td><td>Upper endoscopy may be considered for alarm symptoms, bleeding, persistent symptoms or specialist plan.</td><td>Duration, weight loss, anaemia, bleeding, dysphagia, medications, H. pylori testing and prior treatment.</td></tr>
            <tr><td><strong>Lower-GI symptoms</strong></td><td>History, examination and targeted labs or stool tests based on symptoms.</td><td>Colonoscopy may be considered for bleeding, anaemia, alarm features, screening context or specialist indication.</td><td>Duration, rectal bleeding, weight loss, family history, Hb, stool tests and prior endoscopy.</td></tr>
            <tr><td><strong>Recurrent UTI</strong></td><td>Urinalysis and culture. Imaging is selected when recurrence, obstruction, stones or structural issues are suspected.</td><td>Ultrasound or further imaging depends on complexity and clinician rationale.</td><td>Culture results, recurrence pattern, fever, pregnancy, stone history and previous treatment.</td></tr>
            <tr><td><strong>Thyroid symptoms or nodule</strong></td><td>Clinical review, thyroid-function tests and ultrasound for a nodule where appropriate.</td><td>Further imaging or biopsy depends on ultrasound risk features and specialist recommendation.</td><td>TSH, examination, ultrasound category, compressive symptoms, family history and endocrinology plan.</td></tr>
            <tr><td><strong>Joint pain after injury</strong></td><td>Clinical assessment and plain radiography where fracture or structural injury is suspected.</td><td>MRI may be considered for persistent symptoms, suspected internal derangement or a specialist plan.</td><td>Mechanism, examination, X-ray result, duration, conservative care and orthopaedic assessment.</td></tr>
            <tr><td><strong>Hearing symptoms</strong></td><td>ENT review and audiology pathway as clinically indicated.</td><td>Coverage is TOB-dependent even when clinically indicated.</td><td>Laterality, duration, ENT findings, otoscopy and benefit wording.</td></tr>
            <tr><td><strong>Dental pain</strong></td><td>Dental examination and targeted dental radiography where indicated.</td><td>Coverage depends on dental benefit, exclusions, annual limit and network rules.</td><td>Dental benefit, emergency status, tooth number, diagnosis, treatment plan and cost.</td></tr>
          </table>
          <div class="source-note">For imaging decisions, use current clinical guidance and local protocols. A useful official reference library is the <a href="https://acsearch.acr.org/list" target="_blank">American College of Radiology Appropriateness Criteria</a>. These prompts intentionally avoid claiming that one pathway fits every patient.</div>
        </div>
        """, unsafe_allow_html=True)

    #  TAB 2: DENTAL 
    with t2:
        st.markdown("""
        <div class="glass-card">
          <div class="card-title">Dental Coverage  Adjudication Steps</div>
          <div class="timeline-item">
            <div class="timeline-dot" style="background:#4f9cf922;color:#4f9cf9;">1</div>
            <div><strong>Check dental benefit exists</strong>  Dental is a standard exclusion unless explicitly added in the TOB. Check custom fields for dental coverage flag and access level.</div>
          </div>
          <div class="timeline-item">
            <div class="timeline-dot" style="background:#22d3c522;color:#22d3c5;">2</div>
            <div><strong>Check dental network</strong>  Verify the requesting provider is in the dental network list. This is often a separate list from the main medical network. Open networks (no network check needed): Generali, Integra Global, Expacare.</div>
          </div>
          <div class="timeline-item">
            <div class="timeline-dot" style="background:#a78bfa22;color:#a78bfa;">3</div>
            <div><strong>Check dental sub-limit and balance</strong>  Dental has its own annual sub-limit (e.g. AED 3,000). Track separately from main medical limit. Some plans split into Class I / II / III sublimits (e.g. Integra Global).</div>
          </div>
          <div class="timeline-item">
            <div class="timeline-dot" style="background:#fbbf2422;color:#fbbf24;">4</div>
            <div><strong>Check tooth number</strong>  Tooth number must be documented and updated in the dental medical file for all dental approvals.</div>
          </div>
          <div class="timeline-item">
            <div class="timeline-dot" style="background:#34d39922;color:#34d399;">5</div>
            <div><strong>Approve within scope, deny out-of-scope</strong>  Basic dental: check-up, extraction, simple filling, scaling. Major dental: crown, RCT, bridge. Orthodontics: separate benefit. Cosmetic: excluded.</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card">
          <div class="card-title">Dental Terms Explained  What Each Service Actually Is</div>
          <table class="styled-table">
            <tr><th>Term</th><th>What It Is</th><th>Coverage Logic</th></tr>
            <tr><td><strong>Scaling & Polishing</strong></td><td>Professional cleaning of teeth to remove tartar (calculus) and surface stains. Does not involve drilling or filling.</td><td>Usually covered under basic dental. Some TOBs limit to once or twice per year. Check session limit in TOB.</td></tr>
            <tr><td><strong>Deep Scaling / Root Planing / Curettage</strong></td><td>Cleaning below the gumline to treat gum (periodontal) disease. More invasive than standard scaling.</td><td>Only covered if the TOB includes periodontal or gum treatment as a specific benefit. Standard scaling coverage does NOT automatically include deep scaling.</td></tr>
            <tr><td><strong>Composite Filling</strong></td><td>Tooth-coloured resin used to fill a cavity. Matches tooth appearance.</td><td>Covered if fillings are in TOB. Check if TOB specifies types: composite, amalgam, or glass ionomer  only cover what is listed.</td></tr>
            <tr><td><strong>Amalgam Filling</strong></td><td>Silver-coloured metal alloy filling. Durable, used in back teeth.</td><td>Same as composite  check TOB for which filling types are covered.</td></tr>
            <tr><td><strong>Sealant</strong></td><td>A thin protective coating applied to the chewing surfaces of back teeth to prevent cavities. Does NOT restore a damaged tooth.</td><td>Classified as <strong>preventive</strong> dental treatment  not a restorative filling. Not covered as an alternative to fillings. Only covered if TOB explicitly includes preventive dental.</td></tr>
            <tr><td><strong>Fluoride Treatment</strong></td><td>Application of fluoride to strengthen tooth enamel and prevent decay.</td><td>Generally not covered unless TOB specifies it. Some policies cover topical fluoride for children under a certain age (check TOB).</td></tr>
            <tr><td><strong>Root Canal Treatment (RCT)</strong></td><td>Removal of infected pulp from inside the tooth, followed by cleaning and sealing. Saves a tooth from extraction.</td><td>Covered if major dental or endodontic treatment is in TOB. Often must precede crown placement for the same tooth.</td></tr>
            <tr><td><strong>Crown</strong></td><td>A cap placed over a damaged tooth to restore shape, strength, and appearance.</td><td>Covered if TOB includes crown. If TOB says crown must be preceded by RCT, ask for X-ray confirming RCT was performed. If TOB does NOT specify this requirement, do not ask for RCT evidence.</td></tr>
            <tr><td><strong>Post & Core</strong></td><td>A metal post and core material placed inside the root canal to support a crown when the tooth structure is insufficient.</td><td>Covered only alongside a crown. If crown is covered, post & core is covered. If the provider requests post & core separately but crown was already done previously on the same tooth, it can still be covered.</td></tr>
            <tr><td><strong>Bridge</strong></td><td>A fixed dental prosthesis that replaces one or more missing teeth by anchoring to adjacent teeth (abutments).</td><td>Covered only if TOB explicitly includes bridgework or dental prosthesis. Crown coverage alone does NOT imply bridge coverage  these are separate benefits. No RCT prerequisite for bridges.</td></tr>
            <tr><td><strong>Pontic</strong></td><td>The artificial tooth in the middle of a bridge that fills the gap where the natural tooth was missing.</td><td>Covered as part of bridgework. If bridge is covered, the pontic is covered as a component.</td></tr>
            <tr><td><strong>Denture</strong></td><td>Removable replacement for missing teeth  full (complete) or partial.</td><td>Covered under dental prosthesis if TOB includes it. Check if partial vs full dentures are both included.</td></tr>
            <tr><td><strong>Dental Implant</strong></td><td>A titanium post surgically inserted into the jawbone to replace a missing tooth root. A crown is then placed on top.</td><td>High-cost item. Only covered if TOB explicitly lists implants. Most basic and standard plans exclude implants.</td></tr>
            <tr><td><strong>Orthodontic Treatment</strong></td><td>Braces, aligners, and related appliances to correct misaligned teeth and jaw positioning.</td><td>Separate benefit from general dental. Usually has its own age limit (e.g. under 17 or 18) and its own sub-limit. Request a treatment plan and itemised cost breakdown. CDT codes should be submitted per service.</td></tr>
            <tr><td><strong>Space Maintainer</strong></td><td>A dental appliance that holds space for a permanent tooth after a baby tooth is lost early.</td><td>Classified under orthodontics  only covered if orthodontic benefit is in TOB.</td></tr>
            <tr><td><strong>Retainer</strong></td><td>A removable or fixed appliance worn after braces are removed to keep teeth in their new position. Last stage of orthodontic treatment.</td><td>Covered under orthodontic benefit. It is part of the orthodontic treatment course, not a separate benefit.</td></tr>
            <tr><td><strong>Simple Extraction</strong></td><td>Removal of a visible, erupted tooth using forceps under local anaesthesia.</td><td>Generally covered under basic dental. Some policies cover simple extractions only and exclude surgical extractions  check TOB wording carefully.</td></tr>
            <tr><td><strong>Surgical Extraction</strong></td><td>Removal of a tooth that is impacted, broken, or requires cutting of gum/bone tissue (e.g. wisdom teeth).</td><td>More complex and expensive than simple extraction. Only covered if TOB includes surgical extractions. Do not approve if TOB specifies simple extractions only.</td></tr>
            <tr><td><strong>Inhalational Sedation (Nitrous Oxide)</strong></td><td>Gas sedation (laughing gas) used to relax an anxious patient during dental treatment. Patient remains conscious.</td><td>Typically covered for children up to 8 years of age. For older age groups, check TOB and assess medical necessity (severe dental anxiety, special needs).</td></tr>
            <tr><td><strong>General Anaesthesia (GA) for Dental</strong></td><td>Full general anaesthesia for dental procedures  typically for young children, complex cases, or severe dental phobia.</td><td>If TOB does not specify GA coverage: deny GA charges and approve only the dental services themselves. If TOB covers GA and the request includes room and board, it should be handled as an inpatient (IP) case by the IP team, not OP dental.</td></tr>
            <tr><td><strong>TMJ Treatment</strong></td><td>Treatment of the temporomandibular joint (jaw joint)  may include splints, physiotherapy, medication, or surgery.</td><td>MRI and CT are first-line investigations for TMJ. Ultrasound is also first-line for TMJ. Treatment coverage depends on TOB.</td></tr>
            <tr><td><strong>Incision & Drainage (I&D)</strong></td><td>Surgical drainage of a dental abscess.</td><td>Not routinely covered unless specifically listed in TOB. Check before approving.</td></tr>
            <tr><td><strong>Panoramic X-ray (OPG)</strong></td><td>A wide X-ray showing all teeth, jaws, and surrounding structures in one image.</td><td>Generally covered as a diagnostic tool for dental treatment planning. Required for orthodontic treatment assessment.</td></tr>
            <tr><td><strong>Temporary Filling / Temporary Crown</strong></td><td>Short-term restoration while a permanent solution is being prepared.</td><td>Covered if fillings or crowns are covered in the TOB. Temporary items are included under the same benefit as permanent ones.</td></tr>
            <tr><td><strong>CDT Code D8040 / D8080</strong></td><td>Orthodontic banding codes for comprehensive treatment.</td><td>For large orthodontic packages, request itemised breakdown. Each service should be submitted using its specific CDT code rather than a single package code.</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box">
          <strong>UAE Dental Regulatory Context:</strong> There is no single UAE-wide standard for dental insurance coverage.
          DHA and HAAD regulations cover medical insurance  dental is treated as an add-on benefit.
          The extent of dental coverage is entirely defined by the TOB. The only universal rule is that
          <strong>dental prostheses and orthodontic treatment are excluded from the basic mandatory plan</strong>
          under both DHA (GC 03/2024) and HAAD standard health insurance regulations.
          Everything beyond the basic exclusion is a contractual matter between the insurer and the employer.
        </div>
        """, unsafe_allow_html=True)

    #  TAB 3: VACCINATIONS 
    with t3:
        st.markdown("""
        <div class="glass-card">
          <div class="card-title">Vaccination Coverage  UAE Health Insurance Framework</div>
          <div class="warning-box">
            <strong>Default position:</strong> Vaccinations are a <strong>standard exclusion</strong> under the basic mandatory plans
            of both DHA and HAAD, and under Northern Emirates standard policies.
            They are classified as preventive services, which are excluded from the minimum benefit package.
            Coverage is only available if the TOB <strong>explicitly</strong> adds a vaccination benefit.
          </div>
          <table class="styled-table">
            <tr><th>Regulatory Framework</th><th>Vaccination Coverage Rule</th></tr>
            <tr>
              <td><strong>DHA  Dubai Basic / EBP</strong></td>
              <td>Vaccinations excluded as preventive services. Not part of the Essential Benefits Plan (EBP) minimum standard per DHA GC 03/2024. Enhanced plans may add vaccination benefit  check TOB.</td>
            </tr>
            <tr>
              <td><strong>HAAD / DOH  Abu Dhabi</strong></td>
              <td>Vaccinations excluded under Clause 23 of HAAD standard exclusions: "Preventive services, including vaccinations, immunizations, allergy testing and desensitization." Enhanced corporate plans may add it  always check TOB.</td>
            </tr>
            <tr>
              <td><strong>Northern Emirates (MOH)</strong></td>
              <td>Vaccinations excluded as preventive treatment under standard policy wording. "Vaccinations or inoculations" are listed explicitly in standard Northern Emirates exclusion clauses.</td>
            </tr>
            <tr>
              <td><strong>UAE National Immunisation Programme (NIP)</strong></td>
              <td>Mandatory childhood vaccinations (BCG, Hepatitis B, DTP, Polio, MMR, Varicella, etc.) are provided FREE at government primary healthcare centres (PHCs) for all UAE residents  regardless of insurance status. This is a government-funded programme, not an insurance benefit.</td>
            </tr>
            <tr>
              <td><strong>Employer / Corporate Plans (Enhanced)</strong></td>
              <td>Many corporate group plans (Standard and above) add a vaccination benefit in the TOB. Common inclusions: flu vaccine (annual), travel vaccines, Hepatitis A/B vaccine courses. Check TOB for specific vaccines covered and any age limits.</td>
            </tr>
            <tr>
              <td><strong>COVID-19 Vaccine</strong></td>
              <td>COVID-19 vaccination is excluded from health insurance under all regulatory frameworks  it was provided as a national programme. Complications arising directly from the COVID-19 vaccine are also not covered as a standard position (the vaccine is excluded, so complications follow). Check any updated TOB or specific PIC position on this.</td>
            </tr>
            <tr>
              <td><strong>Travel Vaccines</strong></td>
              <td>Not covered under any standard plan. Classified as preventive/travel-related care. Some premium/international plans add travel vaccination as a specific benefit  rare and always TOB-dependent.</td>
            </tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card">
          <div class="card-title">When Vaccinations May Be Covered  Common Scenarios</div>
          <table class="styled-table">
            <tr><th>Scenario</th><th>Coverage Position</th><th>What to Check</th></tr>
            <tr><td>Annual influenza vaccine requested via network clinic</td><td>Covered only if TOB includes vaccination benefit. Many enhanced corporate plans do include flu vaccine.</td><td>Check TOB for "vaccination benefit" or "preventive care" section. Check if specific vaccine is listed.</td></tr>
            <tr><td>Hepatitis B vaccine course (3 doses)</td><td>Excluded under standard plans. Some enhanced plans cover Hep B vaccine course as occupational health requirement (healthcare workers).</td><td>Check TOB. If healthcare worker, some PICs may make an exception  escalate to PIC if in doubt.</td></tr>
            <tr><td>HPV vaccine</td><td>Not covered under standard plans as a vaccination. Under DHA, HPV as an <em>infection requiring treatment</em> may be covered  but the preventive vaccine itself is not.</td><td>Distinguish between HPV vaccine (preventive = excluded) and treatment of active HPV infection (clinical = may be covered under DHA).</td></tr>
            <tr><td>Futtaim / Mediclinic group members requesting vaccination</td><td>Al Futtaim group employees can access HealthHub providers for vaccination requests. Mediclinic group members access Mediclinic providers. Network access rules still apply.</td><td>Verify network access. Check if vaccination benefit is in TOB for these specific groups.</td></tr>
            <tr><td>Child vaccination at clinic  standard EBP member</td><td>Not covered through insurance. Direct member to nearest government PHC for NIP vaccinations, which are free of charge.</td><td>No insurance claim needed. Government PHCs provide NIP vaccines free to all UAE residents regardless of nationality.</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box">
          <strong>UAE National Immunisation Programme (NIP)  Quick Reference:</strong><br/>
          The UAE Ministry of Health and Prevention operates a comprehensive free vaccination programme at all government PHCs.
          This covers: BCG, Hepatitis B (birth + course), DTP (Diphtheria/Tetanus/Pertussis), IPV (Polio), Hib,
          Pneumococcal, Rotavirus, MMR (Measles/Mumps/Rubella), Varicella, and meningococcal vaccines for children.
          Annual influenza vaccine is available free at PHCs during flu season.
          <strong>Insurance is not required and not used for NIP vaccinations.</strong>
          Source: MOHAP UAE National Immunisation Schedule.
        </div>
        """, unsafe_allow_html=True)

    #  TAB 4: ESCALATION & HIGH VALUE 
    with t4:
        st.markdown("""
        <div class="glass-card">
          <div class="card-title">When to Escalate  The General Principle</div>
          <p style="font-size:.87rem;color:#9aa3b8;line-height:1.7;">
            As a TPA adjudicator, you have authority to approve and deny within defined limits.
            Escalation means sending the case to your Team Leader (TL), the Primary Insurance Company (PIC),
            or the Medical Investigation Unit (MIU) before you make a final decision.
            Escalating when you should not wastes time. Not escalating when you should = a compliance breach.
          </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card">
          <div class="card-title">Escalation Triggers  When You Must Escalate</div>
          <table class="styled-table">
            <tr><th>Trigger</th><th>Escalate To</th><th>Why</th></tr>
            <tr>
              <td><strong>Cost exceeds payer escalation threshold</strong></td>
              <td>PIC (Primary Insurance Company)</td>
              <td>Each payer has a defined AED threshold above which all approvals require PIC written authorisation before the TPA can approve. This protects the PIC from large unexpected liabilities. Thresholds vary by payer  check your TPA's payer escalation matrix.</td>
            </tr>
            <tr>
              <td><strong>Undeclared Pre-existing Condition (UNPEC) suspected</strong></td>
              <td>PIC (for designated payers) or MIU</td>
              <td>Certain PICs (e.g. Orient, AIAW, Watania, Generali/GGH, Salama) require the TPA to obtain their written authorisation before issuing a denial for UNPEC. Denying without escalation for these payers = process violation.</td>
            </tr>
            <tr>
              <td><strong>File Audit required</strong></td>
              <td>MIU (Medical Investigation Unit)</td>
              <td>When UNPEC is suspected, onset is documented, and case meets FA threshold. Raise FA ticket with all reports to MIU for deep investigation.</td>
            </tr>
            <tr>
              <td><strong>Grey-zone medical necessity</strong></td>
              <td>Team Leader (TL) / Senior Medical Reviewer</td>
              <td>Cases where clinical justification is borderline  not clearly approvable or deniable. Discuss with TL before deciding. Document the discussion.</td>
            </tr>
            <tr>
              <td><strong>Work-related injury (Enhanced plan)</strong></td>
              <td>PIC  notify by email immediately</td>
              <td>For non-EBP plans with WRI covered: approve and notify the PIC immediately by email, asking for details of their Workmen's Compensation Policy coverage. This allows the PIC to subrogate against the employer's WCP.</td>
            </tr>
            <tr>
              <td><strong>Suspected fraud or billing irregularity</strong></td>
              <td>Compliance / TL / PIC</td>
              <td>If you identify phantom billing, upcoding, or provider-member collusion  do not proceed. Flag to your TL and compliance team immediately. Document everything before taking any action.</td>
            </tr>
            <tr>
              <td><strong>Case under internal discussion / pending PIC response</strong></td>
              <td>PIC</td>
              <td>Use AUTH-012 internal discussion template: "Please note that the case is currently under internal discussion and assessment and final decision will be conveyed shortly." Update the provider while the escalation is being resolved.</td>
            </tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card">
          <div class="card-title">High-Value Claims  General Thresholds and Process</div>
          <div class="info-box">
            <strong>Important:</strong> Exact escalation thresholds are set by each PIC and are confidential to your TPA contract.
            The values below are illustrative of the types of thresholds that exist  your TPA will have its own
            payer escalation matrix which is the authoritative reference. Always use your internal matrix.
          </div>
          <table class="styled-table">
            <tr><th>Claim Value Category</th><th>Typical Action</th></tr>
            <tr><td>Below internal TPA approval limit</td><td>TPA medical reviewer approves or denies independently within their authority.</td></tr>
            <tr><td>Above TPA authority limit  below PIC threshold</td><td>Escalate to TL for approval. TL signs off before authorisation is issued to provider.</td></tr>
            <tr><td>Above PIC escalation threshold</td><td>Email sent to PIC with full clinical summary, all reports, and cost breakdown. Await PIC written approval. Do NOT authorise until PIC responds. Use the standard escalation email template with member details, payer, group, underwriting status, diagnosis, estimated cost, and TPA recommendation.</td></tr>
            <tr><td>File audit cases (suspected UNPEC &gt; AED 4,0005,000)</td><td>Raise FA ticket to MIU even below PIC threshold if UNPEC is suspected. Approve initial diagnostics while FA is pending.</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card">
          <div class="card-title">Escalation Email  What to Include</div>
          <p style="font-size:.84rem;color:#9aa3b8;margin-bottom:.8rem;">When escalating a high-value case or UNPEC case to PIC, your email must include:</p>
          <table class="styled-table">
            <tr><th>Field</th><th>Detail Required</th></tr>
            <tr><td>Member name</td><td>Full name as per policy</td></tr>
            <tr><td>Member card number</td><td>Policy card / ID number</td></tr>
            <tr><td>Payer (PIC)</td><td>Insurance company name</td></tr>
            <tr><td>Group / employer</td><td>Employer or group name</td></tr>
            <tr><td>Underwriting status</td><td>Is the member subject to underwriting? MAF attached? Any declared conditions?</td></tr>
            <tr><td>Enrollment / effective date</td><td>When did the member join? Policy start and expiry date.</td></tr>
            <tr><td>Provider name</td><td>Hospital or clinic requesting the service</td></tr>
            <tr><td>Case summary</td><td>Brief clinical summary  diagnosis, requested service, clinical justification</td></tr>
            <tr><td>Diagnosis (ICD-10)</td><td>Diagnosis code and description</td></tr>
            <tr><td>Estimated cost</td><td>Total estimated cost of requested service(s)</td></tr>
            <tr><td>TPA recommendation</td><td>Your medical opinion  approve, deny, or undecided with reason</td></tr>
            <tr><td>Attachments</td><td>All clinical reports received, prior approval history, investigation results</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)
