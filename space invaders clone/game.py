import pygame
import random
from pygame.locals import *
from pygame import mixer
from math import sqrt, pow

# costanti di gioco
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

PLAYERX = 380
PLAYERY = 480

ALIENSIZE = 64
SHIPSIZE = 64
BULLETSIZE = 32

READY = "ready"
FIRED = "fired"

class Alien:

    def __init__(self, screen):
        """Costruttore degli alieni"""
        self.screen = screen
        self.alienX = random.randint(0, DISPLAY_WIDTH - ALIENSIZE)
        self.alienY = random.randint(50, 200)
        self.alienXchange = 3
        self.alienYchange = 40
        self.alienImg = pygame.image.load("alien.png")

    def draw_alien(self):
        """Disegna alieno"""
        self.screen.blit(self.alienImg, (self.alienX, self.alienY))


class Player:

    def __init__(self, screen, x, y):
        """Costruttore del giocatore"""
        self.screen = screen
        self.shipX = x
        self.shipY = y
        self.shipXchange = 0        
        self.shipImg = pygame.image.load("spaceship.png")

    def draw_player(self):
        """Disegna il giocatore"""
        self.screen.blit(self.shipImg, (self.shipX, self.shipY))


class Bullet:

    def __init__(self, screen, x, y):
        """Costruttore del proiettile"""
        self.screen = screen
        self.bulletX = x
        self.bulletY = y                      # deve essere sullo stesso y di ship
        self.bulletYchange = 15
        self.bulletState = READY
        self.bulletImg = pygame.image.load("bullet.png")

    def fire_bullet(self):
        """Disegna il proiettile e ne aggiorna lo status"""
        self.screen.blit(self.bulletImg, (self.bulletX + 16, self.bulletY + 10))
        self.bulletState = FIRED


class Game:

    def __init__(self, screen):
        """Costruttore del gioco"""
        self.done = False
        self.screen = screen
        self.game_score = 0
        self.background = pygame.image.load("background.jpeg")

    def display_background(self):
        """Copia l'immagine di background sulla schermata
        Nota che questa operazione deve essere effettuata PRIMA di disegnare gli
        oggetti di gioco, possibilmente ad inizio Game Loop"""
        self.screen.blit(self.background, (0, 0))

    def display_score(self):
        """Renderizza e poi visualizza il punteggio"""
        font = pygame.font.Font("freesansbold.ttf", 32)
        score = font.render("Score: " + str(self.game_score), True, (255, 255, 255))
        textX = 10
        textY = 10
        self.screen.blit(score, (textX, textY))

    def collision_occurred(self, alienx, alieny, bulletx, bullety):
        """Controlla se è avvenuta una collisione usando la formula matematica per la
        distanza tra due punti identificati da due coordinate:
        D = sqrt((x2 - x1)^2 + (y2 - y1)^2)"""
        distance = sqrt((pow(alienx - bulletx, 2)) + (pow(alieny - bullety, 2)))
        if distance < 27:
            return True
        else:
            return False

    def laser_sound(self):
        laser = mixer.Sound("laser.wav")
        laser.play()

    def explosion_sound(self):
        explosion = mixer.Sound("explosion.wav")
        explosion.play()

    def game_over(self):
        font = pygame.font.Font("freesansbold.ttf", 64)
        text = font.render("GAME OVER", True, (255, 0, 0))
        self.screen.blit(text, (200, 250))

    def run(self):
        """Genera tutti gli elementi istanziandoli e avvia il game loop"""
        self.player = Player(self.screen, PLAYERX, PLAYERY)
        self.bullet = Bullet(self.screen, self.player.shipX, PLAYERY)

        # Genera i nemici necessari e aggiunge ogni istanza alla lista apposita
        self.number_of_enemies = 10
        self.enemies_list = []
        for i in range(self.number_of_enemies):
            self.enemies_list.append(Alien(self.screen))

        self.handle_events()

    def handle_events(self):
        """Gestisce il Game Loop e gli eventi di gioco"""
        while not self.done:
            
            ## RIPRISTINO DISPLAY VUOTO (qui con BACKGROUND)
            self.display_background()

            ## EVENT LOOP
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.done = True

                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        self.player.shipXchange = -5
                    if event.key == K_RIGHT:
                        self.player.shipXchange = 5

                    if event.key == K_SPACE:
                        if self.bullet.bulletState is READY:
                            self.bullet.bulletX = self.player.shipX
                            self.bullet.fire_bullet()
                            self.laser_sound()

                elif event.type == KEYUP:
                    if event.key == K_LEFT or event.key == K_RIGHT:
                        self.player.shipXchange = 0

            self.player.shipX += self.player.shipXchange

            
            ## CONTROLLO MOVIMENTO ASTRONAVE ENTRO BORDI SCHERMATA
            if self.player.shipX <= 0:
                self.player.shipX = 0
            elif self.player.shipX >= DISPLAY_WIDTH - SHIPSIZE:
                self.player.shipX = DISPLAY_WIDTH - SHIPSIZE

            ## CONTROLLO MOVIMENTO PROIETTILE
            if self.bullet.bulletY <= 0:
                self.bullet.bulletY = PLAYERY
                self.bullet.bulletX = self.player.shipX
                self.bullet.bulletState = READY
            if self.bullet.bulletState is FIRED:
                self.bullet.fire_bullet()
                self.bullet.bulletY -= self.bullet.bulletYchange

            ## MOVIMENTO NEMICI
            # Nota che ogni nemico è un elemento iesimo della lista di nemici
            # ogni singola istanza di alieno si chiama self.enemies_list[i]
            # ed ha attributi alienX, alienY, alienXchange

            for i in range(self.number_of_enemies):

                # controllo game over
                if self.enemies_list[i].alienY > 440:
                    for j in range(self.number_of_enemies):
                        self.enemies_list[j].alienY = 2000
                    self.game_over()
                    break

                self.enemies_list[i].alienX += self.enemies_list[i].alienXchange        
                if self.enemies_list[i].alienX <= 0:
                    self.enemies_list[i].alienXchange *= -1
                    self.enemies_list[i].alienY += self.enemies_list[i].alienYchange
                elif self.enemies_list[i].alienX >= DISPLAY_WIDTH - ALIENSIZE:
                    self.enemies_list[i].alienXchange *= -1
                    self.enemies_list[i].alienY += self.enemies_list[i].alienYchange

                ## CONTROLLO COLLISIONI
                collision = self.collision_occurred(self.enemies_list[i].alienX, self.enemies_list[i].alienY, self.bullet.bulletX, self.bullet.bulletY)
                if collision:
                    self.explosion_sound()
                    self.bullet.bulletY = PLAYERY
                    self.bullet.bulletState = READY
                    self.game_score += 1

                    ## RESPAWNA L'ALIENO COLPITO
                    self.enemies_list[i].alienX = random.randint(0, DISPLAY_WIDTH - ALIENSIZE)
                    self.enemies_list[i].alienY = random.randint(50, 200)


            ## DISEGNI VARI
            # disegna il giocatore
            self.player.draw_player()
            self.display_score()

            # disegna tutte le istanze di alieno contenute nella lista
            for i in range(self.number_of_enemies):
                self.enemies_list[i].draw_alien()

            ## AGGIORNAMENTO DISPLAY
            pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption("Space Invaders Clone")
    Game(screen).run()
