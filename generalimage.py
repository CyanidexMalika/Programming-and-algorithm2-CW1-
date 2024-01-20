import cv2

# image=cv2.imread('photos/download.jpeg')
# image=cv2.resize(image,(900,800))
# image=cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
# # cv2.imwrite('New_image.jpeg',image)
# cv2.imshow("Image",image)
# cv2.waitKey(0)




video=cv2.VideoCapture(0)
# video=cv2.flip(video,1)
while True:
    success, frame=video.read()
    flipvid=cv2.flip(frame,1)
    cv2.imshow("Video",flipvid)
    if cv2.waitKey(1) == ord('q'):
        break
    
video.release()
cv2.destoryAllWindows()

