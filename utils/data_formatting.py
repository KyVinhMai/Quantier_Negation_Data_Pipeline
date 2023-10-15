from dataclasses import dataclass
from utils.text_preprocessing_functions import load_jsondoc

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

