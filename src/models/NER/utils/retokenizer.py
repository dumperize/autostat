def split_token_by_2(doc, num_token, pos_str):
    with doc.retokenize() as retokenizer:
        heads = [(doc[num_token], 1), doc[num_token - 1]]
        retokenizer.split(
            doc[num_token], 
            [doc[num_token].text[:pos_str], doc[num_token].text[pos_str:]], 
            heads=heads, 
            attrs={}
        )

def split_token_by_3(doc, num_token, pos_str_1, pos_str_2):
    with doc.retokenize() as retokenizer:
        heads = [(doc[num_token], 2), doc[num_token - 1]]
        retokenizer.split(
            doc[num_token], 
            [doc[num_token].text[:pos_str_1], doc[num_token].text[pos_str_1:pos_str_2], doc[num_token].text[:pos_str_2]], 
            heads=heads, 
            attrs={}
        )