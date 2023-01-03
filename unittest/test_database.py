import unittest
import database
from warnings import filterwarnings

class TestDatabase(unittest.TestCase):
    """ Test class that inherits from unittest.testcase """

    def test_build_url(self):
        """ Using assertEqual(a, b) because URLs must follow a certain format """

        test_url = database.build_url(1, "https://stackoverflow.com/questions/tagged/", "python")

        self.assertEqual(test_url, "https://stackoverflow.com/questions/tagged/python?tab=votes&page=1")

    def test_build_answer_url(self):
        """ Using assertEqual(a, b) because URLs must follow a certain format """

        test_url = database.build_answer_url("https://stackoverflow.com/questions/", "231767")

        self.assertEqual(test_url, "https://stackoverflow.com/questions/231767")

    def test_paraphrase_text(self):
        """ Using assertIsInstance(a, b) because paraphrase_text must return a list of sentences """

        sentence = ["What are metaclasses in Python?"]

        test_sentence = database.paraphrase_text(1234, sentence)

        self.assertIsInstance(test_sentence, list)

    def test_scrape_one_question_page(self):
        """ Using assertIsInstance(a, b) because output to database must be in list format """

        filterwarnings(action='ignore', category=DeprecationWarning, message='`np.bool8` is a deprecated alias for `np.bool_`.')

        test_data = database.scrape_one_question_page(1)

        self.assertIsInstance(test_data, list)

    def test_export_data(self):
        """ Using assertIsNone(x) because export data shouldnt return anything """

        filterwarnings(action='ignore', category=DeprecationWarning, message='`np.bool8` is a deprecated alias for `np.bool_`.')

        test_file = database.export_data(1, "test.json")

        self.assertIsNone(test_file)

if __name__ == '__main__':
    
    unittest.main()