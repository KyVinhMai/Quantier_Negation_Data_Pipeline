from utils.data_formatting import *
import unittest
import en_core_web_sm
nlp = en_core_web_sm.load()
import pandas as pd

class Test_table_formatting(unittest.TestCase):
    def test_ensure_correct_formatting(self):
        """
        Checks that the data class has the proper value types loaded in
        """
        df = pd.read_csv('main_links.tsv', delimiter='\t', usecols=["link", "audio_dir","clauses",	"transcript","batches","html"])
        df_row = df.sample(n=1)

        row = link_item(df_row["link"].item(), df_row["audio_dir"].item(),
                        df_row["clauses"].item(), df_row["transcript"].item(),
                        df_row["batches"].item(),
                        df_row["html"].item())
        print(row)
        assert(isinstance(row.clauses, int))
        assert(isinstance(row.sentences, list))
        for i in row.sentences:
            assert type(i) == str


if __name__ == "__main__":
    unittest.main()