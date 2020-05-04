import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

port = 465
#password = "hGI7&7v@Y8PM#XXP0G4B"
#smtp_server = "mail.mgurney.co.uk"
#sender_email = "mark@mgurney.co.uk"
smtp_server = "smtp.gmail.com"
sender_email = "mgurney98@gmail.com"
password = "aV16M#xxpP"
receiver_email = "mark@mgurney.co.uk"
message = MIMEMultipart("alternative")
message["Subject"] = "multipart test"
message["From"] = sender_email
message["To"] = receiver_email

text = """\
Hi,
This is the plain text version"""

html = """\
<html>
  <body>
    <p>Hi,<br>
       How are you?<br>
       <a href="http://www.realpython.com">Real Python</a> 
       has many great tutorials.
    </p>
  </body>
</html>
"""

#message = f"""\
#Subject : Python Test Email
#To : {receiver_email}
#From : {sender_email}

#This message is sent by python script"""

part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

message.attach(part1)
message.attach(part2)

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())

