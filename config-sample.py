verbose = 0

#Options for sending an E-Mail, when change happened
send_mail = 1 # 1== Enabled
smtp_user = "sender@sender.com"
smtp_password = "password"
sender = smtp_user
receivers = ['receiver@receiver.com']

#Set Your message
message = """From: Studi-Bot <python@doofmars.de>
To: Receiver
Subject: Studi-Portal: Something has Changed

Something has Changed!

Goto https://studi-portal.hs-furtwangen.de to look it up!
"""

#Studi-Portal Options
studi_url = "https://studi-portal.hs-furtwangen.de"
studi_user = 'hfu_name'
studi_password = 'password'

#Tracked courses
track = ["Sprachen",
         "Datenbanken",
         "Mathematik"]
