
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 19:13:28 2023

@author: CBT
"""

import time

start_time = time.time()

import pandas as pd

import csv

import traceback

import hashlib

import json

import difflib

# from kafka import KafkaProducer

import sys

sys.path.append(r'C:\Users\CBT\AppData\Local\Programs\Python\Python311\Lib\site-packages')

config = pd.read_excel('config.xlsx',engine = 'openpyxl')

config = dict(list(zip(config['key'],config['value'])))

import configparser

import requests

#Reading files

import os

from unidecode import unidecode

import re

def hash(row,column,hash_value):

    columnName = 'hash_'


    # hashColumn = pd.Series()
    
    # for i in range((len(sourcedf[column[0]]))):

    concatstr = ''

    for j in column:

        concatstr = concatstr + row[j]

    row[hash_value] = hashlib.sha512( concatstr.encode("utf-8") ).hexdigest()
    
    return row


email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


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

def special_character_check_firstname(row):

    first_name = row['FIRSTNAME']
    
    last_name = row['LASTNAME']

    while(True):

        special_char = re.compile(r'[^a-zA-Z0-9.]')
    
        if special_char.search(row[config['FirstName']].replace(' ','').replace('-','')) != None:
            
            if len(row[config['LastName']].split(' '))>1:
                
                temp_last_name = row[config['LastName']].split(' ')
                
                row[config['FirstName']] = ' '.join(temp_last_name[0:len(temp_last_name)-1])
                
                row[config['LastName']] = temp_last_name[len(temp_last_name)-1]
            
            else:
                
                row['valid'] = 'invalid'
    
                if row['reason']=='':
                
                    row['reason'] = 'special characters in First name'
                    
                else:
                    
                    row['reason'] += ',Special characters in first name'


        if ((row['FIRSTNAME']==first_name) & (row['LASTNAME']==last_name)):
            
            break
        
        else:

            first_name = row['FIRSTNAME']
            
            last_name = row['LASTNAME']                
            
            pass


        row = single_character_check_firstname(row)

        row = single_character_check_lastname(row)

        row = number_check_firstname(row)

        row = number_check_lastname(row)
                
            
            
    return row

def special_character_check_lastname(row):
    
    first_name = row['FIRSTNAME']
    
    last_name = row['LASTNAME']

    while(True):


        special_char = re.compile(r'[^a-zA-Z0-9.]')

#        print(row['LASTNAME'])


#        print(special_char.search(row[config['FirstName']].replace(' ','').replace('-','')) != None)
        
        if special_char.search(row[config['LastName']].replace(' ','').replace('-','')) != None:
            
            if len(row[config['FirstName']].split(' '))>1:
                
                temp_last_name = row[config['FirstName']].split(' ')
                
                row[config['FirstName']] = ' '.join(temp_last_name[0:len(temp_last_name)-1])
                
                row[config['LastName']] = temp_last_name[len(temp_last_name)-1]
            
            else:
                
                row['valid'] = 'invalid'
                
                
                if row['reason']=='':
                
                    row['reason'] = 'Special characters in last name'
                    
                else:
                    
                    row['reason'] += ',Special characters in last name'
                    

        if ((row['FIRSTNAME']==first_name) & (row['LASTNAME']==last_name)):
            
            break
        
        else:

            first_name = row['FIRSTNAME']
            
            last_name = row['LASTNAME']                
            
            pass


        row = single_character_check_firstname(row)

        row = single_character_check_lastname(row)

        row = number_check_firstname(row)

        row = number_check_lastname(row)
                
        row = special_character_check_firstname(row)

    return row

def check_phonenumber_format(row):

	contact_details = str(row['CONTACT_DETAILS'])
	
	if contact_details != 'nan':
        	
		contact_details = contact_details.replace(" ", "").upper()
		
		if contact_details.startswith('9'):
            		
			contact_details = '+63' + contact_details

		elif contact_details.startswith('0'):

           		contact_details = '+63' + contact_details[1:]

		pattern = re.compile(r'^\+?63(\d{10})$')
        		
		if re.match(pattern, contact_details):
            
			row['CONTACT_DETAILS'] = contact_details

			row['PHONE_ERROR_FORMAT'] = 0
		else:

		        row['CONTACT_DETAILS'] = contact_details
        		
		        row['PHONE_ERROR_FORMAT'] = 1

		if row['CONTACT_DETAILS'] == '+63':
            
		        row['CONTACT_DETAILS'] = ''

	row['CONTACT_DETAILS'] = str(row['CONTACT_DETAILS'])
    					
	return row

def add_country_code(contact):
    if contact and contact.startswith('9') and len(contact) == 10:
        return '+63' + contact
    return contact

def add_country_code1(contact):
    if contact and contact.startswith('09') and len(contact) == 11:
        return '+63' + contact[1:] 
    return contact


def add_country_code2(contact):
    if contact and contact.startswith('63') and len(contact) == 12:
        return '+' + contact
    return contact

def GYU(row):
    
    if 'GYU' in row[config['FirstName']]:
        
        row[config['FirstName']] = row[config['FirstName']].replace('GYU ','')
        
        splitted_words = row[config['FirstName']].split('#')
        
        if len(splitted_words)>1:
    
            splitted_words.pop()        
        
        splitted_words = splitted_words[0].split(' ')
        
        temp_last_name = splitted_words


        # temp_last_name = row[config['FirstName']].split(' ')
        
        row[config['FirstName']] = ' '.join(temp_last_name[0:len(temp_last_name)-1])
        
        row[config['LastName']] = temp_last_name[len(temp_last_name)-1]
        

        
    elif 'GYU ' in row[config['LastName']]:
        
        row[config['LastName']] = row[config['LastName']].replace('GYU ','')
        
        splitted_words = row[config['LastName']].split('#')

        if len(splitted_words)>1:
    
            splitted_words.pop()        
 
        splitted_words = splitted_words[0].split(' ')
        
        temp_last_name = splitted_words

        # temp_last_name = row[config['FirstName']].split(' ')
        
        row[config['FirstName']] = ' '.join(temp_last_name[0:len(temp_last_name)-1])
        
        row[config['LastName']] = temp_last_name[len(temp_last_name)-1]
        
            
    return row        
        
        

def number_check_firstname(row):
    
    first_name = row['FIRSTNAME']
    
    last_name = row['LASTNAME']

    while(True):

    
        if len(re.findall(r'[0-9]+', row[config['FirstName']]))>0:
            
            
            if len(row[config['LastName']].split(' '))>1:
                
                
                temp_last_name = row[config['LastName']].split(' ')
                
                row[config['FirstName']] = ' '.join(temp_last_name[0:len(temp_last_name)-1])
                
                row[config['LastName']] = temp_last_name[len(temp_last_name)-1]
            
            else:
                
                
                row['valid'] = 'invalid'
    
                if row['reason']=='':
                
                    row['reason'] = 'Numeric characters in First name'
                    
                else:
                    
                    row['reason'] += ',Numeric characters in first name'
            

        if ((row['FIRSTNAME']==first_name) & (row['LASTNAME']==last_name)):
            
            break
        
        else:

            first_name = row['FIRSTNAME']
            
            last_name = row['LASTNAME']                
            
            pass


        row = single_character_check_firstname(row)

        row = single_character_check_lastname(row)
            
    return row




def number_check_lastname(row):

    first_name = row['FIRSTNAME']
    
    last_name = row['LASTNAME']

    while(True):
    
        if len(re.findall(r'[0-9]+', row[config['LastName']]))>0:
            
            if len(row[config['FirstName']].split(' '))>1:
                
                temp_last_name = row[config['FirstName']].split(' ')
                
                row[config['FirstName']] = ' '.join(temp_last_name[0:len(temp_last_name)-1])
                
                row[config['LastName']] = temp_last_name[len(temp_last_name)-1]
            
            else:
                
                row['valid'] = 'invalid'
                
                
                if row['reason']=='':
                
                    row['reason'] = 'Numeric characters in last name'
                    
                else:
                    
                    row['reason'] += ',Numeric characters in last name'


        if ((row['FIRSTNAME']==first_name) & (row['LASTNAME']==last_name)):
            
            break
        
        else:
            
            first_name = row['FIRSTNAME']
            
            last_name = row['LASTNAME']                
            
            pass


        row = single_character_check_firstname(row)

        row = single_character_check_lastname(row)

        row = number_check_firstname(row)

    return row



def single_character_check_firstname(row):
    
    if len(row[config['FirstName']])<2:
        
        if len(row[config['LastName']].split(' '))>1:
            
            temp_last_name = row[config['LastName']].split(' ')
            
            row[config['FirstName']] = ' '.join(temp_last_name[0:len(temp_last_name)-1])
            
            row[config['LastName']] = temp_last_name[len(temp_last_name)-1]
            

        
        else:
            
            row['valid'] = 'invalid'
            
            if row[config['FirstName']]=='':
                    
                row['reason'] = 'Null Value in first name'

            else:
                
                row['reason'] = 'Single character in first name'
            
    return row

    
def single_character_check_lastname(row):
    

    first_name = row['FIRSTNAME']
    
    last_name = row['LASTNAME']

    while(True):
    
        if len(row[config['LastName']])<2:
            
            if len(row[config['FirstName']].split(' '))>1:
                
                temp_last_name = row[config['FirstName']].split(' ')
                
                row[config['FirstName']] = ' '.join(temp_last_name[0:len(temp_last_name)-1])
                
                row[config['LastName']] = temp_last_name[len(temp_last_name)-1]
                
            
            else:
                
                row['valid'] = 'invalid'
                
                if row[config['LastName']]=='':
                    
                
                    if row['reason']=='':
                    
                        row['reason'] = 'Null value in last name'
                        
                    else:
                        
                        row['reason'] += ',Null value in last name'
                
                else:
                    
                    if row['reason']=='':
                    
                        row['reason'] = 'Single character in last name'
                        
                    else:
                        
                        row['reason'] += ',Single character in last name'
    

        
            row = single_character_check_firstname(row)
        
        if ((row['FIRSTNAME']==first_name) & (row['LASTNAME']==last_name)):
            
            break
        
        else:
            
            first_name = row['FIRSTNAME']
            
            last_name = row['LASTNAME']                

            pass


    return row
    

def change_accent(row):

    row[config['FirstName']]= unidecode(row[config['FirstName']])

    row[config['LastName']]= unidecode(row[config['LastName']])

    row[config['CustomerAddress']]= unidecode(row[config['CustomerAddress']])

    return row


def list_all_files_in_drive(drive):

    all_files = []

    for root, dirs, files in os.walk(drive):

        for file in files:

            file_path = os.path.join(root, file)

            all_files.append(file_path)

    return all_files

config_parser = configparser.ConfigParser()

config_parser.read_string('[default]\n' + open('config.properties').read())

CDMS_properties = {}

for option in config_parser.options('default'):
    CDMS_properties[option] = config_parser.get('default', option)

process_name=''

if __name__ == "__main__":
    
    if len(sys.argv) > 1:

        process_name = sys.argv[1]

        print(f"Process Name: {process_name}")

    else:

        print("No process name provided.")

drive_to_list = CDMS_properties['source_path']

files_in_drive = list_all_files_in_drive(drive_to_list)

files_location = []

print(files_in_drive)

for file in files_in_drive:
    
    file = file.replace('\\','/')
    
    list1 = file.split('/')    
    
    # list1.pop()
    
    list1 = '/'.join(list1)
                       
    files_location.append(list1)



files_location = list(set(files_location))


count = 0

total_dataframe = pd.DataFrame()

print(files_location)
# files_location = files_location[0:1]

# files_location=['/STFS0029M/CDMS/AUG/2023-08-01']

for file_path in files_location:

    try:
        
        i, filename = os.path.split(file_path)

        if (filename) in os.listdir(i) and filename.endswith('.csv'):
            
            print(i,filename)
            
            # print(i)

            url = CDMS_properties['main_app'] + 'crm/getDudupStatus'

            df_ = pd.read_csv(i+"//"+filename)

            total_rows = len(df_)

            preProcess_body = {
            
                "fileName":"CDMS_valid_"+filename,
            
                "inputLocation":i,

                "inputCount":total_rows,
            
                "processName": process_name,

                "origin":'CDMS',

                "status":'Processing',

                "subListID":76,
            
                "userID":149,
            
                "businessHierarchyId":23
            }

            response = requests.post(url = CDMS_properties['main_app']+'crm/saveDedupStatus',headers = {'X-AUTH-TOKEN':CDMS_properties['x-auth-token'],'Content-Type':'application/json'},json = preProcess_body)

            content =False

            if response.status_code == 200:
                # Parse JSON response
                response_data = response.json()
                content = response_data['content']  # Extract the 'content' field from the response
                print("Content:", content)
            else:
                print("Request failed with status code:", response.status_code)

            if not content:
                continue

            field_id=content    

            cunk_size = 30000

            if os.path.exists(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//valid//temp_valid_"+filename):

                os.remove(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//valid//temp_valid_"+filename)

            if os.path.exists(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//invalid//invalid_"+filename):

                os.remove(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//invalid//invalid_"+filename)

            if os.path.exists(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//valid//corporate_customers"+filename):

                os.remove(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//valid//corporate_customers"+filename)

            for j, chunk_df in enumerate(pd.read_csv(i+"//"+filename, chunksize=cunk_size, low_memory=False)):

                # continue

                start_index = j * cunk_size

                end_index = min((j + 1) * cunk_size, total_rows)

                print(f"Processing chunk {j+1}: Rows {start_index}-{end_index}")

                CDMS_merged = df_[start_index:end_index]
            
                # file1 = pd.read_csv(i+"//"+CDMS_properties['cdms_file1'], sep="|")
                
                # file2 = pd.read_csv(i+'//'+CDMS_properties['cdms_file2'], sep="|")
                
                # file3 = pd.read_csv(i+"//"+CDMS_properties['cdms_file3'], sep="|")
                
                # file4 = pd.read_csv(i+'//'+CDMS_properties['cdms_file4'], sep="|")

                # file3['sort'] = 15

                # file3.loc[((file3['IsCurrent'] == 1) & (file3['ResidenceType'] == 1)),'sort'] = 1

                # file3.loc[((file3['IsCurrent'] == 0) & (file3['ResidenceType'] == 1)),'sort'] = 2 

                # file3.loc[((file3['IsCurrent'] == 1) & (file3['ResidenceType'] == 2)),'sort'] = 3

                # file3.loc[((file3['IsCurrent'] == 0) & (file3['ResidenceType'] == 2)),'sort'] = 4

                # file3.loc[((file3['IsCurrent'] == 1) & (file3['ResidenceType'] == 3)),'sort'] = 5

                # file3.loc[((file3['IsCurrent'] == 1) & (file3['ResidenceType'] == 4)),'sort'] = 6

                # file3.loc[((file3['IsCurrent'] == 0) & (file3['ResidenceType'] == 3)),'sort'] = 7
    
                # file3.loc[((file3['IsCurrent'] == 0) & (file3['ResidenceType'] == 4)),'sort'] = 8

                # file3.loc[((file3['IsCurrent'] == 1) & (file3['ResidenceType'] == 5)),'sort'] = 9

                # file3.loc[((file3['IsCurrent'] == 0) & (file3['ResidenceType'] == 5)),'sort'] = 10

                # file3.sort_values(['CustomerNumber','sort'],inplace = True,ascending = True)

                # file3.drop_duplicates(['CustomerNumber'],inplace = True)



            
                headers = pd.read_csv('single_header_match.csv')
                
                headers = dict(list(zip(headers['key'],headers['value'])))
                
                CDMS_merged.rename(columns = headers,inplace = True)

                # file1.rename(columns = headers,inplace = True)
                
                # file2.rename(columns = headers,inplace = True)
                
                # file3.rename(columns = headers,inplace = True)
                
                # file4.rename(columns = headers,inplace = True)
                    
                

                # file3.loc[file3['sort']==15,config['ADDRESS1']] = ''

                # file3.loc[file3['sort']==15,config['ADDRESS2']] = ''

                # file3.loc[file3['sort']==15,config['ADDRESS3']] = ''



                
                # #Merging all the files
                # file3.loc[file3['sort']==15,config['ADDRESS4']] = '' 


                # CDMS_merged = pd.merge(file1,file2,how = 'left',on = [config['customer_id']])
                
                # CDMS_merged = pd.merge(CDMS_merged,file3,how = 'left',on = [config['customer_id']])
                
                # CDMS_merged = pd.merge(CDMS_merged,file4,how = 'left',on = [config['customer_id']])
                
                # print('missed columns:',set(CDMS_merged) - set(headers.values()))
                
                #merging_address
                
                
                
                CDMS_merged[config['CustomerAddress']] = CDMS_merged[config['ADDRESS1']] + CDMS_merged[config['ADDRESS2']] + CDMS_merged[config['ADDRESS3']] + CDMS_merged[config['ADDRESS4']]
        
                #Columns rename
                
                # renaming_columns = dict(list(zip(config['columns_present'].split(','),config['columns_to_be_changed'].split(','))))
                
                # CDMS_merged.rename(columns = renaming_columns,inplace = True)
                
                # print(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with']+"//CDMS_output.csv"))
                
                #Creating Hash Code function
                
                
                CDMS_merged_HASH_1 = pd.DataFrame()
                
                CDMS_merged_HASH_2 = pd.DataFrame()
                
                # hash(CDMS_merged,CDMS_merged_HASH_1,config['HASH_1_columns'].split(','))
                
                # CDMS_output = pd.concat([CDMS_merged,CDMS_merged_HASH_1],axis = 1)
                
                # CDMS_output.rename(columns = {'hash_'+''.join(config['HASH_1_columns'].split(',')):'HASH_1'},inplace = True)
                
                # hash(CDMS_merged,CDMS_merged_HASH_2,config['HASH_2_columns'].split(','))
                
                # CDMS_output = pd.concat([CDMS_output,CDMS_merged_HASH_2],axis = 1)
                
                # CDMS_output.rename(columns = {'hash_'+''.join(config['HASH_2_columns'].split(',')):'HASH_2'},inplace = True)
                
                # CDMS_output = CDMS_output[config['output_columns'].split(',')]
                
                CDMS_output = CDMS_merged.copy()
                
    #            print(i.replace(config['replace_string'],config['replace_with'])+"//CDMS_output.csv")
                
                if os.path.exists(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])):
                    
                    pass
                
                else:
                    
                    os.makedirs(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with']))
        
        
        
        
                
                # CDMS_output.to_csv(i.replace(config['replace_string'],config['replace_with'])+"//CDMS_output.csv",index = False)
                
                
        
                
                # print(business.loc[i,'File Name'])
                
                df = CDMS_output.copy()
                
                # print(df[df['CUSTOMER_ID']==26536694]['LASTNAME'])
                
                errored_headers = ['EMAIL','LANDLINE_NO','EXPIRYDATE','LOAD_DT','ISSUEDATE','DATEOFBIRTH']
                
                
                print('Input file Length')
                
                print(len(df))
                
                
                
                #rule1 upper case and accent change
                
                
                
                df[config['FirstName']] = df[config['FirstName']].fillna('')   
                
                df[config['LastName']] = df[config['LastName']].fillna('')   
                
                df[config['CustomerAddress']] = df[config['CustomerAddress']].fillna('')   
                        
                df[config['FirstName']] = df[config['FirstName']].str.upper()   
                
                df[config['LastName']] = df[config['LastName']].str.upper()   
                
                df[config['CustomerAddress']] = df[config['CustomerAddress']].str.upper()  

                # print(df[df['CUSTOMER_ID']==26536694]['LASTNAME'])
        
                #dela cruz
                
                last_name_words = config['lastname_words']
                
                for words in last_name_words.split(','):
                    
                    df[config['FirstName']] = df[config['FirstName']].str.replace(words.upper(),words.upper().replace(' ','-')) 
        
                    df[config['LastName']] = df[config['LastName']].str.replace(words.upper(),words.upper().replace(' ','-')) 
        
                #GYU code
                    
                df = df.apply(lambda row:GYU(row),axis = 1)
                
                        
        
                # print(df[df['CUSTOMER_ID']==26536694]['LASTNAME'])
                #change_accent
                
                for column in df.columns:
                    
                    df[column] = df[column].astype(str)
                    
                    df[column] = df[column].apply(lambda x: unidecode(str(x)) if pd.notnull(x) else x)
                    
                    df[column] = df[column].str.replace(',',';')
                    
                # print(df[df['CUSTOMER_ID']=='26536694']['LASTNAME'])
                
                
                df = df.apply(lambda row:change_accent(row),axis = 1)
                
                # print(df[df['CUSTOMER_ID']=='26536694']['LASTNAME'])
                #email validation
                
                for column in ['EMAIL','LANDLINE_NO']:
                    
                    df[column+'_error'] = df[column].copy()
                    

                print("before Email")

                df.loc[~(df['EMAIL'].str.contains(email_regex)),'floki_changes']= 'invalid Email so replaced as null;'
                            
                df['EMAIL']= df[df['EMAIL'].str.contains(email_regex, na=False)]['EMAIL']
                print("after Email") 
                #landline number validation
                
                df['LANDLINE_CHECK'] = df['LANDLINE_NO']
                
                df['LANDLINE_NO'] = pd.to_numeric(df['LANDLINE_NO'],errors = 'coerce')
                
                
                df.loc[df['LANDLINE_NO'].isna(),'floki_changes'] += 'invalid landline no;'


                #date format
                
                df.rename(columns = {'EXPIRYDATE_x':'EXPIRYDATE','LOAD_DT_x':'LOAD_DT'},inplace = True)
                        
                        
                for column in ['EXPIRYDATE','LOAD_DT','ISSUEDATE','DATEOFBIRTH']:
                    
                    df[column+'_error'] = df[column].copy()

                
                
                df['ISSUEDATE'] = pd.to_datetime(df['ISSUEDATE'],format = '%Y-%m-%dT%H:%M:%S.%fZ',errors = 'coerce')

                df['ISSUEDATE'] = df['ISSUEDATE'].dt.strftime('%m/%d/%Y')
                
                df['ISSUEDATE'].fillna('',inplace = True)

                df['EXPIRYDATE'] = pd.to_datetime(df['EXPIRYDATE'],format = '%Y-%m-%dT%H:%M:%S.%fZ',errors = 'coerce')

                df['EXPIRYDATE'] = df['EXPIRYDATE'].dt.strftime('%m/%d/%Y')
                
                df['EXPIRYDATE'].fillna('',inplace = True)

                df['DATEOFBIRTH'] = pd.to_datetime(df['DATEOFBIRTH'],format = '%Y-%m-%dT%H:%M:%S.%fZ',errors = 'coerce')

                df['DATEOFBIRTH'] = df['DATEOFBIRTH'].dt.strftime('%m/%d/%Y')
                
                df['DATEOFBIRTH'].fillna('',inplace = True)

                df['LOAD_DT'] = pd.to_datetime(df['LOAD_DT'],format = '%Y-%m-%dT%H:%M:%S.%fZ',errors = 'coerce')

                df['LOAD_DT'] = df['LOAD_DT'].dt.strftime('%m/%d/%Y')
                
                df['LOAD_DT'].fillna('',inplace = True)

                gender_map = {'M': 'Male', 'F': 'Female'}

                df['GENDER'] = df['GENDER'].map(gender_map).fillna(df['GENDER'])

                status_map = {'U': 'Unmarried', 'M': 'Married', 'S': 'Seprated', 'W': 'Widowed','D': 'Divorced','A':'Annuled'}

                df['CIVILSTATUS'] = df['CIVILSTATUS'].map(status_map).fillna(df['CIVILSTATUS'])

                minor_map = {'False': 'No', 'True': 'Yes'}

                df['IS_MINOR'] = df['IS_MINOR'].map(minor_map).fillna(df['IS_MINOR'])

                df.loc[df['ISSUEDATE']=='','floki_changes']+='issuedate not in format or empty;'

                df.loc[df['EXPIRYDATE']=='','floki_changes']+='expiry date not in format or empty;'

                df.loc[df['DATEOFBIRTH']=='','floki_changes']+='DOB not in format or empty;'

                df.loc[df['LOAD_DT']=='','floki_changes']+='LOAD_DT not in format or empty;'

                # df['ISSUEDATE'] = pd.to_datetime(df['ISSUEDATE'],format = '%Y-%m-%dT%H:%M:%S.%fZ')

                #adding suffix
                                
                suffixes = [' JR.',' SR.',' JR', ' SR',' I', ' II', ' III', ' IV', ' V']    
                
                df['SUFFIX'] = ''
                
                for suffix in suffixes:
                    
                    # df.loc[df[config['FirstName']].str.contains(suffix),'SUFFIX'] = suffix 
                
                    # df[config['FirstName']]=  df[config['FirstName']].str.replace(suffix,'')
                
                    # df.loc[df[config['LastName']].str.contains(suffix),'SUFFIX'] = suffix 
                
                    # df[config['LastName']] = df[config['LastName']].str.replace(suffix,'')

                    pattern = re.escape(suffix) + r'\b'
                     # Check and update FirstName
                    df.loc[df[config['FirstName']].str.contains(suffix), 'SUFFIX'] = df.loc[df[config['FirstName']].str.contains(suffix), config['FirstName']].apply(lambda x: re.search(pattern, x).group() if re.search(pattern, x) is not None else '')
                    df.loc[df[config['LastName']].str.contains(suffix), 'SUFFIX'] = df.loc[df[config['LastName']].str.contains(suffix), config['LastName']].apply(lambda x: re.search(pattern, x).group() if re.search(pattern, x) is not None else '')
                    df[config['FirstName']] = df[config['FirstName']].apply(lambda x: re.sub(pattern, '', x))
                    df[config['LastName']] = df[config['LastName']].apply(lambda x: re.sub(pattern, '', x))
                            
                # corporate customers
                
                print('corporate customers')
                
                corp_name_pattern = ['ACADEMY ', ' ACADEMY', 'TECHNOLOGY ', ' TECHNOLOGY', 'TECHNO ', ' TECHNO', 'STALL ', ' STALL', 'SERVICES ', ' SERVICES', 'BRANCH ', ' BRANCH', 'OUTLET ', ' OUTLET', 'EXPRESS ', ' EXPRESS', 'CENTER ', ' CENTER', 'BUSINESS ', ' BUSINESS', 'CORPORATION ', ' CORPORATION', 'COMPANY ', ' COMPANY', ' INC ', '  INC', 'INC  ', ' INC ', 'COURIER ', ' COURIER', 'COOPERATIVE ', ' COOPERATIVE', 'BANK ', ' BANK', 'SECURITY ', ' SECURITY', 'DISTRIBUTOR ', ' DISTRIBUTOR', 'DISTILLERS ', ' DISTILLERS', 'PHARMACY ', ' PHARMACY', 'MOTORS ', ' MOTORS', 'SCHOOL ', ' SCHOOL', 'TRADEING ', ' TRADEING', 'ACCOUNTS ', ' ACCOUNTS', 'ASSOCIATION ', ' ASSOCIATION', 'UNIV ', ' UNIV', 'COLLEGES ', ' COLLEGES', 'MERCHANT/MERCHANDIZING ', ' MERCHANT/MERCHANDIZING', 'STORE ', ' STORE', 'PHILS ', ' PHILS', 'INSTITUTE ', ' INSTITUTE', 'LIMITED ', ' LIMITED', 'ENTERPRISES ', ' ENTERPRISES', 'VENTURES ', ' VENTURES', 'SHOP ', ' SHOP', 'BOUTIQUE ', ' BOUTIQUE', 'CLINIC ', ' CLINIC', 'HOSPITAL ', ' HOSPITAL', 'FINANCIAL ', ' FINANCIAL', 'PETROL ', ' PETROL', 'GASSTATION ', ' GASSTATION', 'FUEL ', ' FUEL', 'DRUG ', ' DRUG', 'TRAVEL ', ' TRAVEL', 'TOURS ', ' TOURS', 'TOURISM ', ' TOURISM', 'RESTAURANT ', ' RESTAURANT', 'LTD ', ' LTD', 'FINANCE ', ' FINANCE', 'REGION ', ' REGION', 'MARKETING ', ' MARKETING', 'DOLE NCR ', ' DOLE NCR', 'FOOD ', ' FOOD', 'BAKERY ', ' BAKERY', 'CONSTRUCTION ', ' CONSTRUCTION', 'BUILDERS ', ' BUILDERS', 'SUPPLY MATERIALS ', ' SUPPLY MATERIALS', 'JEWELRY ', ' JEWELRY', 'JEWELERS ', ' JEWELERS', 'EDUCATIONAL ', ' EDUCATIONAL', 'AUTO ', ' AUTO', 'MOTORCYCLE ', ' MOTORCYCLE', 'PARTS ', ' PARTS', 'INSURANCE ', ' INSURANCE', 'HEALTH ', ' HEALTH', 'WELLNESS ', ' WELLNESS', 'REALESTATE ', ' REALESTATE', 'PROPERTIES ', ' PROPERTIES']
                
                df['CORPORATE'] = False
                
                for corporate_key in corp_name_pattern:
                    
                    df_temp = df[df['CORPORATE']==False]
                    
                    df = df[df['CORPORATE']==True]

                    corporate_key = re.escape(corporate_key) + r'\b'
                            
                    df_temp['CORPORATE'] = df_temp[config['FirstName']].str.contains(corporate_key)
                    
                    df = pd.concat([df,df_temp],axis = 0)        
                    
                    df_temp = df[df['CORPORATE']==False]
                    
                    df = df[df['CORPORATE']==True]
                    
                    df_temp['CORPORATE'] = df_temp[config['LastName']].str.contains(corporate_key)
                    
                    df = pd.concat([df,df_temp],axis = 0)        
                    
                df['valid'] = 'valid'
                
                df['reason'] = ''
                
                #using branch codes
                
                branch_codes = pd.read_excel('branch_code.xlsx',engine = 'openpyxl')
                
                branch_codes1 = dict(list(zip(branch_codes['PEPP Code'],branch_codes['Partner Name'])))
                
                df['some'] = ''
        
                df.loc[((df['CORPORATE']=='False') & (df['BRANCHCODE'].isin(branch_codes['PEPP Code']))),'CORPORATE'] = True
                
                df.loc[((df['CORPORATE']=='False') & (df['BRANCHCODE'].isin(branch_codes['PEPP Code']))),'some'] = df.loc[((df['CORPORATE']=='False') & (df['BRANCHCODE'].isin(branch_codes['PEPP Code']))),'BRANCHCODE']
                
                df['some'] = df['some'].replace(branch_codes1)
                
                df.loc[((df['CORPORATE']=='False') & (df['BRANCHCODE'].isin(branch_codes['PEPP Code']))),config['LastName']] = df.loc[((df['CORPORATE']=='False') & (df['BRANCHCODE'].isin(branch_codes['PEPP Code']))),'some']
                
                df.drop(columns = ['some'],inplace = True)
                
                corporate_customers = df[df['CORPORATE'] == True]
                
                df = df[df['CORPORATE']==False]
                
                #single character
                
                # df['count'] = df[config['FirstName']].str.len()
                
                # df_temp = df[df['count']<2]
                
                # df = df[df['count']>=2]
                
                # temp_split = df_temp[config['LastName']].str.split(' ')
                
                # df_temp = pd.concat([df_temp,temp_split],axis = 1)
                
                # valid_count = 0
                
                # invalid_count = 0
                
                print(time.time() - start_time)
                
                
                # while(True):
                
                print()
                
                print('single character check')
                
                
                df = df.apply(lambda row:single_character_check_firstname(row),axis = 1)
                
                print('first name completed')
                
                # df = df[0:10]
                
                df = df.apply(lambda row:single_character_check_lastname(row),axis = 1)
                
                print()
                
                print('numeric character check')
                
                df = df.apply(lambda row:number_check_firstname(row),axis = 1)
                
                df = df.apply(lambda row:number_check_lastname(row),axis = 1)
                
    #            print(df['valid'])
                
                print('contact details check')
                
                df['length'] = df['CONTACT_DETAILS'].str.len()
                
                # df.loc[(df['length']==10) & (df['CONTACT_DETAILS'])]
                
                df['CONTACT_DETAILS'].fillna('',inplace = True)
                
    #            df_valid = ((df['CONTACT_DETAILS'].str.len()==10) & (df['CONTACT_DETAILS'].str.startswith('9')) | ((df['CONTACT_DETAILS'].str.len()==11) & (df['CONTACT_DETAILS'].str.startswith('0'))) | ((df['CONTACT_DETAILS'].str.len()==12) & (df['CONTACT_DETAILS'].str.startswith('6'))) | (df['CONTACT_DETAILS']==''))
                
    #            df_invalid_phone = ~((df['CONTACT_DETAILS'].str.len()==10) & (df['CONTACT_DETAILS'].str.startswith('9')) | ((df['CONTACT_DETAILS'].str.len()==11) & (df['CONTACT_DETAILS'].str.startswith('0'))) | ((df['CONTACT_DETAILS'].str.len()==12) & (df['CONTACT_DETAILS'].str.startswith('6'))) | (df['CONTACT_DETAILS']==''))
                
                # df.loc[df_valid,'valid'] = 'valid'
                
    #            df.loc[df_invalid_phone,'valid'] = 'invalid'
        
    #            df.loc[df_invalid_phone,'reason'] = 'phone number is invalid'
                
                # print(df[df['CONTACT_DETAILS']=='0']['valid'].unique())             
        
                # print()    
                
    #            print(df['valid'])
                
                
                print('special character check')
    #            print(df['valid'])
    #            df['CUSTOMER_ID'] = df['CUSTOMER_ID'].astype(str)

    #            df = df[df['CUSTOMER_ID']=='7734889']

                df['PHONE_ERROR_FORMAT'] = ''
                
                # df = df.apply(lambda row:check_phonenumber_format(row),axis = 1)
                df['CONTACT_DETAILS'] = df['CONTACT_DETAILS'].astype(str).apply(lambda x: x[:-2] if x.endswith('.0') else x)
                df['CONTACT_DETAILS'] = df['CONTACT_DETAILS'].apply(add_country_code)
                df['CONTACT_DETAILS'] = df['CONTACT_DETAILS'].apply(add_country_code1)
                df['CONTACT_DETAILS'] = df['CONTACT_DETAILS'].apply(add_country_code2)
                
                df = df.apply(lambda row:special_character_check_firstname(row),axis = 1)
                
                df = df.apply(lambda row:special_character_check_lastname(row),axis = 1)
                
    #            print(df['valid'])

                    
                    # if ((valid_count == df['valid'].value_counts()['valid']) and (invalid_count == df['valid'].value_counts()['invalid'])):
                        
                    #     break
        
                    # else:
                        
                    #     valid_count = df['valid'].value_counts()['valid']
                        
                    #     invalid_count = df['valid'].value_counts()['invalid']
                        
                print(time.time() - start_time)

                    
                
                missing_columns = set(config['HASH_1_columns'].split(',')) - set(df.columns)
                
                for xy in missing_columns:
                    
                    df[xy] = ''
                
                missing_columns = set(config['HASH_2_columns'].split(',')) - set(df.columns)
                
                for xy in missing_columns:
                    
                    df[xy] = ''
                
                if 'CustomerBirthDate' in df.columns:
                    
                    df['CustomerBirthDate'] = df['CustomerBirthDate'].fillna('')
                
                
                df1 = pd.DataFrame()
                
                df2 = pd.DataFrame()
                
                
                print('Hash code generation started')
                
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

                #print(df[df['CONTACT_DETAILS']=='0']['valid'].unique())             

                

                # total_dataframe  = pd.concat([total_dataframe,df],axis = 0)
                
                # print(len(total_dataframe))
                
                final_df = df.copy()

                
                

                    
                count = count+1
                    

                # final_df = total_dataframe.copy()
                
                final_df_duplicates1 = final_df[final_df.duplicated(['HASH_1'])]
                
                # final_df = final_df[~(final_df.duplicated(['HASH_1']))]
                
                final_df_duplicates2 = final_df[final_df.duplicated(['HASH_2'])]
                
                # final_df = final_df[~(final_df.duplicated(['HASH_2']))]
                
                final_df_duplicates = pd.concat([final_df_duplicates1,final_df_duplicates2],axis = 0)                    
                
                final_df_duplicates['valid'] = 'invalid'

    #            print(final_df[final_df['CONTACT_DETAILS']=='0']['valid'].unique())             

                    
                # final_df_duplicates['reason'] +=',' 
                
                final_df_duplicates.loc[final_df_duplicates['reason']=='','reason'] = 'duplicates in raw data'
                
                final_df_duplicates.loc[final_df_duplicates['reason']!='','reason'] += 'duplicates in raw data'
                
    #            print(final_df[final_df['CONTACT_DETAILS']=='0']['valid'].unique())             
                
                #mis spelling logic
                print('mis spelling logic')
                
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
                
                # final_df_duplicates = final_df[final_df.duplicated(['HASH_2'])]
                
                # final_df = final_df[~(final_df.duplicated(['HASH_2']))]
                
                # final_df_duplicates['valid'] = 'invalid'
                    
                # # final_df_duplicates['reason'] +=',' 
                
                # final_df_duplicates.loc[final_df_duplicates['reason']=='','reason'] = 'duplicates in raw data'
                
                # final_df_duplicates.loc[final_df_duplicates['reason']!='','reason'] += 'duplicates in raw data'
                
                
                # cdms = pd.read_csv('CDMS_merged.csv')
                
                
                
                
    #            hashcode chcek API

                # print(time.time() - start_time)
                            
                # print(hello)
                            
                # duplicate_hash_df = pd.DataFrame()
                
                # duplicate_hash_list = []
                
                # for xy in range(0,(len(final_df)//500)):
                    
                #     hash_codes = final_df['HASH_1'][(xy*500):((xy*500)+500)]
                
                #     body = {"hashCodes":list(hash_codes)}
                
                #     response = requests.post(url = 'http://mr403s0332d.palawangroup.com:4200/getCustomerDataby3Hashcode',headers = {'X-AUTH-TOKEN':'eyJ1c2VybmFtZSI6InN5c3RlbSIsInRva2VuIjoiODRjOWZmNmQtZTllMy00MWUwLWI0MDctZmY5ZGQ5YjFmYWU4In0=','Content-Type':'application/json'},json = body,params = {'BusinessId':'9','isCustomer':True})
                
                #     duplicate_hashcodes = response.json()     
                    
                #     print()
                        
                #     print(response.status_code)
                
                    
                #     # duplicate_hash = final_df[final_df['HASH_1'].isin(duplicate_hashcodes)]
                    
                #     duplicate_hash_list.extend(duplicate_hashcodes)
                    
                #     # duplicate_hash_df = pd.concat([duplicate_hash_df,duplicate_hash],axis = 0)
                    
                #     # valid_output = valid_output[~(valid_output['HASH_1'].isin(duplicate_hashcodes))]
                
                
                
                # hash_codes = final_df[(len(final_df)//500)*500:]
                
                # body = {"hashCodes":list(hash_codes)}
                
                # response = requests.post(url = 'http://mr403s0332d.palawangroup.com:4200/getCustomerDataby3Hashcode',headers = {'X-AUTH-TOKEN':'eyJ1c2VybmFtZSI6InN5c3RlbSIsInRva2VuIjoiODRjOWZmNmQtZTllMy00MWUwLWI0MDctZmY5ZGQ5YjFmYWU4In0=','Content-Type':'application/json'},json = body,params = {'BusinessId':'9','isCustomer':True})
                
                # duplicate_hashcodes = response.json()        
                
                # duplicate_hash_list.extend(duplicate_hashcodes)
                
                # duplicate_hash = final_df[final_df['HASH_1'].isin(duplicate_hashcodes)]
                
                # final_df = final_df[~(final_df['HASH_1'].isin(duplicate_hashcodes))]
                
                # duplicate_hash_df = pd.concat([duplicate_hash_df,duplicate_hash],axis = 0)
                
                # # valid_output = final_df[~(valid_output['HASH_1'].isin(duplicate_hashcodes))]
                
                
                duplicate_hash_list = []
                
                
                chunk_size = 500

                for xy in range(0, (len(final_df) // chunk_size) + 1):  # +1 to include the remaining data

                    start_index = xy * chunk_size

                    end_index = min((xy + 1) * chunk_size, len(final_df))

                    hash_codes = final_df['HASH_1'][start_index:end_index]
                
                    body = {"hashCodes":list(hash_codes)}
                
                    response = requests.post(url = CDMS_properties['main_app']+'getCustomerDataby3Hashcode',headers = {'X-AUTH-TOKEN':CDMS_properties['x-auth-token'],'Content-Type':'application/json'},json = body,params = {'BusinessId':'9','isCustomer':True})
                
                    duplicate_hashcodes = response.json()     
                
                    print()
                        
                    # print(response.status_code)
                    
                    # duplicate_hash = final_df[final_df['HASH_2'].isin(duplicate_hashcodes)]
                
                    duplicate_hash_list.extend(duplicate_hashcodes)
                
                    
                #     # duplicate_hash_df = pd.concat([duplicate_hash_df,duplicate_hash],axis = 0)
                    
                #     # valid_output = valid_output[~(valid_output['HASH_2'].isin(duplicate_hashcodes))]
                    
                    
                
                # hash_codes = final_df[(len(final_df)//500)*500:]
                
                # body = {"hashCodes":list(hash_codes)}
                
                # response = requests.post(url = 'http://mr403s0332d.palawangroup.com:4200/getCustomerDataby3Hashcode',headers = {'X-AUTH-TOKEN':'eyJ1c2VybmFtZSI6InN5c3RlbSIsInRva2VuIjoiODRjOWZmNmQtZTllMy00MWUwLWI0MDctZmY5ZGQ5YjFmYWU4In0=','Content-Type':'application/json'},json = body,params = {'BusinessId':'9','isCustomer':True})
                
                # duplicate_hashcodes = response.json()  
                
                # duplicate_hash_list.extend(duplicate_hashcodes)      
                
                # duplicate_hash = final_df[final_df['HASH_2'].isin(duplicate_hash_list)]
                
                # duplicate_hash_df = pd.concat([duplicate_hash_df,duplicate_hash],axis = 0)
                
                # # valid_output = valid_output[~(valid_output['HASH_2'].isin(duplicate_hashcodes))]
                
                # final_df = final_df[~(final_df['HASH_2'].isin(duplicate_hash_list))]
                
                # duplicates = duplicate_hash_df.copy()
                
                # duplicates['reason'] = 'duplicates identified from system'
                
                
                
                
                
                
                
                
                
                
                
                #completion of API check on hash codes
                
                
                
                
                
                
                
                
                
                
                
                
                #     # response = requests.post(url = 'http://mr403s0332d.palawangroup.com:4200/fileUploadExternalApi',headers = {'X-AUTH-TOKEN':'eyJ1c2VybmFtZSI6InN5c3RlbSIsInRva2VuIjoiODRjOWZmNmQtZTllMy00MWUwLWI0MDctZmY5ZGQ5YjFmYWU4In0=','Content-Type':'application/json'},json = body)
                
                
                # duplicates.to_csv('invalid//duplicates_'+business.loc[i,'File Name'],index  = False)
                
                invalid_records = final_df[final_df['valid']=='invalid']
                
                final_df = final_df[final_df['valid']=='valid']  
                
    #            print(final_df[final_df['CONTACT_DETAILS']=='0']['valid'].unique())             
                
                if os.path.exists(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//valid"):
                    
                    pass
                
                else:
                    
                    os.makedirs(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//valid")
                
                if os.path.exists(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//invalid"):
                    
                    pass
                
                else:
                    
                    os.makedirs(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//invalid")
                    
                    
                if ('Remarks_y' in final_df.columns):
                    
                    pass
                
                else:
                    
                    final_df['Remarks_y'] = ''
                
                
                final_df.fillna('',inplace = True)
                
                final_df.replace('none','')
                
                # final_df['CONTACT_DETAILS'] = final_df[]
                
                final_df.rename(columns = {'EXPIRYDATE_x':'EXPIRYDATE','LOAD_DT_x':'LOAD_DT'},inplace = True)
                
                final_df['PRIMARYIDTYPE'] = ''
                
                final_df['PRIMARYID'] = ''
                
    #            print(final_df[final_df['CONTACT_DETAILS']=='0']['valid'].unique())             
                
                
                headers_final = list(headers.values())
                
                headers_final.append('HASH_1')
                
                headers_final.append('HASH_2')
                
                
                final_df.fillna('',inplace = True)
                
                
    #            print(final_df[final_df['CONTACT_DETAILS']=='0']['valid'].unique())             
                
                
                final_df.fillna('',inplace = True)
                
                final_df = final_df.replace('NONE','')
                    
                # final_df.to_csv(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//valid//CDMS_output.csv",index  = False)
                
                
                # final_df = pd.read_csv(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//valid//CDMS_output.csv")
                
                
                
                
                final_df.fillna('',inplace = True)
                
                errored_df = final_df[(((final_df['EMAIL']=='') & (final_df['EMAIL_error']!='')) | ((final_df['LANDLINE_NO']=='') & (final_df['LANDLINE_NO_error']!='')) | ((final_df['EXPIRYDATE']=='') & (final_df['EXPIRYDATE_error']!='')) | ((final_df['LOAD_DT']=='') & (final_df['LOAD_DT_error']!='')) |((final_df['DATEOFBIRTH']=='') & (final_df['DATEOFBIRTH_error']!='')))]
                
                errored_df.to_csv(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//invalid//errored_out.csv",index  = False)
                
                headers_final.append('CUSTOMERADDRESS')
                            
                final_df = final_df[headers_final]
                
                
                
                final_df['Remarks_y'] = ''
                
                final_df['ID'] = ''
                
                final_df['BIZ_ID'] = ''

                final_df['GEN_ID'] = ''

                final_df['FILE_LOC'] = i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//valid//CDMS_output.csv"

                final_df['IN_SYSTEM'] = ''

                final_df.loc[final_df['HASH_1'].isin(duplicate_hash_list), 'IN_SYSTEM'] = 'existing in system'
                
                # duplicate_hash = final_df[final_df['HASH_1'].isin(duplicate_hash_list)]

                # duplicate_hash.to_csv(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//valid//CDMS_update_output.csv",index  = False, mode='a', header=not os.path.exists(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//valid//CDMS_update_output.csv"))

                # print(len(duplicate_hash))

                # final_df = final_df[~(final_df['HASH_1'].isin(duplicate_hash_list))]
                
                final_df.to_csv(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//valid//temp_valid_"+filename,index  = False, mode='a', header=not os.path.exists(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//valid//temp_valid_"+filename))
                
                final_count =len(final_df)
                
                print(final_count)

                # duplicate_hash.to_csv('invalid//duplicates_'+business.loc[i,'File Name'],index  = False)
                
                final_df_duplicates['reason'] = 'duplicates in input'
                
                
                # invalid_records = pd.concat([invalid_records,final_df_duplicates],axis = 0)
                
                invalid_records = pd.concat([invalid_records,mis_spelled_duplicates_final],axis = 0)
                
                print(len(invalid_records))
                
                invalid_records.to_csv(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//invalid//invalid_"+filename,index  = False, mode='a', header=not os.path.exists(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//invalid//invalid_"+filename))
                
                corporate_customers.to_csv(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//valid//corporate_customers"+filename,index  = False, mode='a', header=not os.path.exists(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//valid//corporate_customers"+filename))
                
                
                # print(len(corporate_customers))

                # print(len(final_df))


                
                # print(CDMS_output.columns)
            
            df=pd.read_csv(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//valid//temp_valid_"+filename)

            final_df = df[~(df.duplicated(['HASH_1']))]

            duplicate_df = df[(df.duplicated(['HASH_1']))]

            # corporate_customers = final_df[final_df['CORPORATE'] == True]
                
            # final_df = final_df[final_df['CORPORATE']==False]

            # corporate_customers.to_csv(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//valid//corporate_valid_"+filename,index  = False)

            final_df.to_csv(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//valid//CDMS_valid_"+filename,index  = False)

            duplicate_df.to_csv(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//invalid//CDMS_duplicate_"+filename,index  = False)

            dedup_body = {

                "fileId":field_id,
                        
                "outputlocation":i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//valid//",

                "outputCount":len(final_df),
            
                "processName": process_name,

                "status":'Processed',
            }
                
            body = {
            
                "fileName":"CDMS_valid_"+filename,
            
                "filePath":i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//valid//",
            
                "subListID":76,
            
                "userID":149,
            
                "businessHierarchyId":23,

                "batchNo":"b1",

                "dedupStatus":dedup_body
            
            }
            
            
            response = requests.post(url = CDMS_properties['main_app']+'fileUploadExternalApi',headers = {'X-AUTH-TOKEN':CDMS_properties['x-auth-token'],'Content-Type':'application/json'},json = body)

            upload_id=0         

            if response.status_code == 200:
                # Parse JSON response
                response_data = response.json()
                content = response_data['content']  # Extract the 'content' field from the response
                
                # Check if content exists and if it has 'uploadId'
                if content and 'uploadId' in content:
                    upload_id = content['uploadId']
                    # print("Upload ID:", upload_id)
                else:
                    print("Upload ID not found in the response content.")
            else:
                print("Request failed with status code:", response.status_code)
           
            print("Message sent successfully")
                                        
            # with open('response.txt','r') as w:
                
            #     text = w.read()

            # with open('response.txt','w') as w:
                
            #     w.write(text+str(count)+"."+i+"\n")
                                    

                
    except Exception as e:
    
        print(str(e))            
        
        print(traceback.print_exc())
                
            
        # count = count+1
            
            
        # with open('response.txt','r') as w:
            
        #     text = w.read()

        # with open('response.txt','w') as w:
            
        #     w.write(text+"Error at file:"+str(count)+"."+i+"\n")








