import cv2
import time
import wave
import threading
import pyaudio
start_time = time.time()  # Record start time
time_limit = 2 * 60  # 2 minutes (in seconds)

# Video settings
video_filename = "output.avi"
fps = 20.0
frame_size = (640, 480)


# Audio settings
audio_filename = "output.wav"
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Open default webcam (0), use 1 or 2 if multiple cameras are connected
# object to read from camera 
cap = cv2.VideoCapture(0)

# Initialize PyAudio
audio = pyaudio.PyAudio()


if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
result = cv2.VideoWriter('filename.l&t',  
                         cv2.VideoWriter_fourcc(*'MJPG'), 10, frame_size) 


while True:

    # Capture frame-by-frame
    ret, frame = cap.read()
    start_time = time.time()  # Record start time
    time_limit = 2 * 60 

    if not ret:
        print("Error: Could not read frame.")
        break

    # Display the resulting frame
    cv2.imshow('LIMIT 2:00', frame)
    


        
    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('m') and start_time> time_limit:
        
# Release the webcam and close windows
        cap.release()    
        result.release
        cv2.destroyAllWindows()



print("the video saved sucessfully")

    
