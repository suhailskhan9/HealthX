
from flask import Flask, render_template, request, redirect,flash
import sqlite3
import smtplib
import os
import bcrypt
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
# import seaborn as sns
import pandas as pd
from datetime import datetime, timedelta, date
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sklearn.naive_bayes import MultinomialNB
import time
from plyer import notification

app = Flask(__name__)
app.secret_key='secretkey'
userId=None
import numpy as np
import pandas as pd
from flask import Flask, render_template , request , redirect , url_for, session
from sklearn.naive_bayes import MultinomialNB
# from db import *
disease_prediction = Flask(__name__)
l1=['itching','skin_rash','nodal_skin_eruptions','continuous_sneezing','shivering','chills','joint_pain',
    'stomach_pain','acidity','ulcers_on_tongue','muscle_wasting','vomiting','burning_micturition','spotting_ urination','fatigue',
    'weight_gain','anxiety','cold_hands_and_feets','mood_swings','weight_loss','restlessness','lethargy','patches_in_throat',
    'irregular_sugar_level','cough','high_fever','sunken_eyes','breathlessness','sweating','dehydration','indigestion',
    'headache','yellowish_skin','dark_urine','nausea','loss_of_appetite','pain_behind_the_eyes','back_pain','constipation',
    'abdominal_pain','diarrhoea','mild_fever','yellow_urine','yellowing_of_eyes','acute_liver_failure','fluid_overload',
    'swelling_of_stomach','swelled_lymph_nodes','malaise','blurred_and_distorted_vision','phlegm','throat_irritation',
    'redness_of_eyes','sinus_pressure','runny_nose','congestion','chest_pain','weakness_in_limbs','fast_heart_rate',
    'pain_during_bowel_movements','pain_in_anal_region','bloody_stool','irritation_in_anus','neck_pain','dizziness','cramps',
    'bruising','obesity','swollen_legs','swollen_blood_vessels','puffy_face_and_eyes','enlarged_thyroid','brittle_nails',
    'swollen_extremeties','excessive_hunger','extra_marital_contacts','drying_and_tingling_lips','slurred_speech','knee_pain','hip_joint_pain',
    'muscle_weakness','stiff_neck','swelling_joints','movement_stiffness','spinning_movements','loss_of_balance','unsteadiness','weakness_of_one_body_side',
    'loss_of_smell','bladder_discomfort','foul_smell_of urine','continuous_feel_of_urine','passage_of_gases','internal_itching','toxic_look_(typhos)',
    'depression','irritability','muscle_pain','altered_sensorium','red_spots_over_body','belly_pain','abnormal_menstruation','dischromic _patches',
    'watering_from_eyes','increased_appetite','polyuria','family_history','mucoid_sputum','rusty_sputum','lack_of_concentration','visual_disturbances',
    'receiving_blood_transfusion','receiving_unsterile_injections','coma','stomach_bleeding','distention_of_abdomen','history_of_alcohol_consumption',
    'fluid_overload','blood_in_sputum','prominent_veins_on_calf','palpitations','painful_walking','pus_filled_pimples','blackheads','scurring','skin_peeling',
    'silver_like_dusting','small_dents_in_nails','inflammatory_nails','blister','red_sore_around_nose','yellow_crust_ooze']
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login/")
def login():
    return render_template("login.html")
email=None
@app.route("/loginCheck/",methods=["POST"])
def loginCheck():
    global email
    email=request.form["email"]
    password=request.form["password"]
    database_connection=sqlite3.connect("medications.db")
    database_cursor=database_connection.cursor()
    # database_cursor.execute("select * from register_user where email=? and password=? ",(email,password))
    database_cursor.execute("select email from register_user where email=?",(email,))
    result=database_cursor.fetchone()
    
    if result:
        global userId
        database_cursor.execute("select password from register_user where email=?",(email,))
        passw=database_cursor.fetchone()[0]
        password=password.encode('utf-8')
        if bcrypt.checkpw(password,passw):
            userId=database_cursor.execute("select id from register_user where email=?",(email,))
            userId=userId.fetchone()[0]
            flash("Login Successful!",category='success')
            return redirect('/home/')
        else:
            flash("Invalid Email or Password!",category='error')
            return redirect('/login/')
        # userId=database_cursor.execute("select id from register_user where email=?",(email,))
        # userId=userId.fetchone()[0]
        # flash("Login Successful!",category='success')
        # return redirect('/home/')
    else:
        flash("User not Registered with us, kindly Register!",category='error')
        return redirect('/register/')
        # database_cursor.execute("select (email) from register_user where email=?",(email,))
        # email=database_cursor.fetchone()
        # database_connection.commit()
        # database_connection.close()
        # if email:
        #  flash("Invalid Email or Password!",category='error')
        #  return redirect('/login/')
        # else:
        #     flash("User not Registered with us, kindly Register!",category='error')
        #     return redirect('/register/')

@app.route("/register/")
def register():
    return render_template("register.html")

