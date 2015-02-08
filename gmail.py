#!/usr/bin/env python
 
"""MailBox class for processing IMAP email.

(To use with Gmail: enable IMAP access in your Google account settings)

usage with GMail:

    import mailbox

    with mailbox.MailBox(gmail_username, gmail_password) as mbox:
        print mbox.get_count()
        print mbox.print_msgs()


for other IMAP servers, adjust settings as necessary.    
"""

#Source: https://gist.github.com/cgoldberg/4149804
 
 
import imaplib
import time
import uuid
from email import email
import string 
 
 
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = '993'
IMAP_USE_SSL = True
 
 
 
class MailBox(object):
    
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.unread_email = []
        if IMAP_USE_SSL:
            self.imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        else:
            self.imap = imaplib.IMAP4(IMAP_SERVER, IMAP_PORT)
 
    def __enter__(self):
        self.imap.login(self.user, self.password)
        return self
 
    def __exit__(self, type, value, traceback):
        self.imap.close()
        self.imap.logout()
 
    def get_count(self):
        self.imap.select('Inbox')
        status, data = self.imap.search(None, 'ALL')
        return sum(1 for num in data[0].split())
 
    def fetch_message(self, num):
        self.imap.select('Inbox')
        status, data = self.imap.fetch(str(num), '(RFC822)')
        email_msg = email.message_from_string(data[0][1])
        return email_msg
 
    def delete_message(self, num):
        self.imap.select('Inbox')
        self.imap.store(num, '+FLAGS', r'\Deleted')
        self.imap.expunge()
 
    def delete_all(self):
        self.imap.select('Inbox')
        status, data = self.imap.search(None, 'ALL')
        for num in data[0].split():
            self.imap.store(num, '+FLAGS', r'\Deleted')
        self.imap.expunge()
 
    def print_msgs(self):
        self.imap.select('Inbox')
        status, data = self.imap.search(None, 'ALL')
        for num in reversed(data[0].split()):
            status, data = self.imap.fetch(num, '(RFC822)')
            print 'Message %s\n%s\n' % (num, data[0][1])

    def parse_data(self, foo):
        yolo = foo.split()
        flag = False
        doge = ''
        yahtzee = 'Yahtzee'
        #print foo
        for i in yolo:
            if i == 'text_0.txt':
                flag = True
            if len(i) > 1:
                if i[0:2] == '--':
                    flag = False
            if (flag) & (i != 'text_0.txt'):
                doge = doge + (i + ' ')
        if doge == '':
            print "nothing got parsed for some reason, here's the string input"
            print foo
            return yahtzee
        return doge

    def print_unread_msgs(self):
        
        self.imap.select('Inbox')
        status, data = self.imap.search(None, '(UNSEEN)')
        for num in data[0].split():
            status, data = self.imap.fetch(num, '(RFC822)')
            #print 'Message %s\n%s\n' % (num, data[0][1])          
            #print self.parse_data(data[0][1]) 
            self.unread_email.append(self.parse_data(data[0][1]))


    def get_latest_email_sent_to(self, email_address, timeout=300, poll=1):
        start_time = time.time()
        while ((time.time() - start_time) < timeout):
            # It's no use continuing until we've successfully selected
            # the inbox. And if we don't select it on each iteration
            # before searching, we get intermittent failures.
            status, data = self.imap.select('Inbox')
            if status != 'OK':
                time.sleep(poll)
                continue
            status, data = self.imap.search(None, 'TO', email_address)
            data = [d for d in data if d is not None]
            if status == 'OK' and data:
                for num in reversed(data[0].split()):
                    status, data = self.imap.fetch(num, '(RFC822)')
                    email_msg = email.message_from_string(data[0][1])
                    return email_msg
            time.sleep(poll)
        raise AssertionError("No email sent to '%s' found in inbox "
             "after polling for %s seconds." % (email_address, timeout))
 
    def delete_msgs_sent_to(self, email_address):
        self.imap.select('Inbox')
        status, data = self.imap.search(None, 'TO', email_address)
        if status == 'OK':
            for num in reversed(data[0].split()):
                status, data = self.imap.fetch(num, '(RFC822)')
                self.imap.store(num, '+FLAGS', r'\Deleted')
        self.imap.expunge()
 
 
 
if __name__ == '__main__':
    # example:
    imap_username = 'BostonUnderwater@gmail.com'
    imap_password = 'Yahtzee2012'
    with MailBox(imap_username, imap_password) as mbox:
        print "There are " + str(mbox.get_count()) + " unread emails!"
        print mbox.print_unread_msgs()
        print mbox.unread_email