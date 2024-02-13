import pandas as pd

import time

start_time = time.time()

import traceback

from fuzzywuzzy import process 

import difflib 

def deduplicate_strings(strings, threshold=80):

    deduped_strings = process.dedupe(strings, threshold=70)

    return deduped_strings

import sys

start_time = time.time()

sys.path.append(r'C:\Users\CBT\AppData\Local\Programs\Python\Python311\Lib\site-packages')

config = pd.read_excel('config.xlsx',engine = 'openpyxl')

config = dict(list(zip(config['key'],config['value'])))

import os

def list_all_files_in_drive(drive):

    all_files = []

    for root, dirs, files in os.walk(drive):

        for file in files:

            file_path = os.path.join(root, file)


            all_files.append(file_path)

    return all_files

drive_to_list = config['source_path']

files_in_drive = list_all_files_in_drive(drive_to_list)

files_location = []

for file in files_in_drive:

    file = file.replace('\\','/')

    list1 = file.split('/')

    list1.pop()

    list1 = '/'.join(list1)

    files_location.append(list1)

files_location = list(set(files_location))

count = 0

files_location = list(set(files_location))

count = 0

total_dataframe = pd.DataFrame()

mapping_config = pd.read_excel('business_configuration.xlsx',engine = 'openpyxl')

mapping_config.dropna(subset = ['File Name'],inplace = True)

mapping_config.dropna(subset = ['First Name'],inplace = True)

mapping_config.dropna(subset = ['Last Name'],inplace = True)

mapping_config.reset_index(inplace = True,drop = True)

mapping_config.fillna('',inplace = True)

mapping = pd.read_excel('column_mapping.xlsx',engine = 'openpyxl')

mapping.fillna('',inplace = True)

mapping = mapping.to_dict(orient = 'records')

files_location = list(set(files_location))

print(len(files_location))

files_location  = ['/STFS0029M/PPG Extractor/2023-08-11','/STFS0029M/PPG Extractor/2023-09-07','/STFS0029M/PPG Extractor/2023-09-24','/STFS0029M/PPG Extractor/2023-10-12']

print(files_location)

for i in files_location:

    csv_files = os.listdir(i)

    csv_files=['CORPORATE_TXN_BENE.csv']

    print(csv_files)

    for transaction_file in csv_files:

        try:        

            if (('.csv' in transaction_file) and (transaction_file in list(mapping_config['File Name'])) and ('E-LOADING' not in transaction_file)):

                print(transaction_file)

                print(i)
 
                with open('response1.txt','a') as a:

                     a.write(i+transaction_file+"\n")


                for row in range(len(mapping)):

                    if mapping[row]['Actual CSV Files']==transaction_file:

                        mapping1 = {

                            value: key for key, value in mapping[row].items()  if value!=''

                        }

                file1 = pd.read_csv(i+"//"+transaction_file, sep="|")

                current_config = mapping_config[mapping_config['File Name']==transaction_file]

                current_config.reset_index(inplace = True,drop = True)

                columns = []

                for j in file1.columns:

                    columns.append(j.upper())

                file1.columns = columns

                file1.rename(columns = {current_config.loc[0,'First Name'].upper():config['FirstName']},inplace = True)

                file1.rename(columns = {current_config.loc[0,'Last Name'].upper():config['LastName']},inplace = True)

                file1.rename(columns = {current_config.loc[0,'Address'].upper():config['ADDRESS1']},inplace = True)

                file1.rename(columns = {current_config.loc[0,'DOB'].upper():config['CustomerDOB']},inplace = True)

                file1.rename(columns = mapping1,inplace = True)

                # file1.to_csv('total_transaction.csv',index = False)

                if 'CONTACT_DETAILS' not in file1.columns:

                       file1['CONTACT_DETAILS'] = ''

                if config['CustomerDOB'] not in list(file1.columns):
                        
                        file1[config['CustomerDOB']] = ''

                missing_columns = set([config['FirstName'],config['LastName'],config['CustomerAddress'],config['CustomerDOB']]) - set(file1.columns) 

                if len(missing_columns)>1:

                    print('missing')

                    print('columns missing in file '+current_config.loc[0,'File Name']+" : "+','.join(missing_columns))

                    continue

                df = file1.copy() 

                with open('response_total.txt','a') as a:

                     a.write(str(len(df))+"\n")

                df[config['ADDRESS2']] = ''

                df[config['ADDRESS3']] = ''

                df[config['ADDRESS4']] = ''

                df[config['CustomerAddress']] = df[config['ADDRESS1']]

                df['floki_changes'] = ''

                print('Input file Length')

                print(len(df))

                df[config['FirstName']] = df[config['FirstName']].fillna('')

                df[config['LastName']] = df[config['LastName']].fillna('')

                df[config['CustomerAddress']] = df[config['CustomerAddress']].fillna('')

                df[config['FirstName']] = df[config['FirstName']].str.upper()

                df['CustomerLasttName'] = df[config['LastName']].str.upper()

                df[config['CustomerAddress']] = df[config['CustomerAddress']].str.upper()

                last_name_words = config['lastname_words']

                for words in last_name_words.split(','):

                    df[config['FirstName']] = df[config['FirstName']].str.replace(words.upper(),words.upper().replace(' ','-')) 
        
                    df[config['LastName']] = df[config['LastName']].str.replace(words.upper(),words.upper().replace(' ','-')) 

                df.to_csv('total_transaction.csv',index = False)

        except Exception as e:

            print(str(e))

            print(traceback.print_exc())

