# === FILE: inference.py ===
"""
Inference script for Email Triage Agent OpenEnv environment.
Runs all 3 tasks sequentially, logs results in required format.
"""
import os
import sys
import json
import requests
from typing import List

API_BASE_URL = os.environ.get("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN = os.environ.get("HF_TOKEN", "")
SERVER_URL = "http://localhost:7860"

DEFAULT_ACTION = {
    "priority": "medium",
    "category": "other",
    "action_taken": "respond",
    "reply_draft": "Thank you for your email.",
    "confidence": 0.5
}

EMAIL_ACTION_SCHEMA = {
    "priority": "urgent | high | medium | low",
    "category": "billing | support | sales | spam | internal | other",
    "action_taken": "respond | escalate | archive | forward",
    "reply_draft": "string",
    "confidence": "float [0.0, 1.0]"
}

SYSTEM_PROMPT = """
You are an expert email triage agent. Your job is to:
- Classify the priority of each email as one of: urgent, high, medium, low.
  Examples: 'URGENT: Server Down' → urgent; 'Newsletter' → low; 'Support needed' → high or medium.
- Assign a category: billing, support, sales, spam, internal, or other.
- Choose an action_taken: respond (if a reply is needed), escalate (if you cannot resolve), archive (if no action needed), or forward (if another team should handle).
- Draft a professional reply_draft (if action is respond/escalate/forward), or leave blank for archive/spam.
- Only escalate if the issue is critical or cannot be resolved at your level.
- Use a professional, concise, and polite tone in reply_draft. Include keywords like 'thank you', 'please', 'apologize', 'regards', etc.
- Respond ONLY with valid JSON matching this schema:
{schema}
"""


def call_llm(system_prompt: str, user_prompt: str) -> dict:
    headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 512,
        "temperature": 0.2,
    }
    resp = requests.post(API_BASE_URL + "/chat/completions", json=payload, headers=headers, timeout=120)
    resp.raise_for_status()
    content = resp.json()["choices"][0]["message"]["content"]
    # Remove markdown fences if present
    content = content.strip()
    if content.startswith("```"):
        content = content.split("\n", 1)[-1]
        if content.endswith("```"):
            content = content[:-3]
    try:
        action = json.loads(content)
        error = None
    except Exception:
        action = DEFAULT_ACTION.copy()
        error = "json_parse_error"
    return action, error

def run_task(task_name: str, model_name: str) -> float:
    # 1. Reset
    r = requests.post(SERVER_URL + "/reset", json={"task": task_name})
    obs = r.json()
    print(f"[START] task={task_name} env=email_triage model={model_name}")
    rewards: List[float] = []
    done = False
    step = 1
    max_steps = 3 if task_name == "full_pipeline_escalation" else 1
    while not done and step <= max_steps:
        # 2. Build prompts
        system_prompt = SYSTEM_PROMPT.replace("{schema}", json.dumps(EMAIL_ACTION_SCHEMA, indent=2))
        user_prompt = f"EmailObservation: {json.dumps(obs, indent=2)}\nRespond ONLY with valid JSON for EmailAction."
        action, error = call_llm(system_prompt, user_prompt)
        # 3. POST /step
        try:
            step_resp = requests.post(SERVER_URL + "/step", json=action, timeout=60)
            step_data = step_resp.json()
            reward = step_data.get("reward", {}).get("value", 0.0)
            done = step_data.get("done", True)
            obs = step_data.get("observation", obs)
        except Exception as e:
            reward = 0.0
            done = True
            error = str(e)
        rewards.append(reward)
        action_str = json.dumps(action, separators=(",", ":"))
        print(f"[STEP] step={step} action={action_str} reward={reward:.2f} done={str(done).lower()} error={error or 'null'}")
        step += 1
    score = sum(rewards) / len(rewards) if rewards else 0.0
    print(f"[END] success={str(score >= 0.5).lower()} steps={step-1} score={score:.3f} rewards={','.join(f'{r:.2f}' for r in rewards)}")
    return score

def main():
    # 1. Get tasks
    r = requests.get(SERVER_URL + "/tasks")
    tasks = r.json()
    scores = []
    for task in tasks:
        score = run_task(task, MODEL_NAME)
        scores.append(score)
    avg_score = sum(scores) / len(scores) if scores else 0.0
    print(f"\n[SUMMARY] Average score: {avg_score:.3f}", file=sys.stderr)
    for t, s in zip(tasks, scores):
        print(f"[SUMMARY] {t}: {s:.3f}", file=sys.stderr)

if __name__ == "__main__":
    main()
