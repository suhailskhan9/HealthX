
from flask import Flask, render_template, request, redirect
import sqlite3
import smtplib
from datetime import datetime, timedelta

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')




def send_email(to_email):
    # Set up SMTP server
    smtp_server = "smtp.sendgrid.net" # Replace with your email provider's SMTP server
    smtp_port = 587 # Replace with your email provider's SMTP port
    smtp_username = "apikey" # Replace with your email address
    smtp_password = "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" # Replace with your email password

    # Create message object
    message = MIMEMultipart()
    message['From'] = smtp_username
    message['To'] = to_email
    message['Subject'] = "Medication Reminder"

    # Construct message body
    message_body = f"Reminder: It's time to take your medicine)."
    # message_body = f"Reminder: It's time to take {med_name} ({med_dose})."

    # Attach message body as plain text
    message.attach(MIMEText(message_body, 'plain'))

    # Send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, to_email, message.as_string())




@app.route('/add', methods=['POST'])
def add():
    email = request.form['email']
    dose = request.form['dose']
    frequency = request.form['frequency']
    start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
    time = request.form['time']
    conn = sqlite3.connect('medications.db')
    c = conn.cursor()
    c.execute('INSERT INTO medications (email, dose, frequency, start_date, end_date) VALUES (?, ?, ?, ?, ?)',
              (email, dose, frequency, start_date, end_date))
    conn.commit()
    conn.close()
    send_email(email)
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
    conn = sqlite3.connect('medications.db')
    c = conn.cursor()
    c.execute('SELECT * FROM medications')
    meds = c.fetchall()
    reminders = []
    for med in meds:
        start_date = datetime.strptime(str(med[4]), '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(str(med[5]), '%Y-%m-%d %H:%M:%S')
        if start_date <= now <= end_date:
            days_since_start = (now - start_date).days
            if days_since_start % med[3] == 0:
                time_due = start_date + timedelta(days=days_since_start, hours=med[2])
                reminder = (med[0], med[1], time_due)
                reminders.append(reminder)
    conn.close()
    return render_template('reminder.html', reminders=reminders)
















# @app.route('/submit', methods=['POST'])
# def submit():
#     # Get form data
#     name = request.form['name']
#     email = request.form['email']
#     med_name = request.form['med_name']
#     med_dose = request.form['med_dose']


#     # Save data to database
#     db.add_medication(name, email, med_name, med_dose, time)

#     # Send email reminder
#     send_email(email, med_name, med_dose)

#     # Redirect to success page
#     return render_template('success.html', message='Medication reminder set successfully!')



if __name__ == '__main__':
    app.run(debug=True)