import socket
 
def Main():
    mySocket = socket.socket()
    
    #host = socket.gethostname()
    maxLaptopHost = "192.168.1.176"
    port = 5000
     
    mySocket.connect((maxLaptopHost,port))
     
         
         
    while True:
        data = mySocket.recv(1024).decode()
        print ('Received from server: ' + data)          
        

        message = input(" -> ")
        mySocket.send(message.encode())

        data = mySocket.recv(1024).decode()
        print ('Received from server: ' + data) 
                 
    mySocket.close()
 
if __name__ == '__main__':
    Main()	