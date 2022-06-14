import jsonlines
import spacy
import ru_core_news_sm

from src.models.NER.expand_model import expand_model
from src.models.NER.levenshtain import levenshtain
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
    rules.append({"label": "YEAR", "pattern": [{"LOWER": {"REGEX": "[1][9][6-9][0-9]|(20)[0-1][0-9]|(20)[2][0-2]"}}], "id": "4-digits"})
    rules.append({'label': 'BRAND', 'pattern': 'YAMAHA', 'id': 'YAMAHA'}),
    ruler.add_patterns(rules)
    nlp.add_pipe("expand_model")
    # nlp.add_pipe("levenshtain", before="expand_model")
    print(rules)

    doc = nlp('марка YAMAHA 32007 года выпуска№ кузова JMZBK12F681713003№ шасси отсутствуетцвет серебристый№ двигателя LF 10473621г/н А830АМ124')
    print([x.label_ for x in doc.ents])

    return nlp
