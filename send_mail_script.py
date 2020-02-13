from email.mime.text import MIMEText
import smtplib

def send_mail(email,height,avg_height,count):
    from_email="shiprasha*****@gmail.com"
    from_pass="*********"
    to_mail=email
    subject="Height Data"
    message="Hey there your height is <strong> %s </strong>.<br> Average height is<strong> %s </strong> out of <strong> %s </strong> people.<br> Thanks! " % (height,avg_height,count)
    msg=MIMEText(message,'html')
    msg['Subject']=subject
    msg['From']=from_email
    msg['To']=to_mail

    gmail=smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email,from_pass)
    gmail.send_message(msg)
