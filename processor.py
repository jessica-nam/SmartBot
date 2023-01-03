##### Natural Language Processing libraries #####
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

##### Machine Learning Libraries #####
from keras.models import load_model
model = load_model('model.h5')

##### Libraries for file management #####
import json
import random
intents = json.loads(open('intents.json', encoding='utf-8').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

def clean_up_sentence(sentence):
    """ Tokenizes sentence words and makes them case-insensitive """
    sentence_words = nltk.word_tokenize(sentence) # Tokenize
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words] # Lower
    return sentence_words # This is a list

def bow(sentence, words, show_details=True):
    """ Convert STR data into numerical values so that machine learning model can understand """

    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)

    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))

def predict_class(sentence, model):
    """ Predict what category (tag) user's question belongs in """

    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]

    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)

    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    """ Tries to find an answer. If unable to, Stacky outputs random default sentence """
    try:
        tag = ints[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if(i['tag']== tag):
                result = random.choice(i['responses'])
                break
            else:
                result = "You must ask the right questions"
    except IndexError:
        temp = random.randrange(0,5)
        if temp == 0:
            result = "Could you be more specific?"
        elif temp == 1:
            result = "Could you try rephrasing by adding or removing specific words?"
        elif temp == 2:
            result = "I am sorry. I don't understand. Stacky is only a baby after all..."
        elif temp == 3:
            result = "I am not sure I have an answer for that. But of course you can always go to https://stackoverflow.com/"
        else:
            result = "Could you try wording your question in a different way?"
        
    return result

def chatbot_response(msg):
    """ Generates and returns response """
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    # print(res)
    return res

### Uncomment this to debug in terminal and not flask app ###

# while True:
#     print("Type")
#     msg = input("")

#     chatbot_response(msg)