import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="Dashboard Interativo - Diabetes", layout="wide")
st.title("📊 Dashboard Interativo - Predição de Diabetes")

# =====================
# 1. Carregar dados
# =====================
@st.cache_data
def load_data():
    return pd.read_csv("diabetes_prediction_dataset.csv")

df = load_data()
df = df.sort_values(by="age")  # ordenação para sliders
cols_continuas = ['age', 'bmi', 'HbA1c_level', 'blood_glucose_level']

# =====================
# 2. Sidebar
# =====================
st.sidebar.title("🔎 Selecione uma opção:")
opcao = st.sidebar.radio(
    "Escolha uma visualização:",
    ["Parallel Coordinates", "Boxplot", "Histograma", "Preditor de Diabetes", "Acurácia do Modelo"]
)

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
        labels={"age": "Idade", "bmi": "IMC", "HbA1c_level": "HbA1c", "blood_glucose_level": "Glicose"}
    )
    st.plotly_chart(fig, use_container_width=True)

# ==========================
# 2. Boxplot
# ==========================
elif opcao == "Boxplot":
    st.subheader("📦 Boxplot por Diabetes")
    var = st.selectbox("Escolha a variável contínua:", cols_continuas)
    fig = px.box(df_filtrado, x="diabetes", y=var, color="diabetes", labels={"diabetes": "Diabetes", var: var})
    st.plotly_chart(fig, use_container_width=True)

# ==========================
# 3. Histograma
# ==========================
elif opcao == "Histograma":
    st.subheader("📊 Histograma Empilhado")
    var = st.selectbox("Escolha uma variável para distribuição:", cols_continuas)
    fig = px.histogram(df_filtrado, x=var, color="diabetes", nbins=40, barmode="overlay", labels={"diabetes": "Diabetes"})
    st.plotly_chart(fig, use_container_width=True)

# ==========================
# 4. Preditor de Diabetes (entrada do usuário)
# ==========================
elif opcao == "Preditor de Diabetes":
    st.subheader("🧠 Predição de Diabetes com Dados do Usuário")
    st.markdown("Preencha os dados abaixo para estimar a probabilidade de diabetes:")

    with st.form("form_predicao"):
        age = st.slider("Idade", 0, 100, 30)
        bmi = st.slider("IMC", 10.0, 50.0, 25.0)
        hba1c = st.slider("HbA1c Level", 3.0, 9.0, 5.0)
        glucose = st.slider("Glicose no sangue", 50, 300, 100)

        gender = st.selectbox("Gênero", ["Female", "Male"])
        hypertension = st.selectbox("Hipertensão", ["No", "Yes"])
        heart_disease = st.selectbox("Doença Cardíaca", ["No", "Yes"])
        smoking_history = st.selectbox("Histórico de Fumo", df["smoking_history"].unique())

        submitted = st.form_submit_button("🔍 Prever")

    if submitted:
        # Pré-processamento
        input_dict = {
            "age": age,
            "bmi": bmi,
            "HbA1c_level": hba1c,
            "blood_glucose_level": glucose,
            "gender_Male": 1 if gender == "Male" else 0,
            "hypertension": 1 if hypertension == "Yes" else 0,
            "heart_disease": 1 if heart_disease == "Yes" else 0,
        }

        for cat in df["smoking_history"].unique():
            input_dict[f"smoking_history_{cat}"] = 1 if smoking_history == cat else 0

        df_model = pd.get_dummies(df.copy(), drop_first=True)
        X = df_model.drop("diabetes", axis=1)
        y = df_model["diabetes"]

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)

        for col in X.columns:
            if col not in input_dict:
                input_dict[col] = 0

        input_df = pd.DataFrame([input_dict])[X.columns]
        pred = model.predict(input_df)[0]
        prob = model.predict_proba(input_df)[0][1]

        st.markdown(f"### 🩺 Resultado: {'🟥 Diabético' if pred == 1 else '🟩 Não Diabético'}")
        st.markdown(f"### 🔬 Probabilidade de Diabetes: `{prob:.2%}`")

# ==========================
# 5. Acurácia do Modelo (90% treino, 10% teste)
# ==========================
elif opcao == "Acurácia do Modelo":
    st.subheader("📈 Avaliação da Acurácia do Modelo")

    df_model = pd.get_dummies(df.copy(), drop_first=True)
    X = df_model.drop("diabetes", axis=1)
    y = df_model["diabetes"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)

    st.markdown("O modelo foi treinado com 90% dos dados e testado nos 10% restantes.")
    st.markdown(f"### 🎯 Acurácia no conjunto de teste: `{accuracy:.2%}`")
