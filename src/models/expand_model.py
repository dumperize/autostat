from spacy.language import Language
import re
import numpy as np


def brand_1_model_one_or_many(brand, models, doc):
    brand_name = brand.ent_id_.lower() + '_'
    # модели по бренду
    fit_models = list(filter(lambda x: re.compile(brand_name).match(x.ent_id_.lower()), models))
        
    if len(fit_models):
        doc.ents = [brand] + fit_models # только подходящие модели
        doc.user_data['count_models'] = len(fit_models) # сколько всего найдено моделей
        doc.user_data['models'] = ', '.join(list(set([x.ent_id_.lower() for x in fit_models])))
        doc.user_data['have_fit_model'] = True
        
def brand_many_model_one_or_many(brands, models, doc):
    brands_name = '|'.join([brand.ent_id_.lower() + '_' for brand in brands])
    # модели по бренду
    fit_models = list(filter(lambda x: re.compile(brands_name).match(x.ent_id_.lower()), models))

    if len(fit_models):
        doc.user_data['have_fit_model'] = True
        
        
@Language.component("expand_model")
def expand_model(doc):
    ent_brands = []
    ent_models = []
    ent_years = []
    for ent in doc.ents:
        if ent.label_ == 'BRAND': ent_brands.append(ent)
        if ent.label_ == 'MODEL': ent_models.append(ent)
        if ent.label_ == 'YEAR': 
            prev_token = None if ent.start - 1 < 0 else doc[ent.start - 1]
            next_token = None if ent.start < len(doc) else doc[ent.start + 1]

            # TODO 
            match_string = r'г\.|года|год|выпуска|изготовления|в\.|^см|^с.|^кг\.'
            prev_result = re.search(match_string, str(prev_token))
            next_result = re.search(match_string, str(next_token))
            inner_result = re.search(match_string, str(ent.text))
            only_digits = re.search(r'^[19|20]\d{3}$', str(ent.text))
            
            if prev_result or next_result or inner_result or only_digits:
                ent_years.append(ent)

    
    doc.ents = ent_brands + ent_models
    
    def findYear(ent):
        if ent.ent_id_ == '4-digits':
            elements = re.findall(r'[19|20]\d{3}', ent.text)
        else:
            elements = re.findall(r'\d{2}', ent.text)
        return None if len(elements) == 0 else elements[0]

    name_brands_set = list(set([x.ent_id_.lower() for x in ent_brands]))
    name_models_set = list(set([x.ent_id_.lower() for x in ent_models]))
    name_years_set = list(set([findYear(x) for x in ent_years]))
    
    doc.user_data['count_brands'] = len(name_brands_set) # сколько всего найдено брендов
    doc.user_data['count_models'] = len(name_models_set) # сколько всего найдено моделей
    doc.user_data['first_brand'] = name_brands_set[0] if len(name_brands_set) else None # самый первый бренд
    doc.user_data['brands'] = ', '.join(name_brands_set)
    doc.user_data['models'] = ', '.join(name_models_set)
    doc.user_data['years'] = ', '.join(name_years_set)
    doc.user_data['have_fit_model'] = False
    
    # есть бренды и модели
    if len(name_brands_set) > 1 and len(name_models_set):
        brand_many_model_one_or_many(ent_brands, ent_models, doc)

    # есть 1 бренд и модели
    if len(name_brands_set) == 1 and len(name_models_set):
        brand_1_model_one_or_many(ent_brands[0], ent_models, doc)
    
    doc.ents = list(doc.ents) + ent_years
    return doc