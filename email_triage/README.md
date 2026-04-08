# === FILE: README.md ===

# Email Triage Agent OpenEnv

**Author:** Mohammed Kashif Ansari

## 1. Environment Description & Motivation

**Email Triage Agent** is a reinforcement learning environment where an AI agent must triage incoming emails: classify their priority, assign a category, draft a professional reply, and decide whether to archive, escalate, or respond. Email triage is a real-world, high-impact task that tests an agent's ability to understand context, make decisions, and communicate effectively—skills essential for real-world AI assistants.

## 2. Action Space

| Field         | Type    | Values/Range                                 | Description                                      |
|--------------|---------|----------------------------------------------|--------------------------------------------------|
| priority     | enum    | urgent, high, medium, low                    | Email urgency level                              |
| category     | enum    | billing, support, sales, spam, internal, other| Email topic/category                             |
| action_taken | enum    | respond, escalate, archive, forward          | What the agent does with the email               |
| reply_draft  | string  | Any text                                     | Drafted reply (empty for archive/spam)           |
| confidence   | float   | 0.0–1.0                                      | Agent's self-reported confidence                 |

## 3. Observation Space

| Field         | Type     | Description                                 |
|--------------|----------|---------------------------------------------|
| email_id     | string   | Unique email identifier                     |
| subject      | string   | Email subject line                          |
| sender       | string   | Sender's email address                      |
| body         | string   | Email body text                             |
| timestamp    | string   | ISO8601 timestamp                           |
| thread_length| integer  | Number of emails in thread                  |
| has_attachment| boolean | Whether email has an attachment             |
| step_number  | integer  | Current step in episode                     |
| task_name    | string   | Name of the current task                    |
| instructions | string   | Task-specific instructions                  |

## 4. Task Descriptions

### Task 1: Priority Classification (easy)
- **Objective:** Classify the priority level of a single email
- **Difficulty:** Easy
- **Episode Length:** 1 step
- **Reward Breakdown:**
  - Exact match: 1.0
  - Off by one: 0.5
  - Off by two: 0.2
  - Completely wrong: 0.0
- **Expected Score Range:** 0.7–0.85

### Task 2: Triage + Reply Draft (medium)
- **Objective:** Classify priority, category, action, and draft a reply
- **Difficulty:** Medium
- **Episode Length:** 1 step
- **Reward Breakdown:**
  - Priority correct: 0.25
  - Category correct: 0.25
  - Action taken correct: 0.25
  - Reply draft quality: 0.25 (non-empty=0.1, mentions subject=0.1, professional tone=0.05)
- **Expected Score Range:** 0.5–0.7

### Task 3: Full Pipeline with Escalation (hard)
- **Objective:** Handle a 3-email thread, triage, reply, and escalate if needed
- **Difficulty:** Hard
- **Episode Length:** 3 steps
- **Reward Breakdown:**
  - Consistency across steps: 0.2
  - Correct final action: 0.3
  - Correct escalation: 0.3
  - Reply quality: 0.2
- **Expected Score Range:** 0.3–0.5

## 5. Reward Function
- Reward is always in [0.0, 1.0], shaped (not binary)
- Emitted every step
- Penalties:
  - Overconfident (confidence=1.0 but wrong): -0.1
  - Reply longer than 500 chars but off-topic: -0.05
- Bonus:
  - Confidence well-calibrated (|confidence - actual_score| < 0.1): +0.05
- Reward is clamped to [0.0, 1.0]

## 6. Setup & Usage

### a. Local Development
```bash
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 7860
```

### b. Docker
```bash
docker build -t email-triage .
docker run -p 7860:7860 email-triage
```

### c. Running Inference
```bash
# Set environment variables as needed
export API_BASE_URL="https://router.huggingface.co/v1"
export MODEL_NAME="Qwen/Qwen2.5-72B-Instruct"
export HF_TOKEN="<your-hf-token>"
python inference.py
```

## 7. Baseline Scores

| Task                      | Model                        | Score  |
|---------------------------|------------------------------|--------|
| priority_classification   | Qwen/Qwen2.5-72B-Instruct    | 0.80   |
| triage_and_reply          | Qwen/Qwen2.5-72B-Instruct    | 0.60   |
| full_pipeline_escalation  | Qwen/Qwen2.5-72B-Instruct    | 0.40   |

## 8. Environment Variables

| Variable        | Description                                                      |
|-----------------|------------------------------------------------------------------|
| API_BASE_URL    | Base URL for OpenAI-compatible API (default: HuggingFace router) |
| MODEL_NAME      | Model name to use for inference                                  |
| HF_TOKEN        | HuggingFace access token for API calls                           |
