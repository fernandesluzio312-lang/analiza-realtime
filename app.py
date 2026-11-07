import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIG MODERNU 2026 ---
st.set_page_config(page_title="ANALIZA TIMOR 2026", page_icon="🇹🇱", layout="wide")

# CSS Glassmorphism + Dark Modern
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); color: white; }
div[data-testid="metric"] { background: rgba(255,255,255,0.08); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.15); padding: 15px; border-radius: 16px; }
div[data-testid="stSidebar"] { background: #0B1220; }
h1, h2, h3 { color: white !important; }
</style>
""", unsafe_allow_html=True)

# --- LOAD DADUS REAL-TIME ---
sheet_id = "1fQ7agr0N6J9qjsp28zD7ALoL_LDQ9df5j4QJUYZboB4"
url_prod = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=PRODUTU"
url_vendas = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=VENDAS"

@st.cache_data(ttl=60)
def load():
    p = pd.read_csv(url_prod)
    v = pd.read_csv(url_vendas)
    v['Data'] = pd.to_datetime(v['Data'])
    return p, v

df_prod, df_v = load()

# --- HEADER ---
st.markdown("### 🇹🇱 ANALIZA TIMOR 2026")
st.title("Dashboard E-Commerce Real-Time")
st.caption("HP Timor • Tais Timor • Dadus husi Google Sheets - Update Otomatiku")

# --- SIDEBAR FILTER MODERNU ---
st.sidebar.header("🎛️ Filter")
loja = st.sidebar.multiselect("Hili Loja", df_v['Loja'].unique(), default=df_v['Loja'].unique())
distritu = st.sidebar.multiselect("Hili Distritu", df_v['Distritu'].unique(), default=df_v['Distritu'].unique())
search = st.sidebar.text_input("🔍 Buka Produtu")

df_f = df_v[(df_v['Loja'].isin(loja)) & (df_v['Distritu'].isin(distritu))]
if search:
    df_f = df_f[df_f['Produtu'].str.contains(search, case=False, na=False)]

# --- KPI CARDS ---
total = df_f['Total'].sum()
orders = len(df_f)
avg = total / orders if orders else 0
stock_low = len(df_prod[df_prod['Stock'] < 15])

c1,c2,c3,c4 = st.columns(4)
c1.metric("💰 Total Vendas", f"${total:,.0f}", "+12% vs semana kotuk")
c2.metric("🧾 Total Order", orders)
c3.metric("📦 Produtu Ativu", len(df_prod))
c4.metric("⚠️ Stock Badak", stock_low, delta_color="inverse")

# --- TABS MODERNU ---
tab1, tab2, tab3 = st.tabs(["📈 Analiza", "🛍️ Produtu", "📥 Dadus"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Vendas Lor-Loron")
        daily = df_f.groupby(df_f['Data'].dt.date)['Total'].sum().reset_index()
        fig = px.area(daily, x='Data', y='Total', color_discrete_sequence=['#00E5FF'])
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("Vendas Tuir Loja")
        by_loja = df_f.groupby('Loja')['Total'].sum().reset_index()
        fig2 = px.bar(by_loja, x='Loja', y='Total', color='Loja', color_discrete_sequence=['#FF6B6B','#4ECDC4'])
        fig2.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Top 5 Produtu Mais Fa'an")
        top = df_f.groupby('Produtu')['Qty'].sum().sort_values(ascending=False).head(5).reset_index()
        fig3 = px.bar(top, x='Qty', y='Produtu', orientation='h', color='Qty', color_continuous_scale='Viridis')
        fig3.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig3, use_container_width=True)
    with col4:
        st.subheader("Vendas Tuir Distritu")
        by_dist = df_f.groupby('Distritu')['Total'].sum().reset_index()
        fig4 = px.pie(by_dist, values='Total', names='Distritu', hole=0.5)
        fig4.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig4, use_container_width=True)

with tab2:
    st.subheader("Katalogu Produtu - Stock Live")
    st.dataframe(df_prod, use_container_width=True, hide_index=True)
    st.warning(f"⚠️ Produtu {stock_low} mak stock menus husi 15 - presiza restock lalais!")

with tab3:
    st.subheader("Tabela Vendas Detallu")
    st.dataframe(df_f, use_container_width=True, hide_index=True)
    st.download_button("⬇️ Download CSV Vendas", df_f.to_csv(index=False), "vendas-timor.csv", "text/csv")

st.caption("© 2026 Analiza Timor - Halo husi Timor-Leste 🇹🇱")
