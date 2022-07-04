import pygame
from pygame import mixer
from random import choice, randint
from button import Button

pygame.font.init()
mixer.init()

#dimensions
SCREEN_WIDTH = 550
SCREEN_HEIGHT = 700
TILE_SIZE = 25

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define colours
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (168, 2, 184)
ORANGE = (255, 100, 23)
YELLOW = (247, 255, 23)
GRAY = (146, 148, 147)
WHITE = (255, 255, 255)

#game variables
allowed_colours = [RED, GREEN, BLUE, PURPLE, ORANGE, YELLOW]
COOLDOWN = 500
SIDE_OFFSET = 125
BOTTOM_OFFSET = 50

#rows and columns
ROWS = (SCREEN_HEIGHT - BOTTOM_OFFSET) // TILE_SIZE
COLUMNS = (SCREEN_WIDTH - 2*SIDE_OFFSET) // TILE_SIZE

print(COLUMNS)

#create screen and set caption
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

#load and scale button images
play_again_image = pygame.image.load("assets/play_again.png")
play_again_scaled_image = pygame.transform.scale(play_again_image, ((play_again_image.get_width() // 3),
                        (play_again_image.get_height() // 3)))

exit_image = pygame.image.load("assets/exit.png")
exit_scaled_image = pygame.transform.scale(exit_image, ((exit_image.get_width() // 6),
                        (exit_image.get_height() // 6)))

#load mand play music
pygame.mixer.music.load("assets/tetris_main.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0, 0)

#functions for drawing text
def draw_text(surface, x, y, font, color, string, height):
    format = pygame.font.SysFont(font, height)
    text = format.render(string, True, color)
    return surface.blit(text, (x, y))

def centeredx_text(surface, y, font, color, string, height):
    format = pygame.font.SysFont(font, height)
    text = format.render(string, True, color)
    return surface.blit(text, ((surface.get_width() -text.get_width())/2, y))

def centeredy_text(surface, x, font, color, string, height):
    format = pygame.font.SysFont(font, height)
    text = format.render(string, True, color)
    return surface.blit(text, ((x, (surface.get_height() - text.get_height())/2)))

#tetris and their rotation
I = [[[0, 0, 0, 0],
      [1, 1, 1, 1]],

     [[0, 1],
      [0, 1],
      [0, 1],
      [0, 1]],

    [[0, 0, 0, 0],
     [0, 0, 0, 0],
     [1, 1, 1, 1]],

    [[0, 0, 1],
     [0, 0, 1],
     [0, 0, 1],
     [0, 0, 1]]]

L = [[[1, 0, 0],
      [1, 1, 1]],

     [[0, 1, 1],
      [0, 1, 0],
      [0, 1, 0]],

     [[0, 0, 0],
      [1, 1, 1],
      [0, 0, 1]],

     [[0, 1, 0],
      [0, 1, 0],
      [1, 1, 0]]]

J = [[[0, 0, 1],
      [1, 1, 1]],

     [[0, 1, 0],
      [0, 1, 0],
      [0, 1, 1]],

     [[0, 0, 0],
      [1, 1, 1],
      [1, 0, 0]],

     [[1, 1, 0],
      [0, 1, 0],
      [0, 1, 0]]]

O = [[[1, 1],
      [1, 1]],

     [[1, 1],
      [1, 1]],

     [[1, 1],
      [1, 1]],

     [[1, 1],
      [1, 1]]]

S = [[[0, 1, 1],
      [1, 1, 0]],

     [[0, 1, 0],
      [0, 1, 1],
      [0, 0, 1]],

     [[0, 0, 0],
      [0, 1, 1],
      [1, 1, 0]],

     [[1, 0, 0],
      [1, 1, 0],
      [0, 1, 0]]]

Z = [[[1, 1, 0],
      [0, 1, 1]],

     [[0, 0, 1],
      [0, 1, 1],
      [0, 1, 0]],

     [[0, 0, 0],
      [1, 1, 0],
      [0, 1, 1]],

     [[0, 1, 0],
      [1, 1, 0],
      [1, 0, 0]]]

T = [[[0, 1, 0],
     [1, 1, 1]],

     [[0, 1, 0],
      [0, 1, 1],
      [0, 1, 0]],

     [[0, 0, 0],
      [1, 1, 1],
      [0, 1, 0]],

     [[0, 1, 0],
      [1, 1, 0],
      [0, 1, 0]]]

all_tetris = [I, L, J, O, S, Z, T]

#tetris class
class Tetris:

    def __init__(self, tetris, vel, cooldown):
        self.tetris = tetris
        self.vel = vel
        self.min_cooldown = cooldown
        self.cooldown = self.min_cooldown
        self.last_time = pygame.time.get_ticks()
        self.keys = pygame.key.get_pressed()
        self.colour = choice(allowed_colours)
        self.wait = True
        self.wait_rotation = True
        self.moving = True
        self.stop = False
        self.game_over = False
        self.rotation = randint(0, len(self.tetris) - 1)
        self.floor_time = 20
        self.shape = self.tetris[self.rotation]
        self.lenght = len(self.tetris[self.rotation][0])
        self.rect_list = []
        self.possible_x = randint(0,COLUMNS - self.lenght)
        self.corner = pygame.Rect((SIDE_OFFSET + TILE_SIZE * self.possible_x, -2 * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        for y, row in enumerate(self.tetris[self.rotation]):
            for x, i in enumerate(row):
                if i == 1:
                    self.rect = pygame.Rect((SIDE_OFFSET +  TILE_SIZE*self.possible_x + TILE_SIZE * x, -2 * TILE_SIZE + TILE_SIZE * y, TILE_SIZE, TILE_SIZE))
                    self.rect_list.append(self.rect)

    def draw(self):
        for rect in self.rect_list:
            pygame.draw.rect(screen, self.colour, rect)
            pygame.draw.rect(screen, WHITE, rect, 2)
            #pygame.draw.rect(screen, BLACK, self.corner)

    def check(self):
        #check collision with other tetris
        if self.game_over == False:
            self.moving_counter = 0
            self.left_counter = 0
            self.right_counter = 0
            if len(tetris) > 1:
                for element in tetris[:-2]:
                    for rect1 in element.rect_list:
                        for rect in self.rect_list:
                            temp_rect_down = pygame.Rect(rect[0], rect[1] + TILE_SIZE, rect[2], rect[3])
                            temp_rect_left = pygame.Rect(rect[0] - TILE_SIZE, rect[1], rect[2], rect[3])
                            temp_rect_right = pygame.Rect(rect[0] + TILE_SIZE, rect[1], rect[2], rect[3])

                            if temp_rect_down.colliderect(rect1):
                                self.moving_counter += 1
                            if temp_rect_left.colliderect(rect1):
                                self.left_counter += 1
                            if temp_rect_right.colliderect(rect1):
                                self.right_counter += 1

            if self.moving_counter != 0:
                self.moving = False

                if self.left_counter != 0 and self.right_counter != 0:
                    self.stop = True

    def move_down(self):
        if self.game_over == False:
            self.keys = pygame.key.get_pressed()
            if self.stop == False and self.moving == True:
                if pygame.time.get_ticks() - self.last_time >= self.cooldown:
                    for rect in self.rect_list:
                        rect.y += self.vel
                    self.last_time = pygame.time.get_ticks()
                    self.corner.y += self.vel

            #increase speed
            if self.keys[pygame.K_s]:
                self.cooldown /= 5
            elif not self.keys[pygame.K_s]:
                self.cooldown = self.min_cooldown

            # collision with floor
            counter = 0
            for rect in self.rect_list:
                if rect.bottom + TILE_SIZE > SCREEN_HEIGHT - BOTTOM_OFFSET:
                    counter += 1
            if counter == 0 and self.moving_counter == 0:
                self.moving = True
            else:
                self.moving = False
                self.floor_time -= 1
            if self.floor_time < 0:
                self.stop = True

    def move_right(self):
        if self.game_over == False:
            #right border collision
            if self.keys[pygame.K_d] and self.wait == True and self.stop == False and self.floor_time > 0:
                self.counter_right = 0
                for rect in self.rect_list:
                    if rect.right + TILE_SIZE > SCREEN_WIDTH - SIDE_OFFSET:
                        self.counter_right += 1

                #move right
                if self.counter_right == 0 and self.right_counter == 0:
                    for rect in self.rect_list:
                        rect.x += TILE_SIZE
                        self.wait = False
                    self.corner.x += TILE_SIZE

            # release both a and d for moving again
            if (not self.keys[pygame.K_d]) and (not self.keys[pygame.K_a]):
                self.wait = True

    def move_left(self):
        if self.game_over == False:
            #left border collision
            if self.keys[pygame.K_a] and self.wait == True and self.stop == False and self.floor_time > 0:
                self.counter_left = 0
                for rect in self.rect_list:
                    if rect.left - TILE_SIZE < SIDE_OFFSET:
                        self.counter_left += 1

                #move left
                if self.counter_left == 0 and self.left_counter == 0:
                    for rect in self.rect_list:
                        rect.x -= TILE_SIZE
                        self.wait = False
                    self.corner.x -= TILE_SIZE

                # release both a and d for moving again
                if (not self.keys[pygame.K_d]) and (not self.keys[pygame.K_a]):
                    self.wait = True

    def rotate(self):
        if self.game_over == False:
            self.rotated_list = []

            if self.keys[pygame.K_r] and self.wait_rotation:
                self.rotation += 1
                if self.rotation > len(self.tetris) - 1:
                    self.rotation = 0
                self.wait_rotation = False
                self.shape = self.tetris[self.rotation]

                for y, row in enumerate(self.shape):
                    for x, i in enumerate(row):
                        if i == 1:
                            self.rotated_rect = pygame.Rect(self.corner.x + TILE_SIZE*x, self.corner.y + TILE_SIZE*y,
                                                            TILE_SIZE, TILE_SIZE)
                            self.rotated_list.append(self.rotated_rect)

                self.rotate_counter = 0
                if len(tetris) > 1:
                    for element in tetris[:-2]:
                        for rect1 in element.rect_list:
                            for rect in self.rotated_list:
                                if rect.colliderect(rect1) or rect.left < SIDE_OFFSET or rect.right > SCREEN_WIDTH - SIDE_OFFSET \
                                        or rect.bottom > SCREEN_HEIGHT - BOTTOM_OFFSET:
                                    self.rotate_counter += 1

                elif len(tetris) == 1:
                    for rect in self.rotated_list:
                        if rect.left < SIDE_OFFSET or rect.right > SCREEN_WIDTH - SIDE_OFFSET \
                                or rect.bottom > SCREEN_HEIGHT - BOTTOM_OFFSET:
                            self.rotate_counter += 1

                if self.rotate_counter == 0:
                    self.rect_list = self.rotated_list
                else:
                    self.rotation -= 1

            if not self.keys[pygame.K_r]:
                self.wait_rotation = True

    def gameover(self):
        if self.stop == True:
            gameover_counter = 0
            for rect in self.rect_list:
                if rect.bottom <= 0:
                    gameover_counter += 1

            if gameover_counter != 0:
                self.game_over = True

#special tetris
donut = [[1, 1, 1, 1],
         [1, 0, 0, 1],
         [1, 0, 0, 1],
         [1, 1, 1, 1]]

#tetris list
tetris = []
tetris.append(Tetris(choice(all_tetris), TILE_SIZE, COOLDOWN))

highscore = 0

#main function
def main():
    global highscore
    run = True
    score = 0

    # game loop
    while run:

            clock.tick(FPS)

            #if all the drawn tetris aren't moving then create a new one
            counter = len(tetris) - 1
            for element in tetris:
                if element.moving == False and element.stop == True and element.game_over == False:
                    counter -= 1
            if counter == 0:
                tetris.append(Tetris(choice(all_tetris), TILE_SIZE, COOLDOWN))

            #possible feature using mouse
            '''mouse = pygame.mouse.get_pos()
                if SIDE_OFFSET <= mouse[0] <= SCREEN_WIDTH - SIDE_OFFSET and 0 <= mouse[1] <= SCREEN_HEIGHT - BOTTOM_OFFSET:
                    x = int((mouse[0] - SIDE_OFFSET) / TILE_SIZE) + 1
                    y = int(mouse[1] / TILE_SIZE) + 1
                    coords = [x, y]
                    print(coords)'''

            #draw background
            screen.fill(WHITE)

            #draw border
            pygame.draw.rect(screen, BLACK, (0, 0, SIDE_OFFSET, SCREEN_HEIGHT))
            pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - SIDE_OFFSET, 0, SIDE_OFFSET, SCREEN_HEIGHT))
            pygame.draw.rect(screen, BLACK, (SIDE_OFFSET, SCREEN_HEIGHT - BOTTOM_OFFSET, SCREEN_WIDTH - 2*SIDE_OFFSET, BOTTOM_OFFSET))

            #draw 10*13 grid
            grid = []
            for i in range(ROWS):
                row = []
                for j in range(COLUMNS):
                    rect = pygame.Rect((SIDE_OFFSET + TILE_SIZE*j, TILE_SIZE*i, TILE_SIZE, TILE_SIZE))
                    pygame.draw.rect(screen, BLACK, rect, 1)
                    row.append(rect)
                grid.append(row)

            #rotate the last tetris created
            tetris[-2].rotate()

            #draw all the tetris
            for element in tetris[:-1]:
                element.draw()

            #move the tetris only if it won't collide with others, or the borders, from above, left and right
            tetris[-2].check()
            tetris[-2].move_down()
            tetris[-2].move_left()
            tetris[-2].move_right()

            #check if the game is over
            tetris[-2].gameover()

            #check complete row
            for r, row in enumerate(grid):
                row_counter = COLUMNS
                for square in row:
                    for element in tetris[:-2]:
                        for rect in element.rect_list:
                            if square.colliderect(rect):
                                row_counter -= 1

                #create a list of the rectangles that have to be removed
                if row_counter == 0:
                    remove_list = []
                    for element in tetris[:-2]:
                        for rect in element.rect_list:
                            if rect.top == r * TILE_SIZE:
                                remove_list.append(rect)

                    #remove those rectangles
                    for rect in remove_list:
                        for element in tetris[:-2]:
                            try:
                                element.rect_list.remove(rect)
                            except ValueError:
                                pass

                    # create a list of the rectangles that have to be moved down by 1 tile
                    move_list = []
                    for element in tetris[:-2]:
                        for rect in element.rect_list:
                            if rect.top < r * TILE_SIZE:
                                move_list.append(rect)

                    #move those rectangles
                    for rect in move_list:
                        rect.y += TILE_SIZE

                    score += 1

            #update highscore
            if score > highscore:
                highscore = score

            #draw score and highscore
            centeredx_text(screen, SCREEN_HEIGHT - BOTTOM_OFFSET, "futura", BLUE, "LINES: " + str(score), 20)
            centeredy_text(screen, 4, "futura", WHITE, "HIGHSCORE: " + str(highscore), 20)
            draw_text(screen, SCREEN_WIDTH - SIDE_OFFSET + 40, SCREEN_HEIGHT // 2 - 70, "futura", BLUE, "NEXT", 20)

            #draw next tetris
            if len(tetris) > 1:
                height = len(tetris[-1].tetris[tetris[-1].rotation])
                width = len(tetris[-1].tetris[tetris[-1].rotation][0])
                for y, row in enumerate(tetris[-1].tetris[tetris[-1].rotation]):
                    for x, i in enumerate(row):
                        if i == 1:
                            rect = pygame.Rect((SCREEN_WIDTH - SIDE_OFFSET + width * 5 + TILE_SIZE * x,
                                                     SCREEN_HEIGHT // 2 - height*TILE_SIZE // 2 + TILE_SIZE * y, TILE_SIZE, TILE_SIZE))
                            pygame.draw.rect(screen, tetris[-1].colour, rect)



            #gameover function
            if tetris[-2].game_over:
                pygame.mixer.music.stop()
                play_again = Button(screen, SCREEN_WIDTH // 2 - play_again_scaled_image.get_width() // 2,
                                    SCREEN_HEIGHT // 2 - 100, play_again_scaled_image.get_width(),
                                    play_again_scaled_image.get_height(), BLUE, play_again_scaled_image, None)

                exit = Button(screen, SCREEN_WIDTH // 2 - exit_scaled_image.get_width() // 2,
                                    SCREEN_HEIGHT // 2, exit_scaled_image.get_width(),
                                    exit_scaled_image.get_height(), BLUE, exit_scaled_image, None)
                play_again.draw()
                exit.draw()
                if play_again.is_pressed_left():
                    tetris.clear()
                    tetris.append(Tetris(choice(all_tetris), TILE_SIZE, COOLDOWN))
                    pygame.mixer.music.play(-1, 0, 0)
                    main()
                elif exit.is_pressed_left():
                    run = False

            #event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            #update the screen
            pygame.display.update()

    if run:
        main()

if __name__ == "__main__":
    main()

pygame.quit()

#highscore 52