@app.route("/registerAdd/",methods=["POST"])
def registerAdd():
     name=request.form["name"]
     email=request.form["email"]
     password=request.form["password"]
     database_connection = sqlite3.connect("medications.db")
     database_cursor = database_connection.cursor()
     database_cursor.execute("select (email) from register_user where email=?",(email,))
     result=database_cursor.fetchone()
     if result:
        flash("Email Already Exist !",category='error')
        return redirect("/register/")
     elif len(password)<6:
        flash("Password must be atleast 6 character long",category='error')
        return redirect("/register/")
     password=password.encode('utf-8')
     password=bcrypt.hashpw(password,bcrypt.gensalt())
     database_cursor.execute("insert into register_user (name,email,password) values (?,?,?)",(name,email,password))
     database_connection.commit()
     database_connection.close()
     flash("Registration Successful!",category='success')
     return redirect('/login/')
userdata=None
@app.route("/home/")
def home():
    global userdata
    database_connection=sqlite3.connect("medications.db")
    database_cursor=database_connection.cursor()
    userdata=database_cursor.execute("select name,email,password from register_user where id=?",(userId,))
    userdata=userdata.fetchall()
    return render_template("home.html",userdata=userdata)

@app.route("/predict/")
def predict():
    return render_template("predictor_1.html",l1=l1)
@app.route("/symget/",methods=["POST"])
def getsym():
    global l1
    disease=['Fungal infection','Allergy','GERD','Chronic cholestasis','Drug Reaction',
        'Peptic ulcer diseae','AIDS','Diabetes','Gastroenteritis','Bronchial Asthma','Hypertension',
        ' Migraine','Cervical spondylosis',
        'Paralysis (brain hemorrhage)','Jaundice','Malaria','Chicken pox','Dengue','Typhoid','hepatitis A',
   'Hepatitis B','Hepatitis C','Hepatitis D','Hepatitis E','Alcoholic hepatitis','Tuberculosis',
   'Common Cold','Pneumonia','Dimorphic hemmorhoids(piles)',
   'Heartattack','Varicoseveins','Hypothyroidism','Hyperthyroidism','Hypoglycemia','Osteoarthristis',
   'Arthritis','(vertigo) Paroymsal  Positional Vertigo','Acne','Urinary tract infection','Psoriasis',
   'Impetigo']
    
    l2=[]
    for x in range(0,len(l1)):
       l2.append(0)

# TESTING DATA
    tr=pd.read_csv("Testing.csv")
    tr.replace({'prognosis':{'Fungal infection':0,'Allergy':1,'GERD':2,'Chronic cholestasis':3,'Drug Reaction':4,
   'Peptic ulcer diseae':5,'AIDS':6,'Diabetes ':7,'Gastroenteritis':8,'Bronchial Asthma':9,'Hypertension ':10,
   'Migraine':11,'Cervical spondylosis':12,
   'Paralysis (brain hemorrhage)':13,'Jaundice':14,'Malaria':15,'Chicken pox':16,'Dengue':17,'Typhoid':18,'hepatitis A':19,
   'Hepatitis B':20,'Hepatitis C':21,'Hepatitis D':22,'Hepatitis E':23,'Alcoholic hepatitis':24,'Tuberculosis':25,
   'Common Cold':26,'Pneumonia':27,'Dimorphic hemmorhoids(piles)':28,'Heart attack':29,'Varicose veins':30,'Hypothyroidism':31,
   'Hyperthyroidism':32,'Hypoglycemia':33,'Osteoarthristis':34,'Arthritis':35,
   '(vertigo) Paroymsal  Positional Vertigo':36,'Acne':37,'Urinary tract infection':38,'Psoriasis':39,
   'Impetigo':40}},inplace=True)

    X_test= tr[l1]
    y_test = tr[["prognosis"]]
    np.ravel(y_test)

    # TRAINING DATA
    df=pd.read_csv("Training.csv")

    df.replace({'prognosis':{'Fungal infection':0,'Allergy':1,'GERD':2,'Chronic cholestasis':3,'Drug Reaction':4,
    'Peptic ulcer diseae':5,'AIDS':6,'Diabetes ':7,'Gastroenteritis':8,'Bronchial Asthma':9,'Hypertension ':10,
    'Migraine':11,'Cervical spondylosis':12,
    'Paralysis (brain hemorrhage)':13,'Jaundice':14,'Malaria':15,'Chicken pox':16,'Dengue':17,'Typhoid':18,'hepatitis A':19,
    'Hepatitis B':20,'Hepatitis C':21,'Hepatitis D':22,'Hepatitis E':23,'Alcoholic hepatitis':24,'Tuberculosis':25,
    'Common Cold':26,'Pneumonia':27,'Dimorphic hemmorhoids(piles)':28,'Heart attack':29,'Varicose veins':30,'Hypothyroidism':31,
    'Hyperthyroidism':32,'Hypoglycemia':33,'Osteoarthristis':34,'Arthritis':35,
    '(vertigo) Paroymsal  Positional Vertigo':36,'Acne':37,'Urinary tract infection':38,'Psoriasis':39,
    'Impetigo':40}},inplace=True)

    X= df[l1]

    y = df[["prognosis"]]
    np.ravel(y)



    s1 =request.form.get("sym1")
    s2=request.form.get("sym2")
    s3=request.form.get("sym3")
    s4=request.form.get("sym4")
    s5=request.form.get("sym5")
    gnb = MultinomialNB()
    gnb=gnb.fit(X,np.ravel(y))
    from sklearn.metrics import accuracy_score
    y_pred = gnb.predict(X_test)
    print(accuracy_score(y_test, y_pred))
    print(accuracy_score(y_test, y_pred, normalize=False))

    psymptoms = [s1,s2,s3,s4,s5]

    for k in range(0,len(l1)):
        for z in psymptoms:
            if(z==l1[k]):
                l2[k]=1

    inputtest = [l2]
    predict = gnb.predict(inputtest)
    predicted=predict[0]
    
    h='no'
    for a in range(0,len(disease)):
        if(disease[predicted] == disease[a]):
            h='yes'
            break
    if (h=='yes'):
        t3=disease[a]
        return redirect(url_for('pre_ans',ans=t3))
    else:
        t3="No Disease"
        return redirect(url_for('pre_ans',ans=t3))
