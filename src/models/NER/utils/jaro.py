import Levenshtein

def replace_rus_to_eng_char(sample_string):
    sample_string = sample_string.upper()
    char_to_replace = {'А': 'A',
                       'В': 'B',
                       'С': 'C',
                       'Е': 'E',
                       'Н': 'H',
                       'К': 'K',
                       'О': 'O',
                       'Р': 'P',
                       'Т': 'T',
                       'Х': 'X'}
    return sample_string.translate(str.maketrans(char_to_replace))

def get_jaro(word, similar_word): 
    word = replace_rus_to_eng_char(word)
    similar_word = replace_rus_to_eng_char(similar_word)
    return Levenshtein.jaro_winkler(word, similar_word)

def get_jaro_with_threshold(word, similar_word, threshold):
    jaro = get_jaro(word, similar_word)
    return -1.0 if jaro < threshold else jaro


def get_most_likely_word(word, brands_dictionary): 
    if len(word) < 3: return None

    rate = 0.0
    most_likely_word = ''
    for brand in brands_dictionary:
        jaro = max(get_jaro_with_threshold(word, item['name'], item['threshold']) for item in brand['names'])
        if jaro > rate:
            rate = jaro
            most_likely_word = brand['id']

    return (rate, most_likely_word)