import cv2



frameHeight = 600
frameWidth = 700
capture=cv2.VideoCapture(0)
# capture.set(4,frameHeight)
while True:
    success,frame=capture.read()
    frame=cv2.resize(frame,(frameWidth,frameHeight))
    cv2.imshow("Test Video",frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

