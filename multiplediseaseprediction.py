import streamlit as st
import pickle
import ollama

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

def chat_with_gemma(prompt):
    try:
        response = ollama.chat(model="gemma:2b", messages=[{"role": "user", "content": prompt}])
        return response.get("message", {}).get("content", "Sorry, I couldn't process that.")
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"

def generate_suggestion(disease_name, risk_level, input_values):
    prompt = f"User input values: {input_values}\nRisk Level: {risk_level}\nProvide personalized health suggestions for {disease_name} in a friendly tone."
    return chat_with_gemma(prompt)

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
    elif st.session_state.step == 0:
        diseases = ["Diabetes", "Heart Disease", "Parkinson's"]
        for disease in diseases:
            if disease.lower() in prompt.lower():
                st.session_state.disease_name = disease
                st.session_state.step = 1
                st.session_state.input_values = {}
                st.session_state.current_field = None
                st.session_state.messages.append({"role": "assistant", "content": f"Alright! Let's check your {disease} risk. I'll ask a few questions."})
                st.rerun()
        st.session_state.messages.append({"role": "assistant", "content": "Which condition would you like to check? (Diabetes, Heart Disease, Parkinson's)"})

elif st.session_state.step == 1:
    disease_fields = {
        "Diabetes": ["Pregnancy Count", "Glucose Level", "Blood Pressure", "Skin Thickness (mm)", "Insulin Level", "BMI", "Diabetes Pedigree Function", "Age"],
        "Heart Disease": ["Age", "Sex", "Chest Pain Type", "Resting Blood Pressure", "Serum Cholesterol", "Fasting Blood Sugar", "Resting ECG Result", "Max Heart Rate", "Exercise-Induced Angina", "ST Depression", "Slope of ST", "Major Vessels", "Thalassemia"],
        "Parkinson's": ["MDVP:Fo(Hz)", "MDVP:Fhi(Hz)", "MDVP:Flo(Hz)", "MDVP:Jitter(%)", "MDVP:Jitter(Abs)", "MDVP:RAP", "MDVP:PPQ", "Jitter:DDP", "MDVP:Shimmer", "MDVP:Shimmer(dB)"]
    }
    fields = disease_fields[st.session_state.disease_name]
    
    if st.session_state.current_field is None:
        st.session_state.current_field = fields[0]
    
    st.session_state.messages.append({"role": "assistant", "content": st.session_state.current_field})
    
    if prompt:
        try:
            st.session_state.input_values[st.session_state.current_field] = float(prompt)
            if len(st.session_state.input_values) < len(fields):
                st.session_state.current_field = fields[len(st.session_state.input_values)]
            else:
                st.session_state.step = 2
                diagnosis, risk_level = get_prediction(st.session_state.disease_name, st.session_state.input_values)
                st.session_state.messages.append({"role": "assistant", "content": diagnosis})
                st.session_state.step = 3
        except ValueError:
            st.session_state.messages.append({"role": "assistant", "content": "⚠️ Please enter a valid number."})

st.rerun()

