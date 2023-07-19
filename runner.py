import threading
import pygame
import sys
import time

import mazeutils as mm

pygame.init()

pygame.display.set_caption("Durian's Quest to Find His BHM")
pygame.display.set_icon(pygame.image.load("pathfinder-icon.png"))

size = width, height = 900, 600
padding = 20

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (70, 204, 47)
red = (204, 30, 47)
yellow = (237, 210, 24)
orange = (255, 165, 0)

screen = pygame.display.set_mode(size)

# Fonts
smallFont = pygame.font.Font("JetBrainsMono-Regular.ttf", 20)
mediumFont = pygame.font.Font("JetBrainsMono-Regular.ttf", 28)
largeFont = pygame.font.Font("JetBrainsMono-Regular.ttf", 32)

maze = mm.initial_state()
pointToggle = True

editing = True
solving = False

class Maze():
    def __init__(self, maze, mode):
        self.mode = mode

        self.height = 20
        self.width = 20

        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if maze[i][j] == mm.START:
                        self.start = (i, j)
                        row.append(False)
                    elif maze[i][j] == mm.END:
                        self.goal = (i, j)
                        row.append(False)
                    elif maze[i][j] == mm.EMPTY:
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    def neighbors(self, cell):
        row, col = cell
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result
    
    def print(self):
        global maze
        # solution = self.solution[1] if self.solution is not None else None
        # print()
        # for i, row in enumerate(self.walls):
        #     for j, col in enumerate(row):
        #         if col:
        #             print("#", end="")
        #         elif (i, j) == self.start:
        #             print("A", end="")
        #         elif (i, j) == self.goal:
        #             print("B", end="")
        #         elif solution is not None and (i, j) in solution:
        #             print("*", end="")
        #         else:
        #             print(" ", end="")
        #     print()
        # print()
        for i in range(len(self.explored)):
            time.sleep(0.05)
            if self.explored[i] != self.start and self.explored[i] != self.goal:
                rect = pygame.Rect(
                    self.explored[i][0] * tile_size,
                    self.explored[i][1] * tile_size,
                    tile_size, tile_size
                )
                if self.explored[i] in self.solution[1]:
                    pygame.draw.rect(screen, orange, rect, 15)
                    maze = mm.result(maze, self.explored[i], mm.ANSWER)
                else:
                    pygame.draw.rect(screen, yellow, rect, 15)
                    maze = mm.result(maze, self.explored[i], mm.PATH)
    
    def solve(self):
        global maze
        global solving

        start = mm.Node(state=self.start, parent=None, action=None)
        # Change between StackFrontier() and QueueFrontier() to switch between the search algorithms
        if self.mode == "DFS":
            frontier = mm.StackFrontier()
        elif self.mode == "BFS":
            frontier = mm.QueueFrontier()
        frontier.add(start)

        self.explored = []

        # Keep looping until solution found
        while solving:

            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # Choose a node from the frontier
            node = frontier.remove()

            # If node is the goal, then we have a solution
            if node.state == self.goal:
                solving = False
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # Mark node as explored
            self.explored.append(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = mm.Node(state=state, parent=node, action=action)
                    frontier.add(child)

while True:
    
    # Close Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Fill Background Color
    screen.fill(white)

    # Update Board (Editing)
    tile_size = 30
    tiles = []

    for i in range(20):
        row = []
        for j in range(20):
            rect = pygame.Rect(
                j * tile_size,
                i * tile_size,
                tile_size, tile_size
            )
            pygame.draw.rect(screen, black, rect, 1)

            if maze[i][j] == mm.WALL:
                pygame.draw.rect(screen, black, rect, 15)
            elif maze[i][j] == mm.START:
                pygame.draw.rect(screen, green, rect, 15)
            elif maze[i][j] == mm.END:
                pygame.draw.rect(screen, red, rect, 15)
            elif maze[i][j] == mm.PATH:
                pygame.draw.rect(screen, yellow, rect, 15)
            elif maze[i][j] == mm.ANSWER:
                pygame.draw.rect(screen, orange, rect, 15)
            row.append(rect)
        tiles.append(row)
        
    # Draw Buttons (Add Feedback on Hover and Click in the future)
    dfsButton = pygame.Rect(600 + padding, padding, 260, 80)
    dfs = smallFont.render("Depth-First Search", True, white)
    dfsRect = dfs.get_rect()    
    dfsRect.center = dfsButton.center
    pygame.draw.rect(screen, black, dfsButton, border_radius=20)
    screen.blit(dfs, dfsRect)

    bfsButton = pygame.Rect(600 + padding, 80 + 2 * padding, 260, 80)
    bfs = smallFont.render("Breadth-First Search", True, white)
    bfsRect = bfs.get_rect()    
    bfsRect.center = bfsButton.center
    pygame.draw.rect(screen, black, bfsButton, border_radius=20)
    screen.blit(bfs, bfsRect)

    resetButton = pygame.Rect(600 + padding, 500, 260, 80)
    reset = mediumFont.render("Reset", True, white)
    resetRect = reset.get_rect()    
    resetRect.center = resetButton.center
    pygame.draw.rect(screen, black, resetButton, border_radius=20)
    screen.blit(reset, resetRect)

    # Button Functionality
    click, _, _ = pygame.mouse.get_pressed()
    if click == 1:
        mouse = pygame.mouse.get_pos()
        if resetButton.collidepoint(mouse):
            maze = mm.initial_state()
            pointToggle = True

            editing = True
            solving = False
            
    # Editing Mode
    if editing:
        left, middle, right = pygame.mouse.get_pressed()
        if left == 1:
            mouse = pygame.mouse.get_pos()
            if dfsButton.collidepoint(mouse):
                editing = False
                solving = True
                m = Maze(maze, "DFS")         
                m.solve()

                threading.Thread(target=m.print).start()
            
            elif bfsButton.collidepoint(mouse):
                editing = False
                solving = True
                m = Maze(maze, "BFS")
                m.solve()

                threading.Thread(target=m.print).start()
                    
            else:
                for i in range(20):
                    for j in range(20):
                        if (maze[i][j] == mm.EMPTY and tiles[i][j].collidepoint(mouse)):
                            maze = mm.result(maze, (i, j), mm.WALL)
        elif right == 1:
            mouse = pygame.mouse.get_pos()
            for i in range(20):
                for j in range(20):
                    if (tiles[i][j].collidepoint(mouse)):
                        maze = mm.result(maze, (i, j), mm.EMPTY)
        elif middle == 1:
            mouse = pygame.mouse.get_pos()
            for i in range(20):
                for j in range(20):
                    if (tiles[i][j].collidepoint(mouse)):
                        if (pointToggle):
                            if mm.checker(maze, mm.START) > 0: maze = mm.result(maze, mm.where_is(maze, mm.START), mm.EMPTY)
                            maze = mm.result(maze, (i, j), mm.START)
                        else:
                            if mm.checker(maze, mm.END) > 0: maze = mm.result(maze, mm.where_is(maze, mm.END), mm.EMPTY)
                            maze = mm.result(maze, (i, j), mm.END)
                        pointToggle = not pointToggle
                        time.sleep(0.2)
    # Update Screen / Display
    pygame.display.flip()
