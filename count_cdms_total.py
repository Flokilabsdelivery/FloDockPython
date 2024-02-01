# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 16:08:54 2023

@author: CBT
"""

import pandas as pd

import os

config = pd.read_excel('config.xlsx',engine = 'openpyxl')

config = dict(list(zip(config['key'],config['value'])))


def list_all_files_in_drive(drive):

    all_files = []

    for root, dirs, files in os.walk(drive):

        for file in files:

            file_path = os.path.join(root, file)

            all_files.append(file_path)

    return all_files



drive_to_list = '/STFS0029M/CDMS'

files_in_drive = list_all_files_in_drive(drive_to_list)

files_location = []



for file in files_in_drive:
    
    file = file.replace('\\','/')
    
    list1 = file.split('/')    
    
    list1.pop()
    
    list1 = '/'.join(list1)
                       
    files_location.append(list1)



files_location = list(set(files_location))

#files_location = files_location[0:1]

count = 0

total_dataframe = pd.DataFrame()

print()

print(files_location)

df = pd.DataFrame(columns = ['Path',config['CDMS_file1'],config['CDMS_file2'],config['CDMS_file3'],config['CDMS_file4'],'overall_input'])

for i in range(0,len(files_location)):
    
    df.loc[i,'Path'] = files_location[i]

df = df.drop_duplicates(['Path'])

df.index = df['Path']

print()

for i in files_location:
    
    
    if (config['CDMS_file1']) in os.listdir(i):
        
        
        print(i)

        file1 = pd.read_csv(i+"//"+config['CDMS_file1'], sep="|")
        
        file2 = pd.read_csv(i+'//'+config['CDMS_file2'], sep="|")

        #file2 = file2[file2['IsCurrent']==1]
        
        file3 = pd.read_csv(i+"//"+config['CDMS_file3'], sep="|")
        
        #file3 = file3[file3['IsCurrent']==1]

        file4 = pd.read_csv(i+'//'+config['CDMS_file4'], sep="|")




    
        headers = pd.read_csv('headers_matching.csv')
        
        headers = dict(list(zip(headers['key'],headers['value'])))
        
        file1.rename(columns = headers,inplace = True)
        
        file2.rename(columns = headers,inplace = True)
        
        file3.rename(columns = headers,inplace = True)
        
        file4.rename(columns = headers,inplace = True)




            
#        print(file1)        
        
        #Merging all the files
        


#        with pd.ExcelWriter('overall/customer_individual.xlsx', engine='openpyxl', mode='a') as writer:

 #              file1.to_excel(writer, sheet_name='Sheet1', index=False, header=True)


  #      with pd.ExcelWriter('overall/customer_identification.xlsx', engine='openpyxl', mode='a') as writer: 
 
   #            file2.to_excel(writer, sheet_name='Sheet1', index=False, header=True)


    #    with pd.ExcelWriter('overall/customer_address.xlsx', engine='openpyxl', mode='a') as writer:

     #          file3.to_excel(writer, sheet_name='Sheet1', index=False, header=True)

      #  with pd.ExcelWriter('overall/suki.xlsx', engine='openpyxl', mode='a') as writer:

       #        file4.to_excel(writer, sheet_name='Sheet1', index=False, header=True)


        file1.to_csv('overall/customer_individual2.csv', mode='a', header=True, index=False)

        file2.to_csv('overall/customer_identification2.csv', mode='a', header=True, index=False)

        file3.to_csv('overall/customer_address2.csv', mode='a', header=True, index=False)

        file4.to_csv('overall/suki2.csv', mode='a', header=True, index=False)
