import spacy
import pandas as pd


data = pd.read_csv('pledges - pledges.csv', delimiter='|')

nlp = spacy.load("ru_core_news_sm")

# ruler = nlp.add_pipe("entity_ruler")
ruler = nlp.add_pipe("entity_ruler").from_disk("./patterns.jsonl")
# patterns = [{"label": "RENAULT", "pattern": "RENAULT"},
#             {"label": "УАЗ", "pattern": "УАЗ"}]
# ruler.add_patterns(patterns)

articles = [
    'RENAULT LOGAN (SR)2006 года выпуска',
    'УАЗ-29891 тип спецпассажирскийкатегория Вгод изготовления 2014номер двигателя 409110*Е3000529; номер кузова 396200Е0200654; регистрационный номер М257МЕ48ПТС 73 НХ 508070',
    'Автомобиль Renault SANDERO',
    'РЕНО ЛОГАНПТС 66 НМ 627666 (дубликат)цвет белый2012г.в.',
    'Легковой автомобиль RENAULTDUSTER коричневый'
]

for article in data['vehicleproperty_description_short'].values:
    doc = nlp(article)

    print(doc.ents)
    # for ent in doc.ents:
    #     print(ent.text, ent.start_char, ent.end_char, ent.label_)