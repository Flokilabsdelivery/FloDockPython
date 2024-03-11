import pandas as pd

import configparser

import os

import traceback

def list_all_files_in_drive(drive):

    all_files = []

    for root, dirs, files in os.walk(drive):

        for file in files:

            file_path = os.path.join(root, file)

            all_files.append(file_path)

    return all_files

# config_parser = configparser.ConfigParser()

# current_directory = os.path.dirname(os.path.realpath(__file__))

# properties_file_path = os.path.join(current_directory, 'config.properties')

# with open(properties_file_path) as file:
#     config_parser.read_string('[default]\n' + file.read())

# CDMS_properties = {}

# for option in config_parser.options('default'):
#     CDMS_properties[option] = config_parser.get('default', option)


config_parser = configparser.ConfigParser()

config_parser.read_string('[default]\n' + open('config.properties').read())

CDMS_properties = {}

for option in config_parser.options('default'):
    CDMS_properties[option] = config_parser.get('default', option)

drive_to_list = CDMS_properties['source_path']

files_in_drive = list_all_files_in_drive(drive_to_list)

files_location = []

for file in files_in_drive:
    
    file = file.replace('\\','/')
    
    list1 = file.split('/')   
    
    list1 = '/'.join(list1)
                       
    files_location.append(list1)



files_location = list(set(files_location))

for file_path in files_location:

    try:

        report_contents = []
        
        i, filename = os.path.split(file_path)

        if (filename) in os.listdir(i) and filename.endswith('.csv'):

            if os.path.exists(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//valid//CDMS_valid_"+filename):

                total_df=pd.read_csv(file_path)

                total_len = len(total_df)

                record = "input records: " + str(total_len)

                report_contents.append(record)

                report_path=i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"/report"

                if not os.path.exists(report_path):

                    os.makedirs(report_path)

                if os.path.exists(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//invalid//invalid_"+filename):

                    df=pd.read_csv(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//invalid//invalid_"+filename)

                    record = "Invalid records: " + str(len(df))

                    report_contents.append(record)

                    df_summary = df.groupby('reason').size().reset_index(name='Counts')

                    df_summary.to_csv(report_path+'/data_summery_'+ filename,index=False)

                    diff_len =total_len - len(df)

                    record = "valid records: " + str(diff_len)

                    report_contents.append(record)    

                if os.path.exists(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//valid//corporate_customers"+filename):

                    df=pd.read_csv(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//valid//corporate_customers"+filename)   

                    record = "Corprate records: " + str(len(df))

                    report_contents.append(record)         

                if os.path.exists(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//valid//temp_valid_"+filename):

                    df=pd.read_csv(i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"//valid//temp_valid_"+filename)

                    df = df[~(df.duplicated(['HASH_2']))]

                    record = "Rule 8 (Fname, Lname, DOB, Address): " + str(len(df))

                    report_contents.append(record)

                    df = df[~(df.duplicated(['HASH_1']))]

                    record = "Subrule 1 (Fname, Lname, DOB): " + str(len(df))

                    report_contents.append(record)

                    df = df[((df["CONTACT_DETAILS"].astype(str).str.startswith('+63')) & (df["CONTACT_DETAILS"].astype(str).str.len() == 13)) ]

                    record = "Filter Valid Phone Number: " + str(len(df))

                    report_contents.append(record)

                    df = df[~(df.duplicated(['CONTACT_DETAILS']))]

                    record = "Use Phone Numbers as Subrule: " + str(len(df))

                    report_contents.append(record)

                
                report_path_1=i.replace(CDMS_properties['replace_string'],CDMS_properties['replace_with'])+"/report/report_"+filename

                if report_path_1.endswith('.csv'):
                    
                    new_report_path = os.path.splitext(report_path_1)[0] + '.txt'

                    if os.path.exists(new_report_path):

                        os.remove(new_report_path)

                    with open(new_report_path, "w") as f:

                        for content in report_contents:

                            f.write(content + "\n")

            else:

                print('Dedup process not done')

            print('Data summary report '+ filename )

    except Exception as e:
    
        print(str(e))            
        
        print(traceback.print_exc())