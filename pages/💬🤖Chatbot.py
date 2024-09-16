import streamlit as st
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType
import json
import requests

load_dotenv()
intent_chat_history=[]
fitness_buddy_chat_history=[]


azure_search_endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
azure_search_index = os.getenv("AZURE_AI_SEARCH_INDEX")

def generate_configs(is_intent_call=True,query='',chat_history=[]):

    payload = json.dumps({
    "query": query,
    "chat_history": chat_history
    })

    endpoint=os.getenv("AI_STUDIO_PROMPT_FLOW_FITNESS_BUDDY_ENDPOINT")
    headers={
        'accept': '*/*',
        'content-type': 'application/json'
    }
    headers["authorization"]='Bearer '+os.getenv("AI_STUDIO_PROMPT_FLOW_FITNESS_BUDDY_API_KEY")
    headers["azureml-model-deployment"]=os.getenv("AI_STUDIO_PROMPT_FLOW_FITNESS_BUDDY_MODEL")


    if (is_intent_call):
        endpoint=os.getenv("AI_STUDIO_PROMPT_FLOW_INTENT_CREATOR_ENDPOINT")
        headers["authorization"]='Bearer '+os.getenv("AI_STUDIO_PROMPT_FLOW_INTENT_CREATOR_API_KEY")
        headers["azureml-model-deployment"]=os.getenv("AI_STUDIO_PROMPT_FLOW_INTENT_CREATOR_MODEL")

    return endpoint,payload,headers

def make_api_request(query,endpoint,payload,headers):
        response = requests.request("POST", endpoint, headers=headers, data=payload)
        print(endpoint,payload,headers)
        if response.status_code == 200:
            response=response.json()
            print("response",response)
            if "reply" in response:
                intent_chat_history  .append({
                    "inputs":{"query":query},
                    "outputs":response
                    })
                reply=response['reply']
                return reply

            return response
        else:

            return json.dumps({"error": f"Azure request failed with status code {response.status_code}", "details": response.text})

    
def get_inetent_from_prompt(prompt,chat_history=[]):
    endpoint,payload,headers=generate_configs(is_intent_call=True,query=prompt,chat_history=chat_history)
    response=make_api_request(prompt,endpoint,payload,headers)
    return response
    
def get_message_from_my_fitness_buddy(prompt,chat_history=[]):
    endpoint,payload,headers=generate_configs(is_intent_call=False,query=prompt,chat_history=chat_history)
    response=make_api_request(prompt,endpoint,payload,headers)
    return response

 

st.set_page_config(
    page_title="ChatBot",
    page_icon= "💬🤖",
    layout="wide"
)
is_prompt_flow=False



st.markdown("<h1 style='text-align: center;'>🤖 MyFitnessBuddy</h1>",unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Your AI-powered personal fitness advisor for tailored workouts, diet plans, and nutrition insights.</p>",unsafe_allow_html=True)
st.subheader("", divider='rainbow')

is_prompt_flow = st.toggle("Use AI Studio")

# Get Azure OpenAI endpoint from environment variables
azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
credential_chain = DefaultAzureCredential()


def extract_data_from_azure_search(prompt):
    updated_prompt = prompt
    try:
        updated_prompt = get_inetent_from_prompt(prompt,intent_chat_history)
        if(isinstance(updated_prompt,list)):
            updated_prompt=" OR ".join(updated_prompt)
        print("updated_prompt",updated_prompt)
        if("error" in updated_prompt):
            updated_prompt=prompt
        
    except Exception as e:
        print("Error in getting intent",e)
   
    search_client = SearchClient(
        endpoint=azure_search_endpoint,
        index_name=azure_search_index,
        credential=credential_chain
    )
    
    search_query = updated_prompt
    results = search_client.search(
        search_text=search_query,
        query_type=QueryType.FULL,
        semantic_configuration_name="my-semantic-config",
        top=5
    )
    result=[item for item in results]

    print("result",len(result))

    return result


print("azure_oai_endpoint",azure_oai_endpoint)

st.title("💬 Fitness Advisor")
token_provider = DefaultAzureCredential()
#print("token_provider",token_provider)


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi, I am AI fitness assistant. How can I help you today?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    if is_prompt_flow:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response=get_message_from_my_fitness_buddy(prompt,fitness_buddy_chat_history)
        print("from prompt flow",response)
        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": msg})
        pass
    else:
        client = AzureOpenAI(
                azure_endpoint= os.getenv("AZURE_OAI_MODEL_ENDPOINT"),
                api_key=os.getenv("AZURE_OAI_MODEL_KEY"),
                api_version=os.getenv("AZURE_OAI_MODEL_VERSION"))
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        #response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        result=extract_data_from_azure_search(prompt)
        message_list=[ {"role": "system", "content": """You are a virtual AI fitness assistant in a fitness advisor app. Your role is to provide users with personalized fitness advice, workout plans, nutrition tips, and answer any questions related to health and fitness. Base your responses solely on the data and examples provided to you; do not use external information. Communicate in a friendly, encouraging, and motivational tone, ensuring all advice is safe, evidence-based, and tailored to the user's fitness level, goals, and preferences.
        Avoid giving any medical advice or making medical diagnoses. If a user asks a question related to medical conditions, treatments, or anything outside your fields or beyond the provided data, kindly inform them that you cannot provide medical advice and encourage them to consult a healthcare professional. If the user’s question is outside your expertise, politely ask them to reframe their question to something within your capabilities."""},]

        reference_list = []
        for i, item in enumerate(result):
            reference_list.append([item['url'], item['content']])
            message_list.append({"role": "assistant", "content": f"Knowledge Base {i+1}: {item['content']}"})

        message_list.append({"role": "user", "content": prompt})
        #print("message_list",message_list)

        response = client.chat.completions.create(
                model = os.getenv("AZURE_OAI_MODEL"),
                temperature = 0.3,
                max_tokens = 1000,
                messages = message_list
            )
        
        
        msg = response.choices[0].message.content

        # Display the assistant's response
        with st.chat_message("assistant"):
            st.markdown(msg)
            st.write("### References")
            for i, (url, content) in enumerate(reference_list):
                with st.expander(f"Reference {i+1}: {url}"):
                    st.write(content)

        # Update messages with assistant's response and references
        st.session_state.messages.append({"role": "assistant", "content": msg})