
import socket
import sys

# Get server IP and port number from command line arguments
if len(sys.argv) < 3:
    print('Usage: python server.py <ip address> <port number>')
    sys.exit(1)

# Define the server's IP address and port number
SERVER_IP = sys.argv[1]  # "127.0.0.1" localhost
SERVER_PORT = int(sys.argv[2])  # 5000 


#FOR SERVER 1 FAKE CLIENT UNCOMMENT &MULTY CLIENT  COMMENT  3 LINE BELOW
# fake_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# fake_client_socket.connect((SERVER_IP, SERVER_PORT))
# fake_client_socket.close()


# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



# Connect to the server
client_socket.connect((SERVER_IP, SERVER_PORT))
print("Connected to the server...")


# FOR MULTY CLIENT CHOOSE NAME FOR SERVER 2 UNCOMMENT  " SELECT  & CTRL+/" 

# name = input(" please Enter your name : ")
# client_socket.send(name.encode('ascii'))
# print("Now you are conn...")
# Reply = client_socket.recv(1024)
# print("Server replied:  " + Reply.decode())

# FUNCTION
while True:
    USER_inp = input(
        "Enter an arithmetic expression (e.g., 9 + 8, 4 / 2, 4 * 7): ")
    client_socket.send(USER_inp.encode('ascii'))

    RESULT = client_socket.recv(1024)
    print("Server replied: " + RESULT.decode())
    inp = input("Do you wish to continue? Y/N\n")
    if (inp == "N"):
        break


# Close the connection
print("close conection")
client_socket.close()
