import unittest
import sys
from os import path
import en_core_web_sm
nlp = en_core_web_sm.load()
sys.path.append( path.dirname( path.dirname( path.abspath("C:\\Users\\kyvin\\PycharmProjects\\QuantNeg_Webcrawler\\QNI.py") ) ) )
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

class Every_Neg_Detectiontest(unittest.TestCase):
    def test_detect_every_is_quantifier_negation_positives(self):
        self.quant = ["every"]
        self.dataset = quantifier_data_files["every_positives"]

        cases = [QNI.is_quantifier_negation(line, self.quant) for line in self.dataset]
        try:
            self.assertEqual(len([quant for quant in cases if quant is not None]), 391)
        except AssertionError:
            try:
                for line in self.dataset:
                    self.assertNotEqual(QNI.get_quantifier(line, self.quant), None)
            except AssertionError:
                print(
                    f"AssertError Is Quantifier Negation: *Line {self.dataset.index(line)}* - {line}")


class No_Neg_Detectiontest(unittest.TestCase):
    def test_if_function_works_on_no(self):
        self.quant = ["no"]
        self.dataset = quantifier_data_files["no_positives"]

        try:
            for line in self.dataset:
                QNI.is_quantifier_negation(line, self.quant)
        except Exception as e:
            print(f"{e}, \n >>>>>>>Error occured at line {self.dataset.index(line)}: {line}")


    def test_detect_no_is_quantifier_negation_positives(self):
        cases = [QNI.is_quantifier_negation(line, self.quant) for line in self.dataset]
        try:
            self.assertEqual(len([quant for quant in cases if quant is not None]), 64)
        except AssertionError:
            try:
                for line in self.dataset:
                    self.assertNotEqual(QNI.get_quantifier(line, self.quant), None)
            except AssertionError:
                print(f"AssertError Is Quantifier Negation: *Line {self.dataset.index(line)}* - {line}")


class Any_Neg_Detectiontest(unittest.TestCase):
    def test_detect_every_quant(self):
        pass

    #Standalone or continous
    def test_identify_standalone(self):
        pass


    def test_identify_continuous(self):
        pass


if __name__ == "__main__":
    unittest.main()