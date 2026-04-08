# === FILE: tasks/task_easy.py ===
"""
Task 1: Priority Classification (easy)
"""
from email_triage.email_triage_env import EmailTriageEnv

def get_easy_task_env(seed=42):
    env = EmailTriageEnv(seed=seed)
    env.reset(task="priority_classification")
    return env
