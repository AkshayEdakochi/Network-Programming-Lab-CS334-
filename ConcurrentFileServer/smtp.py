import smtplib 
import getpass

# creates SMTP session 
s = smtplib.SMTP('smtp.gmail.com', 587) 
  
# start TLS for security 
s.starttls() 
sender_email = input("Enter sender's address:")

#Use app specific password if two factor authentication is enabled
pswd = getpass.getpass('Password:')
s.login(sender_email, pswd) 

sendTo = input("Who do you want to send the email?: ")
message = 'Subject: {}\n\n{}'.format(input("Enter subject:"), input("Compose Message:"))

try:
    s.sendmail(sender_email, sendTo, message) 
    print("Sending email...")
except:
    print("An error occured")

s.quit() 