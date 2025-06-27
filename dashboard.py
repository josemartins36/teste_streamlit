import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Interativo - Diabetes", layout="wide")
st.title("📊 Dashboard Interativo - Predição de Diabetes")

@st.cache_data
def load_data():
    return pd.read_csv("diabetes_prediction_dataset.csv")

df = load_data()
df = df.sort_values(by="age")  # para animações e sliders

# 🎛️ Sidebar
st.sidebar.title("🔎 Selecione um gráfico:")
opcao = st.sidebar.radio(
    "Escolha uma visualização:",
    ["Parallel Coordinates", "Treemap", "Gráfico Animado por Idade", "Boxplot", "Histograma"]
)

# 🧪 Variáveis contínuas
cols_continuas = ['age', 'bmi', 'HbA1c_level', 'blood_glucose_level']

# 🎛️ Filtro de grupo
grupo = st.sidebar.radio("Grupo a visualizar:", ["Todos", "Apenas Diabéticos", "Apenas Não Diabéticos"])
if grupo == "Apenas Diabéticos":
    df_filtrado = df[df["diabetes"] == 1]
elif grupo == "Apenas Não Diabéticos":
    df_filtrado = df[df["diabetes"] == 0]
else:
    df_filtrado = df.copy()

# ==========================
# 1. Parallel Coordinates
# ==========================
if opcao == "Parallel Coordinates":
    st.subheader("🔗 Gráfico Parallel Coordinates")
    fig = px.parallel_coordinates(
        df_filtrado,
        dimensions=cols_continuas,
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

# ==========================
# 2. Treemap
# ==========================
elif opcao == "Treemap":
    st.subheader("🌳 Treemap Interativo")

    st.markdown("Selecione abaixo as variáveis categóricas para compor a hierarquia do Treemap.")
    categorias = ["gender", "smoking_history", "diabetes"]

    path = st.multiselect(
        "Hierarquia (ordem importa):",
        options=categorias,
        default=["gender", "smoking_history", "diabetes"]
    )

    if len(path) >= 2:
        fig = px.treemap(
            df_filtrado,
            path=path,
            title="Treemap Hierárquico"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Selecione pelo menos duas variáveis para montar a hierarquia.")

# ==========================
# 3. Gráfico Animado
# ==========================
elif opcao == "Gráfico Animado por Idade":
    st.subheader("🎥 Animação: Comparação por Faixa Etária")

    eixo_x = st.selectbox("Eixo X", cols_continuas, index=0)
    eixo_y = st.selectbox("Eixo Y", cols_continuas, index=1)

    fig = px.scatter(
        df_filtrado,
        x=eixo_x,
        y=eixo_y,
        animation_frame="age",
        color="diabetes",
        hover_name="gender",
        range_x=[df[eixo_x].min(), df[eixo_x].max()],
        range_y=[df[eixo_y].min(), df[eixo_y].max()],
        title=f"{eixo_y} vs {eixo_x} por Idade"
    )
    st.plotly_chart(fig, use_container_width=True)

# ==========================
# 4. Boxplot Comparativo
# ==========================
elif opcao == "Boxplot":
    st.subheader("📦 Boxplot por Diabetes")
    var = st.selectbox("Escolha a variável contínua:", cols_continuas)

    fig = px.box(df_filtrado, x="diabetes", y=var, color="diabetes",
                 labels={"diabetes": "Diabetes", var: var})
    st.plotly_chart(fig, use_container_width=True)

# ==========================
# 5. Histograma Comparativo
# ==========================
elif opcao == "Histograma":
    st.subheader("📊 Histograma Empilhado")
    var = st.selectbox("Escolha uma variável para distribuição:", cols_continuas)

    fig = px.histogram(
        df_filtrado,
        x=var,
        color="diabetes",
        nbins=40,
        barmode="overlay",
        labels={"diabetes": "Diabetes"}
    )
    st.plotly_chart(fig, use_container_width=True)



