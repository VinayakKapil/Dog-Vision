from flask import Flask, render_template, request, jsonify

import base64

import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import CustomObjectScope
import tensorflow_hub as hub

import numpy as np

app = Flask(__name__)

# List of unique breeds
unique_breeds = np.array([
    'affenpinscher', 'afghan_hound', 'african_hunting_dog', 'airedale',
    'american_staffordshire_terrier', 'appenzeller', 'australian_terrier',
    'basenji', 'basset', 'beagle', 'bedlington_terrier',
    'bernese_mountain_dog', 'black-and-tan_coonhound', 'blenheim_spaniel',
    'bloodhound', 'bluetick', 'border_collie', 'border_terrier',
    'borzoi', 'boston_bull', 'bouvier_des_flandres', 'boxer',
    'brabancon_griffon', 'briard', 'brittany_spaniel', 'bull_mastiff',
    'cairn', 'cardigan', 'chesapeake_bay_retriever', 'chihuahua',
    'chow', 'clumber', 'cocker_spaniel', 'collie',
    'curly-coated_retriever', 'dandie_dinmont', 'dhole', 'dingo',
    'doberman', 'english_foxhound', 'english_setter', 'english_springer',
    'entlebucher', 'eskimo_dog', 'flat-coated_retriever', 'french_bulldog',
    'german_shepherd', 'german_short-haired_pointer', 'giant_schnauzer',
    'golden_retriever', 'gordon_setter', 'great_dane', 'great_pyrenees',
    'greater_swiss_mountain_dog', 'groenendael', 'ibizan_hound', 'irish_setter',
    'irish_terrier', 'irish_water_spaniel', 'irish_wolfhound', 'italian_greyhound',
    'japanese_spaniel', 'keeshond', 'kelpie', 'kerry_blue_terrier',
    'komondor', 'kuvasz', 'labrador_retriever', 'lakeland_terrier',
    'leonberg', 'lhasa', 'malamute', 'malinois', 'maltese_dog',
    'mexican_hairless', 'miniature_pinscher', 'miniature_poodle',
    'miniature_schnauzer', 'newfoundland', 'norfolk_terrier',
    'norwegian_elkhound', 'norwich_terrier', 'old_english_sheepdog',
    'otterhound', 'papillon', 'pekinese', 'pembroke', 'pomeranian',
    'pug', 'redbone', 'rhodesian_ridgeback', 'rottweiler',
    'saint_bernard', 'saluki', 'samoyed', 'schipperke',
    'scotch_terrier', 'scottish_deerhound', 'sealyham_terrier',
    'shetland_sheepdog', 'shih-tzu', 'siberian_husky', 'silky_terrier',
    'soft-coated_wheaten_terrier', 'staffordshire_bullterrier',
    'standard_poodle', 'standard_schnauzer', 'sussex_spaniel',
    'tibetan_mastiff', 'tibetan_terrier', 'toy_poodle', 'toy_terrier',
    'vizsla', 'walker_hound', 'weimaraner', 'welsh_springer_spaniel',
    'west_highland_white_terrier', 'whippet', 'wire-haired_fox_terrier', 'yorkshire_terrier'
])

# Load the model with CustomObjectScope
URL = "https://www.kaggle.com/models/google/mobilenet-v2/TensorFlow2/035-224-classification/2"
with CustomObjectScope({'KerasLayer': hub.KerasLayer}):
    model = load_model('./dog_vision_model.h5', custom_objects={'KerasLayer': hub.KerasLayer})

## Define image size
IMG_SIZE = 224

def process_image(image_bytes, img_size=IMG_SIZE):
    """
    Takes image bytes and converts them into tensors.
    """
    # Convert image bytes to tensor
    image = tf.io.decode_image(image_bytes, channels=3)
    
    # Convert color channel values from 0-255 to 0-1
    image = tf.image.convert_image_dtype(image, tf.float32)
    
    # Resize the image to the desired size
    image = tf.image.resize(image, size=[img_size, img_size])
    
    return image

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def predictor():
    if request.method == 'POST':
        if 'Imagefile' not in request.files:
            return "No file part"
        imagefile = request.files['Imagefile']
        if imagefile.filename == '':
            return "No selected file"
        if imagefile:
            image_data = imagefile.read()
            image = process_image(image_data)
            image = tf.expand_dims(image, axis=0)  # Add batch dimension

            # Make prediction
            yhat = model.predict(image)
            label = unique_breeds[np.argmax(yhat)]
            
            return render_template('dog.html', prediction=label + ' ' + f"with {np.argmax(yhat)}% of confidence")
    return render_template('dog.html')

if __name__ == '__main__':
    app.run(debug=True)
