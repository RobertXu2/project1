# Import the socket module to use networking functions
from socket import *

# Define the port number the server will listen on
serverPort = 6789

# Create a TCP server socket
# AF_INET means we're using IPv4, and SOCK_STREAM means it's a TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare the server socket
# Bind the socket to the server's IP address and port
# An empty string ('') means the server will listen on all available interfaces
serverSocket.bind(('', serverPort))

# Start listening for incoming connections
# The number '1' means the server can handle one connection at a time
serverSocket.listen(1)

# Print a message to confirm the server is running
print('The web server is up on port:', serverPort)

# Start an infinite loop to keep the server running and accepting connections
while True:

    # Accept a connection from a client
    # connectionSocket is the new socket for this connection, and addr is the client's address
    connectionSocket, addr = serverSocket.accept()

    # Try to handle the client's request
    try:
        # Receive the HTTP request from the client
        # The request is received as bytes, so we decode it to a string
        message = connectionSocket.recv(1024).decode()

        # Print the received message and its components for debugging
        print(message, '::', message.split()[0], ':', message.split()[1])

        # Extract the filename from the HTTP request
        # The filename is the second part of the request (e.g., '/simpleWeb.html')
        filename = message.split()[1]

        # Print the filename for debugging (removing the leading '/')
        print(filename, '||', filename[1:])

        # Open the requested file in read mode
        # filename[1:] removes the leading '/' to get the actual file path
        with open(filename[1:], 'r') as f:
            # Read the contents of the file
            outputdata = f.read()

        # Send an HTTP response header to the client
        # The header includes the HTTP version, status code, and content type
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'

        # Send the header to the client (encode it as bytes first)
        connectionSocket.send(header.encode())

        # Send the contents of the requested file to the client
        connectionSocket.send(outputdata.encode())

        # Close the connection socket after sending the response
        connectionSocket.close()

    # If the file is not found, handle the error
    except IOError:
        # Prepare an HTTP 404 Not Found response header
        error_header = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n'

        # Prepare a simple HTML error message for the 404 page
        error_message = '<html><body><h1>404 Not Found</h1></body></html>'

        # Send the 404 header to the client (encode it as bytes first)
        connectionSocket.send(error_header.encode())

        # Send the 404 error message to the client
        connectionSocket.send(error_message.encode())

        # Close the connection socket after sending the error response
        connectionSocket.close()

# Close the server socket (this line will never be reached because of the infinite loop)
serverSocket.close()
