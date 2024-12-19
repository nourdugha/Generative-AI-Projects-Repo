import streamlit as st
import openai
import os 
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

## Langsmith Tracking
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACKING_V2'] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Q&A Chatbot with OpenAI and Ollama"

## Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system","you are helpful assitant. Please response to the user qeuries"),
    ("user","Question:{question}")
])

def generate_response_openai(question,api_key,llm,temperature,max_tokens):
    openai.api_key = api_key
    llm = ChatOpenAI(model=llm,temperature=temperature,max_tokens=max_tokens)
    output_parser = StrOutputParser()
    chain = prompt|llm|output_parser
    answer = chain.invoke({'question': question})
    return answer

def generate_response_llama(question,llm,temperature,max_tokens):
    llm = OllamaLLM(model="llama3.2",temperature=temperature,max_tokens=max_tokens)
    output_parser = StrOutputParser()
    chain = prompt|llm|output_parser
    answer = chain.invoke({'question': question})
    return answer

## Title of the app
st.title("Enhancerd Q&A Chatbot with OpenAI or Llama")

## Siderbar for settings
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your OpenAI key:",type="password")

## Dropdown for selecting llm models
llm = st.sidebar.selectbox("Select llm models",["gpt-4o","gpt-4-turbo","gpt-4","llama3.2"])

## Adjust the response parameters
temperature = st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens = st.sidebar.slider("Max tokens",min_value=50,max_value=300,value=150)

## Main interface for user input
st.write("Go ahead and enter your question")
user_input = st.text_input("you:")

if user_input:
    if llm in ["gpt-4o","gpt-4-turbo","gpt-4"]:
        response = generate_response_openai(user_input,api_key,llm,temperature,max_tokens)
    elif llm in ["llama3.2"]:
        response = generate_response_llama(user_input,llm,temperature,max_tokens)
    else:
        st.write("Invalid llm model selected. Please choose from gpt-4o, gpt-4-turbo, gpt-4, or llama3.2")
    st.write(response)
else:
    st.write("Please enter a question")