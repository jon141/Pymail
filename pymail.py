import smtplib
#from email.mime.text import MIMEText
from email.message import EmailMessage
import json
from datetime import datetime


import time
import socket

def wait_for_internet(host="8.8.8.8", port=53, timeout=3): # wenn das Skript mit crontab automatisch beim boot gestartet werden soll, ist erstmal bzw. bis zum Anmelden keine Verbindung vorhande
    while True:
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            print("Internetverbindung verfügbar!")
            break
        except socket.error:
            print("Keine Internetverbindung. Neuer Versuch in 5 Sekunden...")
            time.sleep(5)

wait_for_internet()

# Danach läuft E-Mail-Script weiter...


def append_sent_log(message):
    with open("sent_log.txt", 'a', encoding='utf-8') as log:
        log.write(message + '\n')

try:
    
    with open('birthdays.json', 'r', encoding='utf-8') as file:
        birthday_json = json.load(file)  # JSON in ein Python-Objekt umwandeln

    print(birthday_json)

    birthday_today_persons = []
    date_today = datetime.today().strftime("%d.%m")

    for item in birthday_json:
        date = birthday_json[item]['date']
        day_month = ".".join(date.split(".")[:2])

        if day_month == date_today:
            birthday_today_persons.append(item)


    full_date_today = datetime.today().strftime("%d.%m.%y") # das gesammte datum, mit Jahr


    print(birthday_today_persons)
    if birthday_today_persons != []:

        with open('config.json', 'r', encoding='utf-8') as file:
            config_json = json.load(file)  # JSON in ein Python-Objekt umwandeln

        from_email = config_json["fromMail"]
        password = config_json["password"]
        smtp_server = config_json["smtp_server"]
        smtp_port = config_json["smtp_port"]
        signature = config_json["signature"]
        bcc = config_json["bcc"]

        # log laden, um dopplungen zu vermeiden
        try:
            with open('sent_log.txt', 'r', encoding='utf-8') as file:
                sent_log_file = file.read()
            log_entries = sent_log_file.split('\n')
            relevant_log_part_list = []
            for entry in log_entries:
                relevant_log_part_list.append(entry.split('|')[0])
        except FileNotFoundError: # wenn datei noch nicht existiert
            with open('sent_log.txt', 'w', encoding='utf-8') as file:
                pass  
            relevant_log_part_list = []



        for item in birthday_today_persons:

            try:
                name = birthday_json[item]["name"]
                to_email = birthday_json[item]['mail']
                subject_file = birthday_json[item]['subject']
                message_file = birthday_json[item]['message']
                try:
                    print(full_date_today, 'fulldatetoday')
                    birthyear = birthday_json[item]['date'].split('.')[-1]
                    year = f"20{((str(full_date_today)).split('.'))[-1]}"
                    print(year, 'year')
                    print(birthyear, 'birthyear')
                    age = int(year) - int(birthyear)
                    print(age, 'age')
                except:
                    age = '(error when calculating age)'


                try:
                    with open(subject_file, 'r', encoding='utf-8') as file:
                        subject = file.read()

                    with open(message_file, 'r', encoding='utf-8') as file:
                        message = file.read() 
                except Exception as e:
                    print(e)
                    with open('standardsubject.txt', 'r', encoding='utf-8') as file:
                        subject = file.read()

                    with open('standardmessage.html', 'r', encoding='utf-8') as file:
                        message = file.read() 


                message = message.format(name=name, signature=signature, age=age)
                subject = subject.format(name=name, signature=signature, age=age)



                if f'sent to {item} ({to_email}) at {full_date_today} ' in relevant_log_part_list: # wenn diese Mail heute schon einmal geschickt wurde
                    time_now = datetime.now().strftime("%H:%M:%S") # aktuelle Uhrzeit

                    log_message = f'email was already sent today | -> sent to {item} ({to_email}) at {full_date_today} | {time_now}'
                    append_sent_log(log_message)
                    continue


                msg = EmailMessage() 

                msg['Subject'] = subject
                msg['From'] = from_email
                msg['To'] = to_email
                msg.set_content(message, subtype='html')

                if bcc == True:
                    recipients = [msg['To'], from_email] 
                else:
                    recipients = [msg['To']]
                
                try:

                    time_now = datetime.now().strftime("%H:%M:%S") # aktuelle Uhrzeit

                    if smtp_port == 465:  # SSL für Port 465
                        with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp:
                            smtp.login(from_email, password)
                            smtp.send_message(msg, to_addrs=recipients)
                            print(f"E-Mail erfolgreich gesendet an {item}: {name}.")

                            log_message = f'sent to {item} ({to_email}) at {full_date_today} | {time_now}, Port: {smtp_port}, bcc: {bcc}, subject: {subject_file}, message: {message_file}, address_name: {name}' # an Item gesendet, am heutigen Datum, zur aktuellen Uhrzeit

                    elif smtp_port == 587:  # STARTTLS für Port 587
                        with smtplib.SMTP(smtp_server, smtp_port) as smtp:
                            smtp.starttls()  # Verschlüsselung
                            smtp.login(from_email, password)
                            smtp.send_message(msg, to_addrs=recipients)
                            print(f"E-Mail erfolgreich gesendet an {item}: {name}.")

                            log_message = f'sent to {item} ({to_email}) at {full_date_today} | {time_now}, Port: {smtp_port}, bcc: {bcc}, subject: {subject_file}, message: {message_file}, address_name: {name}' # an Item gesendet, am heutigen Datum, zur aktuellen Uhrzeit


                    else:
                        print(f"Unbekannter Port: {smtp_port}. Keine Verbindung hergestellt.")
                        log_message = f'error when sending to {item} ({to_email}) at {full_date_today} | {time_now}| unknown port: {smtp_port}, no connection established'
                
                    append_sent_log(log_message)

                except Exception as e:
                    print(f'Fehler: {e}')
                    log_message = f'error when sending to {item} ({to_email}) at {full_date_today} | {time_now}| error: {e} | Port: {smtp_port}, bcc: {bcc}, subject: {subject_file}, message: {message_file}, address_name: {name}'
                    append_sent_log(log_message)
            except Exception as e:
                print(f'Fehler beim Laden und verschicken der Daten von {item}')
                print(e)
except Exception as e:
    print('Fehler im gesammtskript')

# fehlt dann noch: in sent_log hinzufügen; fail_log bei errors


