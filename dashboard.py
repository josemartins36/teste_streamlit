import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard - Diabetes", layout="wide", page_icon="🩺")

st.title("🩺 Dashboard Interativo de Predição de Diabetes")

# Função para carregar os dados
@st.cache_data
def carregar_dados():
    df = pd.read_csv("diabetes_prediction_dataset.csv")
    return df

df = carregar_dados()

# Sidebar com filtros
st.sidebar.header("🎛️ Filtros")
genero = st.sidebar.selectbox("Selecione o gênero", ["Todos"] + sorted(df['gender'].unique()))
fumante = st.sidebar.multiselect("Histórico de tabagismo", options=df['smoking_history'].unique())
faixa_idade = st.sidebar.slider("Faixa etária", int(df['age'].min()), int(df['age'].max()), (20, 60))

# Aplicação dos filtros
df_filtrado = df.copy()

if genero != "Todos":
    df_filtrado = df_filtrado[df_filtrado["gender"] == genero]

if fumante:
    df_filtrado = df_filtrado[df_filtrado["smoking_history"].isin(fumante)]

df_filtrado = df_filtrado[(df_filtrado["age"] >= faixa_idade[0]) & (df_filtrado["age"] <= faixa_idade[1])]

# === Métricas rápidas ===
col1, col2, col3 = st.columns(3)
col1.metric("Total de Registros", len(df_filtrado))
col2.metric("Casos de Diabetes", df_filtrado["diabetes"].sum())
col3.metric("Porcentagem Diabéticos", f"{100 * df_filtrado['diabetes'].mean():.1f}%")

st.divider()

# === Gráfico 1: Faixa Etária x Diabetes ===
st.subheader("📊 Distribuição de Diabetes por Faixa Etária")
df_filtrado['faixa_etaria'] = pd.cut(df_filtrado['age'], bins=[0, 20, 40, 60, 80, 120],
                                     labels=['0-20', '21-40', '41-60', '61-80', '81+'])

fig1 = px.histogram(df_filtrado, x='faixa_etaria', color='diabetes', barmode='group',
                    labels={'faixa_etaria': 'Faixa Etária', 'diabetes': 'Diabetes'})
st.plotly_chart(fig1, use_container_width=True)

# === Gráfico 2: IMC vs Glicose ===
st.subheader("🧬 Correlação entre IMC e Nível de Glicose")
fig2 = px.scatter(df_filtrado, x='bmi', y='blood_glucose_level',
                  color='diabetes', hover_data=['age', 'gender', 'hypertension'],
                  labels={'bmi': 'IMC', 'blood_glucose_level': 'Glicose'})
st.plotly_chart(fig2, use_container_width=True)

# === Gráfico 3: Proporção por Gênero ===
st.subheader("🚻 Proporção de Diabéticos por Gênero (com base no filtro)")
proporcao = df_filtrado.groupby('gender')['diabetes'].mean().reset_index()
fig3 = px.bar(proporcao, x='gender', y='diabetes',
              labels={'gender': 'Gênero', 'diabetes': 'Proporção de Diabéticos'},
              color='gender', text='diabetes')
st.plotly_chart(fig3, use_container_width=True)

# === Tabela ===
st.subheader("🗃️ Dados Filtrados")
st.dataframe(df_filtrado, use_container_width=True)

# Rodapé
st.caption("Desenvolvido com ❤️ usando Streamlit e Plotly")

