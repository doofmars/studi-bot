verbose = 0

# Options for sending an E-Mail, when change happened
send_mail = 1  # 1== Enabled
smtp_user = "sender@sender.com"
smtp_password = "password"
smtp_server = "yourserver"
smtp_port = 587
sender = smtp_user
receivers = ['receiver@receiver.com']

# Set Your message
message_addresults = 1
message = """From: Studi-Bot <python@doofmars.de>
To: Receiver
Subject: Studi-Portal: Something has Changed

Something has Changed!

Goto https://studi-portal.hs-furtwangen.de to look it up!
"""

# Studi-Portal Options
studi_url = "https://studi-portal.hs-furtwangen.de"
studi_user = 'hfu_name'
studi_password = 'password'

# Add the courses you want to track here
track = ["Sprachen",
         "Datenbanken",
         "Mathematik"]
