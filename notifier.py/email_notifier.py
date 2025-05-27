# research_rag_agent/notifier/email_notifier.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailNotifier:
    def __init__(self, sender_email, sender_password, smtp_server="smtp.gmail.com", smtp_port=587):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send_digest(self, recipient_email, summaries):
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "📚 Weekly AI Alignment Research Digest"
        msg["From"] = self.sender_email
        msg["To"] = recipient_email

        html = "<h2>Weekly AI Alignment Digest</h2><ul>"
        for paper in summaries:
            html += f"<li><b>{paper['title']}</b><br><a href='{paper['url']}'>Read paper</a><br>{paper['summary']}</li><br><br>"
        html += "</ul>"

        part = MIMEText(html, "html")
        msg.attach(part)

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, recipient_email, msg.as_string())
            server.quit()
            print("[INFO] Email digest sent successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to send email: {e}")
