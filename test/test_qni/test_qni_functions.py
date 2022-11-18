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
        cases = [QNI.is_quantifier_negation(line, ["every"]) for line in quantifier_data_files["every_positives"]]
        try:
            self.assertEqual(len([quant for quant in cases if quant is not None]), 391)
        except AssertionError:
            try:
                for line in quantifier_data_files["every_positives"]:
                    self.assertNotEqual(QNI.get_quantifier(line, ["every"]), None)
            except AssertionError:
                print(
                    f"AssertError Is Quantifier Negation: *Line {quantifier_data_files['every_positives'].index(line)}* - {line}")

class No_Neg_Detectiontest(unittest.TestCase):
    def test_if_function_works_on_no(self):
        try:
            for line in quantifier_data_files["no_positives"]:
                QNI.is_quantifier_negation(line, ["no"])
        except Exception as e:
            print(f"{e}, \n >>>>>>>Error occured at line {quantifier_data_files['no_positives'].index(line)}: {line}")


    def test_detect_no_is_quantifier_negation_positives(self):
        cases = [QNI.is_quantifier_negation(line, ["no"]) for line in quantifier_data_files["no_positives"]]
        try:
            self.assertEqual(len([quant for quant in cases if quant is not None]), 64)
        except AssertionError:
            try:
                for line in quantifier_data_files["no_positives"]:
                    self.assertNotEqual(QNI.get_quantifier(line, ["no"]), None)
            except AssertionError:
                print(f"AssertError Is Quantifier Negation: *Line {quantifier_data_files['no_positives'].index(line)}* - {line}")


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