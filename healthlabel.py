import pygame as game
#Helper class to make the label a Sprite for more efficient updating
class healthlabel(game.sprite.Sprite):
    def __init__(self, health):
        game.sprite.Sprite.__init__(self)
        #will make font sexier later
        self.font = game.font.Font(None,30)
        self.text = "Health: 100%"
        self.image = self.font.render(self.text,1,(0,255,0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)

    def update(self,health):
        #Get appropriate label color based on health
        if (health < 25):
            COLOR = (255,0,0)
        elif (health < 75):
            COLOR = (255,255,0)
        else:
            COLOR = (0,255,0)
        self.image = self.font.render("Health: " + str(health) + "%",1,COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)

