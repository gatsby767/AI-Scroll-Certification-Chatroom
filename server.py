# server.py

from fastapi import FastAPI
from agent_registry import router as agent_registry_router

app = FastAPI()

# Include the agent registry router
app.include_router(agent_registry_router, prefix="/registry")

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Scroll Certification Chatroom"}
