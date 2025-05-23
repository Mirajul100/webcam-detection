import cv2
import time

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
while True:
    check , frame = video.read()
    gray_frame = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)

    # This is blur the video and tuple are use to blur the video
    gray_frame_gau = cv2.GaussianBlur(gray_frame , (21 , 21) , 0)

    if first_frame is None:
        first_frame = gray_frame_gau
    
    # Compare the first_frame and gray_frame
    gama_frame = cv2.absdiff(first_frame , gray_frame)

    thresh = cv2.threshold(gama_frame , 60.50 , 255 , cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh , None , iterations=2)

    # This code for show the video
    # cv2.imshow("My video", dil_frame)

    contour_frame , check = cv2.findContours(dil_frame , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)
    for contour in contour_frame:
        if cv2.contourArea(contour) < 5000:
            continue
        x , y , w , h = cv2.boundingRect(contour)
        cv2.rectangle(frame , pt1=(x, y) , pt2=(x+w , y+h) , color=(0 , 255 , 0) , thickness=2)

    cv2.imshow("Video" , frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()