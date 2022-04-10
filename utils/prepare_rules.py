import jsonlines

def list_lower(words_list):
    list_rules = []
    for word in words_list.split():
        word_punct = word.split('-')
        if len(word_punct):
            for index, x in enumerate(word_punct):
                list_rules.append({"LOWER": x.lower()})
                if index < len(word_punct) - 1: list_rules.append({"IS_PUNCT": True})
        else:
            list_rules.append({"LOWER": word.lower()})
    return list_rules

def create_rules(brands, label='BRAND'):
    rules = []
    for brand in brands:
            id_brand = brand['id'].lower()
            
            parrern_list = list_lower(brand['id'])
            rules.append({"label": label, "pattern": parrern_list, "id": id_brand})
            
            for alias in (brand['alias']):
                alias_list = list_lower(alias)
                rules.append({"label": label, "pattern": alias_list, "id": id_brand})
                
            for reg in (brand['regex']):
                pattern = []
                if isinstance(reg, list):
                    for x in reg:
                        if x == '-':
                            pattern.append({"IS_PUNCT": True})
                        else:
                            pattern.append({"LOWER": {"REGEX": x.lower()}})
                else:
                    pattern = [{"LOWER": {"REGEX": reg.lower()}}]
                rules.append({"label": label, "pattern": pattern, "id": id_brand})
                
    return rules