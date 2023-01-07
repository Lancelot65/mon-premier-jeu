import pygame
from sys import exit
from random import randint
from sys import exit
import json

class Runner():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 400))
        pygame.display.set_caption("Runner")
        self.start_time = 0

        # écrire sur la fenetre
        self.text = pygame.font.SysFont('arial', 20, True)
        self.text1 = pygame.font.SysFont('arial', 50, True)

        # importer une image ici le fond
        self.fond = pygame.image.load("paysage.png").convert()
        # crée le player
        self.player = pygame.image.load("baton1.png").convert_alpha()
        # placer le joueur precisement
        self.player_move1 = pygame.image.load('baton1.png')
        self.player_move2 = pygame.image.load('baton2.png')
        self.player_jump = pygame.image.load('jump.png')

        self.player_rect = self.player.get_rect(topleft=(170, 230))
        self.player_move = [self.player_move1, self.player_move2]
        self.player_index = 0

        self.ennemi_surf = self.player_move[self.player_index]

        # player gravity
        self.player_gravity = 0

        self.player_image = pygame.image.load("baton1.png").convert_alpha()
        # grossir l'image
        self.player_image = pygame.transform.scale(self.player_image, (81, 186))

        self.player_image_rect = self.player_image.get_rect(center=(400, 150))
        self.text_lose = self.text1.render("Taper espace pour recommencer.", False, (34, 34, 34))
        self.text_lose_rect = self.text_lose.get_rect(center=(400, 300))

        # crée un ennemi
        self.zombie = pygame.image.load('noel.png').convert_alpha()
        self.zombie_rect = self.zombie.get_rect(center=(200, 390))

        # deuxieme ennemi
        self.rocket_1 = pygame.image.load('boom.png').convert_alpha()
        self.rocket_2 = pygame.image.load('boom1.png').convert_alpha()
        self.rocket_3 = pygame.image.load('boom2.png').convert_alpha()
        self.ennemi2_move = [self.rocket_1, self.rocket_2, self.rocket_3]
        self.ennemi2_index = 0

        self.ennemi_surf = self.ennemi2_move[self.ennemi2_index]

        self.obstacle_rect_list = []
        self.acceleration = .005

        self.move = 5

        self.rect_retour = pygame.Rect(10, 10, 75, 50)
        self.text_retour = self.text.render("Quit", True, (34, 34, 34))
        self.text_retour_rect = self.text_retour.get_rect(topleft=(26, 24))



    def display_score(self):
        self.time = (pygame.time.get_ticks() - self.start_time) / 1000
        self.time = int(self.time)
        self.score = self.text.render(f'Score : {self.time}', False, (34, 34, 34))
        self.score_rect = self.score.get_rect(center = (400, 50))
        self.screen.blit(self.score, self.score_rect)

    def obstacle_movement(self, obstacle_list):
        if obstacle_list:
            for obstacle_rect in obstacle_list:
                obstacle_rect.x -= self.move

                if obstacle_rect.y == 265:
                    self.screen.blit(self.zombie, obstacle_rect)
                else:
                    self.ennemi2_annimation()
                    self.screen.blit(self.ennemi_surf, obstacle_rect)

            obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -20]

            return obstacle_list
        else:
            return []

    def collision(self, obstacles):
        if obstacles:
            for obstacle_rect in obstacles:
                if self.player_rect.colliderect(obstacle_rect):
                   return False
        return True

    def ennemi2_annimation(self):

        self.ennemi2_index += 0.1
        if self.ennemi2_index >= len(self.ennemi2_move):
            self.ennemi2_index = 0

        self.ennemi_surf = self.ennemi2_move[int(self.ennemi2_index)]

    def player_annimation(self):

        self.time = (pygame.time.get_ticks() - self.start_time) / 1000
        self.time = int(self.time)

        if self.player_rect.y < 255:
            self.player_surf = self.player_jump
        else:
            self.player_index = self.player_index + .1 + self.acceleration + self.acceleration
            if self.player_index >= len(self.player_move):
                self.player_index = 0

            self.player_surf = self.player_move[int(self.player_index)]
    def run(self, pseudo, max_score):



        pygame.init()
        self.clock = pygame.time.Clock()
        # game active
        self.game_active = True
        #minuterie on regl les milliseconde
        self.start_time = pygame.time.get_ticks()

        self.maxscore = max_score

        self.timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer, 900)
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect_retour.collidepoint(event.pos):
                        self.game_active = False
                        with open('joueur.json', 'r+') as file:
                            data = json.load(file)
                            file.seek(0)

                            # supprimé ce qu'il y a apres
                            file.truncate()

                            data[pseudo] = self.max_score1

                            json.dump(data, file)
                        return False
                if self.game_active:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.player_rect.collidepoint(event.pos) and self.player_rect.y >= 250:
                            self.player_gravity = -15
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and self.player_rect.y >= 250:
                            self.player_gravity = -15

                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.game_active = True
                        self.zombie_rect.x = 700
                        self.player_rect.y = 250
                        self.start_time = pygame.time.get_ticks()
                        self.move = 5
                        self.chrono = 0

                if event.type == self.timer and self.game_active:
                    if randint(0, 2):
                        self.obstacle_rect_list.append(self.zombie.get_rect(topleft = (randint(900, 1100), 265)))
                    else:
                        self.obstacle_rect_list.append(self.rocket_1.get_rect(topleft = (randint(900, 1100), 200)))
            if self.game_active:
                #on "écrit" la surface et on dit ou
                self.screen.blit(self.fond, (0, 0))
                self.screen.blit(self.fond, (400, 0))
                self.display_score()
                self.move += self.acceleration
                self.chrono = (pygame.time.get_ticks() - self.start_time) / 1000

                self.player_gravity += 1
                self.player_rect.y += self.player_gravity
                self.player_annimation()
                if self.player_rect.y >= 250:
                    self.player_rect.y = 250
                self.screen.blit(self.player_surf, self.player_rect)

                #obstacle move
                self.obstacle_rect_list = self.obstacle_movement(self.obstacle_rect_list)

                self.game_active = self.collision(self.obstacle_rect_list)

            else:
                self.screen.fill((94, 129, 162))

                self.chrono = int(self.chrono)
                self.max_score1 = max_score
                if self.max_score1 < self.chrono :
                    self.max_score1 = self.chrono

                self.text_score = self.text.render(f"Ton score est de {self.chrono}.", False, (34, 34, 34))
                self.text_score_rect = self.text_lose.get_rect(topleft=(10, 60))

                self.text_maxscore = self.text.render(f"Ton meilleur score est de {self.max_score1}.", False,(34, 34, 34))
                self.text_maxscore_rect = self.text_lose.get_rect(topleft=(10, 100))

                self.text_pseudo = self.text.render(f"{pseudo}", False, (34, 34, 34))
                self.text_pseudo_rect = self.text_pseudo.get_rect(center=(400, 10))

                self.screen.blit(self.text_score, self.text_score_rect)
                self.screen.blit(self.text_maxscore, self.text_maxscore_rect)
                self.screen.blit(self.text_pseudo, self.text_pseudo_rect)

                self.screen.blit(self.player_image, self.player_image_rect)
                self.obstacle_rect_list.clear()
                self.screen.blit(self.text_lose, self.text_lose_rect)

            self.screen.blit(self.text_retour, self.text_retour_rect)
            pygame.draw.rect(self.screen, 'black', self.rect_retour, 3)
            # on rappele les def de base
            pygame.display.update()


            self.clock.tick(60)