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
    #quantifiers
    def test_detect_every_quant(self):
        pass

class No_Neg_Detectiontest(unittest.TestCase):
    def test_detect_no_Quant_positives(self):
        cases = [QNI.get_quantifier(line, ["no"]) for line in quantifier_data_files["no_positives"]]
        try:
            self.assertEqual(len([quant for quant in cases if quant is not None]), 64)
        except AssertionError:
            "If the numbers don't match, find the line which interupts the program"
            try:
                for line in quantifier_data_files["no_positives"]:
                    self.assertNotEqual(QNI.get_quantifier(line, ["no"]), None)
            except AssertionError:
                print(f"AssertError: *Line {quantifier_data_files['no_positives'].index(line)}* - {line}")


    def test_detect_no_Quant_negatives(self):
        cases = [QNI.get_quantifier(line, ["no"]) for line in quantifier_data_files["no_negatives"]]
        try:
            self.assertEqual(len([quant for quant in cases if quant is not None]), 64)
        except AssertionError:
            "If the numbers don't match, find the line which interupts the program"
            try:
                for line in quantifier_data_files["no_positives"]:
                    self.assertNotEqual(QNI.get_quantifier(line, ["no"]), None)
            except AssertionError:
                print(f"AssertError: *Line {quantifier_data_files['no_positives'].index(line)}* - {line}")


    def test_detect_no_assoneg_positives(self):
        q_root = nlp("no")
        cases = [QNI.assoc_negation_exists(line, q_root) for line in quantifier_data_files["no_positives"]]
        try:
            self.assertEqual(len([quant for quant in cases if quant is not None]), 64)
        except AssertionError:
            try:
                for line in quantifier_data_files["no_positives"]:
                    self.assertNotEqual(QNI.get_quantifier(line, ["no"]), None)
            except AssertionError:
                print(f"AssertError - Associate Negation: *Line {quantifier_data_files['no_positives'].index(line)}* - {line}")

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
        cases = [QNI.get_quantifier(line, ["any"]) for line in quantifier_data_files["any_positives"]]
        self.assertEqual(len([quant for quant in cases if quant is not None]), 4)


    #Standalone or continous
    def test_identify_standalone(self):
        pass


    def test_identify_continuous(self):
        pass


if __name__ == "__main__":
    unittest.main()