import pygame as game
#Helper class to make the label a Sprite for more efficient updating
class label(game.sprite.Sprite):
    def __init__(self, name, inittext, location):
        game.sprite.Sprite.__init__(self)
        #will make font sexier later
        self.font = game.font.Font(None,30)
        self.text = inittext
        self.image = self.font.render(self.text,1,(0,255,0))
        self.rect = self.image.get_rect()
        self.rect.topleft = location
        self.name = name

    #one method for all the updates - type will be used kinda like an enum
    def update(self,param):
        if self.name == "health":
            #Get appropriate label color based on health
            if (param < 25):
                COLOR = (255,0,0)
            elif (param < 75):
                COLOR = (255,255,0)
            else:
                COLOR = (0,255,0)
            self.image = self.font.render("Health: " + str(param) + "%",1,COLOR)
        else:
            COLOR = (255,255,255)
            self.image = self.font.render(self.text + "%3.4f" % (param),1,COLOR)