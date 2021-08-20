import pygame
import time
pygame.init()
from graph import Graph
from misc import Misc
from backend.agent import *
from backend.env import Env
from backend.data import *
from yishun_graph import YishunGraph

WINDOW_SIZE = (1200,800)
BACKGROUND = (255,255,255)


#Create the screen
screen = pygame.display.set_mode(WINDOW_SIZE)

#title and icon
pygame.display.set_caption("Demo")

#misc functions
misc = Misc(screen)


def play(difficulty):
    #init env
    environment=Env(difficulty)
    
    #get goals
    goals = environment.exits
    
    #init graph
    if difficulty=='yishun':
        #init defender
        defender=AgentEvalYishun()
        graph = YishunGraph(screen,environment.attacker_init,environment.defender_init[0],goals)
    else:
        #init defender
        defender=AgentEval(difficulty)
        #get data
        data = environment.mapSize
        data.append(environment.adjlist)
        graph = Graph(screen,data,environment.attacker_init,environment.defender_init[0],goals)

    #main loop
    running = True
    #limit for num of turns
    limit=environment.time_horizon
    #gameover var
    gameover = False

    game_state=environment.reset()

    while running:
        screen.fill(BACKGROUND)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if difficulty=='yishun':
                if event.type == pygame.MOUSEBUTTONUP:
                    #player select where to move for thief
                    turn, attacker_a =graph.check_move()
                    if turn:
                        #police move base on algo here
                        defender_obs, attacker_obs = game_state.obs()
                        def_current_legal_action, att_current_legal_action = game_state.legal_action()
                        defender_a = defender.select_action([defender_obs], [def_current_legal_action])
                        game_state = environment.simu_step(defender_a, attacker_a)
                        #move police in graph
                        graph.thief_move()
                        graph.police_move(defender_a)
                        limit-=1
                    #after police has moved etc....
                    graph.reset_move()

            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #player select where to move for thief
                    if not gameover:
                        turn, attacker_a =graph.choose(event.pos)
                        if turn:
                            #police move base on algo here
                            defender_obs, attacker_obs = game_state.obs()
                            def_current_legal_action, att_current_legal_action = game_state.legal_action()
                            defender_a = defender.select_action([defender_obs], [def_current_legal_action])
                            game_state = environment.simu_step(defender_a, attacker_a)
                            graph.police_move(defender_a)
                            limit-=1
        
        #check who win
        result = graph.checkWin()
        if result ==1: #player win
            misc.message_to_screen('Player wins!',(255,0,0),0,0,'large')
            m= misc.button("Restart",900,320,150,150,(55,255,255),(0,255,0))
            gameover = True
            if m:
                return
        elif result ==2: #police win
            #draw game boundary
            pygame.draw.rect(screen,(0,0,0),(50,50,700,700),1)
            #display graph
            graph.display_lose()
            #display turns left
            misc.message_to_screen('You got caught! Player lose...',(0,0,255),330,-200,'small')
            m1= misc.button("Restart",900,320,150,150,(55,255,255),(0,255,0))
            gameover = True
            if m1:
                return
        elif limit==0:
            misc.message_to_screen('Time Out! Player Lose...',(0,255,0),0,0,'large')
            m2= misc.button("Restart",500,500,150,150,(55,255,255),(0,255,0))
            gameover = True
            if m2:
                return
        else:
            #draw game boundary
            pygame.draw.rect(screen,(0,0,0),(50,50,700,700),1)
            #display graph
            graph.display()
            #display turns left
            misc.message_to_screen('Turns left: '+str(limit),(0,0,255),310,-200,'medium')
            m= misc.button("Return",900,320,150,150,(55,255,255),(0,255,0))
            if m:
                return
        pygame.display.update()

def main():
    #main loop
    running = True
    while running:
        screen.fill(BACKGROUND)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        #select difficulty
        misc.message_to_screen("Select Difficulty",(0,0,0),0,-150,'large')
        e= misc.button("Easy",200,350,150,150,(55,255,255),(0,255,0))
        m= misc.button("Medium",368,350,150,150,(55,255,255),(0,255,0))
        h= misc.button("Hard",532,350,150,150,(55,255,255),(0,255,0))
        y = misc.button("Sg",700,350,150,150,(55,255,255),(0,255,0))
        if e:
            play('easy')
        if m:
            play('medium')
        if h:
            play('hard')
        if y:
            play('yishun')
        

        pygame.display.update()

main()