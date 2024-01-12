import pygame
import time
import random
from enum import Enum

PERIOD = 1/30

class TANK1_CMDS(Enum):
    UP = pygame.K_UP
    DOWN = pygame.K_DOWN
    RIGHT = pygame.K_RIGHT
    LEFT = pygame.K_LEFT

class TANK2_CMDS(Enum):
    UP = pygame.K_UP
    DOWN = pygame.K_DOWN
    RIGHT = pygame.K_RIGHT
    LEFT = pygame.K_LEFT

class Game():

    def __init__(self):

        self.screen = ...
        self.running = False

    def start(self):
        self.running = True

    def step_frame():
        temps_actuel = time.time()
        random_x = random.randint(0, 1380)
        random_y = random.randint(0, 720)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if fleche.cliquer(fleche):
            mode = 0

        tank1.move_tank(bool(1)) 
        if temps_actuel - temps_dernier_tir >= 3:
            if tank1.tirer(bool(1)):
                temps_dernier_tir = temps_actuel

        tank2.move_tank(bool(0))
        if temps_actuel - temps_dernier_tir2 >= 3:
            if tank2.tirer(bool(0)):
                temps_dernier_tir2 = temps_actuel

        #on rajoute l'objet invincibilité1 qui apparait toute les 10 secondes
        if temps_actuel - temps_derniere_apparition >= 10:
            Objet.objet_apparition()
        
        tank1.prend_objet(bool(1))
        tank1.perd_objet(bool(1))

        tank2.prend_objet(bool(0))
        tank1.perd_objet(bool(0))

        #si les bullets touche un mur, on les fait "rebondir" en inversant leurs direction
        Objet.mur_inverse_direction()

        #si les bullets touche un tank
        tank1.touche_tank(bool(1))
        tank2.touche_tank(bool(0))
        
        #On met à jour les objets bullet
        updated_bullets = []
        for bullet in bullets:
            bullet.move()
            updated_bullets.append(bullet)

        #bullets = updated_bullets

        #effacer l'écran
        screen.fill((255, 255, 255))


        screen.blit(background_image, (0, 0))
        # Dessiner les score (on dessine les scores en premier pour qu'ils ne cachent pas les autres objets)
        score_tank1 = scores[tank1.score]
        score_tank2 = scores2[tank2.score]
        screen.blit(score_tank2.image, (500, 50))
        screen.blit(score_tank1.image, (700, 50))

        #Dessiner le tank1
        screen.blit(tank1.image, tank1.rect)
        screen.blit(canon1.image, canon1.rect)

        # dessiner le tank2
        screen.blit(tank2.image, tank2.rect)
        screen.blit(canon2.image, canon2.rect)

        # Dessiné les objets bullets
        for bullet in bullets:
            screen.blit(bullet.image, bullet.rect)

        #Dessiner les objet de vitesse
        if objet_invincible_tank:
            screen.blit(objet_invincible_tank.image, objet_invincible_tank.rect)
        
        #Si on dépasse 5 points, l'écran de vicctoire s'affiche (on le met à la fin pour qu'il soit par dessus le 
        if tank1.score == 5 :
            Finjeu.fin_partie(bool(1)) 
        if tank1.score == 5:
            Finjeu.fin_partie(bool(0)) 

        screen.blit(fleche.image, fleche.rect)

        # Rafraîchir l'écran
        pygame.display.update()
    

    def run(self):

        while self.running:

            current_time = time.time()

            self.step_frame()

            while time.time() - current_time < PERIOD:
                time.sleep(0.001)

