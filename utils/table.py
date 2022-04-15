import pandas as pd

def left_align(s):
        direction = 'left'
        return 'text-align: %s' % direction
    
def show_table(data, brand, start=0, end=400, only_empty=True):
    brand = brand.lower()
        

    finaly_df = data[data['first_brand']==brand][['HTML', 'brands', 'models', 'have_fit_model', 'count_brands','count_models']]
    if only_empty:
        finaly_df = finaly_df[(finaly_df['have_fit_model'] == False) | (finaly_df['have_fit_model'].isnull())]
    print("Count rows ", finaly_df.shape[0])
    
    finaly_df = finaly_df[start:end]
    
    finaly_df.style.applymap(left_align, subset=pd.IndexSlice[:, ['HTML']])
    return finaly_df

def show_empty_brand(data,start=0, end=400):
    finaly_df = data[data['count_brands']==0][['HTML', 'brands', 'models', 'have_fit_model', 'count_brands','count_models']]
    finaly_df = finaly_df[(finaly_df['have_fit_model'] == False) | (finaly_df['have_fit_model'].isnull())]
    print("Count rows ", finaly_df.shape[0])
    
    finaly_df = finaly_df[start:end]
    
    finaly_df.style.applymap(left_align, subset=pd.IndexSlice[:, ['HTML']])
    return finaly_df