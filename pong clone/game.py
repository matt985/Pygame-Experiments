import pygame
from pygame.locals import *
import random

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

BAR_WIDTH = 128
BAR_HEIGHT = 16
COMPUTERSPEED = 5

SPEED = 2


class Bar:
    
    def __init__(self, screen, x_coord, y_coord, width, height):
        self.screen = screen
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.x_change = 0
        self.x_computer_change = 4
        self.boxsurf = pygame.Surface((width, height))
        self.boxsurf.fill(BLACK)
        self.boxrect = self.boxsurf.get_rect()
        self.boxrect.center = (self.x_coord, self.y_coord)


    def draw_bar(self):
        self.screen.blit(self.boxsurf, self.boxrect)


class Ball:                   ## uso un quadrato e non il cerchio
    
    def __init__(self, screen, color, x_coord, y_coord, width, height):
        self.screen = screen
        self.color =  color
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.width = width
        self.height = height
        self.ball_speed_x = 0
        self.ball_speed_y = 0
        self.ballsurf = pygame.Surface((width, height))
        self.ballsurf.fill(RED)
        self.ballrect = self.ballsurf.get_rect()
        self.ballrect.center = (self.x_coord, self.y_coord)

    def draw_ball(self):
        self.screen.blit(self.ballsurf, self.ballrect)


