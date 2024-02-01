import pandas as pd

import re

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




df = pd.read_csv('inputs.csv')

#df = df[0:10000]

headers = pd.read_csv('headers_matching.csv')

headers = dict(list(zip(headers['key'],headers['value'])))

df.rename(columns = headers,inplace = True)

df[config['CustomerAddress']] = df[config['ADDRESS1']] + df[config['ADDRESS2']] + df[config['ADDRESS3']] + df[config['ADDRESS4']]



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



df['reason'] = ''

df['reason'].fillna('',inplace = True)



#df = df[0:10000]

df = df.apply(lambda row:single_character_check_firstname(row),axis = 1)

print('first name completed')

# df = df[0:10]



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




df.to_csv('invalids_new.csv')
