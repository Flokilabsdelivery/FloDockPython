# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 15:51:20 2024

@author: CBT
"""




import pandas as pd

config = pd.read_excel('config.xlsx',engine = 'openpyxl')

config = dict(list(zip(config['key'],config['value'])))


import difflib


def identify_misspelled_names(names):
    # Identify misspelled names (excluding identical names)

    misspelled_names = []

    for i, name1 in enumerate(names):

        for j, name2 in enumerate(names):

            # Skip comparing a name to itself

            if i != j:

                # Calculate similarity between names

                similarity = difflib.SequenceMatcher(None, name1, name2).ratio()

                # Set a threshold for similarity (you may need to adjust this)
                similarity_threshold = 0.8

                # If similarity is below the threshold, consider it misspelled
                if similarity > similarity_threshold and name1.lower() not in misspelled_names:

                    misspelled_names.append(name1.lower())

    return [i.upper() for i in misspelled_names]




df = pd.read_csv('three_hash_duplicates.csv')

final_df = df.copy()

mis_spelled = final_df[((final_df.duplicated(keep='first',subset = [config['LastName'],config['CustomerAddress'],config['CustomerDOB']])) | (final_df.duplicated(keep='last',subset = [config['LastName'],config['CustomerAddress'],config['CustomerDOB']])))]

mis_spelled_unique = mis_spelled[~(mis_spelled.duplicated([config['LastName'],config['CustomerAddress'],config['CustomerDOB']]))]

final_df = final_df[~((final_df.duplicated(keep='first',subset = [config['LastName'],config['CustomerAddress'],config['CustomerDOB']])) | (final_df.duplicated(keep='last',subset = [config['LastName'],config['CustomerAddress'],config['CustomerDOB']])))]

mis_spelled_duplicates_final = pd.DataFrame()

mis_spelled_unique.reset_index(inplace = True,drop = True)

for xy in range(0,len(mis_spelled_unique)):
    
    lastname = mis_spelled_unique.loc[xy,config['LastName']]

    address = mis_spelled_unique.loc[xy,config['CustomerAddress']]

    dob = mis_spelled_unique.loc[xy,config['CustomerDOB']]

    temp_df = mis_spelled[((mis_spelled[config['LastName']]==lastname) & (mis_spelled[config['CustomerAddress']]==address) & (mis_spelled[config['CustomerDOB']]==dob))]

    identical = identify_misspelled_names(list(temp_df[config['FirstName']]))
    
    if len(identical)>0:
        
        set1 = set(list(temp_df[config['FirstName']]))
    
        final_set = list(set1 - set(identical))
        
        final_set.append(identical[0])

        final_df = pd.concat([final_df,mis_spelled[mis_spelled[config['FirstName']].isin(final_set)]],axis= 0)

        final_set = identical[1:]

        mis_spelled_duplicates = mis_spelled[mis_spelled[config['FirstName']].isin(final_set)]
        
        mis_spelled_duplicates_final = pd.concat([mis_spelled_duplicates_final,mis_spelled_duplicates],axis = 0)
        
    else:
        
        final_df = pd.concat([final_df,temp_df],axis = 0)

    
mis_spelled_duplicates_final['valid'] = 'invalid'

mis_spelled_duplicates_final['reason'] = 'duplicates by mis-spelling logic'



mis_spelled_duplicates_final.to_csv('mis_spelled.csv',index = False)

final_df.to_csv('mis_spelled_unique.csv',index = False)


print('mis_spelling logic completed')






