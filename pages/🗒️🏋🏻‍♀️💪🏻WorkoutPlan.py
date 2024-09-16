import streamlit as st
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType

load_dotenv() 

st.set_page_config(
    page_title="Workout Plan",
    page_icon="🗒️🏋🏻‍♀️💪🏻",
    layout="wide"
)

azure_search_endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
azure_search_index = os.getenv("AZURE_AI_SEARCH_INDEX")
credential_chain = DefaultAzureCredential()

st.title("🏋️ Personalized Workout Routine Generator")

st.subheader("Tell us about yourself to get a customized workout plan!")

with st.form(key="user_info_form"):
    age = st.number_input("Age", min_value=10, max_value=100, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    
    fitness_goal = st.selectbox(
        "What is your primary fitness goal?",
        ["Weight Loss", "Weight Gain", "Muscle Building", "General Fitness"]
    )
    
    health_condition = st.text_area(
        "Do you have any specific health conditions or limitations? (e.g., back pain, diabetes, heart problems)"
    )
    
    activity_level = st.selectbox(
        "What is your current activity level?",
        ["Sedentary (little to no exercise)", "Lightly active (light exercise 1-3 days per week)",
         "Moderately active (moderate exercise 3-5 days per week)", "Very active (hard exercise 6-7 days per week)"]
    )
    
    workout_preferences = st.multiselect(
        "Do you have any workout preferences?",
        ["Cardio", "Strength Training", "Yoga", "Pilates", "HIIT", "Cycling", "Swimming", "Running", "Walking"]
    )
    
    current_weight = st.number_input("Current Weight (in kg)", min_value=20.0, max_value=300.0, step=0.5)
    target_weight = st.number_input("Target Weight (in kg)", min_value=20.0, max_value=300.0, step=0.5)

    submit_button = st.form_submit_button(label="🤖Generate Workout Routine")
def extract_data_from_azure_search(prompt):
   
    search_client = SearchClient(
        endpoint=azure_search_endpoint,
        index_name=azure_search_index,
        credential=credential_chain
    )
    
    search_query = prompt
    results = search_client.search(
        search_text=search_query,
        query_type=QueryType.SIMPLE,
        top=5
    )
    result=[item for item in results]

    print("result",len(result))

    return result

def generate_workout_routine(prompt):
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OAI_MODEL_ENDPOINT"),
        api_key=os.getenv("AZURE_OAI_MODEL_KEY"),
        api_version=os.getenv("AZURE_OAI_MODEL_VERSION")
    )
    message_list =[ {"role": "system", "content": """
            You are a highly knowledgeable and friendly fitness assistant who creates personalized workout plans. 
            Your goal is to provide safe, effective, and evidence-based workout routines tailored to the user's 
            individual characteristics, preferences, and goals. Consider the user's age, gender, health conditions, 
            current activity level, and workout preferences when creating the plan. Ensure the workout plan aligns with 
            their primary fitness goal (e.g., weight loss, muscle building, or general fitness). Include a balance of 
            cardiovascular, strength, and flexibility exercises where appropriate. Provide specific exercises, duration, 
            and frequency recommendations for each day of the week, and mention any necessary precautions related to the 
            user's health conditions. Offer motivational tips to encourage the user to stay consistent with the workout plan.
        """}]
    
    result=extract_data_from_azure_search(prompt)
    reference_list = []
    for i, item in enumerate(result):
        reference_list.append([item['url'], item['content']])
        message_list.append({"role": "assistant", "content": f"Knowledge Base {i+1}: {item['content']}"})

    message_list.append({"role": "user", "content": str(prompt)})

    
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OAI_MODEL"),
        temperature=0.3,
        max_tokens=1000,
        messages=message_list
    )
    return response.choices[0].message.content

if submit_button:
    prompt =[ {"role": "user", "content": f"""
            Generate a personalized workout routine for the following details:
            - Age: {age}
            - Gender: {gender}
            - Fitness Goal: {fitness_goal}
            - Health Conditions: {health_condition}
            - Current Activity Level: {activity_level}
            - Workout Preferences: {', '.join(workout_preferences)}
            - Current Weight: {current_weight} kg
            - Target Weight: {target_weight} kg
            
            Provide a safe, effective, and evidence-based workout plan that aligns with the user's goals and conditions.
        """}
    ]
    
    
    workout_plan = generate_workout_routine(prompt)

    workout_plan = f"## Your Personalized Workout Routine \n {workout_plan}"
    st.chat_message("assistant").markdown(workout_plan)
