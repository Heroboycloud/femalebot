import pyttsx3
import time
import pyperclip
from win10toast import ToastNotifier
from datetime import datetime
import pyjokes
import os,requests,sys
import  subprocess
import speech_recognition as sr
import winsound
from rich.console import Console
from dotenv import load_dotenv

class Femalebot:
    def __init__(self):
        load_dotenv()
        self.API_KEY= os.getenv("API_KEY")
        self.API_URL= os.getenv("API_URL")
        self.headers = {
    'Authorization': f'Bearer {self.API_KEY}',
    'Content-Type': 'application/json'
}
        
        self.engine = pyttsx3.init('sapi5')
        self.toast= ToastNotifier()
        self.console= Console()
        self.BOTNAME="Diana"
        self.recognizer = sr.Recognizer()
        self.listen_duration= 5
        # Set Rate
        self.engine.setProperty('rate', 190)
        # Set Volume
        self.engine.setProperty('volume', 30.0)
        # Set Voice (Female)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.speak("Hi, I am Diana, what can i do for you? ")

    def speak(self,text):
        self.engine.say(text)
        self.engine.runAndWait()

    def notify(self,title="Femalebot",text="Diana greets you"):
        self.toast.show_toast(title,text,duration=2)

    def say_date(self):
        """ Recites the date out for you to hear"""
        now= datetime.now()
        day=now.day # the day for example 12,23
        hour= now.hour  # converted to 12-hour format
        minutes= now.minute # the minute
        month= now.strftime('%B') # month like february
        season= now.strftime('%p') # either AM or PM
        Weekday= now.strftime('%A') # either monday or any day
        year= now.year # yup the year
        mydate= f"The date is {Weekday} {day},{month},{year}"
        self.speak(mydate)
        self.notify("Today Date: ",mydate)

    def say_time(self):
        """ Recites the date out for you to hear"""
        now= datetime.now()
        day=now.day # the day for example 12,23
        hour= now.hour  # converted to 12-hour format
        minutes= now.minute # the minute
        month= now.strftime('%B') # month like february
        season= now.strftime('%p') # either AM or PM
        Weekday= now.strftime('%A') # either monday or any day
        year= now.year # yup the year
        mytime=f"The time is {hour}:{minutes}{season}"
        self.speak(mytime)
        self.notify("Time:",mytime)

    def greet_user(self):
        """Greets the user according to the time"""
        
        hour = datetime.now().hour
        if (hour >= 6) and (hour < 12):
            self.speak(f"Good Morning")
        elif (hour >= 12) and (hour < 16):
            self.speak(f"Good afternoon")
        elif (hour >= 16) and (hour < 19):
            self.speak(f"Good Evening")
        self.speak(f"I am {self.BOTNAME}. I am efficient to help you")
        self.speak("Hi Azeez!! how was your day?")


    def run(self,command):
        command_result=os.system(command)
        if command_result > 0:
            self.console.print(f"[red]Error running command: {command}")
        return command_result
        
    def clipsave(self,text):
        return pyperclip.copy(text)


    def clipget(self):
        return pyperclip.paste()
    def say_joke(self):
        joke= pyjokes.get_joke()
        self.speak("Here is a computer joke..   \n\n"+ joke)
        self.speak("Not my best!! Was it funny?")


    def get_joke(self):
        joke= pyjokes.get_joke()
        return joke


    def notify_joke(self):
        joke= pyjokes.get_joke()
        self.notify("Random joke: ",joke)

    def listen(self,duration=10):
        try:
            self.console.clear()
            self.listen_duration= duration
            winsound.Beep(560,500)
            self.speak("Hi , Diana is listening!! i am here....")
            self.console.log("[green]Listening.....")
            with sr.Microphone() as source:
                audio_data = self.recognizer.record(source, duration=self.listen_duration)
                winsound.Beep(500, 500)
                self.speak("Translating.....")
                self.console.log("[blue]Recognizing...")
                text = self.recognizer.recognize_google(audio_data)
                translated_text= str(text.encode("utf-8"))
                self.speak(text)
                return text
        except:
            self.console.print("[yellow]Please connect to Internet...")
            self.speak("I cannot hear you!! Please Connect to the internet!!")
            return False


    def ask_ai(self,prompt_text="You are a smart virtual Assistant named Diana ",question="Hi Diana"):
        self.API_DATA = {
    "model": "deepseek/deepseek-chat",
    "messages": [{"role": "user", "content": question }]
}
        response = requests.post(self.API_URL, json=self.API_DATA, headers=self.headers)
        if response.status_code == 200:
            print(response.json())
            ai_message = response.json()['choices'][0]['message']['content']
            print(ai_message)
            self.speak(ai_message)
            self.API_DATA["messages"].append(response.json()['choices'][0]['message'])
    
        else:
           self.console.print(f"[bold red]Oops! Something went wrong. Status code: {response.status_code}")
           self.console.print(f"[red]Error details: {response.text}")
           self.speak("Error answering your request")
        