@app.route("/pre_ans/<ans>")
def pre_ans(ans):
    return render_template("predict_ans.html",ans=ans)

@app.route('/visualize')
def visualize():
    return render_template('visualize.html')

@app.route('/dv1h')
def dv1h():
    return render_template('dv.html')

@app.route('/dv2h')
def dv2h():
    return render_template('dv2.html')
@app.route('/dv3h')
def dv3h():
    return render_template('dv3.html')
@app.route('/dv4h')
def dv4h():
    return render_template('dv4.html')
@app.route('/dv5h')
def dv5h():
    return render_template('dv5.html')
@app.route("/dis_rem/")
def dis_rem():
    global email
    database_connection = sqlite3.connect("medications.db")
    database_cursor = database_connection.cursor()
    database_cursor.execute("select dose,start_date,end_date,time from medications where email=?",(email,))
    some_data=database_cursor.fetchall()
    return render_template('dis_rem.html',some_data=some_data)

# @app.route("/rem_d/",methods=['POST'])
# def rem_d():
#     database_connection = sqlite3.connect("medications.db")
#     database_cursor = database_connection.cursor()
#     database_cursor.execute("select dose,start_date,end_date,time where email=?",(email,))
#     some_data=database_cursor.fetchall()
#     return render_template('dis_rem.html')

def send_email(to_email,med_name):
    
    smtp_server = "smtp.gmail.com" 
    smtp_port = 587 
    smtp_username = "healthxnoreply@gmail.com" 
    smtp_password = "nsmtdnziqnvbveqr"
   
    message = MIMEMultipart()
    message['From'] = smtp_username
    message['To'] = to_email
    message['Subject'] = "Medication Reminder"

    message_body = f"Reminder: It's time to take your medicine : [{med_name}]"
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
    dose = request.form['dose']
    # frequency = request.form['frequency']
    start_date = datetime.strptime(str(request.form['start_date']), '%Y-%m-%d')
    end_date = datetime.strptime(str(request.form['end_date']), '%Y-%m-%d')
    time = request.form['time']
    conn = sqlite3.connect('medications.db')
    c = conn.cursor()
    c.execute('INSERT INTO medications (email, dose, start_date, end_date,time) VALUES (?, ?, ?, ?,?)',
              (email, dose, start_date, end_date,time))
    conn.commit()
    conn.close()

    t1 = threading.Thread(target=reminder)
    t1.start()
    flash("Reminder set successfully!",category='success')
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
        conn.commit()
        conn.close()
        for i in meds:
            email=i[1]
            end_date= datetime.strptime(str(i[4]), '%Y-%m-%d %H:%M:%S')
            end_date=end_date.date()
            start_date = datetime.strptime(str(i[3]), '%Y-%m-%d %H:%M:%S')
            start_date=start_date.date()
            time = datetime.strptime(i[5], '%H:%M').time()
            print(date.today(),end_date)
            print(type(date.today()),type(end_date))
            if date.today()>=start_date and date.today()<=end_date:
                now=datetime.now()
                print(now,now.hour,now.minute)
                if now.hour==time.hour and now.minute==time.minute:
                    print("printing email")
                    send_email(email,med_name=i[2])
                    notification.notify(
                        title = "Reminder",
                        message = "It's time to take your medicine ",
                        timeout=20)
                    tomorrow = date.today() + timedelta(1)
                    tomorrow = datetime.combine(tomorrow,datetime.min.time())
                    conn = sqlite3.connect('medications.db')
                    c = conn.cursor()
                    c.execute('update medications set start_date=? where id=?',(tomorrow,i[0],))
                    conn.commit()
                    conn.close()
                    if date.today()==end_date:
                        conn = sqlite3.connect('medications.db')
                        c = conn.cursor()
                        c.execute('delete from medications where id=?',(i[0],))
                        conn.commit()
                        conn.close()


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