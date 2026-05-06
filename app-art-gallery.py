
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🎨 Art Gallery Dashboard",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

/* Hero Title */
.gallery-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.2rem;
    font-weight: 700;
    background: linear-gradient(90deg, #f7c59f, #eb9c70, #f4d03f);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.5px;
    line-height: 1.1;
    margin-bottom: 0.2rem;
}

.gallery-subtitle {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    color: #a89cc8;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

/* Metric Cards */
.metric-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    backdrop-filter: blur(10px);
    transition: transform 0.2s;
}
.metric-card:hover { transform: translateY(-3px); }
.metric-num {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    color: #f7c59f;
}
.metric-label {
    font-size: 0.78rem;
    color: #a89cc8;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.2rem;
}

/* Section Headers */
.section-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    color: #f7c59f;
    border-left: 4px solid #eb9c70;
    padding-left: 0.75rem;
    margin: 1.5rem 0 1rem 0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1535 0%, #0f0c29 100%);
    border-right: 1px solid rgba(247,197,159,0.15);
}
[data-testid="stSidebar"] * {
    color: #e8dff5 !important;
}

/* Inputs */
.stTextInput input, .stNumberInput input, .stSelectbox select {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(247,197,159,0.3) !important;
    border-radius: 10px !important;
    color: white !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #eb9c70, #f4d03f) !important;
    color: #1a1535 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.55rem 1.5rem !important;
    font-size: 0.95rem !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.1);
}

/* Search box */
.stTextInput > label { color: #a89cc8 !important; }

/* Divider */
hr {
    border: none;
    border-top: 1px solid rgba(247,197,159,0.15);
    margin: 1.5rem 0;
}

/* Success */
.stSuccess {
    background: rgba(80,200,120,0.15) !important;
    border: 1px solid rgba(80,200,120,0.3) !important;
    border-radius: 10px !important;
}

/* Period badge colors */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# ─── Sample Data ─────────────────────────────────────────────────────────────
SAMPLE_DATA = [
    {
        "Title": "Starry Night",
        "Artist": "Vincent van Gogh",
        "Year": 1889,
        "Medium": "Oil on canvas",
        "Price ($M)": 82.5,
        "Period": "Post-Impressionism",
        "Emoji": "🌌",
    },
    {
        "Title": "Mona Lisa",
        "Artist": "Leonardo da Vinci",
        "Year": 1503,
        "Medium": "Oil on poplar panel",
        "Price ($M)": 860.0,
        "Period": "Renaissance",
        "Emoji": "👩",
    },
    {
        "Title": "The Persistence of Memory",
        "Artist": "Salvador Dalí",
        "Year": 1931,
        "Medium": "Oil on canvas",
        "Price ($M)": 150.0,
        "Period": "Surrealism",
        "Emoji": "⏰",
    },
    {
        "Title": "Girl with a Pearl Earring",
        "Artist": "Johannes Vermeer",
        "Year": 1665,
        "Medium": "Oil on canvas",
        "Price ($M)": 30.0,
        "Period": "Baroque",
        "Emoji": "💎",
    },
    {
        "Title": "Water Lilies",
        "Artist": "Claude Monet",
        "Year": 1906,
        "Medium": "Oil on canvas",
        "Price ($M)": 54.0,
        "Period": "Impressionism",
        "Emoji": "🌸",
    },
]

PERIOD_COLORS = {
    "Post-Impressionism": "#eb9c70",
    "Renaissance":        "#f4d03f",
    "Surrealism":         "#c39bd3",
    "Baroque":            "#7ec8e3",
    "Impressionism":      "#82e0aa",
    "Modern":             "#f1948a",
    "Contemporary":       "#aab7b8",
    "Abstract":           "#f8c471",
    "Other":              "#d5dbdb",
}

PERIODS = list(PERIOD_COLORS.keys())

# ─── Session State ────────────────────────────────────────────────────────────
if "artworks" not in st.session_state:
    st.session_state.artworks = pd.DataFrame(SAMPLE_DATA)

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0;'>
        <div style='font-size:2.5rem;'>🖼️</div>
        <div style='font-family: Playfair Display, serif; font-size:1.3rem;
                    color:#f7c59f; font-weight:700; margin-top:0.3rem;'>
            Add Artwork
        </div>
        <div style='font-size:0.75rem; color:#7b6fa0; text-transform:uppercase;
                    letter-spacing:0.1em; margin-top:0.2rem;'>
            Expand your collection
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    title  = st.text_input("🎨 Title",          placeholder="e.g. The Scream")
    artist = st.text_input("👤 Artist",          placeholder="e.g. Edvard Munch")
    year   = st.number_input("📅 Year",          min_value=1000, max_value=datetime.now().year, value=2000, step=1)
    medium = st.text_input("🖌️ Medium",          placeholder="e.g. Tempera on cardboard")
    price  = st.number_input("💰 Price ($ millions)", min_value=0.0, value=10.0, step=0.5, format="%.1f")
    period = st.selectbox("🏛️ Art Period", PERIODS)
    emoji  = st.text_input("✨ Emoji", value="🖼️", max_chars=2)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("➕ Add to Gallery"):
        if title and artist and medium:
            new_row = pd.DataFrame([{
                "Title":      title,
                "Artist":     artist,
                "Year":       int(year),
                "Medium":     medium,
                "Price ($M)": price,
                "Period":     period,
                "Emoji":      emoji,
            }])
            st.session_state.artworks = pd.concat(
                [st.session_state.artworks, new_row], ignore_index=True
            )
            st.success(f"✅ '{title}' added!")
        else:
            st.error("Please fill in Title, Artist, and Medium.")

    st.markdown("---")
    if st.button("🔄 Reset to Sample Data"):
        st.session_state.artworks = pd.DataFrame(SAMPLE_DATA)
        st.success("Gallery reset!")

# ─── Main Area ────────────────────────────────────────────────────────────────
st.markdown('<div class="gallery-title">🎨 Art Gallery Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="gallery-subtitle">Curating Masterpieces · Visualizing Beauty · Discovering Art</div>', unsafe_allow_html=True)

df = st.session_state.artworks.copy()

# ── Metric Row ──────────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-num">{len(df)}</div>
        <div class="metric-label">🖼️ Total Artworks</div>
    </div>""", unsafe_allow_html=True)
with m2:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-num">{df['Artist'].nunique()}</div>
        <div class="metric-label">👤 Artists</div>
    </div>""", unsafe_allow_html=True)
