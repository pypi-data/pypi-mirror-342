import pandas as pd
import json
import os

def map_df_to_data_for_canonicality(df, option_including_index=True):
    if option_including_index:
        df = df.reset_index()
    else:
        df = df.reset_index() if df.index.name else df
    data = df.to_dict(orient='records')
    return data

def map_data_to_df_for_canonicality(data, option_index_col=0):
    df = pd.DataFrame(data)
    if option_index_col is not None:
        df = df.set_index(df.columns[option_index_col])
    return df

def map_df_to_csv_for_canonicality(df, file_folder, file_name, option_including_index=False, option_korean=True):
    df = df.reset_index() if option_including_index else df
    if option_korean:
        df.to_csv(os.path.join(file_folder, file_name), index=False, encoding='utf-8-sig')
    else:
        df.to_csv(os.path.join(file_folder, file_name), index=False)
    return None

def map_data_to_json_for_canonicality(data, file_folder, file_name):
    with open(os.path.join(file_folder, file_name), 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return None
