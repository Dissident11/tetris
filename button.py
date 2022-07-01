import pygame

class Button:

    def __init__(self, surface, x, y, width, height, color, image, bg):
        self.surface = surface
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.image = image
        self.bg = bg
        self.mouse_position = pygame.mouse.get_pos()
        self.mouse = pygame.mouse.get_pressed()

    def draw(self):
        if self.image == None:
            self.button = pygame.Rect(self.x, self.y, self.width, self.height)
            pygame.draw.rect(self.surface, self.color, self.button)
        elif self.bg:
            self.bg = pygame.Rect(self.x, self.y,self.width, self.height)
            pygame.draw.rect(self.surface, self.color, self.bg)
            self.surface.blit(self.image, (self.x + self.width/2 - self.image.get_width()/2,
                                            self.y + self.height/2 - self.image.get_height()/2))
        else:
            self.surface.blit(self.image, (self.x, self.y))

    def mouse_on(self):
        if self.x + self.width >= self.mouse_position[0] >= self.x and self.y + self.height >= self.mouse_position[1] >= self.y:
            return True

    def is_pressed_left(self):
        if self.mouse_on() and self.mouse[0]:
            return True
        else:
            return False

    def is_pressed_middle(self):
        if self.mouse_on() and self.mouse[1]:
            return True
        else:
            return False

    def is_pressed_right(self):
        if self.mouse_on() and self.mouse[2]:
            return True
        else:
            return False