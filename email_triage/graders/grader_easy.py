# === FILE: graders/grader_easy.py ===
"""
Grader for Task 1: Priority Classification (easy)
"""
from ..email_triage_env import EmailAction

PRIORITY_LEVELS = ["urgent", "high", "medium", "low"]


def grade_priority_classification(action: EmailAction, email: dict):
    gt = email["ground_truth_priority"]
    pred = action.priority
    breakdown = {}
    feedback = ""
    try:
        gt_idx = PRIORITY_LEVELS.index(gt)
        pred_idx = PRIORITY_LEVELS.index(pred)
    except ValueError:
        breakdown["priority_correct"] = 0.0
        feedback = f"Invalid priority: {pred}."
        reward = 0.0
    else:
        diff = abs(gt_idx - pred_idx)
        if diff == 0:
            reward = 1.0
            breakdown["priority_correct"] = 1.0
            feedback = "Correct priority."
        elif diff == 1:
            reward = 0.5
            breakdown["priority_correct"] = 0.5
            feedback = f"Off by one level: predicted {pred}, actual {gt}."
        elif diff == 2:
            reward = 0.2
            breakdown["priority_correct"] = 0.2
            feedback = f"Off by two levels: predicted {pred}, actual {gt}."
        else:
            reward = 0.0
            breakdown["priority_correct"] = 0.0
            feedback = f"Completely wrong: predicted {pred}, actual {gt}."
    # Penalty: confidence=1.0 but wrong
    if reward < 1.0 and abs(action.confidence - 1.0) < 1e-6:
        reward -= 0.1
        breakdown["confidence_penalty"] = -0.1
        feedback += " Overconfident on wrong answer."
    # Bonus: confidence well-calibrated
    if abs(action.confidence - reward) < 0.1:
        reward += 0.05
        breakdown["confidence_bonus"] = 0.05
        feedback += " Confidence well-calibrated."
    reward = max(0.0, min(1.0, reward))
    return reward, breakdown, feedback
