import pygame
import json
import time

from sys import exit
from random import randint
from runner import Runner

runner = Runner()

pygame.init()

texte = ""

screen = pygame.display.set_mode((800, 400))

x = 800
y = 400

pygame.display.set_caption("test de connexion")
rect_choix1 = pygame.Rect(200, 100, 100, 100)
rect_choix2 = pygame.Rect(600, 100, 100, 100)
rect_jouer = pygame.Rect(400, 150, 100, 100)
rect_retour = pygame.Rect(10, 10, 75, 50)
rect_player = pygame.Rect(400, 200, 200, 50)

text1 = pygame.font.SysFont('arial', 15, True)
text2 = pygame.font.SysFont('arial', 20, True)

text_connexion = text1.render("Connexion", True, (34, 34, 34))
text_connexion_rect = text_connexion.get_rect(center = (250, 150))

text_creation = text1.render("Crée", True, (34, 34, 34))
text_creation_rect = text_connexion.get_rect(center = (670, 140))

text_creation1 = text1.render("compte", True, (34, 34, 34))
text_creation1_rect = text_connexion.get_rect(center = (660, 160))

texte_suface = text1.render(texte, True, 'black')
rect_texte = texte_suface.get_rect(center = (100, 100))

text_pseudo = text1.render("Entrez votre pseudo", True, (34, 34, 34))
text_pseudo_rect = text_pseudo.get_rect(center = (400, 150))

text_retour = text1.render("Retour", True, (34, 34, 34))
text_retour_rect = texte_suface.get_rect(center = (25, 35))

text_exit = text1.render("Exit", True, (34, 34, 34))
text_exit_rect = text_exit.get_rect(center = (45, 35))

text_erreur = text2.render("Pseudo incorect", True, (255, 0, 0))
text_erreur_rect = text_erreur.get_rect(center = (95, 35))

text_existant = text2.render("Pseudo déjà existant", True, (255, 0, 0))
text_exisant_rect = text_existant.get_rect(center = (95, 35))

text_fin = text2.render("Merci d'avoir tester ce jeu j'attend vos retour", True, (255, 0, 0))
text_fin_rect = text_existant.get_rect(center = (95, 35))

top_score = 1
list_mot = []
connecte = False
menu = True
connexion1 = False
connexion2 = False
run = True
while run:

    x, y = pygame.display.get_window_size()
    pygame.display.set_caption("test de connexion")

    rect_choix1.center = x / 4, y / 2
    rect_choix2.center = x * .75, y / 2
    rect_jouer.center = x / 2, y / 2
    rect_player.center = x / 2, y / 2 + 50
    rect_texte.center = x / 2 - 95, y / 2 + 50

    text_connexion_rect.center = x / 4, y / 2
    text_creation_rect.center = x * .75, y / 2 - 5
    text_creation1_rect.center = x * .75, y / 2 + 5
    text_pseudo_rect.center = x / 2, y / 2
    text_erreur_rect.center = x / 2 - 6, y / 2 + 80
    text_exisant_rect.center = x / 2 - 29, y / 2 + 80
    text_fin_rect.center = 280, y / 2

    texte_suface = text1.render(texte, True, 'black')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if menu:

            screen.fill((94, 129, 162))
            screen.blit(text_connexion, text_connexion_rect)
            screen.blit(text_creation, text_creation_rect)
            screen.blit(text_creation1, text_creation1_rect)
            screen.blit(text_exit, text_exit_rect)

            pygame.draw.rect(screen, 'black', rect_choix1, 3)
            pygame.draw.rect(screen, 'black', rect_choix2, 3)
            pygame.draw.rect(screen, 'black', rect_retour, 3)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_retour.collidepoint(event.pos):
                    run = False
                elif rect_choix1.collidepoint(event.pos):
                    connexion1 = True
                    menu = False
                elif rect_choix2.collidepoint(event.pos):
                    connexion2 = True
                    menu = False


        if connexion1 or connexion2:
            screen.fill((94, 129, 162))
            screen.blit(text_retour, text_retour_rect)
            screen.blit(texte_suface, (rect_texte))

            pygame.draw.rect(screen, 'black', rect_retour, 3)


            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_retour.collidepoint(event.pos):
                    connexion2 = False
                    connexion1 = False
                    menu = True
                    texte = ""
            number = len(texte)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    texte = texte[:-1]
                elif event.key == pygame.K_RETURN:
                    pass
                elif event.key == pygame.K_TAB:
                    texte += " " * 3
                else:
                    if number < 17:
                        texte += event.unicode



        if connexion1:
            screen.blit(text_pseudo, text_pseudo_rect)
            pygame.draw.rect(screen, 'black', rect_player, 3)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    with open('joueur.json', 'r') as file:
                        data = json.load(file)

                        try:
                            top_score = data[texte]
                            pseudo = texte
                            connecte = True
                            connexion1 = False
                        except:
                            screen.blit(text_erreur, text_erreur_rect)
                            pygame.display.flip()
                            time.sleep(.5)


        if connexion2:
            screen.blit(text_pseudo, text_pseudo_rect)
            pygame.draw.rect(screen, 'black', rect_player, 3)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    with open('joueur.json', 'r+') as file:
                        data = json.load(file)

                        if texte in data:
                            screen.blit(text_existant, text_exisant_rect)
                            pygame.display.flip()
                            time.sleep(.5)
                        else:
                            # met le curseur en pos 0
                            file.seek(0)

                            # supprimé ce qu'il y a apres
                            file.truncate()

                            top_score = data[texte] = 0

                            json.dump(data, file)

                            pseudo = texte
                            connecte = True
                            connexion2 = False

        if connecte:
            with open('joueur.json', 'r+') as file:
                data = json.load(file)

                connecte = runner.run(pseudo, top_score)


                data[pseudo] = top_score
                if connecte == False:
                    screen.fill('black')
                    screen.blit(text_fin, text_fin_rect)
                    #print(runner.end())

        pygame.display.flip()