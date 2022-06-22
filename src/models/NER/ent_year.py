import re

from src.models.NER.utils.retokenizer import split_token_by_2, split_token_by_3


# TODO 2023 год уже не попадет - надо написать через переменную
currentYearReg = '[1][9][6-9][0-9]|(20)[0-1][0-9]|(20)[2][0-2]'

def get_neighbor(doc, ent, next: bool):
            incr = 1 if next else -1
            is_fit_token = True
            while is_fit_token:
                token =  None if ent.start + incr < 0 or ent.start + incr >= len(doc) else doc[ent.start + incr]
                if token is None:
                    is_fit_token = False
                if re.compile("^[-.?!)(,:]$").match(str(token)):
                    incr = incr + 1 if incr > 0 else incr - 1
                else:
                    is_fit_token = False
            return token

def ent_year(doc, ent):
                prev_token = get_neighbor(doc, ent, False) 
                next_token = get_neighbor(doc, ent, True)

                match_string = r'г\.|года|год|выпуска|изготовления|в\.'
                not_match_string = r'№|куб.см|^см|^с.|^кг\.|^НМ$|^от$|рама|двигатель|двигателя|января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|декабря|номер'

                prev_result = re.match(match_string, str(prev_token)) # есть в пред
                prev_neg_result = re.match(not_match_string, str(prev_token)) # есть плохое в пред
                pos_prev = not prev_neg_result and prev_result

                next_result = re.match(match_string, str(next_token)) # есть в след
                next_neg_result = re.match(not_match_string, str(next_token)) # есть плохое в след
                pos_next = not next_neg_result and next_result

                inner_result = re.match(match_string, str(ent.text)) # есть в внутри
                inner_neg_result = re.match(not_match_string, str(ent.text)) # есть плохое в внутри
                pos_inner = not inner_neg_result and inner_result

                only_digits = re.match(r'^{}$'.format(currentYearReg), str(ent.text)) # состоит только из 4х цифр
                neg_data = re.match(r'\d{2}\.\d{2}\.\d{4}', str(ent.text))  # это не дата

                pos_token = pos_prev or pos_next or pos_inner # в токенах вокруг что-то позитивное
                pos_digits = only_digits and not prev_neg_result and not next_neg_result # это просто 4 цифры и ничего негативного вокруг

                if not neg_data and (pos_token or pos_digits):
                     
                    for match in re.finditer(currentYearReg, ent.text):
                        index = match.start() 
                        year = match.group()

                        if ent.text.startswith(year):
                            split_token_by_2(doc, ent.start, 4)
                        elif ent.text.endswith(year):
                            split_token_by_2(doc, ent.start, index)
                        else:
                            split_token_by_3(doc, ent.start, index, index + 4)
                        
                        span = doc.char_span(ent.start_char + index, ent.start_char + index + 4, label="YEAR")
 
                        ents = [x for x in doc.ents if x != ent]
                        ents.append(span)

                        doc.set_ents(ents)
                    return True
                return False