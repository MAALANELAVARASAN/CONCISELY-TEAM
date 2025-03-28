import threading
import time

def stop_execution():
    print("Time's up!")
    exit()  # Stop the program

# Start a 2-minute timer
timer = threading.Timer(2 * 60, stop_execution)
timer.start()

try:
    while True:
        print("Running...")
        time.sleep(10)  # Simulating work
except KeyboardInterrupt:
    print("Stopped by user.")

timer.cancel()  # Cancel the timer if task finishes early
