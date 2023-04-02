import unittest
import en_core_web_sm
nlp = en_core_web_sm.load()
from audio_processing.utils import preprocessing_functions as pf

class Test_Utils(unittest.TestCase):
    def test_transform_transcript_function(self):
        input = "the fox jumped over the lazy dog"
        correct = "THE|FOX|JUMPED|OVER|THE|LAZY|DOG"

        answer, _ = pf.transform_transcript(input, "the")
        print(answer)
        self.assertEqual(answer, correct)


