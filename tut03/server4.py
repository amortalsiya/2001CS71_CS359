import select
import socket
import sys
import queue

inputs = [] # sockets from which we expect to read
outputs = [] # sockets from which we expect to write
message_queues = {} # outgoing message queues for each socket
client_addresses = {} # mappes socket's connection to its address


def create_socket():
    try:
        global host, port, server
        host = sys.argv[1]
        port = int(sys.argv[2])
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(0) # now server won't get blocked
    except socket.error as message:
        print("Socket Creation Error: " + str(message))
        exit(0)


def bind_socket():
    try:
        global host, port, server
        print("Binding the Port: " + str(port))
        server.bind((host, port))
        server.listen(0)
        inputs.append(server)
    except socket.error as message:
        print("Socket Binding Error: " + str(message))
        exit(0)


def echo(message):
    return message


def socket_accept(server):
    connection, address = server.accept()
    print("Connection has been established with " +
          address[0] + ":" + str(address[1]))
    client_addresses[connection] = address
    return connection


def generate_result(connection, data):
    address = client_addresses[connection]
    message = data.decode() # decode from byte
    result = str(echo(message))
    print("Message received [" + message + "] from " +
          address[0] + ":" + str(address[1]))
    return result


def send_result(connection, result):
    address = client_addresses[connection]
    connection.send(result.encode()) # encode to byte
    print("Message sent to " + address[0] + ":" + str(address[1]))


def close_connection(connection):
    address = client_addresses[connection]
    connection.close()
    print("Connection has been closed with " +
          address[0] + ":" + str(address[1]))


def SELECT():
    while inputs:
        readable, writable, exceptional = select.select(
            inputs, outputs, inputs)
        
        for s in readable: # contains list of sockets available to be read
            if s is server: # ready to accept incoming connection
                connection = socket_accept(s)
                connection.setblocking(0)
                inputs.append(connection) # adding the new connection to the list of inputs to monitor
                message_queues[connection] = queue.Queue()
            else:
                data = s.recv(1024)
                if data: # data sent from an established connection
                    result = generate_result(s, data)
                    message_queues[s].put(result)
                    if s not in outputs:
                        outputs.append(s)
                else: # client has disconnected
                    close_connection(s)
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    del client_addresses[s]
                    del message_queues[s]

        for s in writable:
            try:
                next_message = message_queues[s].get_nowait()
            except queue.Empty:
                outputs.remove(s) # so that select() does not indicate that the socket is ready to send data
            else:
                send_result(s, next_message)

        for s in exceptional: # if there is an error with a socket
            close_connection(s)
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            del client_addresses[s]
            del message_queues[s]


def main():
    create_socket()
    bind_socket()
    SELECT()


if __name__ == "__main__":
    
    main()
