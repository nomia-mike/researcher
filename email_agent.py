"""
email_agent
This agent reformats the report as HTML and send it out as an email
The sender and adressee are picked up from constants.py
"""
# Standard libraries
import os
import certifi
from typing import Dict
# 3rd part libraries
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from agents import Agent, function_tool
# Local libraries
from constants import FROM_EMAIL, TO_EMAIL


# Make urllib/requests use certifi's CA bundle
os.environ.setdefault("SSL_CERT_FILE", certifi.where())
os.environ.setdefault("REQUESTS_CA_BUNDLE", certifi.where())


@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """
    Send an HTML email via Gmail SMTP (SSL 465) with a plain-text fallback.
    Drop-in replacement for the original SendGrid-based function.
    Assumes only one recipient (TO_EMAIL is a string).
    """
    gmail_address = os.environ.get("GMAIL_ADDRESS") or FROM_EMAIL
    app_password = os.environ.get("GMAIL_APP_PASSWORD")
    if not app_password:
        raise RuntimeError("GMAIL_APP_PASSWORD not set. Create a Gmail App Password and export it.")

    # multipart/alternative ensures HTML displays correctly in Outlook and others
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = gmail_address
    msg["To"] = TO_EMAIL

    # simple plain-text fallback
    plain_fallback = "This email contains HTML content. Please view it in an HTML-capable client."
    msg.attach(MIMEText(plain_fallback, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    # Send via Gmail SMTP over SSL
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(gmail_address, app_password)
        smtp.sendmail(gmail_address, TO_EMAIL, msg.as_string())

    return {"status": "success"}


INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)
