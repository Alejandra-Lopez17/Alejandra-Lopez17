import re
from typing import List


class TechnicalTextProcessor:
    TECH_STOPWORDS = {
        "copyright",
        "license",
        "version",
        "rights",
        "reserved",
        "chapter",
        "section",
    }

    @staticmethod
    def preprocess_for_embedding(text: str) -> str:
        """Limpieza especializada para documentación técnica"""
        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        text = re.sub(r"`.*?`", "", text)
        text = re.sub(r"<.*?>", "", text)
        text = re.sub(r"\.\.\..*?::", "", text)
        text = re.sub(r"^[#=-]{3,}.*", "", text, flags=re.MULTILINE)
        text = re.sub(r">>>.*", "", text)
        text = text.lower()
        text = " ".join(
            [
                word
                for word in text.split()
                if word not in TechnicalTextProcessor.TECH_STOPWORDS
            ]
        )
        return text.strip()

    @staticmethod
    def extract_key_terms(text: str, top_n: int = 5) -> List[str]:
        """Extrae términos técnicos importantes"""
        from collections import Counter

        words = re.findall(r"\b[a-z]{3,}\b", text.lower())
        word_counts = Counter(words)
        return [word for word, _ in word_counts.most_common(top_n)]
