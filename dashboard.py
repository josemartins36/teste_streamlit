import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Diabetes", layout="wide")

st.title('Dashboard - Análise de Dados sobre Diabetes')

# ================= Carregar Dados ==================
@st.cache_data
def load_data():
    df = pd.read_csv('diabetes_prediction_dataset.csv')
    return df

df = load_data()

st.subheader('Dados - Primeiras linhas')
st.dataframe(df.head())


# ================= Gráfico de Gênero ==================
st.subheader('📊 Distribuição por Gênero')

fig_gender = px.histogram(df, x='gender', color='gender',
                           title="Distribuição de Gênero",
                           color_discrete_sequence=['lightblue', 'pink', 'gray'])

st.plotly_chart(fig_gender, use_container_width=True)


# ================= Variáveis Numéricas ==================
st.subheader('Distribuição das Variáveis Numéricas')

numerical_cols = ['age', 'bmi', 'HbA1c_level', 'blood_glucose_level']
col1, col2 = st.columns(2)

for i, col in enumerate(numerical_cols):
    if i % 2 == 0:
        with col1:
            fig = px.histogram(df, x=col, nbins=30, title=f'Distribuição de {col}')
            st.plotly_chart(fig, use_container_width=True)
    else:
        with col2:
            fig = px.histogram(df, x=col, nbins=30, title=f'Distribuição de {col}')
            st.plotly_chart(fig, use_container_width=True)


# ================= Matriz de Correlação ==================
st.subheader('Matriz de Correlação')

corr = df.corr(numeric_only=True)

fig_corr = px.imshow(corr, text_auto=True, title='Matriz de Correlação',
                     color_continuous_scale='RdBu_r')
st.plotly_chart(fig_corr, use_container_width=True)


# ================= Filtros ==================
st.sidebar.subheader('Filtros dos Dados')

gender_filter = st.sidebar.multiselect('Gênero', df['gender'].unique(), df['gender'].unique())
smoke_filter = st.sidebar.multiselect('Histórico de Tabagismo', df['smoking_history'].unique(),
                                       df['smoking_history'].unique())
hypertension_filter = st.sidebar.multiselect('Hipertensão', df['hypertension'].unique(),
                                              df['hypertension'].unique())
heart_disease_filter = st.sidebar.multiselect('Doença Cardíaca', df['heart_disease'].unique(),
                                               df['heart_disease'].unique())

# Aplicando filtros
df_filtered = df[
    (df['gender'].isin(gender_filter)) &
    (df['smoking_history'].isin(smoke_filter)) &
    (df['hypertension'].isin(hypertension_filter)) &
    (df['heart_disease'].isin(heart_disease_filter))
]


# ================= Distribuição Diabetes ==================
st.subheader('Distribuição de Diabetes (Pós-Filtros)')

fig_diabetes = px.histogram(df_filtered, x='diabetes', color='diabetes',
                             title='Distribuição de Diabetes',
                             color_discrete_map={1: 'red', 0: 'green'},
                             category_orders={'diabetes': [0, 1]})
st.plotly_chart(fig_diabetes, use_container_width=True)


# ================= Análise Cruzada ==================
st.subheader('Glicose Média por Faixa Etária e Gênero')

# Criar faixa etária
df_filtered['faixa_etaria'] = pd.cut(df_filtered['age'],
                                     bins=[0, 20, 40, 60, 80, 120],
                                     labels=['0-20', '21-40', '41-60', '61-80', '81+'])

fig_cross = px.bar(df_filtered, x='faixa_etaria', y='blood_glucose_level',
                   color='gender', barmode='group',
                   title='Nível Médio de Glicose por Faixa Etária e Gênero',
                   labels={'blood_glucose_level': 'Nível Médio de Glicose'},
                   height=500)

st.plotly_chart(fig_cross, use_container_width=True)

df['faixa_etaria'] = pd.cut(df['age'], bins=[0, 20, 40, 60, 80, 120],
                            labels=['0-20', '21-40', '41-60', '61-80', '81+'])
fig = px.histogram(df, x='faixa_etaria', color='diabetes', barmode='group')

