import pandas as pd

import re

import os

from unidecode import unidecode

config = pd.read_excel('config.xlsx',engine = 'openpyxl')


print('config read')

config = dict(list(zip(config['key'],config['value'])))


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




df_ = pd.read_csv('total_transaction.csv')

chunk_size = 800000  # Define the size of each chunk

total_rows = len(df_)

for i, chunk_df in enumerate(pd.read_csv('total_transaction.csv', chunksize=chunk_size, low_memory=False)):

    start_index = i * chunk_size

    end_index = min((i + 1) * chunk_size, total_rows)

    print(f"Processing chunk {i+1}: Rows {start_index}-{end_index}")

#    df = df[0:800000]
#    df = df[800001:1600000]
#    df = df[1600001:2400000]
#    df = df[2400001:3200000]
#    df = df[3200001:4000000]
#    df = df[4000001:4514109]
    df = df_[start_index:end_index]

    headers = pd.read_csv('headers_matching.csv')

    headers = dict(list(zip(headers['key'],headers['value'])))

    #df.rename(columns = headers,inplace = True)

    #df[config['CustomerAddress']] = df[config['ADDRESS1']] + df[config['ADDRESS2']] + df[config['ADDRESS3']] + df[config['ADDRESS4']]



    df[config['FirstName']] = df[config['FirstName']].fillna('')   

    df[config['LastName']] = df[config['LastName']].fillna('')   

    df[config['CustomerAddress']] = df[config['CustomerAddress']].fillna('')   




    df[config['FirstName']] = df[config['FirstName']].str.upper()   

    df['CustomerLasttName'] = df[config['LastName']].str.upper()   

    df[config['CustomerAddress']] = df[config['CustomerAddress']].str.upper()  


    for column in df.columns:
        
        df[column] = df[column].astype(str)
        
        df[column] = df[column].apply(lambda x: unidecode(str(x)) if pd.notnull(x) else x)
        
        df[column] = df[column].str.replace(',',';')


    last_name_words = config['lastname_words']

    for words in last_name_words.split(','):
        
        df[config['FirstName']] = df[config['FirstName']].str.replace(words.upper(),words.upper().replace(' ','-')) 

        df[config['LastName']] = df[config['LastName']].str.replace(words.upper(),words.upper().replace(' ','-')) 





    suffixes = [ ' I', ' II', ' III', ' IV', ' V', ' JR', ' SR']    

    df['SUFFIX'] = ''

    for suffix in suffixes:
        
        df.loc[df[config['FirstName']].str.contains(suffix),'SUFFIX'] = suffix 

        df[config['FirstName']]=  df[config['FirstName']].str.replace(suffix,'')

        df.loc[df[config['LastName']].str.contains(suffix),'SUFFIX'] = suffix 

        df[config['LastName']] = df[config['LastName']].str.replace(suffix,'')


    print('corporate customers')
                
    corp_name_pattern = ['ACADEMY ', ' ACADEMY', 'TECHNOLOGY ', ' TECHNOLOGY', 'TECHNO ', ' TECHNO', 'STALL ', ' STALL', 'SERVICES ', ' SERVICES', 'BRANCH ', ' BRANCH', 'OUTLET ', ' OUTLET', 'EXPRESS ', ' EXPRESS', 'CENTER ', ' CENTER', 'BUSINESS ', ' BUSINESS', 'CORPORATION ', ' CORPORATION', 'COMPANY ', ' COMPANY', ' INC ', '  INC', 'INC  ', ' INC ', 'COURIER ', ' COURIER', 'COOPERATIVE ', ' COOPERATIVE', 'BANK ', ' BANK', 'SECURITY ', ' SECURITY', 'DISTRIBUTOR ', ' DISTRIBUTOR', 'DISTILLERS ', ' DISTILLERS', 'PHARMACY ', ' PHARMACY', 'MOTORS ', ' MOTORS', 'SCHOOL ', ' SCHOOL', 'TRADEING ', ' TRADEING', 'ACCOUNTS ', ' ACCOUNTS', 'ASSOCIATION ', ' ASSOCIATION', 'UNIV ', ' UNIV', 'COLLEGES ', ' COLLEGES', 'MERCHANT/MERCHANDIZING ', ' MERCHANT/MERCHANDIZING', 'STORE ', ' STORE', 'PHILS ', ' PHILS', 'INSTITUTE ', ' INSTITUTE', 'LIMITED ', ' LIMITED', 'ENTERPRISES ', ' ENTERPRISES', 'VENTURES ', ' VENTURES', 'SHOP ', ' SHOP', 'BOUTIQUE ', ' BOUTIQUE', 'CLINIC ', ' CLINIC', 'HOSPITAL ', ' HOSPITAL', 'FINANCIAL ', ' FINANCIAL', 'PETROL ', ' PETROL', 'GASSTATION ', ' GASSTATION', 'FUEL ', ' FUEL', 'DRUG ', ' DRUG', 'TRAVEL ', ' TRAVEL', 'TOURS ', ' TOURS', 'TOURISM ', ' TOURISM', 'RESTAURANT ', ' RESTAURANT', 'LTD ', ' LTD', 'FINANCE ', ' FINANCE', 'REGION ', ' REGION', 'MARKETING ', ' MARKETING', 'DOLE NCR ', ' DOLE NCR', 'FOOD ', ' FOOD', 'BAKERY ', ' BAKERY', 'CONSTRUCTION ', ' CONSTRUCTION', 'BUILDERS ', ' BUILDERS', 'SUPPLY MATERIALS ', ' SUPPLY MATERIALS', 'JEWELRY ', ' JEWELRY', 'JEWELERS ', ' JEWELERS', 'EDUCATIONAL ', ' EDUCATIONAL', 'AUTO ', ' AUTO', 'MOTORCYCLE ', ' MOTORCYCLE', 'PARTS ', ' PARTS', 'INSURANCE ', ' INSURANCE', 'HEALTH ', ' HEALTH', 'WELLNESS ', ' WELLNESS', 'REALESTATE ', ' REALESTATE', 'PROPERTIES ', ' PROPERTIES']
                
    df['CORPORATE'] = False
                
    for corporate_key in corp_name_pattern:
                    
        df_temp = df[df['CORPORATE']==False]
                    
        df = df[df['CORPORATE']==True]
                            
        df_temp['CORPORATE'] = df_temp[config['FirstName']].str.contains(corporate_key)
                    
        df = pd.concat([df,df_temp],axis = 0)        
                    
        df_temp = df[df['CORPORATE']==False]
                    
        df = df[df['CORPORATE']==True]
                    
        df_temp['CORPORATE'] = df_temp[config['LastName']].str.contains(corporate_key)
                    
        df = pd.concat([df,df_temp],axis = 0)        
                        
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
        

    df['reason'] = ''

    df['reason'].fillna('',inplace = True)


    df = df.apply(lambda row:single_character_check_firstname(row),axis = 1)

    print('first name completed')



    df['reason'].fillna('',inplace = True)

    df = df.apply(lambda row:single_character_check_lastname(row),axis = 1)

    print()

    print('numeric character check')

    df['reason'].fillna('',inplace = True)

    df = df.apply(lambda row:number_check_firstname(row),axis = 1)

    df['reason'].fillna('',inplace = True)

    df = df.apply(lambda row:number_check_lastname(row),axis = 1)

    #print(df['valid'])


    df['reason'].fillna('',inplace = True)

    print('contact details check')

    df['length'] = df['CONTACT_DETAILS'].str.len()

    df['CONTACT_DETAILS'].fillna('',inplace = True)

    #print(df[df['CONTACT_DETAILS']=='0']['valid'].unique())             

    print()    

    #print(df['valid'])


    print('special character check')
    #print(df['valid'])




    df['reason'].fillna('',inplace = True)

    df = df.apply(lambda row:special_character_check_firstname(row),axis = 1)


    df['reason'].fillna('',inplace = True)

    df = df.apply(lambda row:special_character_check_lastname(row),axis = 1)

    #print(df['valid'])
    df1 = df[df['reason'] == '']

    df2 = df[df['reason'] != '']

    df1.to_csv('valid_transaction.csv', index=False, mode='a', header=not os.path.exists('valid_transaction.csv'))
    
    df2.to_csv('invalid_transaction.csv', index=False, mode='a', header=not os.path.exists('invalid_transaction.csv'))
