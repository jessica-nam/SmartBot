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

words = []
classes = []
documents = [] # Conbination
ignore_letters = ['?', '!', '.', ',' ,'"', "'", "''", '*', '(', ')', '``', '[', ']', '”', '“', '§', '{', '}', '...', '....', '#', '$', '&', '-', '--', ':', ';', '<', '=', '==', '===', '>', '@', '/', '//'] # Characters not taken into consideration

for intent in intents['intents']:
    for q in intent['question']:
        word_list = nltk.word_tokenize(q) # Splits into individual words
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

classes = sorted(set(classes))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(words, open('classes.pkl', 'wb'))

##### At this point we only have words. We need to associate these words with numerical values to feed into the ML model #####
## For this we will use "bag_of_words" - we set the individual word values to either 0 or 1 depending on if it is occuring in that specific question

training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]

    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training,  dtype=object) # error

train_x = list(training[:, 0])
train_y = list(training[:, 1])
            
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation="softmax"))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)

model.save('chatbot_model')
print("Done training")