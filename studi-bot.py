# External packages
import mechanize
from bs4 import BeautifulSoup

# Internal Packages
import os
import hashlib
import smtplib
import ssl
import time
from config import *

br = mechanize.Browser()

# Browser options
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
# br.set_debug_http(True)
# br.set_debug_redirects(True)
# br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent',
                  'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


def fetch_results():
    # open hs-furtwangen
    br.open(studi_url)

    ######
    print(time.strftime("%Y-%m-%d %H:%M:%S"))
    print("Fetching courses from", studi_url)

    # Select current form set
    br.select_form(nr=0)

    # Login User
    br.form["asdf"] = studi_user
    br.form["fdsa"] = studi_password
    br.submit()
    if verbose:
        print("Connected")

    found = False
    # Navigate to grade page
    br.follow_link(text_regex="Prüfungsverwaltung")
    br.follow_link(text_regex="Notenspiegel")
    # Find link with title that contains "studi_type"
    for link in br.links():
        for attr in link.attrs:
            if attr[0] == "title":
                if studi_type in attr[1]:
                    br.follow_link(link)
                    found = True
                    if verbose:
                        print("Found type link")
                    break
    if not found:
        # Cannot get grades navigation is broken
        print("Study type not found")
        return

    if verbose:
        print("Site received")

    # Convert HTML Page to Soup
    html = br.response().read()
    soup = BeautifulSoup(html, "html.parser")

    # Get Old hash
    hash_old = ""
    new_string = ""
    if os.path.isfile("cache.txt"):
        fi = open("cache.txt", "r")
        hash_old = fi.read()
        fi.close()

    if verbose:
        print("Old Hash:", hash_old)
        print("Gather results")

    # Loop to gather results
    i = 0
    for td in soup.findAll('td'):
        if i == 0:
            # Check if td contains one of the courses
            for candidate in track:
                if td.get_text().find(candidate) >= 0:
                    if verbose:
                        print(td.get_text().strip())

                    new_string += "\n" + td.get_text().strip()
                    i = 6
                    break
        # Get the next 5 td's without checking
        elif i > 0:
            if verbose:
                print(td.get_text().strip())

            if i == 5:
                # Get the grade
                new_string += "\t" + td.get_text().strip()
            elif i == 4:
                # Get the passed information
                new_string += "\t" + td.get_text().strip()
            i -= 1

    # Generate hash from results
    hash_new_string = hashlib.md5(new_string.encode('utf-8'))
    if verbose:
        print("New Hash:", hash_new_string.hexdigest())

    # Save new Hash
    fo = open("cache.txt", "w")
    fo.write(hash_new_string.hexdigest())
    fo.close()

    # Compare Hash and Send Mail
    if hash_old != "":
        if hash_old != hash_new_string.hexdigest():
            print("Something has Changed")
            if send_mail:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
                    server.login(smtp_user, smtp_password)
                    if message_addresults:
                        server.sendmail(sender, receivers, message + new_string)
                    else:
                        server.sendmail(sender, receivers, message)
                    print("\nSuccessfully sent email\n")
        else:
            print("\nNothing is new\n")

    # Sign out
    br.follow_link(text_regex="Abmelden")


if __name__ == '__main__':
    try:
        fetch_results()
    except Exception as e:
        print(e)
