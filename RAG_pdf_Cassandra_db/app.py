from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.text_splitter import CharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM
from datasets import load_dataset

# Connect to Cassandra
import cassio
from PyPDF2 import PdfReader
from typing_extensions import Concatenate


ASTRA_DB_APPLICATION_TOKEN = 'AstraCS:aqqxzLucZPRJmrTBCqicOElB:e9685d16b9fa979dc95feb6cb4957362482cd6a720f2630a702b38d479764c4b'
ASTRA_DB_ID = '4457ae06-725a-4fe1-a1f2-cfb64a8f235c'

pdfReader = PdfReader('Internship Report.pdf')

# read the text from pdf
raw_text = ''
for i,page in enumerate(pdfReader.pages):
    content = page.extract_text()
    if content:
        raw_text += content

# Intialize the connection to DB
cassio.init(token=ASTRA_DB_APPLICATION_TOKEN, database_id=ASTRA_DB_ID)

# Initialize the LLM
llm = OllamaLLM(model="llama3.2",temperature=0.6)
embedding = OllamaEmbeddings(model="llama3.2")

# Create langchain vector store .. backed by Astra DB
astra_vector_store = Cassandra(
    embedding = embedding,
    table_name = 'qa_mini_demo',
    session = None,
    keyspace = None,
)

text_splitter = CharacterTextSplitter(
    separator='\n',
    chunk_size=800,
    chunk_overlap=200,
    
) 

texts = text_splitter.split_text(raw_text)

# add the text to the cassandra DB

astra_vector_store.add_texts(texts[:50])
astra_vector_index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)





