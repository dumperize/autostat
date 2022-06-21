from spacy.language import Language
import re
import numpy as np
from src.models.NER.ent_year import ent_year, currentYearReg
from src.models.NER.ent_brand_leven import set_similar_model, set_similar_brand


def brand_1_model_one_or_many(brand, models, doc):
            brand_name = brand.lower() + '_'
            # модели по бренду
            return set(filter(lambda x: re.compile(brand_name).match(x.lower()), models))
                
            # if len(fit_models):
            #     doc.ents = [brand] + fit_models # только подходящие модели
            #     doc.user_data['count_models'] = len(fit_models) # сколько всего найдено моделей
            #     doc.user_data['models'] = ', '.join(list(set([x.ent_id_.lower() for x in fit_models])))
            #     doc.user_data['have_fit_model'] = True
                
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

@Language.component("expand_model")
def expand_model(doc):
        brands = set()
        models = set()

        for ent in doc.ents:
            if ent.label_ == 'BRAND': brands.add(ent.ent_id_) # ent_brands.append(ent)
            if ent.label_ == 'MODEL': models.add(ent.ent_id_) # ent_models.append(ent)

        if len(brands) == 0:
            set_similar_brand(doc)

        if len(brands) > 0 and len(models) == 0:
            set_similar_model(doc)



        brands = set()
        models = set()
        ent_years = []
        for ent in doc.ents:
            if ent.label_ == 'BRAND': brands.add(ent.ent_id_ or ent.kb_id_) # ent_brands.append(ent)
            if ent.label_ == 'MODEL': models.add(ent.ent_id_ or ent.kb_id_) # ent_models.append(ent)
            if ent.label_ == 'YEAR'and ent_year(doc, ent): ent_years.append(ent)

        # есть 1 бренд и модели
        if len(brands) == 1 and len(models) > 1:
            brand = list(brands)[0]
            models = brand_1_model_one_or_many(brand, models, doc)

        # print([(x.label_, x.ent_id_, x.kb_id_, x.text) for x in doc.ents])

        # doc.ents = ent_brands + ent_models + ent_years

        # name_brands_set = list(set([x.ent_id_.lower() for x in ent_brands]))
        # name_brands_set_sim = list(set([x.kb_id_.lower() for x in ent_brands_sim]))
        # name_models_set = list(set([x.ent_id_.lower() for x in ent_models]))
        name_years_set = list(set([re.search(r'{}'.format(currentYearReg), x.text).group() for x in ent_years]))
        
        # doc.user_data['count_brands'] = len(name_brands_set) # сколько всего найдено брендов
        # doc.user_data['count_models'] = len(name_models_set) # сколько всего найдено моделей
        # doc.user_data['count_years'] = len(name_years_set) # сколько всего найдено годов
        # doc.user_data['first_brand'] = name_brands_set[0] if len(name_brands_set) else None # самый первый бренд
        doc.user_data['brands'] = ', '.join(list(brands)) if len(brands) else np.nan
        # doc.user_data['brands_sim'] = ', '.join(name_brands_set_sim)
        doc.user_data['models'] = ', '.join(list(models)) if len(models) else np.nan
        doc.user_data['years'] = ', '.join(name_years_set) if len(name_years_set) else np.nan
        
        # есть бренды и модели
        # if len(name_brands_set) > 1 and len(name_models_set):
        #     brand_many_model_one_or_many(ent_brands, ent_models, doc)

        # # есть 1 бренд и модели
        # if len(name_brands_set) == 1 and len(name_models_set):
        #     brand_1_model_one_or_many(ent_brands[0], ent_models, doc)
        
        # doc.ents = list(doc.ents) + ent_years

        return doc