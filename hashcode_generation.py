# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 15:36:54 2024

@author: CBT
"""

import pandas as pd

import hashlib

import os

config = pd.read_excel('config.xlsx',engine = 'openpyxl')

config = dict(list(zip(config['key'],config['value'])))

df_ = pd.read_csv('valid_transaction1.csv')

total_rows = len(df_)

def hash(row,column,hash_value):
 
    concatstr = ''
 
    for j in column:
 
        concatstr = concatstr + row[j]
 
    row[hash_value] = hashlib.sha512( concatstr.encode("utf-8") ).hexdigest()
    
    return row

chunk_size = 100000 

for i, chunk_df in enumerate(pd.read_csv('total_transaction.csv', chunksize=chunk_size, low_memory=False)):

    start_index = i * chunk_size

    end_index = min((i + 1) * chunk_size, total_rows)

    print(f"Processing chunk {i+1}: Rows {start_index}-{end_index}")

    df = df_[start_index:end_index]

    missing_columns = set(config['HASH_1_columns'].split(',')) - set(df.columns)

    for xy in missing_columns:
        
        df[xy] = ''

    missing_columns = set(config['HASH_2_columns'].split(',')) - set(df.columns)

    for xy in missing_columns:
        
        df[xy] = ''
        
    for xy in config['HASH_1_columns'].split(','):
        
        df[xy].fillna('',inplace = True)
        
    for xy in config['HASH_2_columns'].split(','):
        
        df[xy].fillna('',inplace = True)

    print('hash started')

    df = df.apply(lambda row:hash(row,config['HASH_1_columns'].split(','),'HASH_1'),axis = 1)

    df = df.apply(lambda row:hash(row,config['HASH_2_columns'].split(','),'HASH_2'),axis = 1)

    print('hash ended')

    with open('response.txt','r') as w:

        text = w.read()

    with open('response.txt','w') as w:

        w.write(f"Processed chunk {i+1}: Rows {start_index}-{end_index}")


    # df1.to_csv('invalids_after_separation.csv',index = False)

    df.to_csv('valid_with_hash.csv',index = False, mode='a', header=not os.path.exists('valid_with_hash.csv'))





