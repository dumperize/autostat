from spacy.language import Language
import json
import Levenshtein
from spacy.tokens import Span


def replace_rus_to_eng_char(sample_string):
    sample_string = sample_string.upper()
    char_to_replace = {'А': 'A',
                       'В': 'B',
                       'С': 'C',
                       'Е': 'E',
                       'Н': 'H',
                       'К': 'K',
                       'О': 'O',
                       'Р': 'P',
                       'Т': 'T',
                       'Х': 'X'}
    return sample_string.translate(str.maketrans(char_to_replace))

def get_jaro(word, similar_word): 
    word = replace_rus_to_eng_char(word)
    similar_word = replace_rus_to_eng_char(similar_word)
        
    return Levenshtein.jaro_winkler(word, similar_word)
    

def leven(word, brands_dictionary): 
    if len(word) < 3: return None

    rate = 0.0
    most_likely_word = ''
    for brand in brands_dictionary:
        jaro = max(get_jaro(word, name) for name in brand['names'])
        if jaro > rate:
            rate = jaro
            most_likely_word = brand['id']

    return most_likely_word if rate > 0.85 else None

@Language.component("levenshtain")
def levenshtain(doc):
    with open('data/raw/model.json', 'r') as outfile:
        models = json.load(outfile)
        
        new_ents = []
        for index, token in enumerate(doc):
            if len(token) > 2:
                similar_model = leven(str(token), models)
                if similar_model:
                    print(similar_model)
                    new_ent = Span(doc, index, index+1, label=similar_model, kb_id=similar_model)
                    print('---', new_ent.kb_id_)

                    new_ents.append(new_ent)
        print([(x.label_, x.kb_id_, x.text) for x in new_ents])
        doc.set_ents(new_ents)
        return doc