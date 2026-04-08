# === FILE: server.py ===
"""
FastAPI server for the Email Triage Agent environment.
Exposes /reset, /step, /state, /health, /tasks endpoints.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from .email_triage_env import EmailTriageEnv, EmailAction, EmailObservation, EmailReward
import uvicorn
from typing import Dict
import threading

app = FastAPI()

# Allow all CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

global_env = EmailTriageEnv(seed=42)
global_lock = threading.Lock()

TASKS = [
    {
        "name": "priority_classification",
        "difficulty": "easy",
        "description": "Classify the priority level of a single email",
        "max_steps": 1,
        "reward_range": [0.0, 1.0],
    },
    {
        "name": "triage_and_reply",
        "difficulty": "medium",
        "description": "Classify priority, category, action and draft a reply",
        "max_steps": 1,
        "reward_range": [0.0, 1.0],
    },
    {
        "name": "full_pipeline_escalation",
        "difficulty": "hard",
        "description": "Handle a 3-email thread with consistent triage and escalation decisions",
        "max_steps": 3,
        "reward_range": [0.0, 1.0],
    },
]

@app.post("/reset")
async def reset(request: Request):
    data = await request.json()
    task = data.get("task", "priority_classification")
    with global_lock:
        obs = global_env.reset(task=task)
    return obs.model_dump()

@app.post("/step")
async def step(request: Request):
    data = await request.json()
    try:
        action = EmailAction(**data)
    except ValidationError as e:
        return {"error": str(e), "observation": None, "reward": None, "done": True, "info": {}}
    with global_lock:
        obs, reward, done, info = global_env.step(action)
    return {
        "observation": obs.model_dump(),
        "reward": reward.model_dump(),
        "done": done,
        "info": info,
    }

@app.get("/state")
async def state():
    with global_lock:
        return global_env.state()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/tasks")
async def tasks():
    return [t["name"] for t in TASKS]

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=7860, reload=False)
