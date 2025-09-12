from flask import Flask, render_template, request, Response
from ultralytics import YOLO
from PIL import Image
import os
import uuid
import cv2
import base64
import requests
from spotifysearch.client import Client   # ✅ NEW
import random

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

model = YOLO('model/face_emotion_recognition.pt')
camera = None

last_emotion = None
recommended_tracks = []

# 🔑 Spotify API credentials
CLIENT_ID = "022d472f888646949394d7c7ea3f67f4"
CLIENT_SECRET = "c26e03b2cbc24bfe99bd32efa31bed89"

# ---------------- Emotions → Genres mapping ---------------- #
emotion_to_music = {
    "Happy": {"seed_genres": ["pop", "dance"], "target_valence": 0.9, "target_energy": 0.8},
    "Sad": {"seed_genres": ["acoustic", "chill"], "target_valence": 0.2, "target_energy": 0.3},
    "Angry": {"seed_genres": ["rock", "metal"], "target_valence": 0.3, "target_energy": 0.9},
    "Neutral": {"seed_genres": ["indie", "alternative"], "target_valence": 0.5, "target_energy": 0.5},
    "Surprised": {"seed_genres": ["electronic", "edm"], "target_valence": 0.7, "target_energy": 0.7}
}

# ---------------- Spotify helper functions ---------------- #
def get_spotify_recommendations(emotion, limit=5):
    if emotion not in emotion_to_music:
        return []

    params = emotion_to_music[emotion]
    query = " ".join(params["seed_genres"]) + f" {emotion}"

    client = Client(CLIENT_ID, CLIENT_SECRET)
    results = client.search(query)
    tracks = results.get_tracks()

    # 🚀 Shuffle tracks before slicing
    random.shuffle(tracks)

    return [
        {
            "name": t.name,
            "artist": t.artists[0].name if t.artists else "",
            "url": t.url,
            "embed_url": f"https://open.spotify.com/embed/track/{t.id}"
        }
        for t in tracks[:limit]
    ]

# ------------------ ROUTES ------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    global recommended_tracks, last_emotion

    emotion = None
    uploaded_path = None
    show_text = False

    if request.method == 'POST':
        file = request.files.get('image')
        if file:
            filename = f'{uuid.uuid4()}.jpg'
            uploaded_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(uploaded_path)

            results = model(uploaded_path)
            if results and results[0].boxes and len(results[0].boxes.cls) > 0:
                pred_idx = int(results[0].boxes.cls[0])
                emotion = model.names[pred_idx]

                # Fetch Spotify songs when emotion detected
                recommended_tracks = get_spotify_recommendations(emotion)
                last_emotion = emotion

    return render_template('index.html',
                           emotion=emotion,
                           uploaded_path=uploaded_path,
                           show_text=show_text,
                           tracks=recommended_tracks)

def gen_frames():
    global camera, last_emotion, recommended_tracks
    if camera is None:
        camera = cv2.VideoCapture(0)

    label_map = {
        "surprise": "surprise",
        "happy": "happy",
        "sad": "sad",
        "angry": "angry",
        "neutral": "neutral"
    }

    while True:
        success, frame = camera.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        results = model(frame)

        if results and results[0].boxes and len(results[0].boxes.cls) > 0:
            pred_idx = int(results[0].boxes.cls[0])
            raw_label = model.names[pred_idx]
            label = label_map.get(raw_label, raw_label)

            cv2.putText(frame, label, (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

            if last_emotion is None or label != last_emotion:
                last_emotion = label
                recommended_tracks = get_spotify_recommendations(label)
                print(f"🎵 Updated tracks for {label}: {len(recommended_tracks)} found")

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/current_tracks')
def current_tracks():
    global last_emotion, recommended_tracks
    return {
        "emotion": last_emotion,
        "tracks": recommended_tracks
    }

@app.route('/shutdown_camera')
def shutdown_camera():
    global camera
    if camera:
        camera.release()
        camera = None
    return "Camera released"

if __name__ == '__main__':
    app.run(debug=True, port=8000)
