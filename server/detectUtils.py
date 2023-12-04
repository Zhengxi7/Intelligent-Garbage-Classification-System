import io

import numpy as np
from keras.models import load_model
# For HMM model and audio feature extraction
from python_speech_features import mfcc
from scipy.io import wavfile
from tensorflow.keras.utils import load_img, img_to_array

from MyCustomUnpickler import MyCustomUnpickler

# load audio models
model_map = {'1': 'metal',
             '2': 'carton',
             '3': 'plastic'}
reloaded_models = []
for key, value in model_map.items():
    fr = open(f"server/models/model_2_{key}.pkl", 'rb')
    unpickler = MyCustomUnpickler(fr)
    reloaded_models.append((unpickler.load(), value))

# load visual model
model = load_model('server/models/5class_mob.h5')


def detect_audio(audio: bytes):
    # 1: Select test audio file
    audio = io.BytesIO(audio)
    sampling_freq, audio = wavfile.read(audio)
    sampling_freq = sampling_freq / 2.5
    # preprocessing:
    # 1) merge two channels into one
    audio = np.mean(audio, axis=1)
    # 2) adjust length to 0.6s
    # length = audio.shape[0] / sampling_freq
    # target_length = 0.6
    # audio = pyrb.time_stretch(audio, sampling_freq, length / target_length)
    # 3) reduce noice
    # audio = nr.reduce_noise(y=audio, sr=sampling_freq, stationary=True)

    # 2: Extract MFCC features
    mfcc_features = mfcc(audio, sampling_freq)
    max_score = None
    output_label = None

    # 3: Iterate through all HMM models and
    #   pick the one with the highest score
    for item in reloaded_models:
        reloaded_model, label = item
        score = reloaded_model.get_score(mfcc_features)
        print(score, label)
        if max_score is None or score > max_score:
            max_score = score
            output_label = label

    return output_label, max_score


def detect_image(image: bytes):
    image = io.BytesIO(image)
    labels = ["carton", "glass", "metal", "plastic", "trash"]
    # {0: 'Carton', 1: 'Glass', 2: 'Metal', 3: 'Plastic', 4: 'Trash'}
    image = load_img(image, target_size=(224, 224))
    img_tensor = img_to_array(image)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.
    prediction = model.predict(img_tensor)

    label = labels[np.argmax(prediction)]

    return label


def detect_both(audio: bytes, image: bytes):
    label_audio, score = detect_audio(audio)
    if label_audio == "mental" and score > -12500:
        return label_audio
    elif label_audio == "plastic" and score > -12000:
        return label_audio
    elif label_audio == "carton" and score > -11000:
        return label_audio
    else:
        label_image = detect_image(image)
        return label_image
