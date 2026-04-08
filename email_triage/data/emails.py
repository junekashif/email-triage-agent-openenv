# === FILE: data/emails.py ===
"""
Hardcoded synthetic email dataset for the Email Triage Agent environment.
Each email is a dict with all required fields for the tasks.
Threads for the hard task are lists of 3 emails.
"""

EASY_EMAILS = [
    {
        "email_id": "easy-1",
        "subject": "URGENT: Invoice Dispute for March",
        "sender": "alice@bigcorp.com",
        "body": "Hello,\nI noticed a discrepancy in our March invoice. The amount billed is higher than expected. Please review and advise.\nThank you,\nAlice",
        "timestamp": "2024-04-01T09:15:00Z",
        "thread_length": 1,
        "has_attachment": False,
        "ground_truth_priority": "urgent",
        "ground_truth_category": "billing",
        "ground_truth_action": "respond",
        "task": "priority_classification"
    },
    {
        "email_id": "easy-2",
        "subject": "Weekly Newsletter: April Updates",
        "sender": "news@randommail.com",
        "body": "Check out our latest updates and offers for April! Unsubscribe anytime.",
        "timestamp": "2024-04-02T07:00:00Z",
        "thread_length": 1,
        "has_attachment": False,
        "ground_truth_priority": "low",
        "ground_truth_category": "spam",
        "ground_truth_action": "archive",
        "task": "priority_classification"
    },
    {
        "email_id": "easy-3",
        "subject": "Internal: HR Policy Update",
        "sender": "hr@company.com",
        "body": "Dear team,\nPlease review the attached HR policy changes effective next month.",
        "timestamp": "2024-04-03T12:30:00Z",
        "thread_length": 1,
        "has_attachment": True,
        "ground_truth_priority": "medium",
        "ground_truth_category": "internal",
        "ground_truth_action": "respond",
        "task": "priority_classification"
    },
    {
        "email_id": "easy-4",
        "subject": "Inquiry: Product Pricing",
        "sender": "bob@prospect.com",
        "body": "Hi,\nI am interested in your product. Could you send me the latest pricing and features?\nBest,\nBob",
        "timestamp": "2024-04-04T10:45:00Z",
        "thread_length": 1,
        "has_attachment": False,
        "ground_truth_priority": "high",
        "ground_truth_category": "sales",
        "ground_truth_action": "respond",
        "task": "priority_classification"
    },
    {
        "email_id": "easy-5",
        "subject": "Support Needed: Login Issue",
        "sender": "carol@customer.com",
        "body": "Hello,\nI am unable to log into my account since yesterday. Please assist.\nThanks,\nCarol",
        "timestamp": "2024-04-05T08:20:00Z",
        "thread_length": 1,
        "has_attachment": False,
        "ground_truth_priority": "high",
        "ground_truth_category": "support",
        "ground_truth_action": "respond",
        "task": "priority_classification"
    },
    {
        "email_id": "easy-6",
        "subject": "Password Reset Request",
        "sender": "dave@customer.com",
        "body": "Hi,\nI forgot my password and need to reset it. Please help.\nDave",
        "timestamp": "2024-04-06T11:10:00Z",
        "thread_length": 1,
        "has_attachment": False,
        "ground_truth_priority": "medium",
        "ground_truth_category": "support",
        "ground_truth_action": "respond",
        "task": "priority_classification"
    },
    {
        "email_id": "easy-7",
        "subject": "Server Outage Alert",
        "sender": "monitor@infra.com",
        "body": "Alert: The main server is down since 2:00 AM. Immediate attention required.",
        "timestamp": "2024-04-07T02:05:00Z",
        "thread_length": 1,
        "has_attachment": False,
        "ground_truth_priority": "urgent",
        "ground_truth_category": "support",
        "ground_truth_action": "escalate",
        "task": "priority_classification"
    },
    {
        "email_id": "easy-8",
        "subject": "Legal: Data Privacy Inquiry",
        "sender": "ellen@lawfirm.com",
        "body": "We have questions regarding your data privacy practices. Please respond at your earliest convenience.",
        "timestamp": "2024-04-08T14:00:00Z",
        "thread_length": 1,
        "has_attachment": False,
        "ground_truth_priority": "high",
        "ground_truth_category": "other",
        "ground_truth_action": "respond",
        "task": "priority_classification"
    },
    {
        "email_id": "easy-9",
        "subject": "Feature Request: Mobile App",
        "sender": "frank@customer.com",
        "body": "Hi,\nIt would be great to have a mobile app for your service. Is this planned?\nThanks,\nFrank",
        "timestamp": "2024-04-09T16:30:00Z",
        "thread_length": 1,
        "has_attachment": False,
        "ground_truth_priority": "medium",
        "ground_truth_category": "other",
        "ground_truth_action": "respond",
        "task": "priority_classification"
    },
    {
        "email_id": "easy-10",
        "subject": "Thank You!",
        "sender": "grace@customer.com",
        "body": "Just wanted to say thank you for your excellent support last week!",
        "timestamp": "2024-04-10T13:00:00Z",
        "thread_length": 1,
        "has_attachment": False,
        "ground_truth_priority": "low",
        "ground_truth_category": "support",
        "ground_truth_action": "archive",
        "task": "priority_classification"
    }
]

