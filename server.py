import socket
import threading
import queue
import random 
import string
import time
import sys


player1RT = -1
player2RT = -1
class ThreadedServer(object):


    def __init__(self, host, port):
    	print ("initializing")
    	self.port = port
    	self.host = host
    	self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    	self.sock.bind((self.host, self.port))

    	#initalize number of players
    	self.playerNumber = 0

    	#define queues for thread communication
    	self.p1rq = queue.Queue()	#player 1 read queue
    	self.p1wq = queue.Queue()	#player 1 write queue
    	self.p2rq = queue.Queue()	#player 2 read queue
    	self.p2wq = queue.Queue()	#player 2 write queue

    def listen(self):
    	print ("listening for clients")
    	self.sock.listen(5)

    	queueSize = self.p1rq.qsize()

    	#handle connectons
    	#connect to player 1
    	client, address = self.sock.accept()
    	threading.Thread(target = self.listenToClient1,args = (client,address)).start()
    	self.playerNumber = 1

    	#connect to player 2
    	client, address = self.sock.accept()
    	self.playerNumber = 2
    	threading.Thread(target = self.listenToClient2,args = (client,address)).start()

    	#wait for both players to read the intro
    	time.sleep(5)

    	while True:
    		#game logic here
    		self.mainGame()


    def listenToClient1(self, client, address):
        print ("player 1 connected")
        global player1RT
        player1RT = -1
        while True:
            qitem = self.p1rq.get()
            if qitem == "letterList":
                llist =  self.p1rq.get()
       	        client.send(qitem.encode())
       	        
                if(client.recv(100).decode() == "ack"):
                    client.send(llist.encode())
                    raw = client.recv(100).decode()
                    print("recived player 1 rt = " + raw)
                    player1RT = float(raw)
                    time.sleep(1)
                    client.send(self.p1rq.get().encode())
       	        else:
                    break

        client.close()

    def listenToClient2(self, client, address):
        print ("player 2 connected")
        global player2RT
        player2RT = -1
        while True:

            qitem = self.p2rq.get()

            if qitem == "letterList":
                llist =  self.p2rq.get()

                client.send(qitem.encode())
       	        if(client.recv(100).decode() == "ack"):
                    client.send(llist.encode())
                    
                    raw = client.recv(100).decode()
                    print("recived player 2 rt = " + raw)
                    player2RT = float(raw)
                    time.sleep(1)
                    client.send(self.p2rq.get().encode())
       	        else:
                    break
        client.close()
    	
    def mainGame(self):

        global player2RT
        global player1RT

        grab = random.choice(string.ascii_lowercase)
        draw = random.choice(string.ascii_lowercase)
        aim = random.choice(string.ascii_lowercase)
        cock = random.choice(string.ascii_lowercase)
        shoot = random.choice(string.ascii_lowercase)

        print ("The letters for this round are: [" + grab + "], [" + draw + "], [" + aim + "], [" + cock + "], [" + shoot + "]")

        #begin game

        #distribute the letters to both clients
        self.p1rq.put("letterList")
        self.p1rq.put(grab + draw + aim + cock + shoot)

        self.p2rq.put("letterList")
        self.p2rq.put(grab + draw + aim + cock + shoot)
        
        while((player1RT == -1) or (player2RT == -1)):
            print("waiting for clients to respond...")
            time.sleep(5)
        
        #player 2 won
        if(player1RT > player2RT):
            self.p1rq.put("LOSER")
            self.p2rq.put("WINNER")
        #player 1 won
        if(player1RT < player2RT):
            self.p1rq.put("WINNER")
            self.p2rq.put("LOSER")
      
        else:
            self.p2rq.put("LOSER")
            self.p1rq.put("LOSER")

        player1RT = -1
        player2RT = -1

        time.sleep(10)
            



if __name__ == "__main__":
	port_num = 5000
	ThreadedServer('0.0.0.0', port_num).listen()
