import requests
import pickle
import streamlit as st
from streamlit_chat import message

# Hugging Face API Setup
HF_API_KEY = "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"
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

# Load ML Models
diabetes_model = pickle.load(open('diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open('heart_disease_model.sav','rb'))
parkinsons_model = pickle.load(open('parkinsons_model.sav', 'rb'))

# Streamlit Chatbot UI
st.set_page_config(page_title="AI Health Chatbot", page_icon="💬")
st.title("AI Health Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for i, msg in enumerate(st.session_state["messages"]):
    message(msg["content"], is_user=msg["is_user"], key=f"msg_{i}")

# User selects disease type
disease = st.selectbox("Which disease would you like to check?", ["Diabetes", "Heart Disease", "Parkinson's"])

# Collect user inputs dynamically
inputs = {}
if disease == "Diabetes":
    inputs["Pregnancies"] = st.number_input("Number of Pregnancies", min_value=0, step=1)
    inputs["Glucose"] = st.number_input("Glucose Level", min_value=0)
    inputs["BloodPressure"] = st.number_input("Blood Pressure", min_value=0)
    inputs["SkinThickness"] = st.number_input("Skin Thickness", min_value=0)
    inputs["Insulin"] = st.number_input("Insulin Level", min_value=0)
    inputs["BMI"] = st.number_input("BMI", min_value=0.0, format="%.2f")
    inputs["DiabetesPedigreeFunction"] = st.number_input("Diabetes Pedigree Function", min_value=0.0, format="%.2f")
    inputs["Age"] = st.number_input("Age", min_value=0, step=1)
    model = diabetes_model
    feature_order = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]

elif disease == "Heart Disease":
    inputs["Age"] = st.number_input("Age", min_value=0, step=1)
    inputs["Sex"] = st.selectbox("Sex", options=["Male", "Female"])
    inputs["ChestPain"] = st.number_input("Chest Pain Type", min_value=0, max_value=3)
    inputs["RestingBP"] = st.number_input("Resting Blood Pressure", min_value=0)
    inputs["Cholesterol"] = st.number_input("Cholesterol", min_value=0)
    inputs["FastingBS"] = st.selectbox("Fasting Blood Sugar > 120 mg/dl", options=["No", "Yes"])
    inputs["RestECG"] = st.number_input("Resting ECG Results", min_value=0, max_value=2)
    inputs["MaxHR"] = st.number_input("Maximum Heart Rate", min_value=0)
    inputs["ExerciseAngina"] = st.selectbox("Exercise-Induced Angina", options=["No", "Yes"])
    inputs["Oldpeak"] = st.number_input("ST Depression", min_value=0.0, format="%.2f")
    inputs["ST_Slope"] = st.number_input("Slope of Peak Exercise ST Segment", min_value=0, max_value=2)
    model = heart_disease_model
    feature_order = ["Age", "Sex", "ChestPain", "RestingBP", "Cholesterol", "FastingBS", "RestECG", "MaxHR", "ExerciseAngina", "Oldpeak", "ST_Slope"]

elif disease == "Parkinson's":
    inputs["Fo"] = st.number_input("MDVP:Fo(Hz)", min_value=0.0, format="%.2f")
    inputs["Fhi"] = st.number_input("MDVP:Fhi(Hz)", min_value=0.0, format="%.2f")
    inputs["Flo"] = st.number_input("MDVP:Flo(Hz)", min_value=0.0, format="%.2f")
    inputs["Jitter_percent"] = st.number_input("Jitter(%)", min_value=0.0, format="%.4f")
    inputs["Jitter_Abs"] = st.number_input("Jitter(Abs)", min_value=0.0, format="%.4f")
    inputs["Shimmer"] = st.number_input("Shimmer", min_value=0.0, format="%.4f")
    inputs["Shimmer_dB"] = st.number_input("Shimmer(dB)", min_value=0.0, format="%.4f")
    inputs["HNR"] = st.number_input("HNR", min_value=0.0, format="%.2f")
    inputs["RPDE"] = st.number_input("RPDE", min_value=0.0, format="%.4f")
    inputs["DFA"] = st.number_input("DFA", min_value=0.0, format="%.4f")
    model = parkinsons_model
    feature_order = ["Fo", "Fhi", "Flo", "Jitter_percent", "Jitter_Abs", "Shimmer", "Shimmer_dB", "HNR", "RPDE", "DFA"]

if st.button("Predict"):
    input_values = [[inputs[feature] for feature in feature_order]]
    prediction = model.predict(input_values)
    result = "You have the disease." if prediction[0] == 1 else "You do not have the disease."
    st.success(result)

    # Generate suggestions from Hugging Face API
    suggestion = ask_huggingface(f"Provide health suggestions for {disease}.")
    st.info(suggestion)
