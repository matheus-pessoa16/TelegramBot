from threading import Thread
import cv2
import time
stop = True

class tre(Thread):
    def __init__(self,name,bot,chats):
        Thread.__init__(self)
        self.name=name
        self.bot = bot
        self.chats = chats
        for id in self.chats:
            self.bot.send_message(chat_id=id,text='The doorman is waiting someone')

    def run(self):
        try:
            global stop
            stop = True
            cap = cv2.VideoCapture(0)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface.xml')
            while(stop):
                ret, frame = cap.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                if(len(faces)):
                    for (x,y,w,h) in faces:
                        frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                    cv2.imwrite('foto.png',frame)
                    self.call()
                    self.exception()
                    break
            cap.release()
        finally:
            print('[INFO]thread ended')
            
    def exception(self):
        global stop
        stop = False
        print('[ACTION]stopping thread')
        for id in self.chats:
            self.bot.send_message(chat_id=id,text='The wait was stopped')

    def running(self):
        global stop
        return stop

    def call(self):
        print('[ACTION]visitor detected')
        for id in self.chats:
            foto = open('foto.png','rb')
            self.bot.send_message(chat_id=id,text='There is someone at the door!')
            self.bot.send_photo(chat_id=id,photo=foto)
        print('[ACTION]photo sended to all users '+str(self.chats))
