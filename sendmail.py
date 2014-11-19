import smtplib

SERVER = "localhost"

FROM = "8274634@qq.com"
TO = ["58502944@qq.com"] # must be a list

SUBJECT = "Hello!"

TEXT = "This message was sent with Python's smtplib."

# Prepare actual message

message = """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)

# Send the mail

server = smtplib.SMTP(SERVER)
print server.sendmail(FROM, TO, message)
server.quit()
