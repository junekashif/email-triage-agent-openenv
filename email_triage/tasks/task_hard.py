# === FILE: tasks/task_hard.py ===
"""
Task 3: Full Pipeline with Escalation (hard)
"""
from email_triage.email_triage_env import EmailTriageEnv

def get_hard_task_env(seed=42):
    env = EmailTriageEnv(seed=seed)
    env.reset(task="full_pipeline_escalation")
    return env
