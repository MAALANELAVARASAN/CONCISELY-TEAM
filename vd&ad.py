import cv2
import pyaudio
import wave
import threading

# Video settings
video_filename = "Output.L&T"
fps =30.0
frame_size = (640, 480)

# Audio settings
audio_filename = "output.wav"
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Initialize OpenCV video capture
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter(video_filename, fourcc, fps, frame_size)

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open audio stream
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)

frames = []
recording = True

def record_audio():
    """Function to record audio in a separate thread."""
    while recording:
        data = stream.read(CHUNK)
        frames.append(data)

# Start audio recording in a separate thread
audio_thread = threading.Thread(target=record_audio)
audio_thread.start()

print("Recording video and audio. Press 'q' to stop.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    out.write(frame)  # Save video
    cv2.imshow("Recording", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop recording
recording = False
audio_thread.join()

# Stop video capture
cap.release()
out.release()
cv2.destroyAllWindows()

# Stop audio stream
stream.stop_stream()
stream.close()
audio.terminate()

# Save audio file
with wave.open(audio_filename, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"Video saved as {video_filename}")
print(f"Audio saved as {audio_filename}")
