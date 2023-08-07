import cv2
import pickle 
import numpy as np
"""
countNonZero işlevi, belirli bir görüntü veya görüntü bölgesi içindeki 0 olmayan piksel sayisini hesaplar.
Siyah(0) pikseller dolgu olmayan(boş) alanlari temsil ederken,beyaz(255) pikseller doldurulmuş alanlari(araclari) temsil eder.
"""

cap=cv2.VideoCapture("video.mp4")

def check(frame1):
    space_counter=0 #boş alan gösterir
    for pos in liste:
        x,y=pos

        crop=frame1[y:y+15,x:x+26]
        count=cv2.countNonZero(crop) 
        if count<150: #siyah alanlar boşluğu temsil ettiği için  piksel değeri 0a yakın çıkacaktır bu yüzden 150 eşiği kullandık
            color=(0,255,0)
            space_counter+=1
        else:
            color=(0,0,255)
        cv2.rectangle(frame,pos,(pos[0]+26,pos[1]+15),color,2)
    cv2.putText(frame,f"bos:{space_counter}/{len(liste)}",(15,24),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),3)

with open("dots","rb") as f:
    liste=pickle.load(f)

while True:
    _,frame=cap.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gray,(3,3),1)
    thresh=cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
    median=cv2.medianBlur(thresh,5)
    dilates=cv2.dilate(median,np.ones((3,3)),iterations=1)

    check(dilates)




    cv2.imshow("img",frame)
    # cv2.imshow("gray",gray)
    # cv2.imshow("blur",blur)
    # cv2.imshow("thresh",thresh)
    # cv2.imshow("median",median)
    cv2.imshow("dilate",dilates)


    if cv2.waitKey(200) & 0xFF==ord("q"):
        break

cap.release()
cv2.destroyAllWindows()