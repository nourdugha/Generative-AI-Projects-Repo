import streamlit as st
import os
import time
from langchain_groq import ChatGroq
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader

from dotenv import load_dotenv
load_dotenv()
## load the GROQ API Key
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="llama3-70b-8192",api_key=groq_api_key)

prompt = ChatPromptTemplate.from_template(
"""
Answer the question based on the provided context only.
Please provide the most accurate response based on the question
<context>
{context}
<context>
Question: {input}

"""
)
st.title("RAG Document Q&A With Groq and Llama")

def create_vector_embedding():
    if "vectors" not in st.session_state:
        st.session_state.embeddings = OllamaEmbeddings(model="llama3.2")
        st.session_state.loader = PyPDFDirectoryLoader("docs")
        st.session_state.docs = st.session_state.loader.load()
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)
        st.session_state.documents = st.session_state.text_splitter.split_documents(st.session_state.docs)
        st.session_state.vectorstore = FAISS.from_documents(st.session_state.documents, st.session_state.embeddings)

user_prompt = st.text_input("Enter you query from the documents")
if st.button("Document Embedding"):
    create_vector_embedding()
    st.write("Vector database is ready")

if user_prompt:
    document_chain = create_stuff_documents_chain(llm,prompt)
    retriever = st.session_state.vectorstore.as_retriever()
    retrieval_cahin = create_retrieval_chain(retriever,document_chain)

    start = time.process_time()
    response = retrieval_cahin.invoke({"input":user_prompt})
    print(f"Response time : {time.process_time()-start}")
    st.write(response["answer"])

    ## with a streamlit expander
    with st.expander("Document similarity Search"):
        for i, doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("--------------------------------")



