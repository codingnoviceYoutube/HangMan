import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

class HangmanGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.word = "hangman" # the word to guess
        self.guesses = "" # the letters that have been guessed so far
        self.max_incorrect_guesses = 6 # maximum number of incorrect guesses allowed
        self.incorrect_guesses = 0 # number of incorrect guesses made so far
        self.display_word = self.get_display_word() # the word to display to the user
        self.status_label = Label(text=self.display_word) # label to display the status of the game
        self.add_widget(self.status_label)
        # create a text input box for the user to enter their guess
        self.input_box = TextInput(multiline=False)
        self.add_widget(self.input_box)
        # create a submit button
        self.submit_button = Button(text="Submit", on_press=self.handle_guess)
        self.add_widget(self.submit_button)
        self.hangman_label = Label(text="") # label to display the hangman figure
        self.add_widget(self.hangman_label)
        self.lives_label = Label(text=f"Lives remaining: {self.max_incorrect_guesses - self.incorrect_guesses}")
        self.add_widget(self.lives_label)
        self.guesses_label = Label(text=f"Previous guesses: {self.guesses}")
        self.add_widget(self.guesses_label)

    def handle_guess(self, button):
        """Handles a guess made by the user."""
        guess = self.input_box.text.lower()
        if guess == self.word:
            # the guess is correct
            self.status_label.text = "You win!"
        elif len(guess) == 1 and guess not in self.guesses:
            # the guess is a single letter
            self.guesses += guess
            if guess in self.word:
                # the letter is in the word
                self.display_word = self.get_display_word()
                self.status_label.text = self.display_word
                if self.display_word == self.word:
                    # the word has been guessed, so the game is won
                    self.status_label.text = "You win!"
            else:
                # the letter is not in the word
                self.incorrect_guesses += 1
                self.display_word = self.get_display_word()
                self.status_label.text = self.display_word
                if self.incorrect_guesses == self.max_incorrect_guesses:
                    # the maximum number of incorrect guesses has been reached, so the game is lost
                    self.status_label.text = "You lose."
            # update the hangman figure
            self.update_hangman_figure()
        else:
            # the guess is not a single letter or has already been guessed
            self.status_label.text = "Invalid guess. Please enter a single letter or the full word."
        # clear the input box
        self.input_box.text = ""
        # update the lives and guesses labels
        self.lives_label.text = f"Lives remaining: {self.max_incorrect_guesses - self.incorrect_guesses}"
        self.guesses_label.text = f"Previous guesses: {self.guesses}"

    def update_hangman_figure(self):
        """Updates the hangman figure label based on the number of incorrect guesses made."""
        # create a list of strings representing the hangman figure at each stage of the game
        hangman_figures = [
            "",
            " o",
            " o\n/",
            " o\n/|",
            " o\n/|\\",
            " o\n/|\\\n/",
            " o\n/|\\\n/ \\",
        ]
        # get the appropriate string from the list based on the number of incorrect guesses
        hangman_figure = hangman_figures[self.incorrect_guesses]
        # update the hangman figure label with the new figure
        self.hangman_label.text = hangman_figure

    def get_display_word(self):
        """Returns the word to display to the user, with unguessed letters replaced with underscores."""
        display_word = ""
        for letter in self.word:
            if letter in self.guesses:
                # the letter has been guessed, so add it to the display word
                display_word += letter
            else:
                # the letter has not been guessed, so add an underscore to the display word
                display_word += "_"
        return display_word

class HangmanApp(App):
    def build(self):
        game = HangmanGame()
        return game

if __name__ == "__main__":
    HangmanApp().run()
