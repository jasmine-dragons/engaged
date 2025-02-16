import cv2
from deepface import DeepFace
import time

# Initialize webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Variables for emotion analysis
emotions = {}
start_time = time.time()
duration = 30  # 30 seconds

print("Starting webcam for 30 seconds...")

while time.time() - start_time < duration:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Analyze emotions using DeepFace
    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        dominant_emotion = result[0]['dominant_emotion']

        # Update emotions dictionary
        if dominant_emotion in emotions:
            emotions[dominant_emotion] += 1
        else:
            emotions[dominant_emotion] = 1

        # Display the frame with the dominant emotion
        cv2.putText(frame, f"Emotion: {dominant_emotion}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    except Exception as e:
        print(f"Error analyzing frame: {e}")

    # Display the frame
    cv2.imshow('Webcam', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Calculate the most frequent emotion
if emotions:
    most_frequent_emotion = max(emotions, key=emotions.get)
    print(f"Most frequent emotion during the 30 seconds: {most_frequent_emotion}")
else:
    print("No emotions detected.")
