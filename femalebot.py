import pyttsx3
import time
import pyperclip
from win10toast import ToastNotifier
from datetime import datetime
import pyjokes
import os
import requests
import sys
import subprocess
import speech_recognition as sr
import winsound
from rich.console import Console
from rich.panel import Panel
from dotenv import load_dotenv
import json
import webbrowser
import wikipedia
import psutil
import platform
import re
import random



class Femalebot:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.API_KEY = os.getenv("API_KEY")
        self.API_URL = os.getenv("API_URL")
        
        if not self.API_KEY or not self.API_URL:
            print("Warning: API credentials not found in .env file")
            self.API_KEY = ""
            self.API_URL = ""
        
        self.headers = {
            'Authorization': f'Bearer {self.API_KEY}',
            'Content-Type': 'application/json'
        }
        
        # Initialize components
        self.setup_voice_engine()
        self.toast = ToastNotifier()
        
        # Configure console to handle Unicode
        self.console = Console(color_system="auto", force_terminal=True)
        
        self.BOTNAME = "Diana"
        self.recognizer = sr.Recognizer()
        self.listen_duration = 5
        self.is_listening = False
        self.conversation_history = []
        
        # Greet user
        self.greet_user()

    def setup_voice_engine(self):
        """Setup text-to-speech engine with proper error handling"""
        try:
            self.engine = pyttsx3.init('sapi5')
            # Set Rate
            self.engine.setProperty('rate', 190)
            # Set Volume
            self.engine.setProperty('volume', 0.9)
            # Set Voice (Female)
            voices = self.engine.getProperty('voices')
            if len(voices) > 1:
                self.engine.setProperty('voice', voices[1].id)
            else:
                self.engine.setProperty('voice', voices[0].id)
        except Exception as e:
            print(f"Error initializing voice engine: {e}")
            self.engine = None

    def clean_text_for_console(self, text):
        """Remove or replace emojis and special characters that might cause console errors"""
        # Replace common emojis with text representations
        emoji_map = {
            '🚀': '[rocket]',
            '✨': '[sparkles]',
            '🌟': '[star]',
            '💡': '[idea]',
            '🔍': '[search]',
            '📝': '[note]',
            '✅': '[check]',
            '❌': '[cross]',
            '⚠️': '[warning]',
            '🔔': '[bell]',
            '🤖': '[bot]',
            '🎤': '[mic]',
            '💻': '[computer]',
            '📱': '[phone]',
            '🌐': '[web]',
            '🔗': '[link]',
            '📊': '[chart]',
            '🔧': '[tool]',
            '🎯': '[target]',
            '💬': '[chat]',
            '👋': '[wave]',
            '👍': '[thumbsup]',
            '👎': '[thumbsdown]',
            '🎉': '[party]',
            '🔥': '[fire]',
            '⭐': '[star]',
            '❤️': '[heart]',
            '💔': '[brokenheart]'
        }
        
        for emoji, replacement in emoji_map.items():
            text = text.replace(emoji, replacement)
        
        # Remove any other non-ASCII characters that might cause issues
        text = text.encode('ascii', 'ignore').decode('ascii')
        
        return text

    def speak(self, text):
        """Speak text with error handling"""
        if self.engine:
            try:
                # Clean text for speech (remove emojis but keep words)
                clean_text = text.replace('[rocket]', 'rocket').replace('[sparkles]', 'sparkles')
                clean_text = clean_text.replace('[bot]', 'bot').replace('[mic]', 'microphone')
                clean_text = re.sub(r'\[.*?\]', '', clean_text)  # Remove any remaining brackets
                self.engine.say(clean_text)
                self.engine.runAndWait()
            except Exception as e:
                self.console.print(f"[red]Speech error: {e}")
                print(f"Diana: {text}")
        else:
            print(f"Diana: {text}")

    def notify(self, title="Diana", text="How can I help you?"):
        """Show desktop notification"""
        try:
            # Clean text for notification
            clean_text = self.clean_text_for_console(text)
            clean_title = self.clean_text_for_console(title)
            self.toast.show_toast(clean_title, clean_text, duration=3, threaded=True)
        except Exception as e:
            self.console.print(f"[yellow]Notification error: {e}")

    def say_date(self):
        """Recites the date out for you to hear"""
        now = datetime.now()
        day = now.day
        month = now.strftime('%B')
        weekday = now.strftime('%A')
        year = now.year
        
        mydate = f"Today is {weekday}, {month} {day}, {year}"
        self.speak(mydate)
        self.notify("Current Date", mydate)
        return mydate

    def say_time(self):
        """Recites the time out for you to hear"""
        now = datetime.now()
        hour = now.strftime('%I').lstrip('0')  # 12-hour format without leading zero
        minutes = now.strftime('%M')
        period = now.strftime('%p')
        
        mytime = f"The time is {hour}:{minutes} {period}"
        self.speak(mytime)
        self.notify("Current Time", mytime)
        return mytime

    def greet_user(self):
        """Greets the user according to the time"""
        hour = datetime.now().hour
        
        if 6 <= hour < 12:
            greeting = "Good Morning"
        elif 12 <= hour < 17:
            greeting = "Good Afternoon"
        elif 17 <= hour < 21:
            greeting = "Good Evening"
        else:
            greeting = "Hello"
        
        welcome_msg = f"{greeting}! I am {self.BOTNAME}, your virtual assistant. How can I help you today?"
        self.speak(welcome_msg)
        self.notify(f"{self.BOTNAME} is ready", welcome_msg)


    def change_voice(self):
        id=[0,1]
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[random.choice(id)].id)
        self.speak("voice changed...")





    def run_command(self, command):
        """Run system command safely"""
        try:
            if command.startswith("start "):
                os.system(command)
                self.speak(f"Opening {command[6:]}")
                return True
            else:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    return result.stdout
                else:
                    self.console.print(f"[red]Command error: {result.stderr}")
                    return False
        except Exception as e:
            self.console.print(f"[red]Error running command: {e}")
            return False

    def clip_save(self, text):
        """Save text to clipboard"""
        try:
            pyperclip.copy(text)
            self.speak("Text copied to clipboard")
            return True
        except Exception as e:
            self.console.print(f"[red]Clipboard error: {e}")
            return False

    def clip_get(self):
        """Get text from clipboard"""
        try:
            return pyperclip.paste()
        except Exception as e:
            self.console.print(f"[red]Clipboard error: {e}")
            return ""

    def tell_joke(self):
        """Tell a computer joke"""
        try:
            joke = pyjokes.get_joke()
            self.speak("Here's a joke for you:")
            
            # Clean joke for console display
            clean_joke = self.clean_text_for_console(joke)
            self.console.print(Panel(clean_joke, title="Joke", border_style="yellow"))
            
            self.speak(joke)
            self.notify("Random Joke", joke)
            return joke
        except Exception as e:
            self.console.print(f"[red]Joke error: {e}")
            self.speak("Sorry, I couldn't fetch a joke right now.")
            return None

    def listen(self, duration=7):
        """Listen for voice input"""
        try:
            self.console.clear()
            self.console.print("[bold green]Listening... (speak now)[/bold green]")
            winsound.Beep(800, 200)
            
            with sr.Microphone() as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio_data = self.recognizer.listen(source, timeout=duration, phrase_time_limit=10)
                
                winsound.Beep(600, 200)
                self.console.print("[bold blue]Processing...[/bold blue]")
                
                # Recognize speech
                text = self.recognizer.recognize_google(audio_data)
                self.console.print(f"[bold green]You said:[/bold green] {text}")
                return text.lower()
                
        except sr.WaitTimeoutError:
            self.console.print("[yellow]No speech detected[/yellow]")
            return ""
        except sr.UnknownValueError:
            self.console.print("[yellow]Could not understand audio[/yellow]")
            return ""
        except sr.RequestError:
            self.console.print("[red]Internet connection required for speech recognition[/red]")
            self.speak("Please check your internet connection")
            return ""
        except Exception as e:
            self.console.print(f"[red]Listening error: {e}[/red]")
            return ""
    def save_to_file(self,message):
        filename= secrets.token_hex(5) + ".md"
        with open(filename,"wt") as fd:
             fd.write(message)
             self.speak(f"saved to {filename}")
    def ask_ai(self, question):
        """Ask AI for assistance - FIXED UNICODE ERROR"""
        if not self.API_KEY or not self.API_URL:
            self.speak("AI features are not configured. Please set up API credentials.")
            return None
        
        try:
            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": question})
            
            # Prepare API data
            api_data = {
                "model": "deepseek/deepseek-chat",
                "messages": self.conversation_history[-5:]  # Keep last 5 messages for context
            }
            
            self.console.print("[bold cyan]Thinking...[/bold cyan]")
            
            response = requests.post(
                self.API_URL, 
                json=api_data, 
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_message = result['choices'][0]['message']['content']
                
                # Add to conversation history
                self.conversation_history.append({"role": "assistant", "content": ai_message})
                
                # Clean the message for console display (remove emojis)
                clean_message = self.clean_text_for_console(ai_message)
                
                # Display response
                self.console.print(Panel(clean_message, title="Diana", border_style="cyan"))
                
                # Speak response (with cleaned text)
                self.speak("Do you want me to read it or save it")
                com= self.listen(6)
                if "read" in com:
                   self.speak(ai_message)
                elif "save" in com:
                   self.save_to_file(ai_message)
                else:
                    pass
                
                return ai_message
            else:
                self.console.print(f"[red]API Error {response.status_code}: {response.text}[/red]")
                self.speak("I'm having trouble connecting to my AI services.")
                return None
                
        except requests.exceptions.Timeout:
            self.console.print("[red]Request timed out[/red]")
            self.speak("The request timed out. Please try again.")
        except requests.exceptions.ConnectionError:
            self.console.print("[red]Connection error[/red]")
            self.speak("I cannot connect to the internet. Please check your connection.")
        except UnicodeEncodeError as e:
            self.console.print(f"[red]Unicode encoding error: {e}[/red]")
            # Fallback: Try to display without special characters
            try:
                if 'ai_message' in locals():
                    # Remove all non-ASCII characters as last resort
                    ascii_message = ai_message.encode('ascii', 'ignore').decode('ascii')
                    self.console.print(Panel(ascii_message, title="Diana", border_style="cyan"))
                    self.speak(ai_message)
            except:
                self.speak("I received a response but couldn't display it properly.")
        except Exception as e:
            self.console.print(f"[red]AI error: {e}[/red]")
            self.speak("Sorry, I encountered an error processing your request.")
        
        return None

    def get_system_info(self):
        """Get system information"""
        info = {
            "System": platform.system(),
            "Node Name": platform.node(),
            "Release": platform.release(),
            "Version": platform.version(),
            "Machine": platform.machine(),
            "Processor": platform.processor(),
            "CPU Usage": f"{psutil.cpu_percent()}%",
            "Memory Usage": f"{psutil.virtual_memory().percent}%"
        }
        
        info_text = "System Information:\n"
        for key, value in info.items():
            info_text += f"  {key}: {value}\n"
        
        self.console.print(Panel(info_text, title="System Info", border_style="green"))
        
        # Speak summary
        self.speak(f"Your system is running on {info['System']} with {info['CPU Usage']} CPU usage")
        return info

    def open_application(self, app_name):
        """Open common applications"""
        apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "browser": "start chrome",
            "chrome": "start chrome",
            "firefox": "start firefox",
            "edge": "start msedge",
            "word": "start winword",
            "excel": "start excel",
            "powershell": "start powershell",
            "cmd": "start cmd",
            "explorer": "explorer"
        }
        
        app_name = app_name.lower()
        for key, command in apps.items():
            if key in app_name:
                self.run_command(command)
                self.speak(f"Opening {key}")
                return True
        
        # Try to open by name
        try:
            os.system(f"start {app_name}")
            self.speak(f"Trying to open {app_name}")
            return True
        except:
            self.speak(f"Sorry, I don't know how to open {app_name}")
            return False

    def process_command(self, command):
        """Process and execute user commands"""
        if not command:
            return True
        
        command = command.lower()
        
        # Date and time
        if any(word in command for word in ["date", "day", "today"]):
            self.say_date()
        
        elif any(word in command for word in ["time", "clock"]):
            self.say_time()

        elif any(word in command for word in ["voice","change"]):
             self.change_voice()
        # Jokes
        elif any(word in command for word in ["joke", "funny", "laugh"]):
            self.tell_joke()
        
        # System info
        elif any(word in command for word in ["system", "computer info", "pc info"]):
            self.get_system_info()
        
        # Clipboard
        elif "copy" in command and "clipboard" in command:
            text = command.replace("copy", "").replace("to clipboard", "").strip()
            if text:
                self.clip_save(text)
        
        elif "paste" in command or "clipboard" in command:
            text = self.clip_get()
            if text:
                self.speak(f"Clipboard contains: {text}")
            else:
                self.speak("Clipboard is empty")
        
        # Open applications
        elif command.startswith("open "):
            app = command[5:]
            self.open_application(app)
        
        # Search Wikipedia
        elif "wikipedia" in command or "wiki" in command:
            search_term = command.replace("wikipedia", "").replace("wiki", "").strip()
            if search_term:
                self.search_wikipedia(search_term)
        
        # Search web
        elif "search for" in command or "google" in command:
            search_term = command.replace("search for", "").replace("google", "").strip()
            if search_term:
                webbrowser.open(f"https://www.google.com/search?q={search_term}")
                self.speak(f"Searching Google for {search_term}")
        
        # YouTube
        elif "youtube" in command:
            search_term = command.replace("youtube", "").strip()
            if search_term:
                webbrowser.open(f"https://www.youtube.com/results?search_query={search_term}")
                self.speak(f"Searching YouTube for {search_term}")
            else:
                webbrowser.open("https://youtube.com")
                self.speak("Opening YouTube")
        
        # Exit
        elif any(word in command for word in ["exit", "quit", "bye", "goodbye"]):
            self.speak("Goodbye! Have a great day!")
            return False
        
        # Default to AI
        else:
            self.ask_ai(command)
        
        return True

    def search_wikipedia(self, query):
        """Search Wikipedia"""
        try:
            self.speak(f"Searching Wikipedia for {query}")
            result = wikipedia.summary(query, sentences=2)
            self.console.print(Panel(result, title=f"Wikipedia: {query}", border_style="blue"))
            self.speak(result)
        except wikipedia.exceptions.DisambiguationError as e:
            self.speak(f"Multiple results found. Please be more specific.")
        except wikipedia.exceptions.PageError:
            self.speak(f"No Wikipedia page found for {query}")
        except Exception as e:
            self.console.print(f"[red]Wikipedia error: {e}[/red]")

    def run(self):
        """Main execution loop"""
        self.console.print(Panel.fit(
            f"[bold cyan]{self.BOTNAME} Virtual Assistant[/bold cyan]\n"
            "[green]Commands: time, date, joke, system info, open [app], search, exit[/green]",
            title="Welcome"
        ))
        
        running = True
        while running:
            try:
                # Get input (voice or text)
                self.console.print("\n[bold cyan]Choose input method:[/bold cyan]")
                self.console.print("[1] Voice input")
                self.console.print("[2] Text input")
                self.console.print("[3] Exit")
                
                choice = input("Enter choice (1/2/3): ").strip()
                
                if choice == "1":
                    command = self.listen(7)
                    self.speak("Command received successfully")
                elif choice == "2":
                    command = input("You: ").strip().lower()
                elif choice == "3":
                    self.speak("Goodbye!")
                    break
                else:
                    self.console.print("[red]Invalid choice[/red]")
                    continue
                
                if command:
                    running = self.process_command(command)
                else:
                    self.console.print("[yellow]No command detected[/yellow]")
                    
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Interrupted by user[/yellow]")
                self.speak("Goodbye!")
                break
            except UnicodeEncodeError as e:
                self.console.print(f"[red]Unicode error: {e}. Try using text input mode.[/red]")
            except Exception as e:
                self.console.print(f"[red]Unexpected error: {e}[/red]")

if __name__ == "__main__":
    # Create .env file template if it doesn't exist
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write("# API Configuration\n")
            f.write("API_KEY=your_api_key_here\n")
            f.write("API_URL=https://openrouter.ai/api/v1/chat/completions\n")
        print("Created .env template. Please add your API credentials.")
    
    # Set console encoding for Windows
    if sys.platform == "win32":
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    
    # Run the bot
    bot = Femalebot()
    bot.run()
