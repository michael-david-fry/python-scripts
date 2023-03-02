import boto3
import csv

# Hardcoded AWS connection details
AWS_ACCESS_KEY_ID = "SAMPLE"
AWS_SECRET_ACCESS_KEY = "SAMPLE"
AWS_SESSION_TOKEN = "SAMPLE"
REGION_NAME = "ap-southeast-2"

# Connect to AWS using the connection details and session token
ec2 = boto3.client('ec2',
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                  aws_session_token=AWS_SESSION_TOKEN,
                  region_name=REGION_NAME)

# Get all Security Groups in the region
security_groups = ec2.describe_security_groups()

# Write header row in the CSV file
with open('Security_Group_Ingress_Rules.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Description", "GroupId", "GroupName", "VpcId", "Tags", "ToPort", "IpProtocol", "CidrIp", "IpRangeDescription", "PrefixListIds", "UserIdGroupPairs"])

# Loop through each Security Group and get the Ingress rules
    for security_group in security_groups["SecurityGroups"]:
        group_id = security_group["GroupId"]
        group_name = security_group["GroupName"]
        vpc_id = security_group["VpcId"]

        # Get tags for the Security Group
        try:
            tags = [tag["Value"] for tag in security_group["Tags"]]
        except KeyError:
            tags = None

        # Loop through each Ingress rule in the Security Group
        for rule in security_group["IpPermissions"]:
            to_port = rule.get("ToPort", None)
            ip_protocol = rule.get("IpProtocol", None)

            # Loop through each CIDR IP in the Ingress rule
            for ip_range in rule["IpRanges"]:
                cidr_ip = ip_range.get("CidrIp", None)
                description = ip_range.get("Description", None)

                # Write data to the CSV file
                with open('Security_Group_Ingress_Rules.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([description, group_id, group_name, vpc_id, tags, to_port, ip_protocol, cidr_ip, None, None, None])
