from flask import Flask, render_template, request, send_file, Response
import pyodbc
from gtts import gTTS
import os
import subprocess

app = Flask(__name__)

# Connect to Azure SQL DB
server = 'boomlet.database.windows.net'
database = 'boomlet'
username = 'maddy'
password = 'Paneer@1234'
driver = '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return submit()
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    full_name = request.form.get('full_name')
    purpose = request.form.get('purpose')
    number = request.form.get('number')
    welcome_message = f"Welcome {full_name} to BoomLet Media"

    # Insert user details into boomlet table
    cursor = cnxn.cursor()
    insert_query = f"INSERT INTO users (full_name, purpose, number) VALUES ('{full_name}', '{purpose}', '{number}')"
    cursor.execute(insert_query)
    cnxn.commit()

    # Generate audio file using gTTS
    tts = gTTS(welcome_message)
    audio_file = f"static/{full_name}.mp3"
    tts.save(audio_file)

    def generate():
        with open(audio_file, 'rb') as f:
            data = f.read(1024)
            while data:
                yield data
                data = f.read(1024)

    # Return audio file and play it automatically on iOS Safari browser
    headers = {
        'Content-Disposition': f'inline; filename="{full_name}.mp3"',
        'Cache-Control': 'no-cache',
        'X-Accel-Redirect': f'/audio/{full_name}.mp3'
    }
    return Response(generate(), headers=headers, mimetype='audio/mp3')

@app.route('/database', methods=['GET'])
def database():
    # Select all records from boomlet table
    cursor = cnxn.cursor()
    select_query = "SELECT * FROM users"
    cursor.execute(select_query)
    rows = cursor.fetchall()

    return render_template('database.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True, port=5500)
