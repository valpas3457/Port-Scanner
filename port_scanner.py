import sys
import socket
import pyfiglet

# Generate and print ASCII banner
ascii_banner = pyfiglet.figlet_format("developed by \nValentin Thal \nPort Scanner")
print(ascii_banner)

# Ask the user to enter the IP address to scan
ip = input("Please enter the IP address you want to scan: ")

# List to hold open ports
open_ports = []

# Range of ports to scan
ports = range(1, 100)

# Function to probe a specific port on the given IP address
def probe_port(ip, port, result=1):
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set timeout for the socket
        sock.settimeout(0.5)
        # Try to connect to the specified IP and port
        r = sock.connect_ex((ip, port))
        if r == 0:
            result = r
        # Close the socket
        sock.close()
    except Exception as e:
        pass
    return result

# Iterate over the range of ports
for count, port in enumerate(ports, 1):
    # Flush the standard output buffer
    sys.stdout.flush()
    # Probe the current port
    response = probe_port(ip, port)
    # If the port is open, add it to the list of open ports
    if response == 0:
        open_ports.append(port)
    # Print the progress
    print(f"Scanned {count} ports so far...", end="\r")

# Print the list of open ports, if any
if open_ports:
    print("\nOpen Ports are:")
    print(sorted(open_ports))
else:
    print("\nLooks like no ports are open :(")