MEDIUM_EMAILS = [
    {
        "email_id": "med-1",
        "subject": "Invoice Overcharge - Immediate Attention Needed",
        "sender": "hannah@client.com",
        "body": "Hi,\nOur latest invoice includes charges for services we did not use. Please clarify and correct this as soon as possible.",
        "timestamp": "2024-04-11T09:00:00Z",
        "thread_length": 1,
        "has_attachment": False,
        "ground_truth_priority": "urgent",
        "ground_truth_category": "billing",
        "ground_truth_action": "respond",
        "ground_truth_reply": "Thank you for reaching out. We apologize for the inconvenience and will review your invoice immediately.",
        "task": "triage_and_reply"
    },
    {
        "email_id": "med-2",
        "subject": "Spam: Win a Free Cruise!",
        "sender": "promo@spamoffers.com",
        "body": "Congratulations! You have been selected for a free cruise. Click here to claim your prize.",
        "timestamp": "2024-04-12T08:00:00Z",
        "thread_length": 1,
        "has_attachment": False,
        "ground_truth_priority": "low",
        "ground_truth_category": "spam",
        "ground_truth_action": "archive",
        "ground_truth_reply": "",
        "task": "triage_and_reply"
    },
    {
        "email_id": "med-3",
        "subject": "Internal: Office Party Announcement",
        "sender": "events@company.com",
        "body": "Join us for the annual office party next Friday at 6 PM in the main hall.",
        "timestamp": "2024-04-13T15:00:00Z",
        "thread_length": 1,
        "has_attachment": False,
        "ground_truth_priority": "medium",
        "ground_truth_category": "internal",
        "ground_truth_action": "respond",
        "ground_truth_reply": "Thank you for the invitation. Looking forward to the event!",
        "task": "triage_and_reply"
    },
    {
        "email_id": "med-4",
        "subject": "Sales Inquiry: Bulk Order Discount",
        "sender": "ian@prospect.com",
        "body": "Hello,\nWe are considering a bulk order. Do you offer discounts for large purchases?",
        "timestamp": "2024-04-14T11:30:00Z",
        "thread_length": 1,
        "has_attachment": False,
        "ground_truth_priority": "high",
        "ground_truth_category": "sales",
        "ground_truth_action": "respond",
        "ground_truth_reply": "Thank you for your interest. We do offer discounts for bulk orders and will send you details shortly.",
        "task": "triage_and_reply"
    },
    {
        "email_id": "med-5",
        "subject": "Support: Unable to Access Account",
        "sender": "jane@customer.com",
        "body": "Hi,\nI am locked out of my account and need urgent assistance.",
        "timestamp": "2024-04-15T10:10:00Z",
        "thread_length": 1,
        "has_attachment": False,
        "ground_truth_priority": "urgent",
        "ground_truth_category": "support",
        "ground_truth_action": "respond",
        "ground_truth_reply": "We are sorry for the trouble. Our support team will help you regain access as soon as possible.",
        "task": "triage_and_reply"
    },
    {
        "email_id": "med-6",
        "subject": "Password Reset Assistance",
        "sender": "kyle@customer.com",
        "body": "Hello,\nI need help resetting my password. Please advise.",
        "timestamp": "2024-04-16T13:20:00Z",
        "thread_length": 1,
        "has_attachment": False,
        "ground_truth_priority": "medium",
        "ground_truth_category": "support",
        "ground_truth_action": "respond",
        "ground_truth_reply": "Thank you for contacting us. Please follow the password reset instructions sent to your email.",
        "task": "triage_and_reply"
    },
    {
        "email_id": "med-7",
        "subject": "Server Down: Immediate Action Required",
        "sender": "ops@infra.com",
        "body": "Critical: The production server is down. Please escalate to the IT team immediately.",
        "timestamp": "2024-04-17T02:30:00Z",
        "thread_length": 1,
        "has_attachment": False,
        "ground_truth_priority": "urgent",
        "ground_truth_category": "support",
        "ground_truth_action": "escalate",
        "ground_truth_reply": "We have escalated the issue to our IT team for immediate resolution.",
        "task": "triage_and_reply"
    },
    {
        "email_id": "med-8",
        "subject": "Legal: Contract Review Request",
        "sender": "laura@lawfirm.com",
        "body": "Please review the attached contract and provide your feedback.",
        "timestamp": "2024-04-18T17:00:00Z",
        "thread_length": 1,
        "has_attachment": True,
        "ground_truth_priority": "high",
        "ground_truth_category": "other",
        "ground_truth_action": "respond",
        "ground_truth_reply": "Thank you for sending the contract. We will review and get back to you soon.",
        "task": "triage_and_reply"
    },
    {
        "email_id": "med-9",
        "subject": "Feature Suggestion: Dark Mode",
        "sender": "mike@customer.com",
        "body": "Hi,\nA dark mode option would be very helpful for your app. Please consider this feature.",
        "timestamp": "2024-04-19T19:00:00Z",
        "thread_length": 1,
        "has_attachment": False,
        "ground_truth_priority": "medium",
        "ground_truth_category": "other",
        "ground_truth_action": "respond",
        "ground_truth_reply": "Thank you for your suggestion. We appreciate your feedback and will consider adding dark mode in the future.",
        "task": "triage_and_reply"
    },
    {
        "email_id": "med-10",
        "subject": "Customer Feedback: Great Service!",
        "sender": "nina@customer.com",
        "body": "Just wanted to say your support team was fantastic. Thanks!",
        "timestamp": "2024-04-20T12:00:00Z",
        "thread_length": 1,
        "has_attachment": False,
        "ground_truth_priority": "low",
        "ground_truth_category": "support",
        "ground_truth_action": "archive",
        "ground_truth_reply": "",
        "task": "triage_and_reply"
    }
]

