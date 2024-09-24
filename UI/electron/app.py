from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
from utils.llm_config import *
from utils.story_generator import llm
from utils.image_generator import imageGen
import logging
logging.basicConfig(level=logging.DEBUG)  # Set the log level to DEBUG to see all outputs



app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:5000"}})
# if __name__ == '__main__':
#     app.run(debug=True)
# Load model
# tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
# model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")

model_xml = "C:\\Users\\intelaipc\\IntelAIPCProject\\models\\storyTeller\\phi-3-mini-instruct\\INT4_compressed_weights\\openvino_model.xml"
model_bin = "C:\\Users\\intelaipc\\IntelAIPCProject\\models\\storyTeller\\phi-3-mini-instruct\\INT4_compressed_weights\\openvino_model.bin"

LLM = llm(model_xml, model_bin)
imageGen = imageGen()


@app.route('/generate_story_and_images', methods=['GET'])
def generate_story_and_images():
    #try:
    # Example of calling an external API or model
    story_text = LLM.generate_story()
    questions = None  #LLM.generate_questions(story_text)
    images = imageGen.generate_images_from_text(story_text)
    print("Request headers:", request.headers)
    print("Request method:", request.method)
    print("Request URL:", request.url)
    print("Story and Images Generated!")
    return jsonify({"story": story_text, "questions": questions, "images": images})
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    #     return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True, port=5000) # runs local host on port 5000
