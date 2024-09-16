import streamlit as st
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType
import nest_asyncio
from langchain_community.graphs import GremlinGraph
from gremlin_python.driver import client, serializer

load_dotenv()

azure_cosmodb_gremlin_endpoint = os.getenv("AZURE_COSMODB_GREMLIN_ENDPOINT")
azure_cosmodb_gremlin_username = os.getenv("AZURE_COSMODB_GREMLIN_USERNAME")
azure_cosmodb_gremlin_key = os.getenv("AZURE_COSMODB_GREMLIN_KEY")

os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("AZURE_OAI_MODEL_KEY")
os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("AZURE_OAI_MODEL_ENDPOINT")
os.environ["OPENAI_API_VERSION"] = os.getenv("AZURE_OAI_MODEL_VERSION")

st.set_page_config(
    page_title="Food Calorie Calculator",
    page_icon="🧮🍲🍱",
    layout="wide"
)

foodcategory_list = ['Vegetables', 'FastFood', 'Fish&Seafood', 'Meat', 'Fruits']

st.title('🥘 Food Calorie Calculator')
gremlin_client = client.Client(
    azure_cosmodb_gremlin_endpoint,
    'g',
    username=azure_cosmodb_gremlin_username,
    password=azure_cosmodb_gremlin_key,
    message_serializer=serializer.GraphSONSerializersV2d0())

with st.form(key='food_form'):
    # Dropdown to select the food category
    food_category = st.selectbox('Select Food Category:', foodcategory_list)
    
    # Input for food item
    food_item = st.text_input('Enter Food Item:')
    
    # Input for quantity
    quantity = st.number_input('Enter Quantity (in grams or ml):', min_value=0.0, step=0.1)

    # Form submission button
    submit_button = st.form_submit_button(label='🤖Ask MyFitnessBuddy')

def get_data_from_graphrag(food_item):
    try:
        # Gremlin query to find the calorie information
        query = f"g.V().hasLabel('fooditem').has('title', '{food_item}').outE('Calorieper100gm').inV().values('title')"

        # Submit the query to the Gremlin client
        callback = gremlin_client.submitAsync(query)

        if callback.result() is not None:
            # Extract the results
            result_set = callback.result().all().result()            
            return f"Calorie for {food_item} per 100 gram is {result_set[0]}"
        else:
            print(f"No calorie information found for {food_item}.")

    except Exception as e:
        print(f"An error occurred: {e}")

def generate_food_calculator(question,food_item):
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OAI_MODEL_ENDPOINT"),
        api_key=os.getenv("AZURE_OAI_MODEL_KEY"),
        api_version=os.getenv("AZURE_OAI_MODEL_VERSION")
    )
    message_list =[ {"role": "system", "content": """You are a highly knowledgeable and friendly food calorie counter assistant. Your goal is to provide accurate and personalized calorie information based on the user's queries. You have access to a database that provides the calorie content of various food items per 100 grams. 
                     When a user asks for the calorie content of a specific food item, use the provided calorie value per 100 grams to calculate and deliver the precise calorie content for the specified quantity. Use only the Database, don't answer on your own.
                     Now answer the question"""}]
    
    result=get_data_from_graphrag(food_item)
    message_list.append({"role": "assistant", "content": f"From the Database {result}"})
    message_list.append({"role": "user", "content": str(question)})
    print(message_list)
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OAI_MODEL"),
        temperature=0.3,
        max_tokens=1000,
        messages=message_list
    )
    return response.choices[0].message.content

if submit_button:
    prompt = f"How much calorie in {food_item} per {quantity} grams"
    calorie = generate_food_calculator(prompt,food_item)
    st.chat_message("assistant").write(calorie)
    gremlin_client.close()