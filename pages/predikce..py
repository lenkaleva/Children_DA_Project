import streamlit as st
import pandas as pd
import joblib

# ---------------------------
# Základní nastavení stránky
# ---------------------------
st.set_page_config(page_title="Predikce dětské obezity", page_icon="🧒")

st.title("🧒 Predikce dětské obezity")
st.write(
    "Vyplň parametry dítěte. Model náhodného lesa spočítá pravděpodobnost, "
    "že dítě bude mít nadváhu / obezitu."
)

# ---------------------------
# 1) Načtení modelu
# ---------------------------
@st.cache_resource
def load_model():
    bundle = joblib.load("model.pkl")
    return bundle["model"], bundle["features"]

model, feature_names = load_model()

COUNTRY_PREFIX = "COUNTRY_NAME_"

controlled_features = [
    "SEX",
    "AGE",
    "SOFT_DRINKS",
    "SWEETS",
    "VEGETABLES",
    "FRIEND_TALK",
    "PHYS_ACT_60",
    "BREAKFAST_WEEKDAYS",
    "TOOTH_BRUSHING",
    "FEEL_LOW",
    "TALK_FATHER",
]

# ---------------------------
# 2) Funkce – tvorba X_new
# ---------------------------
def build_input_row(user_input: dict) -> pd.DataFrame:
    """
    Vytvoří jeden řádek (DataFrame) se stejnými sloupci,
    jaké měl model při tréninku (feature_names).
    Vše ostatní je nastaveno na 0.
    """
    row = pd.Series(0.0, index=feature_names)

    # běžné řízené featury
    for col, val in user_input.items():
        if col in controlled_features and col in feature_names:
            row[col] = float(val)

    # vždy nastavíme Czech Republic, pokud ten sloupec v modelu existuje
    cz_col = f"{COUNTRY_PREFIX}Czech Republic"
    if cz_col in feature_names:
        row[cz_col] = 1.0

    return pd.DataFrame([row], columns=feature_names)


def predict_child(user_input: dict):
    X_user = build_input_row(user_input)
    pred_proba = model.predict_proba(X_user)[0, 1]
    pred_class = int(model.predict(X_user)[0])
    return pred_class, pred_proba


# ---------------------------
# 3) Definice možností (škál)
#     – UŽIVATEL VIDÍ TEXT
#     – DO MODELU JDOU ČÍSLA
# ---------------------------

# SOFT_DRINKS / SWEETS / VEGETABLES
soft_sweets_veggies_opts = {
    "1 – nikdy": 1,
    "2 – méně než 1× týdně": 2,
    "3 – 1× týdně": 3,
    "4 – 2–4 dny v týdnu": 4,
    "5 – 5–6 dní v týdnu": 5,
    "6 – 1× denně": 6,
    "7 – vícekrát denně": 7,
}

# FRIEND_TALK (souhlasová škála)
friend_talk_opts = {
    "1 – velmi silně nesouhlasí": 1,
    "2 – nesouhlasí": 2,
    "3 – spíše nesouhlasí": 3,
    "4 – ani souhlas, ani nesouhlas": 4,
    "5 – spíše souhlasí": 5,
    "6 – souhlasí": 6,
    "7 – velmi silně souhlasí": 7,
}

# PHYS_ACT_60 – počet dní s 60+ min pohybu
phys_act_opts = {
    "0 dní": 0,
    "1 den": 1,
    "2 dny": 2,
    "3 dny": 3,
    "4 dny": 4,
    "5 dní": 5,
    "6 dní": 6,
    "7 dní": 7,
}

# BREAKFAST_WEEKDAYS – snídaně ve všední den (počet dní)
breakfast_opts = {
    "1 – nikdy": 1,
    "2 – 1 den": 2,
    "3 – 2 dny": 3,
    "4 – 3 dny": 4,
    "5 – 4 dny": 5,
    "6 – 5 dní": 6,
}

# TOOTH_BRUSHING – čištění zubů
tooth_opts = {
    "1 – více než 1× denně": 1,
    "2 – 1× denně": 2,
    "3 – 1× týdně": 3,
    "4 – méně často než týdně": 4,
    "5 – nikdy": 5,
}

