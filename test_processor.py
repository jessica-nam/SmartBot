import unittest
import processor
import pickle
import numpy
import random
import json
from warnings import filterwarnings
from keras.models import load_model

class TestProcessor(unittest.TestCase):
    """ Test class that inherits from unittest.testcase """

    def test_clean_up_sentence(self):
        """ Using assertIsInstance(a, b) because the sentence must be tokenized into a list in this function """

        sentence = "I like sushi"
        test_sentence = processor.clean_up_sentence(sentence)

        self.assertIsInstance(test_sentence, list)

    def test_bow(self):
        """ Using assertIsInstance(a, b) because the sentence must be tokenized into a list in this function """

        words = pickle.load(open('words.pkl','rb'))
        sentence = "I like sushi"
        test_sentence = processor.bow(sentence, words, show_details=False)

        self.assertIsInstance(test_sentence, numpy.ndarray)

    def test_predict_class(self):
        """ Using assertIsInstance(a, b) because the sentence must be tokenized into a list in this function """

        model = load_model('model.h5')
        sentence = "What is Python"
        test_class = processor.predict_class(sentence, model)

        self.assertIsInstance(test_class, list)

    def test_getResponse(self):
        """ Using assertIsInstance(a, b) because the sentence must be tokenized into a list in this function """

        model = load_model('model.h5')
        sentence = "What is Python"

        ints = processor.predict_class(sentence, model)
        intents = json.loads(open('intents.json', encoding='utf-8').read())

        test_response = processor.getResponse(ints, intents)

        self.assertIsInstance(test_response, str)

    def test_chatbot_response(self):
        """ Using assertIsInstance(a, b) because the sentence must be tokenized into a list in this function """

        model = load_model('model.h5')
        sentence = "What is Python"
        intents = json.loads(open('intents.json', encoding='utf-8').read())

        ints = processor.predict_class(sentence, model)
        res = processor.getResponse(ints, intents)

        test_response = processor.getResponse(ints, intents)

        self.assertIsInstance(test_response, str)

if __name__ == '__main__':
    
    unittest.main()