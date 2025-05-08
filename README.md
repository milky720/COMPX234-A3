# COMPX234-A3
20233006400 MiaoKeyan‘s Assignment3

This program implements a distributed "tuple space" system based on a client-server architecture. 
The server uses multithreading to handle concurrent requests from multiple clients, supporting three operations: PUT (add key-value tuples), GET (retrieve and delete key-value pairs), and READ (read key-value pairs). 
Clients send requests via text files, while the server maintains a shared tuple space and periodically outputs statistics (e.g., tuple count, operation metrics). 
All operations communicate over TCP sockets, with thread locks ensuring data consistency.

How to test my networked system:  ^_^
  Run the server.py
  Run the client.py
  Enter the following in the terminal: 
    python client.py localhost 51234 test-workload-1/test-workload/client_1.txt
    (format: python client.py <host> <port> <request_file>)
    (Testing for client_2 to client_10 follows the same principle.)