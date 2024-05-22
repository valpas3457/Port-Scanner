import sys
import socket
import pyfiglet
import threading
from queue import Queue
from tabulate import tabulate

# Generate and print ASCII banner
ascii_banner = pyfiglet.figlet_format("Valentin Thal \nPort Scanner")
print(ascii_banner)

# Ask the user to enter the IP address to scan
ip = input("Please enter the IP address you want to scan: ")

# List to hold open ports
open_ports = []

# Queue for ports
port_queue = Queue()

# Function to probe a specific port on the given IP address
def probe_port(ip, port):
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set timeout for the socket
        sock.settimeout(0.5)
        # Try to connect to the specified IP and port
        r = sock.connect_ex((ip, port))
        if r == 0:
            open_ports.append(port)
            print(f"\nPort {port} is open.")
        # Close the socket
        sock.close()
    except Exception as e:
        pass

# Worker function for threads
def worker():
    while not port_queue.empty():
        port = port_queue.get()
        probe_port(ip, port)
        port_queue.task_done()
        # Print the progress
        print(f"Scanned {port} ports so far...", end="\r")

# Fill the queue with ports
for port in range(1, 5000):
    port_queue.put(port)

# Number of threads
num_threads = 100

# Create and start threads
threads = []
for _ in range(num_threads):
    thread = threading.Thread(target=worker)
    thread.start()
    threads.append(thread)

# Wait for all threads to finish
for thread in threads:
    thread.join()

# Function to print summary of open ports
def print_summary():
    if open_ports:
        table = [[port] for port in sorted(open_ports)]
        headers = ["Open Port"]
        print("\nSummary of open ports:")
        print(tabulate(table, headers, tablefmt="grid"))
    else:
        print("\nLooks like no ports are open :(")

# Print the summary at the end of the scan
print_summary()
