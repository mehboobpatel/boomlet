from flask import Flask, render_template, request
from gtts import gTTS
import os
import subprocess

app = Flask(__name__)
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
    
    # Generate audio file using gTTS
    tts = gTTS(welcome_message)
    tts.save(f"static/{full_name}.mp3")
    
    return render_template('success.html', full_name=full_name, purpose=purpose, number=number)


if __name__ == '__main__':
    app.run(debug=True,port=5500)
