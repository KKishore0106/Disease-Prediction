import pickle
import streamlit as st
from streamlit_option_menu import option_menu

# Load the saved models
diabetes_model = pickle.load(open('diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open('heart_disease_model.sav', 'rb'))
parkinsons_model = pickle.load(open('parkinsons_model.sav', 'rb'))

# Set page configuration
st.set_page_config(page_title='Healthcare Prediction System', page_icon='⚕️', layout='wide')

# Custom CSS for background and styling
st.markdown(
    """
    <style>
        body {
            background-image: url('https://source.unsplash.com/1600x900/?healthcare,medical');
            background-size: cover;
        }
        .stButton > button {
            background-color: #008080;
            color: white;
            font-size: 16px;
            padding: 10px;
        }
        .stButton > button:hover {
            background-color: #004d4d;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for navigation
with st.sidebar:
    selected = option_menu(
        'Healthcare Prediction System',
        ['Diabetes Prediction', 'Heart Disease Prediction', "Parkinson's Prediction"],
        icons=['activity', 'heart', 'person'],
        default_index=0
    )

st.title("⚕️ Healthcare Prediction System")

# Diabetes Prediction Page
if selected == 'Diabetes Prediction':
    st.subheader('Diabetes Prediction')
    
    col1, col2, col3 = st.columns(3)
    with col1:
        Pregnancies = st.number_input('Number of Pregnancies', min_value=0, step=1)
    with col2:
        Glucose = st.number_input('Glucose Level', min_value=0)
    with col3:
        BloodPressure = st.number_input('Blood Pressure')
    with col1:
        SkinThickness = st.number_input('Skin Thickness')
    with col2:
        Insulin = st.number_input('Insulin Level')
    with col3:
        BMI = st.number_input('BMI')
    with col1:
        DiabetesPedigreeFunction = st.number_input('Diabetes Pedigree Function')
    with col2:
        Age = st.number_input('Age', min_value=1, step=1)

    if st.button('Check Diabetes'):
        diab_prediction = diabetes_model.predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
        st.success('Diabetic' if diab_prediction[0] == 1 else 'Not Diabetic')

# Heart Disease Prediction Page
if selected == 'Heart Disease Prediction':
    st.subheader('Heart Disease Prediction')
    
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input('Age', min_value=1, step=1)
    with col2:
        sex = st.selectbox('Sex', ['Male', 'Female'])
    with col3:
        cp = st.number_input('Chest Pain Type', min_value=0)
    with col1:
        trestbps = st.number_input('Resting Blood Pressure')
    with col2:
        chol = st.number_input('Cholesterol')
    with col3:
        fbs = st.selectbox('Fasting Blood Sugar > 120 mg/dl', ['No', 'Yes'])
    with col1:
        restecg = st.number_input('Resting ECG')
    with col2:
        thalach = st.number_input('Max Heart Rate')
    with col3:
        exang = st.selectbox('Exercise Induced Angina', ['No', 'Yes'])
    with col1:
        oldpeak = st.number_input('ST Depression')
    with col2:
        slope = st.number_input('Slope of ST Segment')
    with col3:
        ca = st.number_input('Major Vessels Colored')
    with col1:
        thal = st.number_input('Thalassemia')
    
    if st.button('Check Heart Health'):
        heart_prediction = heart_disease_model.predict([[age, 1 if sex == 'Male' else 0, cp, trestbps, chol, 1 if fbs == 'Yes' else 0, restecg, thalach, 1 if exang == 'Yes' else 0, oldpeak, slope, ca, thal]])
        st.success('Heart Disease Detected' if heart_prediction[0] == 1 else 'No Heart Disease')

# Parkinson's Prediction Page
if selected == "Parkinson's Prediction":
    st.subheader("Parkinson's Disease Prediction")
    
    features = [
        st.number_input(label) for label in [
            'MDVP:Fo(Hz)', 'MDVP:Fhi(Hz)', 'MDVP:Flo(Hz)', 'MDVP:Jitter(%)',
            'MDVP:Jitter(Abs)', 'MDVP:RAP', 'MDVP:PPQ', 'Jitter:DDP',
            'MDVP:Shimmer', 'MDVP:Shimmer(dB)', 'Shimmer:APQ3', 'Shimmer:APQ5',
            'MDVP:APQ', 'Shimmer:DDA', 'NHR', 'HNR', 'RPDE', 'DFA', 'spread1', 'spread2', 'D2', 'PPE'
        ]
    ]
    
    if st.button("Check for Parkinson's"):
        parkinsons_prediction = parkinsons_model.predict([features])
        st.success("Has Parkinson's Disease" if parkinsons_prediction[0] == 1 else "No Parkinson's Disease")

# Footer
st.markdown(
    """
    <hr>
    <div style='text-align: center;'>
        <p style='font-size: 14px;'>
            Developed with ❤️ by Kishore | <a href='https://www.linkedin.com'>LinkedIn</a> | <a href='https://github.com'>GitHub</a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
