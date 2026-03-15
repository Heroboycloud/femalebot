import pyttsx3,time,pyperclip
from win10toast import ToastNotifier
from datetime import datetime
import pyjokes

engine = pyttsx3.init('sapi5')
toast= ToastNotifier()
BOTNAME="Female bot"
# Set Rate
engine.setProperty('rate', 190)

# Set Volume
engine.setProperty('volume', 30.0)

# Set Voice (Female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


# Text to Speech Conversion
def speak(text):
    """Used to speak whatever text is passed to it"""

    engine.say(text)
    engine.runAndWait()


# Greet the user
def greet_user():
    """Greets the user according to the time"""
    
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good afternoon")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good Evening")
    speak(f"I am {BOTNAME}. I am efficient to help you")


def detectCopy():
    """ Keep saying the Copied text"""
    cv=pyperclip.paste()
    greet_user()
    speak(cv)
    

def save_to_file(text,file="newaudio.mp3"):
    """ Save the text to file """
    engine.save_to_file(text,file)
    speak(f"The text has been saved to {file}")


def say_date():
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
    speak(mydate)
    notify("Today Date: ",mydate)

def notify(title="Femalebot",text="Welcome to Femalebot"):
    toast.show_toast(title,text)


def say_time():
    """ Recites the date out for you to hear"""
    now= datetime.now()
    day=now.day # the day for example 12,23
    hour= now.hour  # converted to 12-hour format
    minutes= now.minute # the minute
    month= now.strftime('%B') # month like february
    season= now.strftime('%p') # either AM or PM
    Weekday= now.strftime('%A') # either monday or any day
    year= now.year # yup the year
    mytime=f"The time is {hour}{minutes}{season}"
    speak(mytime)


def say_joke():
    joke= pyjokes.get_joke()
    speak(joke)


def notify_joke():
    joke= pyjokes.get_joke()
    notify("Random joke: ",joke)


notify_joke()