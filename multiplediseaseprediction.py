import streamlit as st
import pickle
import requests
from streamlit_chat import message

# Hugging Face API Setup
HF_API_KEY = "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"
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

# Load ML Models
diabetes_model = pickle.load(open('diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open('heart_disease_model.sav', 'rb'))
parkinsons_model = pickle.load(open('parkinsons_model.sav', 'rb'))

def ask_ai(prompt):
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()["generated_text"]

st.set_page_config(page_title="Health AI Chatbot", page_icon="💬")
st.title("🤖 AI Health Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi! Which disease would you like to check?"}]
    st.session_state["state"] = "select_disease"
    st.session_state["inputs"] = {}

for msg in st.session_state["messages"]:
    message(msg["content"], is_user=(msg["role"] == "user"))

if st.session_state["state"] == "select_disease":
    disease = st.radio("Select a disease:", ["Diabetes", "Heart Disease", "Parkinson's"], key="disease")
    if st.button("Next"):
        if disease == "Diabetes":
            st.session_state["questions"] = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]
            st.session_state["model"] = diabetes_model
        elif disease == "Heart Disease":
            st.session_state["questions"] = ["Age", "Sex", "ChestPain", "RestingBP", "Cholesterol", "FastingBS", "RestECG", "MaxHR", "ExerciseAngina", "Oldpeak", "ST_Slope"]
            st.session_state["model"] = heart_disease_model
        else:
            st.session_state["questions"] = ["Fo", "Fhi", "Flo", "Jitter_percent", "Jitter_Abs", "Shimmer", "Shimmer_dB", "HNR", "RPDE", "DFA"]
            st.session_state["model"] = parkinsons_model
        
        st.session_state["state"] = "ask_questions"
        st.session_state["current_question_index"] = 0
        st.experimental_rerun()

elif st.session_state["state"] == "ask_questions":
    index = st.session_state["current_question_index"]
    if index < len(st.session_state["questions"]):
        question = st.session_state["questions"][index]
        user_input = st.text_input(f"{question}:", key=f"input_{index}")
        
        if user_input:
            try:
                st.session_state["inputs"][question] = float(user_input)
                st.session_state["current_question_index"] += 1
                st.experimental_rerun()
            except ValueError:
                st.error("Please enter a valid number.")
    else:
        model = st.session_state["model"]
        features = [st.session_state["inputs"][q] for q in st.session_state["questions"]]
        prediction = model.predict([features])
        result = "You have the disease." if prediction[0] == 1 else "You do not have the disease."
        suggestion = ask_ai(f"Give health advice for {st.session_state['state']} prevention and management.")
        response = f"{result}\n\n**Suggestion:** {suggestion}"
        st.session_state["messages"].append({"role": "assistant", "content": response})
        
        st.session_state["state"] = "select_disease"
        st.session_state["inputs"] = {}
        st.session_state["questions"] = []
        st.session_state["current_question_index"] = 0
        st.experimental_rerun()
