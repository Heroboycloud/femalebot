import speech_recognition as sr
import sys
import pytgpt.phind as ph
import femalebot 

bot= ph.PHIND()
#read duration from the arguments
#duration = int(sys.argv[1])
duration=5
# initialize the recognizer
r = sr.Recognizer()
print("Please talk")

try:
	with sr.Microphone() as source:
    # read the audio data from the default microphone
         audio_data = r.record(source, duration=duration)
         print("Recognizing...")
    # convert speech to text
         text = r.recognize_google(audio_data)
         print(text)
         result= bot.chat(str(text.encode("utf-8")))
         print(result)
         femalebot.speak(result)
except:
	femalebot.speak("Connect to the Internet ....")
	print("Internet not connected!!!")