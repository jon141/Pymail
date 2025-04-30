
Python Emailverteiler ("Pymail") Dokumentation

wenn du in deinen Nachrichten den Namen und deine Unterschrift automatisch einfügen lassen wilst:
    - {name} -> Name des Empfängers aus der birthday.json Datei
    - {signature} -> Deine Signatur aus der config.json Datei
    - {age} -> das Alter aus dem vollständigen Geburtsdatum berechnet
- da einfügen, wo Name und Unterschrift stehen würden

Dateien, die als Text deiner Mail eingefügt werden können .txt und .html Dateien sein
Der Betreff muss in einer .txt Datei gespeichert werden

Dateien, die nicht entfernt werden dürfen:
    - standartmessage.html
    - standardsubject.txt
- dienen als Absicherung, wenn deine eigentlich angegebene Datei nicht existiert, falsch benannt ist, oder nicht geladen werden kann
    - config.json
    - birthdays.json

damit es funktioniert, muss dein Email Anbieter smtp-Server benutzen
    - gmx funktioniert, web sollte auch gehen (gleicher Anbieter)
    - gmail wahrscheinlich auch
aber ich kann nur Aussagen zu gmx treffen

die config.json Datei
{
    "fromMail": "deine Eimail adresse",         (deine normale Emailadresse)
    "password": "Dein mail password",           (Passwort zu deinem Email Account)
    "smtp_server": "EmailServer",               (zum Beispiel: mail.gmx.net)
    "smtp_port": 587,                           (kann auch 465 sein)
    "signature": "Deine Unterschrift",          (zum Beispiel dein Name)
    "bcc": true                                 (Blindkopie ja, oder nein (true, false))
}

die birthdays.json Datei
{

"Jonas": {                                  (in der Datei einmaliger Name / Kürzel)
    "name": "Jonas",                        (Name der Person (Anrede))
    "date": "02.08.2007",                   (Geburtsdatum Tag.Monat.Jahr Wenn Jahr nicht bekannt einfach 0000 -> dann kein {age} verwenden, Nullen mitschreiben, also nicht 2.8.07, sondern 02.08.2007)
    "message": "standardmessage.html",      (Datei, die deinen Nachrichtentext enthält, Name mit Endung, wenn in seperatem Ordner, vollständigen Dateipfad verwenden)
    "mail": "jkappelix@gmail.com",          (Adresse des Empfängers)
    "subject": "standardsubject.txt"        (Betreff Datei mit Endnung)
}

}

die sent_log.txt Datei
- hier werden Informationen zu den Nachrichten gespeichert, wenn sie verschickt wurden
- und Fehlermeldungen gespeichert, wenn es zu Problemen kommt
- überorüft, ob die Geburtstagsnachricht an die Person heute schon einmal geschickt wurde, dann wird sie NICHT erneut gesendet
- wird neu erstellt, wenn sie entfernt wurde
- kann ab und zu entfernt, oder der Inhalt gelöscht werden, damit die Ausführgeschwindigkeit nicht nachlässt

Antworten auf Nachrichten werden an deine angegebene from_Mail Adresse geschickt
