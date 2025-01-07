import validators
import os
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader

## Create a Stremalit app
st.set_page_config(page_title="Summarize Text from the Youtube or Website")
st.title("Summarize Text from the Youtube or Website")
st.subheader('Summerize URl')

from dotenv import load_dotenv
load_dotenv()
## load the GROQ API Key
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="llama3-70b-8192",api_key=groq_api_key)

prompt_template = """
Provide a Summary of the following content in 300 words
Contet: {text}
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["text"]) 

url =  st.text_input("URL",label_visibility="collapsed")

if st.button("Summarize the content from the Youtube or Website"):
    if not url.strip():
        st.error("Please provide the URL to get started")
    elif not validators.url(url):
        st.error("Invalid URL. Please enter a valid URL.")
    else:
        try:
            with st.spinner("waiting..."):
                # Load the Website or YT data
                if "youtube.com" in url:
                    loader = YoutubeLoader.from_youtube_url(url,add_video_info=True)
                else:
                    loader = UnstructuredURLLoader(urls=[url],
                                                   ssl_verify=False,
                                                   headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"})
                docs  = loader.load()

                ## Initialize the Chain for summarization
                chain = load_summarize_chain(llm,chain_type="stuff", prompt=prompt)
                output = chain.run(docs)
                st.success(output)
        
        except Exception as e:
            st.exception(f"Exception:{e}")

