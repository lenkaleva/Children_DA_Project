import streamlit as st
from openai import OpenAI

st.title("📊 Child Weight Risk Barometer")
st.markdown("""
<style>
    /* Zúžení hlavního obsahu a centrování */
    .main > div {
        max-width: 750px;
        margin: 0 auto;
        padding-top: 2rem;
    }

    /* LABELS (QUESTIONS) – text nad selectboxem */
    div[data-testid="stSelectbox"] label p {
        font-size: 16px !important;
        font-weight: 500 !important;
        color: #555 !important;
        margin-bottom: 6px !important;
        letter-spacing: 0.2px;
    }

    /* SELECTBOX CONTAINER – mezera mezi otázkami */
    div[data-testid="stSelectbox"] {
        margin-bottom: 14px;
    }

    /* SELECTBOX APPEARANCE – border, background, šířka */
    div[data-baseweb="select"] {
        border-radius: 8px !important;
        background-color: #f8f9fb !important;
        border: 1px solid #e2e6ec !important;
        max-width: 600px;
        margin: 0 auto;               /* vycentrování v užším sloupci */
    }

    /* TEXT UVNITŘ SELECTBOXU – bez „tab“ odsazení */
    div[data-baseweb="select"] div {
        font-size: 15px !important;
        color: #222 !important;
        padding-left: 0.2rem !important;  /* minimální, aby text nelepí na hranu */
    }

    /* HOVER EFFECT (jemné zvýraznění) */
    div[data-baseweb="select"]:hover {
        border-color: #c5ccd6 !important;
        background-color: #f5f6f8 !important;
    }
</style>
""", unsafe_allow_html=True)


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


# -----------------------------
# 3) BUILD VECTOR
# -----------------------------
# Convert label "1 – daily" → 1
def extract_number(label: str) -> int:
    return int(label.split("–")[0].split("-")[0].strip())


# 3) BAROMETER SCORE CALCULATED

def compute_risk_score(user_data: dict) -> int:
    """
    Returns lifestyle risk score 0–100.
    0 = very healthy habits, 100 = very unhealthy habits.
    """

    # All 1–7 scales: 1 = best, 7 = worst
    soft_drinks_risk = (user_data["SOFT_DRINKS"] - 1) / 6
    sweets_risk      = (user_data["SWEETS"] - 1) / 6
    vegetables_risk  = (user_data["VEGETABLES"] - 1) / 6
    friend_talk_risk = (user_data["FRIEND_TALK"] - 1) / 6
    phys_risk        = (user_data["PHYS_ACT_60"] - 1) / 6
    breakfast_risk   = (user_data["BREAKFAST_WEEKDAYS"] - 1) / 6
    feel_low_risk    = (user_data["FEEL_LOW"] - 1) / 6
    talk_father_risk = (user_data["TALK_FATHER"] - 1) / 6

    # Tooth brushing has 1–5 scale
    teeth_risk       = (user_data["TOOTH_BRUSHING"] - 1) / 4

    components = [
        soft_drinks_risk,
        sweets_risk,
        vegetables_risk,
        friend_talk_risk,
        phys_risk,
        breakfast_risk,
        teeth_risk,
        feel_low_risk,
        talk_father_risk,
    ]

    base_score = sum(components) / len(components)   # 0–1
    score_0_100 = int(round(base_score * 100))

    return score_0_100


# -----------------------------
# 4) UI
# -----------------------------

sex_label = st.selectbox("👦👧 What is your child's gender?", list(sex_options.keys()))
sex = sex_options[sex_label]

age = st.selectbox("🎂 How old is your child?", list(range(10, 17)))

soft_drinks = st.selectbox(
    "🥤 How many times a week does your child drink soft drinks?",
    soft_drinks_labels
)

sweets = st.selectbox(
    "🍬 How many times a week does your child eat sweets?",
    sweets_labels
)

vegetables = st.selectbox(
    "🥦 How many times a week does your child eat vegetables?",
    vegetables_labels
)

friend_talk = st.selectbox(
    "🗣️ Your child can talk with friends about their problems.",
    friend_talk_labels
)

feel_low = st.selectbox(
    "😔 How often does your child feel low or sad?",
    feellow_labels
)

phys = st.selectbox(
    "🏃‍♂️ On how many days per week is your child physically active for at least 60 minutes?",
    phys_labels
)

breakfast = st.selectbox(
    "🍽️ On how many schooldays does your child usually eat breakfast?",
    breakfast_labels
)

