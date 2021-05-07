# pip install pyttsx3
#pip install SpeechRecognition
# pip install opencv-python
# pip install wikipedia
# pip install pywhatkit
# pip install secure-smtplib

import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import random
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
from _thread import start_new_thread #manual
import time
import smtplib
import sys

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)

#text to speech
def speak(audio) :
    engine.say(audio)
    print(audio)
    engine.runAndWait()
    
#audio input to text
def takeCommand():
    r =sr.Recognizer()
    with sr.Microphone() as source :
        #manual error handling
        try : 
            print("Listening ...")
            r.pause_threshold = 1
            audio = r.listen(source, timeout = 30, phrase_time_limit = 10 )
        
        except KeyboardInterrupt:
            sys.exit()
        
        except : 
            takeCommand()
            pass  
        
    try : 
        print("Recognizing ...")
        query = r.recognize_google(audio, language = "en-in")
        print(f"You said : {query}")
        
    except :
        speak("Say that again please ...")
        return "none"
    
    return query

#greet
def wish():
    hour = int(datetime.datetime.now().hour)

    if hour >=0 and hour <= 12 :
        speak("Good Morning ! ")
    elif hour >12 and hour <= 18 :
        speak("Good Afternoon ! ")
    else :
        speak("Good Evening ! ")

    speak("Hello on the other side. I am Jarvis, pleased " + 
        "to be here ! How may I be of assistance to you")

#send whatsapp message
def messageWhatsAppFunction(mobileNum, message, currHour, currMinute) : 
    kit.sendwhatmsg(mobileNum, message, currHour, currMinute)

    time.sleep(120)

#send email
def sendEmail(id, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
        
    speak("Enter your email address using the keyboard")
    userID = input("Enter here : ")
    
    speak("Enter the password of your email ID")
    userPassword = input("Enter here : ")
    
    server.login(userID, userPassword)
    server.sendmail(userID, id, content)
    server.close()

def main() :
    #manual
    # wish()

    
    while True:
        query = takeCommand().lower()
    
        #logic building for task

        if "open notepad" in query : 
            notepadPath = "C:\\Windows\\system32\\notepad.exe"
            os.startfile(notepadPath)
    
        if "open command prompt" in query : 
            os.system("start cmd")
            
        if "open camera" in query : 
            cap = cv2.VideoCapture(0)
            while True :
                ret, img = cap.read()
                cv2.imshow('webcam', img)
                k = cv2.waitKey(50)
                if k ==27 :
                    break
            
            cap.release()
            cv2.destroyAllWindows()
    
        if "play music" in query :
            music_dir = "D:\\voice\\custom\\songs"
            songs = os.listdir(music_dir)
            randomSong = random.choice(songs)
            os.startfile(os.path.join(music_dir, randomSong)) 
            
        if "ip address" in query :
         ip = get('https://api.ipify.org').text
         speak(f"IP address of your system is :  {ip}")
         
        if "wikipedia" in query : 
            speak("Searching Wikipedia ...")
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query,sentences = 2)
            speak("According to Wikipedia")
            speak(results)
            # print(results)
            
        if "open youtube" in query :
            
            speak("What should I search on Youtube")
            
            requestYoutube = takeCommand().lower() 
            requestYoutube = f"https://www.youtube.com/results?search_query={requestYoutube}"
            webbrowser.open(requestYoutube)
            webbrowser.open(requestYoutube)
            
            # kit.playonty("see you again")
            
            
        if "open facebook" in query :
            webbrowser.open("www.facebook.com")
            
        if "open stackoverflow" in query :
            webbrowser.open("www.stackoverflow.com")
            
        if "open geeksforgeeks" in query :
            webbrowser.open("www.geeksforgeeks.org")
            
        if "open google" in query :
            speak("What shoold I search on Google")
            
            requestGoogle = takeCommand().lower() 
            requestGoogle = requestGoogle.replace(' ', '+')
            requestGoogle = f"https://www.google.com/search?q={requestGoogle}"
            webbrowser.open(requestGoogle)
            
        if "send message" in query :
            speak("Enter the mobile number using keyboard where whatsapp message is " +
                  "to be sent")
            mobileNum = input("Enter here : " )
            mobileNum = mobileNum.replace(' ', '')
            mobileNum = "+91" + mobileNum
            
            speak("What message should I send")
            message = takeCommand() 
            
            currHour = datetime.datetime.now().hour
            currMinute = datetime.datetime.now().minute
            currMinute = currMinute + 2

            start_new_thread(messageWhatsAppFunction, ((mobileNum, message, currHour, currMinute)))


        if "email" in query : 
            try : 
                speak("Enter the email address using keyboard where mail is " +
                  "to be sent")
                mailID = input("Enter here : ")
                mailID = mailID.replace(' ', '')
                
                speak("What mail should I send")
                message = takeCommand() 

                sendEmail(mailID, message)
                speak("Requested email has been sent ...")
                
            except Exception as e:
                print (e)
                speak("Apoligies, I was not able to sent the requested mail ...")
        
        if "no" in query :
            speak("Thanks for calling me up, have a good rest of the day. Later ... ")
            sys.exit()
            
        speak("Do you have any other work ...")

if __name__ == "__main__" : 
    main()