import select
import sys
from socket import *

s = socket(AF_INET, SOCK_STREAM)
s.connect(('127.0.0.1', 6003))

def terminate(s):
    s.close()


def eventloop():
    while 1:
        try:
            socket_list = [sys.stdin, s]
            read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
        except Exception as ex:
            print("Connection error.")

        for sock in read_sockets:
            if sock == s:
                data = s.recv(1024).decode()
                print(data)
                if data.startswith("Bye"):
                    print("Disconnecting")
                    terminate(s)
                    return
            else:
                message = raw_input()
                s.sendall(message.encode())
                if message.startswith("Bye"):
                    terminate(s)
                    return


eventloop()