teeth = st.selectbox(
    "🦷 How often does your child brush their teeth?",
    tooth_labels
)

talk_father = st.selectbox(
    "👨‍👧 How easy is it for your child to talk to their father about their problems?",
    talkfather_labels
)

# -----------------------------
# 5) COMPUTE - BAROMETER ONLY
# -----------------------------
if st.button("🔍 Evaluate"):
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
        "TALK_FATHER": extract_number(talk_father)
    }

    score = compute_risk_score(user_data)   # 0–100
    risk_ratio = score / 100               # 0–1
    arrow_pct = 2 + 96 * risk_ratio 

    st.write("### Behaviour Risk Meter")

    bar_html = f"""
    <div style="
        width: 100%;
        height: 35px;
        background: linear-gradient(to right, 
            #4caf50 0%,
            #ffeb3b 50%,
            #f44336 100%
        );
        border-radius: 8px;
        position: relative;
    ">
        <div style="
            position: absolute;
            left: calc({arrow_pct}% - 10px);
            top: -8px;
            font-size: 26px;
        ">⬆</div>
    </div>

    <p style="text-align:center; font-size:14px; margin-top:4px;">
        Lifestyle risk score: <b>{score}</b> / 100
    </p>
    """

    st.markdown(bar_html, unsafe_allow_html=True)


# AI DOPORUCENI

    st.write("---")
    st.subheader("📊 Recommendation")

    API_KEY = st.secrets.get("OPENAI_API_KEY")

    if not API_KEY:
        st.info("AI recommendation is not available because the API key is not configured.")
    else:
        SYSTEM_PROMPT = """
You are a very supportive health coach for parents, focused to prevent obesity and/or overweight, that's your primary goal. 
You receive a short profile of a child, including sex, age, a lifestyle risk score (0-100)
and a description of daily habits (diet, physical activity, emotional state, hygiene).

Your task:
- Pick up on answers which are most disturbing but also pick up on those most positive and give the parents a cheer up for good work.
- Explain in simple, encouraging language what the main concerns are.
- While giving recommendations, focus ONLY on lifestyle and habits, NOT on diagnosing obesity or giving medical treatment.
- Give 2-3 concrete, practical tips the parents can start with in everyday life 
  (meals, drinks, movement, routines, screen time, sleep, family habits).

Background information from the study:
- Boys had roughly 1.6-1.7 times higher rates of overweight than girls.
- Younger children around 11 years had somewhat higher risk than older teenagers.

Therefore:
- Be slightly more cautious and proactive in your advice for younger boys with high risk scores.
- For girls and older teens, still give clear advice, but avoid exaggerating the risk.

Always stay kind, non-judgmental and supportive.
Never give exact probabilities or medical diagnoses.
Do not ask what you can do next. Give only one time recommendations, that's it.
"""

        if score < 30:
            risk_level = "low"
        elif score < 60:
            risk_level = "medium"
        else:
            risk_level = "high"

        user_summary = f"""
Child profile:
- Sex: {sex_label}
- Age: {age}
- Lifestyle risk score: {score}/100 ({risk_level} risk)

Habits:
- Soft drinks: {soft_drinks_labels[user_data['SOFT_DRINKS'] - 1]}
- Sweets: {sweets_labels[user_data['SWEETS'] - 1]}
- Vegetables: {vegetables_labels[user_data['VEGETABLES'] - 1]}
- Physical activity (60+ min): {phys_labels[user_data['PHYS_ACT_60'] - 1]}
- Breakfast on schooldays: {breakfast_labels[user_data['BREAKFAST_WEEKDAYS'] - 1]}
- Tooth brushing: {tooth_labels[user_data['TOOTH_BRUSHING'] - 1]}
- Feeling low: {feellow_labels[user_data['FEEL_LOW'] - 1]}
- Talking with friends: {friend_talk_labels[user_data['FRIEND_TALK'] - 1]}
- Talking to father: {talkfather_labels[user_data['TALK_FATHER'] - 1]}
"""

        client = OpenAI(api_key=API_KEY)

        try:
            response = client.responses.create(
                model="gpt-5-nano",  
                input=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_summary},
                ],
            )

            
            try:
                recommendation_text = response.output[0].content[0].text
            except Exception:
                recommendation_text = getattr(response, "output_text", "I could not parse the response text.")

            st.write(recommendation_text)

        except Exception as e:
            st.error("Sorry, there was an error while generating the recommendation.")
            st.text(str(e))
