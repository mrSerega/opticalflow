import cv2 as cv
import sys
import math
import matplotlib.pyplot as plt

# mods

ONLINE = 0
OFFLINE = 1
DIAG = 1

# read args

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

# find good foe

LOG_PATH = sys.argv[1]
goodDot = sys.argv[1].split('.')[0]
goodDot = './samples/{}.txt'.format(goodDot)
goodDot = open(goodDot, 'r').read()
gx, gy = goodDot.split(' ')
gx = float(gx)
gy = float(gy)

# consts

LOG_FILE_NAME = './logs/{}/foe_log.txt'.format(LOG_PATH)
RED = (0,0,255)
GREEN = (0,255,0)
RADIUS = 20
THICKNESS = 2
WAIT = 10

def make_history(MODE, log_file):

    cor = []
    filename = []

    if MODE == OFFLINE:
        for line in log_file:
            if line[0] != 's':
                numbers = line.split(' ')
                tempX = float(numbers[0])
                tempY = float(numbers[1])
                if tempX > 1 or tempY > 1:
                    continue
                cor.append((tempX,1-tempY))
            if line[0] == 's':
                l = line.split(' ')
                filename.append(l[-2])
        x = 0
        y = 0
        for elem in cor:
            x += elem[0]
            y += elem[1]

        x /= len(cor)
        y /= len(cor)
        for idx in range(len(cor)):
            cor[idx] = (x,y)
    elif MODE == ONLINE:
        for line in log_file:
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
    
    return cor, filename

def plot_video(cor, filename):
    for idx in range(len(cor)):
        image = cv.imread(filename[idx])
        x = cor[idx][0]
        y = cor[idx][1]
        h = image.shape[0]
        w = image.shape[1]
        DIAG = int(math.sqrt(h*h + w * w))
        cv.circle(image, (int(w * x), int(h* y)), RADIUS ,RED, THICKNESS)
        cv.circle(image, (int(w * gx), int(h * gy)), RADIUS, GREEN, THICKNESS )
        cv.imshow('test',image)
        cv.waitKey(WAIT)

def d(goodDot, badDot, DIAG):
    return ((goodDot[0]-badDot[0])**2 + (goodDot[1]-badDot[1])**2) / DIAG

def quality_online(cor, goodDot, DIAG):

    res = []

    for dot in cor:
        res.append(d(goodDot, dot, DIAG))

    
    plt.plot(res)
    plt.show()

def quality_offline(cor, goodDot, DIAG):
    res = []
    history = []
    for dot in cor:
        history.append(dot)
        xs = 0
        ys = 0
        for elem in history:
            xs += elem[0]
            ys += elem[1]
        xs /= len(history)
        ys /= len(history)
        res.append(d(goodDot, (xs,ys), DIAG))

    plt.plot(res)
    plt.show()

def get_mid_dot(dost):
    xs = 0
    ys = 0
    for dot in dots:
        xs += dots[0]
        ys += dots[1]
    xs /= len(dots)
    ys /= len(dots)
    return (xs, ys)

def quality_online_lag(cor, goodDot, lag, DIAG):
    if lag > len(cor):
        raise Exception('lag more than len of cor list')
        
    res = []
    history = []
    for idx in range(1,len(cor)):
        first = idx - lag
        if first < 0: first = 0
        his = cor[first:idx]
        xs = 0
        ys = 0
        for dot in his:
            xs += dot[0]
            ys += dot[1]
        xs /= len(his)
        ys /= len(his)
        res.append(d(goodDot, (xs,ys), DIAG))
    return sum(res)/len(res)

def plot_quality_online_lag(cor, goodDot, DIAG):
    res = []
    for idx in range(len(cor)):
        res.append(quality_online_lag(cor, goodDot, idx+1, DIAG))
    plt.plot(res)
    plt.show()

def main():
    log = open(LOG_FILE_NAME, 'r')
    cor, filename = make_history(MODE, log)
    plot_video(cor, filename)
    quality_online(cor, (gx, gy), DIAG)
    quality_offline(cor, (gx, gy), DIAG)
    plot_quality_online_lag(cor, (gx, gy), DIAG)

if __name__ == '__main__':
    main()