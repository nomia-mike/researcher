import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- Configure directly here for the test ---
FROM_EMAIL = os.environ.get("GMAIL_ADDRESS") or "your_email@gmail.com"
TO_EMAIL = "mikecharles@hotmail.com"
APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

if not APP_PASSWORD:
    raise RuntimeError("Missing GMAIL_APP_PASSWORD. Set it in your environment first.")

def test_send_email():
    subject = "Test email from Gmail SMTP"
    html_body = """
    <html>
      <body style="font-family:Arial,Helvetica,sans-serif;">
        <h2 style="margin:0 0 8px;">Hello 👋</h2>
        <p style="margin:0 0 12px;">
          This is a <strong>test email</strong> sent via Gmail SMTP.
        </p>
        <p style="font-size:12px;color:#666;">
          If you can read this in Outlook, HTML is working correctly!
        </p>
      </body>
    </html>
    """

    # multipart/alternative → plain-text fallback + HTML part
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL

    plain_fallback = "This is a test email. Please view it in an HTML-capable client."
    msg.attach(MIMEText(plain_fallback, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(FROM_EMAIL, APP_PASSWORD)
        smtp.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())

    print(f"✅ Test email sent to {TO_EMAIL}")

if __name__ == "__main__":
    test_send_email()
