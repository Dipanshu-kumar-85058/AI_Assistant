from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivymd.uix.spinner import MDSpinner
import threading
from voice import listen_for_command, speak
from assistant import process_input
from kivymd.app import MDApp


# Set Dark Theme
Window.clearcolor = (0.1, 0.1, 0.1, 1)

class AIAssistantGUI(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"  
        self.theme_cls.primary_palette = "BlueGray" 

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Logo Image
        self.logo = Image(source='logo.png', size_hint_y=None, height=100)

        # AI Response Label (Above Input)
        self.response_label = Label(
            text="Hello! How can I assist you?",
            size_hint_y=None,
            height=80,
            color=(1, 1, 1, 1)
        )

        # User Input Field
        self.text_input = TextInput(
            hint_text="Type your command here...",
            multiline=False,
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1)
        )

        # Buttons
        self.ask_button = Button(
            text="Ask",
            size_hint_y=None,
            height=50,
            background_color=(0.1, 0.8, 0.1, 1)
        )
        self.speak_button = Button(
            text="Speak",
            size_hint_y=None,
            height=50,
            background_color=(0.3, 0.6, 1, 1)
        )
        self.listen_button = Button(
            text="Listen",
            size_hint_y=None,
            height=50,
            background_color=(0.8, 0.3, 0.3, 1)
        )

        # **Graphical Spinning Loader**
        self.spinner = MDSpinner(
            size_hint=(None, None),
            size=(50, 50),
            active=true,
            color=(1, 1, 1, 1) 
        )

        # Bind Buttons
        self.ask_button.bind(on_press=self.on_ask)
        self.speak_button.bind(on_press=self.on_speak)
        self.listen_button.bind(on_press=self.on_listen)

        # Add widgets to layout
        layout.add_widget(self.logo)
        layout.add_widget(self.response_label)
        layout.add_widget(self.text_input)
        layout.add_widget(self.ask_button)
        layout.add_widget(self.speak_button)
        layout.add_widget(self.listen_button)
        layout.add_widget(self.spinner) 

        return layout

    def on_ask(self, instance):
        """Handles text-based input when 'Ask' button is pressed."""
        text = self.text_input.text.strip()
        if text:
            self.show_loader()
            threading.Thread(target=self.process_and_update, args=(text, False)).start()
            self.text_input.text = ""
            
    def on_speak(self, instance):
        """Handles typed input & speaks the response."""
        text = self.text_input.text.strip()
        if text:
            self.show_loader()
            threading.Thread(target=self.process_speak_update, args=(text,)).start()
            self.text_input.text = ""

    def on_listen(self, instance):
        """Handles voice input when 'Listen' button is pressed."""
        self.show_loader()
        threading.Thread(target=self.listen_and_update).start()

    def show_loader(self):
        """Shows the loading spinner and updates UI."""
        self.spinner.active = True
        self.response_label.text = "Processing..."

    def hide_loader(self, response):
        """Hides the loader and updates AI response."""
        Clock.schedule_once(lambda dt: self.update_label(response), 0)

    def update_label(self, response):
        """Updates AI response label and hides spinner."""
        self.spinner.active = False
        self.response_label.text = response

    def process_and_update(self, text):
        """Processes text input and updates UI."""
        response = process_input(text)
        self.hide_loader(response)

    def process_speak_update(self, text):
        """Processes text, updates UI, and speaks the response."""
        response = process_input(text)
        speak(response)
        self.hide_loader(response)

    def listen_and_update(self):
        """Processes voice command, updates UI, and speaks response."""
        text = listen_for_command()
        if text:
            response = process_input(text)
            speak(response)
            self.hide_loader(response)
        else:
            self.hide_loader("I couldn't hear you. Please try again.")

if __name__ == "__main__":
    AIAssistantGUI().run()
