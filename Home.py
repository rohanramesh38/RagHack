import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px
import altair as alt

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)

st.markdown("<h1 style='text-align: center;'>🤖 MyFitnessBuddy</h1>",unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Your AI-powered personal fitness advisor for tailored workouts, diet plans, and nutrition insights.</p>",unsafe_allow_html=True)
st.subheader("", divider='rainbow')

tab1, tab2, tab3, tab4 = st.tabs(["Origins: Unveiling the Background and Purpose", "Architecture and Implementation","Technology Used","Conclusion and Future Work"])

with tab1:
    coli, colk = st.columns(2)
    with coli:
        st.markdown(" ")
        st.image("https://static01.nyt.com/images/2024/02/27/well/23Well-fitness-data/23Well-fitness-data-superJumbo.jpg")
    with colk:
        st.markdown("""
        ### Problem Definition:
    1. **Personalized Fitness Guidance**: MyFitnessBuddy is a GenAI Fitness Advisor App that provides customized workout routines, diet plans, and a food calorie calculator, addressing the limitations of generic fitness apps.
    2. **Advanced Retrieval-Augmented Generation**: It leverages a hybrid approach combining Retrieval-Augmented Generation (RAG) and Graph Retrieval-Augmented Generation (GRAG) to deliver accurate and context-aware responses to user queries.
    3. **Showcasing Innovation at RAGHack**: Developed for the RAGHack hackathon, MyFitnessBuddy demonstrates the power of RAG technologies in creating engaging and effective AI-driven fitness solutions using Azure AI and popular frameworks. """)
    st.markdown("""
    ## Target Audience:

    - **Fitness Enthusiasts:** Individuals who are passionate about fitness and are looking for personalized workout routines and diet plans to optimize their fitness journey.
    - **Health-Conscious Individuals:** People who prioritize a healthy lifestyle and want easy access to accurate nutritional information, calorie tracking, and tailored dietary advice.
    - **Beginners in Fitness:** Newcomers who need guidance on starting their fitness journey, including basic workout routines, dietary recommendations, and answers to common fitness-related questions.
    - **Busy Professionals:** Users with limited time for fitness planning who seek convenient, on-demand access to customized fitness guidance and quick answers to health-related queries.
    - **Individuals with Specific Health Goals:** Those with unique fitness goals or health conditions who require personalized plans and advice that consider their specific needs and preferences.
    """)

with tab2:
    st.markdown("""### Architecture Overview:""")
    st.image("/Users/jeeva/Documents/RagHack/images/Architecture.png",caption="Fig.1 Architecture")
    st.markdown("""
    MyFitnessBuddy uses a hybrid architecture combining Retrieval-Augmented Generation (RAG) and Graph Retrieval-Augmented Generation (GRAG). Data is extracted using a Python script and ingested into Azure Blob Storage for structured data and Azure Cosmos DB (Gremlin API) for unstructured data. Azure AI Search indexes the structured data, while the graph database manages complex relationships in the unstructured data.
    The application utilizes Azure AI Studio and Prompt Flow to define chat logic and connect data sources. User queries are processed by the app server, retrieving relevant information from Azure AI Search and Cosmos DB, which is then sent to Azure OpenAI Services (ChatGPT) to generate personalized responses.
    This hybrid approach ensures accurate, context-aware, and personalized fitness guidance for users.

    ### Implementation Overview:

    #### Data Extraction and Ingestion:""",unsafe_allow_html=True)
    st.image("/Users/jeeva/Documents/RagHack/images/ArchitectureExtraction.png",caption="Fig 2. Data Extraction Architecture")
    st.markdown("""
    <ul>
    <li>The process begins with a Python script that extracts structured and unstructured data from various sources. This data is then ingested into two different storage systems:
    <ul><li>Azure Blob Storage: Used for structured data, which is chunked and indexed.</li>
    <li>Azure Cosmos DB (Gremlin API): Used for unstructured data, ingested as GraphDoc to enable graph-based retrieval.</li></ul>
    </li>
    </ul>

    #### Hybrid RAG Approach:""",unsafe_allow_html=True)
    st.image("/Users/jeeva/Documents/RagHack/images/ArchitectureRag.png",caption="Fig 4. Hybrid RAG Architecture")

    st.markdown("""
    <ul> <li><b>RAG (Retrieval-Augmented Generation):</b>
    <ul> <li>The structured data ingested into Azure Blob Storage is connected to Azure AI Search for indexing and retrieval.</li>
    <li>Azure AI Studio facilitates the chunking and indexing of data, defining chat logic, and generating endpoints using Azure Prompt Flow.</li>
    <li>When a user query is received, Azure AI Search retrieves relevant information from the indexed data.</li>
    </ul>
    </li>
    </ul>
    <ul><li><b>Graph RAG (Graph Retrieval-Augmented Generation):</b>
    <ul><li>Azure Cosmos DB stores the unstructured data in a graph format using the Gremlin API. This approach allows the application to understand complex relationships between entities such as food items, exercises, and user health metrics.</li>
    <li>The Graph RAG retrieves contextually relevant knowledge from Azure Cosmos DB, which is then combined with structured data for enhanced response generation.</li></ul>
    </li></ul>""",unsafe_allow_html=True)

    st.image("/Users/jeeva/Documents/RagHack/images/graph1.png")
    st.image("/Users/jeeva/Documents/RagHack/images/graph2.png",caption="Fig 4. Example of how Unstructured Data is stored as Graph in Azure CosmoDB(Gremlin API)")

    st.markdown("""
    ### Application Flow:
    - The user interacts with the MyFitnessBuddy app through a Python Streamlit-based chatbot interface.
    - The application server processes the user's query and directs it to the appropriate retrieval system (Azure AI Search for structured data or Azure Cosmos DB for unstructured data) based on the query type.
    - Relevant information is retrieved from the selected data source and sent to Azure OpenAI Services (ChatGPT) along with a crafted prompt to generate a personalized response.
    - The final response, enriched with contextually relevant information, is returned to the user via the Streamlit app, providing tailored fitness advice and recommendations.
    """,unsafe_allow_html=True)

    st.image("/Users/jeeva/Documents/RagHack/images/app.png")
    st.image("/Users/jeeva/Documents/RagHack/images/app1.png")
    st.image("/Users/jeeva/Documents/RagHack/images/app2.png",caption="Fig 5. Application")

with tab3:
    st.markdown("""
## Technologies Used:
- **Data Storage and Retrieval:** Azure Blob Storage, Azure Cosmos DB (Gremlin API), Azure AI Search.
- **AI and Language Models:** Azure OpenAI Services (ChatGPT).
- **Data Processing and Logic Flow:** Azure AI Studio, Azure Prompt Flow.
- **Backend and Application Server:** Python for data extraction and preprocessing, with multiple integration points for data ingestion and retrieval.
""")
    st.markdown("""
- [x] JavaScript
- [ ] Java
- [ ] .NET
- [x] Python
- [x] AI Studio
- [x] AI Search
- [ ] PostgreSQL
- [x] Cosmos DB
- [ ] Azure SQL

""")

with tab4:
    st.markdown("""
    ## Conclusion and Future Works:

    ### Conclusion

    MyFitnessBuddy demonstrates the potential of combining advanced AI techniques like Retrieval-Augmented Generation (RAG) and Graph Retrieval-Augmented Generation (GRAG) to create a highly personalized and context-aware fitness advisor. By leveraging Azure AI's capabilities and integrating multiple data sources, the app provides customized workout routines, dietary plans, and accurate responses to user queries. This approach enhances user engagement and satisfaction by delivering tailored and relevant fitness guidance.

    ### Future Work

    - **Enhanced Personalization:** Further refine the models to provide more granular customization based on user feedback, behavior, and preferences.
    - **Multilingual Support:** Implement multilingual capabilities to reach a broader audience globally.
    - **Advanced Analytics:** Develop advanced analytics features to provide users with deeper insights into their fitness progress, habits, and trends.
    - **Expanded Data Sources:** Incorporate additional data sources such as medical databases and user-generated content to enhance the app’s knowledge base and improve recommendation accuracy.
        """)