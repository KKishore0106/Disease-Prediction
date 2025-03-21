import streamlit as st
import pickle
import requests

# **1️⃣ Set up page configuration**
st.set_page_config(page_title="Medical AI Chatbot", layout="wide")

# **2️⃣ Load ML Models (Optimized with Cache)**
@st.cache_resource
def load_model(filename):
    """Loads and caches the ML model to prevent reloading."""
    try:
        return pickle.load(open(filename, 'rb'))
    except Exception as e:
        st.error(f"Error loading {filename}: {e}")
        return None

diabetes_model = load_model('diabetes_model.sav')
heart_disease_model = load_model('heart_disease_model.sav')
parkinsons_model = load_model('parkinsons_model.sav')

# **3️⃣ Hugging Face API Setup (Cached)**
HF_API_TOKEN = "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"
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"
headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

@st.cache_data
def chat_with_mistral(prompt):
    """Calls Hugging Face API and caches responses."""
    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{MODEL_NAME}",
            headers=headers,
            json={"inputs": prompt}
        )
        data = response.json()
        return data[0]['generated_text'] if isinstance(data, list) else "⚠️ AI response error."
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"

# **4️⃣ Disease Fields**
disease_fields = {
    "Diabetes": ["Pregnancy Count", "Glucose Level", "Blood Pressure", "Skin Thickness (mm)", 
                 "Insulin Level", "BMI", "Diabetes Pedigree Function", "Age"],
    "Heart Disease": ["Age", "Sex", "Chest Pain Type", "Resting Blood Pressure", 
                      "Serum Cholesterol", "Fasting Blood Sugar", "Resting ECG Result", 
                      "Max Heart Rate", "Exercise-Induced Angina", "ST Depression", 
                      "Slope of ST", "Major Vessels", "Thalassemia"],
    "Parkinson's": ["MDVP:Fo(Hz)", "MDVP:Fhi(Hz)", "MDVP:Flo(Hz)", "MDVP:Jitter(%)", 
                    "MDVP:Jitter(Abs)", "MDVP:RAP", "MDVP:PPQ", "Jitter:DDP", 
                    "MDVP:Shimmer", "MDVP:Shimmer(dB)"]
}

# **5️⃣ Predict Function**
def get_prediction(disease, input_values):
    """Runs the ML model for the given disease and returns risk level."""
    try:
        input_data = [float(value) for value in input_values.values()]
        if disease == "Diabetes" and diabetes_model:
            prediction = diabetes_model.predict([input_data])[0][1]  # Probability for class 1
            risk_level = "High" if prediction >= 0.7 else "Medium" if prediction >= 0.4 else "Low"
        elif disease == "Heart Disease" and heart_disease_model:
            prediction = heart_disease_model.predict([input_data])[0]
            risk_level = "High" if prediction >= 0.7 else "Medium" if prediction >= 0.4 else "Low"
        elif disease == "Parkinson's" and parkinsons_model:
            prediction = parkinsons_model.predict([input_data])[0]
            risk_level = "High" if prediction >= 0.7 else "Medium" if prediction >= 0.4 else "Low"
        else:
            return "⚠️ Model not available.", None
        return f"Risk Level: {risk_level}", risk_level
    except ValueError:
        return "⚠️ Invalid input detected. Please enter numeric values only.", None
    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)}", None

# **6️⃣ Streamlit UI**
st.markdown("""
    <h1 style='text-align: center;'>🩺 AI Medical Chatbot</h1>
    <p style='text-align: center; font-size: 18px;'>Your AI assistant for health predictions and advice.</p>
""", unsafe_allow_html=True)

# **7️⃣ Initialize session state variables**
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
    st.session_state.risk_level = None  # Fixes "risk_level not defined" issue

# **8️⃣ Display chat history**
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🧑‍⚕️" if message["role"] == "assistant" else "🙂"):
        st.markdown(message["content"])

# **9️⃣ User input**
prompt = st.chat_input("Type your health question here...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🙂"):
        st.markdown(prompt)

    response = ""  # Initialize response

    # **Step 0: Initial greeting**
    if st.session_state.step == 0:
        if prompt.lower() in ["hi", "hello", "hiii", "hey"]:
            response = "Hello! 😊 Which disease do you want to check: Diabetes, Heart Disease, or Parkinson's?"
            st.session_state.step = 1
        else:
            response = chat_with_mistral(prompt)  # General questions

    # **Step 1: Selecting a disease**
    elif st.session_state.step == 1 and prompt in disease_fields:
        st.session_state.disease_name = prompt
        st.session_state.input_values = {}
        st.session_state.current_field = 0
        response = f"Great! Let's check for {prompt}. Please enter your {disease_fields[prompt][0]}:"
        st.session_state.step = 2

    # **Step 2: Collecting medical values**
    elif st.session_state.step == 2 and st.session_state.disease_name:
        if st.session_state.current_field is None:
            st.session_state.current_field = 0 
        
        field_name = disease_fields[st.session_state.disease_name][st.session_state.current_field]
        st.session_state.input_values[field_name] = prompt
        
        try:
            float(prompt)  # Ensure valid input
            st.session_state.current_field += 1

            if st.session_state.current_field < len(disease_fields[st.session_state.disease_name]):
                response = f"Got it! Now enter your {disease_fields[st.session_state.disease_name][st.session_state.current_field]}:"
            else:
                diagnosis, risk_level = get_prediction(st.session_state.disease_name, st.session_state.input_values)
                st.session_state.risk_level = risk_level  # Store risk level in session
                response = f"{diagnosis}\n\nWould you like some health suggestions? (yes/no)"
                st.session_state.step = 3
        except ValueError:
            response = "⚠️ Please enter a valid number."

    # **Step 3: Providing health suggestions**
    elif st.session_state.step == 3:
        if prompt.lower() in ["yes", "y"]:
            response = chat_with_mistral(f"Provide health suggestions for {st.session_state.disease_name} with risk level {st.session_state.risk_level}.")
        else:
            response = "Okay! Let me know if you need anything else. 😊"
        st.session_state.step = 0  # Reset the chat flow

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant", avatar="🧑‍⚕️"):
        st.markdown(response)

