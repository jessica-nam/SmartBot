import unittest
import chatbot
from keras.models import Sequential

class TestChatbot(unittest.TestCase):
    """ Test class that inherits from unittest.testcase """

    def test_model(self):
        """ Using assertIsNotNone(x) because the output model should not be empty """

        test_bot = chatbot.model()

        self.assertIsNotNone(test_bot)

if __name__ == '__main__':
    
    unittest.main()