from netmiko import ConnectHandler

# Device configuration details
router = {
    'device_type': 'cisco_ios',
    'host': '192.168.56.0',  # Updated router IP address
    'username': 'tuaha',     # Username
    'password': 'cisco123',  # Password
    'secret': 'cisco1234',   # Enable Secret
}

# Configuration script
config_commands = [
    # Loopback and Interface Configuration
    "interface loopback 0",
    "ip address 10.0.0.1 255.255.255.0",
    "no shutdown",
    "interface gigabitEthernet 0/0",
    "ip address 192.168.56.1 255.255.255.0",
    "no shutdown",
    
    # OSPF Configuration
    "router ospf 1",
    "network 10.0.0.0 0.0.0.255 area 0",
    "network 192.168.56.0 0.0.0.255 area 0",
    
    # Access Control List (ACL) Configuration
    "ip access-list extended BLOCK_HTTP",
    "deny tcp any any eq 80",  # Block HTTP traffic
    "permit ip any any",       # Allow all other traffic
    
    # IPSec Configuration
    "crypto isakmp policy 10",
    "encryption aes",
    "hash sha",
    "authentication pre-share",
    "group 14",
    "crypto isakmp key MYSECRETKEY address 0.0.0.0",
    "crypto ipsec transform-set MY_TRANSFORM_SET esp-aes esp-sha-hmac",
    "crypto map MY_CRYPTO_MAP 10 ipsec-isakmp",
    "set peer 192.168.56.2",  # Peer IP (update as needed)
    "set transform-set MY_TRANSFORM_SET",
    "match address 101",     # Link crypto map to ACL
    "interface gigabitEthernet 0/1",
    "crypto map MY_CRYPTO_MAP",
]

def configure_device(device, commands):
    try:
        connection = ConnectHandler(**device)
        connection.enable()
        output = connection.send_config_set(commands)
        print(output)
        connection.disconnect()
    except Exception as e:
        print(f"An error occurred: {e}")

# Execute the script
configure_device(router, config_commands)
