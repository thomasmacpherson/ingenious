from ingeniousModule import *


remote_port = int(input("What is the remote port?"))
ip = socket.gethostbyname(remote_host)
s.connect((ip, remote_port))
playerNumber = int(s.recv(1024))
print(playerNumber)
players = int(s.recv(1024).decode("utf-8"))
running =True

while running:
   mess = s.recv(1024)
    if mess != b'':
        mess = mess.decode("utf-8")
        print(mess)
        if mess == str(playerNumber):
             #Player turn            
            pygame.event.clear()
            turn = True

            while turn:
                for event in pygame.event.get():       
                    if event.type == pygame.QUIT:
                        running = False
     
                    # handle MOUSEBUTTONUP
                    if event.type == pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()

                        for index, obj in enumerate(tilesInHand[playerTurn]):
                            if activeTile == 0:
                                if obj.checkPoint(pos):
                                    activeTile = obj
                                    activeTileIndex = index

                        for row in places:
                            for obj in row:
                                obj.checkPoint(pos)      




        elif mess[0] == 'S':
            print(int(mess[1]))
            print(int(mess[2]))
            print(CharToInt(mess[3]))

            colourScores[int(mess[1])][int(mess[2])] = CharToInt(mess[3])
            print(colourScores)
        elif mess[0] == 'M':
            places[CharToInt(mess[1])][CharToInt(mess[2])] = int(mess[3])
            places[CharToInt(mess[4])][CharToInt(mess[5])] = int(mess[6])
            for row in places:
                print(row)
        elif mess[0] == 'T':
            tiles.append((int(mess[1]),int(mess[2])))
            print("Tile colour " + mess[1] + mess[2])
            print(tiles)
            

#ORIGINAL GAME LOOP
running = True
while running:

    clock.tick(FPS)
    for event in pygame.event.get():       
        if event.type == pygame.QUIT:
            running = False
 
        # handle MOUSEBUTTONUP
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            for row in places:
                for obj in row:
                    obj.checkPoint(pos)      

            for index, obj in enumerate(tilesInHand[playerTurn]):
                if activeTile == 0:
                    if obj.checkPoint(pos):
                        activeTile = obj
                        activeTileIndex = index

    screen.fill(BLACK)
    currentPlayerText = myFont2.render(str(playerTurn), False, WHITE)
    screen.blit(playerText,(550,20))
    screen.blit(currentPlayerText,(660,20))

    for row in places:
        for obj in row:
            obj.draw(screen)

    for player in range(players):
        for obj in tilesInHand[player]:
            obj.draw(screen)

        drawScoreBoard(screen, player)

    pygame.display.flip()       

pygame.quit()