import streamlit as st
import pandas as pd

# --- SETTING BA TELEFONE HOTU ---
st.set_page_config(
    page_title="ANALIZA TIMOR 2026",
    page_icon="🇹🇱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CSS: Halo diak ba ekran kiik ---
st.markdown("""
<style>
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
        padding-left: 0.7rem !important;
        padding-right: 0.7rem !important;
        max-width: 100% !important;
    }
    h1 { font-size: 26px !important; text-align: center; }
    h3 { font-size: 18px !important; }
    div[data-testid="stMetric"] {
        background: #1E1E1E;
        border-radius: 14px;
        padding: 10px;
        border: 1px solid #333;
    }
    div[data-testid="stMetric"] label { font-size: 12px !important; color: #AAA !important; }
    div[data-testid="stMetric"] div { font-size: 22px !important; }
    .stButton > button {
        width: 100% !important;
        height: 52px !important;
        font-size: 18px !important;
        border-radius: 14px !important;
        background: #FF4B4B !important;
        color: white !important;
        border: none !important;
    }
    .stSelectbox > div > div { font-size: 16px !important; }
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("# 🇹🇱 ANALIZA TIMOR 2026")
st.markdown("<p style='text-align:center; color:grey; margin-top:-15px;'>Dashboard Realtime • Bele loke iha Telefone hotu</p>", unsafe_allow_html=True)

# --- DADUS ---
df = pd.DataFrame({
    "Municipiu": ["Dili", "Baucau", "Ermera", "Bobonaro", "Covalima", "Viqueque", "Aileu", "Ainaro"],
    "Total": [120, 85, 65, 50, 45, 40, 32, 28],
    "Aktivo": [90, 60, 45, 35, 30, 28, 22, 20]
})

# --- KARTAUN 2x2 - Diak ba telefone ---
c1, c2 = st.columns(2)
c1.metric("📦 Total Dadus", f"{df['Total'].sum()}")
c2.metric("✅ Aktivo", f"{df['Aktivo'].sum()}")

c3, c4 = st.columns(2)
c3.metric("📍 Municipiu", "8")
c4.metric("🕒 Update", "Agora")

st.divider()

# --- FILTER ---
st.subheader("🔍 Hili Municipiu")
hili = st.selectbox("Hili:", ["Hotu-hotu"] + list(df["Municipiu"]), label_visibility="collapsed")
df_show = df if hili == "Hotu-hotu" else df[df["Municipiu"] == hili]

# --- TABELA ---
st.subheader("📋 Tabela Dadus")
st.dataframe(df_show, use_container_width=True, hide_index=True)

# --- GRAFIKU - Uza Streamlit nian deit, kmaan ---
st.subheader("📊 Grafiku Total")
st.bar_chart(df_show.set_index("Municipiu")["Total"], use_container_width=True)

st.subheader("📈 Grafiku Aktivo")
st.line_chart(df_show.set_index("Municipiu")["Aktivo"], use_container_width=True)

# --- BUTAUN ---
if st.button("🔄 Refresh Dadus"):
    st.rerun()

st.success("✅ Diak ona! Bele loke iha Android no iPhone hotu.")
st.caption("Dili • Baucau • Ermera • Bobonaro • Covalima • Viqueque")
