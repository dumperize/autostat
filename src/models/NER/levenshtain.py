from spacy.language import Language

@Language.component("levenshtain")
def levenshtain(doc):
        ent_brands = []
        ent_models = []
        ent_years = []
        for token in doc[0:4]:
            
        for ent in doc.ents:
            if ent.label_ == 'BRAND': ent_brands.append(ent)
            if ent.label_ == 'MODEL': ent_models.append(ent)
            if ent.label_ == 'YEAR': 
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
                    ent_years.append(ent)

        
        doc.ents = ent_brands + ent_models

        name_brands_set = list(set([x.ent_id_.lower() for x in ent_brands]))
        name_models_set = list(set([x.ent_id_.lower() for x in ent_models]))
        name_years_set = list(set([re.search(r'{}'.format(currentYearReg), x.text).group() for x in ent_years]))
        
        doc.user_data['count_brands'] = len(name_brands_set) # сколько всего найдено брендов
        doc.user_data['count_models'] = len(name_models_set) # сколько всего найдено моделей
        doc.user_data['count_years'] = len(name_years_set) # сколько всего найдено годов
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