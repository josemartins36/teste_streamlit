import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Gráfico Parallel Coordinates com Filtro Interativo")

@st.cache_data
def load_data():
    return pd.read_csv("diabetes_prediction_dataset.csv")

df = load_data()

# 🧪 Apenas variáveis contínuas relevantes
cols = ['age', 'bmi', 'HbA1c_level', 'blood_glucose_level']

# 🎛️ Filtro do grupo
filtro = st.radio(
    "Escolha o grupo para visualizar:",
    ("Todos", "Apenas Diabéticos", "Apenas Não Diabéticos")
)

if filtro == "Apenas Diabéticos":
    df_filtrado = df[df['diabetes'] == 1]
elif filtro == "Apenas Não Diabéticos":
    df_filtrado = df[df['diabetes'] == 0]
else:
    df_filtrado = df

# 📊 Gráfico Parallel Coordinates
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


