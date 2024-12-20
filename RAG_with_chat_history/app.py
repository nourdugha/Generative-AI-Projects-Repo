import streamlit as st
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb

chromadb.api.client.SharedSystemClient.clear_system_cache()

import os

from dotenv import load_dotenv
load_dotenv()

os.environ["HF_TOKEN"]= os.getenv("HF_TOKEN")
embeddings = OllamaEmbeddings(model="llama3.2")
#embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


## set up Streamlit app
st.title("Conversational RAG with PDF uploads with History")
st.write("Upload Pdf's and chat with it")

## input the Groq API key
api_key = st.text_input("Enter the api key: ", type="password")
if api_key:
    llm = ChatGroq(api_key=api_key,model="Gemma2-9b-It")
    session_id = st.text_input("Session ID",value="Default_session")

    ## statefully manage chat history
    if "store" not in st.session_state:
        st.session_state.store = {}
    
    uploaded_files = st.file_uploader("Choose a Pdf file",type="pdf",accept_multiple_files=True)
    if uploaded_files:
        documents = []
        for uploaded_file in uploaded_files:
            temp_pdf = f"./temp.pdf"
            with open(temp_pdf, "wb") as file:
                file.write(uploaded_file.getvalue())
                file_name = uploaded_file.name
            
            loader = PyPDFLoader(temp_pdf)
            docs = loader.load()
            documents.extend(docs)
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000,chunk_overlap=300)
        splits = text_splitter.split_documents(documents)
        vectorstore = Chroma.from_documents(documents=splits,embedding=embeddings)
        retriever = vectorstore.as_retriever()
    
        contextualize_q_system_prompt = (
            "Given a chat history and the latest user question"
            "which might reference context in the chat history"
            "formulate a standalone question which can be understood"
            "without the chat history. Do not answer the question"
            "just reformulate it if needed and otherwise return it as is."
        )

        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system",contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human","{input}")
            ]
        )

        history_aware_retriever = create_history_aware_retriever(llm,retriever,contextualize_q_prompt)

        ## Answer question
        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved contexts to answer the question."
            "If you don't know the answer, say that you don't know"
            "Use three sentences maximum and keep the answer concise"
            "\n\n"
            "{context}"
        )

        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system",system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human","{input}")
            ]
        )

        question_answer_chain = create_stuff_documents_chain(llm,qa_prompt)
        rag_chain = create_retrieval_chain(history_aware_retriever,question_answer_chain)

        def get_session_history(session:str) -> BaseChatMessageHistory:
            if session_id not in st.session_state.store:
                # ChatMessageHistory: all the conversation that happining with respect to session_id will get stored
                st.session_state.store[session_id] = ChatMessageHistory()
            return st.session_state.store[session_id]
        
        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )

        user_input = st.text_input("Your question:")
        if user_input:
            session_history = get_session_history(session_id)
            response = conversational_rag_chain.invoke(
                {"input": user_input},
                config={"configurable":{"session_id": session_id}}

            )
            st.write(st.session_state.store)
            st.success(f"Answer: {response['answer']}")
            st.write("Chat history:",session_history.messages)

else:
    st.warning("Please enter the groq api key")    





