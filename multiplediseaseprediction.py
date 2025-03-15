import pickle
import streamlit as st
from streamlit_chat import message
from transformers import pipeline

# Load LLM from Hugging Face (Mistral-7B)
llm = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct", tokenizer="mistralai/Mistral-7B-Instruct")

# Load prediction models
diabetes_model = pickle.load(open('diabetes_model.sav', 'rb'))

st.set_page_config(page_title="AI Health Chatbot", page_icon="💬", layout="wide")
st.title("🤖 AI Health Chatbot")

# Initialize session state for conversation
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
user_input = st.text_input("Describe your symptoms:", key="user_input")

if user_input:
    st.session_state["messages"].append({"content": user_input, "is_user": True})

    # Step 1: Check if symptoms suggest diabetes
    if st.session_state["state"] == "initial":
        prompt = f"Based on the user's input: '{user_input}', do they have symptoms of diabetes?"
        response = llm(prompt, max_length=150)[0]["generated_text"]

        if "yes" in response.lower():
            response += "\nIt looks like your symptoms might be related to **Diabetes**. Let’s check further. I'll ask you a few questions."
            st.session_state["state"] = "asking_questions"
        else:
            response += "\nYour symptoms don’t seem strongly linked to diabetes, but it's always good to consult a doctor."

    # Step 2: Ask follow-up questions
    elif st.session_state["state"] == "asking_questions":
        questions = {
            "Pregnancies": "How many times have you been pregnant? (Enter 0 if male)",
            "Glucose": "What is your glucose level?",
            "BloodPressure": "What is your blood pressure value?",
            "SkinThickness": "What is your skin thickness measurement?",
            "Insulin": "What is your insulin level?",
            "BMI": "What is your BMI value?",
            "DiabetesPedigreeFunction": "What is your diabetes pedigree function value?",
            "Age": "How old are you?"
        }

        unanswered = [q for q in questions if q not in st.session_state["inputs"]]
        if unanswered:
            question = unanswered[0]
            response = questions[question]
            st.session_state["state"] = "collecting_data"
            st.session_state["current_question"] = question
        else:
            st.session_state["state"] = "predicting"

    # Step 3: Collect user responses
    elif st.session_state["state"] == "collecting_data":
        question = st.session_state["current_question"]
        try:
            value = float(user_input)
            st.session_state["inputs"][question] = value
            response = "Noted! Let's move to the next question."
            st.session_state["state"] = "asking_questions"
        except ValueError:
            response = "Please enter a valid number."

    # Step 4: Make prediction
    elif st.session_state["state"] == "predicting":
        features = [st.session_state["inputs"][q] for q in [
            "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
            "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"
        ]]
        prediction = diabetes_model.predict([features])
        response = "You **have diabetes**." if prediction[0] == 1 else "You **do not have diabetes**."

        # Reset conversation
        st.session_state["state"] = "initial"
        st.session_state["inputs"] = {}

    # Display chatbot response
    st.session_state["messages"].append({"content": response, "is_user": False})
    message(response, is_user=False, key=f"response_{len(st.session_state['messages'])}")
