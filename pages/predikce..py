import streamlit as st
import pandas as pd
import joblib

st.title("🧒 Predikce dětské obezity")

# -----------------------------
# 1) MODEL
# -----------------------------
@st.cache_resource
def load_model():
    bundle = joblib.load("model.pkl")
    return bundle["model"], bundle["features"]

model, feature_names = load_model()

COUNTRY_PREFIX = "COUNTRY_NAME_"

# Feature columns you can control in UI
controlled_features = [
    "SEX", "AGE", 
    "SOFT_DRINKS", "SWEETS", "VEGETABLES",
    "FRIEND_TALK", "PHYS_ACT_60", "BREAKFAST_WEEKDAYS",
    "TOOTH_BRUSHING", "FEEL_LOW", "TALK_FATHER"
]

# -----------------------------
# 2) OPTIONS FOR USER
# -----------------------------

sex_options = {"Kluk": 1, "Holka": 2}

soft_drinks_labels = [
    "1 - never",
    "2 - less once a week",
    "3 - once a week",
    "4 - 2–4 days a week",
    "5 - 5–6 days a week",
    "6 - once daily",
    "7 - more than once daily"
]

sweets_labels = soft_drinks_labels
vegetables_labels = soft_drinks_labels

friend_talk_labels = [
    "1 - very strongly disagree",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7 - very strongly agree"
]

phys_labels = [
    "1 - 0 days",
    "2 - 1 day",
    "3 - 2 days",
    "4 - 3 days",
    "5 - 4 days",
    "6 - 5 days",
    "7 - 6-7 days"
]

breakfast_labels = [
    "1 - never",
    "2 - one day",
    "3 - two days",
    "4 - three days",
    "5 - four days",
    "6 - five days"
]

tooth_labels = [
    "1 - more than once a day",
    "2 - once a day",
    "3 - once a week",
    "4 - less than weekly",
    "5 - never"
]

feellow_labels = [
    "1 - about every day",
    "2 - more than once a week",
    "3 - about every week",
    "4 - about every month",
    "5 - rarely or never"
]

talkfather_labels = [
    "1 - very easy",
    "2 - easy",
    "3 - difficult",
    "4 - very difficult",
    "5 - doesn’t have or see"
]

# ALL COUNTRIES FROM MODEL
country_options = [c.replace(COUNTRY_PREFIX, "") 
                   for c in feature_names if c.startswith(COUNTRY_PREFIX)]

# -----------------------------
# 3) BUILD INPUT VECTOR
# -----------------------------
def build_input_row(user_input):
    row = pd.Series(0, index=feature_names, dtype=float)

    # NORMAL numerical features
    for col, val in user_input.items():
        if col == "COUNTRY_NAME":
            continue
        if col in controlled_features:
            row[col] = val

    # COUNTRY one-hot
    selected = COUNTRY_PREFIX + user_input["COUNTRY_NAME"]
    if selected in feature_names:
        row[selected] = 1

    return pd.DataFrame([row], columns=feature_names)


# -----------------------------
# 4) UI — USER INPUT
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    sex_label = st.selectbox("Pohlaví", list(sex_options.keys()))
    sex = sex_options[sex_label]

    age = st.number_input("Věk dítěte", min_value=7, max_value=18, step=1)

    soft_drinks = st.selectbox("Sladké nápoje", soft_drinks_labels)
    sweets = st.selectbox("Sladkosti", sweets_labels)
    vegetables = st.selectbox("Zelenina", vegetables_labels)

with col2:
    friend_talk = st.selectbox("Mluví s kamarády", friend_talk_labels)
    phys = st.selectbox("Fyzická aktivita (< 60 min)", phys_labels)
    breakfast = st.selectbox("Snídaně – všední dny", breakfast_labels)
    teeth = st.selectbox("Čištění zubů", tooth_labels)
    feel_low = st.selectbox("Cítí se sklesle", feellow_labels)
    talk_father = st.selectbox("Komunikuje s otcem", talkfather_labels)

country = st.selectbox("Země", country_options)

# Convert "1 - never" → 1
def extract_number(label):
    return int(label.split("-")[0].strip())

# -----------------------------
# 5) COMPUTE
# -----------------------------
if st.button("🔍 Spočítat predikci"):
    user_data = {
        "SEX": sex,
        "AGE": age,
        "SOFT_DRINKS": extract_number(soft_drinks),
        "SWEETS": extract_number(sweets),
        "VEGETABLES": extract_number(vegetables),
        "FRIEND_TALK": extract_number(friend_talk),
        "PHYS_ACT_60": extract_number(phys),
        "BREAKFAST_WEEKDAYS": extract_number(breakfast),
        "TOOTH_BRUSHING": extract_number(teeth),
        "FEEL_LOW": extract_number(feel_low),
        "TALK_FATHER": extract_number(talk_father),
        "COUNTRY_NAME": country
    }

    X_user = build_input_row(user_data)
    pred_class = model.predict(X_user)[0]
    pred_proba = model.predict_proba(X_user)[0, 1]

    st.write("---")
    st.subheader("📊 Výsledek")

    if pred_class == 1:
        st.error(f"**Vysoké riziko obezity** – pravděpodobnost: **{pred_proba:.1%}**")
    else:
        st.success(f"**Nízké riziko obezity** – pravděpodobnost: **{pred_proba:.1%}**")
