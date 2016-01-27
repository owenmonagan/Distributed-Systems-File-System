import SocketServer
import logging
import random
import threading
import logging
from parse_request import parse_message
from password_store import add_user, find_user_password
from DistributedFileAccess.server_address_info import get_lan_ip
from encrypt_decrypt import decrypt_func
from session_key_generator import session_key
from token_creator import prepare_token
from server_keys import add_server, find_server_key
host, port= "0.0.0.0", 6596


class ThreadedTCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        #log_in_request form #####\nUserID
        self.log_in_request = self.request.recv(1024)
        self.encyripted_message, self.user_id = parse_message(self.log_in_request)
        self.password=find_user_password(self.user_id)
        print self.password
        self.message= decrypt_func(self.password, self.encyripted_message)
        print self.message

        self.session_key=session_key
        self.server_encryption_key=find_server_key()

        self.ticket=self.session_key


        self.token= prepare_token()
        #prepare token
        #send token

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass




if __name__ == "__main__":
    logging.basicConfig(filename='logging.log',level=logging.DEBUG)
    my_ip = get_lan_ip()
    #h, p = my_ip, int(sys.argv[1])
    authentication_server = ThreadedTCPServer((host, port), ThreadedTCPHandler)
    serverIP, serverPort = authentication_server.server_address  # find out what port we were given

    print(serverIP)
    print(serverPort)
    authentication_server.server_alive=True
    #add_user("owen",1234)
    #add_user("jam",4321)
    try:
        server_thread = threading.Thread(target=authentication_server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        while(authentication_server.server_alive==True):
            pass

        authentication_server.shutdown()
        authentication_server.server_close()
        exit()

    except KeyboardInterrupt:
        print("Key board interrupt \nServer Shutting Down")
        authentication_server.shutdown()
        authentication_server.server_close()
        exit()