class Tank():
    def __init__(self, image, x, y, vitesse, tank_number):
        self.original_image = pygame.image.load(image) #pour definir l'image des tank 
        self.image =self.original_image #On créer une différence entre l'image de base et l'image actuelle
        self.rect = self.image.get_rect() 
        self.rect.center= (x, y) #position du tank
        self.vitesse = vitesse
        self.angle = 0 #angle de base
        self.score = 0
        self.invincible = 0
        self.direction = (0,0)

        self.tank_number = tank_number
        if tank_number == 1:
            self.commands = TANK1_CMDS
        elif tank_number == 2:
            self.commands = TANK2_CMDS

    def rotate(self, angle):
        #pour changer l'angle du tank
        self.image=pygame.transform.rotate(self.original_image,angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def prend_objet(self, bool):
        global objet_invincible_tank
        global temps_fin_invincible
        if bool:
            tank = tank1
        else:
            tank = tank2
        if objet_invincible_tank and tank1.rect.colliderect(objet_invincible_tank.rect):
            tank.change_vitesse(2)
            temps_fin_invincible = temps_actuel + CONSTANTE 
            tank.invincible = 1
            objet_invincible_tank = None
    
    def perd_objet(self, bool):
        if bool:
            tank = tank1
        else:
            tank = tank2
        if temps_fin_invincible != 0 and temps_fin_invincible <= temps_actuel:
            tank.invincible = 0
            tank.change_vitesse(5) 


    def move_tank(self, bool):
        #les déplacements en fonction des positions
        if bool:
             canon, tank = canon1, tank1
             kx, ky = tank1.rect.centerx, tank1.rect.centery
        else:
             canon, tank = canon2, tank2
             kx, ky = tank2.rect.centerx, tank2.rect.centery


        dx, dy = 0, 0
        if pygame.key.get_pressed()[tank.commands.LEFT] and not tank.rect.colliderect(mur1.rect):
            #on fait en sorte que le tank soit bloqué par les murs en l'empéchant d'avancer en cas de colision
            dx = -1 #augemente le x ou le y selon le déplacement
            canon.change_position(kx-50, ky)
            canon.rotate(90)
            tank.direction = (-1, 0)
        if pygame.key.get_pressed()[tank.commands.RIGHT] and not tank.rect.colliderect(mur2.rect):
            dx = 1
            canon.change_position(kx+50, ky)
            canon.rotate(-90)
            tank.direction = (1, 0)
        if pygame.key.get_pressed()[tank.commands.UP] and not tank.rect.colliderect(mur3.rect):
            dy = -1
            canon.change_position(kx, ky-50)
            canon.rotate(0)
            tank.direction = (0, -1)
        if pygame.key.get_pressed()[tank.commands.DOWN] and not tank.rect.colliderect(mur4.rect):
            dy = 1
            canon.change_position(kx, ky+50)
            canon.rotate(180)
            tank.direction = (0, 1)
        tank.change_position(self.rect.centerx + dx*self.vitesse, self.rect.centery + dy*self.vitesse)
        canon.change_position()

    def tirer(self, bool):
        if bool:
            tank,touche_tirer = tank1,pygame.K_SPACE
        else:
            tank,touche_tirer= tank2,pygame.K_LSHIFT

        if tank.direction == (0,1):
            x, y = self.rect.centerx, self.rect.centery+70 # haut
        elif tank.direction == (0,-1):
            x, y = self.rect.centerx, self.rect.centery-70 # bas
        elif tank.direction == (1,0):
            x, y = self.rect.centerx+70, self.rect.centery # droite
        elif tank.direction == (-1,0):
            x, y = self.rect.centerx-70, self.rect.centery # gauche
        else:
            x, y = self.rect.centerx, self.rect.centery+70 # haut par defaut
        
        if pygame.key.get_pressed()[touche_tirer]:
            bullet = Tir("bullet.png", x, y,6, tank.direction)
            bullets.append(bullet)
            return True
    
    def change_vitesse(self, vitesse):
        self.vitesse = vitesse
    
    def change_image(self, image):
        self.original_image = pygame.image.load(image)

    def change_position(self, x, y):
        self.rect.center = (x, y)
    
    def touche_tank(self, bool):
        if bool:
            tank, a= tank1, 1
        else :
           tank, a=tank2, 0
        for bullet in bullets:
        #si c'est le tank2 qui touche le tank1, + 1 point et réinitialisation du jeux
            if bullet.rect.colliderect(tank.rect) and tank.invincible == 0:
                tank.score += 1
                Finjeu.reinitialiser_jeu(a) 
                return True
            
    def augmente_point():
        if tank1.score < 9:
            tank1.score += 1
        else:
            tank2.score += 1
            tank1.score = 0


class Tir():
    def __init__(self, image, x, y, speed, direction):
        #pareil que le tank mais avec les directions                    
        self.original_image = pygame.image.load(image)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.direction = direction  # Direction du tir
        self.angle = 0

    def move(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
    
    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def change_vitesse(self, vitesse): 
        self.vitesse = vitesse


class Objet():
    def __init__(self, image, x, y):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def mur_inverse_direction():
        for bullet in bullets:
            if bullet.rect.colliderect(mur1.rect):
                bullet.direction = (1, 0) #inverser la direction
            if bullet.rect.colliderect(mur2.rect):
                bullet.direction = (-1, 0)
            if bullet.rect.colliderect(mur3.rect):
                bullet.direction = (0, 1)
            if bullet.rect.colliderect(mur4.rect):
                bullet.direction = (0, -1)
    def objet_apparition():
        global temps_derniere_apparition
        global objet_invincible_tank
        objet_invincible_tank = Objet("potion.png", random_x, random_y)
        temps_derniere_apparition = temps_actuel

class Finjeu():
    def reinitialiser_jeu(a):
        if a == 1:
            tank = tank1
        else :
            tank = tank2
        temps_affichage_explosion = time.time()

        while time.time() - temps_affichage_explosion < 1.5: #on fait en sorte que l'image d'explosion reste 1.5 secondes avant la réinitialiation
            screen.blit(explosion_image, (tank.rect.centerx-50, tank.rect.centery-50)) #on ajoute unee image d'explosion par dessus le tank
            pygame.display.update()

        #réinitialisation des tanks et bullets
        tank1.rect.center = (100, 600)
        tank2.rect.center = (1250, 100)
        canon1.change_position(100, 550)
        canon2.change_position(100, 550)
        bullets.clear()

    def fin_partie(bool):
        if bool:
            victoire_image, bool, tank= victoire_image1, 0, tank1
        else:
            victoire_image, bool, tank = victoire_image2, 1, tank2
        screen.blit(victoire_image, (0, 0))
        screen.blit(bouton_rejouer,(1100,500)) 
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            tank.score = 0
            Finjeu.reinitialiser_jeu(bool)

class Menu():
    def __init__(self, image, x, y):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def cliquer(self, bouton):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and bouton.rect.collidepoint(event.pos):
                return True
            
    def change_image(self, image):
        self.image = pygame.image.load(image)


def main():
    #on instancie les class

    game = Game() # init
    window_width, window_height = 1370, 720
    fond = Menu("fond_noir.png", window_width//2, window_height//2)
    jouer = Menu("jouer.png", 700, 150)
    option = Menu("cadre.png", 700, 600)
    v1 = Menu("1v1.png", 500, 400)
    solo = Menu("solo.png", 900, 400)
    mode = 0

    # Création des tanks, "tank1" et "tank2" avec la classe Tank
    tank1 = Tank("tank.png", 100, 600, 5, 1)
    tank2 = Tank("tank2.png", 1250, 100, 5, 2) 

    direction = 0
    direction2 = 0

    canon1 = Tank("canon.png", tank1.rect.x, tank1.rect.y, 0, 1)
    canon2 = Tank("canon.png", tank2.rect.x, tank2.rect.y, 0, 2)

    # Création des murs avec la classe Objet 
    mur1 = Objet ("mur.png", 20, 350)
    mur2 = Objet ("mur.png", 1370, 350)
    mur3 = Objet ("mur2.png", 690, 10)
    mur4 = Objet ("mur2.png", 690, 690)

    #Création des scores (classe Score)
    #scores du tank1
    score0 = Objet("score0.png",0,0)
    score1 = Objet("score1.png",0,0)
    score2 = Objet("score2.png",0,0)
    score3 = Objet("score3.png",0,0)
    score4 = Objet("score4.png",0,0)
    score5 = Objet("score5.png",0,0)
    score6 = Objet("6.png",0,0)
    score7 = Objet("7.png",0,0)
    score8 = Objet("8.png",0,0)
    score9 = Objet("9.png",0,0)

    # scores = []
    # nb_scores = 5
    # for k in range(nb_scores):
    #     scores.append(Objet("score"+str(k)+".png",0,0))


    scores = [score0,score1,score2,score3,score4,score5,score6,score7,score8,score9] #On fait une liste pour faciliter le changement des scrores

    points = 0 

    #scores du tank2
    scores2 = [score0,score1,score2,score3,score4,score5,score6,score7,score8,score9]
    scores2 = scores.copy()
    points2 = 0

    # On créer une liste pour stocker les objets bullet et faciliter l'actualisation des objets bullets
    bullets = []

    fleche = Menu("fleche.png", 100, 100)

    #création des images de victoire
    victoire_image1 = pygame.image.load("victoire_tank1.png")
    bouton_rejouer = pygame.image.load("bouton_rejouer.png")
    victoire_image2 = pygame.image.load("victoire_tank2.png")

    background_image = pygame.image.load("background.png")

    #image de l'explosion
    explosion_image = pygame.image.load("explosion.png")

    #Toutes les variables de
    #variable de temps pour gérer le temps entre les tirs et de l'explosion des tanks
    temps_dernier_tir = time.time()
    temps_dernier_tir2 = time.time()

    temps_derniere_apparition = time.time()
    temps_vitesse = time.time()

    temps_fin_invincible = 0
    temps_fin_vitesse2 = 0

    invincibilité1 = 0
    invincibilité2 = 0
        
    objet_invincible_tank = None

    game.run()

    # game exited


# if __name__ == '__main__':
#     main()

main()