import pandas as pd
import numpy as np
from tqdm import tqdm

def insta_load_data(ds_path='../../data/insta_MBA/10%_sampled_insta_df.csv', debug=False):
    # -> [mba_df, user_ids, user_num, user_ids_kv, item_names, item_num, items_kv, G_user, G_item]
    
    print(f'Loading instacart_MBA dataset from path:{ds_path}')
    
    ## load dataset and basic clean
    insta_df = pd.read_csv(ds_path)
    if debug: print(insta_df.head())
    # clean nan rows
    if insta_df.isna().sum().sum() > 0:
        print('all nan eliminated')
        insta_df = insta_df.dropna()
    # transfer types
    insta_df['product_id'] = insta_df['product_id'].astype('int32')
    insta_df['user_id'] = insta_df['user_id'].astype('int32')
    insta_df['product_name'] = insta_df['product_name'].astype('string')

    ## Identifications
    # for user nodes
    user_ids = insta_df['user_id'].unique()
    user_num = len(user_ids)
    print(f'totally {user_num} unique users')
    user_ids.sort()
    user_ids_kv = {}
    for ui in range(user_num):
        user_ids_kv[user_ids[ui]] = ui
    # for item nodes
    item_names = insta_df['product_name'].unique()
    item_num = len(item_names)
    print(f'totally {item_num} unique items')
    # item_names.sort()
    items_kv = {}
    for ii in range(item_num):
        items_kv[item_names[ii]] = ii

    ## construct the bi-partite graph
    G_user = {} # {uidx: [tidx,]}
    G_item = {} # {tidx: [uidx,]}

    for index,row in tqdm(insta_df.iterrows(), total=len(insta_df)):
        user_index = user_ids_kv[row['user_id']]
        item_index = items_kv[row['product_name']]
        
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

    return insta_df, user_ids, user_num, user_ids_kv, item_names, item_num, items_kv, G_user, G_item