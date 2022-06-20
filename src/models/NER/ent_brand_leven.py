from src.models.NER.utils.get_dictionary import dictionary
from src.models.NER.utils.jaro import get_most_likely_word

from spacy.tokens import Span


def set_similar_brand(doc):
    max_rate = 0.0
    most_likely_brand = ''
    best_index_token = 0
    for index, token in enumerate(doc):
            if len(token) > 2:
                rate, word = get_most_likely_word(str(token), dictionary)
                if max_rate < rate:
                    max_rate = rate
                    most_likely_brand = word
                    best_index_token = index
    if max_rate > 0.0:
            new_ent = Span(doc, best_index_token, best_index_token + 1, label="BRAND", kb_id=most_likely_brand)
            doc.set_ents([new_ent])
            return new_ent
    return None
        
def get_similar_model(brand, doc):
        dictionary_brand = dictionary[brand]['models']
        
        max_rate = 0.0
        most_likely_brand = ''
        best_index_token = 0

        for index, token in enumerate(doc):
            if len(token) > 2:
                rate, word = get_most_likely_word(str(token), dictionary_brand)
                if max_rate < rate:
                    max_rate = rate
                    most_likely_brand = word
                    best_index_token = index
        if max_rate > 0.0:
            new_ent = Span(doc, best_index_token, best_index_token + 1, label="MODEL", kb_id=most_likely_brand)
            doc.set_ents([new_ent])
            return new_ent
        return None