# AI Email Parser - Smart Inbox Assistant
import re

def parse_email(email_text):
    subject = re.search(r'Subject: (.*)', email_text)
    priority = "High" if "urgent" in email_text.lower() else "Normal"
    return {
        "subject": subject.group(1) if subject else "No Subject",
        "priority": priority,
        "summary": f"Email is {priority} priority"
    }

# Test
email = "Subject: Project Update - urgent meeting tomorrow"
print(parse_email(email))
