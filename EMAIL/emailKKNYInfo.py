import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
from SECRETS import secrets

def email_kkny_account(suggestion):
    """
    This method will send a message to the GoDadddy kkny info email account with the info 
    entered by the user into the suggestions box. The sender and receiver is both the same
    email account
    """
    print(suggestion)
    mail = smtplib.SMTP_SSL(secrets.SMTP_SERVER, 465)
    mail.login(secrets.EMAIL, secrets.PASSWORD)
    msg = MIMEMultipart('alternative')
    msg['From'] = formataddr((str(Header(u'KKNY Suggestion Box', 'utf-8')), secrets.EMAIL))
    msg['To'] = secrets.EMAIL
    emailContent = "This suggestion was sent from {} \n. His/Her email is {}. His/Her suggestion is {}"
    emailContent = emailContent.format(suggestion["name"], suggestion["email"], suggestion["content"])
    msg.attach(MIMEText(emailContent, 'html'))
    mail.sendmail(secrets.EMAIL, secrets.EMAIL, msg.as_string())
    mail.close()
