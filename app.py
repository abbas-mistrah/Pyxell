from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image
import io
import google.generativeai as genai
from commands.general import match_command_general
from commands.system import match_command_system
from commands.browser import match_command_browser
from commands.files import match_command_files
from commands.other import match_command_other
import spacy
import webbrowser
import commands.browserfullyautomate as bfa
import os
import tempfile
import requests

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

# Fetch the Gemini API key from the environment or your preferred method
GOOGLE_API_KEY = "AIzaSyBM9X2lZAZ4d7reekRRhpMNKdP9RvSt2Cw"
HUGGING_FACE_API_KEY = "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"

# Configure the Gemini API with your API key
genai.configure(api_key=GOOGLE_API_KEY)

# Function to generate text using the Gemini API
def generate_text(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

# Function to generate image using the Hugging Face API
def generate_image(prompt):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)

    # Save the generated image to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        temp_file.write(response.content)
        temp_file_path = temp_file.name
    return temp_file_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the uploaded image
        image_file = request.files['image']
        image_bytes = image_file.read()

        # Load the image and generate a response
        img = Image.open(io.BytesIO(image_bytes))
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content(["Describe the image in detail.", img])
        
        # Return the generated response as JSON
        return jsonify({'response': response.text})

    # Render the index template for GET requests
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def command():
    user_input = request.form['user_input']
    doc = nlp(user_input)
    tokens = [token.text.lower() for token in doc]

    result = match_command_general(tokens)
    if result is None:
        result = match_command_system(tokens)
    if result is None:
        result = match_command_browser(tokens)
    if result is None:
        result = match_command_files(tokens)
    if result is None:
        result = match_command_other(tokens)
    if result is None:
        result = bfa.process_command(user_input)

    if result is None:  # If no command is found
        if "your name" in user_input or "who are you" in user_input or "what is your good name" in user_input or "who developed you" in user_input:
            return jsonify({'response': "I'm Pyxell! I'm an AI assistant developed by Pyxell.ai, ready to help you with any digital task"})
        elif user_input.startswith("generate image "):
            image_prompt = user_input[14:].strip()
            image_path = generate_image(image_prompt)
            image_filename = os.path.basename(image_path)
            return jsonify({'image_filename': image_filename})
        else:
            generated_text = generate_text(user_input)
            return jsonify({'response': generated_text})

    return jsonify({'response': "Command executed successfully!"}) if result is not None else jsonify({'error': "Command execution failed."})

@app.route('/images/<filename>')
def serve_image(filename):
    image_path = os.path.join(tempfile.gettempdir(), filename)
    return send_file(image_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
