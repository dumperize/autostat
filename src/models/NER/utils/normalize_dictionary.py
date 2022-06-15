import copy

def normalize_brand_dictionary(brand_dictionary):
    dictionary = copy.deepcopy(brand_dictionary)
    for brand in dictionary:
        names = []
        for name in brand['names']:
            if isinstance(name, dict): 
                names.append(name)
            else:
                names.append({"name": name, "threshold": 0.0})
        brand['names'] = names
    return dictionary