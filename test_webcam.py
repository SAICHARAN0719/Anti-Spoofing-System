import cv2
import time

# Use index 0 (or 1 if the first doesn't work)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not access the webcam.")
else:
    print("Webcam opened successfully!")

    # Capture the start time to measure the 1-minute duration
    start_time = time.time()

    # Start capturing video for 1 minute
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to capture an image.")
            break

        # Display the frame in the window
        cv2.imshow("Test Webcam", frame)

        # Check if 60 seconds have passed
        if time.time() - start_time >= 60:
            print("1 minute is up! Closing webcam.")
            break

        # Wait for 1 ms to check if any key is pressed (press 'q' to exit early)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting early...")
            break

    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()
