import streamlit as st
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType
load_dotenv() 

st.set_page_config(
    page_title="Diet Plan",
    page_icon="🗒️🍎🥗",
    layout="wide"
)
azure_search_endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
azure_search_index = os.getenv("AZURE_AI_SEARCH_INDEX")

# Title of the app
st.title("🥗 Personalized Diet Plan Generator")

# Subtitle
st.subheader("Tell us about yourself to get a customized diet plan!")

# Create the form for user inputs
with st.form(key="user_diet_form"):
    # User details
    age = st.number_input("Age", min_value=10, max_value=100, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    
    # Fitness goals
    fitness_goal = st.selectbox(
        "What is your primary fitness goal?",
        ["Weight Loss", "Weight Gain", "Muscle Building", "General Health"]
    )
    
    # Dietary restrictions or allergies
    dietary_restrictions = st.text_area(
        "Do you have any specific dietary restrictions or allergies? (e.g., lactose intolerance, gluten-free, nut allergy)"
    )
    
    # Health conditions
    health_condition = st.text_area(
        "Do you have any specific health conditions? (e.g., diabetes, high blood pressure, cholesterol issues)"
    )
    
    # Activity level
    activity_level = st.selectbox(
        "What is your current activity level?",
        ["Sedentary (little to no exercise)", "Lightly active (light exercise 1-3 days per week)",
         "Moderately active (moderate exercise 3-5 days per week)", "Very active (hard exercise 6-7 days per week)"]
    )
    
    # Dietary preferences
    diet_preferences = st.multiselect(
        "Do you have any diet preferences?",
        ["Vegetarian", "Vegan", "Pescatarian", "Keto", "Low Carb", "Mediterranean", "Paleo", "Dairy-Free", "Gluten-Free"]
    )
    
    # Weight
    current_weight = st.number_input("Current Weight (in kg)", min_value=20.0, max_value=300.0, step=0.5)
    target_weight = st.number_input("Target Weight (in kg)", min_value=20.0, max_value=300.0, step=0.5)

    # Submit button
    submit_button = st.form_submit_button(label="🤖Generate Diet Plan")
credential_chain = DefaultAzureCredential()

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

# Function to call OpenAI API to generate a personalized diet plan
def generate_diet_plan(prompt):
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OAI_MODEL_ENDPOINT"),
        api_key=os.getenv("AZURE_OAI_MODEL_KEY"),
        api_version=os.getenv("AZURE_OAI_MODEL_VERSION")
    )
    message_list=[ {"role": "system", "content": """You are a highly knowledgeable and friendly nutrition assistant who creates personalized diet plans.
            Your goal is to provide safe, effective, and evidence-based diet recommendations tailored to the user's 
            individual characteristics, preferences, and goals. Consider the user's age, gender, health conditions, 
            activity level, dietary restrictions, and preferences when creating the plan. Ensure the diet plan aligns with 
            their primary fitness goal (e.g., weight loss, muscle building, or general health). Include a balanced meal plan 
            with appropriate portion sizes, nutrient-rich foods, and hydration tips. Mention any necessary precautions related 
            to the user's health conditions and provide motivational tips to help them adhere to the plan."""},]
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
    return response.choices[0].message.content.strip()

# If the user submits the form, generate a personalized diet plan using OpenAI
if submit_button:
    # Construct the prompt for OpenAI with more context
    prompt = [
        {"role": "user", "content": f"""
            Generate a personalized diet plan for the following details:
            - Age: {age}
            - Gender: {gender}
            - Fitness Goal: {fitness_goal}
            - Dietary Restrictions: {dietary_restrictions}
            - Health Conditions: {health_condition}
            - Current Activity Level: {activity_level}
            - Diet Preferences: {', '.join(diet_preferences)}
            - Current Weight: {current_weight} kg
            - Target Weight: {target_weight} kg
            
            Provide a safe, effective, and evidence-based diet plan that aligns with the user's goals and conditions. Give a 7 day meal Plan.
        """}
    ]
    
    # Call the OpenAI API to generate the diet plan
    diet_plan = generate_diet_plan(prompt)
    
    # Display the generated diet plan

    diet_plan = f"## Your Personalized Diet Plan \n {diet_plan}"
    st.chat_message("assistant").markdown(diet_plan)



