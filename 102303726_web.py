import os
from flask import Flask, request, render_template
from yt_dlp import YoutubeDL
from pydub import AudioSegment
import subprocess
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import re

\
app = Flask(__name__, template_folder='templates')

SENDER_EMAIL = "aviralbhargava30@gmail.com"
APP_PASSWORD = "password"  

ROLLNO = "102303726"
OUTPUT_MP3 = f"{ROLLNO}-mashup.mp3"
OUTPUT_ZIP = f"{ROLLNO}-mashup.zip"

def valid_email(email):
    return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email) is not None

def create_mashup(singer, N, Y):
    downloaded = []
    audio_files = []
    cut_files = []
    try:
        with YoutubeDL({'quiet': True, 'extract_flat': True, 'skip_download': True}) as ydl:
            info = ydl.extract_info(f'ytsearch{N}:{singer}', download=False)
            urls = [e['url'] for e in info.get('entries', []) if e][:N]
        
        for url in urls:
            try:
                with YoutubeDL({'format': 'best[ext=mp4]', 'outtmpl': '%(id)s.%(ext)s', 'quiet': True}) as ydl:
                    ydl.download([url])
                    fn = ydl.prepare_filename(ydl.extract_info(url, download=False))
                    if os.path.exists(fn): 
                        downloaded.append(fn)
            except: 
                pass
        
        for vid in downloaded:
            try:
                aud = vid.rsplit('.', 1)[0] + '.mp3'
                subprocess.run(['ffmpeg', '-i', vid, '-vn', '-acodec', 'libmp3lame', '-q:a', '2', aud, '-y'],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                audio_files.append(aud)
            except: 
                pass
        
        for aud in audio_files:
            try:
                a = AudioSegment.from_file(aud)[:Y*1000]
                cf = aud.rsplit('.', 1)[0] + '_cut.mp3'
                a.export(cf, format="mp3")
                cut_files.append(cf)
            except: 
                pass
        
        if not cut_files: 
            return False
        
        combined = AudioSegment.from_file(cut_files[0])
        for c in cut_files[1:]:
            combined += AudioSegment.from_file(c)
        combined.export(OUTPUT_MP3, format="mp3")
        
        with zipfile.ZipFile(OUTPUT_ZIP, 'w') as z:
            z.write(OUTPUT_MP3)
        return True
    except:
        return False
    finally:
        for f in os.listdir('.'):
            if f.endswith(('.mp4', '.mp3', '_cut.mp3')) and f not in (OUTPUT_MP3, OUTPUT_ZIP):
                try: 
                    os.remove(f)
                except: 
                    pass

def send_email(to_email, zip_path, singer):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = f"Your {singer} Mashup ZIP"
        
        body = f"Your mashup for {singer} is attached.\nN={request.form.get('N')}, Y={request.form.get('Y')} sec"
        msg.attach(MIMEText(body))
        
        with open(zip_path, "rb") as f:
            part = MIMEBase("application", "zip")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(zip_path)}")
            msg.attach(part)
        
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except:
        return False

@app.route('/')
def home():
    print("Loading template: templates/index.html")
    print("Template exists:", os.path.exists('templates/index.html'))
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    singer = request.form.get('singer','').strip()
    try:
        N = int(request.form.get('N',0))
        Y = int(request.form.get('Y',0))
    except:
        N = Y = 0
    email = request.form.get('email','').strip()
    
    if not singer or N <= 10 or Y <= 20 or not valid_email(email):
        return "<h3>Invalid input (N>10, Y>20, valid email)</h3><a href='/'>Back</a>"
    
    if create_mashup(singer, N, Y) and os.path.exists(OUTPUT_ZIP):
        if send_email(email, OUTPUT_ZIP, singer):
            return f"<h2>Success! ZIP sent to {email}</h2><a href='/'>New Mashup</a>"
        else:
            return "<h3>Mashup created but email failed (check Gmail settings)</h3>"
    return "<h3>Generation failed. Try smaller N/Y.</h3><a href='/'>Back</a>"

if __name__ == "__main__":
    print("Current directory:", os.getcwd())
    print("Templates folder exists:", os.path.exists('templates'))
    if os.path.exists('templates/index.html'):
        print("index.html found!")
    else:
        print("ERROR: index.html NOT found in templates/")
    app.run(host='0.0.0.0', port=5000)
