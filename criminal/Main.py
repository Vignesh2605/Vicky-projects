from flask import Flask, render_template, flash, request, session,send_file
from flask import render_template, redirect, url_for, request
#from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from werkzeug.utils import secure_filename
import datetime
import mysql.connector
import sys
import os
import cv2
import face_recognition
app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
known_criminals_folder = "images"
known_encodings = []
known_names = []
flag = 0

def load_known_criminals():
    for file_name in os.listdir(known_criminals_folder):
        image_path = os.path.join(known_criminals_folder, file_name)
        name = os.path.splitext(file_name)[0]
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)[0]
        known_encodings.append(encoding)
        known_names.append(name)

def match_criminal():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"
            flag = 1
            if True in matches:
                matched_indices = [index for index, match in enumerate(matches) if match]
                first_match_index = matched_indices[0]
                name = known_names[first_match_index]
                flag = 0
            top, right, bottom, left = face_locations[0]
            cv2.rectangle(frame, (left, top), (right, bottom), (237, 255, 32), 2)
            if flag == 0:
                cv2.putText(frame, "Matched Criminal: "+name, (left-40, top - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (158, 49, 255), 2)
            else:
                cv2.putText(frame, "Not Matched", (left, top - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 37), 2)
            #match_label.config(text="Matched Criminal: " + name)
        cv2.imshow('TechVidvan', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
@app.route("/")
def homepage():

    return render_template('index.html')

@app.route("/admin")
def admin():

    return render_template('adlog.html')
@app.route("/Police")
def Police():

    return render_template('user.html')
@app.route("/register")
def register():

    return render_template('register.html')
@app.route("/addcriminal")
def addcriminal():

    return render_template('addcriminal.html')

@app.route("/addcriminal1")
def addcriminal1():

    return render_template('addcriminal1.html')

@app.route("/login")
def emp():
    return render_template('login.html')
@app.route("/adminhome")
def adminhome():



    return render_template('adminhome.html')
@app.route("/emphome")
def emphome():
    return render_template('emphome.html')
@app.route("/empregister")
def empregister():
    return render_template('register.html')
@app.route("/viewcriminal")
def viewcriminal():
    conn11 = mysql.connector.connect(user='root', password='', host='localhost', database='criminaldb')
    cursor11 = conn11.cursor()
    cursor11.execute("select * from criminal")
    data1 = cursor11.fetchall()
    return render_template('viewcriminal.html',data=data1)
@app.route("/viewcriminal1")
def viewcriminal1():
    conn11 = mysql.connector.connect(user='root', password='', host='localhost', database='criminaldb')
    cursor11 = conn11.cursor()
    cursor11.execute("select * from criminal")
    data1 = cursor11.fetchall()
    return render_template('viewcriminal1.html',data=data1)
@app.route("/viewstatus")
def viewstatus():
    conn11 = mysql.connector.connect(user='root', password='', host='localhost', database='criminaldb')
    cursor11 = conn11.cursor()
    cursor11.execute("select * from criminalstatus")
    data1 = cursor11.fetchall()
    return render_template('viewstatus.html',data=data1)
@app.route("/viewstatus1")
def viewstatus1():
    conn11 = mysql.connector.connect(user='root', password='', host='localhost', database='criminaldb')
    cursor11 = conn11.cursor()
    cursor11.execute("select * from criminalstatus")
    data1 = cursor11.fetchall()
    return render_template('viewstatus1.html',data=data1)


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
       if request.form['uname'] == 'admin' or request.form['password'] == 'admin':



           return render_template('adminhome.html')

       else:
        return render_template('index.html', error=error)

@app.route("/newregister", methods=['GET', 'POST'])
def newregister():
     if request.method == 'POST':
          name = request.form['name']

          gender = request.form['gender']
          depart = request.form['depart']

          pnumber = request.form['pnumber']
          sname = request.form['sname']
          location = request.form['location']
          details = request.form['details']
          file = request.files['file']
          file.save("static/uploads/" + secure_filename(file.filename))
          uname = request.form['uname']
          password = request.form['password']


          conn = mysql.connector.connect(user='root', password='', host='localhost', database='criminaldb')
          cursor = conn.cursor()
          cursor.execute("insert into police values('','"+name+"','"+gender+"','"+pnumber+"','"+sname+"','"+location+"','"+depart +"','"+details+"','"+file.filename+"','"+uname+"','"+password+"')")
          conn.commit()
          conn.close()


     return render_template('user.html')

@app.route("/newcriminal", methods=['GET', 'POST'])
def newcriminal():
     if request.method == 'POST':
          name = request.form['name']

          age = request.form['age']
          address = request.form['address']
          ctype = request.form['ctype']
          file = request.files['file']
          file.save("static/uploads/" + secure_filename(file.filename))
          file_path="static/uploads/"+file.filename

          image = cv2.imread(file_path)
          rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
          encoding = face_recognition.face_encodings(rgb_image)[0]

          if name:
              known_encodings.append(encoding)
              known_names.append(name)
              file_name = name + ".jpg"
              save_path = os.path.join(known_criminals_folder, file_name)
              cv2.imwrite(save_path, image)
              print("Criminal added successfully.")





          conn = mysql.connector.connect(user='root', password='', host='localhost', database='criminaldb')
          cursor = conn.cursor()
          cursor.execute("insert into criminal values('','"+name+"','"+age+"','"+address+"','"+ctype+"','"+file.filename+"')")
          conn.commit()
          conn.close()
          conn = mysql.connector.connect(user='root', password='', host='localhost', database='criminaldb')
          cursor = conn.cursor()
          cursor.execute("insert into criminalstatus values('','" + name + "','','')")
          conn.commit()
          conn.close()


     return render_template('addcriminal.html')

@app.route("/newcriminal1", methods=['GET', 'POST'])
def newcriminal1():
     if request.method == 'POST':
          name = request.form['name']

          age = request.form['age']
          address = request.form['address']
          ctype = request.form['ctype']
          file = request.files['file']
          file.save("static/uploads/" + secure_filename(file.filename))
          file_path="static/uploads/"+file.filename

          image = cv2.imread(file_path)
          rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
          encoding = face_recognition.face_encodings(rgb_image)[0]

          if name:
              known_encodings.append(encoding)
              known_names.append(name)
              file_name = name + ".jpg"
              save_path = os.path.join(known_criminals_folder, file_name)
              cv2.imwrite(save_path, image)
              print("Criminal added successfully.")





          conn = mysql.connector.connect(user='root', password='', host='localhost', database='criminaldb')
          cursor = conn.cursor()
          cursor.execute("insert into criminal values('','"+name+"','"+age+"','"+address+"','"+ctype+"','"+file.filename+"')")
          conn.commit()
          conn.close()
          conn = mysql.connector.connect(user='root', password='', host='localhost', database='criminaldb')
          cursor = conn.cursor()
          cursor.execute("insert into criminalstatus values('','" + name + "','','')")
          conn.commit()
          conn.close()


     return render_template('addcriminal1.html')
@app.route("/Policelogin", methods=['GET', 'POST'])
def Policelogin():
     if request.method == 'POST':
          uname = request.form['uname']
          session['uname']=uname

          password = request.form['password']



          conn = mysql.connector.connect(user='root', password='', host='localhost', database='criminaldb')
          cursor = conn.cursor()
          cursor.execute("select * from police where uname='"+uname+"' and password='"+password+"'")
          data1 = cursor.fetchone()
          if data1 is None:
              return "Username And Password Wrong"
          else:
              conn = mysql.connector.connect(user='root', password='', host='localhost', database='criminaldb')
              cursor = conn.cursor()
              cursor.execute("select * from police where uname='"+uname+"' and password='"+password+"'")
              data1 = cursor.fetchall()
              return render_template('policehome.html',data=data1)



@app.route("/policehome")
def policehome():
              uname=session['uname']

              conn = mysql.connector.connect(user='root', password='', host='localhost', database='criminaldb')
              cursor = conn.cursor()
              cursor.execute("select * from police where uname='"+uname+"'")
              data1 = cursor.fetchall()
              return render_template('policehome.html',data=data1)

@app.route("/detectcriminal")
def detectcriminal():
              import Face_Identification_system
              return render_template('policehome.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)