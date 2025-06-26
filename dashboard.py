import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard Diabetes", layout="wide", page_icon="🩺")
st.title("🩺 Dashboard Interativo - Predição de Diabetes")

@st.cache_data
def load_data():
    return pd.read_csv("diabetes_prediction_dataset.csv")

df = load_data()

# Sidebar filtros (simples para o exemplo)
genero = st.sidebar.selectbox("Gênero", ["Todos"] + sorted(df["gender"].unique().tolist()))
if genero != "Todos":
    df = df[df["gender"] == genero]

# Criando o gráfico com botões embutidos
fig = go.Figure()

# Traço IMC
fig.add_trace(go.Scatter(
    x=df['age'],
    y=df['bmi'],
    mode='markers',
    name='IMC',
    marker=dict(color='blue'),
    visible=True
))

# Traço Glicose
fig.add_trace(go.Scatter(
    x=df['age'],
    y=df['blood_glucose_level'],
    mode='markers',
    name='Nível de Glicose',
    marker=dict(color='red'),
    visible=True
))

# Botões para mostrar/ocultar traços
fig.update_layout(
    title="IMC e Nível de Glicose por Idade",
    xaxis_title="Idade",
    yaxis_title="Valor",
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            x=0.5,
            y=1.15,
            showactive=True,
            buttons=list([
                dict(
                    label="Mostrar Ambos",
                    method="update",
                    args=[{"visible": [True, True]}]
                ),
                dict(
                    label="Mostrar Apenas IMC",
                    method="update",
                    args=[{"visible": [True, False]}]
                ),
                dict(
                    label="Mostrar Apenas Glicose",
                    method="update",
                    args=[{"visible": [False, True]}]
                ),
            ]),
        )
    ]
)

st.plotly_chart(fig, use_container_width=True)

