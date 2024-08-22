from flask import Flask, render_template, url_for, request, redirect
import csv
<<<<<<< HEAD
import mysql.connector as mysql
=======
import mysql.connector
>>>>>>> master
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


import sys

app = Flask(__name__)

<<<<<<< HEAD
db= mysql.connect(host="localhost", user="root", password="",database="college")
command_handler = db.cursor(buffered=True)
# db= mysql.connect(host="BereketeabAbebe.mysql.pythonanywhere-services.com", user="BereketeabAbebe", password="BekisgoingtoHost",database="BereketeabAbebe$Contacts")
# command_handler = db.cursor(buffered=True)
=======
# db= mysql.connect(host="localhost", user="root", password="",database="college")
# command_handler = db.cursor(buffered=True)
db_config = {
        "host":"BereketeabAbebe.mysql.pythonanywhere-services.com",
        "user":"BereketeabAbebe",
        "password":"",
        "database":"BereketeabAbebe$Contacts"
        }

mysqlConnection = mysql.connector.connect(**db_config)
cursor = mysqlConnection.cursor()
>>>>>>> master

@app.route("/")
def my_home():
    return render_template('index.html')


<<<<<<< HEAD
=======

>>>>>>> master
@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)

<<<<<<< HEAD
def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email=data["email"]
        subject= data["subject"]
        message=data["message"]
        file= database.write(f'\n{email},\n{subject},\n{message}')
=======

def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        file = database.write(f'{email},{subject},{message}')

>>>>>>> master

def write_to_db(data):

    email=data["email"]
    subject= data["subject"]
    message=data["message"]

<<<<<<< HEAD
   
    csv_data=([email,subject,message])
    
    command_handler.execute("INSERT INTO users(email,subject,message) VALUES(%s,%s,%s)", csv_data)

    db.commit()
    command_handler.close()

=======
    insert_stmt = (
            "INSERT INTO users(email,subject,message) VALUES(%s,%s,%s)"
        )


    data=(email,subject,message)



    cursor.execute(insert_stmt, data)

    mysqlConnection.commit()

    # result_val = cursor.excute("SELECT * FROM users")
    # if result_val >0:
    #         userDetails=  cursor.fetchall()
    #         return render_template('show_users.html', userDetails=userDetails)
>>>>>>> master


def write_to_csv(data):
      with open('database.csv', mode='a',  newline='') as database2:
        email=data["email"]
        subject= data["subject"]
        message=data["message"]
        csv_writer= csv.writer(database2, delimiter=',' , quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email,subject,message])

<<<<<<< HEAD
@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method== 'POST':
        try:
            data= request.form.to_dict()
            write_to_csv(data)
            write_to_db(data)
            return redirect('/thankyou.html')
        except:
            return 'did nott save to  data base'
=======


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            write_to_db(data)
            write_to_file(data)
            return redirect('/thankyou.html')
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return 'An error occurred, data was not saved to the database'
>>>>>>> master
    else:
        return "Something went wrong."

