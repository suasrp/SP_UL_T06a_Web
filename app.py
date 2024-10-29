import streamlit as st
from gtts import gTTS
import nltk
from nltk.corpus import wordnet
import io

nltk.download('wordnet')

# Updated list of words
words = [
    "abbreviate", "abnormality", "abode", "abrasion", "abundantly", "academic",
    # ... add all other words here ...
    "zealous", "zestfully"
]

# Create tests
def create_tests(words_list):
    tests = {}
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        filtered_words = [word for word in words_list if word.startswith(letter)]
        tests[letter] = filtered_words
    return tests

tests = create_tests(words)

class SpellingApp:
    def __init__(self):
        self.score = 0
        self.incorrect_words = set()
        self.current_word = None
        self.words_to_test = []
        self.current_index = 0

    def display_main_menu(self):
        st.title("Spelling Test")
        st.button("Start Test", on_click=self.select_test)
        st.button("View Words", on_click=self.view_words)

    def select_test(self):
        letter = st.selectbox("Select a letter for the test:", list(tests.keys()))
        self.words_to_test = tests[letter]
        self.current_index = 0
        self.score = 0
        self.start_test()

    def start_test(self):
        if self.current_index < len(self.words_to_test):
            self.current_word = self.words_to_test[self.current_index]
            st.write(f"Spell the word: **{self.current_word}**")
            self.play_audio(self.current_word)
            user_input = st.text_input("Your answer:", "")
            if st.button("Submit"):
                self.check_spelling(user_input)
        else:
            st.write(f"Test complete! Your score: {self.score} / {len(self.words_to_test)}")
            self.display_main_menu()

    def check_spelling(self, user_input):
        if user_input.lower() == self.current_word.lower():
            self.score += 1
            st.success("Correct!")
        else:
            self.incorrect_words.add(self.current_word)
            st.error(f"Incorrect! The correct spelling is: {self.current_word}")
        
        self.current_index += 1
        self.start_test()

    def play_audio(self, text):
        tts = gTTS(text=text, lang='en')
        audio_file = io.BytesIO()
        tts.save(audio_file)
        audio_file.seek(0)
        st.audio(audio_file, format='audio/mp3')

    def view_words(self):
        st.title("List of Words")
        for letter, word_list in tests.items():
            st.subheader(f"Words starting with '{letter.upper()}':")
            st.write(", ".join(word_list))
        st.button("Back to Main Menu", on_click=self.display_main_menu)

# Initialize the application
app = SpellingApp()
app.display_main_menu()
