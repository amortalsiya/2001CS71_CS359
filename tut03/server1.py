
import sys
import socket


# claculater
def calculate(expression):
    try:
        return str(eval(expression))
    except:
        return "Error"


# Get server IP and port number from command line arguments
if len(sys.argv) < 3:
    print('Usage: python server.py <ip address> <port number>')
    sys.exit(1)

ip_address = sys.argv[1]
port = int(sys.argv[2])


# Create a TCP/IP socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Bind the socket to a specific address and port
try:
    server_socket.bind((ip_address, port))
    print(f'socket bind to port {port}')
except socket.error as e:
    print('Error:', e)
    sys.exit(1)


# Define the server host and port
HOST = ip_address
PORT = port


# Listen for incoming connections
server_socket.listen(1)
print(f"Server is listening on port {PORT}")


while True:
    # Wait for a connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    # Receive the client's input
    while True:
        data = client_socket.recv(1024) 
        if data:
            expression = data.decode()

            print(f"Received expression: {expression}")
            # Perform the arithmetic operation
            result = calculate(expression)
            # Send the result back to the client
            client_socket.sendall(result.encode())
        else:
            break
    print("connection closed!")
    client_socket.close()
