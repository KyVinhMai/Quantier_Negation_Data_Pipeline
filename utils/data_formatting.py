from dataclasses import dataclass
from utils.text_preprocessing_functions import load_jsondoc, rm_nonlexical_items

def link_init(link_row : tuple) -> dataclass:
    return link_item(
        link_row[0],
        link_row[1],
        link_row[2],
        link_row[3],
        link_row[4],
        link_row[5],
    )

@dataclass
class link_item:
    link: str
    audio_dir: str
    clauses: int
    sentences: list[str] | str
    batch: int
    html: str

    def __post_init__(self):
        if isinstance(self.sentences, str):
            self.sentences = load_jsondoc(self.sentences)

def audio_data_init(row : tuple) -> dataclass:
    return audio_data(
        row[0],
        row[1],
        row[2],
        row[3],
        row[4],
        row[5],
        row[6],
    )
@dataclass
class audio_data:
    ID: int
    audio_dir: str
    sentences: list[str] | str
    utterance: str
    context: list[str] | str
    show: str
    quant: str
    folder: str = f"E:\\AmbiLab_data\\Audio\\processed_audio\\{show}\\{quant}"

    def __post_init__(self):
        if isinstance(self.sentences, str):
            self.sentences = load_jsondoc(self.sentences)

        if isinstance(self.context, str):
            self.context = [rm_nonlexical_items(sent) for sent in self.context]

        if len(self.quant) != 1: #Assumes that if quant is len of 1, then it should have the quantifier information
            if "every" in self.quant:
                self.quant = "every"

            elif "all" in self.quant:
                self.quant = "all"

            elif "each" in self.quant:
                self.quant = "each"



