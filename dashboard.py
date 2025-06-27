import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Interativo - Diabetes", layout="wide")
st.title("📊 Dashboard Interativo: Predição de Diabetes")

# --- Carregar e preparar dados ---
@st.cache_data
def load_data():
    df = pd.read_csv("diabetes_prediction_dataset.csv")
    df['age'] = df['age'].astype(int)

    # Agrupar em faixas etárias
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 100]
    labels = [f"{i}-{i+9}" for i in bins[:-1]]
    df['faixa_etaria'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)

    return df

df = load_data()

# --- Sidebar ---
st.sidebar.header("🔧 Controles")

visualizacao = st.sidebar.radio("Tipo de gráfico:", ["📈 Coordenadas Paralelas", "🎞️ Dispersão Animada"])

grupo = st.sidebar.radio("Grupo:", ["Todos", "Apenas Diabéticos", "Apenas Não Diabéticos"])

# --- Filtragem de dados ---
if grupo == "Apenas Diabéticos":
    df_filtrado = df[df["diabetes"] == 1]
elif grupo == "Apenas Não Diabéticos":
    df_filtrado = df[df["diabetes"] == 0]
else:
    df_filtrado = df

# --- Gráfico 1: Coordenadas Paralelas ---
if visualizacao == "📈 Coordenadas Paralelas":
    st.subheader("📈 Gráfico de Coordenadas Paralelas")

    cols = ['age', 'bmi', 'HbA1c_level', 'blood_glucose_level']

    fig = px.parallel_coordinates(
        df_filtrado,
        dimensions=cols,
        color="diabetes",
        color_continuous_scale=px.colors.diverging.Tealrose,
        color_continuous_midpoint=0.5,
        labels={
            "age": "Idade",
            "bmi": "IMC",
            "HbA1c_level": "HbA1c",
            "blood_glucose_level": "Glicose",
            "diabetes": "Diabetes"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

# --- Gráfico 2: Dispersão Animada ---
elif visualizacao == "🎞️ Dispersão Animada":
    st.subheader("🎞️ Gráfico de Dispersão Animado por Faixa Etária")

    variaveis = ['bmi', 'HbA1c_level', 'blood_glucose_level']

    col1, col2 = st.columns(2)
    with col1:
        eixo_x = st.selectbox("Eixo X", variaveis, index=0)
    with col2:
        eixo_y = st.selectbox("Eixo Y", [v for v in variaveis if v != eixo_x], index=1)

    fig = px.scatter(
        df_filtrado,
        x=eixo_x,
        y=eixo_y,
        animation_frame="faixa_etaria",
        color="diabetes",
        hover_name="gender",
        size_max=12,
        range_x=[df[eixo_x].min(), df[eixo_x].max()],
        range_y=[df[eixo_y].min(), df[eixo_y].max()],
        title=f"{eixo_y} vs {eixo_x} por Faixa Etária"
    )

    st.plotly_chart(fig, use_container_width=True)


