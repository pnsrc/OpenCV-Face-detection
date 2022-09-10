import winsound
import numpy as np
import cv2
import pyttsx3

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height
timer = 0

# Function to draw text on the screen
def draw_text(img, text, pos, bg_color):
    font_face = cv2.FONT_HERSHEY_PLAIN
    scale = 1
    color = (255, 255, 255)
    thickness = cv2.FILLED
    margin = 2

    txt_size = cv2.getTextSize(text, font_face, scale, thickness)
    end_x = pos[0] + txt_size[0][0] + margin
    end_y = pos[1] - txt_size[0][1] - margin
    cv2.rectangle(img, pos, (end_x, end_y), bg_color, thickness)
    cv2.putText(img, text, pos, font_face, scale, color, 1, cv2.LINE_AA)
# озвучивание текста без прерывания программы
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
# make video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('videocam.avi', fourcc, 20.0, (640, 480))


while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face = faceCascade.detectMultiScale(
        gray,

        scaleFactor=1.2,
        minNeighbors=5
        ,
        minSize=(20, 20)
    )

    draw_text(img, "DeWorkers. version 0.0.1b . Press 'ESC' to exit", (10, 20), (0, 0, 0))

    if len(face) > 0 and timer == 0:
        draw_text(img, "Face detected", (10, 60), (0, 255, 0))
        timer = 1
    # Если лицо не обнаружено, то сбрасываем таймер
    if len(face) == 0:
        timer = 0

    # Написать текст на экране о количестве обнаруженных лиц
    draw_text(img, "Faces: "  + str(len(face)), (10, 40), (0, 0, 0))




    for (x,y,w,h) in face:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]



    #show full screen without stretch image
    cv2.namedWindow('DeWorkers', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('DeWorkers', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow('DeWorkers',img)
    out.write(img)

    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break

#if pressed close button on window then close
    if cv2.getWindowProperty('DeWorkers', 0) < 0:
        break




cap.release()
cv2.destroyAllWindows()
