import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Gráfico Parallel Coordinates - Diabetes")

@st.cache_data
def load_data():
    return pd.read_csv("data/diabetes_prediction_dataset.csv")

df = load_data()

# Colunas numéricas para o gráfico paralelo
cols = ['age', 'bmi', 'HbA1c_level', 'blood_glucose_level', 'hypertension', 'heart_disease']

# Opção para colorir pela variável diabetes (0 ou 1)
fig = px.parallel_coordinates(
    df,
    dimensions=cols,
    color='diabetes',
    color_continuous_scale=px.colors.diverging.Tealrose,
    color_continuous_midpoint=0.5,
    labels={
        'age': 'Idade',
        'bmi': 'IMC',
        'HbA1c_level': 'HbA1c',
        'blood_glucose_level': 'Glicose',
        'hypertension': 'Hipertensão',
        'heart_disease': 'Doença Cardíaca',
        'diabetes': 'Diabetes'
    }
)

st.plotly_chart(fig, use_container_width=True)
