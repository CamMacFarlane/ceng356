import socket
import threading
from random import randint

class ThreadedServer(object):
    def __init__(self, host, port):
        print ("in init")
        self.port = port
        self.host = host
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        print ("in listen")
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        print ("in listen to client")
        while True:
            msg = "Guess my number!"
            client.send(msg.encode())
    
            data = client.recv(1024).decode()

            data = str(data)
            data = int(data)
            print("You Guessed : " + str(data))
            num = randint(0,5)
            if (int(data) == num):
                msg = "winner winner"
            else:
                msg = ("loser loser num was " + str(num))

            if not data:
                    break
           # print ("from connected  user: " + str(data))
             
            #data = str(data).upper()
            #print ("sending: " + str(data))
            client.send(msg.encode())
        client.close()

if __name__ == "__main__":
    port_num = 5000
    ThreadedServer('0.0.0.0', port_num).listen()