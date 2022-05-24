import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def show_2_pie(data):
    fig, axes = plt.subplots(1, 2, figsize=(20, 10), facecolor='#e8f4f0')

    #     1
    labels = 'Бренд обнаружен', 'Бренд НЕ обнаружен'
    sizes = [data.count()['first_brand'], data.shape[0] - data.count()['first_brand']]
    ax = axes[0]
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    #     2
    labels = 'Обнаружены подходящие под бренд модели', 'Обнаружены НЕ подходящие под бренд модели', 'НЕ обнаружены модели'
    sizes = [
        data[data['have_fit_model']].shape[0], 
        data[data['count_models']!=0][data['have_fit_model'] == False].shape[0], 
        data[data['count_models']==0].shape[0]]
    ax = axes[1]
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    plt.show()
    
    
def show_bar_model(data, start = 0, end = 40):
    df1 = pd.DataFrame(data['first_brand'].value_counts())
    df1.index.name = 'brand'

    df2 = data.copy()
    cols = ["count_models","have_fit_model"]
    df2[cols] = df2[cols].replace(['0', 0, False], np.nan)

    df2 = df2.groupby(['first_brand']).count()
    df2.index.name = 'brand'

    df = df1.join(df2,on='brand')

    df = df[['count_brands', 'count_models','have_fit_model']][start:end]

    plt.figure(figsize=(20, 10))
    for i in df.columns:
        plt.bar(df.index, df[i])

    plt.rcParams["figure.figsize"] = (20,15)
    plt.xticks(fontsize=18,rotation=90, ha='right')
    plt.xticks(fontsize=18)
    plt.ylabel('Количество строк')
    plt.xlabel('марки')
    plt.legend(df.columns)
    plt.tight_layout()