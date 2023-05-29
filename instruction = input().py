from cv2 import VideoCapture, CascadeClassifier, cvtColor, COLOR_BGR2GRAY, rectangle, resize, waitKey, CAP_PROP_FPS
from playsound import playsound
import threading

# Load the pre-trained Haar cascade for human detection
face_cascade = CascadeClassifier("C:\\Users\\GAMINGPC\\Desktop\\Arduino\\Python Course\\haarcascade_lowerbody.xml")

# Open the webcam
cap = VideoCapture(0)
cap.set(CAP_PROP_FPS, 20)
print('start')

# Check if the webcam is successfully opened
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# Flag variable to track human detection
human_detected = False
sound_thread = None

# Function to play the sound repeatedly
def play_sound():
    while human_detected:
        playsound('C:\\Users\\GAMINGPC\\Desktop\\attack2t22wav-14511.mp3')

while True:
    # Read the current frame from the webcam
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cvtColor(resize(frame, (350, 350)), COLOR_BGR2GRAY)

    # Perform human detection
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.03, minNeighbors=3, minSize=(10, 10))

    # Draw bounding boxes around the detected humans
    for (x, y, w, h) in faces:
        rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        human_detected = True

    # Start or stop the sound thread based on human detection
    if human_detected and sound_thread is None:
        sound_thread = threading.Thread(target=play_sound)
        sound_thread.start()
    elif not human_detected and sound_thread is not None:
        human_detected = False  # Stop the sound loop
        sound_thread.join()
        sound_thread = None

    human_detected = False

    # Break the loop if 'q' key is pressed
    if waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
