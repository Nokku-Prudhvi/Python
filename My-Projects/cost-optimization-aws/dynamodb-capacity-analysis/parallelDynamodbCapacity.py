import boto3
import json
import datetime
import pandas as pd
from joblib import Parallel,delayed

def my_converter(obj):
    if isinstance(obj,datetime.datetime):
        return obj.__str__()

def get_consumed_capacity(account,region,table):
    session=boto3.session.Session(profile_name=account,region_name=region)  
    cloudwatchclient=session.client('cloudwatch')
    date_now=datetime.datetime.utcnow()#.strfy("%m%d%Y %H:%M:%S")
    start_date=date_now-datetime.timedelta(days=5)
    end_date=date_now
    period=432000  #86400
    avg_consumed_read=0
    avg_consumed_write=0
    max_consumed_read=0
    max_consumed_write=0
    write_resp=cloudwatchclient.get_metric_statistics(Namespace='AWS/DynamoDB',
                                                MetricName='ConsumedWriteCapacityUnits',
                                                Dimensions=[{'Name':'TableName','Value':table}],
                                                StartTime=start_date,
                                                EndTime=end_date,
                                                Period=period,
                                                Statistics=["Average","Maximum"])
    read_resp=cloudwatchclient.get_metric_statistics(Namespace='AWS/DynamoDB',
                                                MetricName='ConsumedReadCapacityUnits',
                                                Dimensions=[{'Name':'TableName','Value':table}],
                                                StartTime=start_date,
                                                EndTime=end_date,
                                                Period=period,
                                                Statistics=["Average","Maximum"])
    
    
    print(table)
    print(json.dumps(read_resp,default=my_converter,indent=10))
    avg_consumed_write=write_resp["Datapoints"][0]["Average"]
    avg_consumed_read=read_resp["Datapoints"][0]["Average"]
    max_consumed_write=write_resp["Datapoints"][0]["Maximum"]
    max_consumed_read=read_resp["Datapoints"][0]["Maximum"]
    return (avg_consumed_read,avg_consumed_write,max_consumed_write,max_consumed_read)

def get_dynamodb_capacity(account,region):
    main_list=[]
    session=boto3.session.Session(profile_name=account,region_name=region)  
    dynamodbclient=session.client('dynamodb')
    tables_list=dynamodbclient.list_tables()["TableNames"]
    for table in tables_list:
        res=dynamodbclient.describe_table(TableName=table)
        #print(json.dumps(res,default=my_converter,indent=10))
        provisioned_read=res["Table"]["ProvisionedThroughput"]["ReadCapacityUnits"]
        provisioned_write=res["Table"]["ProvisionedThroughput"]["WriteCapacityUnits"]
        if(provisioned_read==0 or provisioned_write==0):
            table_type="on-demand"
        else:
            table_type="can-be-provisioned"
        (avg_consumed_read,avg_consumed_write,max_consumed_write,max_consumed_read)=get_consumed_capacity(account,region,table)
        main_list.append([account,region,table,provisioned_read,provisioned_write,
        table_type,avg_consumed_read,avg_consumed_write,max_consumed_write,max_consumed_read])
    return main_list

account_list=['oldAccount']
region_list=['us-east-1']
complete_list=Parallel(n_jobs=-1)(delayed(get_dynamodb_capacity)(account,region)for account in account_list for region in region_list)
#print(complete_list)
#print(complete_list[0])
df=pd.DataFrame(complete_list[0],columns=["account","region","table","provisioned_read",
"provisioned_write","table_type","avg_consumed_read","avg_consumed_write",
"max_consumed_write","max_consumed_read"])
print(df)

