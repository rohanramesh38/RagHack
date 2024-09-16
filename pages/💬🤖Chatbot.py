import streamlit as st
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType
load_dotenv()

azure_search_endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
azure_search_index = os.getenv("AZURE_AI_SEARCH_INDEX")

 

st.set_page_config(
    page_title="ChatBot",
    page_icon= "💬🤖",
    layout="wide"
)
   
# Get Azure OpenAI endpoint from environment variables
azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
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