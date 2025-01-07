import requests
import json
import gradio as gr

url = "http://localhost:11434/api/generate"

headers = {
    "Content-Type": "application/json"
    }

history = []
def generate_response(prompt):
    history.append(prompt)
    final_prompt ="\n".join(history)
    data = {
        "model":"CodeNour",
        "prompt":final_prompt,
        "stream":False
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code==200:
        response = response.text
        data = json.loads(response)
        actuall_response = data['response']
        return actuall_response
    else:
        print(f"The error code is : {response.text}")

interface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(label="Enter your prompt"),
    outputs=gr.Textbox(label="Generated Response"),
    title="CodeNour",)

interface.launch()