from crewai import Agent,LLM
from tools import yt_tool
from langchain_ollama import OllamaLLM
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

## load the GROQ API Key
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="llama3-70b-8192",api_key=groq_api_key)

# make custom llm
"""llm= LLM(
    model="groq/llama3-70b-8192",
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)"""



"""llm = LLM(
    model="ollama/llama3.2:3b",
    base_url="http://localhost:11434"
)"""

## Create a Senior blog content researcher agent

blog_researcher = Agent(
    role='Blog Researcher from Youtube video',
    goal='Get the relevant video content for the topic{topic} from the Youtube channel',
    verbose=True,
    #memory = True,
    backstory=(
        "Expert in understanding videos in AI and Data science, Machine learning and providing suggestions"

    ),
    llm=llm,
    tools=[yt_tool],
    # allow the transferring after whatever work this agent does to someone else  
    allow_delegation=True
)

## Create the a senior blog writer agent with YT tool

blog_writer = Agent(
    role='Blog Writer',
    goal='Narrate compelling tech stories about the video {topic} from YouTube channel',
    verbose=True,
    #memory = True,
    backstory=(
        "With a flair for simplifying complex topics, you carft engaging narratives"
        "that captivate and educate, bringing new discoveries to light in an accsessible manner."

    ),
    llm=llm,
    tools=[yt_tool],
    # allow the transferring after whatever work this agent does to someone else  
    allow_delegation=False
)