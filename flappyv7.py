#flappyv6.py
#Haillon Seant code 
# Example file showing a basic pygame "game loop"
import pygame 
from random import randint
pygame.init()
#(0,0)------------> x  
#    |
#    | 
#    |
#    |
#    |
#    v z
#V3->V4 changement prise d'info tick, la même pour flappy et les block
police=pygame.font.SysFont("Arial",40)
screen = pygame.display.set_mode((1280, 720))#Pas adaptable pour le moment
clock = pygame.time.Clock()

running = True
grav=390
puissance=-440

class Flappy:

    def __init__(self,x,z,grav):
        self.x=x
        self.z=z
        
        self.vitz=grav
        
        self.image=pygame.image.load("images/tuyaux.png")
        
        #caracteristique du saut
        self.sautbool=False
        self.t_saut=0
        self.duree_saut=0.2#en seconde
        
        self.cote=20
        
    
    def saut(self,puissance):
        self.t_saut=pygame.time.get_ticks()
        self.vitz=puissance  
        self.sautbool=True 
    
    def mouvement(self,time,t_actuel):
        # t_actuel=pygame.time.get_ticks()
        t=(t_actuel-time)/1000#divise par 1000 pour avoir le temps en seconde entre deux appels de flappy.mouvement()
        if self.sautbool:
            if (t_actuel-self.t_saut)/1000 <= self.duree_saut:#pas propre
                self.z+=self.vitz*t
            else :  
                self.vitz=grav
                self.z+=self.vitz*((t_actuel-self.t_saut)/1000-self.duree_saut)
                self.sautbool=False
        else :
            self.z+=self.vitz*t
            
#amodifier
class Block:
    def __init__(self,top,left,largueur,longueur):
        self.top=top
        self.left=left
        
        self.largeur=largueur#taille en x
        self.longueur=longueur#taille en z
        
class Porte:
    def __init__(self,left,vitx=-120):
        self.blocks=[]
        self.left=left
        self.vitx=vitx
        self.score=False

    def init_alea_block(self,taille):
        mini=20#hauteur minimal
        maxi=700
        longueur=randint(mini,maxi-taille)
        self.blocks.append(Block(0,self.left,80,longueur))#le tuyau du haut 
        self.blocks.append(Block(longueur+taille,self.left,80,720-longueur+taille))          
    
    def alea_block(self,taille):
        self.left=1320
        mini=20#hauteur minimal
        maxi=700
        longueur=randint(mini,maxi-taille)
        self.blocks[0].longueur=longueur
        self.blocks[0].left=self.left
        self.blocks[1].left=self.left
        self.blocks[1].top=longueur+taille
        self.blocks[1].longueur=720-longueur+taille

    def mouvement(self,t_actuel):
        t=(t_actuel-time)/1000
        dist=self.vitx*t 
        self.left+=dist
        for block in self.blocks:
              block.left+=dist
    
    # def va_et_vient(self):

    

def collision(flappy,block):
    if flappy.x+flappy.cote < block.left:
        return False
    
    elif flappy.z+flappy.cote < block.top:
        return False
    
    elif flappy.x-flappy.cote > block.left+block.largeur:
        return False
    
    elif flappy.z-flappy.cote > block.top+block.longueur :
        return False

    return True
def collision_li(li_porte):
    for porte in li_porte:
        for block in porte.blocks:
            if collision(flappy,block):
                return True
    #si flappy touche le haut ou le bas de l'ecran (seulement sont bord bas)
    if flappy.z+flappy.cote <0:
        return True
    if flappy.z-flappy.cote > 720:
        return True
    return False
def draw_block(li_porte):
    for porte in li_porte:
        for block in porte.blocks:
            pygame.draw.rect(screen,(38,144,9),(block.left,block.top,block.largeur,block.longueur))

x=320
z=350
flappy=Flappy(x,z,grav)
start=False
perdue= False
score=0

boost=0
boost_bool=False
boost_vit=40

score_surface=police.render('0',False,"black")
dist_parcourue=0
largueur_porte=280

li_porte=[Porte(700),Porte(1050),Porte(1400),Porte(1750)]
li_porte_buff=li_porte[:]

for porte in li_porte:
    porte.init_alea_block(largueur_porte)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                flappy.saut(puissance)
                if not start:
                    start=True
                    time=pygame.time.get_ticks()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button==1 or event.button==3: #click gauche / click droit
                flappy.saut(puissance)
                if not start:
                    start=True
                    time=pygame.time.get_ticks()
   
    #on regarde si on a pas perdue la partie
    if perdue :
        flappy.x,flappy.z=x,z
        flappy.vitz=puissance
        start=False
        perdue=False
    
    if not perdue:
        screen.fill("white")
        if start:
            t_actuel=pygame.time.get_ticks()
            flappy.mouvement(time,t_actuel)
            
            boost_bool=score//5>boost
            
            if boost_bool:
                boost+=1
            for porte in li_porte:
                
                if boost_bool:
                    boost_vit=boost_vit#vitesse general passer en variable golbal
                    porte.vitx-=boost_vit
                
                porte.mouvement(t_actuel)
                
                if porte.left<=-80: #sortie de l'ecran, depend de la largeur d'une porte
                    porte.left=1320
                    porte.alea_block(largueur_porte)
                    porte.score=False

                elif porte.left<=280 and not porte.score: #x-largeur/2
                    score+=1
                    porte.score=True

        time=pygame.time.get_ticks()
       
        #on dessine les tuyaux
        draw_block(li_porte)        
        
        screen.blit(police.render(str(score),False,"black"),(1200,670))
        #on dessine le carre qui represente flappy notre ami l'oiseau
        pygame.draw.rect(screen,(125,100,0),(flappy.x-(flappy.cote),flappy.z-(flappy.cote),flappy.cote*2,flappy.cote*2))

        
        #on regarde si on a une collision
        perdue=collision_li(li_porte)
        pygame.draw.line(screen,'Blue',(320,0),(320,720))
        # on rafraichi l'ecran
        pygame.display.flip()
    clock.tick(250)  # limits FPS
pygame.quit()


#passer vitx en variable global
#bug apres 20 score