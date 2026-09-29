import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from negotiation import NegotiationEngine


LUCIDE_PATHS = {
    "layout-dashboard": '<rect x="3" y="3" width="7" height="9" rx="1"/><rect x="14" y="3" width="7" height="5" rx="1"/><rect x="14" y="12" width="7" height="9" rx="1"/><rect x="3" y="16" width="7" height="5" rx="1"/>',
    "handshake": '<path d="m11 17 2 2a1 1 0 0 0 1.4 0l4.2-4.2a2 2 0 0 0 0-2.8l-1.8-1.8"/><path d="m14 7-1.2-1.2a2 2 0 0 0-2.8 0L4 11.8a2 2 0 0 0 0 2.8l3.2 3.2a2 2 0 0 0 2.8 0L14 14"/><path d="m8 10 4 4"/><path d="m15 8 2-2 4 4-2 2"/>',
    "arrow-left-right": '<path d="M8 3 4 7l4 4"/><path d="M4 7h16"/><path d="m16 21 4-4-4-4"/><path d="M20 17H4"/>',
    "chart-no-axes-column-increasing": '<path d="M5 21V10"/><path d="M12 21V3"/><path d="M19 21v-7"/>',
    "history": '<path d="M3 12a9 9 0 1 0 2.6-6.4L3 8"/><path d="M3 3v5h5"/><path d="M12 7v5l3 2"/>',
    "circle-help": '<circle cx="12" cy="12" r="10"/><path d="M9.1 9a3 3 0 0 1 5.8 1c0 2-3 3-3 3"/><path d="M12 17h.01"/>',
    "check": '<path d="m20 6-11 11-5-5"/>',
    "chart-line": '<path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/>',
    "trending-down": '<path d="m22 17-8.5-8.5-5 5L2 7"/><path d="M16 17h6v-6"/>',
    "users-round": '<path d="M18 21a8 8 0 0 0-16 0"/><circle cx="10" cy="8" r="5"/><path d="M22 20c0-3-2-5.5-5-6.5"/><path d="M16 3.1a5 5 0 0 1 0 9.8"/>',
    "wallet": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 10h18"/><path d="M16 14h.01"/>',
    "zap": '<path d="M4 14a1 1 0 0 1-.8-1.6l9-11A.5.5 0 0 1 13 1v7h6a1 1 0 0 1 .8 1.6l-9 11A.5.5 0 0 1 10 21v-7z"/>',
}


def lucide_icon(name, size=16):
    return (
        f'<svg class="lucide-icon" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        f'aria-hidden="true">{LUCIDE_PATHS[name]}</svg>'
    )


st.set_page_config(
    page_title="DealMakerAgent | Deal Dashboard",
    page_icon="🤝",
    layout="wide",
)

if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = True
dark_mode = st.session_state["dark_mode"]
if "active_view" not in st.session_state:
    st.session_state["active_view"] = "Dashboard"
