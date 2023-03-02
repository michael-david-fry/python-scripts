import boto3
import csv

# Hard-coded connection details
region_name = 'your_region_name'
access_key_id = 'your_access_key_id'
secret_access_key = 'your_secret_access_key'
session_token = 'your_session_token'

# Create a session using the provided credentials
session = boto3.Session(
    region_name=region_name,
    aws_access_key_id=access_key_id,
    aws_secret_access_key=secret_access_key,
    aws_session_token=session_token
)

# Create an EC2 client using the session
ec2 = session.client('ec2')

# Retrieve the EC2 Security Group Egress rules
try:
    response = ec2.describe_security_groups()
    egress_rules = []
    for group in response['SecurityGroups']:
        group_id = group.get('GroupId', 'null')
        group_name = group.get('GroupName', 'null')
        vpc_id = group.get('VpcId', 'null')
        tags = ','.join([tag['Key'] + ':' + tag['Value'] for tag in group.get('Tags', [])])
        for rule in group.get('IpPermissionsEgress', []):
            description = rule.get('IpRanges', [{}])[0].get('Description', 'null')
            from_port = rule.get('FromPort', 'null')
            protocol = rule.get('IpProtocol', 'null')
            cidr_ip = rule.get('IpRanges', [{}])[0].get('CidrIp', 'null')
            ip_range_description = rule.get('IpRanges', [{}])[0].get('Description', 'null')
            prefix_list_ids = ','.join(rule.get('PrefixListIds', []))
            user_id_group_pairs = ','.join([pair['GroupId'] for pair in rule.get('UserIdGroupPairs', [])])
            egress_rules.append([description, group_id, group_name, vpc_id, tags, from_port, protocol, cidr_ip, ip_range_description, prefix_list_ids, user_id_group_pairs])
except Exception as e:
    print(f'Error retrieving EC2 Security Group Egress rules: {e}')
    exit()

# Output the results to a CSV file
try:
    with open('ec2_security_group_egress_rules.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Description', 'GroupId', 'GroupName', 'VpcId', 'Tags', 'FromPort', 'IpProtocol', 'CidrIp', 'IpRangeDescription', 'PrefixListIds', 'UserIdGroupPairs'])
        for rule in egress_rules:
            writer.writerow(rule)
    print('EC2 Security Group Egress rules successfully written to file.')
except Exception as e:
    print(f'Error writing EC2 Security Group Egress rules to file: {e}')
