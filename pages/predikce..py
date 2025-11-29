import streamlit as st
import pandas as pd
import joblib
from PIL import Image

st.set_page_config(page_title="Predikce obezity", page_icon="🧒")

st.title("🧒 Predikce dětské obezity")
st.write("")

# ---------------------------
# 1) QR KÓD
# ---------------------------
st.subheader("📱 Otevři aplikaci na telefonu")
qr = Image.open("qr.png")   # sem dej název tvého souboru s QR
st.image(qr, caption="Naskenuj QR kód", width=200)

st.markdown("---")

# ---------------------------
# 2) Načtení modelu
# ---------------------------
@st.cache_resource
def load_model():
    bundle = joblib.load("model.pkl")
    return bundle["model"], bundle["features"]

model, feature_names = load_model()

COUNTRY_PREFIX = "COUNTRY_NAME_"

controlled_features = [
    "SEX", "AGE", "SOFT_DRINKS", "SWEETS", "VEGETABLES", "FRIEND_TALK",
    "PHYS_ACT_60", "BREAKFAST_WEEKDAYS", "TOOTH_BRUSHING",
    "FEEL_LOW", "TALK_FATHER"
]

# ---------------------------
# 3) Funkce – tvorba X_new
# ---------------------------
def build_input_row(user_input: dict, feature_names, controlled_features):
    row = pd.Series(0, index=feature_names, dtype="float")

    for col, val in user_input.items():
        if col == "COUNTRY_NAME":
            continue
        if col in controlled_features:
            row[col] = val

    # one-hot encoded country
    if "COUNTRY_NAME" in user_input:
        col_name = f"{COUNTRY_PREFIX}{user_input['COUNTRY_NAME']}"
        if col_name in feature_names:
            row[col_name] = 1

    return pd.DataFrame([row], columns=feature_names)

def predict_child(user_input):
    X_user = build_input_row(user_input, feature_names, controlled_features)
    pred_class = model.predict(X_user)[0]
    pred_proba = model.predict_proba(X_user)[0, 1]
    return pred_class, pred_proba


# ---------------------------
# 4) Formulář – uživatelský vstup
# ---------------------------

st.subheader("✏️ Vyplň parametry dítěte")

col1, col2 = st.columns(2)

with col1:
    sex = st.selectbox("Pohlaví", {"Chlapec": 1, "Dívka": 0})
    age = st.number_input("Věk", min_value=7, max_value=18, step=1)

    sweets = st.slider("Sladkosti", 0, 7, 2)
    soft = st.slider("Sladké nápoje", 0, 7, 2)
    vegetables = st.slider("Zelenina (četnost)", 0, 7, 2)

with col2:
    phys = st.slider("Fyzická aktivita (<60 min)", 0, 7, 3)
    breakfast = st.slider("Snídaně ve všední den", 0, 7, 5)
    teeth = st.slider("Čištění zubů", 0, 7, 4)
    feel_low = st.slider("Cítí se sklesle", 0, 7, 3)
    talk_father = st.slider("Mluví s otcem o problémech", 0, 7, 3)

country = st.selectbox(
    "Země",
    ["Czech Republic", "Slovakia", "Poland", "Germany", "United Kingdom", "Austria"]
)

if st.button("🔍 Spočítat predikci"):
    user_data = {
        "SEX": sex,
        "AGE": age,
        "SOFT_DRINKS": soft,
        "SWEETS": sweets,
        "VEGETABLES": vegetables,
        "FRIEND_TALK": 3,
        "PHYS_ACT_60": phys,
        "BREAKFAST_WEEKDAYS": breakfast,
        "TOOTH_BRUSHING": teeth,
        "FEEL_LOW": feel_low,
        "TALK_FATHER": talk_father,
        "COUNTRY_NAME": country,
    }

    cls, proba = predict_child(user_data)

    st.markdown("---")
    st.subheader("📊 Výsledek")

    if cls == 1:
        st.error(f"**Vaše dítě má zvýšené riziko obezity.**\nPravděpodobnost: **{proba:.1%}**")
    else:
        st.success(f"**Nízké riziko obezity.**\nPravděpodobnost: **{proba:.1%}**")
