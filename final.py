import cv2
import winsound
import os
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust the speaking rate as needed

cam = cv2.VideoCapture(0)
movement_count = 0

while cam.isOpened():
    ret, frame1 = cam.read()
    ret, frame2 = cam.read()
    diff = cv2.absdiff(frame1, frame2)
    grey = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(grey, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 225, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        if cv2.contourArea(c) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        winsound.PlaySound('alert.wav', winsound.SND_ASYNC)
        movement_count += 1

        if movement_count <= 10:
            # Speak the warning for the first 10 movements detected.
            warning_text = f"Warning: Movement detected ({movement_count}/10). Do not move, or you will be logged out."
            engine.say(warning_text)
            engine.runAndWait()
        elif movement_count == 11:
            # After 10 warnings, log out the user (you may need to adjust this based on your system).
            print("Logging out...")
            # You can customize the logout command here.
            os.system("shutdown /l")
        elif movement_count >= 12:
            # After logging out, initiate a system shutdown.
            print("Warning: Detected movement after logout. Shutting down...")
            # You can customize the shutdown command here.
            os.system("shutdown /s /t 1")  # This command shuts down the PC after a 1-second delay.

    if cv2.waitKey(10) == ord('q'):
        break

    cv2.imshow('shail Cam', frame1)

cam.release()
cv2.destroyAllWindows()
