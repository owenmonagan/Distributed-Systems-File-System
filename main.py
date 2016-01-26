import SocketServer
import logging
import threading
import logging
import os
import sys
import socket
from DistributedFileAccess.server_address_info import get_lan_ip, host, port
from DistributedFileAccess.write_file_to_server import write_file
from DistributedFileAccess.read_file_from_server import read_file

studentNumber = "8225096d25e2f49ea3efabe515fd9f58707934a0cb3a9494aea8d64ec363cd17"

class ThreadedTCPHandler(SocketServer.BaseRequestHandler):

    def setup(self):
        self.client_connected=True
        self.return_string= ""

    def handle(self):
        while(self.client_connected):

            request_string = self.request.recv(1024)
            if ("KILL_SERVICE" in request_string):
                #print ("Service killed by Client\n")
                self.client_connected=False
                file_server.server_alive = False

            elif("WRITE" in request_string):
                print(request_string)
                write_file(self, request_string)

            elif("READ" in request_string):
                print(request_string)
                read_file(self, request_string)


            elif ("HELO" in request_string):
                #print(request_string)
                lines=request_string.split()
                request_string = ("HELO {}\nIP:{}\nPort:{}\nStudentID:{}\n".format(lines[1], my_ip, p, studentNumber))
                self.request.send(request_string)

            else:
                pass

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass




if __name__ == "__main__":
    logging.basicConfig(filename='logging.log',level=logging.DEBUG)
    my_ip = get_lan_ip()
    #h, p = my_ip, int(sys.argv[1])
    file_server = ThreadedTCPServer((host, port), ThreadedTCPHandler)
    serverIP, serverPort = file_server.server_address  # find out what port we were given

    print(serverIP)
    print(serverPort)
    file_server.server_alive=True

    try:
        server_thread = threading.Thread(target=file_server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        while(file_server.server_alive==True):
            pass

        file_server.shutdown()
        file_server.server_close()
        exit()

    except KeyboardInterrupt:
        print("Key board interrupt \nServer Shutting Down")
        file_server.shutdown()
        file_server.server_close()
        exit()