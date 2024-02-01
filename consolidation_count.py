# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 11:58:44 2023

@author: CBT
"""

import pandas as pd

import os

df = pd.DataFrame()

df.to_csv('output.csv')

def list_all_files_in_drive(drive):

    all_files = []

    for root, dirs, files in os.walk(drive):

        for file in files:

            file_path = os.path.join(root, file)

            all_files.append(file_path)

    return all_files

drive_to_list = '/STFS0029M/migration_data'

files_in_drive = list_all_files_in_drive(drive_to_list)

#print(files_in_drive)

#files_in_drive = files_in_drive[0:3]

files_location = []
for file in files_in_drive:
    
    file = file.replace('\\','/')
    
    list1 = file.split('/')    
    
    list1.pop()
    
    list1 = '/'.join(list1)

    if 'overall' in list1:

         pass

    else:
                       
         files_location.append(list1)

files_location = list(set(files_location))

#files_location = files_location[0:10]

df = pd.DataFrame(columns = ['Path','valid','invalid','corporate'])

for i in range(0,len(files_location)):
    
    df.loc[i,'Path'] = files_location[i].replace('invalid','').replace('valid','')
    
df.to_csv('index.csv',index = False)

df = df.drop_duplicates(['Path'])

df.index = df['Path']



#print(files_location)

count = 0

valid_count = 0

for i in files_location:


#    print(i.replace('valid/CSDMS_output.csv','').replace('invalid/CDMS_output.csv','').replace('invalid/corporate_customers.csv',''))
    
    some = i.replace('invalid','').replace('valid','')
    
#    print(i)
    
    if i.endswith('invalid'):
        
#        print('invalid')
        
        invalid = pd.read_csv(i+"/CDMS_output.csv")

        if count == 0:

              invalid.to_csv('invalid.csv', header = True, index=False, mode = 'a') 

        else:

              invalid.to_csv('invalid.csv', header = False, index=False, mode = 'a')

        count+=1


        df.loc[some,'invalid'] = len(invalid)

        corporate = pd.read_csv(i+"/corporate_customers.csv")

        df.loc[some,'corporate'] = len(corporate)

    
    elif i.endswith('/valid'):
        
#        print('valid')

        
        valid = pd.read_csv(i+"/CDMS_output.csv")

        print(len(valid))
        
        df.loc[some,'valid'] = len(valid)

        corporate = pd.read_csv(i+"/corporate_customers.csv")
    
        df.loc[some,'corporate'] = len(corporate)

        

#        with pd.ExcelWriter('output.xlsx', engine='openpyxl', mode='a') as writer:
    # Write the DataFrame to the Excel file

        if count == 0:
              valid.to_csv('output.csv', header = True, index=False, mode = 'a')
        else:
              valid.to_csv('output.csv', header = False, index=False, mode = 'a')

        count+=1

        valid_count = valid_count+len(valid)

        print(valid_count)

        print(count)



















#        print('corporate')
        
#        corporate = pd.read_csv(i+"/corporate_customers.csv")
        
#        df.loc[some,'corporate'] = len(corporate)
    
    
df.to_csv('consolidation.csv')    
    

# files_location = files_location[0:1]










for i in files_location:
	print(i)
