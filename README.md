# Emotion-Based Music Recommendation System

The Emotion-Based Music Recommendation System detects a user’s facial expressions in real time and recommends Spotify tracks that align with their emotional state. It integrates Ultralytics YOLO for emotion recognition, OpenCV for live video streaming, and the Spotify API for adaptive music selection, all served through a Flask web interface.

The application captures frames from the webcam, detects the dominant emotion, maps it to valence–arousal features (such as happiness → high valence, sadness → low valence), and dynamically updates music recommendations. The web app overlays emotion labels on the video stream and refreshes tracks seamlessly as user emotions change.

Development followed an iterative, experiment-driven process. Vision-based recognition was chosen over audio analysis due to better dataset availability and real-time integration potential. YOLO was selected after testing CNNs and MobileNet variants, balancing speed with robustness under varied conditions. Integration with OpenCV introduced latency challenges, solved by resizing frames and tuning inference intervals. Emotion-to-music mapping evolved from fixed genres to Spotify’s audio features (valence, energy), yielding more diverse and relevant results. Spotify API queries were refined to improve reliability, while Flask provided a lightweight but effective interface for real-time streaming and dynamic updates.

Key learnings emphasized how feature representation bridges subjective emotions with structured computational inputs, how real-time detection requires careful system-level optimizations, and how robust API handling safeguards user experience. The project also surfaced ethical considerations around bias, personalization, and privacy in affective computing, reinforcing the need for transparency and user control. Iterative refinements highlighted modularity and extensibility, setting the stage for multi-user support, personalization, and deployment at scale.

Planned enhancements include automatic playlist generation, multi-face emotion detection, cloud deployment, and personalized recommendations based on individual Spotify accounts.


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


## Process

The development of this system followed an iterative process, with several points of trial and error that shaped the final design:
1. **Defining the Problem Scope**
   -  The initial goal was to build an emotion-driven music recommender that could operate in real time.
   -  Early considerations involved whether to focus on audio-based emotion detection (speech analysis) or vision-based detection. Vision was chosen due to broader dataset availability and clearer integration with real-time video streams.
2. **Model Selection for Emotion Recognition**
   -  Several approaches were evaluated:
      -  Classical CNN models (e.g., FER2013-based classifiers) provided reasonable accuracy but lacked the speed necessary for real-time video.
      -  Lightweight models (e.g., MobileNet variants) offered faster inference but struggled with robustness under varied lighting and camera conditions.
      -  YOLO (Ultralytics) was ultimately selected for its superior balance of speed and accuracy, along with its flexibility for fine-tuning to emotion recognition tasks.
   -  This decision reflected a broader tradeoff between computational efficiency and predictive performance.
3. **Integration with OpenCV**
   -  Early prototypes processed static images for emotion detection.
   -  Transitioning to real-time frame capture introduced latency challenges, which required pipeline adjustments (e.g., resizing frames, adjusting inference intervals) to ensure responsiveness.
4. **Mapping Emotions to Music Attributes**
   -  Multiple mapping strategies were tested:
      -  A direct one-to-one mapping between emotions and genres.
      -  A valence-arousal model (e.g., happy → high valence, sad → low valence).
   - The second approach was adopted, as it aligned better with Spotify’s track metadata (valence, energy) and allowed for more dynamic and personalized queries.
5. **Spotify API Integration**
   -  Early implementations hardcoded genre seeds, which limited variety.
   -  Iterations introduced adaptive queries where emotion categories were translated into target audio features, producing more relevant and diverse recommendations.
   -  Error handling was added after observing API failures in cases of narrow queries, reinforcing the importance of robustness in external system integration.
6. **Web Application Layer**
   -  A basic command-line prototype was first developed to test the vision and recommendation pipeline.
   -  Flask was introduced as the interface layer to deliver a user-facing application. Trial deployments revealed issues with continuous frame streaming, leading to the adoption of generator-based responses in Flask for stable video updates.
7. **Iterative Refinements**
   -  Each stage of development followed a test-adjust cycle: improving latency, refining emotion-to-music mappings, and ensuring the system could handle unexpected cases (e.g., no face detected, ambiguous emotions).
   -  The project evolved from a minimal proof-of-concept into a modular architecture prepared for future extensions such as multi-user support and cloud deployment.


## Key Learnings

   This project served as an applied study in integrating affective computing with real-time systems. The following summarizes the key technical insights and reasoning behind the design choices:
1. **Emotion Recognition and Feature Mapping**
   -  Facial expressions were abstracted into discrete emotion categories, which were then mapped to Spotify attributes such as valence and energy.
   -  This process underscored the importance of designing feature representations that bridge subjective human states with structured computational inputs.
2. **Real-Time Detection with YOLO**
   -  YOLO was selected for its balance between inference speed and accuracy, which is critical for interactive systems.
   -  Implementing frame-by-frame inference within an OpenCV pipeline highlighted the need for system-level optimizations to maintain responsiveness.
3. **API Integration and Data Flow**
   -  Spotify’s API integration required translating emotional states into query parameters in a consistent and fault-tolerant manner.
   -  This reinforced the principle of robustness in software design, particularly in handling unreliable or incomplete external responses.
4. **System Integration via Flask**
   -  Flask provided a lightweight but effective framework for linking vision models and external APIs within a web-based interface.
   -  Attention to state management and concurrency ensured the system could deliver updates dynamically without interrupting the live video feed.
5. **Human-Centered and Ethical Considerations**
   -  The project raised broader questions around bias, personalization, and data privacy in affective computing.
   -  From a CS perspective, it highlighted the need to design adaptive systems that prioritize transparency and user agency.
6. **Scalability and Extensibility**
   -  Iterative development emphasized modularity, enabling future extensions such as multi-user support, playlist generation, and cloud deployment.
   -  These considerations reflected core CS principles of extensibility and scalability in software architecture.

Overall, the project demonstrated how principles of efficiency, robustness, and human-centered design can be applied to create systems that adapt computationally to human affective states.

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
