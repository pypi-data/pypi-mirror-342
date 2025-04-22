import cv2
import face_recognition
import os
from datetime import datetime

class FaceAttendanceSystem:
    def __init__(self, known_faces_path="known_faces"):
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_known_faces(known_faces_path)

    def load_known_faces(self, path):
        for file in os.listdir(path):
            img = face_recognition.load_image_file(f"{path}/{file}")
            encoding = face_recognition.face_encodings(img)[0]
            self.known_face_encodings.append(encoding)
            self.known_face_names.append(os.path.splitext(file)[0])
        print("✅ Known faces loaded.")

    def mark_attendance(self, name):
        with open("attendance.csv", "a") as f:
            now = datetime.now()
            dt_string = now.strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"{name},{dt_string}\n")
            print(f"📝 Attendance marked for {name}")

    # New method to process attendance from an image
    def run_from_image(self, image_path):
        print(f"📷 Processing image: {image_path}")
        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                index = matches.index(True)
                name = self.known_face_names[index]
                self.mark_attendance(name)
            else:
                print("❌ No match found.")

# Example usage
attendance_system = FaceAttendanceSystem("known_faces")
attendance_system.run_from_image("test_image.jpg")  # replace with your image filename
