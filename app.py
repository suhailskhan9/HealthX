
from flask import Flask, render_template, request, redirect
import sqlite3
import smtplib
import os
from datetime import datetime, timedelta

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")




def send_email(to_email):
    
    smtp_server = "smtp.gmail.com" 
    smtp_port = 587 
    smtp_username = "suhailskhan99@gmail.com" 
    smtp_password = "uaguyxagndgunwku" 

   
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

@app.route('/add', methods=['POST'])
def add():
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
    return redirect('/')

@app.route('/medications')
def medications():
    conn = sqlite3.connect('medications.db')
    c = conn.cursor()
    c.execute('SELECT * FROM medications')
    meds = c.fetchall()
    conn.close()
    return render_template('medications.html', meds=meds)

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('medications.db')
    c = conn.cursor()
    c.execute('DELETE FROM medications WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/medications')

@app.route('/reminder')
def reminder():
    now = datetime.now()
    print("Now:",now)
    conn = sqlite3.connect('medications.db')
    c = conn.cursor()
    c.execute('SELECT * FROM medications')
    meds = c.fetchall()
    reminders = []
    for med in meds:
        start_date = datetime.strftime(med[4], '%Y-%m-%d %H:%M:%S')
        start_date_strip = start_date.replace('-','')
        start_date_strip = start_date.replace(':','')
        start_date_strip = start_date.replace(' ','')
        end_date = datetime.strftime(med[5], '%Y-%m-%d %H:%M:%S')
        end_date_strip = end_date.replace('-','')
        end_date_strip = end_date.replace(':','')
        end_date_strip = end_date.replace(' ','')
        print(start_date)
        print(type(end_date))
        if start_date <= now <= end_date:
            days_since_start = (now - start_date).days
            if days_since_start % int(start_date_strip) == 0:
                time_due = start_date + timedelta(days=days_since_start, hours=med[3])
                reminder = (med[1], med[2], time_due)
                send_email(email)
                reminders.append(reminder)
    conn.close()
    return render_template('reminder.html', reminders=reminders)



if __name__ == '__main__':
    app.run(debug=True)