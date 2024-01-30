# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 15:36:54 2024

@author: CBT
"""

import pandas as pd

config = pd.read_excel('config.xlsx',engine = 'openpyxl')

config = dict(list(zip(config['key'],config['value'])))

df = pd.read_csv('invalids_new.csv')

df1 = df[((df['reason'].isna()) | (df['reason']==''))]

df = df[((df['reason'].isna()) | (df['reason']==''))]

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



df = df.apply(lambda row:hash(row,config['HASH_1_columns'].split(','),'HASH_1'),axis = 1)

df = df.apply(lambda row:hash(row,config['HASH_2_columns'].split(','),'HASH_2'),axis = 1)


df1.to_csv('invalids_after_separation.csv',index = False)

df.to_csv('valid_with_hash.csv',index = False)