with m3:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-num">${df['Price ($M)'].sum():.1f}M</div>
        <div class="metric-label">💰 Total Value</div>
    </div>""", unsafe_allow_html=True)
with m4:
    st.markdown(f"""<div class="metric-card">
        <div class="metric-num">{df['Period'].nunique()}</div>
        <div class="metric-label">🏛️ Art Periods</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Search ──────────────────────────────────────────────────────────────────
search = st.text_input("🔍 Search by Artist Name", placeholder="e.g. van Gogh, Monet …")
if search:
    filtered = df[df["Artist"].str.contains(search, case=False, na=False)]
else:
    filtered = df

# ── Artwork Table ────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🗂️ Collection</div>', unsafe_allow_html=True)

display_df = filtered[["Emoji","Title","Artist","Year","Medium","Period","Price ($M)"]].copy()
display_df["Price ($M)"] = display_df["Price ($M)"].apply(lambda x: f"${x:.1f}M")
display_df = display_df.rename(columns={"Emoji": ""})

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    height=min(400, 60 + len(filtered)*40),
)

if search and len(filtered) == 0:
    st.info("🔍 No artworks found for that artist.")

# ── Charts ──────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col_bar, col_pie = st.columns([3, 2], gap="large")

CHART_BG    = "rgba(0,0,0,0)"
FONT_COLOR  = "#e8dff5"
GRID_COLOR  = "rgba(255,255,255,0.07)"

