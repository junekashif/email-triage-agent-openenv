# === FILE: email_triage_env.py ===
"""
Core environment logic for the Email Triage Agent OpenEnv environment.
Implements the EmailTriageEnv class and Pydantic models.
"""
from typing import Tuple, Dict, Any, Optional
from pydantic import BaseModel, Field, StrictStr, StrictFloat, StrictBool, StrictInt
import random
from .data.emails import EASY_EMAILS, MEDIUM_EMAILS, HARD_THREADS

# --- Pydantic Models ---

class EmailObservation(BaseModel):
    email_id: StrictStr
    subject: StrictStr
    sender: StrictStr
    body: StrictStr
    timestamp: StrictStr
    thread_length: StrictInt
    has_attachment: StrictBool
    step_number: StrictInt
    task_name: StrictStr
    instructions: StrictStr

class EmailAction(BaseModel):
    priority: StrictStr  # "urgent" | "high" | "medium" | "low"
    category: StrictStr  # "billing" | "support" | "sales" | "spam" | "internal" | "other"
    action_taken: StrictStr  # "respond" | "escalate" | "archive" | "forward"
    reply_draft: StrictStr
    confidence: StrictFloat  # 0.0 to 1.0

class EmailReward(BaseModel):
    value: StrictFloat  # 0.0 to 1.0
    breakdown: Dict[str, StrictFloat]
    feedback: StrictStr

# --- Environment Class ---

class EmailTriageEnv:
    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        self.task_name = "priority_classification"
        self.step_number = 0
        self.max_steps = 1
        self.current_email = None
        self.current_thread = None
        self.thread_idx = 0
        self.done = False
        self.info = {}
        self._easy_idx = 0
        self._medium_idx = 0
        self._hard_idx = 0
        self._last_action = None
        self._last_reward = None
        self._last_obs = None

    def reset(self, task: Optional[str] = None) -> EmailObservation:
        if task is not None:
            self.task_name = task
        else:
            self.task_name = "priority_classification"
        self.step_number = 1
        self.done = False
        self.info = {}
        self._last_action = None
        self._last_reward = None
        self._last_obs = None
        if self.task_name == "priority_classification":
            self.max_steps = 1
            email = EASY_EMAILS[self._easy_idx % len(EASY_EMAILS)]
            self._easy_idx += 1
            self.current_email = email
            self.current_thread = None
            obs = self._make_observation(email, instructions="Classify the priority of this email.")
        elif self.task_name == "triage_and_reply":
            self.max_steps = 1
            email = MEDIUM_EMAILS[self._medium_idx % len(MEDIUM_EMAILS)]
            self._medium_idx += 1
            self.current_email = email
            self.current_thread = None
            obs = self._make_observation(email, instructions="Classify priority, category, action, and draft a reply.")
        elif self.task_name == "full_pipeline_escalation":
            self.max_steps = 3
            thread = HARD_THREADS[self._hard_idx % len(HARD_THREADS)]
            self._hard_idx += 1
            self.current_thread = thread
            self.thread_idx = 0
            email = thread[0]
            self.current_email = email
            obs = self._make_observation(email, instructions="Handle this email thread: triage, reply, and decide on escalation.")
        else:
            raise ValueError(f"Unknown task: {self.task_name}")
        self._last_obs = obs
        return obs

    def step(self, action: EmailAction) -> Tuple[EmailObservation, EmailReward, bool, dict]:
        self._last_action = action
        if self.task_name == "priority_classification":
            reward, breakdown, feedback = self._grade_easy(action, self.current_email)
            done = True
            obs = self._make_observation(self.current_email, instructions="Classify the priority of this email.")
        elif self.task_name == "triage_and_reply":
            reward, breakdown, feedback = self._grade_medium(action, self.current_email)
            done = True
            obs = self._make_observation(self.current_email, instructions="Classify priority, category, action, and draft a reply.")
        elif self.task_name == "full_pipeline_escalation":
            thread = self.current_thread
            idx = self.thread_idx
            reward, breakdown, feedback = self._grade_hard(action, thread, idx)
            if idx < 2:
                self.thread_idx += 1
                self.current_email = thread[self.thread_idx]
                obs = self._make_observation(self.current_email, instructions="Handle this email thread: triage, reply, and decide on escalation.")
                done = False
            else:
                obs = self._make_observation(self.current_email, instructions="Handle this email thread: triage, reply, and decide on escalation.")
                done = True
        else:
            raise ValueError(f"Unknown task: {self.task_name}")
        self.step_number += 1
        reward_obj = EmailReward(value=reward, breakdown=breakdown, feedback=feedback)
        self._last_reward = reward_obj
        self._last_obs = obs
        self.done = done
        return obs, reward_obj, done, self.info.copy()

    def state(self) -> dict:
        state = {
            "task_name": self.task_name,
            "step_number": self.step_number,
            "max_steps": self.max_steps,
            "done": self.done,
            "current_email": self.current_email,
            "current_thread": self.current_thread,
            "thread_idx": self.thread_idx,
            "last_action": self._last_action.model_dump() if self._last_action else None,
            "last_reward": self._last_reward.model_dump() if self._last_reward else None,
            "last_observation": self._last_obs.model_dump() if self._last_obs else None,
        }
        return state

    def _make_observation(self, email: dict, instructions: str) -> EmailObservation:
        return EmailObservation(
            email_id=email["email_id"],
            subject=email["subject"],
            sender=email["sender"],
            body=email["body"],
            timestamp=email["timestamp"],
            thread_length=email["thread_length"],
            has_attachment=email["has_attachment"],
            step_number=self.step_number,
            task_name=self.task_name,
            instructions=instructions
        )

    # --- Grading Functions ---

    def _grade_easy(self, action: EmailAction, email: dict) -> Tuple[float, dict, str]:
        from email_triage.graders.grader_easy import grade_priority_classification
        return grade_priority_classification(action, email)


    def _grade_medium(self, action: EmailAction, email: dict) -> Tuple[float, dict, str]:
        from email_triage.graders.grader_medium import grade_triage_and_reply
        return grade_triage_and_reply(action, email)


    def _grade_hard(self, action: EmailAction, thread: list, idx: int) -> Tuple[float, dict, str]:
        from email_triage.graders.grader_hard import grade_full_pipeline_escalation
        return grade_full_pipeline_escalation(action, thread, idx, self)

__all__ = [
    "EmailTriageEnv",
    "EmailObservation",
    "EmailAction",
    "EmailReward"
]
