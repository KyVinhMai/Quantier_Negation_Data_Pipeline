from dataclasses import dataclass
from utils.text_preprocessing_functions import load_json, load
from audio_processing.audio_utils.audio_preprocessing_functions import return_audio_len
import os
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
            self.sentences = load_json(self.sentences)


def audio_data_init(row : tuple) -> dataclass:
    return audio_data(
        row[0],
        row[1],
        row[2],
        row[3],
        row[4],
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
    context_list: list[str] | str
    context_str: str
    show: str
    quant: str

    def __post_init__(self):
        if "every" in self.quant.lower():
            self.quant = "every"

        elif "all" in self.quant.lower():
            self.quant = "all"

        elif "each" in self.quant.lower():
            self.quant = "each"

        self.show = "_".join(self.show.split())
        self.folder = f"E:\\AmbiLab_data\\Audio\\processed_audio\\{self.show}\\{self.quant}\\{self.ID}"

        try:
            os.mkdir(self.folder)
        except OSError as error:
            print(error)

        self.audio_dir = self.audio_dir.replace('D', 'E', 1)
        self.audio_len = return_audio_len(self.audio_dir)

        if isinstance(self.sentences, str):
            self.sentences = load_json(self.sentences)

        if isinstance(self.context_list, str):
            self.context_list = load(self.context_list)



