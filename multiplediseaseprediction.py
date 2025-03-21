import streamlit as st
import pickle
import requests

# Set page config at the very beginning
st.set_page_config(page_title="Medical AI Chatbot", layout="wide")

# Load the saved models with error handling
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
HF_API_TOKEN = "your_huggingface_api_token"
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"

headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}


def chat_with_mistral(prompt):
    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{MODEL_NAME}",
            headers=headers,
            json={"inputs": f"You are a medical AI chatbot. {prompt}"}
        )
        return response.json()[0]['generated_text']
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"


def generate_suggestion(disease_name, risk_level, input_values):
    prompt = f"User input values: {input_values}\nRisk Level: {risk_level}\nProvide personalized health suggestions for {disease_name} in a friendly tone."
    return chat_with_mistral(prompt)


def get_prediction(disease, input_values):
    try:
        input_data = [float(value) for value in input_values.values()]
        
        if disease == "Diabetes" and diabetes_model:
            prediction = diabetes_model.predict([input_data])[0][1]
            risk_level = "High" if prediction >= 0.7 else "Medium" if prediction >= 0.4 else "Low"
            diagnosis = f"Based on your inputs, your estimated risk level for diabetes is {risk_level} ({prediction * 100:.1f}% probability)."
        elif disease == "Heart Disease" and heart_disease_model:
            prediction = heart_disease_model.predict([input_data])[0]
            risk_level = "High" if prediction == 1 else "Low"
            diagnosis = f"Based on your inputs, you {'might have' if prediction == 1 else 'are at low risk for'} heart disease."
        elif disease == "Parkinson's" and parkinsons_model:
            prediction = parkinsons_model.predict([input_data])[0]
            risk_level = "High" if prediction == 1 else "Low"
            diagnosis = f"Based on your inputs, you {'might have' if prediction == 1 else 'are at low risk for'} Parkinson's."
        else:
            return "⚠️ Model not available.", None
        
        return diagnosis, risk_level
    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)}", None

# Streamlit UI
st.markdown("""
    <h1 style='text-align: center;'>🩺 AI Medical Chatbot</h1>
    <p style='text-align: center; font-size: 18px;'>Your friendly AI assistant for health predictions and advice.</p>
""", unsafe_allow_html=True)

# Initialize session state
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
        response = "Hello! 😊 How can I assist you with your health today?"
        st.session_state.messages.append({"role": "assistant", "content": response})
    else:
        response = chat_with_mistral(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})

st.rerun()


