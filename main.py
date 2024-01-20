import cv2


# test_image=cv2.imread("photos/download.jpeg")
# cv2.imshow("downloads",test_image)
# cv2.waitKey(0)



# capture=cv2.VideoCapture("photos/testvid.mp4")


frameHeight = 600
frameWidth = 700
capture=cv2.VideoCapture(0)

# capture.set(3,frameWidth)
# capture.set(4,frameHeight)
while True:
    success,frame=capture.read()
    frame=cv2.resize(frame,(frameWidth,frameHeight))
    cv2.imshow("Test Video",frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

