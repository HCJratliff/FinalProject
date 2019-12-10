import pygame
import sys
import os
import random


class SlidePuzzle:
    def __init__(self, gs, ts, ms):
        self.gs, self.ts, self.ms = gs, ts, ms
        # gs is in the form (n, m) and refers to number of rows and columns respectively
        # ts refers to tile features/size in the game
        # ms refers to margin size (i.e. space between tiles)
        self.tiles = [(x, y) for x in range(gs[0]) for y in range(gs[1])]
        # Setting the number of each tile in columns and rows the array
        self.tile_pos = {(x, y): (x*(ts+ms)+ms, y*(ts+ms)+ms) for x in range(gs[0]) for y in range(gs[1])}
        # setting position of each tile within margin of array in game
        self.tiles_len = gs[0]*gs[1] - 1
        # Number of tiles is number of rows times number of columns minus 1
        self.font = pygame.font.Font(None, 100)
        # Setting default font and size = 120 in pygame
        self.images = []
        font = self.font
        self.prev = None

        for i in range(self.tiles_len):
            image = pygame.Surface((ts, ts))
            image.fill((120, 50, 200))
            # Setting color of tiles in array
            text = font.render(str(i+1), 2, (0, 0, 0))
            width, height = text.get_size()
            image.blit(text, ((ts-width)/2, (ts-height)/2))
            self.images += [image]

        for i in range(0, 1000):
            self.random()
        # randomizes the layout of the puzzle

    def draw(self, screen):
        for i in range(self.tiles_len):
            x, y = self.tile_pos[self.tiles[i]]
            screen.blit(self.images[i], (x, y))
    # draws the screen itself

    def set_as_blank(self):
        return self.tiles[-1]

    def getblank(self, pos):
        self.tiles[-1] = pos
    open_tile = property(set_as_blank, getblank)
    # sets open_tile as blank

    def switch(self, tile):
        n = self.tiles.index(tile)
        self.tiles[n], self.open_tile = self.open_tile, tile
        # defines method of switching a desired tile and the open_tile

    def adjacent(self):
        x, y = self.open_tile
        return (x-1, y), (x+1, y), (x, y-1), (x, y+1)
    # defines all legal move to adjacent tiles

    def in_grid(self, tile):
        return tile[0] >= 0 and tile[0] < self.gs[0] and tile[1] >= 0 and tile[1] < self.gs[1]
    # defines boundaries of array on screen

    def random(self):
        adj = self.adjacent()
        self.switch(random.choice([pos for pos in adj if self.in_grid(pos) and pos != self.prev]))
        # makes a random choice between tiles that are adjacent to the open_tile

    def update(self, dt):
        mouse = pygame.mouse.get_pressed()
        mousepos = pygame.mouse.get_pos()
        if mouse[0]:
            x, y = mousepos[0] % (self.ts+self.ms), mousepos[1] % (self.ts+self.ms)
            if x > self.ms and y > self.ms:
                tile = mousepos[0]//self.ts, mousepos[1]//self.ts
                if self.in_grid(tile) and tile in self.adjacent():
                    self.switch(tile)
                    # defines a mouse click as a switch

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            for key, dx, dy in ((pygame.K_w, 0, -1), (pygame.K_s, 0, 1), (pygame.K_a, -1, 0), (pygame.K_d, 1, 0)):
                # defining interactions if any of a, s, w, d are used
                if event.key == key:
                    x, y = self.open_tile
                    tile = x+dx, y+dy
                    if self.in_grid(tile):
                        self.switch(tile)
                        # switches according to which key is pressed

            if event.key == pygame.K_SPACE:
                self.random()
                # pressing space makes a random move

def main():
    # function that runs continuously while game is live
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    # creates environmental dictionary for mapping purposes
    pygame.display.set_caption('Slide Puzzle')
    # Setting caption for game
    screen = pygame.display.set_mode((800, 800))
    # Setting size of Screen
    fps_clock = pygame.time.Clock()
    program = SlidePuzzle((4, 4), 150, 5)
    # determines dimensions and other arguments of slide puzzle

    while True:
        dt = fps_clock.tick()/1000

        screen.fill((0, 0, 0))
        program.draw(screen)
        pygame.display.flip()
        # creates game window and display

        for event in pygame.event.get():  # I.E. for an action in the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # If the action / event is to quit the game, exit the system
            program.events(event)

        program.update(dt)


if __name__ == '__main__':
    main()