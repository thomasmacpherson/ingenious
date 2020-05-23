from ingeniousModule import *

numberOfPlayers = int(input("How many clients to wait for?"))
setUp(places)

s.bind(('localhost', port))         
print("socket binded to %s" %(port))
  
# put the socket into listening mode 
s.listen(5)      
print("socket is listening" )
c = []
addr = []

for i in range(players):
    c[i], addr[i] = s.accept()      
    print('Got connection from', addr[i] )  
    sendToClient(i, i) 

sendToAllClients(numberOfPlayers)

for client in range(numberOfPlayers):
    for tile in range(6):
        sendToClient(client, "T" + str(tiles[client][tile].colourPair[0]) + str(tiles[client][tile].colourPair[1]))
time.sleep(1)
while True:
    #Player turn
    sendToAllClients(playerTurn)
    clientResponse = c[playerTurn].recv(1024).decode("utf-8")
    print(clientResponse)        
    if clientResponse[0] == "M":
    	sendToClient(i, "T" + str(random.randint(0,6))+str(random.randint(0,6)))
    	
        sendToAllButOne(playerTurn, clientResponse)
        sendToAllClients("S" + str(playerTurn) + str(colour) + IntToCharacter(score))