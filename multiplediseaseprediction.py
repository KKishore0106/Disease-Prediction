import streamlit as st
import pickle
import requests
import time

# Hugging Face API Setup for Health Suggestions
HF_API_KEY = "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"
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

# Load ML Models
diabetes_model = pickle.load(open('diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open('heart_disease_model.sav', 'rb'))
parkinsons_model = pickle.load(open('parkinsons_model.sav', 'rb'))

def ask_ai(prompt):
    """ Get AI-generated health suggestions. """
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json().get("generated_text", "I'm not sure. Can you try rephrasing?")

# Set Page Config
st.set_page_config(page_title="ChatGPT-Style Health Bot", page_icon="💬")

# Load CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Chat UI
st.title("🩺 AI Health Chatbot")
st.write("Predict diseases and get AI-generated health advice.")

# Disease Selection
disease = st.selectbox("Which disease do you want to check?", ["Diabetes", "Heart Disease", "Parkinson’s"])

if disease == "Diabetes":
    st.subheader("🔹 Enter Your Diabetes Test Values")
    pregnancies = st.number_input("Pregnancies", min_value=0)
    glucose = st.number_input("Glucose Level", min_value=0)
    blood_pressure = st.number_input("Blood Pressure", min_value=0)
    skin_thickness = st.number_input("Skin Thickness", min_value=0)
    insulin = st.number_input("Insulin Level", min_value=0)
    bmi = st.number_input("BMI", min_value=0.0)
    dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0)
    age = st.number_input("Age", min_value=0)

    if st.button("Predict Diabetes"):
        features = [[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]]
        prediction = diabetes_model.predict(features)
        result = "You have Diabetes." if prediction[0] == 1 else "You do not have Diabetes."
        advice = ask_ai("Give health advice for diabetes prevention and management.")
        st.success(f"🔹 **Result:** {result}\n\n💡 **Suggestion:** {advice}")

elif disease == "Heart Disease":
    st.subheader("🔹 Enter Your Heart Test Values")
    age = st.number_input("Age", min_value=0)
    sex = st.selectbox("Sex", ["Male", "Female"])
    chest_pain = st.number_input("Chest Pain Type", min_value=0)
    resting_bp = st.number_input("Resting Blood Pressure", min_value=0)
    cholesterol = st.number_input("Cholesterol Level", min_value=0)
    fasting_bs = st.number_input("Fasting Blood Sugar", min_value=0)
    rest_ecg = st.number_input("Resting ECG", min_value=0)
    max_hr = st.number_input("Max Heart Rate", min_value=0)
    exercise_angina = st.selectbox("Exercise-Induced Angina", ["Yes", "No"])
    oldpeak = st.number_input("ST Depression", min_value=0.0)
    st_slope = st.number_input("ST Slope", min_value=0)

    if st.button("Predict Heart Disease"):
        features = [[age, 1 if sex == "Male" else 0, chest_pain, resting_bp, cholesterol, fasting_bs, rest_ecg, max_hr, 1 if exercise_angina == "Yes" else 0, oldpeak, st_slope]]
        prediction = heart_disease_model.predict(features)
        result = "You have Heart Disease." if prediction[0] == 1 else "You do not have Heart Disease."
        advice = ask_ai("Give health advice for heart disease prevention and management.")
        st.success(f"🔹 **Result:** {result}\n\n💡 **Suggestion:** {advice}")

else:
    st.subheader("🔹 Enter Your Parkinson’s Test Values")
    fo = st.number_input("Fo (Hz)", min_value=0.0)
    fhi = st.number_input("Fhi (Hz)", min_value=0.0)
    flo = st.number_input("Flo (Hz)", min_value=0.0)
    jitter_percent = st.number_input("Jitter (%)", min_value=0.0)
    jitter_abs = st.number_input("Jitter (Abs)", min_value=0.0)
    shimmer = st.number_input("Shimmer", min_value=0.0)
    shimmer_db = st.number_input("Shimmer (dB)", min_value=0.0)
    hnr = st.number_input("HNR", min_value=0.0)
    rpde = st.number_input("RPDE", min_value=0.0)
    dfa = st.number_input("DFA", min_value=0.0)

    if st.button("Predict Parkinson’s Disease"):
        features = [[fo, fhi, flo, jitter_percent, jitter_abs, shimmer, shimmer_db, hnr, rpde, dfa]]
        prediction = parkinsons_model.predict(features)
        result = "You have Parkinson’s Disease." if prediction[0] == 1 else "You do not have Parkinson’s Disease."
        advice = ask_ai("Give health advice for Parkinson’s disease prevention and management.")
        st.success(f"🔹 **Result:** {result}\n\n💡 **Suggestion:** {advice}")

