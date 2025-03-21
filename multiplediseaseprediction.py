import streamlit as st
import pickle
import requests

# Set page config
st.set_page_config(page_title="Medical AI Chatbot", layout="wide")

# Load ML models
def load_model(filename):
    try:
        return pickle.load(open(filename, 'rb'))
    except Exception as e:
        st.error(f"Error loading {filename}: {e}")
        return None

diabetes_model = load_model('diabetes_model.sav')
heart_disease_model = load_model('heart_disease_model.sav')
parkinsons_model = load_model('parkinsons_model.sav')

# Hugging Face API setup
HF_API_TOKEN = "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"
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"
headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

def chat_with_mistral(prompt):
    """Calls Hugging Face API for AI-generated responses."""
    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{MODEL_NAME}",
            headers=headers,
            json={"inputs": f"You are a medical AI chatbot. {prompt}"}
        )
        return response.json()[0]['generated_text']
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"

# Disease input fields
disease_fields = {
    "Diabetes": ["Pregnancy Count", "Glucose Level", "Blood Pressure", "Skin Thickness (mm)", "Insulin Level", "BMI", "Diabetes Pedigree Function", "Age"],
    "Heart Disease": ["Age", "Sex", "Chest Pain Type", "Resting Blood Pressure", "Serum Cholesterol", "Fasting Blood Sugar", "Resting ECG Result", "Max Heart Rate", "Exercise-Induced Angina", "ST Depression", "Slope of ST", "Major Vessels", "Thalassemia"],
    "Parkinson's": ["MDVP:Fo(Hz)", "MDVP:Fhi(Hz)", "MDVP:Flo(Hz)", "MDVP:Jitter(%)", "MDVP:Jitter(Abs)", "MDVP:RAP", "MDVP:PPQ", "Jitter:DDP", "MDVP:Shimmer", "MDVP:Shimmer(dB)"]
}

def get_prediction(disease, input_values):
    """Runs the ML model for the given disease."""
    try:
        input_data = [float(value) for value in input_values.values()]
        if disease == "Diabetes" and diabetes_model:
            prediction = diabetes_model.predict([input_data])[0][1]
            risk_level = "High" if prediction >= 0.7 else "Medium" if prediction >= 0.4 else "Low"
        elif disease == "Heart Disease" and heart_disease_model:
            prediction = heart_disease_model.predict([input_data])[0]
            risk_level = "High" if prediction == 1 else "Low"
        elif disease == "Parkinson's" and parkinsons_model:
            prediction = parkinsons_model.predict([input_data])[0]
            risk_level = "High" if prediction == 1 else "Low"
        else:
            return "⚠️ Model not available.", None
        return f"Risk Level: {risk_level}", risk_level
    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)}", None

# Streamlit UI
st.markdown("""
    <h1 style='text-align: center;'>🩺 AI Medical Chatbot</h1>
    <p style='text-align: center; font-size: 18px;'>Your AI assistant for health predictions and advice.</p>
""", unsafe_allow_html=True)

# Chat state management
if "messages" not in st.session_state:
    st.session_state.messages = []
if "step" not in st.session_state:
    st.session_state.step = 0
if "disease_name" not in st.session_state:
    st.session_state.disease_name = None
if "input_values" not in st.session_state:
    st.session_state.input_values = {}
if "current_field" not in st.session_state:
    st.session_state.current_field = None
if "risk_level" not in st.session_state:
    st.session_state.risk_level = None

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🧑‍⚕️" if message["role"] == "assistant" else "🙂"):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("Type your health question here...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🙂"):
        st.markdown(prompt)

    if prompt.lower() in ["hi", "hello", "hiii", "hey"]:
         response = "Hello! 😊 Which disease do you want to check: Diabetes, Heart Disease, or Parkinson's?"
         st.session_state.step = 1

    elif st.session_state.step == 1 and prompt in disease_fields:
        st.session_state.disease_name = prompt
        st.session_state.input_values = {}
        st.session_state.current_field = 0
        response = f"Great! Let's check for {prompt}. Please enter your {disease_fields[prompt][0]}:"
        st.session_state.step = 2

    elif st.session_state.step == 2 and st.session_state.disease_name:
        field_name = disease_fields[st.session_state.disease_name][st.session_state.current_field]
        st.session_state.input_values[field_name] = prompt
        st.session_state.current_field += 1

        if st.session_state.current_field < len(disease_fields[st.session_state.disease_name]):
            response = f"Got it! Now enter your {disease_fields[st.session_state.disease_name][st.session_state.current_field]}:"
        else:
            diagnosis, risk_level = get_prediction(st.session_state.disease_name, st.session_state.input_values)
            st.session_state.risk_level = risk_level  # Store risk level in session state
            response = f"{diagnosis}\n\nWould you like some health suggestions? (yes/no)"
            st.session_state.step = 3

    elif st.session_state.step == 3 and prompt.lower() in ["yes", "y"]:
        if st.session_state.risk_level:  # Ensure risk_level is defined before using it
            response = chat_with_mistral(f"Provide health suggestions for {st.session_state.disease_name} with risk level {st.session_state.risk_level}.")
        else:
            response = "⚠️ Risk level is not available. Please redo the prediction."
        st.session_state.step = 0

    elif st.session_state.step == 3 and prompt.lower() in ["no", "n"]:
        response = "Okay! Let me know if you need anything else. 😊"
        st.session_state.step = 0  # Reset the chat

    else:
        response = chat_with_mistral(prompt)  # Only call AI when user asks open-ended questions

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant", avatar="🧑‍⚕️"):
        st.markdown(response)

st.rerun()

