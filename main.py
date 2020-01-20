import cv2
import camera
import camera_thread
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests
import re
import threading

chats = []
t = None

def is_registered(bot,chat_id):
        for id in chats:
                if(id==chat_id):
                        return True
        print('[INFO]fail acess from : '+str(chat_id))
        bot.send_message(chat_id=chat_id,text='You are not registered')
        return False

def register(bot,update):
        chat_id = update.message.chat_id
        data = update.message.text.split(' ')
        if(len(data)<3):
                bot.send_message(chat_id=chat_id,text='the sintax of this command is:')
                bot.send_message(chat_id=chat_id,text='/remember login password')
        if(data[1]=='labhome' and data[2]=='123'):
                registered = False
                
                for id in chats:
                        if(id == chat_id):
                                registered=True
                                break
                if(registered):
                        print('[INFO]user '+str(chat_id)+' is already registered')
                        bot.send_message(chat_id=chat_id,text='You are already registered')
                else:
                        print("[INFO]registered: "+str(chat_id))
                        bot.send_message(chat_id=chat_id,text='You are registered')
                        chats.append(chat_id)
        else:
                print("[INFO]fail register : "+str(chat_id))
                bot.send_message(chat_id=chat_id,text='Wrong user or password')

def unregister(bot,update):
        if(is_registered(bot,update.message.chat_id)):
                chat_id = update.message.chat_id
                i = 0
                deleted = False
                for id in chats:
                        if(id==chat_id):
                                chats.pop(i)
                                deleted=True
                        i=i+1
                if(deleted):
                        print('[ACTION]user '+str(chat_id)+' unregistered')
                        bot.send_message(chat_id=chat_id,text='You are unregistered')
                else:
                        bot.send_message(chat_id=chat_id,text='You are not registered') 
def wait(bot,update):
        if(is_registered(bot,update.message.chat_id)):
                global t
                print('[ACTION]camera started')
                t = camera_thread.tre(1,bot,chats)
                t.start()
                #t.join()
                #call(bot)

def call(bot):
        print('[ACTION]visitor detected')
        foto = open('foto.png','rb')
        for id in chats:
                bot.send_message(chat_id=id,text='There is someone at the door!')
                bot.send_photo(chat_id=id,photo=foto)
        print('[ACTION]photo sended to all users')

def capture(bot,update):
        global t
        wasrunning = False
        try:
                if(t.running()):
                        t.exception()
                        wasrunning = True
        except:
                pass
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cv2.imwrite("foto.png", frame)
        cap.release()
        print('[INFO]photo captured')
        if(wasrunning):
                wait(bot,update)
                wasrunning=False
                 
def pic(bot, update):
        if(is_registered(bot,update.message.chat_id)):
                capture(bot,update)
                chat_id = update.message.chat_id
                bot.send_photo(chat_id=chat_id, photo=open('foto.png','rb'))
                print('[ACTION]sending photo to : '+str(chat_id))

def stop(bot, update):
        if(is_registered(bot,update.message.chat_id)):
                t.exception()

def main():
	updater = Updater('<your-key-here>')
	son = updater.bot
	dp = updater.dispatcher
	dp.add_handler(CommandHandler('pic',pic))
	dp.add_handler(CommandHandler('wait',wait))
	dp.add_handler(CommandHandler('remember',register))
	dp.add_handler(CommandHandler('forget',unregister))
	dp.add_handler(CommandHandler('stop', stop))
	updater.start_polling()
	updater.idle()


if __name__ == '__main__':

        main()