with col_bar:
    st.markdown('<div class="section-header">💰 Artwork Prices</div>', unsafe_allow_html=True)

    chart_df = filtered.sort_values("Price ($M)", ascending=True).tail(10)
    colors   = [PERIOD_COLORS.get(p, "#eb9c70") for p in chart_df["Period"]]

    fig_bar = go.Figure(go.Bar(
        x=chart_df["Price ($M)"],
        y=chart_df["Title"],
        orientation="h",
        marker=dict(
            color=colors,
            line=dict(width=0),
            opacity=0.9,
        ),
        text=[f"${v:.1f}M" for v in chart_df["Price ($M)"]],
        textposition="outside",
        textfont=dict(color=FONT_COLOR, size=11),
        hovertemplate="<b>%{y}</b><br>$%{x:.1f}M<extra></extra>",
    ))
    fig_bar.update_layout(
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        font=dict(color=FONT_COLOR, family="DM Sans"),
        xaxis=dict(
            showgrid=True, gridcolor=GRID_COLOR,
            tickprefix="$", ticksuffix="M",
            color=FONT_COLOR,
        ),
        yaxis=dict(showgrid=False, color=FONT_COLOR),
        margin=dict(l=10, r=60, t=10, b=10),
        height=320,
        showlegend=False,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_pie:
    st.markdown('<div class="section-header">🏛️ By Period</div>', unsafe_allow_html=True)

    period_counts = filtered["Period"].value_counts().reset_index()
    period_counts.columns = ["Period", "Count"]
    pie_colors = [PERIOD_COLORS.get(p, "#aab7b8") for p in period_counts["Period"]]

    fig_pie = go.Figure(go.Pie(
        labels=period_counts["Period"],
        values=period_counts["Count"],
        marker=dict(colors=pie_colors, line=dict(color="#0f0c29", width=2)),
        textinfo="label+percent",
        textfont=dict(color=FONT_COLOR, size=11),
        hole=0.45,
        hovertemplate="<b>%{label}</b><br>%{value} artworks<extra></extra>",
    ))
    fig_pie.update_layout(
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        font=dict(color=FONT_COLOR, family="DM Sans"),
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        height=320,
        annotations=[dict(
            text=f"<b>{len(filtered)}</b><br>works",
            x=0.5, y=0.5,
            font=dict(size=14, color=FONT_COLOR, family="Playfair Display, serif"),
            showarrow=False,
        )],
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Timeline Scatter ─────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📅 Timeline of Masterpieces</div>', unsafe_allow_html=True)

fig_scatter = go.Figure()
for period in filtered["Period"].unique():
    sub = filtered[filtered["Period"] == period]
    fig_scatter.add_trace(go.Scatter(
        x=sub["Year"],
        y=sub["Price ($M)"],
        mode="markers+text",
        name=period,
        marker=dict(
            color=PERIOD_COLORS.get(period, "#aab7b8"),
            size=sub["Price ($M)"].apply(lambda v: max(10, min(v / 10 + 10, 50))),
            opacity=0.85,
            line=dict(width=1.5, color="rgba(255,255,255,0.3)"),
        ),
        text=sub["Emoji"],
        textposition="middle center",
        textfont=dict(size=14),
        customdata=sub[["Title","Artist","Medium"]].values,
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "👤 %{customdata[1]}<br>"
            "📅 %{x}<br>"
            "💰 $%{y:.1f}M<br>"
            "🖌️ %{customdata[2]}<extra></extra>"
        ),
    ))

fig_scatter.update_layout(
    paper_bgcolor=CHART_BG,
    plot_bgcolor=CHART_BG,
    font=dict(color=FONT_COLOR, family="DM Sans"),
    xaxis=dict(showgrid=True, gridcolor=GRID_COLOR, color=FONT_COLOR, title="Year"),
    yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, color=FONT_COLOR,
               title="Price ($M)", tickprefix="$", ticksuffix="M"),
    legend=dict(
        bgcolor="rgba(255,255,255,0.05)",
        bordercolor="rgba(255,255,255,0.1)",
        borderwidth=1,
        font=dict(color=FONT_COLOR, size=11),
    ),
    height=380,
    margin=dict(l=10, r=10, t=10, b=10),
    hovermode="closest",
)
st.plotly_chart(fig_scatter, use_container_width=True)

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<hr>
<div style='text-align:center; color:#4a3f6b; font-size:0.8rem; padding: 0.5rem 0 1.5rem;'>
    🎨 Art Gallery Dashboard · Built with Streamlit & Plotly
</div>
""", unsafe_allow_html=True)
