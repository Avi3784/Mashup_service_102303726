# Mashup Web Service - Song Mashup Generator

**Roll Number:** 102303726  
**Project:** Web service that creates a mashup from YouTube videos of a given singer and sends the result as a ZIP file via email.

## Features

- User inputs: Singer name, number of videos (N > 10), clip duration (Y seconds > 20), email address
- Searches YouTube for top videos of the singer
- Downloads selected videos
- Extracts audio
- Cuts the first Y seconds of each audio clip
- Merges all clips into a single MP3 file
- Packages the result in a ZIP file
- Sends the ZIP file to the provided email address
- Input validation (N > 10, Y > 20, valid email format)

## Technologies Used

- **Backend:** Python + Flask
- **YouTube downloading:** yt-dlp
- **Audio processing:** pydub + ffmpeg
- **Email sending:** smtplib (Gmail SMTP)
- **Frontend:** Bootstrap + simple HTML form

## Requirements

- Python 3.8+
- FFmpeg installed and added to system PATH
- Gmail account with **App Password** enabled (for sending emails)

### Python Packages



How to Run

Open terminal in the project folder
Install dependencies (if not already done):Bashpip install flask yt-dlp pydub
Update your Gmail credentials in 102303726_web.py
Start the server:Bashpython 102303726_web.py
Open in browser:texthttp://127.0.0.1:5000
Fill the form and submit → wait for processing → check your email for the ZIP file


Important Notes

Processing time depends on N (number of videos) and internet speed
→ Recommended: N = 12–20, Y = 25–30 for testing
YouTube rate limiting may occur with high N → use smaller values if downloads fail
Make sure FFmpeg is correctly installed (test with ffmpeg -version in terminal)
Email may go to Spam/Junk folder — check there if not in Inbox




Submission Files

102303726_web.py
templates/index.html
Screenshots: form page + success message + received email with ZIP




