from flask import Flask, request, send_file
from gtts import gTTS
from pydub import AudioSegment
from subprocess import call

app = Flask(__name__)

@app.route("/ttpwm", methods=["POST"])
def ttpwm():
        try:
            app.logger.info(request.get_data())
            words = request.get_data().decode('utf-8')
            app.logger.info(words)
            app.logger.info("Calling Google: "+words)
            tts = gTTS(words, lang='de')
            app.logger.info("Saving MP3")
            tts.save('tmp-in.mp3')
            app.logger.info("Convert to WAV")
            speech = AudioSegment.from_mp3('tmp-in.mp3')
            speech.export('tmp.wav', format='wav')
            app.logger.info("Convert to 8bit PCM")
            call(["sox","tmp.wav","-e","unsigned","-r","22000","-c","1","-b","8","tmp-out.wav"])
            return send_file("tmp-out.wav", mimetype="audio/wav", as_attachment=True, attachment_filename="tmp-out.wav")
        except Exception as e:
            app.logger.info(e)