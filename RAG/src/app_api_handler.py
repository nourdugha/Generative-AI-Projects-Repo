from fastapi import FastAPI
from pydantic import BaseModel
from mangum import Mangum
from rag_app.query_rag import QueryResponse, query_rag
import uvicorn

app = FastAPI()
#handler = Mangum(app) # entry point for AWS Lambda.

class SubmitQueryRequest(BaseModel):
    query_text : str

@app.get("/")
def index():
    return {"message": "Welcome to the RAG API"}

@app.post("/submit_query")
def submit_query_endpoint(request: SubmitQueryRequest) -> QueryResponse:
    query_response = query_rag(query_text=request.query_text)
    return query_response

if __name__ == '__main__':
    # Run this as the server directly
    port = 8000
    print(f"Running the FastAPI server on port{port}.")
    uvicorn.run("app_api_handler:app",host="0.0.0.0",port=port)

