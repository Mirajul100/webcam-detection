import cv2
import time
from emailing import send_mail
from datetime import datetime
import glob
from threading import Thread
from clean import clean_folder

video = cv2.VideoCapture(0)
time.sleep(1)
status_list = []
image_count = 1

first_frame = None
while True:
    status = 0
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

    cv2.putText(img=frame, text=datetime.now().strftime("%A"), org=(10, 25)
                , fontFace=cv2.FONT_HERSHEY_PLAIN
                , fontScale=1
                , color=(0 , 0 , 0)
                , thickness=1
                , lineType=cv2.LINE_AA)
    
    cv2.putText(img=frame , text=datetime.now().strftime("%Y:%m:%d") , org=(10 , 45) 
                , fontFace=cv2.FONT_HERSHEY_PLAIN 
                , color=(0 , 0 , 0)
                ,fontScale=1
                , thickness=1
                ,lineType=cv2.LINE_AA)
    
    cv2.putText(img=frame , text=datetime.now().strftime("%H:%M:%S") , org=(10 , 65) 
                , fontFace=cv2.FONT_HERSHEY_PLAIN 
                , color=(0 , 0 , 0)
                ,fontScale=1
                , thickness=1
                ,lineType=cv2.LINE_AA)

    contour_frame , check = cv2.findContours(dil_frame , cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_TC89_L1)
    for contour in contour_frame:
        if cv2.contourArea(contour) < 2000:
            continue
        x , y , w , h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame , pt1=(x, y) , pt2=(x+w , y+h) 
                                  , color=(0 , 255 , 0) , thickness=1)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"image/{image_count}.png" , frame)
            image_count = image_count + 1
            all_image = glob.glob("image/*.png")
            middle_image = int(len(all_image) / 2)
            image_obj = all_image[middle_image]
    
    status_list.append(status)
    status_list = status_list[-2:]
    print(status_list)

    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_mail , args=(image_obj ,))
        email_thread.daemon = True
        email_thread.start()

        clean_thread = Thread(target=clean_folder)
        clean_thread.daemon = True
        clean_thread.start()
    
    cv2.imshow("Video", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()


