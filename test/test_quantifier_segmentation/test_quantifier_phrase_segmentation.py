import unittest
import sys
from os import path
import en_core_web_sm
nlp = en_core_web_sm.load()
sys.path.append( path.dirname( path.dirname( path.abspath("C:\\Users\\kyvin\\PycharmProjects\\QuantNeg_Webcrawler\\Quantifier_Phrase_Segmentation.py") ) ) )
import QNI
from pathlib import Path

quantifier_data_files = {}
directory_path = Path.cwd()

for file in directory_path.iterdir():
    if file.match("*.txt"):
        with open(file, "r") as f:
            sentences = []
            for line in f:
                sentences.append(line.rstrip('\n'))
            quantifier_data_files[file.stem] = sentences

class Test_Quantifier_Phrase_Segmentation(unittest.TestCase):
    def test_get__every_quantifier(self):
        cases = [QNI.get_quantifier(line, ["every"]) for line in quantifier_data_files["every_sentence_toy_data"]]

        try:
            for line_num in range(len(cases)):
                self.assertEqual(cases[line_num], quantifier_data_files["extracted_every_quantifier"][line_num])
        except AssertionError as e:
            print(e, f"\n> This is the line number [{line_num + 1}]: {quantifier_data_files['every_sentence_toy_data'][line_num]}")


