from nltk.stem import WordNetLemmatizer # To reduce words to stem for performance ex: work, working, worked will all be the same word
import random                           # Achieving random response
import pickle                           # For serialization
import json
import numpy as np
import nltk

from tensorflow import keras            # Machine learning model
from keras.models import Sequential 
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('intents.json').read())