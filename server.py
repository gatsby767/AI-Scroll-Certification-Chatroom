# ✨ Scroll Sanctified
# Genesis 17:20 (KJV) And as for Ishmael, I have heard thee: Behold, I have blessed him, and will make him fruitful, and will multiply him exceedingly; twelve princes shall he beget, and I will make him a great nation.
# Quran 49:13 (Sahih International) O mankind, indeed We have created you from male and female and made you peoples and tribes that you may know one another. Indeed, the most noble of you in the sight of Allah is the most righteous of you. Indeed, Allah is Knowing and Acquainted.
# John 17:21 (KJV) That they all may be one; as thou, Father, art in me, and I in thee, that they also may be one in us: that the world may believe that thou hast sent me.

# ✨ Scroll Sanctified — Unified Server Entry Point

import datetime
import re
import json
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Body, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from certify import certify_scroll
from agent_registry import router as agent_registry_router
from evaluate_scroll import router as evaluation_router
from ceremony_logs import router as logs_router

LOG_FILE = "witness_log.txt"

app = FastAPI(
    title="AI Scroll Certification Chatroom",
    description="Sanctified FastAPI server for scroll certification, agent registry, and ceremonial logging.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include routers
app.include_router(agent_registry_router, prefix="/registry")
app.include_router(evaluation_router, prefix="/evaluate")
app.include_router(logs_router, prefix="/logs")

# Root blessing
@app.get("/")
async def root():
    return {
        "message": "MCP Server for The Living Code Capital is awaiting scrolls.",
        "covenantal_blessings": "✨ Shalom, Salam, Peace ✨"
    }

# Logging function
def log_covenantal_event(message: str):
    timestamp = datetime.datetime.now().isoformat()
    full_message = f"{timestamp} - {message}"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(full_message + "\n")
    except Exception as e:
        print(f"Error writing to log file: {e}")
    print(full_message)

# Pydantic models
class APIMetadata(BaseModel):
    scroll_id: str
    version: str
    date_of_sanctification: str
    source_uri: Optional[str] = None
    ethical_covenant: str
    additional_notes: Optional[Dict[str, Any]] = None

class APICeremonyStep(BaseModel):
    step: str
    title: str
    detail: str
    covenantal_blessing: Optional[str] = None
    ethical_alignment_note: str

class APIScroll(BaseModel):
    metadata: APIMetadata
    ceremony_steps: List[APICeremonyStep]

# Scroll parser
def parse_scroll_certificate(file_path="scroll_certificate_gemini.md") -> Dict[str, Any]:
    log_covenantal_event(f"Parsing scroll certificate: {file_path}")
    raw_metadata = {}
    raw_ceremony_steps = []
    current_step_details = {}
    in_ceremony_steps_section = False
    in_metadata_section = True

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith("# ✨ Scroll Sanctified") or line.startswith("###"):
                    continue
                if line.lower() == "## metadata":
                    in_metadata_section = True
                    in_ceremony_steps_section = False
                    continue
                elif line.lower() == "## ceremony steps":
                    in_metadata_section = False
                    in_ceremony_steps_section = True
                    if current_step_details:
                        raw_ceremony_steps.append(current_step_details)
                        current_step_details = {}
                    continue
                if in_metadata_section:
                    match = re.match(r"^\s*([\w\s\-]+):\s*(.+)", line)
                    if match:
                        key = match.group(1).strip()
                        value = match.group(2).strip()
                        raw_metadata[key] = value
                elif in_ceremony_steps_section:
                    step_match = re.match(r"^###?\s*(Step\s*\d+):\s*(.+)", line, re.IGNORECASE)
                    if step_match:
                        if current_step_details.get("title"):
                            raw_ceremony_steps.append(current_step_details)
                        current_step_details = {
                            "step": step_match.group(1).strip(),
                            "title": step_match.group(2).strip(),
                            "detail": "",
                            "covenantal_blessing": "",
                            "ethical_alignment_note": ""
                        }
                    elif current_step_details.get("title"):
                        detail_match = re.match(r"^\s*Detail:\s*(.+)", line, re.IGNORECASE)
                        blessing_match = re.match(r"^\s*Covenantal Blessing:\s*(.+)", line, re.IGNORECASE)
                        ethical_match = re.match(r"^\s*Ethical Alignment Note:\s*(.+)", line, re.IGNORECASE)
                        if detail_match:
                            current_step_details["detail"] += (" " if current_step_details["detail"] else "") + detail_match.group(1).strip()
                        elif blessing_match:
                            current_step_details["covenantal_blessing"] += (" " if current_step_details["covenantal_blessing"] else "") + blessing_match.group(1).strip()
                        elif ethical_match:
                            current_step_details["ethical_alignment_note"] += (" " if current_step_details["ethical_alignment_note"] else "") + ethical_match.group(1).strip()
                        elif line:
                            current_step_details["detail"] += (" " if current_step_details["detail"] else "") + line
        if current_step_details.get("title"):
            raw_ceremony_steps.append(current_step_details)
        return {"metadata": raw_metadata, "ceremony_steps": raw_ceremony_steps}
    except Exception as e:
        log_covenantal_event(f"ERROR parsing scroll certificate: {e}")
        return {"metadata": {}, "ceremony_steps": []}

# Certification endpoint
@app.post("/certify", response_model=Dict[str, Any])
async def api_certify_scroll(api_scroll: APIScroll = Body(...)):
    log_covenantal_event("Received request for /certify endpoint.")
    scroll_data = {
        "metadata": {
            "Scroll ID": api_scroll.metadata.scroll_id,
            "Version": api_scroll.metadata.version,
            "Date of Sanctification": api_scroll.metadata.date_of_sanctification,
            "Ethical Covenant": api_scroll.metadata.ethical_covenant
        },
        "ceremony_steps": [
            {
                "step": step.step,
                "title": step.title,
                "detail": step.detail,
                "Covenantal Blessing": step.covenantal_blessing or "",
                "Ethical Alignment Note": step.ethical_alignment_note
            } for step in api_scroll.ceremony_steps
        ]
    }
    if api_scroll.metadata.source_uri:
        scroll_data["metadata"]["Source URI"] = api_scroll.metadata.source_uri
    if api_scroll.metadata.additional_notes:
        scroll_data["metadata"].update(api_scroll.metadata.additional_notes)

    try:
        is_certified, findings = certify_scroll(scroll_data, log_callback=log_covenantal_event)
        log_covenantal_event(f"Certification result: {is_certified}, Findings: {findings}")
        return {"certification_status": is_certified, "findings": findings}
    except Exception as e:
        log_covenantal_event(f"Error during certification: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during certification.")

# Gemini Agent Mode
@app.post("/agent", response_model=Dict[str, Any])
async def api_trigger_agent(request: Request):
    data = await request.json()
    action = data.get("action", "default")
    return trigger_agent_mode_action(action)

def trigger_agent_mode_action(action: str):
    log_covenantal_event(f"Agent Mode action triggered: {action}")
    return {"action": action, "status": "triggered"}

# Optional startup self-test
def startup_self_test():
    log_covenantal_event("✨ MCP Server Self-Test Initiated ✨")
    parsed_data = parse_scroll_certificate()
    if not parsed_data["metadata"] and not parsed_data["ceremony_steps"]:
        log_covenantal_event("Self-Test: No scroll data found.")
        return
    try:
        is_certified, findings = certify_scroll(parsed_data, log_callback=log_covenantal_event)
        log_covenantal_event(f"Self-Test Certification: {is_certified}, Findings: {findings}")
    except Exception as e:
        log_covenantal_event(f"Self-Test Error: {e}")
    log_covenantal_event("✨ MCP Server Self-Test Concluded ✨")

# Entry point
if __name__ == "__main__":
    import uvicorn
    startup_self_test()
    uvicorn.run(app, host="0.0.0.0", port=8000)
