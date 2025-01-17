from crewai import Crew,Process
from agents import blog_writer,blog_researcher
from tasks import research_task, Writing_task

crew = Crew(
    agents=[blog_researcher,blog_writer],
    tasks=[research_task,Writing_task],
    process= Process.sequential,
    #memory=True,
    cache=True,
    max_rpm=100,
    share_crew=True
)

## Start task execution process with enhancement of feedback
result = crew.kickoff(inputs={'topic':"AI VS ML VS DL VS Data Science "})
print(result)