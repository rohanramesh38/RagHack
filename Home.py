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

tab1, tab2, tab3 = st.tabs(["Origins: Unveiling the Background and Purpose", "Architecture and Implementation","Conclusion and Future Work"])

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