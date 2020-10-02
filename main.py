import os
import pandas as pd
from os.path import join, dirname, realpath
from flask import Flask, render_template, request, redirect, url_for




import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="testaction"
)

print(mydb)

mycursor = mydb.cursor()

mycursor.execute("SHOW DATABASES")

# View All Database
for x in mycursor:
  print(x)


app = Flask(__name__)
#
ALLOWED_EXTENSIONS = {'csv'}
app.config["DEBUG"] = True
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

# CVS Column Name
col_names = ['name','car','age']

# Root URL
@app.route('/')
def index():
    return render_template('index.html')

# File Upload Form
@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    # ext = uploaded_file.filename.split('.')[1]
    # and ext == 'csv'
    if uploaded_file.filename != '':
        #uploaded_file.save(uploaded_file.filename)
        #uploaded_file.save(os.path.join(app.config['UPLOADED_FILES']))
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
        readCSV(file_path)
        print('File Name:',uploaded_file)
        #print('File Extension', uploaded_file.filename.split('.')[1])
        #return 'File Uploaded'
    else:
    	print('Wrong file, Please Upload CSV file')
    	p('hello')
    return redirect(url_for('index'))
    
# Read CSV and Insert rows into the database
def readCSV(file_path):
	csvData = pd.read_csv(file_path,names=col_names, header=None)  
	#print(csvData)
	for i,row in csvData.iterrows():
         sql = "INSERT INTO people (name, car, dob) VALUES (%s, %s, %s)"
         value = (row['name'],row['car'], row['age'])
         mycursor.execute(sql, value)
         mydb.commit()
         print('Inserting: ',i,row['name'], row['car'], row['age'])
#        



# Dummy function    
def p(st):
	print('hello csv', st)


app.run()
