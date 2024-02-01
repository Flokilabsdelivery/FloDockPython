from kafka import KafkaProducer

import json

import requests

body = {

    "fileName":"CORPORATE_TXN_BENE_CDMS_output.csv",

    "filePath":'/STFS0029M/migration_transaction/2023-10-08/valid/',

    "subListID":85,

    "userID":149,

    "businessHierarchyId":23

}



response = requests.post(url = 'http://mr403s0332d.palawangroup.com:4200/fileUploadExternalApi',headers = {'X-AUTH-TOKEN':'eyJ1c2VybmFtZSI6InN5c3RlbSIsInRva2VuIjoiODRjOWZmNmQtZTllMy00MWUwLWI0MDctZmY5ZGQ5YjFmYWU4In0=','Content-Type':'application/json'},json = body)


upload_id = response.json()['content']['uploadId']


 
if True:
    producer = KafkaProducer(bootstrap_servers='MR402S0352D.palawangroup.com:9092')

    topic = 'ftpKafkaConsumer'
 
    for i in range(1):

        message = f"Message {i}"

        my_dict = {"fileUploadId":1120,"filePath":"//STFS0029M//migration_transaction//2023-10-08//valid//","fileName":"CORPORATE_TXN_BENE_CDMS_output.csv","subListID":76,"userID":149,"businessHierarchyId":23}

        my_dict = json.dumps(my_dict)

        producer.send(topic, value=my_dict.encode('utf-8'))

        print("Message sent successfully")
 
#except Exception as e:

#    print(f"Error: {e}")

#finally:

        producer.close()
