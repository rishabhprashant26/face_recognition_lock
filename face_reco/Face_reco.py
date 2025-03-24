import cv2
import dlib
import serial
import time

# Initialize serial communication with Arduino
arduino = serial.Serial('COM3', 9600)  # Change 'COM3' to your Arduino port

# Load the face detector and shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # Add this file in the same directory

# Load the desired face image
desired_face = cv2.imread(r"C:\Users\rishabh prashant\OneDrive\Desktop\face recognition\face.jpg", cv2.IMREAD_GRAYSCALE)

# Face recognition function
def recognize_face(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    
    for face in faces:
        x, y, w, h = (face.left(), face.top(), face.width(), face.height())
        face_roi = gray[y:y+h, x:x+w]
        
        # Compare detected face with desired face
        result = cv2.matchTemplate(face_roi, desired_face, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        
        if max_val > 0.6:  # Confidence threshold
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, "Access Granted", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            return True
    return False

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    if recognize_face(frame):
        arduino.write(b'U')  # Send 'U' to unlock
        time.sleep(5)  # Unlock for 5 seconds
        arduino.write(b'L')  # Send 'L' to lock again
    
    cv2.imshow('Face Recognition Lock', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
