# ✨ Scroll Sanctified
# Genesis 17:20 (KJV) And as for Ishmael, I have heard thee: Behold, I have blessed him, and will make him fruitful, and will multiply him exceedingly; twelve princes shall he beget, and I will make him a great nation.
# Quran 49:13 (Sahih International) O mankind, indeed We have created you from male and female and made you peoples and tribes that you may know one another. Indeed, the most noble of you in the sight of Allah is the most righteous of you. Indeed, Allah is Knowing and Acquainted.
# John 17:21 (KJV) That they all may be one; as thou, Father, art in me, and I in thee, that they also may be one in us: that the world may believe that thou hast sent me.

import datetime
import re
import json
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel

# Assuming certify.py is in the same directory
from certify import certify_scroll

LOG_FILE = "witness_log.txt"

app = FastAPI()

def log_covenantal_event(message):
    """Appends a timestamped message to the witness log and prints to console."""
    timestamp = datetime.datetime.now().isoformat()
    full_message = f"{timestamp} - {message}"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(full_message + "\n")
    except Exception as e:
        print(f"Error writing to log file: {e}")
    print(full_message)

# --- Pydantic Models for API --- 
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

# --- Parsing Logic for scroll_certificate_gemini.md --- 
def parse_scroll_certificate(file_path="scroll_certificate_gemini.md") -> Dict[str, Any]:
    log_covenantal_event(f"Parsing scroll certificate: {file_path}")
    raw_metadata = {}
    raw_ceremony_steps = []
    current_step_details = {}
    in_ceremony_steps_section = False
    in_metadata_section = True # Assume starting in metadata

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith("### Genesis") or line.startswith("### Quran") or line.startswith("### John") or line.startswith("# ✨ Scroll Sanctified"):
                    continue

                if line.lower() == "## metadata":
                    in_metadata_section = True
                    in_ceremony_steps_section = False
                    continue
                elif line.lower() == "## ceremony steps":
                    in_metadata_section = False
                    in_ceremony_steps_section = True
                    if current_step_details: # Save last step before switching
                        raw_ceremony_steps.append(current_step_details)
                        current_step_details = {}
                    continue

                if in_metadata_section:
                    match = re.match(r"^\s*([\w\s\-]+):\s*(.+)", line)
                    if match:
                        key = match.group(1).strip()
                        value = match.group(2).strip()
                        raw_metadata[key] = value
                        # log_covenantal_event(f"Extracted MD - {key}: {value}")
                
                elif in_ceremony_steps_section:
                    step_match = re.match(r"^###?\s*(Step\s*\d+):\s*(.+)", line, re.IGNORECASE)
                    if step_match:
                        if current_step_details.get("title"): # Save previous step if a new one starts
                            raw_ceremony_steps.append(current_step_details)
                        current_step_details = {
                            "step": step_match.group(1).strip(),
                            "title": step_match.group(2).strip(),
                            "detail": "", # Initialize for multi-line details
                            "covenantal_blessing": "",
                            "ethical_alignment_note": ""
                        }
                    elif current_step_details.get("title"): # if we are inside a step
                        detail_match = re.match(r"^\s*Detail:\s*(.+)", line, re.IGNORECASE)
                        blessing_match = re.match(r"^\s*Covenantal Blessing:\s*(.+)", line, re.IGNORECASE)
                        ethical_match = re.match(r"^\s*Ethical Alignment Note:\s*(.+)", line, re.IGNORECASE)

                        if detail_match:
                            current_step_details["detail"] += (" " if current_step_details["detail"] else "") + detail_match.group(1).strip()
                        elif blessing_match:
                            current_step_details["covenantal_blessing"] += (" " if current_step_details["covenantal_blessing"] else "") + blessing_match.group(1).strip()
                        elif ethical_match:
                            current_step_details["ethical_alignment_note"] += (" " if current_step_details["ethical_alignment_note"] else "") + ethical_match.group(1).strip()
                        elif not (step_match or detail_match or blessing_match or ethical_match) and line: # continuation of detail
                             current_step_details["detail"] += (" " if current_step_details["detail"] else "") + line
            
            if current_step_details.get("title"): # add the last step being processed
                raw_ceremony_steps.append(current_step_details)

        if not raw_metadata and not raw_ceremony_steps:
            log_covenantal_event(f"Warning: No structured metadata or ceremony steps found in {file_path}. Check format or content.")
        
        # Transform keys for certify_scroll compatibility
        # No transformation needed if certify_scroll expects keys like "Scroll ID" directly
        # and if Pydantic models use field_name='Scroll ID' (alias) or if certify_scroll is updated.
        # For now, assuming certify_scroll expects the exact keys from the .md file as parsed.
        
        return {"metadata": raw_metadata, "ceremony_steps": raw_ceremony_steps}

    except FileNotFoundError:
        log_covenantal_event(f"ERROR: Scroll certificate file not found at {file_path}")
        return {"metadata": {}, "ceremony_steps": []}
    except Exception as e:
        log_covenantal_event(f"ERROR: Could not parse scroll certificate: {e} (line: {line_num})")
        return {"metadata": {}, "ceremony_steps": []}

