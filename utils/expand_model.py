from spacy.language import Language
import re

@Language.component("expand_model")
def expand_model(doc):
    new_ents = []
    
    labels = set()
    brands = []
    models = []
    for ent in doc.ents:
        labels.add(ent.label_)
        if ent.label_ == 'BRAND': brands.append(ent)
        if ent.label_ == 'MODEL': models.append(ent)
    
    brands_set = set([x.ent_id_ for x in brands])
    # брейндов больше одного - TODO
    if len(brands_set) > 1:
#         print("> 1 BRANDS ", brands_set, doc)
        return doc

    # есть и бренд и модель
    if "BRAND" in labels and 'MODEL' in labels:
        brand = brands[0].ent_id_
        r = re.compile(brand.lower() + "_")
        # модели по бренду
        fit_models = list(filter(lambda x: r.match(x.ent_id_.lower()), models))
        
        if len(fit_models):
            new_ents = new_ents + fit_models # только подходящие модели
        else:
            new_ents = new_ents + models # все как есть
    
    new_ents = new_ents + brands

    doc.ents = new_ents
    return doc