
# from datetime import datetime
# start_time = datetime.now()


# def dvr():


# dvr()

# #This shall be the last lines of the code.
# end_time = datetime.now()
# print('Duration of Program Execution: {}'.format(end_time - start_time))


import queue  # Importing the queue module
import threading  # Importing the threading module
import time  # Importing the time module
from os.path import exists  # Importing the os module


class Router:  # Defining a Router class
    INF = 1e18  # Defining a large constant as infinity

    def __init__(self, router_id):  # Constructor to initialize a Router object
        self.id = router_id  # Assigning the router ID
        self.iteration_count = 0  # Initializing the iteration count to 0
        # Creating an empty set to store the changes done in the routing table
        self.changes = set()
        # Creating an empty dictionary to store the neighbours and edge costs -> dict[Router, int]
        self.neighbours = {}
        # Creating an empty list to store the routing table entries -> list[list[Router, Router, int]]
        self.routing_table = []
        # Creating a queue object to store the incoming routing tables.
        self.queue = queue.Queue()

    # Method to add a neighbour to the router
    def add_neighbours(self, neighbour_node, edge_cost):
        if self == neighbour_node:  # Check if neighbour node is the same as the router itself
            print("Self loop is not allowed.")  # Print a warning message
            exit(0)  # Exit the program
        # Add the neighbour and edge cost to the neighbours dictionary
        self.neighbours[neighbour_node] = edge_cost

    # Method to initialize the routing table of the router
    def initialise_routing_table(self, routers):
        for router in routers:  # Loop over all routers in the network
            # Check if the router is a neighbour of the current router
            if self.neighbours.get(router):
                self.routing_table.append(  # If yes, add a routing table entry for this neighbour
                    [router, router, self.neighbours.get(router)])  # [Destination, Via, Cost]
            elif router == self:  # If the router is the current router itself
                # Add a routing table entry for this router itself
                self.routing_table.append([router, router, 0])
            else:
                # Add a routing table entry for all other routers in the network
                self.routing_table.append([router, None, self.INF])

    # Method to print the routing table of a router
    def print_routing_table(self, lock):
        # Acquire the lock before executing the code inside the method
        lock.acquire()

        # Define a string of dashes for use in the output formatting
        DASHES = "-" * 41
        # Define a string to represent the router and iteration count for use in the output formatting
        head_string = f"From Router: {self.id} | Iteration Count: {self.iteration_count}"
        # Print a line of dashes to separate the output
        print(DASHES)
        # Print the header string for this router and iteration count, with proper spacing and alignment
        print(f"| {head_string:<37} |")
        # Print another line of dashes to separate the output
        print(DASHES)
        # Print the table headers for the routing table output
        print("| To Router  | Cost       | Via Router  |")
        print(DASHES)

        # Iterate through each element of the routing table
        for element in self.routing_table:
            # Extract the destination router ID from the element
            to_router = element[0].id
            # If the destination router is in the set of recently changed routers, prepend a "*" to the output
            if element[0].id in self.changes:
                to_router = "* " + to_router
                self.changes.remove(element[0].id)
            # Otherwise, prepend a space to the output
            else:
                to_router = "  " + to_router
            # Print the routing table entry, with proper spacing and alignment
            print(f"| {to_router:<10} |"
                  + f" {element[2] if element[2] != self.INF else 'INF' :<10} |"
                  + f" {(element[1].id if element[1] else '--'):<11} |")

        # Print another line of dashes to separate the output
        print(DASHES, end="\n\n")
        # Release the lock
        lock.release()

    def forward_routing_table(self):
        # For each neighbor in the router's list of neighbors
        for neighbour in self.neighbours.keys():
            # Add this router's instance to the neighbor's message queue
            neighbour.queue.put(self)

    def update_routing_table(self):
        # Set a flag to false indicating that no changes have been made to the routing table
        is_there_a_change = False

        # Loop forever until a break statement is reached
        while True:
            try:
                # Get the next item in the router's message queue
                neighbour = self.queue.get(block=False)

                # Determine the cost to the neighbor and its routing table
                cost_to_neighbour = self.neighbours[neighbour]
                routing_table_of_neighbour = neighbour.routing_table

                # Loop through the router's routing table and update entries as necessary
                for index, entry in enumerate(self.routing_table):
                    # New cost is the cost to the neighbour (say X) plus the cost from X to any other router (say Y)
                    new_cost = cost_to_neighbour + \
                        routing_table_of_neighbour[index][2]
                    # If new cost is less than the cost from the current router to Y, use B-F equation
                    if new_cost < entry[2]:
                        is_there_a_change = True
                        self.changes.add(entry[0].id)
                        self.routing_table[index] = [
                            entry[0], neighbour, new_cost]
            except:
                # If the router's message queue is empty, break out of the loop
                break

        # Return the flag indicating whether a change was made to the routing table
        return is_there_a_change


