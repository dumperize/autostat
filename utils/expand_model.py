from spacy.language import Language
import re


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
    for ent in doc.ents:
        if ent.label_ == 'BRAND': ent_brands.append(ent)
        if ent.label_ == 'MODEL': ent_models.append(ent)
    
    doc.ents = ent_brands + ent_models
    
    name_brands_set = list(set([x.ent_id_.lower() for x in ent_brands]))
    name_models_set = list(set([x.ent_id_.lower() for x in ent_models]))
    
    doc.user_data['count_brands'] = len(name_brands_set) # сколько всего найдено брендов
    doc.user_data['count_models'] = len(name_models_set) # сколько всего найдено моделей
    doc.user_data['first_brand'] = name_brands_set[0] if len(name_brands_set) else None # самый первый бренд
    doc.user_data['brands'] = ', '.join(name_brands_set)
    doc.user_data['models'] = ', '.join(name_models_set)
    doc.user_data['have_fit_model'] = False
    
    # есть бренды и модели
    if len(name_brands_set) > 1 and len(name_models_set):
        brand_many_model_one_or_many(ent_brands, ent_models, doc)

    # есть 1 бренд и модели
    if len(name_brands_set) == 1 and len(name_models_set):
        brand_1_model_one_or_many(ent_brands[0], ent_models, doc)
            

    return doc