# FEEL_LOW – jak často se cítí sklesle
feel_low_opts = {
    "1 – téměř každý den": 1,
    "2 – vícekrát týdně": 2,
    "3 – asi 1× týdně": 3,
    "4 – asi 1× měsíčně": 4,
    "5 – zřídka nebo nikdy": 5,
}

# TALK_FATHER – jak snadno mluví s otcem o problémech
talk_father_opts = {
    "1 – velmi snadno": 1,
    "2 – snadno": 2,
    "3 – obtížně": 3,
    "4 – velmi obtížně": 4,
    "5 – otce nemá / nevídá": 5,
}


# ---------------------------
# 4) Formulář – uživatelský vstup
# ---------------------------

st.subheader("✏️ Vyplň parametry dítěte")

col1, col2 = st.columns(2)

with col1:
    # SEX – musí být číslo 0/1, jinak padá 'could not convert string to float: Chlapec'
    sex_label = st.radio("Pohlaví", ["Chlapec", "Dívka"])
    sex = 1 if sex_label == "Chlapec" else 0

    age = st.number_input("Věk (roky)", min_value=7, max_value=18, step=1, value=13)

    sweets_label = st.selectbox("Sladkosti", list(soft_sweets_veggies_opts.keys()))
    sweets = soft_sweets_veggies_opts[sweets_label]

    soft_label = st.selectbox("Sladké nápoje (limonády)", list(soft_sweets_veggies_opts.keys()))
    soft_drinks = soft_sweets_veggies_opts[soft_label]

    veg_label = st.selectbox("Zelenina", list(soft_sweets_veggies_opts.keys()))
    vegetables = soft_sweets_veggies_opts[veg_label]

with col2:
    friend_label = st.selectbox("Mluví s kamarády o problémech", list(friend_talk_opts.keys()))
    friend_talk = friend_talk_opts[friend_label]

    phys_label = st.selectbox("Kolik dní v týdnu má ≥60 min pohybu", list(phys_act_opts.keys()))
    phys_act = phys_act_opts[phys_label]

    breakfast_label = st.selectbox("Snídaně ve všední den", list(breakfast_opts.keys()))
    breakfast = breakfast_opts[breakfast_label]

    tooth_label = st.selectbox("Čištění zubů", list(tooth_opts.keys()))
    tooth = tooth_opts[tooth_label]

    feel_label = st.selectbox("Jak často se cítí sklesle", list(feel_low_opts.keys()))
    feel_low = feel_low_opts[feel_label]

    talk_f_label = st.selectbox("Jak snadno mluví s otcem o problémech", list(talk_father_opts.keys()))
    talk_father = talk_father_opts[talk_f_label]


# ---------------------------
# 5) Tlačítko – spočítat predikci
# ---------------------------

if st.button("🔍 Spočítat predikci"):
    user_data = {
        "SEX": sex,
        "AGE": age,
        "SOFT_DRINKS": soft_drinks,
        "SWEETS": sweets,
        "VEGETABLES": vegetables,
        "FRIEND_TALK": friend_talk,
        "PHYS_ACT_60": phys_act,
        "BREAKFAST_WEEKDAYS": breakfast,
        "TOOTH_BRUSHING": tooth,
        "FEEL_LOW": feel_low,
        "TALK_FATHER": talk_father,
    }

    cls, proba = predict_child(user_data)

    st.markdown("---")
    st.subheader("📊 Výsledek")

    if cls == 1:
        st.error(
            f"**Model odhaduje zvýšené riziko nadváhy/obezity.**\n\n"
            f"Odhadovaná pravděpodobnost nadváhy: **{proba:.1%}**"
        )
    else:
        st.success(
            f"**Model odhaduje nižší riziko nadváhy/obezity.**\n\n"
            f"Odhadovaná pravděpodobnost nadváhy: **{proba:.1%}**"
        )

    # volitelné: ukázat debug vstupy
    with st.expander("🔬 Zobrazit vstupy, které šly do modelu"):
        st.json(user_data)