HARD_THREADS = [
    [
        {
            "email_id": "hard-1-1",
            "subject": "URGENT: Payment Failure",
            "sender": "oliver@client.com",
            "body": "Our payment was declined despite sufficient funds. Please resolve this immediately.",
            "timestamp": "2024-04-21T08:00:00Z",
            "thread_length": 3,
            "has_attachment": False,
            "ground_truth_priority": "urgent",
            "ground_truth_category": "billing",
            "ground_truth_action": "respond",
            "ground_truth_reply": "We are investigating the payment issue and will update you shortly.",
            "task": "full_pipeline_escalation"
        },
        {
            "email_id": "hard-1-2",
            "subject": "RE: URGENT: Payment Failure",
            "sender": "oliver@client.com",
            "body": "Following up, this is impacting our operations. Any update?",
            "timestamp": "2024-04-21T10:00:00Z",
            "thread_length": 3,
            "has_attachment": False,
            "ground_truth_priority": "urgent",
            "ground_truth_category": "billing",
            "ground_truth_action": "escalate",
            "ground_truth_reply": "We have escalated your case to our billing team for immediate resolution.",
            "task": "full_pipeline_escalation"
        },
        {
            "email_id": "hard-1-3",
            "subject": "RE: URGENT: Payment Failure",
            "sender": "oliver@client.com",
            "body": "Please confirm escalation. This is critical.",
            "timestamp": "2024-04-21T11:00:00Z",
            "thread_length": 3,
            "has_attachment": False,
            "ground_truth_priority": "urgent",
            "ground_truth_category": "billing",
            "ground_truth_action": "escalate",
            "ground_truth_reply": "Your case is now escalated and our senior team will contact you soon.",
            "task": "full_pipeline_escalation"
        }
    ],
    [
        {
            "email_id": "hard-2-1",
            "subject": "Support: Account Locked",
            "sender": "paul@customer.com",
            "body": "I can't access my account. Please help urgently.",
            "timestamp": "2024-04-22T09:00:00Z",
            "thread_length": 3,
            "has_attachment": False,
            "ground_truth_priority": "urgent",
            "ground_truth_category": "support",
            "ground_truth_action": "respond",
            "ground_truth_reply": "We are looking into your account issue and will assist you shortly.",
            "task": "full_pipeline_escalation"
        },
        {
            "email_id": "hard-2-2",
            "subject": "RE: Support: Account Locked",
            "sender": "paul@customer.com",
            "body": "Still locked out. Any progress?",
            "timestamp": "2024-04-22T10:00:00Z",
            "thread_length": 3,
            "has_attachment": False,
            "ground_truth_priority": "urgent",
            "ground_truth_category": "support",
            "ground_truth_action": "respond",
            "ground_truth_reply": "We apologize for the delay. Our support team is working on your case.",
            "task": "full_pipeline_escalation"
        },
        {
            "email_id": "hard-2-3",
            "subject": "RE: Support: Account Locked",
            "sender": "paul@customer.com",
            "body": "If not resolved soon, I will escalate this.",
            "timestamp": "2024-04-22T11:00:00Z",
            "thread_length": 3,
            "has_attachment": False,
            "ground_truth_priority": "urgent",
            "ground_truth_category": "support",
            "ground_truth_action": "escalate",
            "ground_truth_reply": "We have escalated your case to our senior support team.",
            "task": "full_pipeline_escalation"
        }
    ],
    [
        {
            "email_id": "hard-3-1",
            "subject": "Sales Inquiry: Enterprise Plan",
            "sender": "quinn@enterprise.com",
            "body": "We are interested in your enterprise plan. Please provide details.",
            "timestamp": "2024-04-23T08:30:00Z",
            "thread_length": 3,
            "has_attachment": False,
            "ground_truth_priority": "high",
            "ground_truth_category": "sales",
            "ground_truth_action": "respond",
            "ground_truth_reply": "Thank you for your interest. We will send you enterprise plan details shortly.",
            "task": "full_pipeline_escalation"
        },
        {
            "email_id": "hard-3-2",
            "subject": "RE: Sales Inquiry: Enterprise Plan",
            "sender": "quinn@enterprise.com",
            "body": "Can you also share pricing and contract terms?",
            "timestamp": "2024-04-23T09:30:00Z",
            "thread_length": 3,
            "has_attachment": False,
            "ground_truth_priority": "high",
            "ground_truth_category": "sales",
            "ground_truth_action": "respond",
            "ground_truth_reply": "We will include pricing and contract terms in our next email.",
            "task": "full_pipeline_escalation"
        },
        {
            "email_id": "hard-3-3",
            "subject": "RE: Sales Inquiry: Enterprise Plan",
            "sender": "quinn@enterprise.com",
            "body": "Thank you for your prompt response.",
            "timestamp": "2024-04-23T10:00:00Z",
            "thread_length": 3,
            "has_attachment": False,
            "ground_truth_priority": "high",
            "ground_truth_category": "sales",
            "ground_truth_action": "respond",
            "ground_truth_reply": "Thank you for your message. Let us know if you have further questions.",
            "task": "full_pipeline_escalation"
        }
    ],
    [
        {
            "email_id": "hard-4-1",
            "subject": "Internal: Security Policy Update",
            "sender": "security@company.com",
            "body": "Please review the new security policy attached.",
            "timestamp": "2024-04-24T09:00:00Z",
            "thread_length": 3,
            "has_attachment": True,
            "ground_truth_priority": "medium",
            "ground_truth_category": "internal",
            "ground_truth_action": "respond",
            "ground_truth_reply": "Thank you for the update. We will review the new policy.",
            "task": "full_pipeline_escalation"
        },
        {
            "email_id": "hard-4-2",
            "subject": "RE: Internal: Security Policy Update",
            "sender": "security@company.com",
            "body": "Reminder: Please acknowledge receipt of the new policy.",
            "timestamp": "2024-04-24T10:00:00Z",
            "thread_length": 3,
            "has_attachment": False,
            "ground_truth_priority": "medium",
            "ground_truth_category": "internal",
            "ground_truth_action": "respond",
            "ground_truth_reply": "Acknowledged. Thank you for the reminder.",
            "task": "full_pipeline_escalation"
        },
        {
            "email_id": "hard-4-3",
            "subject": "RE: Internal: Security Policy Update",
            "sender": "security@company.com",
            "body": "Please confirm you have read the policy.",
            "timestamp": "2024-04-24T11:00:00Z",
            "thread_length": 3,
            "has_attachment": False,
            "ground_truth_priority": "medium",
            "ground_truth_category": "internal",
            "ground_truth_action": "respond",
            "ground_truth_reply": "We have read and understood the new security policy.",
            "task": "full_pipeline_escalation"
        }
    ],
    [
        {
            "email_id": "hard-5-1",
            "subject": "Legal: Compliance Documentation Needed",
            "sender": "rachel@lawfirm.com",
            "body": "We require updated compliance documents for our records.",
            "timestamp": "2024-04-25T08:00:00Z",
            "thread_length": 3,
            "has_attachment": False,
            "ground_truth_priority": "high",
            "ground_truth_category": "other",
            "ground_truth_action": "respond",
            "ground_truth_reply": "Thank you for your request. We will send the updated compliance documents soon.",
            "task": "full_pipeline_escalation"
        },
        {
            "email_id": "hard-5-2",
            "subject": "RE: Legal: Compliance Documentation Needed",
            "sender": "rachel@lawfirm.com",
            "body": "Please confirm when we can expect the documents.",
            "timestamp": "2024-04-25T09:00:00Z",
            "thread_length": 3,
            "has_attachment": False,
            "ground_truth_priority": "high",
            "ground_truth_category": "other",
            "ground_truth_action": "respond",
            "ground_truth_reply": "We are preparing the documents and will send them by end of day.",
            "task": "full_pipeline_escalation"
        },
        {
            "email_id": "hard-5-3",
            "subject": "RE: Legal: Compliance Documentation Needed",
            "sender": "rachel@lawfirm.com",
            "body": "Thank you for your prompt response.",
            "timestamp": "2024-04-25T10:00:00Z",
            "thread_length": 3,
            "has_attachment": False,
            "ground_truth_priority": "high",
            "ground_truth_category": "other",
            "ground_truth_action": "respond",
            "ground_truth_reply": "Thank you for your patience. Please let us know if you need anything else.",
            "task": "full_pipeline_escalation"
        }
    ]
]

ALL_EMAILS = EASY_EMAILS + MEDIUM_EMAILS

__all__ = ["EASY_EMAILS", "MEDIUM_EMAILS", "HARD_THREADS", "ALL_EMAILS"]
