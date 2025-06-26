import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

st.set_page_config(page_title="Dashboard Diabetes", layout="wide")
st.title("🩺 Dashboard Interativo - Predição de Diabetes")

# ====== Carregamento de Dados ======
@st.cache_data
def load_data():
    df = pd.read_csv('diabetes_prediction_dataset.csv')
    return df

df = load_data()


# ====== 1. Distribuição por Faixa Etária ======
st.subheader("📊 Distribuição de Diabetes por Faixa Etária")

df['faixa_etaria'] = pd.cut(df['age'],
                            bins=[0, 20, 40, 60, 80, 120],
                            labels=['0-20', '21-40', '41-60', '61-80', '81+'])

fig1 = px.histogram(df, x='faixa_etaria', color='diabetes',
                    barmode='group',
                    title="Distribuição de Diabetes por Faixa Etária",
                    labels={'diabetes': 'Diabetes'},
                    category_orders={'diabetes': [0, 1]})

st.plotly_chart(fig1, use_container_width=True)


# ====== 2. Correlação entre BMI e Glicose ======
st.subheader("🧬 Correlação entre IMC e Glicose")

fig2 = px.scatter(df, x='bmi', y='blood_glucose_level',
                  color='diabetes',
                  hover_data=['age', 'gender'],
                  title="IMC vs Nível de Glicose",
                  labels={'bmi': 'IMC', 'blood_glucose_level': 'Glicose'})

st.plotly_chart(fig2, use_container_width=True)


# ====== 3. Matriz de Correlação ======
st.subheader("💥 Matriz de Correlação")

corr = df.corr(numeric_only=True)
fig3 = px.imshow(corr, text_auto=True,
                 title="Matriz de Correlação",
                 color_continuous_scale='RdBu_r')

st.plotly_chart(fig3, use_container_width=True)


# ====== 4. Proporção de Diabéticos por Gênero ======
st.subheader("🚻 Proporção de Diabetes por Gênero")

df_gender = df.groupby('gender')['diabetes'].value_counts(normalize=True)\
              .rename('proporcao').reset_index()

# Filtrando apenas os casos positivos
df_diab = df_gender[df_gender['diabetes'] == 1]

fig4 = px.bar(df_diab, x='proporcao', y='gender',
              orientation='h', color='gender',
              text='proporcao',
              labels={'proporcao': 'Proporção', 'gender': 'Gênero'},
              title="Proporção de Diabéticos por Gênero")

st.plotly_chart(fig4, use_container_width=True)


# ====== 5. Distribuição de Diabetes por Tabagismo ======
st.subheader("🚬 Distribuição de Diabetes por Histórico de Tabagismo")

fig5 = px.pie(df[df['diabetes'] == 1],
              names='smoking_history',
              title="Histórico de Tabagismo entre Diabéticos",
              color_discrete_sequence=px.colors.qualitative.Set3)

st.plotly_chart(fig5, use_container_width=True)

