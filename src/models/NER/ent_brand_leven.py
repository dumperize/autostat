from src.models.NER.utils.add_del_span import add_span_in_doc
from src.models.NER.utils.get_dictionary import dictionary
from src.models.NER.utils.jaro import get_most_likely_word

from spacy.tokens import Span

from src.models.NER.utils.retokenizer import split_token_by_2


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
            span = Span(doc, best_index_token, best_index_token + 1, label="BRAND", kb_id=most_likely_brand)
            add_span_in_doc(doc,span)


def find_in_next_token(ent, doc):
    brand = ent.ent_id_ or ent.kb_id_
    dictionary_brand = dictionary[brand]['models']
    names = map(str.lower, sorted(dictionary_brand.keys(), reverse=True))

    if ent:
        start = ent.end
        end = start + 3 if start + 3 < len(doc) else len(doc)

        pred_model = "".join([doc[x].text for x in range(start, end)]).replace(' ', '').lower()
        model = next(filter(pred_model.startswith, names), None)

        if model: 
            if len(model) < len(doc[start].text):
                split_token_by_2(doc, start, len(model))

                span_model = doc[start:end].char_span(0, len(doc[start].text), label="MODEL")
                add_span_in_doc(doc, span_model)
                exist_ent =doc[start].ent_type_
                if exist_ent =='YEAR':
                    span_year = doc[start:end].char_span(len(doc[start].text), len(doc[start].text)+ len(doc[start + 1].text), label="YEAR")
                    add_span_in_doc(doc, span_year)

                # ents = [x for x in doc.ents if x.start != start]

                # doc.set_ents(list(ents) + spans)
                # add_span_in_doc(doc,span)
            else:
                span = Span(doc, start, start + 1, label="MODEL", kb_id=model.upper())
                add_span_in_doc(doc, span)
            return True
    return False




def set_similar_model(doc):
    brands_ents = [x for x in doc.ents if x.label_ == 'BRAND']

    for iter in range(len(brands_ents)):
        ents = [x for x in doc.ents if x.label_ == 'BRAND']
        ent = ents[iter] if len(ents) > iter else None

        if ent: 
            brand = ent.ent_id_ or ent.kb_id_
            dictionary_brand = dictionary[brand]['models']
            
            find_in_next_token(ent, doc)

    if len([x for x in doc.ents if x.label_ == 'MODEL']):
        return

    max_rate = 0.0
    most_likely_brand = ''
    best_index_token = 0

    for index, token in enumerate(doc):
        if len(token) > 2 and token.ent_type_ == '':
            rate, word = get_most_likely_word(str(token), dictionary_brand)
            if max_rate < rate:
                max_rate = rate
                most_likely_brand = word
                best_index_token = index
    if max_rate > 0.0:
        new_ent = Span(doc, best_index_token, best_index_token + 1, label="MODEL", kb_id=most_likely_brand)
        doc.set_ents(list(doc.ents) + [new_ent])