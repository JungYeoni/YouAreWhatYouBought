def describe_user_insta(uid, df, train_items=[]):
    # train_items: [item_name,]; only summarize for items in the list
    user_df = df[df['user_id'] == uid]
    items = dict(user_df[['product_name', 'count']].values)
    # further filter according to the given train_items variable
    if train_items:
        items = {k:v for k,v in items.items() if k in train_items}
    # add description like "36 PENCILS TUBE SKULLS purchased 16 times"
    items_description = '; '.join([f'{item}, {count} times' for item, count in items.items()])
    return f'The user {uid} has totally purchased {len(items)} unique products, we show each product name followed by its purchased times: he bought ' + items_description

def describe_users_insta(uids, df):
    descriptions = []
    for uid in uids:
        descriptions.append(describe_user_insta(uid, df))
    return '\n\n'.join(descriptions)

def assign_user_labels(
    client, # openai client object;
    grouped_item_df,    # pd.Dataframe;
    prompt_sys, prompt_user,    # str;
    uid,     # int;
    openai_model="gpt-4-0125-preview",   # openai model type
    debug=False, # bool;
) -> dict:

    transaction_data = describe_users_insta([uid], grouped_item_df)
    
    prompt_user_tail = f"""Here is the data of user {uid}'s transaction data for you to analyze:{transaction_data}
    Remind one more time that you can only select from the given 51 personas' list and only use the exactly given persona, you cannot use other words to describe.
    You do not need to explain how you get the result, so please respond no more than the required format.
    """

    if debug:
        print(prompt_user+prompt_user_tail)
        return

    try:
        completion = client.chat.completions.create(
            model=openai_model,
            messages=[
                {"role": "system", "content": prompt_sys},
                {"role": "user", "content": prompt_user+prompt_user_tail},
            ],
            stream=False,
        )

        response_result = ""
        # for chunk in stream:
        if completion.choices[0].message:
            response_result += completion.choices[0].message.content

        return {"user": uid, "users_profile": response_result}

    except Exception as e:  # Consider capturing a specific exception if possible
        print(f"[E] The following error occurred for user {uid} when collecting his persona labels: {e} ")
        return {"user": uid, "users_profile": "QUERY_FAILED"}


def from_json_to_obj(uid, answer_str, defined_persona_set, persona_fix_map):
    # if answer_str is a dict, just use it
    if isinstance(answer_str, dict):
        # but still need to check and fix persona names
        fixed_personas = []
        for p in answer_str[uid]:
            if p in defined_persona_set:
                fixed_personas.append(p)
            elif p in persona_fix_map:
                fixed_personas.append(persona_fix_map[p])
            else:
                print(f'Persona "{p}" will be removed from user {uid}.')
        answer_str[uid] = fixed_personas
        # if no persona，assigns the default 'Unrepresentable'
        if not answer_str[uid]:
            answer_str[uid] = ['Unrepresentable']
        # assert answer_str[uid], 'empty'
        res = answer_str
    else:
        start_idx = 0
        end_idx = len(answer_str)
    
        # case 1: contains keyword 'json'
        json_index = answer_str.find('json')
        if json_index != -1:
            start_idx = json_index + 4
            end_idx = -3
        # case 2: no 'json' but start with '''
        elif answer_str.startswith("```"):
            start_idx = 3
            end_idx = -3        
        res = eval(answer_str[start_idx:end_idx])
        
        assert type(res) == dict, 'oqweiuhd'
        assert res.get(uid) is not None, 'rtyuiold'
        
        # fix wrong persona names
        fixed_ps = []
        for p in res[uid]:
            if p in defined_persona_set:
                fixed_ps.append(p)
            elif p in persona_fix_map:
                fixed_ps.append(persona_fix_map[p])
            else:
                print(f'Persona "{p}" will be removed from user {uid}.')
        res[uid] = fixed_ps
        # if no persona，assigns the default 'Unrepresentable'
        if not res[uid]:
            res[uid] = ['Unrepresentable']
        # assert res[uid], 'empty'

    return res