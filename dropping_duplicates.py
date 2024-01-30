# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 15:43:29 2024

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




duplicates = df[df.duplicated(['FIRSTNAME','LASTNAME','DATEOFBIRTH','CUSTOMERADDRESS'])]

unique = df[~(df.duplicated(['FIRSTNAME','LASTNAME','DATEOFBIRTH','CUSTOMERADDRESS']))]

unique.to_csv('four_hash.csv',index = False)

duplicates.to_csv('four_hash_duplicates.csv',index = False)


duplicates = df[df.duplicated(['FIRSTNAME','LASTNAME','DATEOFBIRTH'])]

unique = df[~(df.duplicated(['FIRSTNAME','LASTNAME','DATEOFBIRTH']))]

unique.to_csv('three_hash.csv',index = False)

duplicates.to_csv('three_hash_duplicates.csv',index = False)















