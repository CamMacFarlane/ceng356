import socket
from random import randint  
def Main():

    mySocket = socket.socket()
    
    host = socket.gethostname()
    port = 5000
     
    mySocket.bind((host,port))
     
    mySocket.listen(1)
    conn, addr = mySocket.accept()
    print ("Connection from: " + str(addr))
    

    while True:
            msg = "Guess my number!"
            conn.send(msg.encode())
    
            data = conn.recv(1024).decode()

            data = str(data)
            data = int(data)
            num = randint(0,5)

            if (int(data) == num):
            	msg = "winner winner"
            else:
                msg = ("loser loser num was " + str(num))

            if not data:
                    break

            conn.send(msg.encode())
             
    conn.close()
     
if __name__ == '__main__':
    Main()