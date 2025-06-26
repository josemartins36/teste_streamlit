import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Interativo - Diabetes", layout="wide")
st.title("📊 Dashboard Interativo: Predição de Diabetes")

@st.cache_data
def load_data():
    df = pd.read_csv("diabetes_prediction_dataset.csv")
    df['age'] = df['age'].astype(int)
    return df

df = load_data()

# Selecionador de visualização
visualizacao = st.sidebar.radio(
    "Selecione o tipo de gráfico:",
    ["📈 Gráfico de Coordenadas Paralelas", "🎞️ Gráfico Animado por Idade"]
)

# 🧪 Variáveis contínuas relevantes
cols = ['age', 'bmi', 'HbA1c_level', 'blood_glucose_level']

# 🎛️ Filtro do grupo
filtro = st.sidebar.radio(
    "Escolha o grupo para visualizar:",
    ("Todos", "Apenas Diabéticos", "Apenas Não Diabéticos")
)

# Filtragem
if filtro == "Apenas Diabéticos":
    df_filtrado = df[df['diabetes'] == 1]
elif filtro == "Apenas Não Diabéticos":
    df_filtrado = df[df['diabetes'] == 0]
else:
    df_filtrado = df

# ================================
# 📌 VISUALIZAÇÃO 1: Parallel Coordinates
# ================================
if visualizacao == "📈 Gráfico de Coordenadas Paralelas":
    st.subheader("Gráfico de Coordenadas Paralelas")
    fig = px.parallel_coordinates(
        df_filtrado,
        dimensions=cols,
        color='diabetes',
        color_continuous_scale=px.colors.diverging.Tealrose,
        color_continuous_midpoint=0.5,
        labels={
            'age': 'Idade',
            'bmi': 'IMC',
            'HbA1c_level': 'HbA1c',
            'blood_glucose_level': 'Glicose',
            'diabetes': 'Diabetes'
        }
    )
    st.plotly_chart(fig, use_container_width=True)

# ================================
# 📌 VISUALIZAÇÃO 2: Gráfico Animado
# ================================
elif visualizacao == "🎞️ Gráfico Animado por Idade":
    st.subheader("Gráfico de Dispersão Animado por Idade")

    x_var = st.selectbox("Eixo X", cols, index=1)
    y_var = st.selectbox("Eixo Y", [c for c in cols if c != x_var], index=2)

    # Gráfico animado com Plotly
    fig = px.scatter(
        df_filtrado,
        x=x_var,
        y=y_var,
        animation_frame="age",
        animation_group="gender",
        color="diabetes",
        hover_name="gender",
        size_max=15,
        range_x=[df[x_var].min(), df[x_var].max()],
        range_y=[df[y_var].min(), df[y_var].max()],
        title=f"{y_var} vs {x_var} por Idade"
    )

    st.plotly_chart(fig, use_container_width=True)



