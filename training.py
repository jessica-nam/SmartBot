import random                           # Achieving random response
import json
import pickle                           # For serialization
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer # To reduce words to stem for performance ex: work, working, worked will all be the same word

from tensorflow import keras            # Machine learning model
from keras.models import Sequential 
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('intents.json').read()) # Reading contents of JSON file as text into JSON object intents (dictionary)

words = []
classes = []
documents = []

ignore_letters = ['?', '!', '.', ',' ,'"', "'", "''", '*', '(', ')', '``', '[', ']'] # Letters not taken into account

# Iterate over intents
for intent in intents['intents']:
    for question in intent['question']:
        word_list = nltk.word_tokenize(question) # Splits into individual words
        words.extend(word_list)
        documents.append((word_list, intent['tag']))

        if intent['tag'] not in classes:
            classes.append(intent['tag'])


words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))
classes = sorted(set(classes))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(words, open('classes.pkl', 'wb'))

