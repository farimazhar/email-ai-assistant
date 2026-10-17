from flask import Flask, request, jsonify, render_template_string
import re
from datetime import datetime

app = Flask(__name__)

def parse_email_smart(email_text):
    # Subject
    subject_match = re.search(r'Subject:\s*(.*)', email_text, re.IGNORECASE)
    subject = subject_match.group(1).strip() if subject_match else "No Subject Found"

    # Priority Logic
    urgent_words = ["urgent", "asap", "emergency", "important", "immediate"]
    text_lower = email_text.lower()
    priority = "High 🔴" if any(word in text_lower for word in urgent_words) else "Normal 🟢"

    # Type
    if "meeting" in text_lower:
        email_type = "Meeting"
    elif "project" in text_lower or "update" in text_lower:
        email_type = "Project Update"
    elif "invoice" in text_lower or "payment" in text_lower:
        email_type = "Finance"
    else:
        email_type = "General"

    # Summary
    summary = f"This is a {priority} priority {email_type} email about '{subject}'."

    return {
        "subject": subject,
        "priority": priority,
        "type": email_type,
        "summary": summary,
        "received": datetime.now().strftime("%d %B %Y, %I:%M %p")
    }

# --- FRONTEND ---
HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Email AI Assistant | Fari Mazhar</title>
<style>
body{font-family:system-ui; background:#0f0f0f; color:white; padding:15px; margin:0}
.container{max-width:600px; margin:auto}
h2{color:#00ff88}
.card{background:#1e1e1e; padding:20px; border-radius:12px; border:1px solid #333}
textarea{width:100%; background:#2a2a2a; color:white; border:1px solid #444; border-radius:8px; padding:12px; font-size:16px; box-sizing:border-box}
button{width:100%; background:#00ff88; color:black; border:none; padding:14px; border-radius:8px; font-weight:bold; font-size:16px; margin-top:12px; cursor:pointer}
.result{background:#2a2a2a; padding:15px; border-radius:8px; margin-top:20px; text-align:left; border-left:4px solid #00ff88}
.tag{display:inline-block; background:#333; padding:4px 10px; border-radius:20px; font-size:12px; margin:5px 5px 0 0}
</style>
</head>
<body>
<div class="container">
<h2>📧 Email AI Assistant</h2>
<p style="color:#aaa">Smart Inbox Parser by Fari Mazhar - Gujrat, PK</p>
<div class="card">
<textarea id="email" rows="4" placeholder="Try: Subject: Project Update - urgent meeting tomorrow at 10am">Subject: Project Update - urgent meeting tomorrow</textarea>
<button onclick="go()">🤖 Parse Email with AI</button>
<div id="out"></div>
</div>
<p style="text-align:center; color:#666; font-size:12px; margin-top:20px">Made in Gujrat, Pakistan 🇵🇰 | Live on Vercel</p>
</div>
<script>
async function go(){
 let text = document.getElementById('email').value;
 if(!text){alert('Email likho pehle!'); return}
 document.getElementById('out').innerHTML = '⏳ Analyzing...';
 let r = await fetch('/api/parse', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({text})});
 let d = await r.json();
 document.getElementById('out').innerHTML = `<div class='result'>
 <b>📌 Subject:</b> ${d.subject}<br><br>
 <span class='tag'>${d.priority}</span> <span class='tag'>${d.type}</span><br><br>
 <b>📝 AI Summary:</b><br>${d.summary}<br><br>
 <small style='color:#888'>🕒 ${d.received}</small>
 </div>`;
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/api/parse', methods=['POST'])
def api():
    data = request.get_json()
    result = parse_email_smart(data.get('text',''))
    return jsonify(result)

# Vercel needs this
# app = app
