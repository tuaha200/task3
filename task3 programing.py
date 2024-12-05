        "interface loopback 1",
        "ip address 192.168.56.101 255.255.255.0",
        "no shutdown",

        # Configure OSPF
        "router ospf 1",
        "network 10.0.0.0 0.0.0.255 area 0",  # Advertise the loopback network
        "network 192.168.56.0 0.0.0.255 area 0",  # Advertise the physical network
    ]

    try:
        # Establish an SSH connection to the router
        print("Connecting to the router...")
        connection = ConnectHandler(**router)
        connection.enable()  # Enter enable mode

        # Send configuration commands
        print("Sending configuration commands...")
        output = connection.send_config_set(config_commands)
        print(output)

        # Save the configuration
        print("Saving the configuration...")
        save_output = connection.send_command("write memory")
        print(save_output)

        # Close the connection
        connection.disconnect()
        print("Configuration complete and connection closed.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the configuration function
if __name__ == "__main__":
    configure_router()
