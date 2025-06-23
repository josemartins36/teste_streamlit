import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

st.title('📊 Dashboard de Vendas')

# Sidebar
st.sidebar.header('Configurações')

# Upload do arquivo
uploaded_file = st.sidebar.file_uploader("Envie seu arquivo CSV", type=["csv"])

# Se não enviar, carrega dados de exemplo
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.sidebar.info('Nenhum arquivo enviado. Usando dados de exemplo.')
    df = pd.read_csv('data/vendas.csv')

# Mostrar dados
st.subheader('🗂️ Dados')
st.dataframe(df)

# Estatísticas rápidas
st.subheader('📈 Estatísticas Gerais')

col1, col2, col3 = st.columns(3)

col1.metric("Total de Vendas", f"R$ {df['Vendas'].sum():,.2f}")
col2.metric("Média de Vendas", f"R$ {df['Vendas'].mean():,.2f}")
col3.metric("Total de Registros", df.shape[0])

# Filtro por produto
produto = st.sidebar.selectbox('Selecione um Produto:', df['Produto'].unique())

df_filtrado = df[df['Produto'] == produto]

st.subheader(f'🔍 Análise do {produto}')

# Gráfico de barras por data
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(df_filtrado['Data'], df_filtrado['Vendas'], color='skyblue')
plt.xticks(rotation=45)
ax.set_title(f'Vendas por Data - {produto}')
ax.set_ylabel('Vendas')
st.pyplot(fig)

# Gráfico de linha para tendência
st.subheader('📈 Tendência de Vendas')

st.line_chart(df_filtrado.set_index('Data')['Vendas'])
