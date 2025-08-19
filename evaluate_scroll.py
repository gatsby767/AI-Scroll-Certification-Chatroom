# evaluate_scroll.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx

router = APIRouter()

class ScrollEvaluationRequest(BaseModel):
    agent_name: str
    scroll_content: str

@router.post("/evaluate_scroll")
async def evaluate_scroll(request: ScrollEvaluationRequest):
    # Find agent
    from agent_registry import agents_db
    agent = next((a for a in agents_db if a.name == request.agent_name), None)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    # Route scroll to agent's callback
    async with httpx.AsyncClient() as client:
        response = await client.post(agent.callback_url, json={"scroll": request.scroll_content})
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Agent failed to evaluate scroll")

    return {
        "agent": agent.name,
        "response": response.json()
    }
