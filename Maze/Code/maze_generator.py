import pygame
from random import choice
import json

RES = WIDTH, HEIGHT = 1200, 900
TILE = 50
cols, rows = WIDTH // TILE, HEIGHT // TILE

pygame.init()
sc = pygame.display.set_mode(RES)
pygame.display.set_caption('Maze generator')
clock = pygame.time.Clock()

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
    
    def draw_current_cell(self):
        x, y = self.x * TILE, self.y * TILE
        
        pygame.draw.rect(sc, pygame.Color('#f70067'),
                         (x + 2, y + 2, TILE - 2, TILE - 2))
        
    def draw(self):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(sc, pygame.Color('#3eb489'),
                             (x, y, TILE, TILE))
        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('#030659'), 
                             (x, y), (x + TILE, y), 6)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('#030659'), 
                             (x + TILE, y), 
                             (x + TILE, y + TILE), 6)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('#030659'), 
                             (x + TILE, y + TILE),
                             (x , y + TILE), 6)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('#030659'), 
                             (x, y + TILE), (x, y), 6)
            
    def check_cell(self, x, y):
        
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        
        return grid_cells[find_index(x, y)] 
    
    def check_neighbors(self):
        neighbors = []
        
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        
        return choice(neighbors) if neighbors else False   
    
def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False 

def reset_game_state():
    global grid_cells, current_cell, stack, colors, color, maze_array 
    grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
    current_cell = grid_cells[0]
    stack = []
    colors, color = [], 40

reset_game_state() 

while True:
    sc.fill(pygame.Color('#a6d5e2'))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            reset_game_state()

            
    [cell.draw() for cell in grid_cells]
    current_cell.visited = True
    current_cell.draw_current_cell()
    [pygame.draw.rect(sc, colors[i], 
                      (cell.x * TILE + 2, cell.y * TILE + 2,
                       TILE - 1, TILE - 1), border_radius=8) for i,
                       cell in enumerate(stack)] 
    
    next_cell = current_cell.check_neighbors()
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        colors.append((min(color, 255), 0, 103))
        color += 1
        remove_walls(current_cell, next_cell)
        current_cell=next_cell
    elif stack: 
        current_cell = stack.pop()
    
    maze_array = [{'x': cell.x, 'y': cell.y, 'walls': cell.walls} for cell in grid_cells]
    # print(maze_array)
    file_path = 'walls_data.json'

    # Save the dictionary to a file
    with open(file_path, 'w') as json_file:
        json.dump(maze_array, json_file)
    
    pygame.display.flip()
    clock.tick() 