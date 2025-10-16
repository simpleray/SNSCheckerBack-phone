import spacy
from spacy.pipeline import EntityRuler
from pathlib import Path
import yaml

_nlp = None

def get_nlp():
    """
    GiNZAモデル + EntityRulerを入れたNLPを返す。
    最初に呼び出したときだけ作り、その後は同じインスタンスを返す。
    """
    global _nlp
    if _nlp is None:
        # GiNZAモデルをロード
        _nlp = spacy.load("ja_ginza")

        # EntityRuler のパターンファイルを読み込み
        patterns_path = Path("nlp/patterns/entity_ruler.yml")
        if patterns_path.exists():
            with open(patterns_path, "r", encoding="utf-8") as f:
                patterns = yaml.safe_load(f)
            ruler = _nlp.add_pipe("entity_ruler", before="ner")
            ruler.add_patterns(patterns)

    return _nlp
