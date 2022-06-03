# import ru_core_news_sm
import jsonlines
# import os
import spacy

from src.models.NER.expand_model import expand_model


colors = {"BRAND": "#aa9cfc", "MODEL": "#fc9ce7", "YEAR": "#9cfcb1"}
options = {"ents": ["BRAND", "MODEL", "YEAR"], "colors": colors}

def create_ner_model(rules_file: str):
    rules = list(jsonlines.open(rules_file))

    nlp = spacy.blank("ru") # ru_core_news_sm.load(exclude=['tok2vec', 'morphologizer', 'parser', 'senter', 'attribute_ruler', 'lemmatizer'])

    config = {"overwrite_ents": True }
    ruler = nlp.add_pipe("entity_ruler", config=config)

    # TODO вынести
    rules.append({"label": "YEAR", "pattern": [{"LOWER": {"REGEX": "[1][9][6-9][0-9]|(20)[0-1][0-9]|(20)[2][0-2]"}}], "id": "4-digits"})
    # rules.append({"label": "YEAR", "pattern": [{"LOWER": {"REGEX": "\D(\d{2})\D"}}], "id": "2-digits"})

    ruler.add_patterns(rules)

    nlp.add_pipe("expand_model")

    return nlp
