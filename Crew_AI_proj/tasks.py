from crewai import Task
from tools import yt_tool
from agents import blog_researcher, blog_writer

# Initialize the Research Task

research_task = Task(
    description= (
    "Identify the video {topic}."
    "Get the detailed information about the video from the channel."
    ),
    expected_output="A Comprehensive 3 paragraphs long report based on the {topic} of video content.",
    tools=[yt_tool],
    agents=blog_researcher
)

# Initialize the Writing Task

Writing_task = Task(
    description= (
    "get the info from the youtube channel on the topic {topic}."
    ),
    expected_output="Summarize the info from the youtube channel video on the topic {topic} and create the content for the blog.",
    tools=[yt_tool],
    agents=blog_writer,
    # to avoid that two agents work parallelly 
    async_execution=False,
    output_file="New-blog-post.md"
)

