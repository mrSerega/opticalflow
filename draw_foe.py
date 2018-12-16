import cv2 as cv
import sys

ONLINE = 0
OFFLINE = 1

cor = []
filename = []

print (sys.argv)

if len(sys.argv) == 2:
    MODE = ONLINE
elif len(sys.argv) == 3:
    if sys.argv[2] == 'online':
        MODE = ONLINE
    elif sys.argv[2] == 'offline':
        MODE = OFFLINE
    else:
        print ('ERROR: usage python draw_foe.py [online|offline]')
else:
     print ('ERROR: usage python draw_foe.py [online|offline]')

LOG_PATH = sys.argv[1]

LOG_FILE_NAME = './logs/{}/foe_log.txt'.format(LOG_PATH)
RED = (0,0,255)
RADIUS = 20
THICKNESS = 2
WAIT = 100

log = open(LOG_FILE_NAME, 'r')

if MODE == OFFLINE:
    for line in log:
        if line[0] != 's':
            print (line)
            numbers = line.split(' ')
            tempX = float(numbers[0])
            tempY = float(numbers[1])
            if tempX > 1 or tempY > 1:
                continue
            cor.append((tempX,1-tempY))
        if line[0] == 's':
            l = line.split(' ')
            print(l)
            filename.append(l[-2])

    x = 0
    y = 0
    for elem in cor:
        x += elem[0]
        y += elem[1]

    x /= len(cor)
    y /= len(cor)

    print ('cor:')
    print ((x,y))

    for idx in range(len(filename)):
        image = cv.imread(filename[idx])
        h = image.shape[0]
        w = image.shape[1]
        cv.circle(image, (int(w * x), int(h* y)), RADIUS ,RED, THICKNESS)
        cv.imshow('test',image)
        cv.waitKey(WAIT)

if MODE == ONLINE:
    for line in log:
        if line[0] != 's':
            numbers = line.split(' ')
            tempX = float(numbers[0])
            tempY = float(numbers[1])
            if tempX > 1 or tempY > 1:
                tempX = 0
                tempY = 1
            cor.append((tempX,1-tempY))
        if line[0] == 's':
            l = line.split(' ')
            print(l)
            filename.append(l[-2])

    for idx in range(len(filename)):
        image = cv.imread(filename[idx])
        x = cor[idx][0]
        y = cor[idx][1]
        h = image.shape[0]
        w = image.shape[1]
        cv.circle(image, (int(w * x), int(h* y)), RADIUS ,RED, THICKNESS)
        cv.imshow('test',image)
        cv.waitKey(WAIT)

