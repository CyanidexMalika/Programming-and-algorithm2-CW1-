import cv2

frameHeight = 600
frameWidth = 900
capture = cv2.VideoCapture(0)

while True:
    success, frame = capture.read()
    frame = cv2.resize(frame, (frameWidth, frameHeight))
    
    # Removing mirrored video from webcam part
    frame = cv2.flip(frame, 1)
    
    cv2.imshow("Test Video", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
