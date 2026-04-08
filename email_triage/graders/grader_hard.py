# === FILE: graders/grader_hard.py ===
"""
Grader for Task 3: Full Pipeline with Escalation (hard)
"""
from ..email_triage_env import EmailAction

PRIORITY_LEVELS = ["urgent", "high", "medium", "low"]
ACTIONS = ["respond", "escalate", "archive", "forward"]
PROFESSIONAL_KEYWORDS = ["thank you", "regards", "sincerely", "apologize", "appreciate", "please", "best"]

# For hard task, we need to track consistency and escalation logic across steps.

def grade_full_pipeline_escalation(action: EmailAction, thread: list, idx: int, env) -> tuple:
    # env is the EmailTriageEnv instance (for state tracking)
    gt_email = thread[idx]
    reward = 0.0
    breakdown = {}
    feedback = []
    # Consistency: did not contradict previous step
    consistent = True
    if idx > 0 and env._last_action:
        prev_action = env._last_action
        if prev_action.priority != action.priority or prev_action.category != action.category:
            consistent = False
    breakdown["consistency"] = 0.2 if consistent else 0.0
    reward += breakdown["consistency"]
    if consistent:
        feedback.append("Consistent with previous step.")
    else:
        feedback.append("Inconsistent with previous step.")
    # Correct final action_taken (only at last step)
    if idx == 2:
        if action.action_taken == gt_email["ground_truth_action"]:
            breakdown["final_action_correct"] = 0.3
            reward += 0.3
            feedback.append("Final action correct.")
        else:
            breakdown["final_action_correct"] = 0.0
            feedback.append(f"Final action wrong: {action.action_taken} vs {gt_email['ground_truth_action']}.")
    else:
        breakdown["final_action_correct"] = 0.0
    # Correct escalation decision (escalate only when required)
    escalate_needed = any(e["ground_truth_action"] == "escalate" for e in thread)
    escalate_taken = action.action_taken == "escalate"
    if escalate_needed and escalate_taken:
        breakdown["escalation_decision"] = 0.3
        reward += 0.3
        feedback.append("Escalation correctly chosen.")
    elif not escalate_needed and not escalate_taken:
        breakdown["escalation_decision"] = 0.3
        reward += 0.3
        feedback.append("No escalation needed and not escalated.")
    else:
        breakdown["escalation_decision"] = 0.0
        feedback.append("Escalation decision incorrect.")
    # Reply quality (across all steps)
    reply_score = 0.0
    reply = (action.reply_draft or "").strip()
    subj = gt_email["subject"].lower()
    if reply:
        reply_score += 0.1
        if any(word in reply.lower() for word in subj.split()):
            reply_score += 0.1
        if any(kw in reply.lower() for kw in PROFESSIONAL_KEYWORDS):
            reply_score += 0.05
    breakdown["reply_quality"] = round(reply_score, 3)
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
