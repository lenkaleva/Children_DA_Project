import streamlit as st
import pandas as pd
import joblib

st.title("🧒 Child Obesity Prediction")

# -----------------------------
# 1) MODEL
# -----------------------------
@st.cache_resource
def load_model():
    bundle = joblib.load("model.pkl")
    return bundle["model"], bundle["features"]

model, feature_names = load_model()

COUNTRY_PREFIX = "COUNTRY_NAME_"

# Feature columns controlled in UI
controlled_features = [
    "SEX", "AGE", 
    "SOFT_DRINKS", "SWEETS", "VEGETABLES",
    "FRIEND_TALK", "PHYS_ACT_60", "BREAKFAST_WEEKDAYS",
    "TOOTH_BRUSHING", "FEEL_LOW", "TALK_FATHER"
]

# -----------------------------
# 2) USER OPTIONS
# -----------------------------

sex_options = {"Boy": 1, "Girl": 2}

soft_sweets_labels = [
    "1 – never",
    "2 – less than once per week",
    "3 – once per week",
    "4 – 2–4 times per week",
    "5 – 5–6 times per week",
    "6 – daily",
    "7 – more than once per day"
]

soft_drinks_labels = soft_sweets_labels
sweets_labels = soft_sweets_labels

vegetables_labels = [
    "1 – daily",
    "2 – 5–6 times per week",
    "3 – 2–4 times per week",
    "4 – once per week",
    "5 – less than once per week",
    "6 – rarely",
    "7 – never"
]

friend_talk_labels = [
    "1 – very easy",
    "2",
    "3",
    "4 – neutral",
    "5",
    "6",
    "7 – very difficult"
]

phys_labels = [
    "1 – 6–7 days",
    "2 – 5 days",
    "3 – 4 days",
    "4 – 3 days",
    "5 – 2 days",
    "6 – 1 day",
    "7 – 0 days"
]

breakfast_labels = [
    "1 – every day",
    "2 – 4 days",
    "3 – 3 days",
    "4 – 2 days",
    "5 – 1 day",
    "6 – less often",
    "7 – never"
]

tooth_labels = [
    "1 – twice per day or more",
    "2 – once per day",
    "3 – once per week",
    "4 – less often",
    "5 – never"
]

feellow_labels = [
    "1 – never",
    "2 – rarely",
    "3 – monthly",
    "4 – weekly",
    "5 – several times per week",
    "6 – almost daily",
    "7 – daily"
]

talkfather_labels = [
    "1 – very easy",
    "2 – easy",
    "3 – rather easy",
    "4 – rather difficult",
    "5 – difficult",
    "6 – very difficult",
    "7 – not in contact"
]

# Countries available in model
country_options = [c.replace(COUNTRY_PREFIX, "") 
                   for c in feature_names if c.startswith(COUNTRY_PREFIX)]

# -----------------------------
# 3) BUILD VECTOR
# -----------------------------
def build_input_row(user_input):
    row = pd.Series(0, index=feature_names, dtype=float)

    for col, val in user_input.items():
        if col == "COUNTRY_NAME":
            continue
        if col in controlled_features:
            row[col] = val

    selected = COUNTRY_PREFIX + user_input["COUNTRY_NAME"]
    if selected in feature_names:
        row[selected] = 1

    return pd.DataFrame([row], columns=feature_names)

# Convert label "1 – daily" → 1
def extract_number(label):
    return int(label.split("–")[0].split("-")[0].strip())

# -----------------------------
# 4) UI
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    sex_label = st.selectbox("Sex", list(sex_options.keys()))
    sex = sex_options[sex_label]

    # Age based on dataset (adjust if needed)
    age = st.selectbox("Age", list(range(10, 18)))

    soft_drinks = st.selectbox("Sugary drinks", soft_drinks_labels)
    sweets = st.selectbox("Sweets", sweets_labels)
    vegetables = st.selectbox("Vegetables", vegetables_labels)

with col2:
    friend_talk = st.selectbox("Talking with friends", friend_talk_labels)
    phys = st.selectbox("Physical activity (< 60 min)", phys_labels)
    breakfast = st.selectbox("Breakfast (weekdays)", breakfast_labels)
    teeth = st.selectbox("Tooth brushing", tooth_labels)
    feel_low = st.selectbox("Feeling low", feellow_labels)
    talk_father = st.selectbox("Talking to father", talkfather_labels)

country = st.selectbox("Country", country_options)

# -----------------------------
# 5) COMPUTE
# -----------------------------
if st.button("🔍 Predict"):
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

    risk_flags = sum(
        1 for k, v in user_data.items()
        if k in controlled_features and isinstance(v, (int, float)) and v >= 6
    )

    #if risk_flags >= 6:
     #   st.warning("⚠ Several responses indicate unhealthy habits. This may increase the risk regardless of model #prediction.")

    # RISK BAR
    st.write("### Behaviour Risk Meter")

    # Normalise risk to 0–1
    risk_ratio = min(risk_flags / 10, 1.0)  # assuming 10 questions, adjust if needed

    # Create bar background (green → yellow → red)
    bar_html = f"""
    <div style="width: 100%; height: 35px; background: linear-gradient(to right, 
        #4caf50 0%,       /* green   */
        #ffeb3b 50%,      /* yellow  */
        #f44336 100%      /* red     */
    ); border-radius: 8px; position: relative;">

    <div style="
            position: absolute;
            left: calc({risk_ratio*100}% - 10px);
            top: -8px;
            font-size: 26px;
        ">⬆</div>

    </div>

    <p style="text-align:center; font-size:14px; margin-top:4px;">
    High-risk answers: <b>{risk_flags}</b> / 10  
    </p>
    """

    st.markdown(bar_html, unsafe_allow_html=True)




    st.write("---")
    st.subheader("📊 Result")

    if pred_class == 1:
        st.error(f"**High risk of obesity** – probability: **{pred_proba:.1%}**")
    else:
        st.success(f"**Low risk of obesity** – probability: **{pred_proba:.1%}**")
