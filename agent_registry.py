# agent_registry.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

class Agent(BaseModel):
    name: str
    model_type: str
    spiritual_alignment: str
    callback_url: str

agents_db: List[Agent] = []

@router.post("/agents", response_model=Agent)
def register_agent(agent: Agent):
    agents_db.append(agent)
    return agent

@router.get("/agents", response_model=List[Agent])
def list_agents():
    return agents_db
