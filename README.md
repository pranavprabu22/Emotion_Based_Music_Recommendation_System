# Emotion-Based Music Recommendation System

This project integrates real-time facial emotion recognition with the Spotify API to recommend music tracks that align with the detected emotional state of the user. It leverages computer vision for emotion detection and a Flask web application to serve the results.


## Features

- **Real-Time Emotion Detection**  
  Uses a YOLO-based model to detect facial expressions from a live camera feed.

- **Emotion-to-Music Mapping**  
  Automatically recommends Spotify tracks based on the detected emotion.

- **Web-Based Streaming**  
  Provides a live video feed with detected emotions annotated on the video frames.

- **Dynamic Updates**  
  Refreshes music recommendations when a new emotion is detected.


## Technologies Used

- **Python 3.9+**
- **Flask** (for serving the web application)
- **OpenCV (cv2)** (for camera capture and video processing)
- **Ultralytics YOLO** (for emotion recognition)
- **Spotify API** (via `spotifysearch` package for music recommendations)
- **Pillow** (for image handling)


## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/emotion-music-recommender.git
   cd emotion-music-recommender
   ```

2. **Create and Activate a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate     # On macOS/Linux
   venv\Scripts\activate        # On Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Spotify API Credentials**
   
-  Register an application in the Spotify Developer Dashboard.
-  Note the Client ID and Client Secret.
-  Add them to your environment variables:
   ```bash
   export SPOTIFY_CLIENT_ID="your_client_id"
   export SPOTIFY_CLIENT_SECRET="your_client_secret"
   ```
   or declare them as globals within the Flask app.

## Running the Application

1. **Start the Flask App**
   ```bash
   python app.py
   ```

2. **Open in Browser**
   
   Navigate to:
   ```bash
   http://127.0.0.1:8000/ # Choose your port number (8000 was used for this project)
   ```

3. **Interact**
-  Allow access to your webcam.
-  The application will display your live video feed with detected emotions.
-  Music recommendations will update dynamically when your emotion changes.
  
## Project Structure
   ```php
   emotion-music-recommender/
   │
   ├── app.py                  # Main Flask application
   ├── model/                  # Pretrained YOLO model for emotion recognition
   ├── static/
   │   └── uploads/            # Uploaded images (if applicable)
   ├── templates/
   │   └── index.html          # Frontend HTML template
   ├── requirements.txt        # Python dependencies
   └── README.md               # Documentation
   ```

## Example Workflow
-  The webcam captures a frame.
-  The YOLO model detects the dominant facial emotion.
-  The detected emotion is mapped to a corresponding category.
-  A set of recommended Spotify tracks is fetched via the spotifysearch package.
-  The recommendations update whenever a new emotion is detected.

## Future Enhancements
-  **Playlist Generation**

   Automatically create and save Spotify playlists based on detected moods.

-  **Support for Multiple Faces**
   
   Extend emotion detection to handle multiple users simultaneously.

-  **Cloud Deployment**

   Deploy the system to a cloud platform such as AWS or Heroku for broader access.

-  **Individualize Music**

   Have the user log in to provide access to their music taste, and finetune the recommendations further based on each user.

**Made by Pranav Prabu**