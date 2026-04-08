# === FILE: tasks/task_medium.py ===
"""
Task 2: Triage + Reply Draft (medium)
"""
from email_triage.email_triage_env import EmailTriageEnv

def get_medium_task_env(seed=42):
    env = EmailTriageEnv(seed=seed)
    env.reset(task="triage_and_reply")
    return env
