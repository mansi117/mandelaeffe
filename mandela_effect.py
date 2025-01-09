import os
import streamlit as st
from PIL import Image

# Dictionary of Mandela Effect examples
mandela_effect_images = {
    "coca_cola_logo": {
        "image1": "images/coca_cola_with_dash.jpg",
        "image2": "images/coca_cola_no_dash.jpg",
        "correct": "image1",
        "explanation": "The Coca-Cola logo never had a dash in between the words 'Coca' and 'Cola'."
    },
    "oreo_double_stuf": {
        "image1": "images/oreo_double_stuff.jpg",
        "image2": "images/oreo_double_stuf.jpg",
        "correct": "image2",
        "explanation": "Oreo has always spelled it 'Double Stuf' without an extra 'f' at the end."
    },
    "peace_symbol": {
        "image1": "images/peace_symbol_correct.jpg",
        "image2": "images/peace_symbol_incorrect.jpg",
        "correct": "image1",
        "explanation": "The peace symbol has a vertical line in the center, which has been part of its iconic design."
    },
    "seahorse_emoji": {
        "image1": "images/seahorse_emoji.jpg",  # Single seahorse emoji image
        "correct": "False",  # The correct answer is 'False'
        "explanation": "No, the Seahorse emoji does not exist in the current Unicode standard."
    }
}

# Helper function to check if file exists
def safe_open_image(image_path, resize_to=None):
    if os.path.exists(image_path):
        img = Image.open(image_path)
        if resize_to:
            img = img.resize(resize_to)
        return img
    else:
        return None

# Streamlit App Setup
st.title("Mandela Effect Quiz")
st.write("Can you identify the correct version of these famous logos, symbols, and scenes?")

# Quiz State Initialization
if "score" not in st.session_state:
    st.session_state.score = 0
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "user_answers" not in st.session_state:
    st.session_state.user_answers = []  # To store user answers and correctness

# List of questions
questions = list(mandela_effect_images.keys())

if st.session_state.current_question < len(questions):
    # Get current question
    question = questions[st.session_state.current_question]
    data = mandela_effect_images[question]

    # Display question
    st.write(f"**Question {st.session_state.current_question + 1}: {question.replace('_', ' ').title()}**")

    # Special handling for the Seahorse Emoji question
    if question == "seahorse_emoji":
        seahorse_image = safe_open_image(data["image1"], resize_to=(150, 150))
        if seahorse_image:
            st.image(seahorse_image, caption="Seahorse Emoji")
        else:
            st.write("Image not found!")

        # Add buttons for True or False
        if st.button("True", key=f"{question}_true"):
            user_choice = "True"
            is_correct = (user_choice == data["correct"])
            st.session_state.user_answers.append((question, user_choice, is_correct))
            if is_correct:
                st.session_state.score += 1
            st.session_state.current_question += 1

        if st.button("False", key=f"{question}_false"):
            user_choice = "False"
            is_correct = (user_choice == data["correct"])
            st.session_state.user_answers.append((question, user_choice, is_correct))
            if is_correct:
                st.session_state.score += 1
            st.session_state.current_question += 1

    # For all other image-based questions
    else:
        col1, col2 = st.columns(2)

        with col1:
            img1 = safe_open_image(data["image1"], resize_to=(300, 300))
            if img1:
                st.image(img1, caption="Option 1")
            else:
                st.write("Image not found!")

            if st.button("Choose Option 1", key=f"{question}_1"):
                user_choice = "image1"
                is_correct = (user_choice == data["correct"])
                st.session_state.user_answers.append((question, "Option 1", is_correct))
                if is_correct:
                    st.session_state.score += 1
                st.session_state.current_question += 1

        with col2:
            img2 = safe_open_image(data["image2"], resize_to=(300, 300))
            if img2:
                st.image(img2, caption="Option 2")
            else:
                st.write("Image not found!")

            if st.button("Choose Option 2", key=f"{question}_2"):
                user_choice = "image2"
                is_correct = (user_choice == data["correct"])
                st.session_state.user_answers.append((question, "Option 2", is_correct))
                if is_correct:
                    st.session_state.score += 1
                st.session_state.current_question += 1
else:
    # Show final score and answer feedback
    st.balloons()
    st.write(f"### Quiz Complete! 🎉 Your Score: {st.session_state.score}/{len(questions)}")

    # Detailed feedback
    st.write("### Detailed Feedback:")
    for question, answer, is_correct in st.session_state.user_answers:
        data = mandela_effect_images[question]
        st.write(f"**{question.replace('_', ' ').title()}**")
        if question == "seahorse_emoji":
            img = safe_open_image(data["image1"], resize_to=(150, 150))
            if img:
                st.image(img, caption="Seahorse Emoji")
        else:
            correct_img = safe_open_image(data[data["correct"]], resize_to=(300, 300))
            if correct_img:
                st.image(correct_img, caption=f"Correct Answer: {answer}")

        st.write(f"**Explanation:** {data['explanation']}")

    # Restart button
    if st.button("Restart Quiz"):
        st.session_state.score = 0
        st.session_state.current_question = 0
        st.session_state.user_answers = []
