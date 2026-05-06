
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import random

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SNS Marketing Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background: #0a0e1a; }

.hero-wrap {
    background: linear-gradient(120deg, #0d1b3e 0%, #0a0e1a 50%, #1a0d3e 100%);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative; overflow: hidden;
}
.hero-wrap::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 80% 50%, rgba(99,102,241,0.12) 0%, transparent 60%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem; font-weight: 700; color: #fff;
    margin: 0 0 0.3rem; letter-spacing: -0.5px;
}
.hero-sub { font-size: 0.88rem; color: #6b7280; letter-spacing: 0.08em; text-transform: uppercase; }
.hero-badge {
    display: inline-block;
    background: rgba(99,102,241,0.15); border: 1px solid rgba(99,102,241,0.35);
    color: #a5b4fc; font-size: 0.72rem; font-weight: 600;
    padding: 3px 10px; border-radius: 20px;
    letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 0.6rem;
}

.camp-row {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px; padding: 0.9rem 1.2rem; margin-bottom: 0.5rem;
}
.camp-good { border-left: 4px solid #10b981 !important; }
.camp-ok   { border-left: 4px solid #f59e0b !important; }
.camp-bad  { border-left: 4px solid #ef4444 !important; }

.plat-badge { font-size: 0.7rem; font-weight: 600; padding: 2px 8px; border-radius: 6px; letter-spacing: 0.05em; }
.plat-instagram { background: rgba(225,48,108,0.15); color: #f472b6; }
.plat-tiktok    { background: rgba(0,242,234,0.1);   color: #5eead4; }
.plat-youtube   { background: rgba(255,0,0,0.12);    color: #f87171; }

[data-testid="stSidebar"] {
    background: #0d1117 !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
[data-testid="stSidebar"] .stMarkdown h3 { color: #a5b4fc !important; font-family: 'Space Grotesk', sans-serif !important; }

.stTextInput input, .stNumberInput input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important; color: #f1f5f9 !important;
}
.stSelectbox > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important; color: #f1f5f9 !important;
}
label { color: #9ca3af !important; font-size: 0.82rem !important; }

.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: #fff !important; border: none !important;
    border-radius: 10px !important; font-weight: 600 !important;
    width: 100% !important; padding: 0.6rem !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 14px !important; padding: 1rem 1.2rem !important;
}
[data-testid="stMetricLabel"] { color: #9ca3af !important; font-size: 0.78rem !important; }
[data-testid="stMetricValue"] { color: #f1f5f9 !important; font-size: 1.6rem !important; font-weight: 700 !important; }
[data-testid="stMetricDelta"] { font-size: 0.8rem !important; }

.sec-header {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem; font-weight: 600; color: #e2e8f0;
    border-left: 3px solid #6366f1; padding-left: 0.7rem; margin: 1.8rem 0 1rem;
}
hr { border: none; border-top: 1px solid rgba(255,255,255,0.07); margin: 1.2rem 0; }
</style>
""", unsafe_allow_html=True)

# ─── Helpers ─────────────────────────────────────────────────────────────────
PLATFORM_EMOJI = {"Instagram": "📸", "TikTok": "🎵", "YouTube": "▶️"}
PLATFORM_CLASS = {"Instagram": "plat-instagram", "TikTok": "plat-tiktok", "YouTube": "plat-youtube"}
CAMP_COLORS    = ["#6366f1", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4"]

def hex_to_rgba(hex_color, alpha=0.1):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f"rgba({r},{g},{b},{alpha})"

def calc_engagement(followers, likes, comments, shares):
    if followers == 0: return 0.0
    return round((likes + comments + shares) / followers * 100, 2)

def calc_roi(budget, likes, shares, comments):
    if budget == 0: return 0.0
    value = likes * 0.5 + shares * 2.0 + comments * 1.0
    return round((value - budget) / budget * 100, 1)

def roi_tier(roi):
    if roi >= 20:  return "camp-good"
    if roi >= 0:   return "camp-ok"
    return              "camp-bad"

def gen_weekly(base_eng, base_roi, seed=42, weeks=8):
    rng   = np.random.default_rng(seed)
    dates = [datetime.today() - timedelta(weeks=weeks-1-i) for i in range(weeks)]
    eng   = np.clip(base_eng + rng.uniform(-1.5, 1.5, weeks), 0, None).tolist()
    roi   = (base_roi + rng.uniform(-10, 10, weeks)).tolist()
    return dates, eng, roi

# ─── Sample Data ─────────────────────────────────────────────────────────────
SAMPLE = [
    dict(name="Summer Glow ☀️",  platform="Instagram", budget=3000,
         followers=85000,  likes=12400, shares=980,  comments=670),
    dict(name="Viral Dance 💃",   platform="TikTok",   budget=1500,
         followers=210000, likes=88000, shares=14200, comments=5300),
    dict(name="Deep Dive 🎬",     platform="YouTube",  budget=8000,
         followers=42000,  likes=3100,  shares=420,  comments=890),
]

if "campaigns" not in st.session_state:
    rows = []
    for s in SAMPLE:
        eng = calc_engagement(s["followers"], s["likes"], s["comments"], s["shares"])
        roi = calc_roi(s["budget"], s["likes"], s["shares"], s["comments"])
        rows.append({**s, "engagement": eng, "roi": roi})
    st.session_state.campaigns = rows

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ➕ New Campaign")
    camp_name = st.text_input("Campaign Name", placeholder="e.g. Summer Sale 🔥")
    platform  = st.selectbox("Platform", ["Instagram", "TikTok", "YouTube"])
    budget    = st.number_input("Budget ($)",   min_value=0, value=2000, step=100)
    followers = st.number_input("Followers",    min_value=0, value=50000, step=1000)
    likes     = st.number_input("Likes",        min_value=0, value=4000,  step=100)
    shares    = st.number_input("Shares",       min_value=0, value=500,   step=50)
    comments  = st.number_input("Comments",     min_value=0, value=300,   step=50)

    # Live preview
    prev_eng = calc_engagement(followers, likes, comments, shares)
    prev_roi = calc_roi(budget, likes, shares, comments)
    st.markdown(f"""
    <div style='background:rgba(99,102,241,0.08); border:1px solid rgba(99,102,241,0.2);
                border-radius:10px; padding:0.8rem 1rem; margin:0.8rem 0; font-size:0.82rem;'>
        <div style='color:#a5b4fc; font-weight:600; margin-bottom:0.4rem;'>⚡ Live Preview</div>
        <div style='color:#e2e8f0;'>Engagement: <b>{prev_eng:.2f}%</b></div>
        <div style='color:#e2e8f0;'>ROI: <b style="color:{"#10b981" if prev_roi>=20 else "#f59e0b" if prev_roi>=0 else "#ef4444"}">{prev_roi:.1f}%</b></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🚀 Add Campaign"):
        if camp_name.strip():
            eng = calc_engagement(followers, likes, comments, shares)
            roi = calc_roi(budget, likes, shares, comments)
            st.session_state.campaigns.append({
                "name": camp_name, "platform": platform, "budget": budget,
                "followers": followers, "likes": likes, "shares": shares,
                "comments": comments, "engagement": eng, "roi": roi,
            })
            st.success(f"✅ '{camp_name}' added!")
        else:
            st.error("Please enter a campaign name.")

    st.markdown("---")
    if st.button("🔄 Reset to Sample Data"):
        rows = []
        for s in SAMPLE:
            eng = calc_engagement(s["followers"], s["likes"], s["comments"], s["shares"])
            roi = calc_roi(s["budget"], s["likes"], s["shares"], s["comments"])
            rows.append({**s, "engagement": eng, "roi": roi})
        st.session_state.campaigns = rows
        st.success("Reset!")

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.75rem; color:#4b5563; line-height:1.8;'>
    <b style='color:#6366f1;'>Engagement Rate</b><br>
    (Likes + Comments + Shares) ÷ Followers × 100<br><br>
    <b style='color:#6366f1;'>ROI</b><br>
    (Value − Budget) ÷ Budget × 100<br>
    <span style='color:#374151;'>Value = Like×0.5 + Share×2 + Comment×1</span><br><br>
    <b style='color:#10b981;'>🟢 Good</b> ROI ≥ 20% &nbsp;
    <b style='color:#f59e0b;'>🟡 OK</b> ROI ≥ 0%<br>
    <b style='color:#ef4444;'>🔴 Bad</b> ROI &lt; 0%
    </div>
    """, unsafe_allow_html=True)

# ─── Main ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
  <div class="hero-badge">📊 Analytics Dashboard</div>
  <div class="hero-title">SNS Marketing Analytics</div>
  <div class="hero-sub">Campaign Performance · Engagement · ROI Tracking</div>
</div>
""", unsafe_allow_html=True)

camps = st.session_state.campaigns
df    = pd.DataFrame(camps)

# ── KPI Metrics ───────────────────────────────────────────────────────────────
total_budget = df["budget"].sum()
avg_eng      = df["engagement"].mean()
avg_roi      = df["roi"].mean()
best_idx     = df["roi"].idxmax()
best_camp    = df.loc[best_idx, "name"] if len(df) else "—"

m1, m2, m3, m4 = st.columns(4)
with m1: st.metric("💰 Total Budget",   f"${total_budget:,.0f}",  f"+${total_budget*0.13:,.0f} vs prev")
with m2: st.metric("💬 Avg Engagement", f"{avg_eng:.2f}%",        f"+{avg_eng*0.09:.2f}%")
with m3: st.metric("📈 Avg ROI",        f"{avg_roi:.1f}%",        f"+{avg_roi*0.22:.1f}%")
with m4: st.metric("🏆 Best Campaign",  (best_camp[:16]+"…") if len(best_camp)>16 else best_camp, "Top performer")

# ── Campaign Cards ────────────────────────────────────────────────────────────
st.markdown('<div class="sec-header">📋 Campaign Overview</div>', unsafe_allow_html=True)

for idx, c in enumerate(camps):
    row_cls  = roi_tier(c["roi"])
    plat_cls = PLATFORM_CLASS[c["platform"]]
    emoji    = PLATFORM_EMOJI[c["platform"]]
    roi_col  = "#10b981" if c["roi"] >= 20 else "#f59e0b" if c["roi"] >= 0 else "#ef4444"

    col_info, col_e, col_r, col_b, col_l = st.columns([3, 1.4, 1.4, 1.4, 1.4])

    with col_info:
        st.markdown(f"""
        <div class="camp-row {row_cls}">
            <span style="font-size:0.95rem;font-weight:600;color:#f1f5f9;">{emoji} {c['name']}</span>
            &nbsp;<span class="plat-badge {plat_cls}">{c['platform']}</span>
            <div style="font-size:0.75rem;color:#6b7280;margin-top:0.3rem;">
                👥 {c['followers']:,} followers &nbsp;|&nbsp;
                <span style="color:{roi_col};font-weight:600;">ROI {c['roi']:+.1f}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_e:
        st.metric("Engagement", f"{c['engagement']:.2f}%")
    with col_r:
        st.metric("ROI", f"{c['roi']:+.1f}%")
    with col_b:
        st.metric("Budget", f"${c['budget']:,}")
    with col_l:
        st.metric("❤️ Likes", f"{c['likes']:,}")

# ── Weekly Performance Charts ─────────────────────────────────────────────────
BG   = "rgba(0,0,0,0)"
FONT = "#9ca3af"
GRID = "rgba(255,255,255,0.05)"

st.markdown('<div class="sec-header">📈 Weekly Performance Trends</div>', unsafe_allow_html=True)
tab_eng, tab_roi = st.tabs(["📊 Engagement Rate (%)", "💹 ROI (%)"])

with tab_eng:
    fig = go.Figure()
    for idx, c in enumerate(camps):
        dates, eng_vals, _ = gen_weekly(c["engagement"], c["roi"], seed=idx*7)
        col = CAMP_COLORS[idx % len(CAMP_COLORS)]
        fig.add_trace(go.Scatter(
            x=dates, y=eng_vals, mode="lines+markers", name=c["name"],
            line=dict(color=col, width=2.5, shape="spline"),
            marker=dict(size=6, color=col, line=dict(color="#0a0e1a", width=1.5)),
            fill="tozeroy",
            fillcolor=hex_to_rgba(col, 0.1),
            hovertemplate=f"<b>{c['name']}</b><br>%{{x|%b %d}}: %{{y:.2f}}%<extra></extra>",
        ))
    fig.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG, font=dict(color=FONT, family="Inter"),
        xaxis=dict(showgrid=True, gridcolor=GRID, color=FONT, tickformat="%b %d"),
        yaxis=dict(showgrid=True, gridcolor=GRID, color=FONT, ticksuffix="%"),
        legend=dict(bgcolor="rgba(0,0,0,0.3)", bordercolor="rgba(255,255,255,0.05)",
                    borderwidth=1, font=dict(color="#e2e8f0", size=11)),
        height=360, margin=dict(l=10, r=10, t=20, b=10), hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True)

with tab_roi:
    fig2 = go.Figure()
    for idx, c in enumerate(camps):
        dates, _, roi_vals = gen_weekly(c["engagement"], c["roi"], seed=idx*7)
        col = CAMP_COLORS[idx % len(CAMP_COLORS)]
        fig2.add_trace(go.Scatter(
            x=dates, y=roi_vals, mode="lines+markers", name=c["name"],
            line=dict(color=col, width=2.5, shape="spline"),
            marker=dict(size=6, color=col, line=dict(color="#0a0e1a", width=1.5)),
            hovertemplate=f"<b>{c['name']}</b><br>%{{x|%b %d}}: %{{y:.1f}}%<extra></extra>",
        ))
    fig2.add_hline(y=0,  line=dict(color="#ef4444", width=1.5, dash="dot"),
                   annotation_text="Break-even (0%)", annotation_font_color="#ef4444",
                   annotation_position="bottom right")
    fig2.add_hline(y=20, line=dict(color="#10b981", width=1.5, dash="dot"),
                   annotation_text="Good ROI (20%)", annotation_font_color="#10b981",
                   annotation_position="top right")
    fig2.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG, font=dict(color=FONT, family="Inter"),
        xaxis=dict(showgrid=True, gridcolor=GRID, color=FONT, tickformat="%b %d"),
        yaxis=dict(showgrid=True, gridcolor=GRID, color=FONT, ticksuffix="%"),
        legend=dict(bgcolor="rgba(0,0,0,0.3)", bordercolor="rgba(255,255,255,0.05)",
                    borderwidth=1, font=dict(color="#e2e8f0", size=11)),
        height=360, margin=dict(l=10, r=10, t=20, b=10), hovermode="x unified",
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── Platform & Bubble Charts ──────────────────────────────────────────────────
st.markdown('<div class="sec-header">🌐 Platform Breakdown</div>', unsafe_allow_html=True)
col_bar, col_sc = st.columns(2, gap="large")

PCOLORS = {"Instagram": "#f472b6", "TikTok": "#5eead4", "YouTube": "#f87171"}

with col_bar:
    plat_df = df.groupby("platform").agg(avg_eng=("engagement","mean")).reset_index()
    fig_b = go.Figure(go.Bar(
        x=plat_df["platform"],
        y=plat_df["avg_eng"],
        marker_color=[PCOLORS.get(p,"#6366f1") for p in plat_df["platform"]],
        marker_opacity=0.85,
        text=[f"{v:.2f}%" for v in plat_df["avg_eng"]],
        textposition="outside",
        textfont=dict(color="#e2e8f0"),
        hovertemplate="<b>%{x}</b><br>Avg Engagement: %{y:.2f}%<extra></extra>",
    ))
    fig_b.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG, showlegend=False,
        font=dict(color=FONT, family="Inter"),
        xaxis=dict(showgrid=False, color=FONT),
        yaxis=dict(showgrid=True, gridcolor=GRID, color=FONT, ticksuffix="%"),
        height=300, margin=dict(l=10, r=10, t=40, b=10),
        title=dict(text="Avg Engagement by Platform", font=dict(color="#e2e8f0", size=13)),
    )
    st.plotly_chart(fig_b, use_container_width=True)

with col_sc:
    fig_s = go.Figure()
    for idx, c in enumerate(camps):
        col = CAMP_COLORS[idx % len(CAMP_COLORS)]
        fig_s.add_trace(go.Scatter(
            x=[c["engagement"]], y=[c["roi"]],
            mode="markers+text",
            name=c["name"],
            text=[PLATFORM_EMOJI[c["platform"]]],
            textposition="middle center",
            textfont=dict(size=16),
            marker=dict(
                size=max(22, min(c["budget"]/180, 55)),
                color=col, opacity=0.8,
                line=dict(width=2, color="rgba(255,255,255,0.2)"),
            ),
            customdata=[[c["name"], c["platform"], c["budget"]]],
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Platform: %{customdata[1]}<br>"
                "Engagement: %{x:.2f}%<br>"
                "ROI: %{y:.1f}%<br>"
                "Budget: $%{customdata[2]:,}<extra></extra>"
            ),
        ))
    fig_s.add_hline(y=0,  line=dict(color="#ef4444", width=1, dash="dot"))
    fig_s.add_hline(y=20, line=dict(color="#10b981", width=1, dash="dot"),
                    annotation_text="Good ROI", annotation_font_color="#10b981")
    fig_s.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG,
        font=dict(color=FONT, family="Inter"),
        xaxis=dict(showgrid=True, gridcolor=GRID, color=FONT,
                   title="Engagement Rate (%)", ticksuffix="%"),
        yaxis=dict(showgrid=True, gridcolor=GRID, color=FONT,
                   title="ROI (%)", ticksuffix="%"),
        legend=dict(bgcolor="rgba(0,0,0,0.3)", font=dict(color="#e2e8f0", size=10)),
        height=300, margin=dict(l=10, r=10, t=40, b=10),
        title=dict(text="Engagement vs ROI  (size = budget)", font=dict(color="#e2e8f0", size=13)),
        showlegend=False,
    )
    st.plotly_chart(fig_s, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<hr>
<div style='text-align:center; color:#1f2937; font-size:0.78rem; padding-bottom:1rem;'>
    📊 SNS Marketing Analytics · Built with Streamlit & Plotly
</div>
""", unsafe_allow_html=True)
