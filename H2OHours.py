from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import random
import requests

class H2OHours(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # H2O Image
        self.window.add_widget(Image(source="water.png"))
        # Reminder label
        self.reminder = Label(
                        text="How many minutes until reminder to drink water?",
                        font_size=18,
                        color='#00FFCE'
                        )
        self.window.add_widget(self.reminder)
        # Text input
        self.input = TextInput(
                        multiline=False,
                        padding_y=(20, 20),
                        size_hint=(1, 0.5)
                        )

        self.window.add_widget(self.input)
        # Button widget
        self.button = Button(
                        text="SET",
                        size_hint=(1, 0.5),
                        bold=True,
                        background_color='#00FFCE'
                        )
        self.window.add_widget(self.button)
        # Setting the reminder
        self.button.bind(on_press=self.callback)

        # Displaying the quotes
        self.quotesLabel = Label(
            text="",
            font_size=20,
            color='#00FFCE'
        )
        self.window.add_widget(self.quotesLabel)

        return self.window

    def callback(self, event):
        reminder_text = self.input.text
        try:
            minutes = int(reminder_text)
            if minutes <= 0:
                raise ValueError()
        except ValueError:
            self.reminder.text = "Please enter a valid positive number of minutes."
            return

        self.reminder.text = "You will be reminded in " + reminder_text + " minutes!"
        Clock.schedule_once(self.remind_user, minutes * 60)
        self.getQuotes()

    def remind_user(self, dt):
        # Reset the reminder text
        self.reminder.text = "How many minutes until reminder to drink water?"
        # Load and play the sound asynchronously
        sound = SoundLoader.load('reminder_sound.wav')
        if sound:
            sound.play()
    
    def getQuotes(self):
        try:
            response = requests.get("https://type.fit/api/quotes")
            if response.status_code == 200:
                quotes = response.json()
                random_quote = random.choice(quotes)
                quoteText = random_quote['text']
                # Weird text after the author's name, so split and take the first portion
                quoteAuthor = random_quote['author'].split(',')[0]
                self.quotesLabel.text = "\"" + str(quoteText) + "\"" + "\n" + "- " + str(quoteAuthor)
            else:
                self.quotesLabel.text = "Failed to fetch quotes."
        except requests.exceptions.RequestException:
            self.quotesLabel.text = "Failed to connect to the quotes API."

if __name__ == "__main__":
    H2OHours().run()