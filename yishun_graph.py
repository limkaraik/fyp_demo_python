import pygame
from data import YISHUN,POSITION
police_img = pygame.image.load("./images/police.png")
thief_img = pygame.image.load("./images/robber.png")
exit_img = pygame.image.load("./images/exit.png")
jail_img = pygame.image.load("./images/jail.png")
map_img = pygame.image.load("./images/Final Yishun.PNG")

LEFT_BOUNDARY = 100
RIGHT_BOUNDARY = 700 
TOP_BOUNDARY = 100
BOTTOM_BOUNDARY = 700
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE=(255,255,255)
NODE_WIDTH=25
NODE_HEIGHT=25

class YishunGraph:

    #police given as array of pos
    def __init__(self,screen,thief,police,goals):
        self.graph = YISHUN
        self.num_police = len(police)
        self.police = police
        self.thief = thief[0]
        self.screen = screen
        self.police_icon = pygame.transform.scale(police_img,(NODE_WIDTH,NODE_HEIGHT))
        self.thief_icon = pygame.transform.scale(thief_img,(NODE_WIDTH,NODE_HEIGHT))
        self.exit_icon = pygame.transform.scale(exit_img,(NODE_WIDTH,NODE_HEIGHT))
        self.jail_icon = pygame.transform.scale(jail_img,(NODE_WIDTH,NODE_HEIGHT))
        self.map_img =  pygame.transform.scale(map_img,(700,700))
        self.police_visited = set(police)
        self.thief_visited = set(thief)
        self.edges={}
        self.goals= set(goals)
        self.move = 0
        self.next_thief = None

    def Node(self,x,y,width,height,inactive_color,active_color,pos):
        cur = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x+width > cur[0] > x and y+height > cur[1] > y:
            pygame.draw.circle(self.screen,active_color,(x+(width//2),y+(height//2)),min(width,height)//2)
            if click[0]==1:
                self.choose(pos)
        else:
            pygame.draw.circle(self.screen,inactive_color,(x+(width//2),y+(height//2)),min(width,height)//2)

    def display(self):
        #draw game boundary and map
        pygame.draw.rect(self.screen,(0,0,0),(50,50,700,700),1)
        self.screen.blit(self.map_img,(50,50))

        #draw nodes
        for k,v in POSITION.items():
            if k in self.thief_visited:
                color = RED
            elif k in self.police_visited:
                color = GREEN
            else:
                color = BLACK
            if k ==self.thief:
                self.Node(v[0],v[1],NODE_WIDTH,NODE_HEIGHT,WHITE,WHITE,k)
                self.screen.blit(self.thief_icon,v)
            elif k in self.police:
                self.Node(v[0],v[1],NODE_WIDTH,NODE_HEIGHT,WHITE,WHITE,k)
                self.screen.blit(self.police_icon,v)
            elif k in self.goals:
                self.Node(v[0],v[1],NODE_WIDTH,NODE_HEIGHT,WHITE,WHITE,k)
                self.screen.blit(self.exit_icon,v)
            else:
                self.Node(v[0],v[1],NODE_WIDTH,NODE_HEIGHT,color,BLUE,k)
    
    def choose(self,p):
        if p in self.graph[self.thief] and self.move==0:
            self.thief_visited.add(p)
            self.next_thief = p
            self.move=1
    
    def reset_move(self):
        self.move=0
    
    def check_move(self):
        if self.move==1:
            return True, self.next_thief
        return False, self.thief

    def thief_move(self):
        self.thief = self.next_thief

    def police_move(self,pos):
        for i in range(len(pos)):
            edge = [pos[i],self.police[i]]
            self.police_visited.add(pos[i])
            edge.sort()
            edge = tuple(edge)
            if self.edges.get(edge)!=None and self.edges[edge]!= RED:
                self.edges[edge] = GREEN
        self.police = pos

    #check who win
    def checkWin(self):
        if self.thief in self.police:
            return 2
        elif self.thief in self.goals:
            return 1
        return 0

    def display_lose(self):
        #draw game boundary and map
        pygame.draw.rect(self.screen,(0,0,0),(50,50,700,700),1)
        self.screen.blit(self.map_img,(50,50))

        #draw nodes
        for k,v in POSITION.items():
            if k in self.thief_visited:
                color = RED
            elif k in self.police_visited:
                color = GREEN
            else:
                color = BLACK
            if k ==self.thief:
                self.Node(v[0],v[1],NODE_WIDTH,NODE_HEIGHT,WHITE,WHITE,k)
                self.screen.blit(self.jail_icon,v)
            elif k in self.police:
                self.Node(v[0],v[1],NODE_WIDTH,NODE_HEIGHT,WHITE,WHITE,k)
                self.screen.blit(self.police_icon,v)
            elif k in self.goals:
                self.Node(v[0],v[1],NODE_WIDTH,NODE_HEIGHT,WHITE,WHITE,k)
                self.screen.blit(self.exit_icon,v)
            else:
                self.Node(v[0],v[1],NODE_WIDTH,NODE_HEIGHT,color,BLUE,k)
    