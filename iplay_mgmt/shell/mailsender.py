#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import smtplib
import sys
import time
import datetime
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
import os.path

class Mailsender:

    def __init__(self):
        print 'I am sending the mails...'

    def setSmtpServer(self, smtpserver):
        self.smtpserver = smtpserver
        print 'Smtpserver is ' + smtpserver

    def setSender(self, sender, password):
        self.sender = sender
        self.password = password
        print 'Sender is ' + sender

    def setReceiver(self, receiver):
        self.receiver = receiver
        print 'Receiver is ' + str(receiver)

    def setContent(self, content):
        self.content = content
        print 'Content is ' + str(content)

    def sendMail(self, line):
        print 'go'
        smtp = smtplib.SMTP()
        smtp.set_debuglevel(1)
        smtp.connect(self.smtpserver, 25)
        smtp.login(self.sender, self.password)

        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = '%s失效游戏和专题' % str(datetime.datetime.now().strftime('%Y-%m-%d'))
        msgRoot['From'] = self.sender
#        msgRoot['Date'] = email.Utils.formatdate()
        receiver = self.receiver
        for i in range(len(receiver)):
            to_list = receiver[i]
            msgRoot['To'] =  to_list
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

#__________p___________________________________邮件附件                                      
        '''
        contype = 'application/octet-stream'
        maintype,subtype = contype.split('/',1)
        data = open(                 'da.csv','rb')
        file_msg = MIMEBase(maintype,subtype)
        file_msg.set_payload(data.read())
        data.close()
#email.Encoders.encode_base64(file_msg)
        basename = os.path.basename('/data/analysis/txt/data..csv')
        file_msg.add_header('Content-Disposition','attachment',filename=basename)
        msgRoot.attach(file_msg)
#_____________________________________________
        '''

        msgText = MIMEText(line,'html','utf-8')
        msgAlternative.attach(msgText)
        
        smtp.sendmail(self.sender, self.receiver, msgRoot.as_string())
        smtp.quit()

    def __del__(self):
        print 'Finish sending mails!'