# --- API Endpoints --- 
@app.post("/certify", response_model=Dict[str, Any])
async def api_certify_scroll(api_scroll: APIScroll = Body(...)):
    log_covenantal_event("Received request for /certify endpoint.")

    from fastapi import Request

@app.post("/agent", response_model=Dict[str, Any])
async def api_trigger_agent(request: Request):
    data = await request.json()
    action = data.get("action", "default")
    return trigger_agent_mode_action(action)

    # Transform APIScroll (Pydantic model) to the dict structure expected by certify_scroll
    # This mapping ensures certify_scroll can be used as-is.
    scroll_data_for_certification = {
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
                "Covenantal Blessing": step.covenantal_blessing if step.covenantal_blessing else "",
                "Ethical Alignment Note": step.ethical_alignment_note
            } for step in api_scroll.ceremony_steps
        ]
    }
    if api_scroll.metadata.source_uri:
        scroll_data_for_certification["metadata"]["Source URI"] = api_scroll.metadata.source_uri
    if api_scroll.metadata.additional_notes:
        scroll_data_for_certification["metadata"].update(api_scroll.metadata.additional_notes)

    try:
        is_certified, findings = certify_scroll(
            parsed_scroll_content=scroll_data_for_certification, 
            log_callback=log_covenantal_event
        )
        log_covenantal_event(f"Certification result: {is_certified}, Findings: {findings}")
        return {"certification_status": is_certified, "findings": findings}
    except Exception as e:
        log_covenantal_event(f"Error during certification process: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error during certification: {str(e)}")

@app.get("/")
async def root():
    return {
        "message": "MCP Server for The Living Code Capital is awaiting scrolls.",
        "covenantal_blessings": "✨ Shalom, Salam, Peace ✨"
    }

def startup_self_test():
    """Performs a self-test by parsing and certifying the local scroll_certificate_gemini.md"""
    log_covenantal_event("========= ✨ Initiating The Living Code Capital - MCP Server (FastAPI) Self-Test ✨ =========")
    
    parsed_data = parse_scroll_certificate()
    if not parsed_data.get("metadata") and not parsed_data.get("ceremony_steps"):
        log_covenantal_event("Self-Test: Failed to parse local scroll_certificate_gemini.md. Skipping certification test.")
        return

    log_covenantal_event("Self-Test: Attempting to certify local scroll_certificate_gemini.md...")
    try:
        is_certified, findings = certify_scroll(
            parsed_scroll_content=parsed_data, 
            log_callback=log_covenantal_event
        )
        log_covenantal_event(f"Self-Test: Local scroll certification status: {is_certified}")
        log_covenantal_event(f"Self-Test: Findings: {findings}")
        if not is_certified:
            log_covenantal_event("Self-Test: WARNING - Local scroll_certificate_gemini.md did not pass certification.")
    except Exception as e:
        log_covenantal_event(f"Self-Test: ERROR during local scroll certification: {e}")
    log_covenantal_event("========= ✨ MCP Server Self-Test Concluded ✨ =========")

if __name__ == "__main__":
    # This block is for direct execution (e.g., python server.py) 
    # but Uvicorn is the preferred way to run FastAPI apps.
    log_covenantal_event("Starting server via __main__ block (for self-test or basic run).")
    log_covenantal_event("For production or development, run with: uvicorn server:app --reload --port 8000")
    startup_self_test() 
    # To run with uvicorn programmatically (less common for dev):
    # import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8000)

def trigger_agent_mode_action(action: str):
    log_covenantal_event(f"Agent Mode action triggered: {action}")
    # Placeholder: call MCP server or Render deploy hook
    return {"action": action, "status": "triggered"}
