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

def create_rules(data, label='BRAND', prefix=''):
    rules = []
    for item in data:
            id_item = prefix + item['id'].lower()
            
            parrern_list = list_lower(item['id'])
            rules.append({"label": label, "pattern": parrern_list, "id": id_item})
            
            for alias in (item['alias']):
                alias_list = list_lower(alias)
                rules.append({"label": label, "pattern": alias_list, "id": id_item})
                
            for reg in (item['regex']):
                pattern = []
                if isinstance(reg, list):
                    for x in reg:
                        if x == '-':
                            pattern.append({"IS_PUNCT": True})
                        else:
                            pattern.append({"LOWER": {"REGEX": x.lower()}})
                else:
                    pattern = [{"LOWER": {"REGEX": reg.lower()}}]
                rules.append({"label": label, "pattern": pattern, "id": id_item})
                
    return rules