from kafka import KafkaProducer

import json

import csv

class Transaction:
    def __init__(data, fileUploadId , filePath, fileName,subListID,userID,businessHierarchyId):
        data.fileUploadId = fileUploadId
        data.filePath = filePath.strip()
        data.fileName = fileName.strip()
        data.subListID = subListID
        data.userID = userID
        data.businessHierarchyId = businessHierarchyId

    def __str__(data):
        return f"{{fileUploadId: {data.fileUploadId}, filePath: {data.filePath}, fileName: {data.fileName},subListID: {data.subListID}, userID: {data.userID}, businessHierarchyId: {data.businessHierarchyId}}}"

def read_csv_and_create_objects(file_path):
    TransactionData = []
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            Transaction_instance = Transaction(int(row['fileUploadId']), row['filePath'], row['fileName'],int(row['subListID']), int(row['userID']), int(row['businessHierarchyId']))
            TransactionData.append(Transaction_instance)
    return TransactionData

if __name__ == "__main__":

    file_path = "formdata.csv"

    TransactionData_objects = read_csv_and_create_objects(file_path)

    start_index = 0
    
    end_index = 1

    for i in range(start_index, end_index):

        print(TransactionData_objects[i].fileUploadId)
        # try:
        #     producer = KafkaProducer(bootstrap_servers='MR402S0352D.palawangroup.com:9092')

        #     topic = 'testKafkaTopic'
        
        #     for i in range(1):

        #         message = f"Message {i}"

        #         my_dict = TransactionData_objects[i]

        #         my_dict = json.dumps(my_dict)

        #         producer.send(topic, value=my_dict.encode('utf-8'))

        #         print("Message sent successfully")
        
        # except Exception as e:

        #     print(f"Error: {e}")

        # finally:

        #     producer.close()