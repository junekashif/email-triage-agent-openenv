# === FILE: tests/test_env.py ===
"""
Pytest tests for Email Triage Agent environment.
"""
import pytest
from email_triage.email_triage_env import EmailTriageEnv, EmailAction
from email_triage.data.emails import EASY_EMAILS, MEDIUM_EMAILS, HARD_THREADS

def test_reset_returns_valid_observation():
    env = EmailTriageEnv(seed=123)
    for task in ["priority_classification", "triage_and_reply", "full_pipeline_escalation"]:
        obs = env.reset(task=task)
        assert obs.email_id
        assert obs.subject
        assert obs.sender
        assert obs.body
        assert obs.timestamp
        assert obs.thread_length >= 1
        assert isinstance(obs.has_attachment, bool)
        assert obs.step_number == 1
        assert obs.task_name == task
        assert obs.instructions

def test_step_returns_reward_in_range():
    env = EmailTriageEnv(seed=123)
    env.reset(task="priority_classification")
    email = env.current_email
    action = EmailAction(priority=email["ground_truth_priority"], category=email["ground_truth_category"], action_taken=email["ground_truth_action"], reply_draft="", confidence=0.8)
    obs, reward, done, info = env.step(action)
    assert 0.0 <= reward.value <= 1.0

def test_step_perfect_action_reward_easy():
    env = EmailTriageEnv(seed=123)
    env.reset(task="priority_classification")
    email = env.current_email
    action = EmailAction(priority=email["ground_truth_priority"], category=email["ground_truth_category"], action_taken=email["ground_truth_action"], reply_draft="", confidence=1.0)
    obs, reward, done, info = env.step(action)
    assert reward.value >= 0.8

def test_state_returns_expected_keys():
    env = EmailTriageEnv(seed=123)
    env.reset(task="triage_and_reply")
    state = env.state()
    expected_keys = {"task_name", "step_number", "max_steps", "done", "current_email", "current_thread", "thread_idx", "last_action", "last_reward", "last_observation"}
    assert set(state.keys()) == expected_keys

def test_done_after_max_steps():
    env = EmailTriageEnv(seed=123)
    # Easy
    env.reset(task="priority_classification")
    email = env.current_email
    action = EmailAction(priority=email["ground_truth_priority"], category=email["ground_truth_category"], action_taken=email["ground_truth_action"], reply_draft="", confidence=1.0)
    obs, reward, done, info = env.step(action)
    assert done
    # Medium
    env.reset(task="triage_and_reply")
    email = env.current_email
    action = EmailAction(priority=email["ground_truth_priority"], category=email["ground_truth_category"], action_taken=email["ground_truth_action"], reply_draft=email.get("ground_truth_reply", ""), confidence=1.0)
    obs, reward, done, info = env.step(action)
    assert done
    # Hard
    env.reset(task="full_pipeline_escalation")
    thread = env.current_thread
    for idx in range(3):
        email = thread[idx]
        action = EmailAction(priority=email["ground_truth_priority"], category=email["ground_truth_category"], action_taken=email["ground_truth_action"], reply_draft=email.get("ground_truth_reply", ""), confidence=1.0)
        obs, reward, done, info = env.step(action)
    assert done

def test_graders_are_deterministic():
    from email_triage.graders.grader_easy import grade_priority_classification
    from email_triage.graders.grader_medium import grade_triage_and_reply
    from email_triage.graders.grader_hard import grade_full_pipeline_escalation
    email = EASY_EMAILS[0]
    action = EmailAction(priority=email["ground_truth_priority"], category=email["ground_truth_category"], action_taken=email["ground_truth_action"], reply_draft="", confidence=1.0)
    r1, b1, f1 = grade_priority_classification(action, email)
    r2, b2, f2 = grade_priority_classification(action, email)
    assert r1 == r2 and b1 == b2 and f1 == f2
    email = MEDIUM_EMAILS[0]
    action = EmailAction(priority=email["ground_truth_priority"], category=email["ground_truth_category"], action_taken=email["ground_truth_action"], reply_draft=email.get("ground_truth_reply", ""), confidence=1.0)
    r1, b1, f1 = grade_triage_and_reply(action, email)
    r2, b2, f2 = grade_triage_and_reply(action, email)
    assert r1 == r2 and b1 == b2 and f1 == f2
    thread = HARD_THREADS[0]
    for idx in range(3):
        email = thread[idx]
        action = EmailAction(priority=email["ground_truth_priority"], category=email["ground_truth_category"], action_taken=email["ground_truth_action"], reply_draft=email.get("ground_truth_reply", ""), confidence=1.0)
        r1, b1, f1 = grade_full_pipeline_escalation(action, thread, idx, EmailTriageEnv())
        r2, b2, f2 = grade_full_pipeline_escalation(action, thread, idx, EmailTriageEnv())
        assert r1 == r2 and b1 == b2 and f1 == f2