active_view = st.session_state["active_view"]

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    :root {
        --ink: #111827;
        --muted: #64748b;
        --line: #e2e8f0;
        --canvas: #f6f8fc;
        --blue: #2563eb;
        --indigo: #4f46e5;
        --purple: #7c3aed;
        --navy: #111827;
        --green: #16a34a;
        --orange: #f97316;
        --card: #ffffff;
    }
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; color: var(--ink); }
    .stApp { background: var(--canvas); }
    [data-testid="stHeader"] { display: none; }
    .block-container { max-width: 1880px; padding: .75rem 1.25rem 1.5rem; }
    h1, h2, h3 { font-family: 'Plus Jakarta Sans', sans-serif; letter-spacing: 0; color: var(--ink); }
    .st-key-topnav { position: sticky; top: 0; z-index: 100; padding: .25rem .65rem; margin: -.75rem -.65rem .75rem; border-bottom: 1px solid rgba(226,232,240,.9); background: rgba(255,255,255,.94); backdrop-filter: blur(14px); }
    .st-key-deal_setup_panel { position: sticky; top: 4.8rem; z-index: 5; align-self: flex-start; max-height: calc(100vh - 7.5rem); overflow-y: auto; scrollbar-width: thin; }
    .st-key-deal_setup_panel [data-testid="stVerticalBlock"] { gap: .45rem; }
    .st-key-deal_setup_panel [data-testid="stElementContainer"] { margin-bottom: .1rem; }
    .st-key-deal_setup_panel [data-testid="stVerticalBlockBorderWrapper"] { padding: .7rem; }
    .nav-rail { position: sticky; top: 4.8rem; display: flex; min-height: calc(100vh - 7.5rem); flex-direction: column; gap: .35rem; padding: .72rem .55rem; border: 1px solid #26324a; border-radius: 16px; background: linear-gradient(180deg,#141b2d,#101727); box-shadow: 0 9px 24px rgba(0,0,0,.2); }
    .nav-rail-link { display: flex; align-items: center; gap: .62rem; padding: .72rem .66rem; border: 1px solid transparent; border-radius: 10px; color: #d5dced; font-size: .72rem; font-weight: 650; text-decoration: none; transition: color .16s ease, background .16s ease, border-color .16s ease; }
    .nav-rail-link:hover { color: #fff; background: #1c2740; text-decoration: none; }
    .nav-rail-link.active { color: #fdba74; border-color: rgba(249,115,22,.28); background: rgba(249,115,22,.12); box-shadow: inset 2px 0 #f97316; }
    .nav-rail-label { margin: .75rem .55rem .2rem; color: #76839d; font-size: .57rem; font-weight: 800; letter-spacing: .1em; }
    .nav-rail-footer { margin-top: auto; padding: .68rem .55rem .3rem; border-top: 1px solid #29354d; color: #93a2bd; font-size: .62rem; line-height: 1.6; }
    .st-key-navigation_rail { position: sticky; top: 4.8rem; min-height: calc(100vh - 7.5rem); padding: .72rem .55rem; border: 1px solid #26324a; border-radius: 16px; background: linear-gradient(180deg,#141b2d,#101727); box-shadow: 0 9px 24px rgba(0,0,0,.2); }
    .st-key-navigation_rail [data-testid="stButton"] button { width: 100%; justify-content: flex-start; min-height: 2.75rem; padding-left: .7rem; border: 1px solid transparent; border-radius: 10px; background: transparent; color: #d5dced; text-align: left; }
    .st-key-navigation_rail [data-testid="stButton"] button:hover { color: #fff; background: #1c2740; border-color: #2b3c5d; }
    .st-key-navigation_rail [data-testid="stButton"] button[kind="primary"] { color: #fdba74; border-color: rgba(249,115,22,.28); background: rgba(249,115,22,.12); box-shadow: inset 2px 0 #f97316; }
    .brandbar { display: flex; align-items: center; gap: .65rem; min-height: 3.1rem; }
    .lucide-icon { display: inline-block; flex: 0 0 auto; vertical-align: middle; }
    .brandmark { font-size: 2rem; line-height: 1; }
    .brandname { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.2rem; font-weight: 800; color: var(--ink); }
    .brandname span { color: var(--indigo); }
    .brandnote { color: var(--muted); font-size: .72rem; }
    .navitem { text-align: center; padding: .62rem .42rem; color: #475569; font-size: .78rem; font-weight: 650; border-radius: 8px; transition: background .16s ease, color .16s ease; white-space: nowrap; }
    .navitem:hover { color: var(--indigo); background: #f1f2ff; }
    .navitem a { display: flex; align-items: center; justify-content: center; gap: .34rem; }
    .navactive { color: #fff; background: var(--indigo); border-radius: 8px; box-shadow: 0 3px 8px rgba(79,70,229,.2); }
    .navactive:hover { color: #fff; background: #4338ca; }
    .modebadge { display: inline-block; margin-top: .55rem; padding: .38rem .65rem; border: 1px solid #bbf7d0; border-radius: 20px; background: #f0fdf4; color: #15803d; font-size: .68rem; font-weight: 700; white-space: nowrap; }
    .profile { display: flex; align-items: center; justify-content: flex-end; gap: .55rem; min-height: 3rem; }
    .avatar { width: 2.35rem; height: 2.35rem; display: grid; place-items: center; border-radius: 50%; background: linear-gradient(145deg, #5267bb, #313f78); color: #fff; font-weight: 700; }
    .profile-name { font-size: .82rem; font-weight: 700; }
    .profile-role { color: var(--muted); font-size: .7rem; }
    .hero-panel { position: relative; overflow: hidden; min-height: 9.6rem; padding: 1.05rem 1.4rem; border: 1px solid rgba(255,255,255,.16); border-radius: 16px; color: #fff; background: radial-gradient(ellipse at 79% 45%, rgba(79,70,229,.72), transparent 28%), linear-gradient(108deg, #101a37 0%, #14275c 62%, #272b73 100%); box-shadow: 0 10px 28px rgba(15,23,42,.12); }
    .hero-panel:after { content: ''; position: absolute; inset: 0; opacity: .12; background-image: radial-gradient(#dbe4ff .75px, transparent .75px); background-size: 18px 18px; mask-image: linear-gradient(90deg, transparent 36%, #000 100%); pointer-events: none; }
    .hero-eyebrow { position: relative; z-index: 1; margin-bottom: .25rem; color: #a5b4fc; font-size: .64rem; font-weight: 800; letter-spacing: .12em; }
    .hero-title { position: relative; z-index: 1; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 2rem; line-height: 1.1; font-weight: 800; color: #fff; }
    .hero-title span { color: #a5b4fc; }
    .hero-subtitle { position: relative; z-index: 1; margin-top: .32rem; max-width: 42rem; font-size: .82rem; font-weight: 500; color: #e2e8f0; }
    .hero-visual { position: absolute; z-index: 1; right: 1.5rem; top: 1.2rem; display: flex; align-items: center; gap: .5rem; }
    .party-chip { padding: .55rem .7rem; border: 1px solid rgba(255,255,255,.23); border-radius: 9px; background: rgba(15,23,42,.5); color: #fff; font-size: .65rem; line-height: 1.5; white-space: nowrap; }
    .party-chip strong { display: block; font-size: .72rem; }
    .handshake-art { font-size: 3.1rem; filter: drop-shadow(0 5px 9px rgba(4,8,40,.45)); }
    .hero-badges { position: relative; z-index: 1; display: flex; gap: .4rem; margin-top: .68rem; flex-wrap: wrap; }
    .hero-badge { padding: .28rem .5rem; border: 1px solid rgba(255,255,255,.16); border-radius: 20px; background: rgba(255,255,255,.1); color: #f1f5f9; font-size: .61rem; font-weight: 600; }
    .hero-badge .lucide-icon { margin-right: .15rem; }
    .panel { padding: .85rem; border: 1px solid var(--line); border-radius: 14px; background: var(--card); box-shadow: 0 3px 12px rgba(15,23,42,.035); }
    .panel-title { font-family: 'Plus Jakarta Sans', sans-serif; font-size: .91rem; font-weight: 800; color: var(--ink); }
    .panel-subtitle { margin-top: .16rem; color: var(--muted); font-size: .72rem; }
    .view-heading { margin-bottom: .8rem; padding: 1rem 1.1rem; border: 1px solid #29354d; border-radius: 14px; background: linear-gradient(110deg,#141b2d,#191932); box-shadow: 0 6px 18px rgba(0,0,0,.16); }
    .view-heading .hero-eyebrow { margin-bottom: .2rem; }
    .view-title { color: #f8fafc; font-family: 'Plus Jakarta Sans',sans-serif; font-size: 1.35rem; font-weight: 800; }
    .view-subtitle { margin-top: .18rem; color: #a5b4cc; font-size: .74rem; }
    .statusbar { display: flex; align-items: center; gap: .7rem; height: 100%; min-height: 4.85rem; padding: .7rem .85rem; border: 1px solid #bbf7d0; border-radius: 14px; background: linear-gradient(105deg, #ecfdf5, #f7fefb); }
    .statusicon { display: grid; flex: 0 0 2.75rem; width: 2.75rem; height: 2.75rem; place-items: center; border-radius: 50%; background: var(--green); color: #fff; font-size: 1.35rem; box-shadow: 0 4px 10px rgba(22,163,74,.2); animation: success-pop .38s ease-out both; }
    @keyframes success-pop { 0% { transform: scale(.75); opacity: .3; } 75% { transform: scale(1.07); } 100% { transform: scale(1); opacity: 1; } }
    .status-title { color: #166534; font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; font-size: .83rem; }
    .status-copy { margin-top: .15rem; color: #456b5a; font-size: .67rem; }
    [data-testid="stMetric"] { min-height: 4.85rem; padding: .72rem .78rem; border: 1px solid var(--line); border-radius: 14px; background: var(--card); box-shadow: 0 3px 12px rgba(15,23,42,.035); transition: transform .16s ease, box-shadow .16s ease; }
    [data-testid="stMetric"]:hover { transform: translateY(-2px); box-shadow: 0 7px 16px rgba(15,23,42,.08); }
    [data-testid="stMetricLabel"] { color: var(--muted); font-size: .68rem; }
    [data-testid="stMetricValue"] { font-family: 'Plus Jakarta Sans', sans-serif; color: var(--ink); font-size: 1.18rem; font-weight: 800; }
    [data-testid="stButton"] button, [data-testid="stFormSubmitButton"] button, [data-testid="stDownloadButton"] button { min-height: 2.5rem; border-radius: 9px; font-weight: 700; transition: transform .16s ease, box-shadow .16s ease, background .16s ease; }
    [data-testid="stFormSubmitButton"] button[kind="primary"] { background: linear-gradient(105deg, #2563eb, #4f46e5); border-color: #4f46e5; box-shadow: 0 5px 12px rgba(79,70,229,.2); }
    [data-testid="stFormSubmitButton"] button[kind="primary"]:hover { background: linear-gradient(105deg, #1d4ed8, #4338ca); border-color: #4338ca; box-shadow: 0 7px 16px rgba(79,70,229,.28); transform: translateY(-1px); }
    [data-testid="stDownloadButton"] button { min-height: 2rem; color: var(--indigo); border-color: #c7d2fe; background: #fff; font-size: .72rem; }
    [data-testid="stDownloadButton"] button:hover { background: #eef2ff; border-color: #818cf8; }
    [data-testid="stNumberInput"] input { min-height: 2.2rem; border-radius: 7px; font-weight: 650; }
    [data-testid="stNumberInput"] input:focus { border-color: var(--indigo); box-shadow: 0 0 0 2px rgba(79,70,229,.15); }
    [data-testid="stNumberInput"] button { border-radius: 6px; color: var(--indigo); }
    [data-testid="stNumberInput"] button:hover { background: #eef2ff; }
    [data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 9px; overflow: hidden; }
    [data-testid="stVerticalBlockBorderWrapper"] { border-color: var(--line); border-radius: 14px; background: var(--card); box-shadow: 0 3px 12px rgba(15,23,42,.035); }
    .st-key-buyer_settings_panel [data-testid="stVerticalBlockBorderWrapper"] { border-color: #bfdbfe; background: #f5f9ff; }
    .st-key-seller_settings_panel [data-testid="stVerticalBlockBorderWrapper"] { border-color: #fed7aa; background: #fff8f1; }
    .section-heading { margin: .2rem 0 .35rem; font-size: .72rem; font-weight: 800; letter-spacing: .04em; }
    .buyer-heading { color: #1d4ed8; }
    .seller-heading { color: #c2410c; }
    .summary-note { color: var(--muted); font-size: .65rem; }
    .history-table-wrap { overflow-x: auto; margin-top: .65rem; border: 1px solid var(--line); border-radius: 9px; }
    .history-table { width: 100%; border-collapse: collapse; font-size: .68rem; white-space: nowrap; }
    .history-table th { padding: .55rem .45rem; background: #f8fafc; color: #475569; font-size: .62rem; font-weight: 800; text-align: left; }
    .history-table td { padding: .52rem .45rem; border-top: 1px solid #edf1f6; color: #334155; }
    .history-table tr:last-child td { color: #111827; font-weight: 650; }
    .table-number { font-variant-numeric: tabular-nums; }
    .pill { display: inline-flex; align-items: center; justify-content: center; padding: .22rem .42rem; border-radius: 20px; font-size: .57rem; font-weight: 800; }
    .pill-counter { color: #c2410c; background: #ffedd5; }
    .pill-agreement { color: #15803d; background: #dcfce7; }
    .insight-card { height: 100%; min-height: 4.5rem; display: flex; align-items: center; gap: .65rem; padding: .7rem .75rem; border: 1px solid var(--line); border-radius: 14px; background: var(--card); box-shadow: 0 3px 12px rgba(15,23,42,.035); transition: transform .16s ease, box-shadow .16s ease; }
    .insight-card:hover { transform: translateY(-2px); box-shadow: 0 7px 16px rgba(15,23,42,.08); }
    .insight-icon { display: grid; flex: 0 0 2.45rem; width: 2.45rem; height: 2.45rem; place-items: center; border-radius: 10px; }
    .insight-icon.red { background: #fef2f2; color: #dc2626; }
    .insight-icon.blue { background: #eff6ff; color: #2563eb; }
    .insight-icon.purple { background: #f5f3ff; color: #7c3aed; }
    .insight-icon.indigo { background: #eef2ff; color: #4f46e5; }
    .insight-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: .65rem; }
    .insight-label { color: #475569; font-size: .61rem; font-weight: 800; text-transform: uppercase; }
    .insight-value { margin-top: .12rem; color: #111827; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1rem; font-weight: 800; }
    .insight-caption { margin-top: .08rem; color: var(--muted); font-size: .6rem; }
    .insight-badge { align-self: flex-start; margin-left: auto; padding: .22rem .4rem; border-radius: 20px; background: #dcfce7; color: #15803d; font-size: .57rem; font-weight: 800; white-space: nowrap; }
    .flowline { display: flex; align-items: center; justify-content: center; gap: .55rem; margin: .55rem 0 .2rem; color: #64748b; font-size: .62rem; font-weight: 700; }
    .flow-step { padding: .26rem .52rem; border: 1px solid #e2e8f0; border-radius: 20px; background: #fff; }
    .flow-arrow { color: #94a3b8; }
    .help-copy { color: var(--muted); font-size: .78rem; }
    hr { border-color: var(--line); }
    @media (max-width: 1200px) {
        .hero-visual { right: .8rem; }
        .party-chip { display: none; }
    }
    @media (max-width: 900px) {
        .block-container { padding: .7rem .75rem 1.5rem; }
        .hero-panel { min-height: 10.5rem; padding: 1.1rem; }
        .hero-visual { display: none; }
        .hero-title { font-size: 1.65rem; }
        .navitem { font-size: .68rem; }
        .nav-rail { position: static; min-height: auto; flex-direction: row; overflow-x: auto; }
        .nav-rail-link { flex: 0 0 auto; }
        .nav-rail-label, .nav-rail-footer { display: none; }
        .st-key-navigation_rail { position: static; min-height: auto; padding: .45rem; }
        .st-key-navigation_rail [data-testid="stVerticalBlock"] { flex-direction: row; overflow-x: auto; }
        .st-key-navigation_rail [data-testid="stButton"] { flex: 0 0 auto; }
        .st-key-deal_setup_panel { position: static; max-height: none; overflow: visible; }
        .insight-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        .history-table { font-size: .62rem; }
    }
    @media (max-width: 560px) {
        .insight-grid { grid-template-columns: 1fr; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if dark_mode:
    st.markdown(
        """
        <style>
        :root { color-scheme:dark; --ink:#f8fafc; --muted:#a5b4cc; --line:#29354d; --canvas:#0b1020; --card:#141b2d; --blue:#38bdf8; --indigo:#6366f1; --purple:#a855f7; --navy:#0b1020; --green:#22c55e; --orange:#fb923c; }
        html, body, [class*="css"] { color:#e5eaf5; }
        .stApp, [data-testid="stAppViewContainer"] { background:#0b1020 !important; color:#e5eaf5; }
        .st-key-topnav { border-color:#26324a; background:rgba(11,16,32,.94); box-shadow:0 8px 22px rgba(0,0,0,.22); }
        .brandname, h1, h2, h3, .panel-title, .insight-value, .profile-name { color:#f8fafc; }
        .brandnote, .profile-role, [data-testid="stCaptionContainer"] { color:#9aa9c2 !important; }
        .navitem { color:#d5dced; }
        .navitem:hover { color:#fdba74; background:rgba(249,115,22,.1); }
        .navactive, .navactive:hover { color:#fdba74; background:rgba(249,115,22,.13); box-shadow:inset 0 -2px #f97316; }
        .modebadge { color:#86efac; background:#10251f; border-color:#1c5439; }
        .avatar { background:linear-gradient(145deg,#5b5de8,#312e81); }
        .st-key-deal_setup_panel, .st-key-chart_panel, .st-key-history_panel { background:#141b2d !important; border:1px solid #29354d !important; border-radius:14px; padding:.7rem; }
        .st-key-buyer_settings_panel { background:#101d35 !important; border:1px solid #1d4f91 !important; border-radius:12px; padding:.6rem; }
        .st-key-seller_settings_panel { background:#251a1a !important; border:1px solid #75421e !important; border-radius:12px; padding:.6rem; }
        .buyer-heading { color:#60a5fa; }
        .seller-heading { color:#fdba74; }
        [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] p { color:#cbd5e1 !important; }
        [data-testid="stNumberInput"] input { color:#f8fafc !important; background:#0d1426 !important; border-color:#33415c !important; }
        [data-testid="stNumberInput"] button { color:#c4b5fd !important; background:#18223a !important; border-color:#33415c !important; }
        [data-testid="stNumberInput"] button:hover { background:#263455 !important; }
        [data-testid="stMetric"] { background:#141b2d !important; border-color:#29354d !important; }
        [data-testid="stMetricLabel"] { color:#9aa9c2 !important; }
        [data-testid="stMetricValue"] { color:#f8fafc !important; }
        [data-testid="stDownloadButton"] button { color:#c4b5fd; background:#171c35; border-color:#454177; }
        [data-testid="stDownloadButton"] button:hover { color:#fff; background:#25224a; border-color:#7770ef; }
        [data-testid="stFormSubmitButton"] button[kind="primary"] { background:linear-gradient(105deg,#2563eb,#6d28d9); border-color:#6366f1; box-shadow:0 0 18px rgba(79,70,229,.28); }
        .statusbar { background:linear-gradient(105deg,#10291f,#11251f); border-color:#1c6841; }
        .statusbar-error { background:linear-gradient(105deg,#301923,#241825); border-color:#7f3342; }
        .statusbar-error .status-title { color:#fda4af; }
        .statusbar-error .status-copy { color:#e8b7c0; }
        .status-title { color:#86efac; }
        .status-copy { color:#b1d9c0; }
        .statusicon { box-shadow:0 0 18px rgba(34,197,94,.25); }
        .history-table-wrap { border-color:#2b3851; }
        .history-table th { background:#1b2438; color:#cbd5e1; }
        .history-table td { color:#d5dced; border-color:#29354d; }
        .history-table tr:last-child td { color:#f8fafc; }
        .pill-counter { color:#fdba74; background:#422719; }
        .pill-agreement { color:#86efac; background:#153b2b; }
        .insight-icon.red { color:#fca5a5; background:#341a25; }
        .insight-icon.blue { color:#7dd3fc; background:#142b44; }
        .insight-icon.purple { color:#d8b4fe; background:#2b2043; }
        .insight-icon.indigo { color:#c4b5fd; background:#232447; }
        .insight-label { color:#c3cee0; }
        .insight-caption { color:#97a6bf; }
        .insight-badge { color:#86efac; background:#153b2b; }
        .flowline { color:#9aa9c2; }
        .flow-step { color:#dbe4f3; background:#141b2d; border-color:#2d3952; }
        .flow-arrow { color:#737f99; }
        .hero-panel { background:radial-gradient(ellipse at 79% 45%,rgba(56,189,248,.24),transparent 20%),radial-gradient(ellipse at 79% 45%,rgba(124,58,237,.44),transparent 42%),linear-gradient(108deg,#0d1428 0%,#101d40 62%,#211846 100%); box-shadow:0 10px 30px rgba(0,0,0,.28),0 0 24px rgba(79,70,229,.12); }
        .handshake-art { color:#dbeafe; filter:drop-shadow(0 0 7px rgba(56,189,248,.85)) drop-shadow(0 0 19px rgba(168,85,247,.7)); }
        .party-chip { border-color:rgba(96,165,250,.42); background:rgba(8,15,34,.76); box-shadow:0 0 15px rgba(59,130,246,.08); }
        .st-key-deal_setup_panel { scrollbar-color:#4b5670 #121a2c; }
        div[data-testid="stAlert"] { background:#35191f; border-color:#7f1d1d; color:#fecaca; }
        .insight-card, [data-testid="stMetric"], .st-key-deal_setup_panel, .st-key-buyer_settings_panel, .st-key-seller_settings_panel, .st-key-chart_panel, .st-key-history_panel { box-shadow:0 6px 18px rgba(0,0,0,.2); }
        </style>
        """,
        unsafe_allow_html=True,
    )

if active_view == "Negotiation":
    view_visibility_css = ".st-key-dashboard_hero,.st-key-workflow_strip,.st-key-chart_panel,.st-key-analytics_cards_panel,.st-key-help_panel{display:none!important;}"
elif active_view == "Analytics":
    view_visibility_css = ".st-key-dashboard_hero,.st-key-workflow_strip,.st-key-summary_panel,.st-key-history_panel,.st-key-help_panel{display:none!important;}"
elif active_view == "History":
    view_visibility_css = ".st-key-dashboard_hero,.st-key-workflow_strip,.st-key-summary_panel,.st-key-chart_panel,.st-key-analytics_cards_panel,.st-key-help_panel{display:none!important;}"
elif active_view == "Help":
    view_visibility_css = ".st-key-dashboard_hero,.st-key-workflow_strip,.st-key-summary_panel,.st-key-chart_panel,.st-key-history_panel,.st-key-analytics_cards_panel{display:none!important;}"
else:
    view_visibility_css = ".st-key-help_panel{display:none!important;}"
st.markdown(f"<style>{view_visibility_css}</style>", unsafe_allow_html=True)


with st.container(key="topnav"):
    top_brand, mode_col, theme_col, profile_col = st.columns(
        [5.3, 1.35, .55, 1.4],
        vertical_alignment="center",
    )
    with top_brand:
        st.markdown(
            f'<div class="brandbar"><span class="brandmark">{lucide_icon("handshake", 32)}</span><div><div class="brandname">DealMaker<span>Agent</span></div><div class="brandnote">Intelligent Negotiation &amp; Deal Optimization</div></div></div>',
            unsafe_allow_html=True,
        )
    with mode_col:
        st.markdown('<div class="modebadge">● &nbsp; Rule-Based / Local</div>', unsafe_allow_html=True)
    with theme_col:
        st.toggle("Dark theme", key="dark_mode", help="Switch between light and dark appearance", label_visibility="collapsed")
    with profile_col:
        st.markdown(
            '<div class="profile"><div class="avatar">D</div><div><div class="profile-name">Deal operator</div><div class="profile-role">Negotiation workspace</div></div></div>',
            unsafe_allow_html=True,
        )

st.markdown('<div id="deal-dashboard"></div>', unsafe_allow_html=True)
nav_col, setup_col, dashboard_col = st.columns([.62, .95, 3.65], gap="medium")
with nav_col:
    with st.container(key="navigation_rail"):
        st.markdown('<div class="nav-rail-label">WORKSPACE</div>', unsafe_allow_html=True)
        for view_name, icon_name in [
            ("Dashboard", ":material/dashboard:"),
            ("Negotiation", ":material/swap_horiz:"),
            ("Analytics", ":material/analytics:"),
            ("History", ":material/history:"),
            ("Help", ":material/help:"),
        ]:
            if st.button(
                view_name,
                key=f"nav_{view_name.lower()}",
                icon=icon_name,
                type="primary" if st.session_state["active_view"] == view_name else "secondary",
                use_container_width=True,
            ):
                st.session_state["active_view"] = view_name
                st.rerun()
        st.markdown(
            '<div class="nav-rail-footer"><strong style="color:#fdba74">DEALMAKER</strong><br>Rule-based workspace<br>Local session</div>',
            unsafe_allow_html=True,
        )
with setup_col:
    st.markdown('<div id="deal-setup"></div>', unsafe_allow_html=True)
    with st.container(border=True, key="deal_setup_panel"):
        st.markdown("### ⚙️ Deal Setup")
        st.caption("Configure the terms for both sides.")
        st.markdown("**GENERAL**")
        quantity = st.number_input(
            "Quantity", min_value=1, value=10, step=1,
            key="quantity_input", help="Number of units in the deal.",
        )
        maximum_rounds = st.number_input(
            "Maximum Negotiation Rounds", min_value=1, value=10, step=1,
            key="maximum_rounds_input", help="Stop the negotiation after this many rounds.",
        )

        with st.container(border=True, key="buyer_settings_panel"):
            st.markdown('<div class="section-heading buyer-heading">BUYER SETTINGS</div>', unsafe_allow_html=True)
            buyer_initial = st.number_input(
                "Initial Offer (₹)", min_value=1.0, value=700.0, step=10.0,
                key="buyer_initial_input", help="The buyer's opening per-unit offer.",
            )
            buyer_maximum = st.number_input(
                "Maximum Price (₹)", min_value=1.0, value=900.0, step=10.0,
                key="buyer_maximum_input", help="The buyer's maximum acceptable per-unit price.",
            )
            buyer_concession = st.number_input(
                "Concession per Round (₹)", min_value=1.0, value=50.0, step=10.0,
                key="buyer_concession_input", help="How much the buyer increases their offer each round.",
            )

        with st.container(border=True, key="seller_settings_panel"):
            st.markdown('<div class="section-heading seller-heading">SELLER SETTINGS</div>', unsafe_allow_html=True)
            seller_initial = st.number_input(
                "Initial Offer (₹)", min_value=1.0, value=1000.0, step=10.0,
                key="seller_initial_input", help="The seller's opening per-unit asking price.",
            )
            seller_minimum = st.number_input(
                "Minimum Price (₹)", min_value=1.0, value=850.0, step=10.0,
                key="seller_minimum_input", help="The seller's minimum acceptable per-unit price.",
            )
            seller_concession = st.number_input(
                "Concession per Round (₹)", min_value=1.0, value=50.0, step=10.0,
                key="seller_concession_input", help="How much the seller decreases their price each round.",
            )

        submitted = st.button(
            "▶  Run negotiation  →",
            key="run_negotiation",
            type="primary",
            use_container_width=True,
        )
        setup_error_slot = st.empty()

if submitted:
    if buyer_initial > buyer_maximum:
        st.session_state["setup_error"] = "Buyer initial offer cannot exceed the maximum price."
    elif seller_initial < seller_minimum:
        st.session_state["setup_error"] = "Seller initial price cannot be below the minimum price."
    else:
        engine = NegotiationEngine(
            quantity=quantity,
            buyer_initial=buyer_initial,
            buyer_maximum=buyer_maximum,
            seller_initial=seller_initial,
            seller_minimum=seller_minimum,
            buyer_concession=buyer_concession,
            seller_concession=seller_concession,
            maximum_rounds=maximum_rounds,
        )
        with st.spinner("Running negotiation rounds..."):
            st.session_state["negotiation_result"] = engine.negotiate()
        st.session_state["negotiation_config"] = {
            "buyer_initial": buyer_initial,
            "seller_initial": seller_initial,
            "maximum_rounds": maximum_rounds,
        }
        st.session_state.pop("setup_error", None)

if "setup_error" in st.session_state:
    setup_error_slot.error(st.session_state["setup_error"])

if "negotiation_result" not in st.session_state:
    st.session_state["negotiation_result"] = NegotiationEngine(
        quantity=10,
        buyer_initial=700,
        buyer_maximum=900,
        seller_initial=1000,
        seller_minimum=850,
        buyer_concession=50,
        seller_concession=50,
        maximum_rounds=10,
    ).negotiate()
    st.session_state["negotiation_config"] = {
        "buyer_initial": 700,
        "seller_initial": 1000,
        "maximum_rounds": 10,
    }

with dashboard_col:
    result = st.session_state["negotiation_result"]
    config = st.session_state["negotiation_config"]
    history_df = pd.DataFrame(result["history"])
    agreed = result["status"] == "Agreement Reached"
    final_price = result["final_price"]
    last_round = history_df.iloc[-1]

    if active_view == "Dashboard":
        with st.container(key="dashboard_hero"):
            st.markdown(
                f"""
                <div class="hero-panel">
                  <div class="hero-eyebrow">SMART NEGOTIATION &bull; BETTER DECISIONS</div>
                  <div class="hero-title">DealMaker<span>Agent</span></div>
                  <div class="hero-subtitle">Simulate, analyze, and find the best possible deal with intelligent negotiation strategies.</div>
                  <div class="hero-badges"><span class="hero-badge">{lucide_icon("check", 12)} Rule-Based Engine</span><span class="hero-badge">{lucide_icon("history", 12)} Real-Time Analysis</span><span class="hero-badge">{lucide_icon("chart-line", 12)} Visual Insights</span><span class="hero-badge">{lucide_icon("circle-help", 12)} Decision Support</span></div>
                  <div class="hero-visual"><div class="party-chip">Buyer<strong>₹{config["buyer_initial"]:,.0f} → ₹{last_round["Buyer Offer"]:,.0f}</strong></div><div class="handshake-art">{lucide_icon("handshake", 58)}</div><div class="party-chip">Seller<strong>₹{config["seller_initial"]:,.0f} → ₹{last_round["Seller Offer"]:,.0f}</strong></div></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with st.container(key="workflow_strip"):
            final_step = "Agreement" if agreed else "Outcome"
            st.markdown(f'<div class="flowline"><span class="flow-step">Inputs</span><span class="flow-arrow">→</span><span class="flow-step">Negotiation</span><span class="flow-arrow">→</span><span class="flow-step">Analysis</span><span class="flow-arrow">→</span><span class="flow-step">{final_step}</span></div>', unsafe_allow_html=True)
    else:
        view_subtitles = {
            "Negotiation": "Configure terms and review the current negotiation rounds.",
            "Analytics": "Explore offer convergence and negotiation performance.",
            "History": "Review and export the complete round-by-round record.",
            "Help": "Understand the rule-based negotiation model.",
        }
        st.markdown(
            f'<div class="view-heading"><div class="hero-eyebrow">DEALMAKERAGENT / WORKSPACE</div><div class="view-title">{active_view}</div><div class="view-subtitle">{view_subtitles[active_view]}</div></div>',
            unsafe_allow_html=True,
        )

    if active_view in ("Dashboard", "Negotiation"):
        with st.container(key="summary_panel"):
            st.markdown(f'<div class="panel-title">{"Live deal overview" if active_view == "Dashboard" else "Negotiation outcome"}</div>', unsafe_allow_html=True)
            st.caption("Latest negotiation outcome")

            status_col, price_col, quantity_col, total_col, rounds_col = st.columns([1.6, 1, .8, 1.15, 1])
            with status_col:
                if agreed:
                    st.markdown(f'<div class="statusbar"><div class="statusicon">{lucide_icon("check", 24)}</div><div><div class="status-title">Agreement Reached!</div><div class="status-copy">Both buyer and seller agreed on the deal.</div></div></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="statusbar statusbar-error"><div class="statusicon" style="background:#dc2626">!</div><div><div class="status-title">No Agreement</div><div class="status-copy">The parties did not meet within the round limit.</div></div></div>', unsafe_allow_html=True)
            with price_col:
                st.metric("Final Price", f"₹{final_price:,.2f}" if agreed else "—", help="Agreed price per unit")
            with quantity_col:
                st.metric("Quantity", f"{result['quantity']:,}", help="Number of units")
            with total_col:
                st.metric("Total Amount", f"₹{result['total_amount']:,.2f}" if agreed else "—", help=f"₹{final_price:,.2f} × {result['quantity']:,}" if agreed else "No total without an agreement")
            with rounds_col:
                st.metric("Total Rounds", result["rounds"], help="Negotiation rounds completed")

    st.write("")
    chart_col, history_col = st.columns([1.25, 1], gap="medium")
    with chart_col:
        with st.container(border=True, key="chart_panel"):
            st.markdown(f'<div id="deal-analytics"></div><div class="panel-title">{lucide_icon("chart-line")} &nbsp; Negotiation Progress</div><div class="panel-subtitle">Buyer and seller offers across negotiation rounds</div>', unsafe_allow_html=True)
            figure, axis = plt.subplots(figsize=(7.4, 2.85))
            chart_background = "#141b2d" if dark_mode else "white"
            chart_text = "#a5b4cc" if dark_mode else "#66728d"
            chart_grid = "#2a3650" if dark_mode else "#e8edf5"
            buyer_annotation = "#60a5fa" if dark_mode else "#1d4ed8"
            seller_annotation = "#fdba74" if dark_mode else "#c2410c"
            figure.patch.set_facecolor(chart_background)
            axis.set_facecolor(chart_background)
            buyer_line, = axis.plot(history_df["Round"], history_df["Buyer Offer"], color="#2563eb", marker="o", linewidth=2.4, markersize=5, label="Buyer Offer")
            seller_line, = axis.plot(history_df["Round"], history_df["Seller Offer"], color="#f97316", marker="o", linewidth=2.4, markersize=5, label="Seller Offer")
            for round_value, offer in zip(history_df["Round"], history_df["Buyer Offer"]):
                if not (agreed and round_value == result["rounds"]):
                    axis.annotate(f"{offer:,.0f}", (round_value, offer), xytext=(0, -14), textcoords="offset points", ha="center", color=buyer_annotation, fontsize=7)
            for round_value, offer in zip(history_df["Round"], history_df["Seller Offer"]):
                if not (agreed and round_value == result["rounds"]):
                    axis.annotate(f"{offer:,.0f}", (round_value, offer), xytext=(0, 8), textcoords="offset points", ha="center", color=seller_annotation, fontsize=7)
            if agreed:
                axis.scatter([result["rounds"]], [final_price], color="#16a34a", edgecolor="white", linewidth=1.5, s=82, zorder=5, label="Agreement Point")
                axis.annotate(f"Agreement\n₹{final_price:,.0f}", (result["rounds"], final_price), xytext=(12, 16), textcoords="offset points", ha="center", color="white", fontsize=7, fontweight="bold", bbox={"boxstyle": "round,pad=.4", "fc": "#16a34a", "ec": "none"}, arrowprops={"arrowstyle": "-", "color": "#16a34a"})
            axis.set_xlabel("Negotiation round", color=chart_text)
            axis.set_ylabel("Price (₹)", color=chart_text)
            axis.set_xticks(history_df["Round"])
            offer_values = list(history_df["Buyer Offer"]) + list(history_df["Seller Offer"])
            price_padding = max((max(offer_values) - min(offer_values)) * .2, 20)
            axis.set_ylim(min(offer_values) - price_padding, max(offer_values) + price_padding)
            axis.grid(axis="y", color=chart_grid, linewidth=.8)
            axis.spines[["top", "right", "left"]].set_visible(False)
            axis.spines["bottom"].set_color(chart_grid)
            axis.tick_params(colors=chart_text, labelsize=8, length=0, pad=7)
            legend = axis.legend(handles=[buyer_line, seller_line] + ([axis.collections[-1]] if agreed else []), frameon=False, ncol=3, fontsize=7, loc="upper center", bbox_to_anchor=(.5, 1.2))
            for label in legend.get_texts():
                label.set_color(chart_text)
            figure.tight_layout(pad=.8)
            st.pyplot(figure, use_container_width=True)
            plt.close(figure)

    with history_col:
        with st.container(border=True, key="history_panel"):
            st.markdown('<div id="deal-history"></div>', unsafe_allow_html=True)
            history_title, download_col = st.columns([1.5, 1], vertical_alignment="center")
            with history_title:
                st.markdown(f'<div class="panel-title">{lucide_icon("history")} &nbsp; Negotiation History</div><div class="panel-subtitle">Round-wise offers and outcomes</div>', unsafe_allow_html=True)
            csv_data = history_df.to_csv(index=False).encode("utf-8")
            with download_col:
                st.download_button(
                    "↓ Download CSV",
                    data=csv_data,
                    file_name="negotiation_history.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
            table_rows = []
            for _, record in history_df.iterrows():
                status_class = "pill-agreement" if record["Status"] == "AGREEMENT" else "pill-counter"
                buyer_offer = f"₹{float(record['Buyer Offer']):,.0f}"
                seller_offer = f"₹{float(record['Seller Offer']):,.0f}"
                difference = f"₹{float(record['Difference']):,.0f}"
                table_rows.append(
                    f"<tr><td>{int(record['Round'])}</td><td class='table-number'>{buyer_offer}</td>"
                    f"<td class='table-number'>{seller_offer}</td><td class='table-number'>{difference}</td>"
                    f"<td><span class='pill {status_class}'>{record['Status']}</span></td></tr>"
                )
            history_table = (
                '<div class="history-table-wrap"><table class="history-table"><thead><tr>'
                '<th>Round</th><th>Buyer Offer</th><th>Seller Offer</th><th>Difference</th><th>Status</th>'
                '</tr></thead><tbody>' + "".join(table_rows) + '</tbody></table></div>'
            )
            st.markdown(history_table, unsafe_allow_html=True)

    st.write("")
    starting_buyer = config["buyer_initial"]
    starting_seller = config["seller_initial"]
    buyer_movement = float(last_round["Buyer Offer"]) - starting_buyer
    seller_reduction = starting_seller - float(last_round["Seller Offer"])
    price_reduction_percent = seller_reduction / starting_seller * 100
    buyer_movement_percent = buyer_movement / starting_buyer * 100
    maximum_rounds_value = config.get("maximum_rounds", 10)
    efficiency_badge = "FAST" if agreed and result["rounds"] < maximum_rounds_value else "COMPLETE"
    insight_cards = [
        ("trending-down", "red", "Price Reduction", f"₹{seller_reduction:,.2f}", f"From ₹{starting_seller:,.0f} to ₹{last_round['Seller Offer']:,.0f}", f"↓ {price_reduction_percent:.0f}%"),
        ("chart-line", "blue", "Buyer Gain", f"₹{buyer_movement:,.2f}", "Offer movement per unit", f"+{buyer_movement_percent:.1f}%"),
        ("wallet", "purple", "Deal Value", f"₹{result['total_amount']:,.2f}" if agreed else "No deal", "Total transaction value" if agreed else "No agreement reached", ""),
        ("zap", "indigo", "Negotiation Efficiency", f"{result['rounds']} Rounds", "Agreement reached" if agreed else "Round limit reached", efficiency_badge),
    ]
    insight_markup = '<div class="insight-grid">' + "".join(
        f'<div class="insight-card"><div class="insight-icon {icon_color}">{lucide_icon(icon, 20)}</div>'
        f'<div><div class="insight-label">{label}</div><div class="insight-value">{value}</div>'
        f'<div class="insight-caption">{caption}</div></div>'
        + (f'<div class="insight-badge">{badge}</div>' if badge else "")
        + '</div>'
        for icon, icon_color, label, value, caption, badge in insight_cards
    ) + '</div>'
    with st.container(key="analytics_cards_panel"):
        st.markdown(insight_markup, unsafe_allow_html=True)

st.caption("Decision support only. Offers are generated deterministically from the configured concession rules.")
with dashboard_col:
    with st.container(key="help_panel"):
        st.markdown('<div class="panel-title">Rule-Based Negotiation</div><div class="panel-subtitle">Transparent, deterministic decision support</div>', unsafe_allow_html=True)
        st.write("")
        st.markdown(
            "Buyer offers increase by the configured concession up to the buyer maximum. "
            "Seller prices decrease by the configured concession down to the seller minimum. "
            "An agreement is reached when the buyer offer meets or exceeds the seller offer. "
            "The final price and transaction total use the existing negotiation rules."
        )
