import socket
import time
import random
from datetime import datetime
intro = 0 
waiting = 1
recievingGameData = 2
battle = 3
done = 4 
def Main():
    mySocket = socket.socket()
    
    host = socket.gethostname()
    #host = "192.168.1.176" #max's laptop
    port = 5000
     
    mySocket.connect((host,port))
    ackString = "ack"     
    state = intro

    while True:

        if(state == intro):
            intromsg = """\



      .~~~~`\\~~\\\n
     ;       ~~ \\\n
     |           ;\n
 ,--------,______|---.\n
/          \\-----`    \\\n
`.__________`-_______-'\n

Howdy Partner! Welcome to Quicker Draw!
Type the letters faster than your opponent to shoot that cactus sucker before they shoot you!

Speanking of which, where is that coward?



"""
            print(intromsg)
            state = waiting

        if(state == waiting):
            data = mySocket.recv(1024).decode()
            #print ('Received from server: ' + data)   
            #print("Waiting for other cowboy.")
            if (data == "letterList"):
                mySocket.send(ackString.encode())
                state = recievingGameData
        
        elif(state == recievingGameData):
            print("Your oponent has arrived!")
            time.sleep(1)
            print("It's almost noon!")
            
            data = mySocket.recv(1024).decode()
            print ('You need to type "' + data + '"  at the stoke of noon!')
            shootSequence = data
            state = battle         
       
        elif(state == battle):
            waitTime = random.randint(3,10)
            for i in range (0, waitTime):  
                print("11:59...")
                time.sleep(1)
            print("NOON!")
            start = datetime.now()    
            userString = input("shoot!")
            stop = datetime.now()
            if (userString == shootSequence):
                reactionDateTime = stop - start
                reactionTimeSeconds = reactionDateTime.total_seconds()
                print("your reaction time was... " + str(reactionTimeSeconds))
            else:
                print("you fumble with your gun and die")
                reactionTimeSeconds = 9999.69
            mySocket.send(str(reactionTimeSeconds).encode())
            state = done
       
        elif(state == done):
            data = mySocket.recv(1024).decode()
            print (data)   
            time.sleep(5)      
            state = waiting

        else:
            print("undefined state!")
                 
    mySocket.close()
 
if __name__ == '__main__':
    Main()	
