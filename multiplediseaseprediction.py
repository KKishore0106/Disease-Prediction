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
st.set_page_config(page_title="AI Health Chatbot", page_icon="💬", layout="wide")
st.title("🤖 AI Health Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "state" not in st.session_state:
    st.session_state["state"] = "initial"
if "inputs" not in st.session_state:
    st.session_state["inputs"] = {}

# Display chat history
for i, msg in enumerate(st.session_state["messages"]):
    message(msg["content"], is_user=msg["is_user"], key=f"msg_{i}")

# Ask which disease to predict
if st.session_state["state"] == "initial":
    st.write("Which disease do you want to predict?")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Diabetes 🩸"):
            st.session_state["state"] = "diabetes_questions"
            st.session_state["questions"] = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]
            st.session_state["model"] = diabetes_model
    with col2:
        if st.button("Heart Disease ❤️"):
            st.session_state["state"] = "heart_questions"
            st.session_state["questions"] = ["Age", "Sex", "ChestPain", "RestingBP", "Cholesterol", "FastingBS", "RestECG", "MaxHR", "ExerciseAngina", "Oldpeak", "ST_Slope"]
            st.session_state["model"] = heart_disease_model
    with col3:
        if st.button("Parkinson's 🧠"):
            st.session_state["state"] = "parkinsons_questions"
            st.session_state["questions"] = ["Fo", "Fhi", "Flo", "Jitter_percent", "Jitter_Abs", "Shimmer", "Shimmer_dB", "HNR", "RPDE", "DFA"]
            st.session_state["model"] = parkinsons_model
    st.stop()

# Ask questions interactively
questions = st.session_state["questions"]
current_index = st.session_state.get("current_question_index", 0)

if current_index < len(questions):
    question = questions[current_index]
    user_answer = st.text_input(f"{question}:", key=f"answer_{current_index}")
    
    if user_answer:
        try:
            st.session_state["inputs"][question] = float(user_answer)
            st.session_state["current_question_index"] += 1
            st.experimental_rerun()
        except ValueError:
            st.write("Please enter a valid number.")
else:
    # Make prediction
    model = st.session_state["model"]
    features = [st.session_state["inputs"][q] for q in questions]
    prediction = model.predict([features])
    result = "You have the disease." if prediction[0] == 1 else "You do not have the disease."
    
    # Get AI-generated suggestion
    suggestion = ask_huggingface(f"Give health advice for {st.session_state['state']} prevention and management.")
    response = f"{result}\n\n**Suggestion:** {suggestion}"
    
    # Reset state
    st.session_state["state"] = "initial"
    st.session_state["inputs"] = {}
    st.session_state["questions"] = []
    st.session_state["current_question_index"] = 0
    
    st.session_state["messages"].append({"content": response, "is_user": False})
    message(response, is_user=False, key=f"response_{len(st.session_state['messages'])}")
