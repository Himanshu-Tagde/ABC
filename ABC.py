import streamlit as st
from gtts import gTTS
import os
import speech_recognition as sr

import random
from PIL import Image

from time import time
from random import randint, shuffle
from datetime import datetime
import pickle
import bisect



# Path to images directory
vegetable_images_path = r'E:\spacece\project 2\stremlit\vegetable_images'

# List of vegetable image filenames (ensure these images exist in the folder)
vegetable_images = [
    'brinjal.jpg', 'cabbage.jpg', 'potato.jpg', 'tomato.jpg',
    'capsicum.jpg', 'onion.jpg', 'carrot.jpg', 'radish.jpg'
]



# Function to add a persistent background image
def add_bg_image(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url({image_url});
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        button {{
            background-color: #4CAF50;
            border-radius: 10px;
            padding: 10px;
            font-size: 18px;
            color: white;
            border: none;
            cursor: pointer;
        }}
        button:hover {{
            background-color: #45a049;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Function to generate text-to-speech audio dynamically
def generate_audio(text, filename):
    tts = gTTS(text)
    tts.save(filename)

# Function to recognize speech in real-time
def recognize_live_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening... Speak now!")
        try:
            audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError as e:
            return f"Could not request results; {e}"
        except Exception as e:
            return f"Error: {e}"

# Function to check if the user spoke the correct word for the image shown
def check_spoken_word(correct_word):
    st.write(f"Please speak the word that corresponds to the image shown.")
    spoken_text = recognize_live_speech()
    st.write(f"**You said:** {spoken_text}")
    if spoken_text.strip().lower() == correct_word.lower():
        st.success(f"Correct! 🎉 You correctly identified the word '{correct_word}'.")
    else:
        st.error(f"Incorrect! ❌ The correct word is '{correct_word}'.")

# Function to check the spelling of the word
def check_spelling_word(correct_word):
    st.write(f"Please spell the word '{correct_word}' by speaking each letter.")
    spoken_text = recognize_live_speech()
    st.write(f"**You said:** {spoken_text}")
    if spoken_text.strip().lower() == correct_word.lower():
        st.success(f"Correct spelling! 🎉 You spelled the word '{correct_word}' correctly.")
    else:
        st.error(f"Incorrect spelling. ❌ The correct spelling is '{correct_word}'.")

# List of letters, words, and image URLs from A to Z
letters = [
    ("A", "Apple", "https://upload.wikimedia.org/wikipedia/commons/1/15/Red_Apple.jpg"),
    ("B", "Ball", "https://upload.wikimedia.org/wikipedia/commons/7/7a/Basketball.png"),
    ("C", "Cat", "https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg"),
    ("D", "Dog", "https://upload.wikimedia.org/wikipedia/commons/d/d9/Collage_of_Nine_Dogs.jpg"),
    ("E", "Elephant", "https://upload.wikimedia.org/wikipedia/commons/3/37/African_Bush_Elephant.jpg"),
    ("F", "Fish", "https://upload.wikimedia.org/wikipedia/commons/2/24/Fish_icon.svg"),
    ("G", "Giraffe", "https://upload.wikimedia.org/wikipedia/commons/e/ec/Giraffe_picture.jpg"),
    ("H", "Hat", "https://upload.wikimedia.org/wikipedia/commons/c/cc/Red_hat.jpg"),
    ("I", "Ice Cream", "https://upload.wikimedia.org/wikipedia/commons/9/91/Ice_cream_cone.jpg"),
    ("J", "Jug", "https://upload.wikimedia.org/wikipedia/commons/2/2a/Jug_icon.png"),
    ("K", "Kite", "https://upload.wikimedia.org/wikipedia/commons/0/04/Kite_icon.svg"),
    ("L", "Lion", "https://upload.wikimedia.org/wikipedia/commons/a/a0/Lion_icon.png"),
    ("M", "Monkey", "https://upload.wikimedia.org/wikipedia/commons/5/56/Monkey_icon.png"),
    ("N", "Nest", "https://upload.wikimedia.org/wikipedia/commons/a/a7/Nest_icon.svg"),
    ("O", "Orange", "https://upload.wikimedia.org/wikipedia/commons/4/43/Orange_icon.svg"),
    ("P", "Pencil", "https://upload.wikimedia.org/wikipedia/commons/3/37/Pencil_icon.svg"),
    ("Q", "Queen", "https://upload.wikimedia.org/wikipedia/commons/d/d4/Queen_icon.svg"),
    ("R", "Rainbow", "https://upload.wikimedia.org/wikipedia/commons/7/7e/Rainbow_icon.png"),
    ("S", "Sun", "https://upload.wikimedia.org/wikipedia/commons/a/a3/Sun_icon.svg"),
    ("T", "Tree", "https://upload.wikimedia.org/wikipedia/commons/1/17/Tree_icon.png"),
    ("U", "Umbrella", "https://upload.wikimedia.org/wikipedia/commons/7/74/Umbrella_icon.png"),
    ("V", "Violin", "https://upload.wikimedia.org/wikipedia/commons/d/df/Violin_icon.svg"),
    ("W", "Whale", "https://upload.wikimedia.org/wikipedia/commons/2/2f/Whale_icon.png"),
    ("X", "Xylophone", "https://upload.wikimedia.org/wikipedia/commons/e/ef/Xylophone_icon.png"),
    ("Y", "Yarn", "https://upload.wikimedia.org/wikipedia/commons/0/04/Yarn_icon.svg"),
    ("Z", "Zebra", "https://upload.wikimedia.org/wikipedia/commons/c/c6/Zebra_icon.svg"),
]

# Initialize session state for current word index
if "current_index" not in st.session_state:
    st.session_state["current_index"] = 0

# Add Title
st.title("ABC Learning")

# Dropdown to choose an activity
option = st.selectbox("Choose an activity:", ["Select", "Learn ABC", "Play Counting Game","Maths for kids", "Progress Report"])

# "Learn ABC" Section
if option == "Learn ABC":
    st.subheader("Learn ABC")
    current_index = st.session_state["current_index"]

    # Display current word and image
    letter, word, image_url = letters[current_index]
    st.image(image_url, caption=f"{letter} for {word}", width=300)
    st.write(f"### **{word}**")

    # Text-to-speech button (Listen to the word)
    audio_file = f"{word.lower()}_audio.mp3"
    if not os.path.exists(audio_file):
        generate_audio(word, audio_file)
    if st.button("🔊 Listen to the word", key="listen_word"):
        st.audio(audio_file)

    # Speech recognition button to check if the user spoke the word correctly
    if st.button("🎤 Speak the word", key="speak_word"):
        check_spoken_word(word)

    # Button to check spelling of the word
    if st.button("🔤 Spell the word", key="spell_word"):
        check_spelling_word(word)

    # Next button to move to the next letter
    if st.button("Next", key="next"):
        st.session_state["current_index"] = (current_index+1) % len(letters)

# "Play Counting Game" Section
elif option == "Play Counting Game":
    # Function to display images and ask user to count the vegetables
    def count_vegetables(difficulty='easy'):
        if 'selected_images' not in st.session_state or 'options' not in st.session_state:
            # Determine the number of images based on the selected difficulty
            num_images = random.randint(1, 5) if difficulty == 'easy' else random.randint(6, 10)
            
            # Select random images
            selected_images = random.sample(vegetable_images, num_images)

            # Store the selected images and their count in session state
            st.session_state.selected_images = selected_images
            st.session_state.correct_count = len(selected_images)

            # Generate 4 unique options (including the correct one)
            options = {st.session_state.correct_count}
            while len(options) < 4:
                random_option = st.session_state.correct_count + random.randint(-1, 2)
                options.add(random_option)

            st.session_state.options = list(options)

        # Display the selected vegetable images in a row
        st.subheader("Guess how many vegetables you see:")
        cols = st.columns(len(st.session_state.selected_images))  # Create columns for each image
        image_paths = [os.path.join(vegetable_images_path, img) for img in st.session_state.selected_images]
        
        for i, image_path in enumerate(image_paths):
            with cols[i]:
                st.image(image_path, width=150)  # Resize each image to fit the columns

        correct_count = st.session_state.correct_count

        # Display options as radio buttons for user to select
        selected_option = st.radio(
            "How many vegetables do you see in the above images?", 
            st.session_state.options, 
            key=f"radio_button_{str(st.session_state.selected_images)}_{st.session_state.correct_count}"  # Unique key with images and count
        )

        # Handle the user's response when they click 'Submit'
        if st.button('Submit'):
            if selected_option == correct_count:
                st.success(f"Correct! There are {correct_count} vegetables!")
            else:
                st.error(f"Incorrect. There are {correct_count} vegetables. Try again!")

        # Continue button to generate a new question
        if st.button('Next Question'):
            # Clear the session state for a new question
            st.session_state.pop('selected_images', None)
            st.session_state.pop('options', None)
            st.session_state.pop('correct_count', None)
            count_vegetables(difficulty=difficulty)  # Regenerate new question

    # Main function to select difficulty level and start the game
    def select_difficulty():
        st.markdown("""
            Welcome to the Vegetable Counting Game! 🥕🥔🍅
            Your goal is to count how many vegetables are shown in the images.
        """)

        # Add Quit button
        if st.button("Quit"):
            st.warning("You have exited the game. Thank you for playing!")
            st.stop()  # Stops execution of further code

        difficulty = st.radio("Select Difficulty Level", ["Easy", "Medium"], key="difficulty_radio")
        count_vegetables(difficulty=difficulty.lower())

    # Streamlit app execution starts here
    st.title("Vegetable Counting Game")
    st.markdown("### Can you count all the vegetables?")

    # Run the game
    select_difficulty()

 
#Maths for kids
elif option == "Maths for kids":
   
       
        # Constants
        NTIMES = 10
        SUBTRACTION = True
        LO = 0
        HI = 10
        HIGHSCORE_FNAME = "highscores"

        # HighScores Class
        class HighScores:
            def __init__(self):
                self.scores = []
                self.num_scores = 10

            def update(self, score):
                """Add a score to the list of high scores.
                Return True if this score is among the top scores, otherwise False.
                """
                if len(self.scores) < self.num_scores:
                    self.scores.append(score)
                    self.scores.sort()
                    return True
                index = bisect.bisect(self.scores, score)
                if index < self.num_scores:
                    self.scores.insert(index, score)
                    self.scores.pop()
                    return True
                return False

            def __str__(self):
                return "\n".join([f"{i + 1:2d}) {score:.2f} sec" for i, score in enumerate(self.scores)])

        # Helper Functions
        def load_scores():
            try:
                with open(HIGHSCORE_FNAME, 'rb') as f:
                    return pickle.load(f)
            except FileNotFoundError:
                return HighScores()


        def save_scores(scores):
            with open(HIGHSCORE_FNAME, 'wb') as f:
                pickle.dump(scores, f)


        def generate_question():
            a = randint(LO, HI)
            b = randint(LO, HI)
            do_subtraction = SUBTRACTION and bool(randint(0, 1))

            if do_subtraction:
                question = f"{a + b} - {b} = ?"
                correct_answer = a
            else:
                question = f"{a} + {b} = ?"
                correct_answer = a + b

            options = [correct_answer]
            while len(options) < 4:
                wrong_answer = randint(LO - 5, HI + 5)
                if wrong_answer != correct_answer:
                    options.append(wrong_answer)

            shuffle(options)
            return question, options, correct_answer

        # Initialize Session State
        if "score" not in st.session_state:
            st.session_state.update({
                "score": 0,
                "start_time": None,
                "message": "",
                "current_question": None,
                "correct_answer": None,
                "answered": False,
                "option_selected": None,
            })

        # Header and Theme
        st.title("🎉 Fun Maths Game for Kids! 🎈")
        st.markdown(
            """Welcome to the **Maths Game**! Solve the questions and try to get the fastest score.
            
            🧮 Add or subtract numbers, pick the correct answer, and see if you can make it to the **High Scores**! Good luck!
            """
        )

        st.image("https://via.placeholder.com/800x200.png?text=Welcome+to+the+Maths+Adventure!", use_column_width=True)

        # Start the Game
        if st.session_state.start_time is None:
            st.session_state.start_time = time()

        # Generate a Question
        if st.session_state.score < NTIMES and st.session_state.current_question is None:
            question, options, correct_answer = generate_question()
            st.session_state.current_question = (question, options)
            st.session_state.correct_answer = correct_answer

        # Display the Question
        if st.session_state.current_question:
            question, options = st.session_state.current_question

            st.header(f"🦄 Question {st.session_state.score + 1}:")
            st.subheader(question)

            option_selected = st.radio("Choose your answer:", options, key=f"q{st.session_state.score}")

            if st.button("🐾 Submit Answer") and not st.session_state.answered:
                st.session_state.option_selected = option_selected
                st.session_state.answered = True

            if st.session_state.answered:
                if st.session_state.option_selected == st.session_state.correct_answer:
                    st.success("🎉 Hooray! That's correct! You're amazing! 🐻")
                    st.balloons()
                    st.session_state.score += 1
                else:
                    st.error(f"❌ Oh no! The correct answer is {st.session_state.correct_answer}. Keep going, you got this! 🐢")
                
                st.write(f"🌟 Your current score: {st.session_state.score}/{NTIMES}")

                if st.button("🔄 Next Question"):
                    st.session_state.answered = False
                    st.session_state.current_question = None

        # End of Game
        if st.session_state.score == NTIMES:
            elapsed = time() - st.session_state.start_time
            st.balloons()
            st.image("https://via.placeholder.com/800x200.png?text=You+Did+It!", use_column_width=True)
            st.write(f"🎯 **Fantastic!** You completed the game in {elapsed:.2f} seconds! 🏆")

            highscores = load_scores()
            if highscores.update(elapsed):
                st.success(f"🏅 Congratulations! You made it to the top {highscores.num_scores} scores!")

            st.write("📜 **High Scores:**")
            st.text(highscores)
            save_scores(highscores)

            st.write("🎉 **Your Score:**")
            st.write(f"⏱️ Time: {elapsed:.2f} seconds")

            st.session_state.score = 0
            st.session_state.start_time = None
            st.session_state.current_question = None

        # Quit Button
        if st.button("🚪 Quit"):
            st.session_state.score = 0
            st.session_state.start_time = None
            st.write("🚪 Game has been quit. Refresh the page to restart.")



# "Progress Report" Section
elif option == "Progress Report":
    st.subheader("Progress Report")
    st.write("Progress report will be here soon!")

else:
    st.write("Choose an activity from the dropdown above.")