class Game:

    def __init__(self, screen):
        self.screen = screen
        self.done = False
        self.newMatch = True

    def game_over(self, winner):

        font = pygame.font.Font("freesansbold.ttf", 64)
        if winner == 1:
            text = font.render("GAME OVER", True, RED)
            self.screen.blit(text, (220, 260))
        elif winner == 2:
            text = font.render("YOU WIN", True, RED)
            self.screen.blit(text, (220, 260))

    def run(self):
        self.playerbar = Bar(self.screen, DISPLAY_WIDTH / 2, 550, BAR_WIDTH, BAR_HEIGHT)
        self.computerbar = Bar(self.screen, DISPLAY_WIDTH / 2, 50, BAR_WIDTH, BAR_HEIGHT)       
        self.ball = Ball(self.screen, RED, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2, 20, 20)
        self.handle_events()

    def handle_events(self):

        while not self.done:
            
            self.screen.fill(WHITE)
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.done = True

                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        self.playerbar.x_change = -5
                    elif event.key == K_RIGHT:
                        self.playerbar.x_change = 5
                if event.type == KEYUP:
                    if event.key == K_LEFT or event.key == K_RIGHT:
                        self.playerbar.x_change = 0


            # movimento giocatore (e controllo bordi)
            self.playerbar.boxrect.left += self.playerbar.x_change            
            if self.playerbar.boxrect.left <= 0 or self.playerbar.boxrect.right >= DISPLAY_WIDTH:
                self.playerbar.x_change = 0

            # movimento computer (e controllo bordi)
            self.computerbar.boxrect.left -= self.computerbar.x_computer_change
            if self.computerbar.boxrect.left <= 0 or self.computerbar.boxrect.right >= DISPLAY_WIDTH:
                self.computerbar.x_computer_change *= -1

            # movimento pallina
            if self.newMatch:
                self.ball.ball_speed_x = random.choice([-SPEED, SPEED])
                self.ball.ball_speed_y = random.choice([-SPEED, SPEED])
                self.ball.ballrect.centerx += self.ball.ball_speed_x
                self.ball.ballrect.centery += self.ball.ball_speed_y
                self.newMatch = False
            else:
                self.ball.ballrect.centerx += self.ball.ball_speed_x
                self.ball.ballrect.centery += self.ball.ball_speed_y

            ## colpita barra giocatore
            if self.ball.ballrect.colliderect(self.playerbar.boxrect):
                print("colpita barra giocatore")
                if self.ball.ballrect.right < self.playerbar.boxrect.centerx:
                    print("colpito metà sinistra barra giocatore")
                    if self.ball.ball_speed_x > 0 and self.ball.ball_speed_y > 0:
                        self.ball.ball_speed_y *= 1
                        self.ball.ball_speed_y *= -1

                    elif self.ball.ball_speed_x < 0 and self.ball.ball_speed_y > 0:
                        self.ball.ball_speed_x *= -1
                        self.ball.ball_speed_y *= -1
                
                elif self.ball.ballrect.left >= self.playerbar.boxrect.centerx:
                    print("colpito metà destra barra giocatore")
                    if self.ball.ball_speed_x > 0 and self.ball.ball_speed_y > 0:
                        self.ball.ball_speed_x * 1
                        self.ball.ball_speed_y *= -1

                    elif self.ball.ball_speed_x < 0 and self.ball.ball_speed_y > 0:
                        self.ball.ball_speed_x *= -1
                        self.ball.ball_speed_y *= -1
            
            ## colpita barra computer
            elif self.ball.ballrect.colliderect(self.computerbar.boxrect):
                print("colpite barra computer")
                if self.ball.ballrect.right < self.computerbar.boxrect.centerx:
                    print("colpito metà sinistra barra computer")
                    if self.ball.ball_speed_x > 0 and self.ball.ball_speed_y < 0:
                        self.ball.ball_speed_x *= 1
                        self.ball.ball_speed_y *= -1

                    elif self.ball.ball_speed_x < 0 and self.ball.ball_speed_y < 0:
                        self.ball.ball_speed_x *= 1
                        self.ball.ball_speed_y *= -1

                elif self.ball.ballrect.left >= self.computerbar.boxrect.centerx:
                    print("colpito metà destra barra computer")
                    if self.ball.ball_speed_x > 0 and self.ball.ball_speed_y < 0:
                        self.ball.ball_speed_x *= 1
                        self.ball.ball_speed_y *= -1

                    elif self.ball.ball_speed_x < 0 and self.ball.ball_speed_y < 0:
                        self.ball.ball_speed_x *= 1
                        self.ball.ball_speed_y *= -1

            ## colpita parete sinistra
            elif self.ball.ballrect.left <= 0:
                print("colpita parete sinistra")
                if self.ball.ballrect.top < DISPLAY_HEIGHT / 2:
                    print("colpita metà superiore parete sinistra")
                    if self.ball.ball_speed_x < 0 and self.ball.ball_speed_y < 0:
                        self.ball.ball_speed_x *= -1
                        self.ball.ball_speed_y *= 1

                    elif self.ball.ball_speed_x < 0 and self.ball.ball_speed_y > 0:
                        self.ball.ball_speed_x *= -1
                        self.ball.ball_speed_y *= 1

                elif self.ball.ballrect.bottom >= DISPLAY_HEIGHT / 2:
                    print("colpita metà inferiore parete sinistra")
                    if self.ball.ball_speed_x < 0 and self.ball.ball_speed_y < 0:
                        self.ball.ball_speed_x *= -1
                        self.ball.ball_speed_y *= 1

                    elif self.ball.ball_speed_x < 0 and self.ball.ball_speed_y > 0:
                        self.ball.ball_speed_x *= -1
                        self.ball.ball_speed_y *= 1

            ## colpita parete destra
            elif self.ball.ballrect.right >= DISPLAY_WIDTH:
                print("colpita parete destra")
                if self.ball.ballrect.top < DISPLAY_HEIGHT / 2:
                    print("colpita metà superiore parete sinistra")
                    if self.ball.ball_speed_x > 0 and self.ball.ball_speed_y < 0:
                        self.ball.ball_speed_x *= -1
                        self.ball.ball_speed_y *= 1

                    elif self.ball.ball_speed_x > 0 and self.ball.ball_speed_y > 0:
                        self.ball.ball_speed_x *= -1
                        self.ball.ball_speed_y *= 1

                elif self.ball.ballrect.bottom >= DISPLAY_HEIGHT / 2:
                    print("colpita metà inferiore parete destra")
                    if self.ball.ball_speed_x > 0 and self.ball.ball_speed_y < 0:
                        self.ball.ball_speed_x *= -1
                        self.ball.ball_speed_y *= 1

                    elif self.ball.ball_speed_x > 0 and self.ball.ball_speed_y > 0:
                        self.ball.ball_speed_x *= -1
                        self.ball.ball_speed_y *= 1

            ## controllo vittorie
            elif self.ball.ballrect.bottom >= DISPLAY_HEIGHT:
                self.screen.fill(WHITE)
                self.game_over(1)

            elif self.ball.ballrect.top <= 0:
                self.screen.fill(WHITE)
                self.game_over(2)



            ## disegno oggetti
            self.playerbar.draw_bar()
            self.computerbar.draw_bar()
            self.ball.draw_ball()

            ## aggiornamento display
            pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption("A pong clone")
    Game(screen).run()
    pygame.quit()