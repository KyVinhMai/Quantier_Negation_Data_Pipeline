from dataclasses import dataclass
from utils.text_preprocessing_functions import load_jsondoc

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

