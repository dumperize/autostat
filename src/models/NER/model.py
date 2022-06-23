import jsonlines
import spacy

from src.models.NER.expand_model import expand_model
from src.models.NER.add_space import CustomTokenizer


def create_ner_model(rules_file: str, important_names_file: str):
    rules = list(jsonlines.open(rules_file))
    important_names = list(jsonlines.open(important_names_file))
    nlp = spacy.blank("ru")
    # nlp = ru_core_news_sm.load(exclude=['tok2vec', 'morphologizer', 'parser', 'senter', 'attribute_ruler', 'lemmatizer'])

    nlp.tokenizer = CustomTokenizer(nlp.vocab, important_names)
    config = {"overwrite_ents": True }
    ruler = nlp.add_pipe("entity_ruler", config=config)

    # TODO вынести
    rules.append({"label": "YEAR", "pattern": [{"LOWER": {"REGEX": "[1][9][6-9][0-9]|(20)[0-1][0-9]|(20)[2][0-2]"}}]})

    ruler.add_patterns(rules)
    nlp.add_pipe("expand_model")

    return nlp
