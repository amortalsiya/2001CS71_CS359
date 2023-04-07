
import sys
import socket
import threading


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
except socket.error as e:
    print('Error:', e)
    sys.exit(1)


# Define the server host and port
HOST = ip_address
PORT = port


# Listen for incoming connections
server_socket.listen(1)
print(f"Server is listening on port {PORT}")


# claculater
def calculate(expression):
    try:
        return str(eval(expression))
    except:
        return "Error enter a valid string"




# Lists For Clients and Their Nicknames
clients = []
names = []

# function for clint connection
def handle_client(client_socket, client_address):
    print(f'Client {client_address} connected')

    # receive data from the client
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
            # Removing And Closing Clients
            index = clients.index(client_socket)
            clients.remove(client_socket)
            client_socket.close()
            name = names[index]
            names.remove(name)
            print(f":{name} connection closed!:")
            break

    client_socket.close()


while True:
    # Wait for a connectionXZXZZXX
    client_socket, client_address = server_socket.accept()
    
    # Request And Store name

    name = client_socket.recv(1024).decode('ascii')
    names.append(name)
    clients.append(client_socket)
    # Print  name
    print(f"Now  {name} is connected")

    client_socket.send('Connected to server!'.encode('ascii'))
    # create a new thread to handle the client connection
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
