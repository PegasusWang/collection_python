# coding:utf-8
import _env
from z42.config import SMTP
from email.MIMEText import MIMEText
from email.Header import Header
from email.Utils import formataddr
import smtplib


def sendmail(to, subject, body, sender=None, html=None, sender_name=None):
    sender_name = sender_name or SMTP.SENDER_NAME
    sender = sender or SMTP.SENDER
    # print to, '#!!!!!!!!!!!!!!!!!!'
    if html:
        text_subtype = 'html'
        msg = MIMEText(html, text_subtype, 'utf-8')
    else:
        text_subtype = 'plain'
        msg = MIMEText(body, text_subtype, 'utf-8')

    # print SMTP

    msg['Subject'] = Header(subject, 'utf-8')
    if sender_name is None:
        sender_name = sender.split('@', 1)[0]
    sender_name = str(Header(sender_name, 'utf-8'))
    msg['From'] = formataddr((sender_name, sender))
    msg['To'] = to
    #msg['Bcc'] = MAIL_ARCHIVE
    smtp = smtplib.SMTP(SMTP.HOST)
    #smtp.set_debuglevel(True)
    print SMTP
    smtp.login(SMTP.USERNAME, SMTP.PASSWORD)
    smtp.sendmail(sender, to, msg.as_string())

if __name__ == '__main__':
    sendmail('archyfilafs@gmail.com', 'aixxz 1234 ts', 'zzzwww xxx')
