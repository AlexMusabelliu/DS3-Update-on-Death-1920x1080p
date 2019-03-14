import cv2, numpy, socket
from PIL import ImageGrab, Image
from time import sleep

left = 598
upper = 475
right = 1320
lower = 612
stopPONGING = 0

HOST = 'irc.twitch.tv'
PORT = 6667
OAUTH = 'oauth:96cwhmzyqou0k3cejcpzafakl74gpk'
USER = 'flameon122'
CHAN = '#flameon122'


irc = socket.socket()
irc.settimeout(0.3)
irc.connect((HOST, PORT))
irc.send("PASS {}\r\n".format(OAUTH).encode("utf-8"))
irc.send("NICK {}\r\n".format(USER).encode("utf-8"))
irc.send("JOIN {}\r\n".format(CHAN).encode("utf-8"))


while True:
    sleep(0.2)
    try:
        scr = numpy.asarray(ImageGrab.grab((left,upper,right,lower)))
    except:
        print("Failed to capture screenshot")
    r, g, b = cv2.split(scr)
    scr = cv2.merge([b, g, r])
    hsv = cv2.cvtColor(scr, cv2.COLOR_BGR2HSV)
    #print(cv2.cvtColor(numpy.uint8([[[13,13,94]]]), cv2.COLOR_BGR2HSV))
    
    mask = cv2.inRange(hsv, numpy.array([0,220,94]), numpy.array([0,225,94]))
    mask2 = cv2.inRange(hsv, cv2.cvtColor(numpy.uint8([[[13,13,94]]]), cv2.COLOR_BGR2HSV), cv2.cvtColor(numpy.uint8([[[13,13,94]]]), cv2.COLOR_BGR2HSV))
    res = cv2.bitwise_and(scr, scr, mask= mask)
    res2 = cv2.bitwise_and(scr, scr, mask= mask2)
    
    difference = cv2.subtract(res, res2)
    b1, g1, r1 = cv2.split(difference)
    if cv2.countNonZero(r1) != 0:
        print("deaths added")
        msg = '!deathadd'
        irc.send("PRIVMSG {} :{}\r\n".format(CHAN, msg).encode("utf-8"))
    try:    
        response = irc.recv(1024).decode("utf-8")
    except:
        pass
    if response == "PING :tmi.twitch.tv\r\n" and stopPONGING == 0:
        stopPONGING = 1
        irc.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        print("Pong")
    if stopPONGING == 5:
        stopPONGING = 0
    else:
        stopPONGING += 1
    #print('cont')
    #cv2.imshow('mask', difference)
    #cv2.imshow('mask2', res2.shape)
    #cv2.waitKey()
    #cv2.destroyAllWindows()

    
