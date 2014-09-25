import pygame
import pygame.display as display
import State
import Play
import HighScore

from Constants import Constants


#This is the state for playing the game
class Menu(State.State):


    #Code to initialize a new game instance
    def __init__(self):
        State.State.__init__(self)
        Constants.SCREEN.fill(pygame.Color("black"))
        self.menu_font = pygame.font.Font(None, 70)
        self.selected = 0

    #Function to draw the sprite groups
    def draw(self):
        play_color = (255, 255, 255)
        adjustv_color = (255, 255, 255)
        adjusta_color = (255, 255, 255)
        high_color = (255, 255, 255)
        quit_color = (255, 255, 255)

        if(self.selected == 0):
            play_color = (255, 255, 0)
        elif self.selected == 1:
            adjustv_color = (255, 255, 0)
        elif self.selected == 2:
            adjusta_color = (255, 255, 0)
        elif self.selected == 3:
            high_color = (255, 255, 0)
        elif self.selected == 4:
            quit_color = (255, 255, 0)

        #Using the title font, render the title Menu Screen
        play = self.menu_font.render("Play", True, play_color)
        adjustV = self.menu_font.render("Adjust Visual Brightness", True,
                                        adjustv_color)
        adjustA = self.menu_font.render("Adjust Audio Volume", True, adjusta_color)
        high_scores = self.menu_font.render("High Scores", True, high_color)
        quit_game = self.menu_font.render("Quit", True, quit_color)

        playwidth, playheight = play.get_size()
        adjust_v_width, adjust_v_height = adjustV.get_size()
        adjust_a_width, adjust_a_height = adjustA.get_size()
        hs_width, hs_height = high_scores.get_size()
        quit_width, quit_height = quit_game.get_size()

        Constants.SCREEN.blit(play, (Constants.WIDTH/2 - playwidth/2 ,
                                      Constants.HEIGHT/2 - playheight/2 + 40))
        Constants.SCREEN.blit(adjustV, (Constants.WIDTH/2 - adjust_v_width/2 ,
                                      Constants.HEIGHT/2 - adjust_v_height/2 +
                                      90))
        Constants.SCREEN.blit(adjustA, (Constants.WIDTH/2 - adjust_a_width/2 ,
                                      Constants.HEIGHT/2 - adjust_a_height/2 +
                                      140))
        Constants.SCREEN.blit(high_scores, (Constants.WIDTH/2 - hs_width/2 ,
                                      Constants.HEIGHT/2 - hs_height/2 + 190))
        Constants.SCREEN.blit(quit_game, (Constants.WIDTH/2 - quit_width/2 ,
                                      Constants.HEIGHT/2 - quit_height/2 + 240))



        display.update()

    #Function for key updates
    def keyEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if(event.key == pygame.K_DOWN and self.selected < 4):
                self.selected += 1
            if(event.key == pygame.K_UP and self.selected > 0):
                self.selected -= 1
            if(event.key == pygame.K_RETURN):
                change_event(self.selected);

    #Code to update all of the sprite groups and clear them from the screen
    def update(self, time):
        pass

def change_event(selected):
    if(selected == 0):
        Constants.STATE = Play.Play()
    elif(selected == 3):
        Constants.STATE = HighScore.HighScore("",0, False)
    elif(selected == 4):
        exit()
