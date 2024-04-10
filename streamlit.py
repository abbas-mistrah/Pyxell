import streamlit as st
import speech_recognition as sr

# Set background color and style for the logo
st.markdown(
    """
    <style>
    body {
        background-color: #7F7FD5 !important; /* Example background color */
    }
    .container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
    #logo {
        max-width: 80%; /* Adjust logo size as needed */
        height: auto;
        margin-bottom: 30px;
    }
    .input-field {
        width: 80%;
        max-width: 400px; /* Adjust input field width as needed */
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        font-size: 16px;
        margin-bottom: 20px;
        box-sizing: border-box; /* Ensure padding and border are included in width */
    }
    .input-field:focus {
        outline: none;
        border-color: #5F5FA0; /* Example focus color */
    }
    .voice-button {
        padding: 10px 20px;
        background-color: #5F5FA0; /* Example button color */
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
    }
    .voice-button:hover {
        background-color: #4C4C7F; /* Example button hover color */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add logo image with HTML and CSS
image_path = "templates/your_logo.png"  # Adjust the path to your logo image
st.markdown(f'<img id="logo" src="{image_path}">', unsafe_allow_html=True)

# Add container for input field and voice button
st.markdown('<div class="container">', unsafe_allow_html=True)

# Add text input field
user_input = st.text_input("Enter your command:", key="user_input")

# Add voice command option
if st.button("Start Voice Command"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening for voice command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        st.write("Voice Command:", command)
        user_input = command
    except sr.UnknownValueError:
        st.write("Sorry, I could not understand your command.")
    except sr.RequestError as e:
        st.write(f"Could not request results from Google Speech Recognition service; {e}")

# Close container for input field and voice button
st.markdown('</div>', unsafe_allow_html=True)

# Process the command
if user_input:
    # You can add your command processing logic here
    st.write("Command processed:", user_input)
