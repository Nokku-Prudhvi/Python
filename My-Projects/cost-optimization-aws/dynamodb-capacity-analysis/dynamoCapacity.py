import boto3
import json
import datetime
import pandas as pd
from joblib import Parallel,delayed

def my_converter(obj):
    if isinstance(obj,datetime.datetime):
        return obj.__str__()

main_list=[]
account='oldAccount'
region='us-east-1'
session=boto3.session.Session(profile_name=account,region_name=region)  
dynamodbclient=session.client('dynamodb')
tables_list=dynamodbclient.list_tables()["TableNames"]
for table in tables_list:
    res=dynamodbclient.describe_table(TableName=table)
    #print(json.dumps(res,default=my_converter,indent=10))
    read_capacity=res["Table"]["ProvisionedThroughput"]["ReadCapacityUnits"]
    write_capacity=res["Table"]["ProvisionedThroughput"]["WriteCapacityUnits"]
    if(read_capacity==0 or write_capacity==0):
        table_type="on-demand"
    else:
        table_type="can-be-provisioned"
    main_list.append([account,region,table,read_capacity,write_capacity,table_type])
    #print(account,region,table,read_capacity,write_capacity,table_type)

df=pd.DataFrame(main_list,columns=["account","region","table","read_capacity","write_capacity","table_type"])
print(df)