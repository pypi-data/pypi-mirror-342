import requests
from pathlib import Path
import cv2
import numpy as np
import tensorflow as tf
from datetime import datetime


class DeepFaceAntiSpoofing:
    def __init__(self):
        self.models_dir = Path.cwd() / "models"
        self.data_dir = Path.cwd() / "data"
        self.age_gender_model_path = self.models_dir / "age_gender_model.h5"
        self.anti_spoofing_model_path = self.models_dir / "anti_spoofing_model.h5"
        self.cascade_path = self.data_dir / "haarcascade_frontalface_default.xml"
        self._ensure_resources()
        self.age_gender_model = self._load_age_gender_model()
        self.anti_spoofing_model = self._load_anti_spoofing_model()
        # Load Haar Cascade
        self.face_cascade = cv2.CascadeClassifier(str(self.cascade_path))
        if self.face_cascade.empty():
            raise Exception("Failed to load Haar Cascade classifier")

    def _ensure_resources(self):
        """
        Ensure models and Haar Cascade file are available.
        Downloads them if they don't exist.
        """
        # Create directories
        self.models_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)

        # Download age_gender_model.h5 if not present
        if not self.age_gender_model_path.exists():
            print("Downloading age_gender_model.h5...")
            response = requests.get("https://ipsoftechs.pythonanywhere.com/media/age_gender_model.h5")
            if response.status_code == 200:
                with open(self.age_gender_model_path, "wb") as f:
                    f.write(response.content)
                print("age_gender_model.h5 downloaded successfully.")
            else:
                raise Exception("Failed to download age_gender_model.h5")

        # Download anti_spoofing_model.h5 if not present
        if not self.anti_spoofing_model_path.exists():
            print("Downloading anti_spoofing_model.h5...")
            response = requests.get("https://ipsoftechs.pythonanywhere.com/media/anti_spoofing_model.h5")
            if response.status_code == 200:
                with open(self.anti_spoofing_model_path, "wb") as f:
                    f.write(response.content)
                print("anti_spoofing_model.h5 downloaded successfully.")
            else:
                raise Exception("Failed to download anti_spoofing_model.h5")

        # Download haarcascade_frontalface_default.xml if not present
        if not self.cascade_path.exists():
            print("Downloading haarcascade_frontalface_default.xml...")
            response = requests.get(
                "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
            )
            if response.status_code == 200:
                with open(self.cascade_path, "wb") as f:
                    f.write(response.content)
                print("haarcascade_frontalface_default.xml downloaded successfully.")
            else:
                raise Exception("Failed to download haarcascade_frontalface_default.xml")

    def _load_age_gender_model(self):
        """
        Load the age and gender model.
        """
        model = tf.keras.models.load_model(self.age_gender_model_path, compile=False)
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
            loss={
                'age': tf.keras.losses.CategoricalCrossentropy(),
                'gender': tf.keras.losses.CategoricalCrossentropy()
            },
            metrics={
                'age': 'accuracy',
                'gender': 'accuracy'
            }
        )
        return model

    def _load_anti_spoofing_model(self):
        """
        Load the anti-spoofing model.
        """
        model = tf.keras.models.load_model(self.anti_spoofing_model_path, compile=False)
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        return model

    def _convert_to_serializable(self, data):
        """
        Convert numpy types to JSON-serializable types.
        """
        if isinstance(data, dict):
            return {k: self._convert_to_serializable(v) for k, v in data.items()}
        elif isinstance(data, (np.float32, np.float64)):
            return float(data)
        elif isinstance(data, (np.int32, np.int64)):
            return int(data)
        return data

    def _detect_face(self, file_path: str) -> tuple[bool, str | tuple]:
        """
        Detect faces in the image using Haar Cascade (from Flask app).

        Args:
            file_path (str): Path to the image file.

        Returns:
            tuple: (True, face_coords) if exactly one face is detected,
                   (False, error_message) otherwise.
        """
        try:
            img = cv2.imread(file_path)
            if img is None:
                return False, "Failed to load image"

            # Convert to grayscale for face detection
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )

            # Return True if exactly one face is detected, False otherwise
            if len(faces) == 1:
                return True, faces[0]  # Return face coordinates
            elif len(faces) == 0:
                return False, "No face detected"
            else:
                return False, "Multiple faces detected"
        except Exception as e:
            return False, str(e)

    def analyze_image(self, file_path: str) -> dict:
        """
        Analyze an image for age, gender, and spoof detection (from Flask app).

        Args:
            file_path (str): Path to the image file.

        Returns:
            dict: Analysis results containing age, gender, spoof, or error details.
        """
        # Validate face detection
        face_detected, message_or_coords = self._detect_face(file_path)
        if not face_detected:
            return {"error": message_or_coords}

        try:
            img = cv2.imread(file_path)
            if img is None:
                raise ValueError("Failed to load image")

            # Preprocess for age/gender (96x96)
            img_age_gender = cv2.resize(img, (96, 96))
            img_age_gender = img_age_gender.astype(np.float32) / 255.0
            img_age_gender = np.expand_dims(img_age_gender, axis=0)

            # Preprocess for anti-spoofing (128x128)
            img_anti_spoof = cv2.resize(img, (128, 128))
            img_anti_spoof = img_anti_spoof.astype(np.float32) / 255.0
            img_anti_spoof = np.expand_dims(img_anti_spoof, axis=0)

            # Predict age and gender
            age_pred, gender_pred = self.age_gender_model.predict(img_age_gender)
            age = int(np.argmax(age_pred[0]))
            gender_probs = gender_pred[0]
            gender_dict = {'Male': float(gender_probs[0]), 'Female': float(gender_probs[1])}
            dominant_gender = 'Male' if gender_probs[0] > gender_probs[1] else 'Female'

            # Predict real/fake
            spoof_pred = self.anti_spoofing_model.predict(img_anti_spoof)
            spoof_prob = float(spoof_pred[0][0])
            is_real = spoof_prob > 0.5
            spoof_dict = {'Fake': 1.0 - spoof_prob, 'Real': spoof_prob}
            dominant_spoof = 'Real' if is_real else 'Fake'

            analysis = {
                "age": age,
                "gender": gender_dict,
                "dominant_gender": dominant_gender,
                "spoof": spoof_dict,
                "dominant_spoof": dominant_spoof,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            return self._convert_to_serializable(analysis)
        except Exception as e:
            return {"error": str(e)}


# Example usage
if __name__ == "__main__":
    deepface = DeepFaceAntiSpoofing()
    result = deepface.analyze_image("path_to_image.jpg")
    print(result)