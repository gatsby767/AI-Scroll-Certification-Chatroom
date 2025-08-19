from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

class Agent(BaseModel):
    name: str
    model: str
    lineage: str

agents_db = []

@router.get("/agents", response_model=List[Agent])
def list_agents():
    return agents_db

@router.post("/agents", response_model=Agent)
def register_agent(agent: Agent):
    agents_db.append(agent)
    return agent

