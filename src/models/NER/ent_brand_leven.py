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
            doc.set_ents(list(doc.ents) + [new_ent])


def find_in_next_token(ent, doc):
    brand = ent.ent_id_ or ent.kb_id_
    dictionary_brand = dictionary[brand]['models']
    names = map(str.lower, sorted(dictionary_brand.keys(), reverse=True))
    # ent = next((ent for ent in doc.ents if ent.label_ == 'BRAND' and (ent.ent_id_ == brand or ent.kb_id_ == brand)), None)
    # print(brand)
    if ent:
        start = ent.end
        end = start + 3 if start + 3 < len(doc) else len(doc)

        pred_model = "".join([doc[x].text for x in range(start, end)]).replace(' ', '').lower()
        model = next(filter(pred_model.startswith, names), None)
        if brand == 'AUDI':
            print(pred_model, model)
        if model: 
            new_ent = Span(doc, start, start + 1, label="MODEL", kb_id=model.upper())
            doc.set_ents(list(doc.ents) + [new_ent])




def set_similar_model(doc):
    for ent in [x for x in doc.ents if x.label_ == 'BRAND']:
        brand = ent.ent_id_ or ent.kb_id_
        dictionary_brand = dictionary[brand]['models']
        
        max_rate = 0.0
        most_likely_brand = ''
        best_index_token = 0

        directly_search_span = find_in_next_token(ent, doc)
        if directly_search_span: return directly_search_span

        for index, token in enumerate(doc):
            if len(token) > 2:
                rate, word = get_most_likely_word(str(token), dictionary_brand)
                if max_rate < rate:
                    max_rate = rate
                    most_likely_brand = word
                    best_index_token = index
        if max_rate > 0.0:
            new_ent = Span(doc, best_index_token, best_index_token + 1, label="MODEL", kb_id=most_likely_brand)
            doc.set_ents(list(doc.ents) + [new_ent])