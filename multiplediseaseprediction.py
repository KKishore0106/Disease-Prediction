import pickle
import streamlit as st
from streamlit_chat import message
from transformers import pipeline

# Load Hugging Face Model for text classification
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Load models
diabetes_model = pickle.load(open('diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open('heart_disease_model.sav', 'rb'))
parkinsons_model = pickle.load(open('parkinsons_model.sav', 'rb'))

st.set_page_config(page_title="Health Chatbot", page_icon="💬", layout="wide")
st.title("🩺 Health Prediction Chatbot")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history with unique keys
for i, msg in enumerate(st.session_state["messages"]):
    message(msg["content"], is_user=msg["is_user"], key=f"msg_{i}")

# User input
user_input = st.text_input("Describe your symptoms:", key="user_input")

if user_input:
    # Add user message
    st.session_state["messages"].append({"content": user_input, "is_user": True})

    # Use Hugging Face model to classify input
    labels = ["Diabetes", "Heart Disease", "Parkinson's"]
    result = classifier(user_input, labels)
    disease = result["labels"][0]  # Highest confidence label

    response = f"Based on your input, I suspect you might be asking about **{disease}**. Please enter your details for a prediction."

    if disease == "Diabetes":
        Pregnancies = st.number_input('Number of Pregnancies', min_value=0, step=1)
        Glucose = st.number_input('Glucose Level', min_value=0)
        BloodPressure = st.number_input('Blood Pressure value', min_value=0)
        SkinThickness = st.number_input('Skin Thickness value', min_value=0)
        Insulin = st.number_input('Insulin Level', min_value=0)
        BMI = st.number_input('BMI value', min_value=0.0, format='%.2f')
        DiabetesPedigreeFunction = st.number_input('Diabetes Pedigree Function value', min_value=0.0, format='%.2f')
        Age = st.number_input('Age of the Person', min_value=0, step=1)

        if st.button("Predict"):
            prediction = diabetes_model.predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
            response = "You are diabetic." if prediction[0] == 1 else "You are not diabetic."

    elif disease == "Heart Disease":
        response = "I see you are asking about heart disease. Please enter your details for a prediction."
        # Add heart disease input fields here...

    elif disease == "Parkinson's":
        response = "I see you are asking about Parkinson’s. Please enter your details for a prediction."
        # Add Parkinson's input fields here...

    # Add chatbot response
    st.session_state["messages"].append({"content": response, "is_user": False})
    message(response, is_user=False, key=f"response_{len(st.session_state['messages'])}")
