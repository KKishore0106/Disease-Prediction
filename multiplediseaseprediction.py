import pickle
import streamlit as st
from streamlit_option_menu import option_menu

# Load the saved models
diabetes_model = pickle.load(open('diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open('heart_disease_model.sav','rb'))
parkinsons_model = pickle.load(open('parkinsons_model.sav', 'rb'))

# Set page config
st.set_page_config(page_title="Healthcare Prediction System", page_icon="🩺", layout="wide")

# Custom styling
st.markdown(
    """
    <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            padding: 10px;
            font-size: 18px;
        }
        .stSidebar {
            background-color: #f0f2f6;
            padding: 20px;
        }
        .main-container {
            background: url('https://source.unsplash.com/1600x900/?healthcare,hospital') no-repeat center center fixed;
            background-size: cover;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for navigation
with st.sidebar:
    st.image("https://source.unsplash.com/400x200/?medical")
    selected = option_menu(
        'Healthcare Prediction System',
        ['Diabetes Prediction', 'Heart Disease Prediction', 'Parkinsons Prediction'],
        icons=['activity', 'heart', 'person'],
        default_index=0
    )

st.title("🩺 Healthcare Prediction System")

# Diabetes Prediction Page
if selected == 'Diabetes Prediction':
    st.subheader('Diabetes Prediction')
    col1, col2, col3 = st.columns(3)
    with col1:
        Pregnancies = st.number_input('Number of Pregnancies', min_value=0, step=1)
    with col2:
        Glucose = st.number_input('Glucose Level', min_value=0)
    with col3:
        BloodPressure = st.number_input('Blood Pressure value', min_value=0)
    with col1:
        SkinThickness = st.number_input('Skin Thickness value', min_value=0)
    with col2:
        Insulin = st.number_input('Insulin Level', min_value=0)
    with col3:
        BMI = st.number_input('BMI value', min_value=0.0, format='%.2f')
    with col1:
        DiabetesPedigreeFunction = st.number_input('Diabetes Pedigree Function value', min_value=0.0, format='%.2f')
    with col2:
        Age = st.number_input('Age of the Person', min_value=0, step=1)
    
    diab_diagnosis = ''
    if st.button('Predict Diabetes'):
        diab_prediction = diabetes_model.predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
        diab_diagnosis = 'The person is diabetic' if diab_prediction[0] == 1 else 'The person is not diabetic'
    st.success(diab_diagnosis)

# Similar structure for Heart Disease Prediction and Parkinson's Prediction... (modify accordingly with number_input)

# Footer
st.markdown(
    """
    <footer style='text-align: center; padding: 20px; background-color: #f0f2f6;'>
        <p>Developed by Kishore | Connect on <a href='https://www.linkedin.com' target='_blank'>LinkedIn</a> | <a href='https://github.com' target='_blank'>GitHub</a></p>
    </footer>
    """,
    unsafe_allow_html=True
)
