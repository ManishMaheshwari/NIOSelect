import select
import sys
from socket import *

s = socket(AF_INET, SOCK_STREAM)
host = ''
port = 6003
s.bind((host, port))

# Listening on Server Socket
s.listen(5)

# Connection accepted. Establish connection with client.
clientSocket, addr = s.accept()
print("Accepted.")
clientSocket.setblocking(False)


def terminate(c, s):
    c.shutdown(1)
    c.close()
    s.close()


def eventloop():
    while True:
        try:
            socket_list = [sys.stdin, clientSocket]  # read list

            # DOC of select method:
            # Wait until one or more file descriptors are ready for some kind of I/O.
            # The first three arguments are sequences of file descriptors to be waited for:
            # rlist -- wait until ready for reading
            # wlist -- wait until ready for writing
            # xlist -- wait for an ``exceptional condition''
            # If only one kind of condition is required, pass [] for the other lists.
            # A file descriptor is either a socket or file object, or a small integer
            # gotten from a fileno() method call on one of those.
            #
            # The optional 4th argument specifies a timeout in seconds; it may be
            # a floating point number to specify fractions of seconds.  If it is absent
            # or None, the call will never time out.
            #
            # The return value is a tuple of three lists corresponding to the first three
            # arguments; each contains the subset of the corresponding file descriptors
            # that are ready.

            # We only pass the readable FD list to select.
            read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
        except Exception as ex:
            print("Connection error.")

        # These are the FD's that are ready to be read.
        for sock in read_sockets:
            if sock == clientSocket:
                data = clientSocket.recv(1024).decode()
                print(data)
                if (data.startswith("Bye")):
                    print("Disconnecting.")
                    terminate(clientSocket, s)
                    return
            else:
                #This is sys.stdin
                message = raw_input()
                if message.startswith("X"):
                    clientSocket.sendall(message.encode())
                if message.startswith("Bye"):
                    clientSocket.sendall(message.encode())
                    terminate(clientSocket, s)
                    return


eventloop()