def parse_input():
    number_of_routers = 0               # Initialize the number of routers to zero
    routers = []                        # Create an empty list for routers
    # Create an empty dictionary for mapping router IDs to their index in the routers list
    routers_map = {}

    filename = "topology.txt"           # Set the filename to "topology.txt"

    if not exists(filename):
        print("`topology.txt` does not exist in the current directory.")
        exit(0)

    with open(filename) as line:        # Open the file for reading
        # Read the first line and convert the string to an integer to get the number of routers
        number_of_routers = int(line.readline().strip())

        for index, router_id in enumerate(line.readline().strip().split(" ")):
            # Read the second line, split the string by space and iterate through the resulting list
            # Create a Router object for each router ID and add it to the routers list
            routers.append(Router(router_id))
            # Add the router ID and its index in the routers list to the routers_map dictionary
            routers_map[router_id] = index

        # If the length of the routers_map dictionary is not equal to the number_of_routers
        if len(routers_map) != number_of_routers:
            print("Duplicate nodes found.")         # Print an error message
            exit(0)                                 # And exit the program

        for edge in line.readlines():              # Iterate through the remaining lines of the file
            # Remove any leading or trailing white space from the line
            edge = edge.strip()
            if edge == "EOF":                       # If the line is "EOF"
                break                               # Stop iterating

            # Split the line by space and get a list of the resulting strings
            edge = edge.split(" ")
            if len(edge) != 3:                      # If the length of the list is not 3
                # Print an error message
                print(
                    "The edge description line must contain only three space separated words.")
                exit(0)                             # And exit the program

            # Get the index of the first node from the routers_map dictionary
            first_node = routers_map[edge[0]]
            # Get the index of the second node from the routers_map dictionary
            second_node = routers_map[edge[1]]
            # Convert the third string to an integer to get the edge cost
            edge_cost = int(edge[2])

            # Add the second node as a neighbour of the first node with the given edge cost
            routers[first_node].add_neighbours(routers[second_node], edge_cost)
            # Add the first node as a neighbour of the second node with the given edge cost
            routers[second_node].add_neighbours(routers[first_node], edge_cost)

    # Return the number of routers and the routers list as a tuple
    return number_of_routers, routers


# Method to initialize the routing table for each router object
def initialise_routers(routers):
    for router in routers:
        router.initialise_routing_table(routers)


# Method to print the routing table for all routers
# It takes a lock as an argument to prevent multiple threads from writing to the console simultaneously
def print_all_routing_tables(routers, lock):
    print("#" * 50, end="\n\n")
    for router in routers:
        router.print_routing_table(lock)
    print("#" * 50, end="\n\n")


# Method to simulate the process of routing information between routers
def simulate(router, lock, routers):
    # Set the waiting time between each iteration to 2 seconds
    waiting_time = 2
    # Set the flag to True indicating that a change is initially present in the routing table
    is_there_a_change = True
    # Set the flag to True indicating that the simulation can continue
    can_continue = True

    # Continue the simulation while the flag can_continue is True
    while can_continue:
        # Increment the iteration count of the current router
        router.iteration_count += 1

        # If there is a change in the routing table, forward the routing table
        if is_there_a_change:
            router.forward_routing_table()

        # Update the routing table and check if there is a change
        is_there_a_change = router.update_routing_table()

        # If there is a change in the routing table, print the routing table
        if is_there_a_change:
            router.print_routing_table(lock)

        # Wait for the specified time before the next iteration
        time.sleep(waiting_time)

        # Set the flag can_continue to False
        can_continue = False

        # Check if any router has any incoming routing table in its queue, if so, set the can_continue flag to True
        for each_router in routers:
            can_continue |= not each_router.queue.empty()


def main():
    # Create a threading lock to control access to shared resources
    lock = threading.Lock()

    # Call parse_input function to get the number of routers and their details from topology.txt file
    number_of_routers, routers = parse_input()

    # Call the initialise_routers function to set the initial routing table for each router
    initialise_routers(routers)

    # Call the print_all_routing_tables function to print the initial routing table for all routers
    print_all_routing_tables(routers, lock)

    # Create a list to hold all the threads
    threads = []

    # Loop over all routers
    for router in routers:
        # Create a new thread for each router
        # The target function for each thread is simulate function
        # The router object, threading lock and routers list are passed as arguments to the simulate function
        thread = threading.Thread(
            target=simulate, args=(router, lock, routers))
        thread.start()
        threads.append(thread)

    # Loop over all threads
    for thread in threads:
        # Wait for each thread to finish executing
        thread.join()

    # Call the print_all_routing_tables function to print the final routing table for all routers
    print_all_routing_tables(routers, lock)


if __name__ == "__main__":
    main()
