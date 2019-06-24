# coding: utf-8
from email import message_from_bytes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid
from imaplib import IMAP4, IMAP4_SSL, IMAP4_PORT, IMAP4_SSL_PORT
from smtplib import SMTP, SMTP_SSL, SMTP_PORT, SMTP_SSL_PORT
from subprocess import call
from textwrap import dedent
from time import sleep

import datetime

import gender_guesser.detector as gender
from nameparser import HumanName

import os 

#__author__ = 'Bertrand Bordage'
#__copyright__ = 'Copyright © 2016 Bertrand Bordage'
#__license__ = 'MIT'


class AutoReplyer:
    refresh_delay = 5  # seconds

    imap_server = None
    imap_use_ssl = False
    imap_port = IMAP4_PORT
    imap_ssl_port = IMAP4_SSL_PORT
    imap_user = None
    imap_password = None

    smtp_server = None
    smtp_use_ssl = False
    smtp_port = SMTP_PORT
    smtp_ssl_port = SMTP_SSL_PORT
    smtp_user = None
    smtp_password = None

    from_address = None
    body = None
    body_html = None
    a = ""
    
    def __init__(self):
        self.imap = IMAP4_SSL(self.imap_server, self.imap_ssl_port)
        self.imap.login("username@gmail.com", "passphrases")
        self.smtp = SMTP_SSL(self.smtp_server, self.smtp_ssl_port)
        self.smtp.login("username@gmail.com", "passphrases")

    def close(self):
        self.smtp.close()
        self.imap.logout()
        
    def create_auto_reply(self,original):
        mail = MIMEMultipart('alternative')
        mail['Message-ID'] = make_msgid()
        mail['References'] = mail['In-Reply-To'] = original['Message-ID']
        mail['Subject'] = 'Re: ' + str(original['Subject'])
        mail['From'] = self.from_address
        mail['To'] = original['Reply-To'] or original['From']
       
        #print (str(original))
       
        with open('cv.txt', 'a') as the_file:
            the_file.write(str(original))
            
        #extract only name from the From of the email body
        fromName = self.from_address
        fullName = ' '.join([item for item in fromName.split() if '@' not in item])

        print (fullName)
        
        # name splitting 
        name = HumanName(fullName)      
        salutation = name.last + "," + name.middle + " " + name.suffix + " " +  name.nickname + "," + name.title + " " + name.first+ ":\n"   
        
        # gender detection 
        d = gender.Detector()
        typeGender = d.get_gender(name.first)
        
        if typeGender == "male" or typeGender == "mostly_male":
            starts="Mr. "
        elif typeGender == "female" or typeGender == "mostly_female":
            starts="Miss. "
        else: 
            starts="Dear/Honorable "
            
        coreBody = starts + " " + salutation + self.body_html
    
        #categorize body of emails 
        ########################
        # write body to cv.txt
                
        os.system('python3 categorize.py')

        #with open('coreCategory.txt', 'r') as file:
            #allCategory = file.read().replace('\n', '')

        allCategory = ""
        with open('coreCategory.txt') as f:
            for line in f.readlines():
                allCategory += line + "/"

        print (allCategory)
        
        alphaBody = coreBody + "\n" + "#EmailClassifies as:/" + (allCategory) 
        
        clearCommand1 = 'rm -rf cv.txt coreCategory.txt'
        os.system(clearCommand1)

        #mail.attach(MIMEText(dedent(self.body), 'plain'))
        mail.attach(MIMEText(alphaBody, 'html'))
        return mail

    def send_auto_reply(self, original):
        self.smtp.sendmail(
            self.from_address, [original['From']],
            self.create_auto_reply(original).as_bytes())
        log = 'Replied to “%s” for the mail “%s”' % (original['From'],
                                                     original['Subject'])
        print(log)
        try:
            call(['notify-send', log])
        except FileNotFoundError:
            pass

    def reply(self, mail_number):
        self.imap.select(readonly=True)
        _, data = self.imap.fetch(mail_number, '(RFC822)')
        
        
        self.imap.close()
        self.send_auto_reply(message_from_bytes(data[0][1]))
    
        self.imap.select(readonly=False)
        self.imap.store(mail_number, '+FLAGS', '\\Answered')
        self.imap.close()

    def check_mails(self):
        self.imap.select(readonly=False)
        date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")
        _, data = self.imap.search(None, '(UNSEEN UNANSWERED)','(SENTSINCE {0})'.format(date))
        self.imap.close()
        for mail_number in data[0].split():
            self.reply(mail_number)
        
    def run(self):
        try:
            while True:
                self.check_mails()
                sleep(self.refresh_delay)
        finally:
            self.close()
