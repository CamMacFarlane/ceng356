import socket
import threading
import queue
import random 
import string
import time

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

    	while True:
        	#handle connectons
        	if self.playerNumber == 0:
        		#connect to player 1
        		client, address = self.sock.accept()
        		threading.Thread(target = self.listenToClient1,args = (client,address)).start()
        		self.playerNumber = 1
        	elif self.playerNumber == 1:
        		#connect to player 2
        		client, address = self.sock.accept()
        		self.playerNumber = 2
        		threading.Thread(target = self.listenToClient2,args = (client,address)).start()
        	else:
        		#game logic here

        		#generate 5 random letters
        		grab = random.choice(string.ascii_lowercase)
        		draw = random.choice(string.ascii_lowercase)
        		aim = random.choice(string.ascii_lowercase)
        		cock = random.choice(string.ascii_lowercase)
        		shoot = random.choice(string.ascii_lowercase)

        		print ("The letters for this round are: [" + grab + "], [" + draw + "], [" + aim + "], [" + cock + "], [" + shoot + "]")

        		#begin game

        		#distribute the letters to both clients
        		self.p1rq.put("letterList")
        		self.p1rq.put(grab)
        		self.p1rq.put(draw)
        		self.p1rq.put(aim)
        		self.p1rq.put(cock)
        		self.p1rq.put(shoot)

        		self.p2rq.put("letterList")
        		self.p2rq.put(grab)
        		self.p2rq.put(draw)
        		self.p2rq.put(aim)
        		self.p2rq.put(cock)
        		self.p2rq.put(shoot)

        		#test
        		time.sleep(5)

        		#countdown

        		#wait for correct sequence notification from either cliet

        		#declare winner

    def listenToClient1(self, client, address):
    	print ("player 1 connected")
    	msg = "You are Player 1"
    	client.send(msg.encode())

    	while True:
    		#example

            #msg = "You are Player 1"
            #client.send(msg.encode())
    
            #data = client.recv(1024).decode()

            #data = str(data)
            #data = int(data)
            #print("You Guessed : " + str(data))
            #num = randint(0,5)
            #if (int(data) == num):
            #    msg = "winner winner"
            #else:
            #    msg = ("loser loser num was " + str(num))

            #if not data:
            #        break
            #print ("from connected  user: " + str(data))
             
            #data = str(data).upper()
            #print ("sending: " + str(data))
        	#client.send(msg.encode())

        	qitem = self.p1rq.get()
        	

        	if qitem == "letterList":
        		grab = self.p1rq.get()
        		draw = self.p1rq.get()
        		aim = self.p1rq.get()
        		cock = self.p1rq.get()
        		shoot = self.p1rq.get()

        		client.send(qitem.encode())
        		client.send(grab.encode())
        		client.send(draw.encode())
        		client.send(aim.encode())
        		client.send(cock.encode())
        		client.send(shoot.encode())

    	client.close()

    def listenToClient2(self, client, address):
    	print ("player 2 connected")
    	msg = "You are Player 2"
    	client.send(msg.encode())

    	while True:
            #example

            #msg = "You are Player 1"
            #client.send(msg.encode())
    
            #data = client.recv(1024).decode()

            #data = str(data)
            #data = int(data)
            #print("You Guessed : " + str(data))
            #num = randint(0,5)
            #if (int(data) == num):
            #    msg = "winner winner"
            #else:
            #    msg = ("loser loser num was " + str(num))

            #if not data:
            #        break
            #print ("from connected  user: " + str(data))
             
            #data = str(data).upper()
            #print ("sending: " + str(data))
        	#client.send(msg.encode())

        	qitem = self.p2rq.get()

        	if qitem == "letterList":
        		grab = self.p2rq.get()
        		draw = self.p2rq.get()
        		aim = self.p2rq.get()
        		cock = self.p2rq.get()
        		shoot = self.p2rq.get()

        		client.send(qitem.encode())
        		client.send(grab.encode())
        		client.send(draw.encode())
        		client.send(aim.encode())
        		client.send(cock.encode())
        		client.send(shoot.encode())
    	client.close()

if __name__ == "__main__":
	port_num = 5000
	ThreadedServer('0.0.0.0', port_num).listen()