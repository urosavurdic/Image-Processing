# if you    try this code in your compiler be sure to change the size of the images depending on your webcam

import numpy as np
import cv2

# promenljiva koja identifikuje da li je doslo do klika
provera = False
# promenljive koje pamte 2D polozaj zeljenog frejma
a, b, c, d = -1, -1, -1, -1
# promenljive koje pamte lokaciju misa gde je kliknuo
x, y = -1, -1
# odre]ivanje ranga boja koje dolaze u obzir
lower = np.array([40, 40, 20])
upper = np.array([135, 255, 255])

# povezivanje sa kamerom!
cap = cv2.VideoCapture(0)

# odabiranje zeljene slike
image = cv2.imread("nature.jpg")
image = cv2.resize(image, (1024, 576))


# generise konture oko svih plavih i zelenih objekata do klika a posle njega projektuje sliku na zadati objekat
def napravi_konture(m):
    global x
    global y
    global a
    global b
    global c
    global d
    global provera
    if not provera:
        contures, hierarchy = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contures) != 0:
            for contour in contures:
                if cv2.contourArea(contour) > 500:
                    x2, y2, w, h = cv2.boundingRect(contour)
                    if x > x2 and x < x2 + w and y > y2 and y < y2 + h:
                        provera = True
                        a = x2
                        b = x2 + w
                        c = y2
                        d = y2 + h
                        print(a, b, c, d)
                    else:
                        cv2.rectangle(frame, (x2, y2), (x2 + w, y2 + h), (0, 0, 255), 3)


# funkcija izbacuje deo pod maskom
def filtriraj(frame, k):
    # kreira sliku pre filtriranja
    res = cv2.bitwise_and(frame, frame, mask=k)
    cv2.imshow("Res", res)
    # ckreira filtiranu sliku
    return frame - res


# funkcija hvata poslednje kliknutu koordinatu misa
def klik(event, x1, y1, flags, parameters):
    global x
    global y
    if event == cv2.EVENT_LBUTTONDOWN:
        x, y = x1, y1


if not cap.isOpened():
    print("Error opening video stream or file")

while cap.isOpened():
    # formira se skroz crna slika
    slika_filtar = np.zeros((576, 1024, 1), np.uint8)
    # prikayuje se skroz crna flika

    # snima se frejm po frejm
    ret, frame = cap.read()

    # detektuju se boje
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow("HSV", hsv)

    maska = cv2.inRange(hsv, lower, upper)
    cv2.imshow("Maska", maska)

    # crating lines
    napravi_konture(maska)
    if provera:
        # slika koja ce sluziti kao filtar definise se do kraja tacnije ocrtava koji segmet treba da isfiltrira
        slika_filtar = cv2.rectangle(slika_filtar, (b, a), (d, c), (255, 255, 255), -1)
        cv2.imshow("slika filtar", slika_filtar)

        # formira ce maska koja ce filtrirati zeljeni segment
        final_filtar = cv2.bitwise_and(slika_filtar, maska)
        cv2.imshow("Krajnje", final_filtar)
        f = filtriraj(frame, final_filtar)
        # cv2.imshow("maska", maska)
        final = np.where(f == 0, image, f)
        cv2.imshow('Filtered', f)
        # prikazuje filtriran snimak
        cv2.imshow('Final', final)

    if ret:

        cv2.imshow('Frame', frame)
        cv2.setMouseCallback('Frame', klik)
        # Pritiskom na q se izlazi iz programa
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

# osloba]a objekat koji snima
cap.release()

# Zatvara sve prozorw

cv2.destroyAllWindows()
