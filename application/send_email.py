import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import current_app as app
from flask import url_for, render_template
from itsdangerous import URLSafeTimedSerializer


def send_email(receiver_email, subject):

    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "mgurney98@gmail.com"
    password = "aV16M#xxpP"
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    if subject == "Lending Library - Password Reset":
        password_reset_serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])

        password_reset_url = url_for(
            "reset_with_token",
            token=password_reset_serializer.dumps(receiver_email, salt="93kjng02"),
            _external=True,
        )

        html_text = render_template(
            "password_reset_email.html", password_reset_url=password_reset_url
        )

        plain_text = """\
        Hi,
        This is the plain text version"""

    part1 = MIMEText(plain_text, "plain_text")
    part2 = MIMEText(html_text, "html")
    message.attach(part1)
    message.attach(part2)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
