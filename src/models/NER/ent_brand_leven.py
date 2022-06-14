from src.models.NER.utils.jaro import get_most_likely_word
import json
from spacy.tokens import Span


def set_similar_model(doc):
    with open('data/raw/model.json', 'r') as outfile:
        models = json.load(outfile)
        
        max_rate = 0.0
        most_likely_brand = ''
        best_index_token = 0

        for index, token in enumerate(doc):
            if len(token) > 3:
                rate, word = get_most_likely_word(str(token), models)
                if max_rate < rate:
                    max_rate = rate
                    most_likely_brand = word
                    best_index_token = index
        if max_rate > 0.85:
            new_ent = Span(doc, best_index_token, best_index_token + 1, label="BRAND", kb_id=most_likely_brand)
            doc.set_ents([new_ent])
            return new_ent
        return None
        