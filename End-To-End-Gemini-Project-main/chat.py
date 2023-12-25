#GEMINI_CHATBOT

 ## loading all the environment variables
from dotenv import load_dotenv

load_dotenv() 


import streamlit as st
import os
import google.generativeai as genai


genai.configure(api_key=os.getenv ("GOOGLE_API_KEY"))
## function to load Gemini Pro model and get repsonses
model=genai.GenerativeModel("gemini-pro")
def get_gemini_response (question):
    response=model.generate_content (question) 
    return response.text

##initialize our streamlit app
st.set_page_config(page_title="Q&A Demo")


st.header("Gemini LLM Application")


# Initialize session state for chat history if it doesn't exist


if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input=st.text_input("Input: ",key="input")
submit=st.button("Ask the question")

if submit and input:
    response=get_gemini_response(input)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))
st.subheader("The Chat History is")
    
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")



