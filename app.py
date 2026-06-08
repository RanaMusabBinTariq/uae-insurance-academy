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
        "quiz": False, "resources": False, "procedures": False
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
- The material focuses on general learning principles. Where policy wording or local rules differ, the current official source and the member-specific TOB take precedence.
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
        ("📋", "Claims Processing", "OP/IP workflow, review outcomes and prior authorisation", "claims", "claims"),
        ("🔢", "Medical Coding", "CPT, ICD-10, HCPCS, DRG and HCC concepts", "coding", "coding"),
        ("🔍", "Pre-existing Conditions", "Declarations, evidence review and policy wording", "preex", "preex"),
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
              <td>Mandatory coverage since 2006. Thiqa and the Abu Dhabi Basic Product operate within the DOH framework. Always verify the current official product rules.</td>
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
              <td><span class="badge badge-amber">Near-EBP / Budget Basic</span></td>
              <td>Near-EBP plans</td>
              <td>Small employers, budget groups</td>
              <td>Restricted-network products may have narrower provider access and additional referral or authorisation requirements. Always check the member-specific TOB, network and current product rules.</td>
            </tr>
            <tr>
              <td><span class="badge badge-blue">Standard / Enhanced</span></td>
              <td>Corporate group plans</td>
              <td>Mid-size companies, professionals</td>
              <td>Broader-network products may add dental, optical, maternity or rehabilitation benefits. Referral, authorisation and physiotherapy limits remain member-specific and must be checked in the TOB.</td>
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
            <tr><td><span class="badge badge-cyan">Thiqa</span></td><td>Eligible UAE nationals in Abu Dhabi</td><td>Government-supported programme. Always verify the current eligibility and benefit rules through the official Abu Dhabi framework.</td></tr>
            <tr><td><span class="badge badge-blue">Basic Product</span></td><td>Eligible Abu Dhabi residents</td><td>Mandatory minimum product under the Abu Dhabi health insurance framework. Confirm the current benefit schedule and tariff rules.</td></tr>
            <tr><td><span class="badge badge-violet">Enhanced Product</span></td><td>Members with upgraded benefits</td><td>May extend the Basic Product. Always adjudicate against the member-specific TOB and network.</td></tr>
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
              <td>Licensed UAE insurers and authorised health insurance companies</td>
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
            <tr><td><strong>UAE Example</strong></td><td>A licensed insurer sells a group health policy to an employer.</td><td>The insurer may transfer part of its risk to a reinsurer under a separate contract. This does not alter the member's stated TOB.</td></tr>
            <tr><td><strong>Member awareness</strong></td><td>Member has a policy card, TOB, network list</td><td>Member is unaware of reinsurance arrangement — no impact on their benefits</td></tr>
          </table>
        </div>
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:0.6rem;">🔑 Key Terms for Day-One Work</div>
          <table class="styled-table">
            <tr><th>Term</th><th>Meaning</th></tr>
            <tr><td>TOB</td><td>Table of Benefits — the master document listing covered and excluded services, limits, co-pays, networks</td></tr>
            <tr><td>MAF</td><td>Medical Application Form — used where applicable for underwriting and declarations</td></tr>
            <tr><td>Declaration Form</td><td>Lists pre-existing conditions declared by the member at enrollment</td></tr>
            <tr><td>Prior Authorization (PA)</td><td>Pre-approval required before a service is rendered — most elective procedures, specialist referrals, high-cost diagnostics</td></tr>
            <tr><td>Co-pay / Deductible</td><td>Member's share of cost. Co-pay = fixed amount per visit. Deductible = amount member pays before insurance kicks in.</td></tr>
            <tr><td>Sub-limit</td><td>A cap within the annual limit for a specific category. Dental, optical, maternity, rehabilitation, and pharmacy limits must be read from the member-specific TOB.</td></tr>
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
            <tr><td><strong>COVID testing</strong></td><td>Apply the current DHA circulars and the member-specific TOB.</td><td>Apply the current DOH circulars and funded-programme rules where relevant.</td></tr>
            <tr><td><strong>HIV/AIDS</strong></td><td>Check the current Dubai basic-plan exclusions and the member-specific TOB.</td><td>Check the current Abu Dhabi Basic Product exclusions and any applicable enhanced-product extension.</td></tr>
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
    st.markdown('<div class="section-sub">Prior authorisation, eligibility checks, medical-necessity review, and clear decision documentation</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🔄 Workflow", "🧾 Review Outcomes", "🧠 Imaging Review", "📋 Procedure Review"])

    with tab1:
        st.markdown("""
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:1rem;">Prior Authorisation (PA) — Practical Review Flow</div>
          <div class="timeline-item"><div class="timeline-dot" style="background:rgba(79,156,249,0.2);color:#4f9cf9;">1</div><div><strong>Confirm the request</strong> — Member identifier, provider, diagnosis, requested service, code, clinical notes, date and cost estimate.</div></div>
          <div class="timeline-item"><div class="timeline-dot" style="background:rgba(34,211,197,0.2);color:#22d3c5;">2</div><div><strong>Check eligibility and benefit</strong> — Active membership, network, TOB wording, limits, exclusions, waiting periods and any referral requirement.</div></div>
          <div class="timeline-item"><div class="timeline-dot" style="background:rgba(167,139,250,0.2);color:#a78bfa;">3</div><div><strong>Review medical necessity</strong> — Clinical indication, red flags, prior assessment, relevant results, treatment plan and whether the requested setting is appropriate.</div></div>
          <div class="timeline-item"><div class="timeline-dot" style="background:rgba(251,191,36,0.2);color:#fbbf24;">4</div><div><strong>Choose a clear outcome</strong> — Approve, request specific missing information, redirect to the applicable benefit route, or decline with a documented reason linked to the TOB or evidence reviewed.</div></div>
          <div class="timeline-item"><div class="timeline-dot" style="background:rgba(52,211,153,0.2);color:#34d399;">5</div><div><strong>Record the decision trail</strong> — Evidence reviewed, rationale, reference number, approved scope where applicable, and any follow-up requirement.</div></div>
        </div>
        <div class="glass-card">
          <div style="font-weight:700;margin-bottom:.8rem;">Services Commonly Checked for Prior Authorisation</div>
          <table class="styled-table">
            <tr><th>Category</th><th>General Review Approach</th><th>Key Checks</th></tr>
            <tr><td>Elective inpatient admission</td><td>Usually reviewed before admission.</td><td>Admission necessity, setting, diagnosis, proposed treatment, expected length of stay, network and benefit.</td></tr>
            <tr><td>Day surgery and elective procedures</td><td>Often require benefit and medical-necessity review.</td><td>Procedure code, indication, relevant results, alternatives, provider eligibility and TOB.</td></tr>
            <tr><td>Advanced imaging</td><td>Review is indication-specific; avoid blanket rules.</td><td>Clinical question, red flags, prior assessment, relevant first-line tests and guideline context.</td></tr>
            <tr><td>Physiotherapy and rehabilitation</td><td>Requirements vary by product and regulator framework.</td><td>Assessment, functional goals, treatment plan, milestones, progress documentation, referral route and benefit balance.</td></tr>
            <tr><td>Emergency care</td><td>Treat immediate clinical risk first; administrative review follows the applicable framework.</td><td>Emergency presentation, stabilisation needs, network status, notification requirements and ongoing-care plan.</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        outcomes = [
            ("Approve", "badge-green", "The request is eligible, covered and supported by the documentation reviewed.", "Record the approved scope and reference."),
            ("Request information", "badge-blue", "The request may be appropriate but the evidence is incomplete.", "Ask only for the missing items: symptom duration, examination findings, results, prior treatment, operative plan or progress note."),
            ("Benefit or network clarification", "badge-amber", "The service route depends on the member-specific plan.", "Confirm TOB, network, referral pathway, reimbursement route, limits and co-pay."),
            ("Duplicate or frequency review", "badge-amber", "A recent similar service or claim needs comparison.", "Check dates, provider, code, clinical change and previous authorisation."),
            ("Medical-necessity concern", "badge-coral", "The submitted evidence does not currently support the requested service or setting.", "State the clinical gap clearly and identify what evidence was reviewed."),
            ("Coverage exclusion", "badge-coral", "The service or condition appears excluded under the applicable wording.", "Quote the relevant TOB or regulatory source and check whether an enhanced benefit applies."),
            ("Coding or submission correction", "badge-violet", "The request cannot be processed accurately as submitted.", "Identify the incorrect or missing field, code, cost, date or document."),
        ]
        rows = "".join(
            '<tr><td><span class="badge ' + badge + '">' + label + '</span></td><td>' + meaning + '</td><td>' + action + '</td></tr>'
            for label, badge, meaning, action in outcomes
        )
        st.markdown(
            '<div class="glass-card"><div style="font-weight:700;margin-bottom:.8rem;">Common Review Outcomes</div>'
            '<p style="font-size:.86rem;color:#9aa3b8;">Use the terminology configured in the live claims platform. The categories below are learning concepts; labels may differ between systems.</p>'
            '<table class="styled-table"><tr><th>Outcome</th><th>When It Fits</th><th>Documentation Focus</th></tr>' + rows + '</table></div>',
            unsafe_allow_html=True
        )

    with tab3:
        st.markdown('<div style="font-weight:700;margin-bottom:1rem;">🧠 Imaging Review Prompts</div>', unsafe_allow_html=True)
        body_part = st.selectbox("Select review area:", ["Spine / musculoskeletal", "Brain / neurological", "Breast", "Abdomen / pelvis"])
        if body_part == "Spine / musculoskeletal":
            st.markdown("""<div class="glass-card"><div class="card-title">Spine and Musculoskeletal Imaging</div>
            <div class="info-box">The imaging pathway depends on the clinical scenario. Do not require the same prerequisite for every request.</div>
            <table class="styled-table"><tr><th>Question</th><th>What to Review</th></tr>
            <tr><td>Are red flags present?</td><td>Trauma, progressive neurological deficit, suspected infection, malignancy, cauda-equina symptoms or another urgent concern.</td></tr>
            <tr><td>What is the clinical question?</td><td>Clarify whether imaging is intended to assess fracture, neurological compression, inflammatory disease, structural pathology or persistent symptoms.</td></tr>
            <tr><td>What has already been assessed?</td><td>Examination findings, duration, relevant prior imaging, treatment tried and response where appropriate.</td></tr>
            <tr><td>Does the requested modality fit?</td><td>Use current appropriateness guidance and the treating clinician's documented rationale.</td></tr></table></div>""", unsafe_allow_html=True)
        elif body_part == "Brain / neurological":
            st.markdown("""<div class="glass-card"><div class="card-title">Brain and Neurological Imaging</div>
            <table class="styled-table"><tr><th>Question</th><th>What to Review</th></tr>
            <tr><td>Is this an emergency presentation?</td><td>Acute trauma, altered consciousness, focal deficit, sudden severe headache or other red flags may change the preferred modality and urgency.</td></tr>
            <tr><td>What condition is being assessed?</td><td>Seizure, demyelinating disease, stroke, tumour, infection, headache syndrome or another documented clinical concern.</td></tr>
            <tr><td>What evidence is available?</td><td>Neurological examination, symptom chronology, relevant specialist note and prior results where applicable.</td></tr></table></div>""", unsafe_allow_html=True)
        elif body_part == "Breast":
            st.markdown("""<div class="glass-card"><div class="card-title">Breast Imaging</div>
            <table class="styled-table"><tr><th>Review Area</th><th>What to Check</th></tr>
            <tr><td>Clinical context</td><td>Screening versus diagnostic request, age, symptoms, examination findings, personal risk and previous imaging.</td></tr>
            <tr><td>Modality selection</td><td>Mammography, ultrasound and MRI have different roles. Confirm the documented indication and use current breast-imaging guidance.</td></tr>
            <tr><td>Prior findings</td><td>Review prior mammography, ultrasound, pathology or specialist recommendation where relevant.</td></tr></table></div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div class="glass-card"><div class="card-title">Abdominal and Pelvic Imaging</div>
            <table class="styled-table"><tr><th>Question</th><th>What to Review</th></tr>
            <tr><td>What organ system is involved?</td><td>Hepatobiliary, renal, gastrointestinal, pelvic, vascular or another documented concern.</td></tr>
            <tr><td>What has already been done?</td><td>Clinical assessment, laboratory tests and any relevant ultrasound, CT or prior specialist review.</td></tr>
            <tr><td>Why this modality now?</td><td>Confirm how the requested scan is expected to answer the clinical question or change management.</td></tr></table></div>""", unsafe_allow_html=True)
        st.markdown('<div class="source-note">For imaging decisions, use the current clinical guideline applicable to the scenario. The <a href="https://www.acr.org/Clinical-Resources/ACR-Appropriateness-Criteria" target="_blank">ACR Appropriateness Criteria</a> are a useful reference library.</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown("""
        <div class="glass-card">
          <div class="card-title">Procedure Review Checklist</div>
          <table class="styled-table">
            <tr><th>Review Area</th><th>Questions to Ask</th></tr>
            <tr><td>Eligibility and benefit</td><td>Is the member active? Is the service covered? Is a limit, co-pay, waiting period, network rule or referral pathway relevant?</td></tr>
            <tr><td>Clinical indication</td><td>What diagnosis, symptoms, duration, examination findings and red flags support the request?</td></tr>
            <tr><td>Evidence and prior care</td><td>Which relevant tests, treatment attempts, specialist opinions or progress notes are available?</td></tr>
            <tr><td>Setting</td><td>Is the proposed outpatient, day-case or inpatient setting clinically appropriate?</td></tr>
            <tr><td>Coding and documentation</td><td>Do the diagnosis, procedure code, units, dates, site and clinical note align?</td></tr>
            <tr><td>Decision trail</td><td>Can another reviewer understand what was reviewed and why the outcome was reached?</td></tr>
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
            <tr><td>97161–97163</td><td>PT evaluation</td><td>Complexity-based</td><td>Use the evaluation level supported by the documented history, examination, clinical decision-making and applicable coding standard.</td></tr>
            <tr><td>97164</td><td>PT re-evaluation</td><td>Per encounter</td><td>Use when a clinically supported reassessment is required; do not bill automatically at each follow-up.</td></tr>
            <tr><td>97110</td><td>Therapeutic exercises</td><td>Per 15 min</td><td>Document the exercise-based intervention, duration and treatment goal.</td></tr>
            <tr><td>97140</td><td>Manual therapy techniques</td><td>Per 15 min</td><td>Use only when clinically documented and supported by the applicable coding standard and tariff.</td></tr>
            <tr><td>97530</td><td>Therapeutic activities</td><td>Per 15 min</td><td>Document the functional activity, duration and patient-specific goal.</td></tr>
            <tr><td>97035</td><td>Ultrasound therapy</td><td>Per 15 min</td><td>Use only when supported by the treatment plan and applicable coding guidance.</td></tr>
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
    st.markdown('<div class="section-sub">Declarations, evidence review, waiting periods, and careful documentation</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📖 Core Concepts", "🔬 Evidence Review", "📂 Case Documentation"])

    with tab1:
        st.markdown("""
        <div class="glass-card">
          <div class="card-title">Core Concepts</div>
          <table class="styled-table">
            <tr><th>Term</th><th>Learning Definition</th></tr>
            <tr><td><strong>Pre-existing condition (PEC)</strong></td><td>A condition that may have existed before the relevant policy effective date. The exact contractual definition must be taken from the applicable policy wording.</td></tr>
            <tr><td><strong>Declared condition</strong></td><td>A condition disclosed during enrolment or underwriting where a declaration process applies.</td></tr>
            <tr><td><strong>Possible undeclared PEC</strong></td><td>A case where the records suggest earlier onset and the declaration history needs review. It is a review trigger, not an automatic conclusion.</td></tr>
            <tr><td><strong>Waiting period</strong></td><td>A policy-defined period during which specified benefits may be restricted. Duration and applicability must be checked in the member-specific TOB and policy wording.</td></tr>
            <tr><td><strong>Medical declaration</strong></td><td>The enrolment or underwriting record used to compare disclosed history with the documentation available for the current request.</td></tr>
          </table>
        </div>
        <div class="glass-card">
          <div class="card-title">Three Principles for Fair Review</div>
          <table class="styled-table">
            <tr><th>Principle</th><th>How to Apply It</th></tr>
            <tr><td>Use the contract</td><td>Read the exact policy wording, effective date, TOB and any underwriting decision. Avoid relying on assumptions from another product.</td></tr>
            <tr><td>Use evidence</td><td>Review documented onset, diagnosis date, prior treatment, medication history, investigations and declaration records. Do not infer a conclusion from the diagnosis name alone.</td></tr>
            <tr><td>Document uncertainty</td><td>When evidence is incomplete, request the missing information and record the reason for the query.</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="glass-card">
          <div class="card-title">Evidence Review Workflow</div>
          <div class="timeline-item"><div class="timeline-dot" style="background:rgba(255,107,107,.2);color:#ff6b6b;">1</div><div><strong>Identify the review question</strong> — What information suggests possible earlier onset or prior treatment?</div></div>
          <div class="timeline-item"><div class="timeline-dot" style="background:rgba(251,191,36,.2);color:#fbbf24;">2</div><div><strong>Check the policy record</strong> — Effective date, TOB, waiting-period wording, declaration form where applicable, and any underwriting note.</div></div>
          <div class="timeline-item"><div class="timeline-dot" style="background:rgba(167,139,250,.2);color:#a78bfa;">3</div><div><strong>Collect clinical evidence</strong> — Documented onset, diagnosis date, previous visits, medication history, relevant reports and treatment chronology.</div></div>
          <div class="timeline-item"><div class="timeline-dot" style="background:rgba(79,156,249,.2);color:#4f9cf9;">4</div><div><strong>Compare evidence with wording</strong> — Decide whether the available records answer the contractual question or whether further clarification is needed.</div></div>
          <div class="timeline-item"><div class="timeline-dot" style="background:rgba(52,211,153,.2);color:#34d399;">5</div><div><strong>Record the outcome</strong> — Summarise the evidence reviewed, missing items, applicable policy language and final rationale.</div></div>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class="glass-card">
          <div class="card-title">Minimum Documentation for a PEC Review</div>
          <table class="styled-table">
            <tr><th>Area</th><th>What to Capture</th></tr>
            <tr><td>Policy context</td><td>Product, effective date, TOB, waiting-period wording and declaration process where applicable.</td></tr>
            <tr><td>Clinical chronology</td><td>Symptoms, documented onset, diagnosis date, treatment dates, medication history and previous investigations.</td></tr>
            <tr><td>Evidence source</td><td>Clinical note, report, prescription history, discharge summary, declaration form or other relevant record.</td></tr>
            <tr><td>Open question</td><td>The precise missing item needed to reach a fair decision.</td></tr>
            <tr><td>Outcome</td><td>Decision rationale linked to the member-specific policy wording and evidence reviewed.</td></tr>
          </table>
          <div class="info-box" style="margin-top:.8rem;"><strong>Good practice:</strong> Distinguish a genuine evidence gap from an unsupported assumption. A diagnosis recorded soon after enrolment does not, by itself, prove non-disclosure.</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 7 — INPATIENT & EMERGENCY
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "🏥  Inpatient & Emergency":
    st.session_state.progress["inpatient"] = True
    st.markdown('<div class="section-title">Inpatient & Emergency</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Admission review, emergency stabilisation, length of stay, and DRG payment concepts</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🏥 Admission Review", "🚨 Emergency Review", "💰 DRG & Payment"])

    with tab1:
        st.markdown("""
        <div class="glass-card">
          <div class="card-title">Elective Inpatient Review</div>
          <table class="styled-table"><tr><th>Step</th><th>What to Review</th></tr>
          <tr><td>1. Eligibility</td><td>Membership, network, inpatient benefit, TOB, limits and any referral or authorisation requirement.</td></tr>
          <tr><td>2. Clinical need</td><td>Reason for admission, diagnosis, proposed treatment, comorbidities, monitoring needs and whether a lower-acuity setting is safe.</td></tr>
          <tr><td>3. Expected course</td><td>Estimated length of stay, procedure plan, discharge criteria and any foreseeable complication risk.</td></tr>
          <tr><td>4. Ongoing review</td><td>Progress notes, investigations, treatment response, continued-stay justification and discharge planning.</td></tr>
          <tr><td>5. Discharge record</td><td>Discharge summary, final diagnoses, procedures, dates and documentation required for accurate grouping and payment.</td></tr></table>
        </div>
        <div class="glass-card"><div class="card-title">Length-of-Stay Review</div>
        <div class="info-box">Length of stay is a clinical-review question, not a fixed number copied from another case. Compare the expected course with the documented condition, complications, treatment response and discharge readiness.</div></div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="glass-card">
          <div class="card-title">Emergency Care Review</div>
          <div class="success-box"><strong>Clinical priority:</strong> Immediate assessment and stabilisation take priority when delay could place the patient at risk.</div>
          <table class="styled-table"><tr><th>Review Area</th><th>What to Capture</th></tr>
          <tr><td>Presentation</td><td>Symptoms, triage category, vital signs, examination findings and the reason urgent care was required.</td></tr>
          <tr><td>Stabilisation</td><td>Immediate treatment, investigations, clinical response and the point at which the patient could safely continue in the appropriate setting.</td></tr>
          <tr><td>Administrative follow-up</td><td>Network status, notification timing and ongoing-care authorisation according to the applicable policy and regulator framework.</td></tr>
          <tr><td>Transfer planning</td><td>Whether transfer is clinically safe and appropriate after stabilisation.</td></tr></table>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class="glass-card">
          <div class="card-title">DRG — Inpatient Payment Logic</div>
          <p style="font-size:.88rem;color:#9aa3b8;line-height:1.7;">Diagnosis Related Groups are case-based categories used for inpatient reimbursement. A grouper processes the coded encounter and returns a DRG. Payment then depends on the applicable local methodology, relative weight, base rate, contract terms and eligible adjustments.</p>
          <table class="styled-table"><tr><th>Review Layer</th><th>What to Validate</th><th>Common Risk</th></tr>
          <tr><td>Clinical</td><td>Reason for admission, course of treatment, length of stay and discharge plan.</td><td>Admission or continued stay not supported by the clinical record.</td></tr>
          <tr><td>Coding</td><td>Principal diagnosis, secondary diagnoses, procedures, dates and discharge status.</td><td>Unsupported secondary diagnosis, incorrect sequencing or mismatched procedure coding.</td></tr>
          <tr><td>Grouping</td><td>Correct local grouper version and expected DRG output.</td><td>Wrong grouper version or overlooked edit.</td></tr>
          <tr><td>Payment</td><td>Relative weight, base rate, outlier logic and contracted adjustments.</td><td>Incorrect outlier or unsupported add-on.</td></tr>
          <tr><td>Audit trail</td><td>Discharge summary, operative report, clinical evidence and coding-query history.</td><td>Code assignment not supported by contemporaneous documentation.</td></tr></table>
          <div class="source-note">For Abu Dhabi, use the current <a href="https://www.doh.gov.ae/en/shafafiya" target="_blank">DOH Shafafiya</a> standards, claims and adjudication rules, coding manual and applicable updates. This page is a learning summary, not a tariff calculator.</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 8 — INTERNAL AUDIT
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "🔎  Internal Audit":
    st.session_state.progress["audit"] = True
    st.markdown('<div class="section-title">Internal Audit in Health Insurance</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Risk-based review, coding quality, utilisation patterns, FWA awareness, and defensible documentation</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔎 Audit Fundamentals", "⚠️ FWA Awareness", "📋 Audit Documentation"])

    with tab1:
        st.markdown("""
        <div class="glass-card"><div class="card-title">Types of Health-Insurance Review</div>
        <table class="styled-table"><tr><th>Review Type</th><th>When It Happens</th><th>Focus</th></tr>
        <tr><td><span class="badge badge-violet">Prospective</span></td><td>Before a planned service</td><td>Eligibility, benefit, medical necessity, setting and documentation.</td></tr>
        <tr><td><span class="badge badge-cyan">Concurrent</span></td><td>During an active admission</td><td>Clinical progress, continued-stay need, complications and discharge planning.</td></tr>
        <tr><td><span class="badge badge-blue">Retrospective</span></td><td>After claim submission or payment</td><td>Coding, billing, documentation, utilisation and payment accuracy.</td></tr>
        <tr><td><span class="badge badge-amber">Focused provider review</span></td><td>After a pattern or outlier is identified</td><td>Peer comparison, claim sample review and evidence-based findings.</td></tr></table></div>
        <div class="glass-card"><div class="card-title">A Simple Risk-Based Audit Cycle</div>
        <div class="timeline-item"><div class="timeline-dot" style="background:rgba(79,156,249,.2);color:#4f9cf9;">1</div><div><strong>Define the question</strong> — What pattern, risk or quality concern is being tested?</div></div>
        <div class="timeline-item"><div class="timeline-dot" style="background:rgba(34,211,197,.2);color:#22d3c5;">2</div><div><strong>Select a reproducible sample</strong> — Document the population, period, sampling method and inclusion criteria.</div></div>
        <div class="timeline-item"><div class="timeline-dot" style="background:rgba(167,139,250,.2);color:#a78bfa;">3</div><div><strong>Review against a defined standard</strong> — TOB, coding guideline, claims rule, contract term or clinical evidence standard.</div></div>
        <div class="timeline-item"><div class="timeline-dot" style="background:rgba(251,191,36,.2);color:#fbbf24;">4</div><div><strong>Quantify the finding</strong> — Frequency, severity, financial impact and whether the issue is isolated or systemic.</div></div>
        <div class="timeline-item"><div class="timeline-dot" style="background:rgba(52,211,153,.2);color:#34d399;">5</div><div><strong>Close the loop</strong> — Correct errors, provide feedback, track actions and measure whether the pattern improves.</div></div></div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="glass-card"><div class="card-title">Fraud, Waste and Abuse — Learning Definitions</div>
        <table class="styled-table"><tr><th>Category</th><th>Meaning</th><th>Example Pattern</th></tr>
        <tr><td><span class="badge badge-coral">Fraud</span></td><td>Intentional deception intended to obtain an improper benefit or payment.</td><td>Billing for a service that was not rendered or deliberately falsifying a record.</td></tr>
        <tr><td><span class="badge badge-amber">Waste</span></td><td>Unnecessary expenditure or inefficient use of resources, even where deliberate deception is not established.</td><td>Repeated testing without a documented clinical reason.</td></tr>
        <tr><td><span class="badge badge-blue">Abuse or misuse</span></td><td>A practice inconsistent with sound clinical, coding or billing standards.</td><td>Unsupported upcoding, unbundling or inappropriate modifier use.</td></tr></table></div>
        <div class="glass-card"><div class="card-title">Signals That Justify Review — Not Automatic Conclusions</div>
        <table class="styled-table"><tr><th>Signal</th><th>Why Review It</th><th>Next Step</th></tr>
        <tr><td>Unusual code distribution</td><td>May indicate case-mix differences, documentation issues or coding inflation.</td><td>Compare peers, stratify by service type and review a sample of records.</td></tr>
        <tr><td>Frequent duplicate-like claims</td><td>Could be a resubmission issue, split billing or duplicate payment risk.</td><td>Compare claim identifiers, dates, codes, units and remittance history.</td></tr>
        <tr><td>High modifier usage</td><td>May signal bypass of bundling rules.</td><td>Review code pairs, documentation and the applicable coding rule.</td></tr>
        <tr><td>Outlier length of stay or admission rate</td><td>Could reflect case mix or an avoidable-utilisation pattern.</td><td>Review clinical acuity, diagnoses, treatment course and peer comparison.</td></tr>
        <tr><td>Unsupported CC/MCC coding</td><td>May alter DRG weight and payment.</td><td>Verify whether the diagnosis is documented and meets the applicable coding standard.</td></tr></table>
        <div class="info-box" style="margin-top:.8rem;"><strong>Key lesson:</strong> A red flag starts an evidence-based review. It is not proof of wrongdoing.</div></div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class="glass-card"><div class="card-title">Audit Finding — Quality Checklist</div>
        <table class="styled-table"><tr><th>Element</th><th>What a Strong Finding Includes</th></tr>
        <tr><td>Audit objective</td><td>The question being tested and why it matters.</td></tr>
        <tr><td>Scope and sample</td><td>Review period, population, sample method and records examined.</td></tr>
        <tr><td>Evidence</td><td>Clinical notes, coded data, claim lines, reports, remittance records and relevant correspondence.</td></tr>
        <tr><td>Applicable standard</td><td>TOB, claims rule, coding guideline, contract term or evidence standard used for comparison.</td></tr>
        <tr><td>Finding</td><td>What happened, how often, and whether the issue is isolated or systemic.</td></tr>
        <tr><td>Impact</td><td>Clinical, operational, quality and financial effect where measurable.</td></tr>
        <tr><td>Action plan</td><td>Correction, education, process improvement, recovery review or further investigation, with an owner and target date.</td></tr>
        <tr><td>Follow-up</td><td>How improvement will be measured and when re-audit will occur.</td></tr></table>
        <div class="info-box" style="margin-top:.8rem;"><strong>Professional writing tip:</strong> Separate facts, criteria, analysis and recommendation. A reviewer should be able to reproduce the conclusion from the evidence cited.</div></div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 9 — SPECIALTY RULES
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "💊  Specialty Rules":
    st.session_state.progress["specialty"] = True
    st.markdown('<div class="section-title">Specialty Rules</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">General review frameworks for physiotherapy, pharmacy, maternity and dental benefits</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🦴 Physiotherapy", "💊 Pharmacy & Rx", "🤱 Maternity", "🦷 Dental"])

    with tab1:
        st.markdown("""
        <div class="glass-card">
          <div class="card-title">Physiotherapy — General UAE Review Framework</div>
          <div class="info-box">There is no single UAE-wide fixed session allowance that applies to every member. Review the regulator framework, product, member-specific TOB, network, referral route, prior-authorisation requirement and benefit balance.</div>
          <table class="styled-table">
            <tr><th>Review Area</th><th>General Principle</th><th>What to Check</th></tr>
            <tr><td>Clinical indication</td><td>Physiotherapy should address a documented impairment, activity limitation or participation restriction.</td><td>Diagnosis, reason for referral or direct-access assessment, baseline findings and functional goals.</td></tr>
            <tr><td>Assessment and plan</td><td>Use an individualised treatment plan with milestones and regular reassessment.</td><td>Baseline assessment, treatment method, frequency or duration, site, progress and outcome measure.</td></tr>
            <tr><td>Referral route</td><td>DHA standards recognise physician referral in inpatient care and direct access or self-referral in other settings. Insurance-payment rules may still require a referral.</td><td>Setting, product rules, network and member-specific TOB.</td></tr>
            <tr><td>Prior approval</td><td>The Abu Dhabi Basic Product regulations state that physiotherapy treatment services require prior approval from the authorised insurer.</td><td>Regulator framework, product, authorisation status and contracted process.</td></tr>
            <tr><td>Additional sessions</td><td>Do not assume that one fixed session batch applies to every UAE product.</td><td>Clinical progress, treatment milestones, remaining benefit and applicable TOB limits.</td></tr>
            <tr><td>Coding</td><td>Bill only documented services using the applicable coding standard and tariff.</td><td>Evaluation or re-evaluation, timed services, duration, units and treatment note.</td></tr>
          </table>
          <div class="source-note">Official starting points: <a href="https://dha.gov.ae/uploads/062023/Standards%20Physiotherapy%20Service%20Final%202023625844.pdf" target="_blank">DHA Standards for Physiotherapy Services</a> and the <a href="https://www.doh.gov.ae/-/media/0BE585B5E6814D81913697DD6E644C02.ashx" target="_blank">Abu Dhabi health-insurance regulations</a>. Always confirm the current product and TOB.</div>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="glass-card">
          <div class="card-title">Pharmacy Benefit Review</div>
          <div class="info-box">Medication coverage is product-specific. Formularies and exclusions vary by product, so use a consistent review sequence rather than assume that one list applies to every member.</div>
          <table class="styled-table">
            <tr><th>Review Area</th><th>What to Check</th></tr>
            <tr><td>Prescription and diagnosis</td><td>Licensed prescriber, covered diagnosis, dose, duration, quantity and clinical indication.</td></tr>
            <tr><td>Formulary status</td><td>Covered medicine, preferred alternative, generic substitution rule, step-therapy requirement and any prior-authorisation condition.</td></tr>
            <tr><td>Safety</td><td>Duplicate therapy, allergy, contraindication, interaction, renal or hepatic adjustment and age-appropriate dosing where relevant.</td></tr>
            <tr><td>Benefit limits</td><td>Co-pay, pharmacy network, chronic refill rule, quantity limit and any product-specific exclusion.</td></tr>
            <tr><td>Documentation</td><td>Prescription, diagnosis, clinical note and supporting laboratory result where the medicine requires monitoring or documented deficiency.</td></tr>
          </table>
          <div class="source-note">The <a href="https://www.dha.gov.ae/uploads/112021/f6eb62ac-f666-4cce-9a2f-47788a25f565.pdf" target="_blank">DHA Pharmacy Guidelines</a> are an official starting point for safe pharmacy practice. Insurance coverage still depends on the member-specific TOB and formulary.</div>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class="glass-card">
          <div class="card-title">Maternity Benefit Review</div>
          <div class="info-box">Separate the clinical-care question from the insurance-benefit question. Clinical timing follows current antenatal guidance; payment depends on the member-specific maternity benefit and TOB.</div>
          <table class="styled-table">
            <tr><th>Review Area</th><th>What to Check</th></tr>
            <tr><td>Maternity benefit</td><td>Whether maternity is included, waiting-period wording, network, co-pay, package structure and any sub-limit.</td></tr>
            <tr><td>Antenatal consultation</td><td>Gestational age, risk category, care plan and whether the request is routine or related to a complication.</td></tr>
            <tr><td>Ultrasound request</td><td>Gestational age, clinical indication, prior scan history and the type of scan requested. Use current official antenatal guidance for timing and indications.</td></tr>
            <tr><td>Delivery planning</td><td>Expected delivery route, documented clinical indication for intervention, facility network and package or itemised-billing rules.</td></tr>
            <tr><td>Pregnancy complication</td><td>Review the medical indication, severity, treatment plan and whether the service falls under maternity or another covered medical benefit.</td></tr>
          </table>
          <div class="source-note">For Abu Dhabi clinical-care standards, see the <a href="https://www.doh.gov.ae/-/media/53DDEF165163450481481DE46FCA653C.ashx" target="_blank">DOH Antenatal Care Standard</a> and <a href="https://www.doh.gov.ae/-/media/Feature/Resources/Guidelines/antenatal-ultrasound-guideline.ashx" target="_blank">DOH Antenatal Ultrasound Guideline</a>. Use the current source and the member-specific TOB.</div>
        </div>
        """, unsafe_allow_html=True)

    with tab4:
        st.markdown("""
        <div class="glass-card">
          <div class="card-title">Dental Coverage — General Adjudication Principles</div>
          <table class="styled-table">
            <tr><th>Check</th><th>What to Do</th></tr>
            <tr><td>1. Confirm the applicable framework</td><td>Identify the emirate, policy type, network and current TOB. Do not assume that a dental benefit exists merely because the medical policy is active.</td></tr>
            <tr><td>2. Check the dental benefit wording</td><td>Read the TOB for covered categories, exclusions, annual or category limits, co-pay, waiting periods, frequency rules, age rules and any pre-authorisation requirement.</td></tr>
            <tr><td>3. Check network and provider eligibility</td><td>Verify that the requesting dental provider is eligible for the member's network and that the requested service is within the provider's licensed scope.</td></tr>
            <tr><td>4. Review clinical documentation</td><td>Confirm tooth number, diagnosis, treatment plan, relevant radiographs or periodontal charting, service code, cost and previous treatment on the same tooth where relevant.</td></tr>
            <tr><td>5. Assess categories separately</td><td>Preventive, restorative, endodontic, periodontal, prosthodontic, orthodontic, implant, sedation and emergency dental services may have different benefit rules.</td></tr>
          </table>
          <div class="info-box" style="margin-top:.8rem;"><strong>Important:</strong> The Abu Dhabi Basic Product lists dental treatment, dental prostheses and orthodontic treatment among excluded healthcare services. Enhanced products may extend coverage. For Dubai and other emirates, check the current framework and member-specific TOB.</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 10 — CASE STUDIES
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "🎯  Case Studies":
    st.session_state.progress["cases"] = True
    st.markdown('<div class="section-title">Case Study Simulator</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Fictional scenarios for practising structured review. Focus on the next best step, not a rule copied from another product.</div>', unsafe_allow_html=True)
    st.markdown("""<div class="disclaimer">These scenarios are fictional. In live work, use the member-specific TOB, current official rules, clinical documentation and the configured claims workflow.</div>""", unsafe_allow_html=True)

    cases = [
        {"id":1,"title":"MRI Lumbar Spine — Missing Clinical Detail","scenario":"""**Request:** MRI lumbar spine for low-back pain. **Documentation:** short symptom history; no red-flag assessment or examination findings attached.""","options":["Approve automatically","Deny automatically","Request the missing clinical assessment, symptom chronology, red flags and relevant prior management","Assume an exclusion"],"answer":2,"explanation":"The best next step is a focused information request. Imaging appropriateness depends on the scenario; avoid a blanket rule that every patient needs the same prerequisite."},
        {"id":2,"title":"Physiotherapy — Additional Sessions","scenario":"""**Request:** Additional physiotherapy sessions for a shoulder condition. **Documentation:** previous sessions are visible, but the progress note is not attached.""","options":["Approve every request","Deny because a fixed session maximum has been reached","Review the TOB and request progress against baseline findings and functional goals","Ignore previous treatment"],"answer":2,"explanation":"There is no single UAE-wide session batch for every product. Review the benefit and request functional-progress documentation."},
        {"id":3,"title":"Possible Pre-existing Condition","scenario":"""**Request:** Chronic-condition follow-up shortly after enrolment. **Documentation:** note mentions treatment before the policy date; declaration history is not attached.""","options":["Deny immediately","Approve without review","Request declaration records, documented onset and relevant previous history","Assume fraud"],"answer":2,"explanation":"Possible earlier onset is a reason to review evidence, not an automatic decision. Compare documented chronology with the applicable policy wording."},
        {"id":4,"title":"Emergency — Out-of-Network Presentation","scenario":"""**Presentation:** Acute symptoms at an out-of-network facility. Immediate assessment and stabilisation are underway.""","options":["Delay care until network status is confirmed","Treat the urgent clinical need first and review administrative requirements for ongoing care","Reject automatically","Transfer before the patient is stable"],"answer":1,"explanation":"Clinical stabilisation takes priority. The ongoing-care route, notification and transfer plan should then follow the applicable framework."},
        {"id":5,"title":"DRG Audit — Unsupported Secondary Diagnosis","scenario":"""**Audit sample:** A secondary diagnosis increases DRG severity, but the discharge summary and progress notes do not clearly support it.""","options":["Accept the code automatically","Remove every secondary diagnosis","Query the documentation and apply the coding standard before finalising the finding","Assume fraud immediately"],"answer":2,"explanation":"A DRG audit must be evidence-based. Verify whether the secondary diagnosis is documented and meets the applicable coding standard."},
        {"id":6,"title":"Duplicate-Like Claim","scenario":"""**Audit signal:** Two similar claim lines appear for the same member, provider and date.""","options":["Recoup automatically","Ignore the second line","Compare claim identifiers, codes, units, remittance history and whether one line is a corrected resubmission","Report fraud without review"],"answer":2,"explanation":"A duplicate-like signal needs validation. Resubmissions and corrected claims can resemble duplicates."},
        {"id":7,"title":"Dental Crown — Benefit Check","scenario":"""**Request:** Crown with tooth number and treatment plan. The member's dental benefit details are not attached.""","options":["Approve because crowns are always covered","Deny because crowns are always excluded","Check the TOB, network, dental category, limits and supporting documentation","Apply a fixed limit from another product"],"answer":2,"explanation":"Dental benefits are product-specific. Review the exact member benefit rather than applying a remembered company rule."},
        {"id":8,"title":"Vaccination — Routine Schedule Question","scenario":"""**Request:** Childhood vaccination dose. The child has an incomplete record.""","options":["Create a schedule from memory","Use the current emirate schedule and official catch-up guidance","Deny the request","Apply an adult schedule"],"answer":1,"explanation":"Use the current official DHA or DOH schedule and catch-up guidance, including minimum intervals and special-risk instructions."},
        {"id":9,"title":"Provider Outlier — High Modifier Use","scenario":"""**Audit signal:** One provider uses a billing modifier far more often than peers.""","options":["Conclude fraud immediately","Review a reproducible sample against the coding rule and documentation","Recoup every modified claim","Ignore peer comparison"],"answer":1,"explanation":"An outlier is a review trigger. Compare peers, select a defensible sample and assess supporting documentation."},
        {"id":10,"title":"Elective Admission — Setting Review","scenario":"""**Request:** Elective inpatient admission for a planned procedure. The note does not explain why outpatient or day-case care is unsuitable.""","options":["Approve every admission","Request the clinical rationale for the proposed setting and expected length of stay","Reject every inpatient request","Use cost alone"],"answer":1,"explanation":"Admission review should assess whether the proposed setting is clinically appropriate and supported by the record."},
    ]
    if "case_answers" not in st.session_state:
        st.session_state.case_answers = {}
    case_num = st.selectbox("Select Case:", [f"Case {c['id']}: {c['title']}" for c in cases])
    case_idx = int(case_num.split(":")[0].replace("Case ", "")) - 1
    case = cases[case_idx]
    st.markdown(f'<div class="glass-card"><div style="font-weight:700;font-size:1rem;margin-bottom:.8rem;">📋 Case {case["id"]}: {case["title"]}</div>', unsafe_allow_html=True)
    st.markdown(case["scenario"])
    st.markdown('</div>', unsafe_allow_html=True)
    choice = st.radio("Your decision:", case["options"], key=f"case_{case['id']}")
    chosen_idx = case["options"].index(choice)
    if st.button("Submit Decision", key=f"submit_{case['id']}"):
        st.session_state.case_answers[case['id']] = chosen_idx
        if chosen_idx == case["answer"]:
            st.markdown(f'<div class="success-box">✅ <strong>Correct.</strong><br/>{case["explanation"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="warning-box">Review the principle again. Suggested answer: <strong>{case["options"][case["answer"]]}</strong><br/><br/>{case["explanation"]}</div>', unsafe_allow_html=True)
    correct = sum(1 for cid, ans in st.session_state.case_answers.items() if cid <= len(cases) and ans == cases[cid-1]["answer"])
    st.markdown(f'<div class="metric-card" style="margin-top:1rem;"><div class="metric-val" style="color:#22d3c5;">{correct}/{len(st.session_state.case_answers)}</div><div class="metric-lbl">Cases Correct So Far</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 11 — QUIZ
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "📝  Knowledge Quiz":
    st.session_state.progress["quiz"] = True
    st.markdown('<div class="section-title">Knowledge Quiz</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Test your understanding across all modules. 80% required to pass each section.</div>', unsafe_allow_html=True)

    all_questions = [
        {"q":"What is the best first step when a prior-authorisation request is missing important clinical detail?","opts":["Approve automatically","Deny automatically","Request the specific missing information","Apply a rule from another product"],"a":2,"module":"Claims"},
        {"q":"Which document should be checked for member-specific coverage, limits and co-pay?","opts":["The TOB","A previous member's approval","A general internet article","A provider price list only"],"a":0,"module":"Foundations"},
        {"q":"What does DRG stand for?","opts":["Drug Reimbursement Guide","Diagnosis Related Group","Diagnostic Referral Grade","Documentation Review Grid"],"a":1,"module":"Coding"},
        {"q":"Which item can change an inpatient DRG result?","opts":["Principal diagnosis and supported secondary diagnoses","The colour of the insurance card","The reviewer name","The day of the week alone"],"a":0,"module":"Coding"},
        {"q":"A physiotherapy request for additional sessions should be reviewed using:","opts":["One fixed UAE-wide session maximum","The TOB, clinical progress and functional goals","The provider name only","The member age only"],"a":1,"module":"Specialty"},
        {"q":"A possible undeclared pre-existing condition should first trigger:","opts":["Automatic denial","Evidence review and comparison with policy wording","Automatic fraud referral","Deletion of the claim"],"a":1,"module":"Pre-existing"},
        {"q":"What is the purpose of a risk-based audit sample?","opts":["To prove wrongdoing before review","To test a defined concern using a reproducible method","To review only the most expensive claim","To avoid documentation"],"a":1,"module":"Audit"},
        {"q":"A red flag in an audit is:","opts":["Proof of fraud","A signal that justifies evidence-based review","Always a billing error","A reason to recoup every claim"],"a":1,"module":"Audit"},
        {"q":"Which is a core element of an audit finding?","opts":["A vague statement without evidence","Evidence and the applicable standard","A copied conclusion without analysis","A copied template without analysis"],"a":1,"module":"Audit"},
        {"q":"For an emergency presentation, the first priority is:","opts":["Administrative paperwork","Immediate clinical assessment and stabilisation","Waiting for network transfer","Cost negotiation"],"a":1,"module":"Inpatient"},
        {"q":"Dental coverage should be assessed using:","opts":["One fixed UAE-wide dental limit","The member-specific TOB and clinical documentation","A previous product's rule","The provider name alone"],"a":1,"module":"Specialty"},
        {"q":"For a childhood catch-up vaccination schedule, use:","opts":["A schedule created from memory","The current official emirate guidance","An adult schedule","A rule from another product"],"a":1,"module":"Specialty"},
        {"q":"A TPA generally:","opts":["Processes claims on behalf of the insurer","Always holds the insurance risk","Is the same as the regulator","Only handles dental claims"],"a":0,"module":"Foundations"},
        {"q":"Why should the grouper version be checked in DRG review?","opts":["Because the output can depend on the applicable version","Because it changes the member name","Because it replaces clinical documentation","Because it removes the need for coding"],"a":0,"module":"Coding"},
        {"q":"When an imaging request is reviewed, the most useful question is:","opts":["Is this always approved?","What clinical question should the imaging answer?","Did another member receive it?","Is it expensive?"],"a":1,"module":"Claims"},
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
    st.session_state.progress["resources"] = True
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
            <tr><td>DHA Standards for Physiotherapy Services</td><td>Dubai physiotherapy service requirements, referral, assessment, treatment planning, reassessment and documentation</td><td><a href="https://dha.gov.ae/uploads/062023/Standards%20Physiotherapy%20Service%20Final%202023625844.pdf" target="_blank" style="color:#4f9cf9;">DHA physiotherapy standard PDF</a></td></tr>
            <tr><td>DHA Pharmacy Guidelines</td><td>Dubai pharmacy practice, medication safety, prescribing and dispensing guidance</td><td><a href="https://www.dha.gov.ae/uploads/112021/f6eb62ac-f666-4cce-9a2f-47788a25f565.pdf" target="_blank" style="color:#4f9cf9;">DHA pharmacy guideline PDF</a></td></tr>
            <tr><td>DOH Antenatal Care Standard</td><td>Abu Dhabi antenatal-care service specifications and minimum requirements</td><td><a href="https://www.doh.gov.ae/-/media/53DDEF165163450481481DE46FCA653C.ashx" target="_blank" style="color:#4f9cf9;">DOH antenatal standard PDF</a></td></tr>
            <tr><td>DOH Antenatal Ultrasound Guideline</td><td>Abu Dhabi ultrasound guidance for pregnancy</td><td><a href="https://www.doh.gov.ae/-/media/Feature/Resources/Guidelines/antenatal-ultrasound-guideline.ashx" target="_blank" style="color:#4f9cf9;">DOH ultrasound guideline PDF</a></td></tr>
            <tr><td>DHA Immunisation Guideline — Issue 4</td><td>Current Dubai / UAE NIP childhood schedule, school-age schedule, minimum intervals, catch-up guidance, RSV and PCV updates</td><td><a href="https://dha.gov.ae/uploads/102024/Clinical%20Guideline%20for%20Best%20Practice%20in%20Immunization20241028945.pdf" target="_blank" style="color:#4f9cf9;">DHA guideline PDF</a></td></tr>
            <tr><td>DOH Circular 77/2026</td><td>Abu Dhabi childhood and school vaccination schedule update, effective from issuance</td><td><a href="https://www.doh.gov.ae/-/media/950546F00B64465CA91D7729996B3487.ashx" target="_blank" style="color:#4f9cf9;">DOH circular PDF</a></td></tr>
            <tr><td>Abu Dhabi Health Insurance Law and Regulations</td><td>Basic Product benefits and exclusion schedule, including dental exclusions</td><td><a href="https://www.doh.gov.ae/-/media/0BE585B5E6814D81913697DD6E644C02.ashx" target="_blank" style="color:#4f9cf9;">DOH regulations PDF</a></td></tr>
            <tr><td>DOH — Dept of Health Abu Dhabi</td><td>HAAD/DOH health insurance framework, Basic Product, Enhanced Product</td><td><a href="https://www.doh.gov.ae" target="_blank" style="color:#4f9cf9;">doh.gov.ae</a></td></tr>
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
            ("DOH Basic Product", "Mandatory minimum health insurance product under the Abu Dhabi framework"),
            ("DOH", "Department of Health Abu Dhabi — successor to HAAD"),
            ("DRG", "Diagnosis Related Group — inpatient payment grouping system"),
            ("EBP", "Essential Benefits Plan — minimum mandatory DHA health coverage plan"),
            ("Additional review", "Documented review of the member medical file where permitted by the applicable review process"),
            ("FWA", "Fraud, Waste and Abuse — improper billing or utilisation practices"),
            ("HAAD", "Health Authority Abu Dhabi — predecessor to DOH, rules still referred to as HAAD regulations"),
            ("HCC", "Hierarchical Condition Category — ICD-10 code groupings used in risk adjustment models"),
            ("HCPCS", "Healthcare Common Procedure Coding System — Level I = CPT, Level II = supplies/equipment codes"),
            ("ICD-10", "International Classification of Diseases 10th Revision — diagnosis coding standard"),
            ("IP", "Inpatient — admission to hospital for at least one overnight stay"),
            ("LoS", "Length of Stay — number of days in hospital"),
            ("MAF", "Medical Application Form — health declaration form for underwriting"),
            ("MCC", "Major Complication/Comorbidity — serious secondary diagnosis increasing DRG weight"),
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
      Regulatory content is summarised from publicly available sources. Always check the current official publication and the member-specific TOB before applying a rule in practice. The creator assumes no liability for decisions made based on content in this application.
    </div>
    """, unsafe_allow_html=True)

# 
# PAGE  PROCEDURES, DENTAL & VACCINES
# 
elif nav == "🩺  Procedures, Dental & Vaccines":
    st.session_state.progress["procedures"] = True
    st.markdown('<div class="section-title">Procedures, Dental & Vaccines</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Procedure review prompts · Dental benefit checks · UAE vaccination schedules · Complex-case documentation</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="disclaimer">
      These pathways are educational review prompts, not automatic approval or denial rules.
      The treating clinician's judgment, red flags, current official guidance and the member's specific TOB always take precedence. Verify live cases against current sources.
    </div>
    """, unsafe_allow_html=True)

    t1, t5, t2, t3, t4 = st.tabs(["🧪 First-Line & Procedures", "🧭 Common Indications", "🦷 Dental Rules", "💉 Vaccinations UAE", "📈 Escalation & High-Value"])

    #  TAB 1: FIRST LINE
    with t1:
        st.markdown("""
        <div class="glass-card">
          <div class="card-title">How to Review a Procedure Request</div>
          <p style="font-size:.87rem;color:#9aa3b8;line-height:1.7;">A procedure is not approved or declined merely because it appears on a memorised list. Start with the clinical question, then review the applicable evidence, member-specific benefit and the requested setting.</p>
          <table class="styled-table"><tr><th>Step</th><th>Questions</th></tr>
          <tr><td>1. Define the clinical question</td><td>What diagnosis or symptom is being evaluated or treated? What decision will the test or procedure inform?</td></tr>
          <tr><td>2. Check urgency and red flags</td><td>Would delay create risk? Is the request part of emergency assessment, elective workup or follow-up?</td></tr>
          <tr><td>3. Review prior assessment</td><td>Which relevant examinations, laboratory results, imaging, treatment attempts or specialist recommendations are available?</td></tr>
          <tr><td>4. Check the benefit</td><td>Is the service covered under the TOB? Are network, co-pay, limit, referral or authorisation rules relevant?</td></tr>
          <tr><td>5. Document the rationale</td><td>Record what was reviewed, what is missing and why the selected outcome is reasonable.</td></tr></table>
        </div>
        <div class="glass-card">
          <div class="card-title">Common Procedure Review Areas</div>
          <table class="styled-table"><tr><th>Area</th><th>Useful Review Questions</th></tr>
          <tr><td>Advanced imaging</td><td>What condition is being assessed? Are there red flags? How will the requested modality change management?</td></tr>
          <tr><td>Endoscopy</td><td>What symptoms, duration, alarm features, prior management and specialist rationale are documented?</td></tr>
          <tr><td>Cardiac testing</td><td>What symptoms, examination findings, ECG or other relevant evidence support the test requested?</td></tr>
          <tr><td>Rehabilitation</td><td>What impairment, functional goal, baseline assessment, treatment plan and progress measure are documented?</td></tr>
          <tr><td>Interventional procedures</td><td>What diagnosis, imaging or examination findings, alternatives, risks and treatment plan are documented?</td></tr>
          <tr><td>Laboratory monitoring</td><td>What clinical question is being answered, and is repeat testing supported by the patient's current situation and relevant guidance?</td></tr></table>
          <div class="source-note">Use current clinical guidance for the relevant scenario. The <a href="https://www.acr.org/Clinical-Resources/ACR-Appropriateness-Criteria" target="_blank">ACR Appropriateness Criteria</a> provide a useful imaging reference library.</div>
        </div>
        """, unsafe_allow_html=True)

    #  TAB 1B: COMMON INDICATION REVIEW PROMPTS
    with t5:
        st.markdown("""
        <div class="glass-card">
          <div class="card-title">Common Indications — Educational Review Prompts</div>
          <div class="warning-box"><strong>Use as a learning checklist, not an automatic approval rule.</strong> The treating clinician's judgment, red flags, age, pregnancy status, comorbidities, official guidelines, the member's TOB and the current applicable review process take precedence.</div>
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
          <div class="card-title">Dental Coverage — General, TOB-Based Adjudication</div>
          <div class="warning-box">
            Dental coverage is not a single UAE-wide package. Use the regulator framework, the member-specific TOB, the contracted network, and the clinical documentation. Do not assume that a remembered limit applies to every product.
          </div>
          <div class="timeline-item">
            <div class="timeline-dot" style="background:#4f9cf922;color:#4f9cf9;">1</div>
            <div><strong>Identify the policy framework</strong> — Confirm emirate, Basic or Enhanced Product, member network, dental add-on status, and current TOB.</div>
          </div>
          <div class="timeline-item">
            <div class="timeline-dot" style="background:#22d3c522;color:#22d3c5;">2</div>
            <div><strong>Verify benefit categories</strong> — Read the TOB separately for preventive, restorative, endodontic, periodontal, prosthodontic, orthodontic, implant, sedation, and emergency dental services.</div>
          </div>
          <div class="timeline-item">
            <div class="timeline-dot" style="background:#a78bfa22;color:#a78bfa;">3</div>
            <div><strong>Verify limit, co-pay, and frequency</strong> — Use only the member's stated TOB. Limits may be annual, per category, per tooth, per visit, or frequency-based. Never hard-code a product-specific amount.</div>
          </div>
          <div class="timeline-item">
            <div class="timeline-dot" style="background:#fbbf2422;color:#fbbf24;">4</div>
            <div><strong>Review clinical records</strong> — Confirm tooth number, diagnosis, treatment plan, service code, cost, radiographs where clinically relevant, periodontal charting where relevant, and previous treatment on the same tooth.</div>
          </div>
          <div class="timeline-item">
            <div class="timeline-dot" style="background:#34d39922;color:#34d399;">5</div>
            <div><strong>Apply the contract and escalate grey zones</strong> — Adjudicate only within the TOB and current workflow. Escalate unclear, high-cost, or clinically complex cases through the applicable review process.</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card">
          <div class="card-title">Dental Services — Neutral Reference Guide</div>
          <table class="styled-table">
            <tr><th>Service</th><th>What It Is</th><th>Adjudication Review</th></tr>
            <tr><td><strong>Dental consultation</strong></td><td>Clinical assessment of oral symptoms and treatment needs.</td><td>Check dental benefit, network eligibility, diagnosis, and any consultation-frequency rule in the TOB.</td></tr>
            <tr><td><strong>Dental radiography</strong></td><td>Targeted periapical, bitewing, panoramic, or other dental imaging used for diagnosis and treatment planning.</td><td>Confirm clinical indication and whether the requested imaging is proportionate to the treatment plan.</td></tr>
            <tr><td><strong>Scaling and polishing</strong></td><td>Professional removal of plaque, calculus, and surface stains.</td><td>Check whether preventive dental is covered and whether the TOB applies a frequency limit.</td></tr>
            <tr><td><strong>Periodontal treatment</strong></td><td>Treatment of gum disease, which may include deep scaling or root planing.</td><td>Check periodontal benefit wording, diagnosis, charting, and the requested quadrant or site.</td></tr>
            <tr><td><strong>Filling / restoration</strong></td><td>Restoration of a tooth affected by caries or structural loss.</td><td>Check restorative benefit wording, tooth number, surfaces, material rule if specified, and previous restoration history.</td></tr>
            <tr><td><strong>Root canal treatment</strong></td><td>Endodontic treatment of infected or inflamed pulp tissue.</td><td>Check endodontic coverage, tooth number, diagnosis, radiographic support where clinically relevant, and any crown-related plan wording.</td></tr>
            <tr><td><strong>Crown</strong></td><td>A restoration placed over a damaged tooth to restore structure and function.</td><td>Check prosthodontic coverage, clinical justification, tooth number, prior restoration history, and any waiting-period or frequency rule.</td></tr>
            <tr><td><strong>Bridge / denture</strong></td><td>Prosthetic replacement of missing teeth.</td><td>Check whether prostheses are expressly covered. Do not infer bridge or denture coverage from crown coverage.</td></tr>
            <tr><td><strong>Simple extraction</strong></td><td>Removal of an erupted tooth without a complex surgical approach.</td><td>Check extraction benefit, tooth number, diagnosis, and clinical note.</td></tr>
            <tr><td><strong>Surgical extraction</strong></td><td>Removal requiring a surgical approach, such as impacted or complex teeth.</td><td>Check surgical dental wording, imaging, clinical indication, and any pre-authorisation requirement.</td></tr>
            <tr><td><strong>Orthodontics</strong></td><td>Correction of tooth or jaw alignment using appliances.</td><td>Do not assume coverage. Check for an explicit orthodontic benefit, age rule, waiting period, lifetime limit, and pre-authorisation requirement.</td></tr>
            <tr><td><strong>Implant dentistry</strong></td><td>Surgical and prosthetic replacement of missing teeth using implants.</td><td>Do not assume coverage. Check explicit implant wording, clinical plan, imaging, licensed scope, and any high-value escalation rule.</td></tr>
            <tr><td><strong>Dental sedation or GA</strong></td><td>Sedation or general anaesthesia used to support dental treatment in selected cases.</td><td>Check medical necessity, setting, licensed scope, TOB wording, and whether inpatient or day-case handling is required.</td></tr>
            <tr><td><strong>Emergency dental care</strong></td><td>Urgent assessment and treatment for acute pain, trauma, bleeding, or infection.</td><td>Check the emergency definition, immediate treatment need, TOB, and any post-treatment notification workflow.</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box">
          <strong>Regulatory context:</strong> Abu Dhabi's Basic Product exclusion schedule lists all expenses relating to dental treatment, dental prostheses, and orthodontic treatment as excluded healthcare services. The regulations allow authorised insurers to extend cover for excluded services under an enhanced product. For Dubai, use the member's current TOB and the current Dubai Health Insurance Corporation framework. This page is a training summary, not a substitute for the live contract or regulator circular.
        </div>
        <div class="source-note">
          Official references: <a href="https://www.doh.gov.ae/-/media/0BE585B5E6814D81913697DD6E644C02.ashx" target="_blank">Abu Dhabi Health Insurance Law and Regulations</a> ·
          <a href="https://www.dha.gov.ae/en/dubai-health-insurance-corporation" target="_blank">Dubai Health Insurance Corporation</a> ·
          <a href="https://www.dha.gov.ae/en/licensing-regulations-dental" target="_blank">DHA Dental Policies and Regulations</a>
        </div>
        """, unsafe_allow_html=True)

    #  TAB 3: VACCINATIONS 
    with t3:
        st.markdown("""
        <div class="glass-card">
          <div class="card-title">Vaccination Coverage and Public-Health Schedule — Keep These Separate</div>
          <div class="warning-box">
            <strong>Do not mix two different questions:</strong><br/>
            1) Which vaccines are included in the current public-health immunisation schedule?<br/>
            2) Is a particular vaccine payable under this member's insurance policy?<br/><br/>
            Use the current DHA or DOH immunisation schedule for timing. Use the member-specific TOB, regulator framework, network and current applicable review process for insurance coverage. Confirm the current benefit route for the member and emirate.
          </div>
          <table class="styled-table">
            <tr><th>Framework</th><th>Training Rule</th></tr>
            <tr><td><strong>Dubai</strong></td><td>Use the current DHA immunisation guideline and the current Dubai Health Insurance Corporation framework. Confirm whether the requested vaccine is delivered through the public programme, a funded pathway, or an insurance benefit.</td></tr>
            <tr><td><strong>Abu Dhabi</strong></td><td>Use current DOH / ADPHC circulars and the member-specific product. DOH Circular 77/2026 updated the childhood and school vaccination schedule and is effective from its date of issuance.</td></tr>
            <tr><td><strong>Insurance adjudication</strong></td><td>Check the TOB for preventive care, vaccination, occupational-health, travel, school, age, network, and pre-authorisation wording. Do not infer coverage solely from the vaccine name.</td></tr>
            <tr><td><strong>Catch-up or special-risk schedule</strong></td><td>Refer to the current official schedule and clinical guideline. High-risk, delayed, preterm, immunocompromised, travel, pregnancy, and adult schedules require the applicable official guidance.</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card">
          <div class="card-title">Dubai / UAE NIP — Routine Childhood Schedule (DHA Guideline, effective 27 Jan 2026)</div>
          <table class="styled-table">
            <tr><th>Timing</th><th>Routine schedule summary</th></tr>
            <tr><td><strong>Birth — within 24 hours</strong></td><td>BCG; Hepatitis B dose 1; long-acting RSV monoclonal antibody at birth only for newborns in the defined RSV-season pathway, unless the maternal-vaccination exception applies.</td></tr>
            <tr><td><strong>2 months</strong></td><td>Hexavalent vaccine: DTaP, Hib, IPV dose 1, Hepatitis B dose 2; PCV dose 1; rotavirus dose 1.</td></tr>
            <tr><td><strong>4 months</strong></td><td>Hexavalent vaccine: DTaP, Hib, IPV dose 2, Hepatitis B dose 3; PCV dose 2; rotavirus dose 2.</td></tr>
            <tr><td><strong>6 months</strong></td><td>Pentavalent vaccine: DTP, Hib dose 3, Hepatitis B dose 4; OPV; seasonal influenza vaccine.</td></tr>
            <tr><td><strong>12 months</strong></td><td>MMR dose 1; varicella dose 1; meningococcal ACWY conjugate vaccine.</td></tr>
            <tr><td><strong>18 months</strong></td><td>Combined DTaP, Hib, IPV; OPV booster; PCV dose 3; MMR dose 2.</td></tr>
            <tr><td><strong>5–6 years</strong></td><td>Combined DTaP, IPV; OPV booster; varicella dose 2.</td></tr>
          </table>
          <div class="source-note">Use the live guideline for exceptions, minimum ages, minimum intervals, catch-up schedules, and special-risk pathways.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card">
          <div class="card-title">Dubai — School-Age Routine Schedule Summary</div>
          <table class="styled-table">
            <tr><th>Age / school stage</th><th>Routine schedule summary</th></tr>
            <tr><td><strong>5–6 years</strong></td><td>OPV booster; varicella second dose; combined DTaP-IPV booster.</td></tr>
            <tr><td><strong>10–11 years</strong></td><td>HPV first dose for girls and boys, with second dose after 6–12 months; meningococcal ACWY dose.</td></tr>
            <tr><td><strong>15–18 years</strong></td><td>Tdap booster; meningococcal ACWY dose.</td></tr>
            <tr><td><strong>From 6 months onward</strong></td><td>Seasonal influenza: one annual dose at the beginning of each influenza season, typically September–October. Children receiving influenza vaccine for the first time may require the schedule specified in the guideline.</td></tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card">
          <div class="card-title">Abu Dhabi — Childhood and School Schedule (DOH Circular 77/2026)</div>
          <table class="styled-table">
            <tr><th>Timing</th><th>Routine schedule summary</th></tr>
            <tr><td><strong>Birth</strong></td><td>BCG; Hepatitis B; RSV long-acting monoclonal antibodies for the defined newborn pathway.</td></tr>
            <tr><td><strong>End of month 2</strong></td><td>Hexavalent vaccine: diphtheria, tetanus, acellular pertussis, Hib, Hepatitis B, IPV; PCV20; RV1.</td></tr>
            <tr><td><strong>End of month 4</strong></td><td>Hexavalent vaccine; PCV20; RV1.</td></tr>
            <tr><td><strong>End of month 6</strong></td><td>Hexavalent vaccine; bOPV.</td></tr>
            <tr><td><strong>End of month 12</strong></td><td>MMR; varicella; MCV4 meningococcal ACYW135 conjugate vaccine.</td></tr>
            <tr><td><strong>End of month 18</strong></td><td>DTaP-Hib-IPV; bOPV; MMR; PCV20.</td></tr>
            <tr><td><strong>Grade 1</strong></td><td>DTaP-IPV; bOPV; varicella.</td></tr>
            <tr><td><strong>Grade 5</strong></td><td>MCV4 meningococcal ACYW135 conjugate vaccine, starting from the 2026–2027 academic year.</td></tr>
            <tr><td><strong>Grade 8</strong></td><td>HPV9 for females and males — two doses. The circular includes age-dependent HPV catch-up instructions.</td></tr>
            <tr><td><strong>Grade 11</strong></td><td>Tdap; MCV4 meningococcal ACYW135 conjugate vaccine.</td></tr>
          </table>
          <div class="source-note">DOH Circular 77/2026 also updates pneumococcal products and catch-up rules. Use the circular appendix for delayed schedules, high-risk children, and product-specific details.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card">
          <div class="card-title">Vaccination Adjudication Checklist</div>
          <table class="styled-table">
            <tr><th>Question</th><th>What to Check</th></tr>
            <tr><td>Is this a routine public-health dose?</td><td>Use the current emirate schedule and confirm where the dose should be delivered.</td></tr>
            <tr><td>Is the request an insurance claim?</td><td>Read the TOB for vaccination or preventive-care benefits, exclusions, funded pathways, age rules, network restrictions, and pre-authorisation requirements.</td></tr>
            <tr><td>Is this a catch-up dose?</td><td>Use the current official catch-up schedule and minimum-interval guidance. Do not create a schedule manually.</td></tr>
            <tr><td>Is this a special-risk case?</td><td>Check the applicable official guidance for preterm children, immunocompromised patients, RSV season, travel, occupational health, pregnancy, or adult vaccination.</td></tr>
            <tr><td>Is the information current?</td><td>Check the latest DHA and DOH circulars before applying the training summary in practice.</td></tr>
          </table>
        </div>
        <div class="source-note">
          Official references: <a href="https://dha.gov.ae/uploads/102024/Clinical%20Guideline%20for%20Best%20Practice%20in%20Immunization20241028945.pdf" target="_blank">DHA Clinical Guideline for Best Practice in Immunization — Issue 4, effective 27 Jan 2026</a> ·
          <a href="https://www.doh.gov.ae/-/media/950546F00B64465CA91D7729996B3487.ashx" target="_blank">DOH Circular 77/2026 — Updates to the Immunization Program</a>
        </div>
        """, unsafe_allow_html=True)

    #  TAB 4: COMPLEX CASE REVIEW
    with t4:
        st.markdown("""
        <div class="glass-card"><div class="card-title">Complex-Case Review</div>
        <p style="font-size:.87rem;color:#9aa3b8;line-height:1.7;">Some requests need a more detailed review because the clinical picture, policy wording or documentation is incomplete. The goal is a clear, reproducible decision trail.</p></div>
        <div class="glass-card"><div class="card-title">When to Request a More Detailed Review</div>
        <table class="styled-table"><tr><th>Scenario</th><th>Documentation Focus</th></tr>
        <tr><td>Complex elective request</td><td>Clinical summary, diagnosis, service code, reports, treatment plan, alternative options, setting and TOB.</td></tr>
        <tr><td>Possible pre-existing condition</td><td>Effective date, policy wording, declaration record where applicable, documented onset and treatment chronology.</td></tr>
        <tr><td>Unclear medical necessity</td><td>Symptoms, duration, examination findings, red flags, prior management, relevant results and specialist rationale.</td></tr>
        <tr><td>Potential coding or billing issue</td><td>Diagnosis, procedure code, units, dates, site, notes and applicable coding standard.</td></tr>
        <tr><td>Possible FWA pattern</td><td>Claims pattern, peer comparison, reproducible sample, records reviewed and evidence-based finding.</td></tr></table></div>
        <div class="glass-card"><div class="card-title">Decision-Trail Checklist</div>
        <table class="styled-table"><tr><th>Field</th><th>What to Record</th></tr>
        <tr><td>Request</td><td>Member identifier, provider, diagnosis, service, code, date and cost estimate.</td></tr>
        <tr><td>Coverage context</td><td>Eligibility, network, TOB, limits, exclusions, waiting period and authorisation status.</td></tr>
        <tr><td>Clinical evidence</td><td>Symptoms, duration, findings, results, prior management and treatment plan.</td></tr>
        <tr><td>Outcome</td><td>Approval, targeted information request, benefit clarification or documented reason for decline.</td></tr>
        <tr><td>Rationale</td><td>The evidence and policy wording that support the outcome.</td></tr></table>
        <div class="info-box" style="margin-top:.8rem;"><strong>Learning objective:</strong> A second reviewer should be able to understand and reproduce the reasoning from the record.</div></div>
        """, unsafe_allow_html=True)
