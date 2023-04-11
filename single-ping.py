import subprocess

# Read the list of IP addresses from an external text file
with open('ip_list.txt') as f:
    ip_list = [line.strip() for line in f]

# Get the list of network interfaces
interfaces = subprocess.check_output(['ifconfig', '-s']).decode().splitlines()[1:]

# Loop through each interface
for interface in interfaces:
    interface_name = interface.split()[0]
    
    # Loop through each IP address in the list
    for ip in ip_list:
        # Execute the ping command for the IP address on the current interface
        try:
            subprocess.check_output(['ping', '-I', interface_name, '-c', '1', '-W', '1', ip])
            print(f'Successful: {ip} on {interface_name}')
        except subprocess.CalledProcessError:
            print(f'Failed:     {ip} on {interface_name}')
