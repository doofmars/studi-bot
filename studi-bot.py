import mechanize
import os
import hashlib
import smtplib
from mechanize import ParseResponse
from config import *
from bs4 import BeautifulSoup

br = mechanize.Browser()

# Browser options
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

#open hs-furtwangen
br.open(studi_url)

######
print time.strftime("%Y-%m-%d %H:%M:%S")
print "Fetching the following courses from ", studi_url

#Select current form set
br.select_form(nr=0)

#Login User
br.form["asdf"] = studi_user
br.form["fdsa"] = studi_password
br.submit()

#Navigate to Notenspiegel
br.follow_link(text_regex="Meine Pr\xc3\xbcfungen")
br.follow_link(text_regex="Notenspiegel")

#Convert HTML Page to Soup
html = br.response().read()
soup = BeautifulSoup(html)

#Get Old hash
hash_old = ""
new_string = ""
if os.path.isfile("cache.txt"):
    fi = open("cache.txt", "r")
    hash_old = fi.read()
    fi.close()

#Loop to gather results
i = 0
for td in soup.findAll('td'):
    if i == 0:
        for candidate in track:
            if td.get_text().find(candidate) >= 0:
                print td.get_text()
                new_string += td.get_text()
                i = 9
                break
    elif i > 0:
        if verbose:
            print td.get_text()
        new_string += td.get_text()
        i -= 1

#Generate hash from results
hash_new_string = hashlib.md5(new_string.encode('utf-8'))
if verbose:
    print(hash_new_string.hexdigest())

#Save new Hash
fo = open("cache.txt", "w")
fo.write(hash_new_string.hexdigest())
fo.close()

#Compare Hash and Send Mail
if hash_old != "":
    if hash_old != hash_new_string.hexdigest():
        print "Something has Changed"
        if send_mail:
            try:
               smtpObj = smtplib.SMTP('aquila.uberspace.de', 587)
               smtpObj.login(smtp_user,smtp_password)
               smtpObj.sendmail(sender, receivers, message)
               print "Successfully sent email"
            except smtplib.SMTPException:
               print "Error: unable to send email"
    else:
        print "\n\nNothing new"

#Sign out
br.follow_link(text_regex="Abmelden")