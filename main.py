from flask import Flask, render_template, request, url_for, send_from_directory
import os
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)

if not os.path.isfile('food_avail.db'):
  db = sqlite3.connect('food_avail.db')
  db.execute('''CREATE TABLE food_avail
  (name TEXT,
  food TEXT,
  contact TEXT, 
  address TEXT,
  validity TEXT)''')
  db.commit()
  db.close()

if not os.path.isfile('needy_avail.db'):
  db = sqlite3.connect('needy_avail.db')
  db.execute('''CREATE TABLE needy_avail
  (name1 TEXT,
  mouths TEXT,
  contact1 TEXT, 
  address1 TEXT)''')
  db.commit()
  db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signupFood.html', methods=['GET', 'POST'])
def signupFood():
  if request.method == 'POST' and \
  request.files and 'validity' in request.files:
    name = request.form['name']
    food = request.form['food']
    contact = request.form['contact']
    address = request.form['address']
    validity = request.files['validity']
    filename = secure_filename(validity.filename)  # Get the original filename
    path = os.path.join('uploads', filename)
    validity.save(path)

    db = sqlite3.connect('food_avail.db')
    db.execute('''
        INSERT INTO food_avail (name, food, contact, address, validity)
        VALUES (?, ?, ?, ?, ?)''', (name, food, contact, address, filename, ))
    db.commit()
    db.close()
  return render_template('signupFood.html')

@app.route('/signupNeedy.html', methods=['GET', 'POST'])
def signupNeedy():
  if request.method == 'POST':
    name1 = request.form['name1']
    mouths = request.form['mouths']
    contact1 = request.form['contact1']
    address1 = request.form['address1']

    db = sqlite3.connect('needy_avail.db')
    db.execute('''
        INSERT INTO needy_avail (name1, mouths, contact1, address1)
        VALUES (?, ?, ?, ?)''', (name1, mouths, contact1, address1,))
    db.commit()
    db.close()
  return render_template('signupNeedy.html')

@app.route('/viewFood.html')
def viewFood():
  db = sqlite3.connect('food_avail.db')
  cursor = db.cursor()
  cursor.execute('SELECT name, food, contact, address, validity FROM food_avail')
  foods = cursor.fetchall()
  db.close()
  return render_template('viewFood.html', foods=foods)

@app.route('/viewNeedy.html')
def viewNeedy():
  db = sqlite3.connect('needy_avail.db')
  cursor = db.cursor()
  cursor.execute('SELECT name1, mouths, contact1, address1 FROM needy_avail')
  needys = cursor.fetchall()
  db.close()
  return render_template('viewNeedy.html', needys=needys)

@app.route('/validity/<filename>')
def get_file(filename):
    return send_from_directory('uploads', filename)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
