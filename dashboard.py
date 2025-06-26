import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("Gráfico Parallel Coordinates com Filtro de Diabetes")

@st.cache_data
def load_data():
    return pd.read_csv("diabetes_prediction_dataset.csv")

df = load_data()

cols = ['age', 'bmi', 'HbA1c_level', 'blood_glucose_level', 'hypertension', 'heart_disease']

# Criando listas de índices para diabetes = 0 e diabetes = 1
idx_diabetes_0 = df[df['diabetes'] == 0].index.tolist()
idx_diabetes_1 = df[df['diabetes'] == 1].index.tolist()

# Função para criar traços (linhas) para cada grupo
def create_trace(indices, color, name):
    return go.Parcoords(
        line=dict(color=color, colorscale=[[0, color], [1, color]], showscale=False),
        dimensions=[dict(range=[df[col].min(), df[col].max()], label=col, values=df.loc[indices, col]) for col in cols],
        name=name,
        visible=True
    )

# Cria dois traços: um para não diabeticos, outro para diabeticos
trace_0 = create_trace(idx_diabetes_0, 'blue', 'Não Diabéticos')
trace_1 = create_trace(idx_diabetes_1, 'red', 'Diabéticos')

fig = go.Figure(data=[trace_0, trace_1])

# Botões para controlar a visibilidade dos traços
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            x=0.5,
            y=1.2,
            showactive=True,
            buttons=list([
                dict(label="Mostrar Ambos",
                     method="update",
                     args=[{"visible": [True, True]}]),
                dict(label="Apenas Não Diabéticos",
                     method="update",
                     args=[{"visible": [True, False]}]),
                dict(label="Apenas Diabéticos",
                     method="update",
                     args=[{"visible": [False, True]}]),
            ]),
        )
    ],
    title="Parallel Coordinates Plot - Diabetes"
)

st.plotly_chart(fig, use_container_width=True)

