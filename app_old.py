import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Predikce dětské obezity", page_icon="🧒")

st.title("🧒 Predikce dětské obezity")

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
    "SEX", "AGE", "SOFT_DRINKS", "SWEETS", "VEGETABLES", "FRIEND_TALK",
    "PHYS_ACT_60", "BREAKFAST_WEEKDAYS", "TOOTH_BRUSHING",
    "FEEL_LOW", "TALK_FATHER"
]

# ---------------------------
# 2) Funkce – vytvoření vstupu
# ---------------------------
def build_input_row(user_input: dict, feature_names, controlled_features):
    row = pd.Series(0, index=feature_names, dtype="float")

    for col, val in user_input.items():
        if col == "COUNTRY_NAME":
            continue
        if col in controlled_features and col in feature_names:
            row[col] = float(val)

    # COUNTRY one-hot
    if "COUNTRY_NAME" in user_input:
        country_col = f"{COUNTRY_PREFIX}{user_input['COUNTRY_NAME']}"
        if country_col in feature_names:
            row[country_col] = 1

    return pd.DataFrame([row], columns=feature_names)


def predict_child(user_input):
    X_user = build_input_row(user_input, feature_names, controlled_features)
    pred_class = model.predict(X_user)[0]
    pred_proba = model.predict_proba(X_user)[0, 1]
    return pred_class, pred_proba


# ---------------------------
# 3) Alias map 1–7 (1 good → 7 bad)
# ---------------------------

soft_drinks_map = {
    1: "1 - never",
    2: "2 - less than once a week",
    3: "3 - once a week",
    4: "4 - 2–4 days a week",
    5: "5 - 5–6 days a week",
    6: "6 - once daily",
    7: "7 - more than once daily",
}

sweets_map = soft_drinks_map
vegetables_map = soft_drinks_map

friend_talk_map = {
    1: "1 - very strongly disagree",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7 - very strongly agree",
}

phys_map = {
    1: "1 - 0 days",
    2: "2 - 1 day",
    3: "3 - 2 days",
    4: "4 - 3 days",
    5: "5 - 4 days",
    6: "6 - 5 days",
    7: "7 - 6–7 days",
}

breakfast_map = {
    1: "1 - never",
    2: "2 - one day",
    3: "3 - two days",
    4: "4 - three days",
    5: "5 - four days",
    6: "6 - five days",
    7: "7 - every day",
}

tooth_map = {
    1: "1 - more than once a day",
    2: "2 - once a day",
    3: "3 - once a week",
    4: "4 - less than weekly",
    5: "5 - never",
}

feel_low_map = {
    1: "1 - never",
    2: "2 - rarely",
    3: "3 - monthly",
    4: "4 - weekly",
    5: "5 - several times per week",
}

talk_father_map = {
    1: "1 - very easy",
    2: "2 - easy",
    3: "3 - difficult",
    4: "4 - very difficult",
    5: "5 - doesn't see",
}


# ---------------------------
# 4) UI – formulář
# ---------------------------

col1, col2 = st.columns(2)

with col1:
    sex = st.selectbox("Pohlaví", {"Kluk": 1, "Holka": 2})
    age = st.number_input("Věk dítěte", min_value=7, max_value=18, step=1)

    soft = st.selectbox("Sladké nápoje", list(soft_drinks_map.values()))
    sweets = st.selectbox("Sladkosti", list(sweets_map.values()))
    vegetables = st.selectbox("Zelenina", list(vegetables_map.values()))

with col2:
    friend_talk = st.selectbox("Mluví s kamarády", list(friend_talk_map.values()))
    phys = st.selectbox("Fyzická aktivita (< 60 min)", list(phys_map.values()))
    breakfast = st.selectbox("Snídaně – všední dny", list(breakfast_map.values()))
    teeth = st.selectbox("Čištění zubů", list(tooth_map.values()))
    feel_low = st.selectbox("Cítí se sklesle", list(feel_low_map.values()))
    talk_father = st.selectbox("Komunikuje s otcem", list(talk_father_map.values()))

