import re
from typing import List


class Tokenizer:
    """
    Tokenizer defining the DFA input alphabet Σ.
    Converts raw strings into a list of word tokens.
    """

    @staticmethod
    def tokenize(text: str) -> List[str]:
        if not text:
            return []

        text = text.lower()
        # Σ = alphanumeric word tokens
        return re.findall(r"[a-z0-9]+", text)
