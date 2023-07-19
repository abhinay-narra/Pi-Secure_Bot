import time
import telepot
import RPi.GPIO as GPIO
import subprocess
import fswebcam 



bot = telepot.Bot('6136636907:AAHlylcTI4Dj0bh7U2OE3NvL94mShcuwpiw') 
chat_id = 1203088996
pir_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(pir_pin, GPIO.IN)





def handle_message(msg): 
    global continue_sending
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        if msg['text'] == 'Yo': 
            bot.sendMessage(chat_id, 'Hello, I am your PIR sensor bot.') 
        elif msg['text'] == 'Stop': bot.sendMessage(chat_id, 'Stopping notifications.') 
        continue_sending = False
        else: bot.sendMessage(chat_id, 'Sorry, I did not understand your message. Please type "Yo" to get started and "Stop" to stop notifications')





bot.message_loop(handle_message) 
continue_sending = True 
while continue_sending:
    if GPIO.input(pir_pin): 
        message = 'Motion detected!' 
        bot.sendMessage(chat_id, message)
        print('Message sent: {}'.format(message)) 
        subprocess.call(['fswebcam', '-r', '640X480', '--no-banner', 'motion.jpg']) 
        with open('motion.jpg', 'rb') as f: 
            bot.sendPhoto(chat_id, f)
        print('Photo sent.')
        time.sleep(1) 
    else: 
        message = 'Motion not detected.' 
        bot.sendMessage(chat_id, message)
        print('Message sent: {}'.format(message))
        time.sleep(1)
