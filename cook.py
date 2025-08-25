import streamlit as st
import os
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.runnables import RunnableLambda
import langchain.globals as lcg

lcg.set_verbose(True)

os.environ["GOOGLE_API_KEY"] = 'AIzaSyCeAynIIf2iBwD6M_Q-_WMUKcJ1bmz3EJQ'

generation_config = {"temperature": 0.6, "top_p": 1, "top_k": 1, "max_output_tokens": 2048}
model = GoogleGenerativeAI(model="gemini-1.5-flash", generation_config=generation_config)

prompt_template_resto = PromptTemplate(
    input_variables=['name', 'age', 'gender', 'weight', 'height', 'veg_or_nonveg', 'disease', 'region', 'state', 'allergics', 'foodtype'],
    template="Think you are a chef and fitness coach, given a person's height, weight, region, food type, and food allergy, provide the following information : BMI (and healthy BMI range), healthy weight for the height, BMI Prime, Ponderal Index, fat percentage, obese level (all this in headline font) and recommended diet plan with calories count, and grams for each meal, and then cooking procedure for each meal, please provide absolute results without mentioning the method."
             "Person name: {name}\n"
             "Person age: {age}\n"
             "Person gender: {gender}\n"
             "Person weight: {weight}\n"
             "Person height: {height}\n"
             "Person veg_or_nonveg: {veg_or_nonveg}\n"
             "Person generic disease: {disease}\n"
             "Person region: {region}\n"
             "Person state: {state}\n"
             "Person allergics: {allergics}\n"
             "Person foodtype: {foodtype}."
)

chain_resto = RunnableLambda(lambda inputs: prompt_template_resto.format(**inputs)) | model

st.markdown(
    f"""
    <style>
        .title {{
            font-size: 32px;
            font-weight: bold;
            font-family: 'Arial', sans-serif;
            text-align: center;
            color: #FFFFFF;
            margin-bottom: 20px;
            background: rgba(0, 0, 0, 0.5);
            padding: 10px;
            border-radius: 10px;
        }}
        .subtitle {{
            font-size: 20px;
            font-family: 'Helvetica', sans-serif;
            text-align: center;
            color: #FFFFFF;
            margin-bottom: 30px;
            background: rgba(0, 0, 0, 0.5);
            padding: 10px;
            border-radius: 10px;
        }}
        .form-label {{
            font-weight: bold;
            color: #FFFFFF;
        }}
        .form-input {{
            margin-bottom: 15px;
        }}
        .recommendations {{
            margin-top: 20px;
            font-family: 'Helvetica', sans-serif;
        }}
        .stButton button {{
            transition: background-color 0.3s, transform 0.3s;
        }}
        .stButton button:hover {{
            background-color: #4CAF50;
            transform: scale(1.05);
        }}
        .form-container {{
            background: rgba(255, 255, 255, 0.8);
            padding: 20px;
            border-radius: 10px;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="title">FITNEZZ-FIZZ</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">COOK your Personal DIET with AI</div>', unsafe_allow_html=True)

with st.form(key='user_input_form', clear_on_submit=True):
    st.markdown('<div class="form-label">Name:</div>', unsafe_allow_html=True)
    name = st.text_input('Name', key='name', placeholder='Enter your name', label_visibility='hidden')

    st.markdown('<div class="form-label">Age:</div>', unsafe_allow_html=True)
    age = st.text_input('Age', key='age', placeholder='Enter your age', label_visibility='hidden')

    st.markdown('<div class="form-label">Gender:</div>', unsafe_allow_html=True)
    gender = st.selectbox('Gender', ['Male', 'Female'], key='gender', label_visibility='hidden')

    st.markdown('<div class="form-label">Weight (kg):</div>', unsafe_allow_html=True)
    weight = st.text_input('Weight (kg)', key='weight', placeholder='Enter your weight in kg', label_visibility='hidden')

    st.markdown('<div class="form-label">Height (cm):</div>', unsafe_allow_html=True)
    height = st.text_input('Height (cm)', key='height', placeholder='Enter your height in cm', label_visibility='hidden')

    st.markdown('<div class="form-label">Veg or Non-Veg:</div>', unsafe_allow_html=True)
    veg_or_nonveg = st.selectbox('Veg or Non-Veg', ['Veg', 'Non-Veg'], key='veg_or_nonveg', label_visibility='hidden')

    st.markdown('<div class="form-label">Disease:</div>', unsafe_allow_html=True)
    disease = st.text_input('Disease', key='disease', placeholder='Enter any generic disease', label_visibility='hidden')

    st.markdown('<div class="form-label">Region:</div>', unsafe_allow_html=True)
    region = st.text_input('Region', key='region', placeholder='Enter your region', label_visibility='hidden')

    st.markdown('<div class="form-label">State:</div>', unsafe_allow_html=True)
    state = st.text_input('State', key='state', placeholder='Enter your state', label_visibility='hidden')

    st.markdown('<div class="form-label">Allergics:</div>', unsafe_allow_html=True)
    allergics = st.text_input('Allergics', key='allergics', placeholder='Enter any allergies', label_visibility='hidden')

    st.markdown('<div class="form-label">Food Type:</div>', unsafe_allow_html=True)
    foodtype = st.text_input('Food Type', key='foodtype', placeholder='Enter your preferred food type', label_visibility='hidden')

    submit_button = st.form_submit_button(label='Get Recommendations')
    st.markdown('</div>', unsafe_allow_html=True)

if submit_button:
    if all([name, age, gender, weight, height, veg_or_nonveg, disease, region, state, allergics, foodtype]):
        input_data = {
            'name': name,
            'age': age,
            'gender': gender,
            'weight': weight,
            'height': height,
            'veg_or_nonveg': veg_or_nonveg,
            'disease': disease,
            'region': region,
            'state': state,
            'allergics': allergics,
            'foodtype': foodtype
        }

        recommendations = chain_resto.invoke(input_data)

        st.markdown('<div class="subtitle">Recommendations:</div>', unsafe_allow_html=True)
        st.markdown('<div class="recommendations">', unsafe_allow_html=True)
        st.markdown(recommendations, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.error("Please fill in all the form fields.")