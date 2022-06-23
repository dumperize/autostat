from spacy.language import Language
import re
import numpy as np
from src.models.NER.ent_year import ent_year, currentYearReg
from src.models.NER.ent_brand_leven import set_similar_model, set_similar_brand
from src.models.NER.utils.operation import filter_ent


def brand_1_model_one_or_many(brand, models, doc):
            brand_name = brand.text.lower() + '_'
            # модели по бренду
            return set(filter(
                lambda x: re.compile(brand_name).match(x.kb_id_.lower()) or re.compile(brand_name).match(x.ent_id_.lower()), 
                models
            ))
                
def brand_many_model_one_or_many(brands, models, doc):
            brands_name = '|'.join([brand.ent_id_.lower() + '_' for brand in brands])
            # модели по бренду
            fit_models = list(filter(lambda x: re.compile(brands_name).match(x.ent_id_.lower()), models))

            if len(fit_models):
                doc.user_data['have_fit_model'] = True

# def most_likely_brands(doc):
#     ents = doc.ents
#     brand_ents = [ent.ent_id_ for ent in ents if ent.label_ == 'BRAND']
#     for brand in brand_ents:
#         prev_index = brand.start - 1
#         doc[prev_index]= 


def get_ents_id(ents): return map(lambda ent: ent.ent_id_ or ent.kb_id_, ents)

@Language.component("expand_model")
def expand_model(doc):
        for ent in doc.ents:
            if ent.label_ == 'YEAR': ent_year(doc, ent)

        if len(filter_ent(doc, 'BRAND')) == 0: 
            set_similar_brand(doc)

        if len(filter_ent(doc, 'BRAND')) > 0 and len(filter_ent(doc, 'MODEL')) == 0:
            set_similar_model(doc)


        ent_brands = filter_ent(doc, 'BRAND')
        ent_models = filter_ent(doc, 'MODEL')
        ent_years = filter_ent(doc, 'YEAR')

        # есть 1 бренд и модели
        if len(ent_brands) == 1 and len(ent_models) > 1:
            brand = list(ent_brands)[0]
            ent_models = brand_1_model_one_or_many(brand, ent_models, doc)

        name_years_set = list(set([re.search(r'{}'.format(currentYearReg), x.text).group() for x in ent_years]))

        doc.user_data['brands'] = ', '.join(set(get_ents_id(ent_brands))) if len(ent_brands) else np.nan
        doc.user_data['models'] = ', '.join(set(get_ents_id(ent_models))) if len(ent_models) else np.nan
        doc.user_data['years'] = ', '.join(name_years_set) if len(name_years_set) else np.nan
        
        return doc