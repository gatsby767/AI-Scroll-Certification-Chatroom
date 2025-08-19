from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
import os

router = APIRouter()

LOG_FILE_PATH = "ceremony_log.txt"

@router.get("/logs", response_class=PlainTextResponse, tags=["Ceremony"])
async def get_ceremony_logs():
    if not os.path.exists(LOG_FILE_PATH):
        raise HTTPException(status_code=404, detail="Ceremony log file not found.")
    try:
        with open(LOG_FILE_PATH, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading log file: {e}")
