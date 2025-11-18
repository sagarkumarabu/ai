from flask import Flask, render_template, request, send_file
import pyttsx3
import os

app = Flask(__name__)

# Create audio folder if not exists
AUDIO_FOLDER = "audio"
os.makedirs(AUDIO_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    audio_file = None
    if request.method == 'POST':
        text = request.form.get('text')
        if text:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 1.0)

            audio_file = os.path.join(AUDIO_FOLDER, "output.mp3")

            engine.save_to_file(text, audio_file)
            engine.runAndWait()

    return render_template('index.html', audio_file=audio_file)

@app.route('/download/<path:filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5555)
