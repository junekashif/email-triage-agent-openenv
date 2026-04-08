# === FILE: graders/grader_medium.py ===
"""
Grader for Task 2: Triage + Reply Draft (medium)
"""
from ..email_triage_env import EmailAction

PRIORITY_LEVELS = ["urgent", "high", "medium", "low"]
CATEGORIES = ["billing", "support", "sales", "spam", "internal", "other"]
ACTIONS = ["respond", "escalate", "archive", "forward"]

PROFESSIONAL_KEYWORDS = ["thank you", "regards", "sincerely", "apologize", "appreciate", "please", "best"]

def grade_triage_and_reply(action: EmailAction, email: dict):
    gt_priority = email["ground_truth_priority"]
    gt_category = email["ground_truth_category"]
    gt_action = email["ground_truth_action"]
    gt_reply = email.get("ground_truth_reply", "")
    reward = 0.0
    breakdown = {}
    feedback = []
    # Priority
    try:
        if action.priority == gt_priority:
            breakdown["priority_correct"] = 0.25
            reward += 0.25
            feedback.append("Priority correct.")
        else:
            breakdown["priority_correct"] = 0.0
            feedback.append(f"Priority wrong: {action.priority} vs {gt_priority}.")
    except Exception:
        breakdown["priority_correct"] = 0.0
        feedback.append("Invalid priority.")
    # Category
    try:
        if action.category == gt_category:
            breakdown["category_correct"] = 0.25
            reward += 0.25
            feedback.append("Category correct.")
        else:
            breakdown["category_correct"] = 0.0
            feedback.append(f"Category wrong: {action.category} vs {gt_category}.")
    except Exception:
        breakdown["category_correct"] = 0.0
        feedback.append("Invalid category.")
    # Action
    try:
        if action.action_taken == gt_action:
            breakdown["action_taken_correct"] = 0.25
            reward += 0.25
            feedback.append("Action correct.")
        else:
            breakdown["action_taken_correct"] = 0.0
            feedback.append(f"Action wrong: {action.action_taken} vs {gt_action}.")
    except Exception:
        breakdown["action_taken_correct"] = 0.0
        feedback.append("Invalid action.")
    # Reply draft quality
    reply_score = 0.0
    reply = (action.reply_draft or "").strip()
    if gt_action in ["respond", "escalate", "forward"]:
        if reply:
            reply_score += 0.1
            feedback.append("Reply non-empty.")
            subj = email["subject"].lower()
            if any(word in reply.lower() for word in subj.split()):
                reply_score += 0.1
                feedback.append("Reply mentions subject topic.")
            if any(kw in reply.lower() for kw in PROFESSIONAL_KEYWORDS):
                reply_score += 0.05
                feedback.append("Professional tone present.")
        else:
            feedback.append("Reply empty.")
    else:
        if not reply:
            reply_score += 0.25
            feedback.append("Correctly left reply empty.")
        else:
            feedback.append("Reply should be empty for archive/spam.")
    breakdown["reply_draft_quality"] = round(reply_score, 3)
    reward += reply_score
    # Penalty: confidence=1.0 but wrong
    if reward < 1.0 and abs(action.confidence - 1.0) < 1e-6:
        reward -= 0.1
        breakdown["confidence_penalty"] = -0.1
        feedback.append("Overconfident on wrong answer.")
    # Penalty: reply too long but off-topic
    if len(reply) > 500 and reply_score < 0.15:
        reward -= 0.05
        breakdown["reply_length_penalty"] = -0.05
        feedback.append("Reply too long and off-topic.")
    # Bonus: confidence well-calibrated
    if abs(action.confidence - reward) < 0.1:
        reward += 0.05
        breakdown["confidence_bonus"] = 0.05
        feedback.append("Confidence well-calibrated.")
    reward = max(0.0, min(1.0, reward))
    return reward, breakdown, "; ".join(feedback)
