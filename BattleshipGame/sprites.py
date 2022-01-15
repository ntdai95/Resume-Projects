import pygame as pg
from os import path
from settings import *


class Cruiser(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(path.join(path.join(path.dirname(__file__), "Images"), "cruiser.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = [1100, 135]
        self.position = "horizontal"
        self.position_computer = None

    def update(self, rotate_ship, selected_ship, mouse_position, player_grid, game_battle_running, computer_turn, missile_position_y, missile_on, computer_grid, computer_ships_sunk):
        if game_battle_running == False and computer_turn == False and (rotate_ship == "cruiser" or (self.position == "horizontal" and (TABLE_POSITION_X + 2 * CELL_SIZE > self.rect.center[0] or self.rect.center[0] > TABLE_POSITION_X - 2 * CELL_SIZE + TABLE_SIZE \
            or TABLE_POSITION_Y > self.rect.center[1] or self.rect.center[1] > TABLE_POSITION_Y + TABLE_SIZE)) or (self.position == "vertical" and (TABLE_POSITION_X > self.rect.center[0] \
            or self.rect.center[0] > TABLE_POSITION_X + TABLE_SIZE or TABLE_POSITION_Y + 2 * CELL_SIZE > self.rect.center[1] or self.rect.center[1] > TABLE_POSITION_Y - 2 * CELL_SIZE + TABLE_SIZE))):
            for row_index in range(11):
                for column_index in range(11):
                    if player_grid[row_index][column_index] == 5:
                        player_grid[row_index][column_index] = 0
    
        if rotate_ship == "cruiser" and self.position == "horizontal":
            self.position = "vertical"
            self.image = pg.transform.rotate(self.image, 90)
            self.rect = self.image.get_rect(center = [1450, 250])
        elif rotate_ship == "cruiser" and self.position == "vertical":
            self.position = "horizontal"
            self.image = pg.transform.rotate(self.image, 270)
            self.rect = self.image.get_rect(center = [1100, 135])
        elif selected_ship != "cruiser" and any(5 in row for row in player_grid) and rotate_ship != "cruiser":
            if game_battle_running and computer_turn == False:
                list_of_cells = []
                for row_index in range(11):
                    for column_index in range(11):
                        if computer_grid[row_index][column_index] == 5:
                            list_of_cells.append([column_index, row_index])
                center_cell = list_of_cells[2]
                if 5 not in computer_ships_sunk:
                    self.rect.center = tuple([center_cell[0] * CELL_SIZE + CELL_SIZE / 2 - SCREEN_WIDTH + TABLE_POSITION_X_MAIN_BATTLE, center_cell[1] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_Y])
                elif center_cell[0] == list_of_cells[1][0]:
                    if self.position == "vertical" and self.position_computer == None:
                        self.image = pg.transform.rotate(self.image, 270)
                        self.rect = self.image.get_rect(center = [1100, 135])
                        self.position_computer = "horizontal"
                    self.rect.center = tuple([center_cell[1] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_X_MAIN_BATTLE, center_cell[0] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_Y])   
                else:
                    if self.position == "horizontal" and self.position_computer == None:
                        self.image = pg.transform.rotate(self.image, 90)
                        self.rect = self.image.get_rect(center = [1450, 250])
                        self.position_computer = "vertical"
                    self.rect.center = tuple([center_cell[1] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_X_MAIN_BATTLE, center_cell[0] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_Y])   
            else:    
                list_of_cells = []
                for row_index in range(11):
                    for column_index in range(11):
                        if player_grid[row_index][column_index] == 5:
                            list_of_cells.append([column_index, row_index])
                center_cell = list_of_cells[2]
                if game_battle_running:
                    if self.position == "horizontal" and self.position_computer == "vertical":
                        self.image = pg.transform.rotate(self.image, 270)
                        self.rect = self.image.get_rect(center = [1100, 135])
                        self.position_computer = None
                    elif self.position == "vertical" and self.position_computer == "horizontal":
                        self.image = pg.transform.rotate(self.image, 90)
                        self.rect = self.image.get_rect(center = [1450, 250])
                        self.position_computer = None
                    self.rect.center = tuple([center_cell[0] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_X_MAIN_BATTLE_COMPUTER_TURN, center_cell[1] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_Y])
                else:
                    self.rect.center = tuple([center_cell[0] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_X, center_cell[1] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_Y])
        elif selected_ship == "cruiser":
            self.rect.center = mouse_position
        elif any(5 in row for row in player_grid) == False and selected_ship != "cruiser" and self.position == "horizontal" and game_battle_running == False:
            self.rect = self.image.get_rect(center = [1100, 135])
        elif any(5 in row for row in player_grid) == False and selected_ship != "cruiser" and self.position == "vertical" and game_battle_running == False:
            self.rect = self.image.get_rect(center = [1450, 250])


class AircraftCarrier(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(path.join(path.join(path.dirname(__file__), "Images"), "aircraftcarrier.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = [1060, 600]
        self.position = "horizontal"
        self.position_computer = None

    def update(self, rotate_ship, selected_ship, mouse_position, player_grid, game_battle_running, computer_turn, missile_position_y, missile_on, computer_grid, computer_ships_sunk):
        if game_battle_running == False and computer_turn == False and (rotate_ship == "aircraftcarrier" or (self.position == "horizontal" and (TABLE_POSITION_X + 2 * CELL_SIZE > self.rect.center[0] or self.rect.center[0] > TABLE_POSITION_X - CELL_SIZE + TABLE_SIZE \
            or TABLE_POSITION_Y > self.rect.center[1] or self.rect.center[1] > TABLE_POSITION_Y  - CELL_SIZE + TABLE_SIZE)) or (self.position == "vertical" and (TABLE_POSITION_X > self.rect.center[0] \
            or self.rect.center[0] > TABLE_POSITION_X - CELL_SIZE + TABLE_SIZE or TABLE_POSITION_Y + CELL_SIZE > self.rect.center[1] or self.rect.center[1] > TABLE_POSITION_Y - 2 * CELL_SIZE + TABLE_SIZE))):
            for row_index in range(11):
                for column_index in range(11):
                    if player_grid[row_index][column_index] == 4:
                        player_grid[row_index][column_index] = 0

        if rotate_ship == "aircraftcarrier" and self.position == "horizontal":
            self.position = "vertical"
            self.image = pg.transform.rotate(self.image, 90)
            self.rect = self.image.get_rect(center = [1380, 520])
        elif rotate_ship == "aircraftcarrier" and self.position == "vertical":
            self.position = "horizontal"
            self.image = pg.transform.rotate(self.image, 270)
            self.rect = self.image.get_rect(center = [1060, 600])
        elif selected_ship != "aircraftcarrier" and any(4 in row for row in player_grid) and rotate_ship != "aircraftcarrier":
            if game_battle_running and computer_turn == False:
                list_of_cells = []
                for row_index in range(11):
                    for column_index in range(11):
                        if computer_grid[row_index][column_index] == 4:
                            list_of_cells.append([column_index, row_index])
                center_cell = list_of_cells[1]
                if 4 not in computer_ships_sunk:
                    self.rect.center = tuple([center_cell[0] * CELL_SIZE + CELL_SIZE / 2 - self.image.get_width() * 1/8 + TABLE_POSITION_X_MAIN_BATTLE - SCREEN_WIDTH, center_cell[1] * CELL_SIZE + CELL_SIZE / 2 + self.image.get_height() * 1/4 + TABLE_POSITION_Y])
                elif center_cell[0] == list_of_cells[3][0] and center_cell[0] == list_of_cells[5][0]:
                    if self.position == "vertical" and self.position_computer == None:
                        self.image = pg.transform.rotate(self.image, 270)
                        self.rect = self.image.get_rect(center = [1060, 600])
                        self.position_computer = "horizontal"
                    center_cell = list_of_cells[4]
                    self.rect.center = tuple([center_cell[1] * CELL_SIZE + CELL_SIZE / 2 - self.image.get_width() * 1/8 + TABLE_POSITION_X_MAIN_BATTLE, center_cell[0] * CELL_SIZE + CELL_SIZE / 2 + self.image.get_height() * 1/4 + TABLE_POSITION_Y])
                else:
                    if self.position == "horizontal" and self.position_computer == None:
                        self.image = pg.transform.rotate(self.image, 90)
                        self.rect = self.image.get_rect(center = [1380, 520])
                        self.position_computer = "vertical"
                    self.rect.center = tuple([center_cell[1] * CELL_SIZE + CELL_SIZE / 2 + self.image.get_width() * 1/4 + TABLE_POSITION_X_MAIN_BATTLE, center_cell[0] * CELL_SIZE + CELL_SIZE / 2 + self.image.get_height() * 1/8 + TABLE_POSITION_Y])
            else:
                list_of_cells = []
                for row_index in range(11):
                    for column_index in range(11):
                        if player_grid[row_index][column_index] == 4:
                            list_of_cells.append([column_index, row_index])
                center_cell = list_of_cells[2]
                if game_battle_running and self.position == "horizontal":
                    if self.position_computer == "vertical":
                        self.image = pg.transform.rotate(self.image, 270)
                        self.rect = self.image.get_rect(center = [1060, 600])
                        self.position_computer = None
                    self.rect.center = tuple([center_cell[0] * CELL_SIZE + CELL_SIZE / 2 - self.image.get_width() * 1/8 + TABLE_POSITION_X_MAIN_BATTLE_COMPUTER_TURN, center_cell[1] * CELL_SIZE + CELL_SIZE / 2 + self.image.get_height() * 1/4 + TABLE_POSITION_Y])
                elif self.position == "horizontal":
                    self.rect.center = tuple([center_cell[0] * CELL_SIZE + CELL_SIZE / 2 - self.image.get_width() * 1/8 + TABLE_POSITION_X, center_cell[1] * CELL_SIZE + CELL_SIZE / 2 + self.image.get_height() * 1/4 + TABLE_POSITION_Y])
                elif game_battle_running and self.position == "vertical":
                    if self.position_computer == "horizontal":
                        self.image = pg.transform.rotate(self.image, 90)
                        self.rect = self.image.get_rect(center = [1380, 520])
                        self.position_computer = None
                    self.rect.center = tuple([center_cell[0] * CELL_SIZE + CELL_SIZE / 2 + self.image.get_width() * 1/4 + TABLE_POSITION_X_MAIN_BATTLE_COMPUTER_TURN, center_cell[1] * CELL_SIZE + CELL_SIZE / 2 + self.image.get_height() * 1/8 + TABLE_POSITION_Y])
                else:
                    self.rect.center = tuple([center_cell[0] * CELL_SIZE + CELL_SIZE / 2 + self.image.get_width() * 1/4 + TABLE_POSITION_X, center_cell[1] * CELL_SIZE + CELL_SIZE / 2 + self.image.get_height() * 1/8 + TABLE_POSITION_Y])
        elif selected_ship == "aircraftcarrier" and self.position == "horizontal":
            self.rect.center = tuple([mouse_position[0] - self.image.get_width() * 1/8, mouse_position[1] + self.image.get_height() * 1/4])
        elif selected_ship == "aircraftcarrier" and self.position == "vertical":
            self.rect.center = tuple([mouse_position[0] + self.image.get_width() * 1/4, mouse_position[1] + self.image.get_height() * 1/8])
        elif any(4 in row for row in player_grid) == False and selected_ship != "aircraftcarrier" and self.position == "horizontal" and game_battle_running == False:
            self.rect = self.image.get_rect(center = [1060, 600])
        elif any(4 in row for row in player_grid) == False and selected_ship != "aircraftcarrier" and self.position == "vertical" and game_battle_running == False:
            self.rect = self.image.get_rect(center = [1380, 520])


class Destroyer(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(path.join(path.join(path.dirname(__file__), "Images"), "destroyer.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = [1065, 365]
        self.position = "horizontal"
        self.position_computer = None

    def update(self, rotate_ship, selected_ship, mouse_position, player_grid, game_battle_running, computer_turn, missile_position_y, missile_on, computer_grid, computer_ships_sunk):
        if game_battle_running == False and computer_turn == False and (rotate_ship == "destroyer" or (self.position == "horizontal" and (TABLE_POSITION_X + 2 * CELL_SIZE > self.rect.center[0] or self.rect.center[0] > TABLE_POSITION_X - CELL_SIZE + TABLE_SIZE \
            or TABLE_POSITION_Y > self.rect.center[1] or self.rect.center[1] > TABLE_POSITION_Y + TABLE_SIZE)) or (self.position == "vertical" and (TABLE_POSITION_X > self.rect.center[0] \
            or self.rect.center[0] > TABLE_POSITION_X + TABLE_SIZE or TABLE_POSITION_Y + 2 * CELL_SIZE > self.rect.center[1] or self.rect.center[1] > TABLE_POSITION_Y - CELL_SIZE + TABLE_SIZE))):
            for row_index in range(11):
                for column_index in range(11):
                    if player_grid[row_index][column_index] == 3:
                        player_grid[row_index][column_index] = 0

        if rotate_ship == "destroyer" and self.position == "horizontal":
            self.position = "vertical"
            self.image = pg.transform.rotate(self.image, 90)
            self.rect = self.image.get_rect(center = [1170, 350])
        elif rotate_ship == "destroyer" and self.position == "vertical":
            self.position = "horizontal"
            self.image = pg.transform.rotate(self.image, 270)
            self.rect = self.image.get_rect(center = [1065, 365])
        elif selected_ship != "destroyer" and any(3 in row for row in player_grid) and rotate_ship != "destroyer":
            if game_battle_running and computer_turn == False:
                list_of_cells = []
                for row_index in range(11):
                    for column_index in range(11):
                        if computer_grid[row_index][column_index] == 3:
                            list_of_cells.append([column_index, row_index])
                center_cell = list_of_cells[1]
                if 3 not in computer_ships_sunk:
                    self.rect.center = tuple([center_cell[0] * CELL_SIZE + CELL_SIZE / 2 - self.image.get_width() * 1/8 + TABLE_POSITION_X_MAIN_BATTLE - SCREEN_WIDTH, center_cell[1] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_Y])
                elif center_cell[0] == list_of_cells[3][0]:
                    if self.position == "vertical" and self.position_computer == None:
                        self.image = pg.transform.rotate(self.image, 270)
                        self.rect = self.image.get_rect(center = [1065, 365])
                        self.position_computer = "horizontal"
                    center_cell = list_of_cells[2]
                    self.rect.center = tuple([center_cell[1] * CELL_SIZE + CELL_SIZE / 2 - self.image.get_width() * 1/8 + TABLE_POSITION_X_MAIN_BATTLE, center_cell[0] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_Y])
                else:
                    if self.position == "horizontal" and self.position_computer == None:
                        self.image = pg.transform.rotate(self.image, 90)
                        self.rect = self.image.get_rect(center = [1170, 350])
                        self.position_computer = "vertical"
                    self.rect.center = tuple([center_cell[1] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_X_MAIN_BATTLE, center_cell[0] * CELL_SIZE + CELL_SIZE / 2 + self.image.get_height() * 1/8 + TABLE_POSITION_Y])
            else:
                list_of_cells = []
                for row_index in range(11):
                    for column_index in range(11):
                        if player_grid[row_index][column_index] == 3:
                            list_of_cells.append([column_index, row_index])
                if game_battle_running and self.position == "horizontal":
                    if self.position_computer == "vertical":
                        self.image = pg.transform.rotate(self.image, 270)
                        self.rect = self.image.get_rect(center = [1065, 365])
                        self.position_computer = None
                    center_cell = list_of_cells[2]
                    self.rect.center = tuple([center_cell[0] * CELL_SIZE + CELL_SIZE / 2 - self.image.get_width() * 1/8 + TABLE_POSITION_X_MAIN_BATTLE_COMPUTER_TURN, center_cell[1] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_Y])                
                elif self.position == "horizontal":
                    center_cell = list_of_cells[2]
                    self.rect.center = tuple([center_cell[0] * CELL_SIZE + CELL_SIZE / 2 - self.image.get_width() * 1/8 + TABLE_POSITION_X, center_cell[1] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_Y])   
                elif game_battle_running and self.position == "vertical":
                    if self.position_computer == "horizontal":
                        self.image = pg.transform.rotate(self.image, 90)
                        self.rect = self.image.get_rect(center = [1170, 350])
                        self.position_computer = None
                    center_cell = list_of_cells[1]
                    self.rect.center = tuple([center_cell[0] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_X_MAIN_BATTLE_COMPUTER_TURN, center_cell[1] * CELL_SIZE + CELL_SIZE / 2 + self.image.get_height() * 1/8 + TABLE_POSITION_Y])
                else:
                    center_cell = list_of_cells[1]
                    self.rect.center = tuple([center_cell[0] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_X, center_cell[1] * CELL_SIZE + CELL_SIZE / 2 + self.image.get_height() * 1/8 + TABLE_POSITION_Y])
        elif selected_ship == "destroyer" and self.position == "horizontal":
            self.rect.center = tuple([mouse_position[0] - self.image.get_width() * 1/8, mouse_position[1]])
        elif selected_ship == "destroyer" and self.position == "vertical":
            self.rect.center = tuple([mouse_position[0], mouse_position[1] + self.image.get_height() * 1/8])
        elif any(3 in row for row in player_grid) == False and selected_ship != "destroyer" and self.position == "horizontal" and game_battle_running == False:
            self.rect = self.image.get_rect(center = [1065, 365])
        elif any(3 in row for row in player_grid) == False and selected_ship != "destroyer" and self.position == "vertical" and game_battle_running == False:
            self.rect = self.image.get_rect(center = [1170, 350])


class Frigate(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(path.join(path.join(path.dirname(__file__), "Images"), "frigate.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = [1030, 480]
        self.position = "horizontal"
        self.position_computer = None

    def update(self, rotate_ship, selected_ship, mouse_position, player_grid, game_battle_running, computer_turn, missile_position_y, missile_on, computer_grid, computer_ships_sunk):
        if game_battle_running == False and computer_turn == False and (rotate_ship == "frigate" or (self.position == "horizontal" and (TABLE_POSITION_X + CELL_SIZE > self.rect.center[0] or self.rect.center[0] > TABLE_POSITION_X - CELL_SIZE + TABLE_SIZE \
            or TABLE_POSITION_Y > self.rect.center[1] or self.rect.center[1] > TABLE_POSITION_Y + TABLE_SIZE)) or (self.position == "vertical" and (TABLE_POSITION_X > self.rect.center[0] \
            or self.rect.center[0] > TABLE_POSITION_X + TABLE_SIZE or TABLE_POSITION_Y + CELL_SIZE > self.rect.center[1] or self.rect.center[1] > TABLE_POSITION_Y - CELL_SIZE + TABLE_SIZE))):
            for row_index in range(11):
                for column_index in range(11):
                    if player_grid[row_index][column_index] == 2:
                        player_grid[row_index][column_index] = 0

        if rotate_ship == "frigate" and self.position == "horizontal":
            self.position = "vertical"
            self.image = pg.transform.rotate(self.image, 90)
            self.rect = self.image.get_rect(center = [1260, 480])
        elif rotate_ship == "frigate" and self.position == "vertical":
            self.position = "horizontal"
            self.image = pg.transform.rotate(self.image, 270)
            self.rect = self.image.get_rect(center = [1030, 480])
        elif selected_ship != "frigate" and any(2 in row for row in player_grid) and rotate_ship != "frigate":
            if game_battle_running and computer_turn == False:
                list_of_cells = []
                for row_index in range(11):
                    for column_index in range(11):
                        if computer_grid[row_index][column_index] == 2:
                            list_of_cells.append([column_index, row_index])
                center_cell = list_of_cells[1]
                if 2 not in computer_ships_sunk:
                    self.rect.center = tuple([center_cell[0] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_X_MAIN_BATTLE - SCREEN_WIDTH, center_cell[1] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_Y])
                elif center_cell[0] == list_of_cells[2][0]:
                    if self.position == "vertical" and self.position_computer == None:
                        self.image = pg.transform.rotate(self.image, 270)
                        self.rect = self.image.get_rect(center = [1030, 480])
                        self.position_computer = "horizontal"
                    self.rect.center = tuple([center_cell[1] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_X_MAIN_BATTLE, center_cell[0] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_Y])
                else:
                    if self.position == "horizontal" and self.position_computer == None:
                        self.image = pg.transform.rotate(self.image, 90)
                        self.rect = self.image.get_rect(center = [1260, 480])
                        self.position_computer = "vertical"
                    self.rect.center = tuple([center_cell[1] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_X_MAIN_BATTLE, center_cell[0] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_Y])
            else:
                list_of_cells = []
                for row_index in range(11):
                    for column_index in range(11):
                        if player_grid[row_index][column_index] == 2:
                            list_of_cells.append([column_index, row_index])
                center_cell = list_of_cells[1]
                if game_battle_running:
                    if self.position == "horizontal" and self.position_computer == "vertical":
                        self.image = pg.transform.rotate(self.image, 270)
                        self.rect = self.image.get_rect(center = [1030, 480])
                        self.position_computer = None
                    elif self.position == "vertical" and self.position_computer == "horizontal":
                        self.image = pg.transform.rotate(self.image, 90)
                        self.rect = self.image.get_rect(center = [1260, 480])
                        self.position_computer = None
                    self.rect.center = tuple([center_cell[0] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_X_MAIN_BATTLE_COMPUTER_TURN, center_cell[1] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_Y])
                else:
                    self.rect.center = tuple([center_cell[0] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_X, center_cell[1] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_Y])
        elif selected_ship == "frigate":
            self.rect.center = mouse_position
        elif any(2 in row for row in player_grid) == False and selected_ship != "frigate" and self.position == "horizontal" and game_battle_running == False:
            self.rect = self.image.get_rect(center = [1030, 480])
        elif any(2 in row for row in player_grid) == False and selected_ship != "frigate" and self.position == "vertical" and game_battle_running == False:
            self.rect = self.image.get_rect(center = [1260, 480])


class Submarine(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(path.join(path.join(path.dirname(__file__), "Images"), "submarine.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = [1015, 250]
        self.position = "horizontal"
        self.position_computer = None

    def update(self, rotate_ship, selected_ship, mouse_position, player_grid, game_battle_running, computer_turn, missile_position_y, missile_on, computer_grid, computer_ships_sunk):
        if game_battle_running == False and computer_turn == False and (rotate_ship == "submarine" or (self.position == "horizontal" and (TABLE_POSITION_X + CELL_SIZE > self.rect.center[0] or self.rect.center[0] > TABLE_POSITION_X - CELL_SIZE + TABLE_SIZE \
            or TABLE_POSITION_Y > self.rect.center[1] or self.rect.center[1] > TABLE_POSITION_Y + TABLE_SIZE)) or (self.position == "vertical" and (TABLE_POSITION_X > self.rect.center[0] \
            or self.rect.center[0] > TABLE_POSITION_X + TABLE_SIZE or TABLE_POSITION_Y + CELL_SIZE > self.rect.center[1] or self.rect.center[1] > TABLE_POSITION_Y - CELL_SIZE + TABLE_SIZE))):
            for row_index in range(11):
                for column_index in range(11):
                    if player_grid[row_index][column_index] == 1:
                        player_grid[row_index][column_index] = 0

        if rotate_ship == "submarine" and self.position == "horizontal":
            self.position = "vertical"
            self.image = pg.transform.rotate(self.image, 90)
            self.rect = self.image.get_rect(center = [1300, 250])
        elif rotate_ship == "submarine" and self.position == "vertical":
            self.position = "horizontal"
            self.image = pg.transform.rotate(self.image, 270)
            self.rect = self.image.get_rect(center = [1015, 250])
        elif selected_ship != "submarine" and any(1 in row for row in player_grid) and rotate_ship != "submarine":
            if game_battle_running and computer_turn == False:
                list_of_cells = []
                for row_index in range(11):
                    for column_index in range(11):
                        if computer_grid[row_index][column_index] == 1:
                            list_of_cells.append([column_index, row_index])
                center_cell = list_of_cells[1]
                if 1 not in computer_ships_sunk:
                    self.rect.center = tuple([center_cell[0] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_X_MAIN_BATTLE - SCREEN_WIDTH, center_cell[1] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_Y])
                elif center_cell[0] == list_of_cells[2][0]:
                    if self.position == "vertical" and self.position_computer == None:
                        self.image = pg.transform.rotate(self.image, 270)
                        self.rect = self.image.get_rect(center = [1015, 250])
                        self.position_computer = "horizontal"
                    self.rect.center = tuple([center_cell[1] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_X_MAIN_BATTLE, center_cell[0] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_Y])
                else:
                    if self.position == "horizontal" and self.position_computer == None:
                        self.image = pg.transform.rotate(self.image, 90)
                        self.rect = self.image.get_rect(center = [1300, 250])
                        self.position_computer = "vertical"
                    self.rect.center = tuple([center_cell[1] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_X_MAIN_BATTLE, center_cell[0] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_Y])
            else:
                list_of_cells = []
                for row_index in range(11):
                    for column_index in range(11):
                        if player_grid[row_index][column_index] == 1:
                            list_of_cells.append([column_index, row_index])
                center_cell = list_of_cells[1]
                if game_battle_running:
                    if self.position == "horizontal" and self.position_computer == "vertical":
                        self.image = pg.transform.rotate(self.image, 270)
                        self.rect = self.image.get_rect(center = [1015, 250])
                        self.position_computer = None
                    elif self.position == "vertical" and self.position_computer == "horizontal":
                        self.image = pg.transform.rotate(self.image, 90)
                        self.rect = self.image.get_rect(center = [1300, 250])
                        self.position_computer = None
                    self.rect.center = tuple([center_cell[0] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_X_MAIN_BATTLE_COMPUTER_TURN, center_cell[1] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_Y])
                else:
                    self.rect.center = tuple([center_cell[0] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_X, center_cell[1] * CELL_SIZE + CELL_SIZE / 2 + TABLE_POSITION_Y])
        elif selected_ship == "submarine":
            self.rect.center = mouse_position
        elif any(1 in row for row in player_grid) == False and selected_ship != "submarine" and self.position == "horizontal" and game_battle_running == False:
            self.rect = self.image.get_rect(center = [1015, 250])
        elif any(1 in row for row in player_grid) == False and selected_ship != "submarine" and self.position == "vertical" and game_battle_running == False:
            self.rect = self.image.get_rect(center = [1300, 250])


class RotationSign(pg.sprite.Sprite):
    def __init__(self, i):
        super().__init__()
        self.image = pg.image.load(path.join(path.join(path.dirname(__file__), "Images"), "rotation.png")).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = [850, 135 + i * 115]

    def update(self, rotate_ship, selected_ship, mouse_position, player_grid, game_battle_running, computer_turn, missile_position_y, missile_on, computer_grid, computer_ships_sunk):
        if game_battle_running:
            self.kill()    


class Missile(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(path.join(path.join(path.dirname(__file__), "Images"), "missile.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.missile_position = "horizontal"
        self.missile_speed_x = 10
        self.missile_position_x = 0

    def update(self, rotate_ship, selected_ship, mouse_position, player_grid, game_battle_running, computer_turn, missile_position_y, missile_on, computer_grid, computer_ships_sunk):
        if game_battle_running and computer_turn == False and missile_on == False:
            self.missile_position_x = -500
            if self.missile_position == "vertical":
                self.image = pg.transform.rotate(self.image, 180)
                self.missile_position = "horizontal"
        elif game_battle_running and computer_turn and missile_on == False:
            self.missile_position_x = 2000
            if self.missile_position == "horizontal":
                self.image = pg.transform.rotate(self.image, 180)
                self.missile_position = "vertical"

        if game_battle_running and missile_on == False:
            self.rect.center = [-100, -100]
        elif game_battle_running and computer_turn == False and missile_on:
            self.missile_position_x += self.missile_speed_x
            self.rect.center = [self.missile_position_x, missile_position_y]
        elif game_battle_running and computer_turn and missile_on:
            self.missile_position_x -= self.missile_speed_x
            self.rect.center = [self.missile_position_x, missile_position_y]
                
        if game_battle_running == False:
            self.kill()
