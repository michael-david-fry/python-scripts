import boto3
import csv

# Hardcoded AWS connection details
AWS_ACCESS_KEY_ID = "YOUR_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY = "YOUR_SECRET_ACCESS_KEY"
REGION_NAME = "REGION_NAME"
SESSION_TOKEN = "SESSION_TOKEN"

# Creating boto3 client to interact with AWS
client = boto3.client('ec2', 
                      aws_access_key_id=AWS_ACCESS_KEY_ID, 
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
                      region_name=REGION_NAME, 
                      aws_session_token=SESSION_TOKEN)

# Call to describe_vpcs method to get the VPCs
vpcs = client.describe_vpcs()['Vpcs']

# Creating a CSV file to store the output
with open('vpcs.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    
    # Writing header row to the CSV file
    writer.writerow(["VPC CIDR", "VPC Name", "Region"])
    
    # Iterating through the VPCs
    for vpc in vpcs:
        cidr = vpc['CidrBlock']
        vpc_name = ''
        for tag in vpc['Tags']:
            if tag['Key'] == 'Name':
                vpc_name = tag['Value']
                break
        region = REGION_NAME
        
        # Writing the row to the CSV file
        writer.writerow([cidr, vpc_name, region])
