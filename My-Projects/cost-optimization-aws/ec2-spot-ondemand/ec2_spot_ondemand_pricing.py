#https://stackoverflow.com/questions/51673667/use-boto3-to-get-current-price-for-given-ec2-instance-type
#https://maori.geek.nz/aws-api-to-get-ec2-instance-prices-b04a155860da
#https://github.com/awslabs/ec2-spot-labs/blob/master/ec2-spot-history-notebook/ec2-spot-historic-prices.ipynb


#Note: if you are geting error like "AttributeError: 'EC2' object has no attribute 'describe_instance_type_offerings'"
#you need to upgrade boto3/botocore
#pip3 install botocore –upgrade
#pip3 install boto3 --upgrade

import boto3
import json
import datetime
import pandas as pd
from joblib import Parallel,delayed


def my_converter(obj):
    if isinstance(obj,datetime.datetime):
        return obj.__str__()

def getEC2Regions(account):
    session = boto3.session.Session(profile_name=account,region_name='us-east-1')
    ec2_client = session.client('ec2')
    # exception handling
    regions_response = ec2_client.describe_regions()
    return [ region['RegionName'] for region in regions_response['Regions']]

def getInstanceTypesInRegion(account, region):
    session = boto3.session.Session(profile_name=account, region_name=region)
    ec2_client = session.client('ec2')
    instance_types_offering = ec2_client.describe_instance_type_offerings(LocationType='region')
    #print(instance_types_offering)
    return [it['InstanceType'] for it in instance_types_offering['InstanceTypeOfferings']]
    
def getGlobalInstanceTypes(account):
    regions = getEC2Regions(account)
    instance_type_set = set([])
    for region in regions:
        #print(region)
        instances_types = getInstanceTypesInRegion(account,region)
        #print(instances_types)
        for instance_type in instances_types:
            instance_type_set.add(instance_type)
    return instance_type_set



# Translate region code to region name
def get_region_name(region_code):
    default_region = 'EU (Ireland)'
    """
    endpoint_file = resource_filename('botocore', 'data/endpoints.json')
    try:
        with open(endpoint_file, 'r') as f:
            data = json.load(f)
        return data['partitions'][0]['regions'][region_code]['description']
    except IOError:
        return default_region
    """
    return 'US East (N. Virginia)'


# Search product filter
#Added Licence filter to eradicate the issue caused in listing price of WIndows instances
FLT = '[{{"Field": "tenancy", "Value": "shared", "Type": "TERM_MATCH"}},'\
      '{{"Field": "operatingSystem", "Value": "{o}", "Type": "TERM_MATCH"}},'\
      '{{"Field": "preInstalledSw", "Value": "NA", "Type": "TERM_MATCH"}},'\
      '{{"Field": "instanceType", "Value": "{t}", "Type": "TERM_MATCH"}},'\
      '{{"Field": "location", "Value": "{r}", "Type": "TERM_MATCH"}},'\
      '{{"Field": "licenseModel", "Value": "No License required", "Type": "TERM_MATCH"}},'\
      '{{"Field": "capacitystatus", "Value": "Used", "Type": "TERM_MATCH"}}]'




# Get current AWS price for an on-demand instance
def get_ondemand_price(client,region,instance, os):
    region_name=get_region_name(region)
    f = FLT.format(r=region_name, t=instance, o=os)
    data = client.get_products(ServiceCode='AmazonEC2', Filters=json.loads(f))
    #print("#####################")
    for dat in data['PriceList']:
        #print(dat)
        some_str=json.loads(dat)
        print(json.dumps(some_str,default=my_converter,indent=10))
        print("###########################")
    #some_str=json.loads(data['PriceList'][0])
    #print(json.dumps(some_str,default=my_converter,indent=10))
    od = json.loads(data['PriceList'][0])['terms']['OnDemand']
    id1 = list(od)[0]
    id2 = list(od[id1]['priceDimensions'])[0]
    return od[id1]['priceDimensions'][id2]['pricePerUnit']['USD']


def get_spot_price(client,region, instance, os):
    now = datetime.datetime.utcnow()
    ec2Client = boto3.client('ec2')
    #????????????AvailabilityZone
    ##############
    response = ec2Client.describe_spot_price_history(StartTime=now,EndTime=now,InstanceTypes=[instance],AvailabilityZone='us-east-1a',ProductDescriptions=[os])
    pricehistory = response['SpotPriceHistory']
    if pricehistory == []:
        response = ec2Client.describe_spot_price_history(StartTime=now,EndTime=now,InstanceTypes=[instance],AvailabilityZone='us-east-1a',ProductDescriptions=[os+' (Amazon VPC)'])
        pricehistory = response['SpotPriceHistory']
    #print(json.dumps(pricehistory,default=my_converter))
    #print(pricehistory[0]['SpotPrice'])
    return pricehistory[0]['SpotPrice']

###########
if __name__=="__main__":
    account='oldAccount'
    #region='us-east-1'
    #regions_list= sorted(getEC2Regions(account))
    #instances_types_list = sorted(list(getGlobalInstanceTypes(account)))
    regions_list=["us-east-1"]
    for region in regions_list:
        print(region)
        session=boto3.session.Session(profile_name=account,region_name=region)  
        # Use AWS Pricing API at US-East-1
        price_client = session.client('pricing')
        ondemand_os_list=["Linux","Windows","SUSE","RHEL"]
        ondemand_os_list=["Windows"]
        spot_os_list=["Linux/UNIX","Windows","SUSE Linux","Red Hat Enterprise Linux"]
        spot_os_list=["Windows"]
        for ondemand_os,spot_os in zip(ondemand_os_list,spot_os_list):
            # Get current price for a given instance, region and os
            print(ondemand_os,spot_os)
            ondemand_price=0
            spot_price=0
            ondemand_price = get_ondemand_price(price_client,region, 't3.nano', ondemand_os)
            #spot_price = get_spot_price(price_client,region, 't3.medium', spot_os)
            print(ondemand_price,spot_price)
            #break
        #break

"""
df=pd.DataFrame(main_list,columns=["account","region","table","read_capacity","write_capacity","table_type"])
print(df)
"""

