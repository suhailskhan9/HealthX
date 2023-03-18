
from flask import Flask, render_template, request, redirect
import sqlite3
import smtplib
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, date
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sklearn.naive_bayes import MultinomialNB
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

def send_email(to_email):
    
    smtp_server = "smtp.gmail.com" 
    smtp_port = 587 
    smtp_username = "healthxnoreply@gmail.com" 
    smtp_password = "nsmtdnziqnvbveqr"
   
    message = MIMEMultipart()
    message['From'] = smtp_username
    message['To'] = to_email
    message['Subject'] = "Medication Reminder"

   
    message_body = f"Reminder: It's time to take your medicine)."
    # message_body = f"Reminder: It's time to take {med_name} ({med_dose})."

    message.attach(MIMEText(message_body, 'plain'))

    
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, to_email, message.as_string())
        print(smtp_username,smtp_password)


email = None

@app.route("/add/", methods=['POST'])
def add():
    print("In add")
    global email
    email = request.form['email']
    dose = request.form['dose']
    frequency = request.form['frequency']
    start_date = datetime.strptime(str(request.form['start_date']), '%Y-%m-%d')
    end_date = datetime.strptime(str(request.form['end_date']), '%Y-%m-%d')
    time = request.form['time']
    conn = sqlite3.connect('medications.db')
    c = conn.cursor()
    c.execute('INSERT INTO medications (email, dose, frequency, start_date, end_date,time) VALUES (?, ?, ?, ?, ?,?)',
              (email, dose, frequency, start_date, end_date,time))
    conn.commit()
    conn.close()
    t1 = threading.Thread(target=reminder)
    t1.start()
    return redirect("/medications/")

@app.route("/medications/")
def medications():
    print("hello world")
    return render_template("medications.html")

def reminder():
    while(True):
        conn = sqlite3.connect('medications.db')
        c = conn.cursor()
        c.execute('SELECT * FROM medications')
        meds = c.fetchall()
        
        for i in meds:
            email=i[1]
            end_date= datetime.strptime(str(i[4]), '%Y-%m-%d %H:%M:%S')
            end_date=end_date.date()
            start_date = datetime.strptime(str(i[5]), '%Y-%m-%d %H:%M:%S')
            start_date=start_date.date()
            time = datetime.strptime(i[6], '%H:%M').time()
            print(date.today(),end_date)
            print(type(date.today()),type(end_date))
            if date.today()==end_date:
                now=datetime.now()
                print(now,now.hour,now.minute)
                if now.hour==time.hour and now.minute==time.minute:
                    c.execute('delete from medications where id=?',(i[0],))
                    conn.commit()
                    conn.close()
                    print("printing email")
                    send_email(email)
                    break


# def reminder():
#     now = datetime.now()
#     print("Now:",now)
#     conn = sqlite3.connect('medications.db')
#     c = conn.cursor()
#     c.execute('SELECT * FROM medications')
#     meds = c.fetchall()
#     reminders = []
#     for med in meds:
#         start_date = datetime.strptime(str(med[4]), '%Y-%m-%d %H:%M:%S')
#         end_date = datetime.strptime(str(med[5]), '%Y-%m-%d %H:%M:%S')
#         print(start_date)
#         print(type(start_date))
#         # print(type(end_date_strip))
#         if start_date <= now <= end_date:
#             days_since_start = (now - start_date).days
#             start_date_strip = str(datetime.strptime(str(med[4]), '%Y-%m-%d %H:%M:%S'))
#             print(start_date)
            
#             start_date_strip = start_date_strip.replace('-','')
#             start_date_strip = start_date_strip.replace(' ','')
#             start_date_strip = start_date_strip.replace(':','')
#             print(start_date_strip)
            
#             if days_since_start % int(start_date_strip) == 0:
#                 time_due = start_date + timedelta(days=days_since_start, hours=med[3])
#                 reminder = (med[1], med[2], time_due)
#                 send_email(email)
#                 reminders.append(reminder)
#     conn.close()
#     return render_template('reminder.html', reminders=reminders)



if __name__ == '__main__':
    app.run(debug=True)