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

# Function to query Hugging Face API
def ask_huggingface(prompt):
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()[0]["generated_text"]

# Streamlit Chatbot UI
st.set_page_config(page_title="AI Health Chatbot", page_icon="\ud83d\udcac", layout="wide")
st.title("\ud83e\ude7a AI Health Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "state" not in st.session_state:
    st.session_state["state"] = "initial"
if "inputs" not in st.session_state:
    st.session_state["inputs"] = {}

# Display chat history
for i, msg in enumerate(st.session_state["messages"]):
    message(msg["content"], is_user=msg["is_user"], key=f"msg_{i}")

# User input
user_input = st.text_input("Describe your symptoms or ask a question:", key="user_input")

if user_input:
    st.session_state["messages"].append({"content": user_input, "is_user": True})

    # Step 1: Determine if it relates to a disease
    response = ask_huggingface(f"Does this question relate to diabetes, heart disease, or Parkinson's: {user_input}")
    
    if "diabetes" in response.lower():
        st.session_state["state"] = "diabetes_questions"
        response = "I will now ask you some questions to predict diabetes. How many times have you been pregnant? (Enter 0 if male)"
        st.session_state["current_question"] = "Pregnancies"
    elif "heart" in response.lower():
        st.session_state["state"] = "heart_questions"
        response = "Let's check for heart disease. What is your age?"
        st.session_state["current_question"] = "Age"
    elif "parkinson" in response.lower():
        st.session_state["state"] = "parkinsons_questions"
        response = "Let's check for Parkinson's. What is your MDVP:Fo(Hz) value?"
        st.session_state["current_question"] = "Fo"
    else:
        response = ask_huggingface(user_input)  # Generic AI response
    
    st.session_state["messages"].append({"content": response, "is_user": False})
    message(response, is_user=False, key=f"response_{len(st.session_state['messages'])}")

# Collect user responses for predictions
if st.session_state["state"] in ["diabetes_questions", "heart_questions", "parkinsons_questions"]:
    question = st.session_state["current_question"]
    user_answer = st.text_input(f"{question}:", key="answer_input")

    if user_answer:
        try:
            st.session_state["inputs"][question] = float(user_answer)
            next_question = None
            
            if st.session_state["state"] == "diabetes_questions":
                questions = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]
            elif st.session_state["state"] == "heart_questions":
                questions = ["Sex", "ChestPain", "RestingBP", "Cholesterol", "FastingBS", "RestECG", "MaxHR", "ExerciseAngina", "Oldpeak", "ST_Slope"]
            elif st.session_state["state"] == "parkinsons_questions":
                questions = ["Fhi", "Flo", "Jitter_percent", "Jitter_Abs", "Shimmer", "Shimmer_dB", "HNR", "RPDE", "DFA"]

            for q in questions:
                if q not in st.session_state["inputs"]:
                    next_question = q
                    break

            if next_question:
                st.session_state["current_question"] = next_question
                response = f"{next_question}?"
            else:
                # Make prediction
                if st.session_state["state"] == "diabetes_questions":
                    model = diabetes_model
                elif st.session_state["state"] == "heart_questions":
                    model = heart_disease_model
                else:
                    model = parkinsons_model
                
                features = [st.session_state["inputs"][q] for q in questions]
                prediction = model.predict([features])
                response = "You have the disease." if prediction[0] == 1 else "You do not have the disease."
                
                # Reset state
                st.session_state["state"] = "initial"
                st.session_state["inputs"] = {}
            
            st.session_state["messages"].append({"content": response, "is_user": False})
            message(response, is_user=False, key=f"response_{len(st.session_state['messages'])}")
        except ValueError:
            st.write("Please enter a valid number.")
