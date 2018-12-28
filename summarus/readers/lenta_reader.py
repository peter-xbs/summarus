import csv
from typing import Dict

from allennlp.data.dataset_readers.dataset_reader import DatasetReader
from allennlp.data.tokenizers.tokenizer import Tokenizer
from allennlp.data.token_indexers.token_indexer import TokenIndexer

from summarus.readers.summarization_reader import SummarizationReader


@DatasetReader.register("lenta")
class LentaReader(SummarizationReader):
    def __init__(self,
                 tokenizer: Tokenizer = None,
                 source_token_indexers: Dict[str, TokenIndexer] = None,
                 target_token_indexers: Dict[str, TokenIndexer] = None,
                 source_max_tokens: int = 400,
                 target_max_tokens: int = 100,
                 separate_namespaces: bool = False) -> None:
        super().__init__(
            tokenizer=tokenizer,
            source_token_indexers=source_token_indexers,
            target_token_indexers=target_token_indexers,
            source_max_tokens=source_max_tokens,
            target_max_tokens=target_max_tokens,
            separate_namespaces=separate_namespaces
        )

    def parse_set(self, path):
        with open(path, "r", encoding="utf-8") as r:
            reader = csv.reader(r, delimiter=",", quotechar='"')
            header = next(reader)
            assert header[1] == "title"
            assert header[2] == "text"
            for row in reader:
                assert len(row) >= 3
                title, text = row[1], row[2]
                assert text and title
                yield text, title
