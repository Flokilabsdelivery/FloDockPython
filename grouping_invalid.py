# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 09:27:12 2023

@author: CBT
"""


import pandas as pd

import csv

import traceback

import hashlib

import json

import difflib

from kafka import KafkaProducer

import sys

sys.path.append(r'C:\Users\CBT\AppData\Local\Programs\Python\Python311\Lib\site-packages')

config = pd.read_excel('config_CDMS.xlsx',engine = 'openpyxl')

config = dict(list(zip(config['key'],config['value'])))

import requests

#Reading files

import os

from unidecode import unidecode

import re


def list_all_files_in_drive(drive):

    all_files = []

    for root, dirs, files in os.walk(drive):

        for file in files:

            file_path = os.path.join(root, file)

            all_files.append(file_path)

    return all_files


files_in_drive = list_all_files_in_drive('/STFS0029M/migration_data')

files_location = []



for file in files_in_drive:
    
    if (('invalid' in file) & ('overall' not in file)):
    
        file = file.replace('\\','/')
        
        list1 = file.split('/')    
        
        list1.pop()
        
        list1 = '/'.join(list1)
                           
        files_location.append(list1)



files_location = list(set(files_location))

total_df = pd.DataFrame()

some = {}

count = 0

for i in files_location:

    print(i)
    
    df = pd.read_csv(i+'/CDMS_output.csv')

    print(len(df))
    
    df = df[['reason','CUSTOMER_ID']]
    
#    split = df['reason'].str.split(',',expand = True)
    
#    df['reason'] = split[0]

    count+=len(df)    
    
    total_df = pd.concat([total_df,df],axis = 0)

    some[i] = len(df)
    
    
    
#    print(df)


print(len(total_df))


print(count)
total_df = total_df.groupby(['reason']).count()


total_df.to_csv('invalid_counts.csv')

df = pd.DataFrame.from_dict(some,orient = 'index',columns = ['value'])

df.to_csv('invalid_file_wise.csv')


