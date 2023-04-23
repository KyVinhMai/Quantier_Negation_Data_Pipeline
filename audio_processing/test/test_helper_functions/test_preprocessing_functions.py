import unittest
import en_core_web_sm
nlp = en_core_web_sm.load()
from audio_processing.utils import preprocessing_functions as pf, \
    localization_functions as lf

class Test_Utils(unittest.TestCase):

    def test_localize_context(self):
        pass

    def test_transform_transcript_function(self):
        input = "the fox jumped over the lazy dog"
        correct = "THE|FOX|JUMPED|OVER|THE|LAZY|DOG"

        answer, _ = pf.insert_vertical(input, "the")
        print(answer)
        self.assertEqual(answer, correct)

    def test_rm_nonlexical(self):
        text1 = ""
        text2 = ""
        with open("../data/raw_text_1") as file:
            for line in file:
                text1 = line

        with open("../data/raw_text_2") as file:
            for line in file:
                text2 = line

        correct1 = "  Over the weekend, several buses from Texas arrived here in Washington. They dropped off  Inside a steamy home kitchen in northwest Washington, Ana Monge is busy making tamales. . Monge's been making hundreds of tamalesbuses. The immediate sensation was, like, how can I help? Coming to this country as  finding something better. It definitely hit home."
        correct2 = " All eyes turn to the Senate now. How quickly might they act?  Well, there are interesting dynamics at play in the Senate. Some Republicans and even progressives are not willing to support just one bill that forces the contract agreement, but they're inclined to support it if it comes with a bill to provide seven days of sick leave. Here's Missouri GOP Senator Josh Hawley."
        self.assertEqual(pf.rm_nonlexical_items(text1), correct1)
        self.assertEqual(pf.rm_nonlexical_items(text2), correct2)


