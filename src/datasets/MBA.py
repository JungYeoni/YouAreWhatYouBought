import pandas as pd
import numpy as np
from tqdm import tqdm

def MBA_load_data(ds_path='../ds/MBA/data.csv', debug=False):
    # -> [mba_df, user_ids, user_num, user_ids_kv, item_names, item_num, items_kv, G_user, G_item]
    
    print(f'Loading MBA dataset from path:{ds_path}')
    
    ## load dataset and basic clean
    mba_df = pd.read_csv(ds_path, sep=';')
    if debug: print(mba_df.head())
    # clean nan rows
    if mba_df.isna().sum().sum() > 0:
        print('all nan eliminated')
        mba_df = mba_df.dropna()
    # transfer types
    mba_df['BillNo'] = mba_df['BillNo'].astype('int32')
    mba_df['Itemname'] = mba_df['Itemname'].astype('string')
    mba_df['Quantity'] = mba_df['Quantity'].astype('int32')
    mba_df['Date'] = mba_df['Date'].astype('string')
    mba_df['Price'] = mba_df['Price'].astype('string')
    mba_df['CustomerID'] = mba_df['CustomerID'].astype('int32')

    ## Identifications
    # for user nodes
    user_ids = mba_df['CustomerID'].unique()
    user_num = len(user_ids)
    print(f'totally {user_num} unique users')
    user_ids.sort()
    user_ids_kv = {}
    for ui in range(user_num):
        user_ids_kv[user_ids[ui]] = ui
    # for item nodes
    item_names = mba_df['Itemname'].unique()
    item_num = len(item_names)
    print(f'totally {item_num} unique items')
    # item_names.sort()
    items_kv = {}
    for ii in range(item_num):
        items_kv[item_names[ii]] = ii

    ## construct the bi-partite graph
    G_user = {} # {uidx: [tidx,]}
    G_item = {} # {tidx: [uidx,]}

    for index,row in tqdm(mba_df.iterrows()):
        user_index = user_ids_kv[row['CustomerID']]
        item_index = items_kv[row['Itemname']]
        
        # update user side
        if G_user.get(user_index) is None:
            G_user[user_index] = {item_index}
        else:
            G_user[user_index].update([item_index])
        
        # update item side
        if G_item.get(item_index) is None:
            G_item[item_index] = {user_index}
        else:
            G_item[item_index].update([user_index])

    assert len(G_item.keys()) == item_num and len(G_user.keys()) == user_num

    return mba_df, user_ids, user_num, user_ids_kv, item_names, item_num, items_kv, G_user, G_item