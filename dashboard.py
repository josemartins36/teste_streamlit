import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Diabetes", layout="wide", page_icon="🩺")
st.title("🩺 Dashboard Interativo - Predição de Diabetes")

# === Carregar dados ===
@st.cache_data
def load_data():
    return pd.read_csv("diabetes_prediction_dataset.csv")

df = load_data()

# === Sidebar ===
st.sidebar.header("🎛️ Filtros Interativos")

# Filtro por gênero
genero = st.sidebar.selectbox("Gênero", ["Todos"] + sorted(df["gender"].unique().tolist()))
# Filtro por tabagismo
fumante = st.sidebar.multiselect("Histórico de tabagismo", df["smoking_history"].unique().tolist())
# Filtro por idade
idade = st.sidebar.slider("Idade (anos)", int(df["age"].min()), int(df["age"].max()), (20, 60))
# Mostrar correlação
mostrar_correlacao = st.sidebar.checkbox("Mostrar matriz de correlação", value=False)

# === Aplicar filtros ===
df_filtro = df.copy()

if genero != "Todos":
    df_filtro = df_filtro[df_filtro["gender"] == genero]

if fumante:
    df_filtro = df_filtro[df_filtro["smoking_history"].isin(fumante)]

df_filtro = df_filtro[(df_filtro["age"] >= idade[0]) & (df_filtro["age"] <= idade[1])]

# === Métricas ===
col1, col2, col3 = st.columns(3)
col1.metric("📊 Total de Registros", len(df_filtro))
col2.metric("🧪 Casos de Diabetes", df_filtro["diabetes"].sum())
col3.metric("💯 % com Diabetes", f"{100 * df_filtro['diabetes'].mean():.1f}%")

st.divider()

# === Gráfico 1: Histograma por faixa etária ===
st.subheader("📈 Distribuição por Faixa Etária")
df_filtro["faixa"] = pd.cut(df_filtro["age"], bins=[0,20,40,60,80,120], labels=["0-20","21-40","41-60","61-80","81+"])
fig1 = px.histogram(df_filtro, x="faixa", color="diabetes", barmode="group", text_auto=True)
st.plotly_chart(fig1, use_container_width=True)

# === Gráfico 2: Dispersão IMC vs Glicose ===
st.subheader("📉 Relação IMC × Nível de Glicose")
fig2 = px.scatter(df_filtro, x="bmi", y="blood_glucose_level", color="diabetes",
                  hover_data=["age", "gender", "hypertension"], symbol="gender")
st.plotly_chart(fig2, use_container_width=True)

# === Gráfico 3: Proporção de diabetes por gênero ===
st.subheader("🚻 Proporção de Diabetes por Gênero")
proporcao = df_filtro.groupby("gender")["diabetes"].mean().reset_index()
fig3 = px.bar(proporcao, x="gender", y="diabetes", text="diabetes", color="gender")
fig3.update_layout(yaxis_tickformat=".0%")
st.plotly_chart(fig3, use_container_width=True)

# === Correlação (opcional) ===
if mostrar_correlacao:
    st.subheader("📊 Matriz de Correlação")
    corr = df_filtro.drop(columns=["gender", "smoking_history"]).corr()
    fig_corr, ax = plt.subplots(figsize=(8,6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig_corr)

# === Tabela ===
st.subheader("🗃️ Dados filtrados")
st.dataframe(df_filtro, use_container_width=True)

st.caption("📌 Use os filtros no menu lateral para personalizar sua análise.")