country = st.selectbox(
    "Země",
    [c.replace(COUNTRY_PREFIX, "") for c in feature_names if c.startswith(COUNTRY_PREFIX)]
)


# ---------------------------
# 5) Převod aliasů zpět na hodnoty 1–7
# ---------------------------
def reverse_lookup(value, dictionary):
    for k, v in dictionary.items():
        if v == value:
            return k
    return None


# ---------------------------
# 6) VÝPOČET + GAUGE
# ---------------------------
if st.button("🔍 Spočítat predikci"):

    user_data = {
        "SEX": sex,
        "AGE": age,
        "SOFT_DRINKS": reverse_lookup(soft, soft_drinks_map),
        "SWEETS": reverse_lookup(sweets, sweets_map),
        "VEGETABLES": reverse_lookup(vegetables, vegetables_map),
        "FRIEND_TALK": reverse_lookup(friend_talk, friend_talk_map),
        "PHYS_ACT_60": reverse_lookup(phys, phys_map),
        "BREAKFAST_WEEKDAYS": reverse_lookup(breakfast, breakfast_map),
        "TOOTH_BRUSHING": reverse_lookup(teeth, tooth_map),
        "FEEL_LOW": reverse_lookup(feel_low, feel_low_map),
        "TALK_FATHER": reverse_lookup(talk_father, talk_father_map),
        "COUNTRY_NAME": country
    }

    cls, proba = predict_child(user_data)

    # ---------- RISK SCORE ----------
    behaviour_vars = [
        "SOFT_DRINKS", "SWEETS", "VEGETABLES", "FRIEND_TALK",
        "PHYS_ACT_60", "BREAKFAST_WEEKDAYS", "TOOTH_BRUSHING",
        "FEEL_LOW", "TALK_FATHER"
    ]

    risk_score = 0.0
    for k in behaviour_vars:
        v = user_data[k]
        if v in [4, 5, 6]:
            risk_score += 0.5
        elif v == 7:
            risk_score += 1.0

    max_score = len(behaviour_vars)
    risk_ratio = risk_score / max_score

    # ---------- Výsledek ----------
    st.markdown("---")
    st.subheader("📊 Výsledek")

    if cls == 1:
        st.error(f"**Zvýšené riziko obezity.** Pravděpodobnost: **{proba:.1%}**")
    else:
        st.success(f"Nízké riziko obezity – pravděpodobnost: **{proba:.1%}**")

    # ---------- GRAFICKÝ GAUGE ----------
    st.write("### Behaviour Risk Meter")

    angle = risk_ratio * 180  # 0–180°

    gauge_html = f"""
    <div style="width: 280px; margin: auto;">

      <div style="
          width: 280px;
          height: 140px;
          background: conic-gradient(
              #4caf50 0deg 60deg,
              #ffeb3b 60deg 120deg,
              #f44336 120deg 180deg
          );
          border-radius: 280px 280px 0 0;
          position: relative;
          margin-top: 10px;
          overflow: hidden;
      ">

          <div style="
              width: 4px;
              height: 95px;
              background: black;
              position: absolute;
              bottom: 0;
              left: 50%;
              transform-origin: bottom;
              transform: translateX(-50%) rotate({angle}deg);
              border-radius: 2px;
          "></div>

          <div style="
              width: 22px;
              height: 22px;
              background: black;
              border-radius: 50%;
              position: absolute;
              bottom: -5px;
              left: 50%;
              transform: translateX(-50%);
          "></div>

      </div>

      <p style="text-align:center; font-size:15px; margin-top:6px;">
        Weighted risk score: <b>{risk_score:.1f}</b> / {max_score}
      </p>

    </div>
    """

    st.markdown(gauge_html, unsafe_allow_html=True)
