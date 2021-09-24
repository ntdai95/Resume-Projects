import sys
from os import path
import pygame as pg
import random
import time
import pickle
from settings import *
from sprites import *


class PickleHighScore:
    def __init__(self, list_of_highscores):
        self.list_of_highscores = list_of_highscores


    def saving_highscore_pickle(self):
        with open(".highscores.pickle", "wb") as p:
            pickle.dump(self.list_of_highscores, p)

class Main:
    def __init__(self):
        pg.init()
        pg.mixer.music.load(path.join(path.join(path.dirname(__file__), "Music"), "background_music.wav"))
        pg.mixer.music.set_volume(0.4)
        self.explosion_sound = pg.mixer.Sound(path.join(path.join(path.dirname(__file__), "Music"), "explosion.wav"))
        self.rocket_sound = pg.mixer.Sound(path.join(path.join(path.dirname(__file__), "Music"), "rocket.wav"))
        self.ship_sound = pg.mixer.Sound(path.join(path.join(path.dirname(__file__), "Music"), "steamwhistle.wav"))
        self.water_splash_sound = pg.mixer.Sound(path.join(path.join(path.dirname(__file__), "Music"), "watersplash.wav"))
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.first_background = pg.image.load(path.join(path.join(path.dirname(__file__), "Images"), "first_background.png")).convert()
        self.main_battle_background = pg.image.load(path.join(path.join(path.dirname(__file__), "Images"), "main_battle_background.png")).convert()
        self.main_setup_background = pg.image.load(path.join(path.join(path.dirname(__file__), "Images"), "main_setup_background.png")).convert()
        self.main_battle_background_x = 0
        self.main_battle_background_x_2 = self.main_battle_background.get_width()
        self.game_over_background = pg.image.load(path.join(path.join(path.dirname(__file__), "Images"), "game_over_background.png")).convert()
        self.game_win_background = pg.image.load(path.join(path.join(path.dirname(__file__), "Images"), "game_win_background.png")).convert()
        pg.display.set_caption(TITLE)
        self.icon = pg.image.load(path.join(path.join(path.dirname(__file__), "Images"), "icon.png")).convert()
        self.icon.set_colorkey(BLACK)
        pg.display.set_icon(self.icon)
        self.clock = pg.time.Clock()
        self.reset()

    def reset(self):
        self.is_music_playing = True
        self.is_sound_playing = True
        self.game_open = True
        self.instruction_first_page = False
        self.instruction_second_page = False
        self.highscores_page = False
        self.game_setup_running = False
        self.game_battle_running = False
        self.game_ending_lose = False
        self.game_ending_win = False
        self.computer_turn = False
        self.mouse_position = None
        self.list_of_button_texts = ["START GAME", "INSTRUCTIONS", "HIGHSCORES", "MUSIC ON/OFF", "SOUND ON/OFF", "EXIT GAME"]
        self.list_of_button_positions_x = None
        self.list_of_button_positions_y = None
        self.buttons_size_x = None
        self.buttons_size_y = None
        self.refresh_button_size_x = 100
        self.refresh_button_size_y = 90
        self.list_of_ships = ["cruiser", "submarine", "destroyer", "frigate", "aircraftcarrier"]
        self.selected_ship = None
        self.rotate_ship = None
        self.selected_cell = None
        self.selected_cell_main_battle = None
        self.selected_cell_main_battle_computer_turn = None
        self.player_grid = [[0 for _ in range(11)] for _ in range(11)]
        self.computer_grid = [[0 for _ in range(11)] for _ in range(11)]
        self.player_entered_grid = [[0 for _ in range(11)] for _ in range(11)]
        self.computer_entered_grid = [[0 for _ in range(11)] for _ in range(11)]
        self.missile_on = False
        self.missile_x_border = 0
        self.missile_position_y = 0
        self.player_ships_sunk = 0
        self.computer_ships_sunk = []
        self.player_score = 0
        self.final_player_score = 0
        self.list_of_highscores = []
        self.final_player_score_in_highscores = None
        self.player_name = ""
        self.length_smallest_ship_alive = 3
        self.list_of_cells_to_select_for_computer = []
        for row in range(11):
            list_of_cells_to_select_in_row = []
            if row % 3 == 0:
                for column in range(3):
                    list_of_cells_to_select_in_row.append([row, column * 3 + 2 + row % 3, 0])
            else:
                for column in range(-1, 3):
                    list_of_cells_to_select_in_row.append([row, column * 3 + 2 + row % 3, 0])
            self.list_of_cells_to_select_for_computer.extend(list_of_cells_to_select_in_row)


### GAME START SCREEN ###

    def game_start_screen(self):
        pg.mixer.music.play(-1)
        while self.game_open:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game_open = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    for i in range(6):
                        if i == 0 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y: 
                            self.game_setup_running = True
                        elif i == 1 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            self.instruction_first_page = True
                        elif i == 2 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            self.highscores_page = True
                        elif i == 3 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            if self.is_music_playing:
                                pg.mixer.music.stop()
                                self.is_music_playing = False
                            else:
                                pg.mixer.music.play(-1)
                                self.is_music_playing = True
                        elif i == 4 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            if self.is_sound_playing:
                                self.is_sound_playing = False
                            else:
                                self.is_sound_playing = True
                        elif i == 5 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            self.game_open = False

            self.instructions_screen_first_page()
            self.highscores_screen()
            self.run_main_setup()
            self.screen.blit(self.first_background, (0, 0))
            self.initial_message_to_screen(self.screen)
            self.loading_buttons_on_first_page(self.screen, self.mouse_position, self.list_of_button_texts)

            pg.display.update()
            self.clock.tick(FPS)

        pg.quit()
        sys.exit()

    def initial_message_to_screen(self, screen):
        line_font = pg.font.Font('freesansbold.ttf', 60)
        line = line_font.render("Welcome to Oceanic Warfare!", True, YELLOW)
        line_surface = pg.Surface(line.get_size())
        line_surface.fill(BLACK)
        line_surface.blit(line, (0, 0))
        self.screen.blit(line_surface, (325, 150))

    def loading_buttons_on_first_page(self, screen, mouse_position, list_of_button_texts):
        self.mouse_position = pg.mouse.get_pos()
        self.list_of_button_positions_x = [100, 575, 1050, 100, 575, 1050]
        self.list_of_button_positions_y = [350, 350, 350, 550, 550, 550]
        self.buttons_size_x = 350
        self.buttons_size_y = 100

        # Button Texts
        for i in range(6):
            if self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y: 
                pg.draw.rect(self.screen, RED, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y])
                pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y], 5)
            else: 
                pg.draw.rect(self.screen, GREEN, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y])
                pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y], 5)

            font = pg.font.Font('freesansbold.ttf', 40)
            text_font = font.render(self.list_of_button_texts[i], True, BLACK)
            text_font_width = text_font.get_width()
            text_font_height = text_font.get_height()
            self.screen.blit(text_font, (self.list_of_button_positions_x[i] + (self.buttons_size_x - text_font_width) // 2, self.list_of_button_positions_y[i] + (self.buttons_size_y - text_font_height) // 2))

### HIGHSCORES PAGE ###

    def highscores_screen(self):
        try:
            with open(".highscores.pickle", "rb") as p:
                pickle_objects = pickle.load(p)
            self.list_of_highscores = pickle_objects
            self.list_of_highscores.sort(reverse = True, key = lambda x: x[1])
        except EOFError:
            self.list_of_highscores = []

        while self.highscores_page:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.highscores_page = False
                    self.game_open = False
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    for i in range(4):
                        if i == 0 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            self.list_of_highscores = []
                            instance_of_PickleHighScore = PickleHighScore(self.list_of_highscores)
                            instance_of_PickleHighScore.saving_highscore_pickle()
                        elif i == 2 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            self.highscores_page = False

            self.screen.blit(self.first_background, (0, 0))
            self.highscores_message_to_screen(self.screen)
            self.loading_buttons_on_highscores_page(self.screen, self.mouse_position, self.list_of_button_texts, self.buttons_size_x, self.buttons_size_y)

            if self.highscores_page == False and self.game_open:
                self.reset()

            pg.display.update()
            self.clock.tick(FPS)

    def highscores_message_to_screen(self, screen):
        first_line_font = pg.font.Font('freesansbold.ttf', 60)
        line_font = pg.font.Font('freesansbold.ttf', 40)
        list_of_messages = ["TOP 10 HIGHSCORES!"]
        for index, name_score in enumerate(self.list_of_highscores):
            name_score_message = f"{index + 1}. {name_score[0]} --> {name_score[1]} points"
            list_of_messages.append(name_score_message)
        for index, message in enumerate(list_of_messages):
            if index == 0:
                line = first_line_font.render(message, True, BLACK)
            else:
                line = line_font.render(message, True, BLACK)
            line_surface = pg.Surface(line.get_size())
            line_surface.fill(PINK)
            line_surface.blit(line, (0, 0))
            if index == 0:
                self.screen.blit(line_surface, (470, 20))
            elif index < 6:
                self.screen.blit(line_surface, (60, 60 + 100 * index))  
            else:
                self.screen.blit(line_surface, (800, 60 + 100 * (index - 5)))

    def loading_buttons_on_highscores_page(self, screen, mouse_position, list_of_button_texts, buttons_size_x, buttons_size_y):
        self.mouse_position = pg.mouse.get_pos()
        self.list_of_button_texts = ["DELETE", "ALL SCORES", "MAIN", "PAGE"]
        self.list_of_button_positions_x = [450, 450, 750, 750]
        self.list_of_button_positions_y = [665, 705, 665, 705]
        self.buttons_size_x = 290
        self.buttons_size_y = 110

        # Button Texts
        for i in range(4):
            if i % 2 == 0 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y: 
                pg.draw.rect(self.screen, RED, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y])
                pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y], 5)
            elif i % 2 == 0: 
                pg.draw.rect(self.screen, GREEN, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y])
                pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y], 5)

            font = pg.font.Font('freesansbold.ttf', 40)
            text_font = font.render(self.list_of_button_texts[i], True, BLACK)
            text_font_width = text_font.get_width()
            text_font_height = text_font.get_height()
            self.screen.blit(text_font, (self.list_of_button_positions_x[i] + (self.buttons_size_x - text_font_width) // 2, self.list_of_button_positions_y[i] + (self.buttons_size_y - text_font_height) // 4))

### INSTRUCTIONS PAGE ###

    def instructions_screen_first_page(self):
        while self.instruction_first_page:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.instruction_first_page = False
                    self.game_open = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    for i in range(4):
                        if i == 0 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            self.instruction_second_page = True
                        elif i == 2 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            self.instruction_first_page = False

            self.instructions_screen_second_page()
            self.screen.blit(self.first_background, (0, 0))
            self.instruction_message_to_screen_first_page(self.screen)
            self.loading_buttons_on_instruction_first_page(self.screen, self.mouse_position, self.list_of_button_texts, self.buttons_size_x, self.buttons_size_y)

            if self.instruction_first_page == False and self.game_open:
                self.reset()

            pg.display.update()
            self.clock.tick(FPS)
    
    def instruction_message_to_screen_first_page(self, screen):
        first_line_font = pg.font.Font('freesansbold.ttf', 50)
        line_font = pg.font.Font('freesansbold.ttf', 30)
        list_of_messages = ["Instructions (page 1)!",
        "In this classic battleship game, there are five ships that you need to sunk in order to win with the",
        "following widths and heights: Cruiser (5x1 squares), Aircraft Carrier (4x2 squares),",
        "Destroyer (4x1 squares), Frigate (3x1 squares), and Submarine (3x1 squares).",
        "During the set up, you can grab the ship from the right side of the window, and then place it on the",
        "grid. The valid placement of the ship will be shown on the grid with filled pink cells around the ship.",
        "If the placement of the ship is not valid, then the ship will return to its original position on the right",
        "side of the window.",
        "If you wish to change the orientation of the ship from horizontal to vertical and vice",
        "versa, you can click on the rotation sign (located in a yellow square on the right side of the grid) to",
        "change the orientation of the ship, which is originally located next to the clicked rotation sign.",
        "Note that if you rotate the ship that has been placed on the grid, the ship will be rotated and placed",
        "at its original position (on the right side of the window). Thus, you need to place it again on the grid.",
        "You won't be able to move on to the battle phase until you place all the five ships on the grid."]
        for index, message in enumerate(list_of_messages):
            if index == 0:
                line = first_line_font.render(message, True, BLACK)
            else:
                line = line_font.render(message, True, BLACK)
            line_surface = pg.Surface(line.get_size())
            line_surface.fill(PINK)
            line_surface.blit(line, (0, 0))
            if index == 0:
                self.screen.blit(line_surface, (470, 20))
            elif index < 4:
                self.screen.blit(line_surface, (20, 100 + 30 * index))
            elif 4 <= index < 11:
                self.screen.blit(line_surface, (20, 140 + 30 * index))    
            else:
                self.screen.blit(line_surface, (20, 180 + 30 * index))

    def loading_buttons_on_instruction_first_page(self, screen, mouse_position, list_of_button_texts, buttons_size_x, buttons_size_y):
        self.mouse_position = pg.mouse.get_pos()
        self.list_of_button_texts = ["NEXT", "PAGE", "MAIN", "PAGE"]
        self.list_of_button_positions_x = [560, 560, 740, 740]
        self.list_of_button_positions_y = [665, 705, 665, 705]
        self.buttons_size_x = 170
        self.buttons_size_y = 110

        # Button Texts
        for i in range(4):
            if i % 2 == 0 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y: 
                pg.draw.rect(self.screen, RED, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y])
                pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y], 5)
            elif i % 2 == 0: 
                pg.draw.rect(self.screen, GREEN, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y])
                pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y], 5)

            font = pg.font.Font('freesansbold.ttf', 40)
            text_font = font.render(self.list_of_button_texts[i], True, BLACK)
            text_font_width = text_font.get_width()
            text_font_height = text_font.get_height()
            self.screen.blit(text_font, (self.list_of_button_positions_x[i] + (self.buttons_size_x - text_font_width) // 2, self.list_of_button_positions_y[i] + (self.buttons_size_y - text_font_height) // 4))

    def instructions_screen_second_page(self):
        while self.instruction_second_page:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.instruction_second_page = False
                    self.instruction_first_page = False
                    self.game_open = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    for i in range(4):
                        if i == 0 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            self.instruction_second_page = False
                        elif i == 2 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            self.instruction_second_page = False
                            self.instruction_first_page = False

            self.screen.blit(self.first_background, (0, 0))
            self.instruction_message_to_screen_second_page(self.screen)
            self.loading_buttons_on_instruction_second_page(self.screen, self.mouse_position, self.list_of_button_texts, self.buttons_size_x, self.buttons_size_y)

            pg.display.update()
            self.clock.tick(FPS)
    
    def instruction_message_to_screen_second_page(self, screen):
        first_line_font = pg.font.Font('freesansbold.ttf', 50)
        line_font = pg.font.Font('freesansbold.ttf', 30)
        list_of_messages = ["Instructions (page 2)!",
        "In the battle phase, you can select a cell to launch a rocket on it. If the rocket hits the ship, then the",
        "cell will be filled with red color. Otherwise, the selected cell will be filled with grey color.",
        "If you manage to hit every part of the ship, then the ship will be sunk and will be shown up on the grid.", 
        "Whoever manages to sunk all the opponent's five ships first will win the game.",
        "For scoring, you will get 5 points minus everytime when your rocket does not hit a ship and",
        "30 points plus otherwise. In addition, for every ship sunk, you will get 50 points plus.",
        "However, if the computer manages to hit your ship, then you will get 10 points",
        "minus and additional 40 points minus for every ship that the computer manages to sunk.",
        "You can only save your score if you win the game and your score is among the top 10 highscores."]
        for index, message in enumerate(list_of_messages):
            if index == 0:
                line = first_line_font.render(message, True, BLACK)
            else:
                line = line_font.render(message, True, BLACK)
            line_surface = pg.Surface(line.get_size())
            line_surface.fill(PINK)
            line_surface.blit(line, (0, 0))
            if index == 0:
                self.screen.blit(line_surface, (470, 20))
            elif index < 5:
                self.screen.blit(line_surface, (20, 150 + 30 * index))
            else:
                self.screen.blit(line_surface, (20, 250 + 30 * index))

    def loading_buttons_on_instruction_second_page(self, screen, mouse_position, list_of_button_texts, buttons_size_x, buttons_size_y):
        self.mouse_position = pg.mouse.get_pos()
        self.list_of_button_texts = ["GO", "BACK", "MAIN", "PAGE"]
        self.list_of_button_positions_x = [560, 560, 740, 740]
        self.list_of_button_positions_y = [665, 705, 665, 705]
        self.buttons_size_x = 170
        self.buttons_size_y = 110

        # Button Texts
        for i in range(4):
            if i % 2 == 0 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y: 
                pg.draw.rect(self.screen, RED, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y])
                pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y], 5)
            elif i % 2 == 0: 
                pg.draw.rect(self.screen, GREEN, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y])
                pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y], 5)

            font = pg.font.Font('freesansbold.ttf', 40)
            text_font = font.render(self.list_of_button_texts[i], True, BLACK)
            text_font_width = text_font.get_width()
            text_font_height = text_font.get_height()
            self.screen.blit(text_font, (self.list_of_button_positions_x[i] + (self.buttons_size_x - text_font_width) // 2, self.list_of_button_positions_y[i] + (self.buttons_size_y - text_font_height) // 4))

### GAME MAIN SETUP SCREEN ###

    def loading_sprites_main_setup(self, screen):
        self.all_sprites_group = pg.sprite.Group()
        self.frigate = Frigate()
        self.all_sprites_group.add(self.frigate)
        self.aircraftcarrier = AircraftCarrier()
        self.all_sprites_group.add(self.aircraftcarrier)
        self.cruiser = Cruiser()
        self.all_sprites_group.add(self.cruiser)
        self.destroyer = Destroyer()
        self.all_sprites_group.add(self.destroyer)
        self.submarine = Submarine()
        self.all_sprites_group.add(self.submarine)
        self.rotation_sign = []
        for i in range(5):
            self.rotation_sign.append(RotationSign(i))
            self.all_sprites_group.add(self.rotation_sign[i])

    def run_main_setup(self):
        self.loading_sprites_main_setup(self.screen)
        while self.game_setup_running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game_setup_running = False
                    self.game_open = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    for i in range(13):
                        if i == 0 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y \
                        and any(5 in row for row in self.player_grid) and any(4 in row for row in self.player_grid) and any(3 in row for row in self.player_grid) and any(2 in row for row in self.player_grid) and any(1 in row for row in self.player_grid): 
                            self.generating_computer_ships(self.player_entered_grid)
                            self.game_battle_running = True
                        elif i == 2 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            if self.is_sound_playing:
                                self.is_sound_playing = False
                            else:
                                self.is_sound_playing = True
                        elif i == 4 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            self.game_setup_running = False
                        elif i == 6 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            self.game_setup_running = False
                            self.game_open = False
                        elif i >= 8 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.refresh_button_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.refresh_button_size_y:
                            self.rotate_ship = self.list_of_ships[i - 8]
                    
                    for ship in self.all_sprites_group:
                        if ship == self.cruiser and ship.rect.collidepoint(event.pos):
                            self.selected_ship = self.list_of_ships[0]
                            if any(5 in row for row in self.player_grid):
                                for row_index in range(11):
                                    for column_index in range(11):
                                        if self.player_grid[row_index][column_index] == 5:
                                            self.player_grid[row_index][column_index] = 0
                        elif ship == self.submarine and ship.rect.collidepoint(event.pos):
                            self.selected_ship = self.list_of_ships[1]
                            if any(1 in row for row in self.player_grid):
                                for row_index in range(11):
                                    for column_index in range(11):
                                        if self.player_grid[row_index][column_index] == 1:
                                            self.player_grid[row_index][column_index] = 0
                        elif ship == self.destroyer and ship.rect.collidepoint(event.pos):
                            self.selected_ship = self.list_of_ships[2]
                            if any(3 in row for row in self.player_grid):
                                for row_index in range(11):
                                    for column_index in range(11):
                                        if self.player_grid[row_index][column_index] == 3:
                                            self.player_grid[row_index][column_index] = 0
                        elif ship == self.frigate and ship.rect.collidepoint(event.pos):
                            self.selected_ship = self.list_of_ships[3]
                            if any(2 in row for row in self.player_grid):
                                for row_index in range(11):
                                    for column_index in range(11):
                                        if self.player_grid[row_index][column_index] == 2:
                                            self.player_grid[row_index][column_index] = 0
                        elif ship == self.aircraftcarrier and ship.rect.collidepoint(event.pos):
                            self.selected_ship = self.list_of_ships[4]
                            if any(4 in row for row in self.player_grid):
                                for row_index in range(11):
                                    for column_index in range(11):
                                        if self.player_grid[row_index][column_index] == 4:
                                            self.player_grid[row_index][column_index] = 0
            
                if event.type == pg.MOUSEBUTTONUP and self.selected_ship != None:
                    if self.selected_ship == "cruiser" and self.cruiser.position == "horizontal" and 1 < self.selected_cell[0] < 9 and self.player_grid[self.selected_cell[1]][self.selected_cell[0] - 2] == 0 \
                    and self.player_grid[self.selected_cell[1]][self.selected_cell[0] - 1] == 0 and self.player_grid[self.selected_cell[1]][self.selected_cell[0]] == 0 \
                    and self.player_grid[self.selected_cell[1]][self.selected_cell[0] + 1] == 0 and self.player_grid[self.selected_cell[1]][self.selected_cell[0] + 2] == 0:
                        for i in range(5):
                            self.player_grid[self.selected_cell[1]][self.selected_cell[0] - 2 + i] = 5
                        if self.is_sound_playing:
                            self.ship_sound.play()
                    elif self.selected_ship == "cruiser" and self.cruiser.position == "vertical" and 1 < self.selected_cell[1] < 9 and self.player_grid[self.selected_cell[1] - 2][self.selected_cell[0]] == 0 \
                    and self.player_grid[self.selected_cell[1] - 1][self.selected_cell[0]] == 0 and self.player_grid[self.selected_cell[1]][self.selected_cell[0]] == 0 \
                    and self.player_grid[self.selected_cell[1] + 1][self.selected_cell[0]] == 0 and self.player_grid[self.selected_cell[1] + 2][self.selected_cell[0]] == 0:
                        for i in range(5):
                            self.player_grid[self.selected_cell[1] - 2 + i][self.selected_cell[0]] = 5
                        if self.is_sound_playing:
                            self.ship_sound.play()
                    elif self.selected_ship == "aircraftcarrier" and self.aircraftcarrier.position == "horizontal" and 1 < self.selected_cell[0] < 10 and self.selected_cell[1] < 10 \
                    and self.player_grid[self.selected_cell[1]][self.selected_cell[0] - 2] == 0 and self.player_grid[self.selected_cell[1]][self.selected_cell[0] - 1] == 0 \
                    and self.player_grid[self.selected_cell[1]][self.selected_cell[0]] == 0 and self.player_grid[self.selected_cell[1]][self.selected_cell[0] + 1] == 0 \
                    and self.player_grid[self.selected_cell[1] + 1][self.selected_cell[0] - 2] == 0 and self.player_grid[self.selected_cell[1] + 1][self.selected_cell[0] - 1] == 0 \
                    and self.player_grid[self.selected_cell[1] + 1][self.selected_cell[0]] == 0 and self.player_grid[self.selected_cell[1] + 1][self.selected_cell[0] + 1] == 0:
                        for i in range(4):
                            self.player_grid[self.selected_cell[1]][self.selected_cell[0] - 2 + i] = 4
                            self.player_grid[self.selected_cell[1] + 1][self.selected_cell[0] - 2 + i] = 4
                        if self.is_sound_playing:
                            self.ship_sound.play()
                    elif self.selected_ship == "aircraftcarrier" and self.aircraftcarrier.position == "vertical" and self.selected_cell[0] < 10 and 0 < self.selected_cell[1] < 9 \
                    and self.player_grid[self.selected_cell[1] - 1][self.selected_cell[0] + 1] == 0 and self.player_grid[self.selected_cell[1] - 1][self.selected_cell[0]] == 0 \
                    and self.player_grid[self.selected_cell[1]][self.selected_cell[0] + 1] == 0 and self.player_grid[self.selected_cell[1]][self.selected_cell[0]] == 0 \
                    and self.player_grid[self.selected_cell[1] + 1][self.selected_cell[0] + 1] == 0 and self.player_grid[self.selected_cell[1] + 1][self.selected_cell[0]] == 0 \
                    and self.player_grid[self.selected_cell[1] + 2][self.selected_cell[0] + 1] == 0 and self.player_grid[self.selected_cell[1] + 2][self.selected_cell[0]] == 0:
                        for i in range(4):
                            self.player_grid[self.selected_cell[1] - 1 + i][self.selected_cell[0]] = 4
                            self.player_grid[self.selected_cell[1] - 1 + i][self.selected_cell[0] + 1] = 4
                        if self.is_sound_playing:
                            self.ship_sound.play()
                    elif self.selected_ship == "destroyer" and self.destroyer.position == "horizontal" and 1 < self.selected_cell[0] < 10 \
                    and self.player_grid[self.selected_cell[1]][self.selected_cell[0] - 2] == 0 and self.player_grid[self.selected_cell[1]][self.selected_cell[0] - 1] == 0 \
                    and self.player_grid[self.selected_cell[1]][self.selected_cell[0]] == 0 and self.player_grid[self.selected_cell[1]][self.selected_cell[0] + 1] == 0:
                        for i in range(4):
                            self.player_grid[self.selected_cell[1]][self.selected_cell[0] - 2 + i] = 3
                        if self.is_sound_playing:
                            self.ship_sound.play()
                    elif self.selected_ship == "destroyer" and self.destroyer.position == "vertical" and 0 < self.selected_cell[1] < 9 \
                    and self.player_grid[self.selected_cell[1] - 1][self.selected_cell[0]] == 0 and self.player_grid[self.selected_cell[1]][self.selected_cell[0]] == 0 \
                    and self.player_grid[self.selected_cell[1] + 1][self.selected_cell[0]] == 0 and self.player_grid[self.selected_cell[1] + 2][self.selected_cell[0]] == 0:
                        for i in range(4):
                            self.player_grid[self.selected_cell[1] - 1 + i][self.selected_cell[0]] = 3
                        if self.is_sound_playing:
                            self.ship_sound.play()
                    elif self.selected_ship == "frigate" and self.frigate.position == "horizontal" and 0 < self.selected_cell[0] < 10 and self.player_grid[self.selected_cell[1]][self.selected_cell[0] - 1] == 0 \
                    and self.player_grid[self.selected_cell[1]][self.selected_cell[0]] == 0 and self.player_grid[self.selected_cell[1]][self.selected_cell[0] + 1] == 0:
                        for i in range(3):
                            self.player_grid[self.selected_cell[1]][self.selected_cell[0] - 1 + i] = 2
                        if self.is_sound_playing:
                            self.ship_sound.play()
                    elif self.selected_ship == "frigate" and self.frigate.position == "vertical" and 0 < self.selected_cell[1] < 10 and self.player_grid[self.selected_cell[1] - 1][self.selected_cell[0]] == 0 \
                    and self.player_grid[self.selected_cell[1]][self.selected_cell[0]] == 0 and self.player_grid[self.selected_cell[1] + 1][self.selected_cell[0]] == 0:
                        for i in range(3):
                            self.player_grid[self.selected_cell[1] - 1 + i][self.selected_cell[0]] = 2
                        if self.is_sound_playing:
                            self.ship_sound.play()
                    elif self.selected_ship == "submarine" and self.submarine.position == "horizontal" and 0 < self.selected_cell[0] < 10 and self.player_grid[self.selected_cell[1]][self.selected_cell[0] - 1] == 0 \
                    and self.player_grid[self.selected_cell[1]][self.selected_cell[0]] == 0 and self.player_grid[self.selected_cell[1]][self.selected_cell[0] + 1] == 0:
                        for i in range(3):
                            self.player_grid[self.selected_cell[1]][self.selected_cell[0] - 1 + i] = 1
                        if self.is_sound_playing:
                            self.ship_sound.play()
                    elif self.selected_ship == "submarine" and self.submarine.position == "vertical" and 0 < self.selected_cell[1] < 10 and self.player_grid[self.selected_cell[1] - 1][self.selected_cell[0]] == 0 \
                    and self.player_grid[self.selected_cell[1]][self.selected_cell[0]] == 0 and self.player_grid[self.selected_cell[1] + 1][self.selected_cell[0]] == 0:
                        for i in range(3):
                            self.player_grid[self.selected_cell[1] - 1 + i][self.selected_cell[0]] = 1
                        if self.is_sound_playing:
                            self.ship_sound.play()

                    self.selected_ship = None

            if TABLE_POSITION_X <= self.mouse_position[0] <= TABLE_POSITION_X + TABLE_SIZE and TABLE_POSITION_Y <= self.mouse_position[1] <= TABLE_POSITION_Y + TABLE_SIZE:
                self.selected_cell = [(self.mouse_position[0] - TABLE_POSITION_X) // CELL_SIZE, (self.mouse_position[1] - TABLE_POSITION_Y) // CELL_SIZE]
            
            self.run_main_battle()
            self.update_main_setup(self.rotate_ship, self.selected_ship, self.mouse_position, self.player_grid, self.game_battle_running, self.computer_turn, self.missile_position_y, self.missile_on)
            self.draw_main_setup()

            if self.game_setup_running == False and self.game_open:
                self.reset()

            pg.display.update()
            self.clock.tick(FPS)

    def generating_computer_ships(self, player_entered_grid):
        computer_ship_sizes = [[3, 1], [3, 1], [4, 1], [4, 2], [5, 1]]
        for index, computer_ship_size in enumerate(computer_ship_sizes):
            valid = False
            while not valid:
                computer_ship_x = random.randint(0, 10)
                computer_ship_y = random.randint(0, 10)
                computer_ship_position = random.choice(["horizontal", "vertical"])
                valid = self.validate(self.player_entered_grid, computer_ship_size, computer_ship_x, computer_ship_y, computer_ship_position)

            if computer_ship_position == "horizontal":
                for j in range(computer_ship_size[1]):
                    for i in range(computer_ship_size[0]):
                        self.player_entered_grid[computer_ship_y + j][computer_ship_x + i] = index + 1
            else:
                for j in range(computer_ship_size[1]):
                    for i in range(computer_ship_size[0]):
                        self.player_entered_grid[computer_ship_y + i][computer_ship_x + j] = index + 1

    def validate(self, player_entered_grid, computer_ship_size, computer_ship_x, computer_ship_y, computer_ship_position):
        if computer_ship_position == "horizontal" and (computer_ship_x + computer_ship_size[0] > 10 or computer_ship_y + computer_ship_size[1] > 10):
            return False
        elif computer_ship_position == "vertical" and (computer_ship_x + computer_ship_size[1] > 10 or computer_ship_y + computer_ship_size[0] > 10):
            return False
        elif computer_ship_position == "horizontal":
            for j in range(computer_ship_size[1]):
                for i in range(computer_ship_size[0]):
                    if self.player_entered_grid[computer_ship_y + j][computer_ship_x + i] != 0:
                        return False
        elif computer_ship_position == "vertical":
            for j in range(computer_ship_size[1]):
                for i in range(computer_ship_size[0]):
                    if self.player_entered_grid[computer_ship_y + i][computer_ship_x + j] != 0:
                        return False
        return True

    def update_main_setup(self, rotate_ship, selected_ship, mouse_position, player_grid, game_battle_running, computer_turn, missile_position_y, missile_on):
        self.all_sprites_group.update(self.rotate_ship, self.selected_ship, self.mouse_position, self.player_grid, self.game_battle_running, self.computer_turn, self.missile_position_y, self.missile_on, self.computer_grid, self.computer_ships_sunk)
        self.rotate_ship = False

    def draw_main_setup(self):
        self.screen.blit(self.main_setup_background, (0, 0))
        self.message_to_screen_main_setup(self.screen)
        self.loading_buttons_on_main_setup(self.screen, self.mouse_position, self.list_of_button_texts, self.buttons_size_x, self.buttons_size_y)
        self.selected_cell_fill(self.screen)
        self.table_cell_draw_main_setup(self.screen)
        self.all_sprites_group.draw(self.screen)

    def selected_cell_fill(self, screen):
        for row_index in range(11):
            for column_index in range(11):
                if self.player_grid[row_index][column_index] != 0:
                    pg.draw.rect(self.screen, PINK, (column_index * CELL_SIZE + TABLE_POSITION_X, row_index * CELL_SIZE + TABLE_POSITION_Y, CELL_SIZE, CELL_SIZE))

        if self.selected_ship == "cruiser" and self.cruiser.position == "horizontal" and TABLE_POSITION_X + 2 * CELL_SIZE < self.mouse_position[0] < TABLE_POSITION_X - 2 * CELL_SIZE + TABLE_SIZE and TABLE_POSITION_Y < self.mouse_position[1] < TABLE_POSITION_Y + TABLE_SIZE:
            pg.draw.rect(self.screen, PINK, ((self.selected_cell[0] - 2) * CELL_SIZE + TABLE_POSITION_X, self.selected_cell[1] * CELL_SIZE + TABLE_POSITION_Y, 5 * CELL_SIZE, CELL_SIZE))
        elif self.selected_ship == "cruiser" and self.cruiser.position == "vertical" and TABLE_POSITION_X < self.mouse_position[0] < TABLE_POSITION_X + TABLE_SIZE and TABLE_POSITION_Y + 2 * CELL_SIZE < self.mouse_position[1] < TABLE_POSITION_Y - 2 * CELL_SIZE + TABLE_SIZE:
            pg.draw.rect(self.screen, PINK, (self.selected_cell[0] * CELL_SIZE + TABLE_POSITION_X, (self.selected_cell[1] - 2) * CELL_SIZE + TABLE_POSITION_Y, CELL_SIZE, 5 * CELL_SIZE))
        elif self.selected_ship == "aircraftcarrier" and self.aircraftcarrier.position == "horizontal" and TABLE_POSITION_X + 2 * CELL_SIZE < self.mouse_position[0] < TABLE_POSITION_X - CELL_SIZE + TABLE_SIZE and TABLE_POSITION_Y < self.mouse_position[1] < TABLE_POSITION_Y - CELL_SIZE + TABLE_SIZE:
            pg.draw.rect(self.screen, PINK, ((self.selected_cell[0] - 2) * CELL_SIZE + TABLE_POSITION_X, self.selected_cell[1] * CELL_SIZE + TABLE_POSITION_Y, 4 * CELL_SIZE, 2 * CELL_SIZE))
        elif self.selected_ship == "aircraftcarrier" and self.aircraftcarrier.position == "vertical" and TABLE_POSITION_X < self.mouse_position[0] < TABLE_POSITION_X - CELL_SIZE + TABLE_SIZE and TABLE_POSITION_Y + CELL_SIZE < self.mouse_position[1] < TABLE_POSITION_Y - 2 * CELL_SIZE + TABLE_SIZE:
            pg.draw.rect(self.screen, PINK, (self.selected_cell[0] * CELL_SIZE + TABLE_POSITION_X, (self.selected_cell[1] - 1) * CELL_SIZE + TABLE_POSITION_Y, 2 * CELL_SIZE, 4 * CELL_SIZE))
        elif self.selected_ship == "destroyer" and self.destroyer.position == "horizontal" and TABLE_POSITION_X + 2 * CELL_SIZE < self.mouse_position[0] < TABLE_POSITION_X - CELL_SIZE + TABLE_SIZE and TABLE_POSITION_Y < self.mouse_position[1] < TABLE_POSITION_Y + TABLE_SIZE:
            pg.draw.rect(self.screen, PINK, ((self.selected_cell[0] - 2) * CELL_SIZE + TABLE_POSITION_X, self.selected_cell[1] * CELL_SIZE + TABLE_POSITION_Y, 4 * CELL_SIZE, CELL_SIZE))
        elif self.selected_ship == "destroyer" and self.destroyer.position == "vertical" and TABLE_POSITION_X < self.mouse_position[0] < TABLE_POSITION_X + TABLE_SIZE and TABLE_POSITION_Y + 2 * CELL_SIZE < self.mouse_position[1] < TABLE_POSITION_Y - CELL_SIZE + TABLE_SIZE:
            pg.draw.rect(self.screen, PINK, (self.selected_cell[0] * CELL_SIZE + TABLE_POSITION_X, (self.selected_cell[1] - 1) * CELL_SIZE + TABLE_POSITION_Y, CELL_SIZE, 4 * CELL_SIZE))
        elif self.selected_ship == "frigate" and self.frigate.position == "horizontal" and TABLE_POSITION_X + CELL_SIZE < self.mouse_position[0] < TABLE_POSITION_X - CELL_SIZE + TABLE_SIZE and TABLE_POSITION_Y < self.mouse_position[1] < TABLE_POSITION_Y + TABLE_SIZE:
            pg.draw.rect(self.screen, PINK, ((self.selected_cell[0] - 1) * CELL_SIZE + TABLE_POSITION_X, self.selected_cell[1] * CELL_SIZE + TABLE_POSITION_Y, 3 * CELL_SIZE, CELL_SIZE))
        elif self.selected_ship == "frigate" and self.frigate.position == "vertical" and TABLE_POSITION_X < self.mouse_position[0] < TABLE_POSITION_X + TABLE_SIZE and TABLE_POSITION_Y + CELL_SIZE < self.mouse_position[1] < TABLE_POSITION_Y - CELL_SIZE + TABLE_SIZE:
            pg.draw.rect(self.screen, PINK, (self.selected_cell[0] * CELL_SIZE + TABLE_POSITION_X, (self.selected_cell[1] - 1) * CELL_SIZE + TABLE_POSITION_Y, CELL_SIZE, 3 * CELL_SIZE))
        elif self.selected_ship == "submarine" and self.submarine.position == "horizontal" and TABLE_POSITION_X + CELL_SIZE < self.mouse_position[0] < TABLE_POSITION_X - CELL_SIZE + TABLE_SIZE and TABLE_POSITION_Y < self.mouse_position[1] < TABLE_POSITION_Y + TABLE_SIZE:
            pg.draw.rect(self.screen, PINK, ((self.selected_cell[0] - 1) * CELL_SIZE + TABLE_POSITION_X, self.selected_cell[1] * CELL_SIZE + TABLE_POSITION_Y, 3 * CELL_SIZE, CELL_SIZE))
        elif self.selected_ship == "submarine" and self.submarine.position == "vertical" and TABLE_POSITION_X < self.mouse_position[0] < TABLE_POSITION_X + TABLE_SIZE and TABLE_POSITION_Y + CELL_SIZE < self.mouse_position[1] < TABLE_POSITION_Y - CELL_SIZE + TABLE_SIZE:
            pg.draw.rect(self.screen, PINK, (self.selected_cell[0] * CELL_SIZE + TABLE_POSITION_X, (self.selected_cell[1] - 1) * CELL_SIZE + TABLE_POSITION_Y, CELL_SIZE, 3 * CELL_SIZE))

    def message_to_screen_main_setup(self, screen):
        line_font = pg.font.Font('freesansbold.ttf', 60)
        line = line_font.render("Battleship formation!", True, YELLOW)
        line_surface = pg.Surface(line.get_size())
        line_surface.fill(BLACK)
        line_surface.blit(line, (0, 0))
        self.screen.blit(line_surface, (825, 5))

    def table_cell_draw_main_setup(self, screen):
        pg.draw.rect(self.screen, BLACK, (TABLE_POSITION_X, TABLE_POSITION_Y, TABLE_SIZE, TABLE_SIZE), 5)
        for i in range(1, 11):
            pg.draw.line(self.screen, BLACK, (TABLE_POSITION_X + i * CELL_SIZE, TABLE_POSITION_Y), (TABLE_POSITION_X + i * CELL_SIZE, TABLE_POSITION_Y + TABLE_SIZE), 5)
            pg.draw.line(self.screen, BLACK, (TABLE_POSITION_X, TABLE_POSITION_Y + i * CELL_SIZE), (TABLE_POSITION_X + TABLE_SIZE, TABLE_POSITION_Y + i * CELL_SIZE), 5)

    def loading_buttons_on_main_setup(self, screen, mouse_position, list_of_button_texts, buttons_size_x, buttons_size_y):
        self.mouse_position = pg.mouse.get_pos()
        self.list_of_button_texts = ["START", "GAME", "SOUND", "ON/OFF", "MAIN", "PAGE", "EXIT", "GAME"]
        self.list_of_button_positions_x = [785, 785, 965, 965, 1145, 1145, 1325, 1325, 800, 800, 800, 800, 800]
        self.list_of_button_positions_y = [665, 705, 665, 705, 665, 705, 665, 705, 90, 205, 320, 435, 550]
        self.buttons_size_x = 170
        self.buttons_size_y = 110

        # Button Texts
        for i in range(13):
            if self.selected_ship == None and i < 8 and i % 2 == 0 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y: 
                pg.draw.rect(self.screen, RED, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y])
                pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y], 5)
            elif self.selected_ship == None and i >= 8 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.refresh_button_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.refresh_button_size_y:
                pg.draw.rect(self.screen, GREEN, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.refresh_button_size_x, self.refresh_button_size_y])
                pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.refresh_button_size_x, self.refresh_button_size_y], 5)
            elif i < 8 and i % 2 == 0: 
                pg.draw.rect(self.screen, GREEN, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y])
                pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y], 5)
            elif i >= 8:
                pg.draw.rect(self.screen, YELLOW, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.refresh_button_size_x, self.refresh_button_size_y])
                pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.refresh_button_size_x, self.refresh_button_size_y], 5)
            
        for i in range(8):
            font = pg.font.Font('freesansbold.ttf', 40)
            text_font = font.render(self.list_of_button_texts[i], True, BLACK)
            text_font_width = text_font.get_width()
            text_font_height = text_font.get_height()
            self.screen.blit(text_font, (self.list_of_button_positions_x[i] + (self.buttons_size_x - text_font_width) // 2, self.list_of_button_positions_y[i] + (self.buttons_size_y - text_font_height) // 4))

### GAME MAIN BATTLE SCREEN ###
    
    def game_ending_win_check(self):
        self.computer_ships_sunk = []
        for i in range(5):
            if sum(ship_type.count(i + 1) for ship_type in self.player_entered_grid) == 0:
                self.computer_ships_sunk.append(i + 1)

    def run_main_battle(self):
        self.missile = Missile()
        self.all_sprites_group.add(self.missile)
        for row_index, row in enumerate(self.player_grid):
            for column_index, column in enumerate(row):
                self.computer_entered_grid[row_index][column_index] = column

        for row_index, row in enumerate(self.player_entered_grid):
            for column_index, column in enumerate(row):
                self.computer_grid[row_index][column_index] = column

        while self.game_battle_running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game_battle_running = False
                    self.game_setup_running = False
                    self.game_open = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.missile_on == False:
                        self.selected_cell_main_battle = [(self.mouse_position[0] - TABLE_POSITION_X_MAIN_BATTLE) // CELL_SIZE, (self.mouse_position[1] - TABLE_POSITION_Y) // CELL_SIZE]
                    if TABLE_POSITION_X_MAIN_BATTLE > self.mouse_position[0] or self.mouse_position[0] > TABLE_POSITION_X_MAIN_BATTLE + TABLE_SIZE or TABLE_POSITION_Y > self.mouse_position[1] or self.mouse_position[1] > TABLE_POSITION_Y + TABLE_SIZE or \
                    self.player_entered_grid[self.selected_cell_main_battle[0]][self.selected_cell_main_battle[1]] ==  "miss" or self.player_entered_grid[self.selected_cell_main_battle[0]][self.selected_cell_main_battle[1]] ==  "hit":
                        self.selected_cell_main_battle = None
                    if self.is_sound_playing and self.selected_cell_main_battle != None:
                        self.rocket_sound.play()
                            
                    for i in range(6):
                        if i == 0 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            if self.is_sound_playing:
                                self.is_sound_playing = False
                            else:
                                self.is_sound_playing = True
                        elif i == 2 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            self.game_battle_running = False
                            self.game_setup_running = False
                        elif i == 4 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            self.game_battle_running = False
                            self.game_setup_running = False
                            self.game_open = False

            self.update_main_battle(self.rotate_ship, self.selected_ship, self.mouse_position, self.player_grid, self.game_battle_running, self.computer_turn, self.missile_position_y, self.missile_on)
            self.draw_main_battle()

            self.game_ending_win_check()
            if len(self.computer_ships_sunk) == 5:
                self.game_ending_win = True
                self.game_win_screen()

            if self.game_battle_running == False and self.game_setup_running == False and self.game_open:
                self.reset()

            pg.display.update()

            if self.missile_x_border != 0 and self.missile_on == False:
                time.sleep(1)
                self.computer_turn = True
                self.missile_x_border = 0
                self.run_main_battle_computer_turn()

            self.clock.tick(FPS)

    def update_main_battle(self, rotate_ship, selected_ship, mouse_position, player_grid, game_battle_running, computer_turn, missile_position_y, missile_on):
        if self.selected_cell_main_battle:
            self.missile_on = True
            self.missile_x_border = self.selected_cell_main_battle[0] * CELL_SIZE + TABLE_POSITION_X_MAIN_BATTLE + 1/2 * CELL_SIZE
            self.missile_position_y = self.selected_cell_main_battle[1] * CELL_SIZE + TABLE_POSITION_Y + 1/2 * CELL_SIZE

        if self.missile.rect.center[0] == self.missile_x_border and self.missile_on:
            self.missile_on = False
            self.selected_cell_main_battle = None
        
        self.all_sprites_group.update(self.rotate_ship, self.selected_ship, self.mouse_position, self.player_grid, self.game_battle_running, self.computer_turn, self.missile_position_y, self.missile_on, self.computer_grid, self.computer_ships_sunk)

    def draw_main_battle(self):
        self.main_battle_background_x += 0.5
        self.main_battle_background_x_2 += 0.5

        if self.main_battle_background_x > self.main_battle_background.get_width():
            self.main_battle_background_x = -self.main_battle_background.get_width()
        if self.main_battle_background_x_2 > self.main_battle_background.get_width():
            self.main_battle_background_x_2 = -self.main_battle_background.get_width()

        self.screen.blit(self.main_battle_background, (self.main_battle_background_x, 0))
        self.screen.blit(self.main_battle_background, (self.main_battle_background_x_2, 0))

        self.message_to_screen_main_battle(self.screen)
        self.selected_cell_fill_main_battle(self.screen, self.selected_cell_main_battle)
        self.table_cell_draw_main_battle(self.screen)
        self.loading_buttons_on_main_battle(self.screen, self.mouse_position, self.list_of_button_texts, self.buttons_size_x, self.buttons_size_y)
        self.all_sprites_group.draw(self.screen)

    def selected_cell_fill_main_battle(self, screen, selected_cell_main_battle):
        if self.missile.rect.center[0] == self.missile_x_border and self.selected_cell_main_battle != None and (self.player_entered_grid[self.selected_cell_main_battle[0]][self.selected_cell_main_battle[1]] != 0 and self.player_entered_grid[self.selected_cell_main_battle[0]][self.selected_cell_main_battle[1]] != "miss"):
            self.player_entered_grid[self.selected_cell_main_battle[0]][self.selected_cell_main_battle[1]] = "hit"
            self.player_score += 30
            if self.is_sound_playing:
                self.explosion_sound.play()
        elif self.missile.rect.center[0] == self.missile_x_border and self.selected_cell_main_battle != None and self.player_entered_grid[self.selected_cell_main_battle[0]][self.selected_cell_main_battle[1]] == 0:
            self.player_entered_grid[self.selected_cell_main_battle[0]][self.selected_cell_main_battle[1]] = "miss"
            self.player_score -= 5
            if self.is_sound_playing:
                self.water_splash_sound.play()

        for row_index, row in enumerate(self.player_entered_grid):
            for column_index, column in enumerate(row):
                if column == "hit":
                    pg.draw.rect(self.screen, RED, (row_index * CELL_SIZE + TABLE_POSITION_X_MAIN_BATTLE, column_index * CELL_SIZE + TABLE_POSITION_Y, CELL_SIZE, CELL_SIZE))
                elif column == "miss":
                    pg.draw.rect(self.screen, GREY, (row_index * CELL_SIZE + TABLE_POSITION_X_MAIN_BATTLE, column_index * CELL_SIZE + TABLE_POSITION_Y, CELL_SIZE, CELL_SIZE))

    def message_to_screen_main_battle(self, screen):
        line_font = pg.font.Font('freesansbold.ttf', 60)
        list_of_messages = ["Your turn!", f"Your score: {len(self.computer_ships_sunk) * 50 - self.player_ships_sunk * 30 + self.player_score}", "Computer's ships", f"sunk: {len(self.computer_ships_sunk)}/5"]
        for index, message in enumerate(list_of_messages):
            line = line_font.render(message, True, YELLOW)
            line_surface = pg.Surface(line.get_size())
            line_surface.fill(BLACK)
            line_surface.blit(line, (0, 0))
            if index == 0:
                self.screen.blit(line_surface, (1090, 20))
            elif index == 1:
                self.screen.blit(line_surface, (1010, 210))
            elif index == 2:
                self.screen.blit(line_surface, (970, 400))
            else:
                self.screen.blit(line_surface, (1100, 470))

    def table_cell_draw_main_battle(self, screen):
        pg.draw.rect(self.screen, BLACK, (TABLE_POSITION_X_MAIN_BATTLE, TABLE_POSITION_Y, TABLE_SIZE, TABLE_SIZE), 5)
        for i in range(1, 11):
            pg.draw.line(self.screen, BLACK, (TABLE_POSITION_X_MAIN_BATTLE + i * CELL_SIZE, TABLE_POSITION_Y), (TABLE_POSITION_X_MAIN_BATTLE + i * CELL_SIZE, TABLE_POSITION_Y + TABLE_SIZE), 5)
            pg.draw.line(self.screen, BLACK, (TABLE_POSITION_X_MAIN_BATTLE, TABLE_POSITION_Y + i * CELL_SIZE), (TABLE_POSITION_X_MAIN_BATTLE + TABLE_SIZE, TABLE_POSITION_Y + i * CELL_SIZE), 5)

    def loading_buttons_on_main_battle(self, screen, mouse_position, list_of_button_texts, buttons_size_x, buttons_size_y):
        self.mouse_position = pg.mouse.get_pos()
        self.list_of_button_texts = ["SOUND", "ON/OFF", "MAIN", "PAGE", "EXIT", "GAME"]
        self.list_of_button_positions_x = [965, 965, 1145, 1145, 1325, 1325]
        self.list_of_button_positions_y = [665, 705, 665, 705, 665, 705]
        self.buttons_size_x = 170
        self.buttons_size_y = 110

        # Button Texts
        for i in range(6):
            if i % 2 == 0 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y: 
                pg.draw.rect(self.screen, RED, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y])
                pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y], 5)
            elif i % 2 == 0: 
                pg.draw.rect(self.screen, GREEN, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y])
                pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y], 5)

            font = pg.font.Font('freesansbold.ttf', 40)
            text_font = font.render(self.list_of_button_texts[i], True, BLACK)
            text_font_width = text_font.get_width()
            text_font_height = text_font.get_height()
            self.screen.blit(text_font, (self.list_of_button_positions_x[i] + (self.buttons_size_x - text_font_width) // 2, self.list_of_button_positions_y[i] + (self.buttons_size_y - text_font_height) // 4))

        if self.selected_cell_main_battle == None and TABLE_POSITION_X_MAIN_BATTLE < self.mouse_position[0] < TABLE_POSITION_X_MAIN_BATTLE + TABLE_SIZE and TABLE_POSITION_Y < self.mouse_position[1] < TABLE_POSITION_Y + TABLE_SIZE:
            hovered_cell = [(self.mouse_position[0] - TABLE_POSITION_X_MAIN_BATTLE) // CELL_SIZE, (self.mouse_position[1] - TABLE_POSITION_Y) // CELL_SIZE]
            if isinstance(self.player_entered_grid[hovered_cell[0]][hovered_cell[1]], int):
                pg.draw.rect(self.screen, YELLOW, (hovered_cell[0] * CELL_SIZE + TABLE_POSITION_X_MAIN_BATTLE, hovered_cell[1] * CELL_SIZE + TABLE_POSITION_Y, CELL_SIZE, CELL_SIZE))

### GAME MAIN BATTLE COMPUTER TURN SCREEN ###

    def game_ending_lose_check(self):
        self.player_ships_sunk = 0
        for i in range(5):
            if sum(ship_type.count(i + 1) for ship_type in self.computer_entered_grid) == 0:
                self.player_ships_sunk += 1

    def computer_select_cell(self):
        ship_hit_but_not_sunk, next_cell_target = self.checking_ship_hit_but_not_sunk()

        if ship_hit_but_not_sunk:
            if self.computer_entered_grid[next_cell_target[0]][next_cell_target[1]] == 0:
                self.computer_entered_grid[next_cell_target[0]][next_cell_target[1]] = "miss"
            else:
                self.computer_entered_grid[next_cell_target[0]][next_cell_target[1]] = "hit"
                self.player_score -= 10

            self.selected_cell_main_battle_computer_turn = [next_cell_target[1], next_cell_target[0]]

        elif self.game_ending_lose == False:
            if any(1 in row for row in self.computer_entered_grid) == False and any(2 in row for row in self.computer_entered_grid) == False and (any(3 in row for row in self.computer_entered_grid) or any(4 in row for row in self.computer_entered_grid)):
                self.length_smallest_ship_alive = 4
            elif any(1 in row for row in self.computer_entered_grid) == False and any(2 in row for row in self.computer_entered_grid) == False and any(3 in row for row in self.computer_entered_grid) == False and any(4 in row for row in self.computer_entered_grid) == False:
                self.length_smallest_ship_alive = 5
                
            list_of_indexes_of_cells_to_delete = []
            for index, cell in enumerate(self.list_of_cells_to_select_for_computer):
                row = cell[0]
                column = cell[1]
                if isinstance(self.computer_entered_grid[row][column], int):
                    free_horizontal_cells_count = 1
                    free_vertical_cells_count = 1
                    not_found_hit_or_miss_cell_left = True
                    not_found_hit_or_miss_cell_right = True
                    not_found_hit_or_miss_cell_up = True
                    not_found_hit_or_miss_cell_down = True
                    for i in range(1, self.length_smallest_ship_alive):
                        if row - i >= 0 and not_found_hit_or_miss_cell_left and isinstance(self.computer_entered_grid[row - i][column], int):
                            free_horizontal_cells_count += 1
                        else:
                            not_found_hit_or_miss_cell_left = False
                        if row + i < 11 and not_found_hit_or_miss_cell_right and isinstance(self.computer_entered_grid[row + i][column], int):
                            free_horizontal_cells_count += 1
                        else:
                            not_found_hit_or_miss_cell_right = False
                        if column - i >= 0 and not_found_hit_or_miss_cell_up and isinstance(self.computer_entered_grid[row][column - i], int):
                            free_vertical_cells_count += 1
                        else:
                            not_found_hit_or_miss_cell_up = False
                        if column + i < 11 and not_found_hit_or_miss_cell_down and isinstance(self.computer_entered_grid[row][column + 1], int):
                            free_vertical_cells_count += 1
                        else:
                            not_found_hit_or_miss_cell_down = False

                    if free_horizontal_cells_count < self.length_smallest_ship_alive and free_vertical_cells_count < self.length_smallest_ship_alive:
                        list_of_indexes_of_cells_to_delete.append(index)
                    else:
                        cell.pop()
                        cell.append(free_horizontal_cells_count + free_vertical_cells_count)
                else:
                    list_of_indexes_of_cells_to_delete.append(index)
            
            for index in sorted(list_of_indexes_of_cells_to_delete, reverse = True):
                del self.list_of_cells_to_select_for_computer[index]

            self.list_of_cells_to_select_for_computer.sort(key = lambda x: x[2])
            computer_select_row = self.list_of_cells_to_select_for_computer[-1][0]
            computer_select_column = self.list_of_cells_to_select_for_computer[-1][1]
            self.list_of_cells_to_select_for_computer.pop()

            if self.computer_entered_grid[computer_select_row][computer_select_column] == 0:
                self.computer_entered_grid[computer_select_row][computer_select_column] = "miss"
            elif self.computer_entered_grid[computer_select_row][computer_select_column] != 0 and isinstance(self.computer_entered_grid[computer_select_row][computer_select_column], int):
                self.computer_entered_grid[computer_select_row][computer_select_column] = "hit"
                self.player_score -= 10

            self.selected_cell_main_battle_computer_turn = [computer_select_column, computer_select_row]


    def checking_ship_hit_but_not_sunk(self):
        for row_index, row in enumerate(self.computer_entered_grid):
            for column_index, column in enumerate(row):
                if column == "hit" and sum(ship_type.count(self.player_grid[row_index][column_index]) for ship_type in self.computer_entered_grid) > 0:
                    if self.player_grid[row_index][column_index] in [1, 2, 3, 5]:
                        row_check_index_right = 1
                        if row_index < 10 and self.computer_entered_grid[row_check_index_right + row_index][column_index] == "hit":
                            while row_check_index_right + row_index <= 10:
                                if isinstance(self.computer_entered_grid[row_check_index_right + row_index][column_index], int):
                                    return True, [row_check_index_right + row_index, column_index]
                                elif self.computer_entered_grid[row_check_index_right + row_index][column_index] == "miss":
                                    break                                
                                row_check_index_right += 1

                            if row_index > 0 and isinstance(self.computer_entered_grid[row_index - 1][column_index], int):
                                return True, [row_index - 1, column_index]

                        column_check_index_up = 1
                        if column_index < 10 and self.computer_entered_grid[row_index][column_index + column_check_index_up] == "hit":
                            while column_check_index_up + column_index <= 10:
                                if isinstance(self.computer_entered_grid[row_index][column_index + column_check_index_up], int):
                                    return True, [row_index, column_index + column_check_index_up]
                                elif self.computer_entered_grid[row_index][column_index + column_check_index_up] == "miss":
                                    break
                                column_check_index_up += 1

                            if column_index > 0 and isinstance(self.computer_entered_grid[row_index][column_index - 1], int):
                                return True, [row_index, column_index - 1]

                    if row_index < 10:
                        if isinstance(self.computer_entered_grid[row_index + 1][column_index], int) and self.computer_entered_grid[row_index][column_index] == "hit":
                            return True, [row_index + 1, column_index]
                    if row_index > 0:
                        if isinstance(self.computer_entered_grid[row_index - 1][column_index], int) and self.computer_entered_grid[row_index][column_index] == "hit":
                            return True, [row_index - 1, column_index]
                    if column_index < 10:
                        if isinstance(self.computer_entered_grid[row_index][column_index + 1], int) and self.computer_entered_grid[row_index][column_index] == "hit":
                            return True, [row_index, column_index + 1]
                    if column_index > 0:
                        if isinstance(self.computer_entered_grid[row_index][column_index - 1], int) and self.computer_entered_grid[row_index][column_index] == "hit":
                            return True, [row_index, column_index - 1]
        return False, None


    def run_main_battle_computer_turn(self):
        self.computer_select_cell()
        if self.is_sound_playing:
            self.rocket_sound.play()
        while self.computer_turn:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game_battle_running = False
                    self.game_setup_running = False
                    self.game_open = False
                    self.computer_turn = False
            
            self.update_main_battle_computer_turn(self.rotate_ship, self.selected_ship, self.mouse_position, self.player_grid, self.game_battle_running, self.computer_turn, self.missile_position_y, self.missile_on)
            self.draw_main_battle_computer_turn()

            self.game_ending_lose_check()
            if self.player_ships_sunk == 5 and self.missile.rect.center[0] == self.missile_x_border:
                self.game_ending_lose = True
                self.game_lose_screen()

            if self.game_battle_running == False and self.game_setup_running == False and self.computer_turn == False and self.game_open:
                self.reset()

            pg.display.update()

            if self.missile_x_border != 0 and self.missile_on == False:
                time.sleep(1)
                self.computer_turn = False
                self.missile_x_border = 0

            self.clock.tick(FPS)


    def update_main_battle_computer_turn(self, rotate_ship, selected_ship, mouse_position, player_grid, game_battle_running, computer_turn, missile_position_y, missile_on):
        if self.missile.rect.center[0] == self.missile_x_border and self.missile_on:
            if self.is_sound_playing and self.computer_entered_grid[self.selected_cell_main_battle_computer_turn[1]][self.selected_cell_main_battle_computer_turn[0]] == "hit":
                self.explosion_sound.play()
            elif self.is_sound_playing:
                self.water_splash_sound.play()
            self.missile_on = False
            self.selected_cell_main_battle_computer_turn = None

        self.all_sprites_group.update(self.rotate_ship, self.selected_ship, self.mouse_position, self.player_grid, self.game_battle_running, self.computer_turn, self.missile_position_y, self.missile_on, self.computer_grid, self.computer_ships_sunk)
        
        if self.selected_cell_main_battle_computer_turn:
            self.missile_on = True
            self.missile_x_border = self.selected_cell_main_battle_computer_turn[0] * CELL_SIZE + TABLE_POSITION_X_MAIN_BATTLE_COMPUTER_TURN + 1/2 * CELL_SIZE
            self.missile_position_y = self.selected_cell_main_battle_computer_turn[1] * CELL_SIZE + TABLE_POSITION_Y + 1/2 * CELL_SIZE


    def draw_main_battle_computer_turn(self):
        self.main_battle_background_x += 0.5
        self.main_battle_background_x_2 += 0.5

        if self.main_battle_background_x > self.main_battle_background.get_width():
            self.main_battle_background_x = -self.main_battle_background.get_width()
        if self.main_battle_background_x_2 > self.main_battle_background.get_width():
            self.main_battle_background_x_2 = -self.main_battle_background.get_width()
        self.screen.blit(self.main_battle_background, (self.main_battle_background_x, 0))
        self.screen.blit(self.main_battle_background, (self.main_battle_background_x_2, 0))

        self.selected_cell_fill_main_battle_computer_turn(self.screen)
        self.message_to_screen_main_battle_computer_turn(self.screen)
        self.table_cell_draw_main_battle_computer_turn(self.screen)
        self.all_sprites_group.draw(self.screen)


    def selected_cell_fill_main_battle_computer_turn(self, screen):
        for row_index, row in enumerate(self.computer_entered_grid):
            for column_index, column in enumerate(row):
                if column == "hit" and ([column_index, row_index] != self.selected_cell_main_battle_computer_turn or (self.missile.rect.center[0] == self.missile_x_border and [column_index, row_index] == self.selected_cell_main_battle_computer_turn)):
                    pg.draw.rect(self.screen, RED, (column_index * CELL_SIZE + TABLE_POSITION_X_MAIN_BATTLE_COMPUTER_TURN, row_index * CELL_SIZE + TABLE_POSITION_Y, CELL_SIZE, CELL_SIZE))
                elif column == "miss" and ([column_index, row_index] != self.selected_cell_main_battle_computer_turn or (self.missile.rect.center[0] == self.missile_x_border and [column_index, row_index] == self.selected_cell_main_battle_computer_turn)):
                    pg.draw.rect(self.screen, GREY, (column_index * CELL_SIZE + TABLE_POSITION_X_MAIN_BATTLE_COMPUTER_TURN, row_index * CELL_SIZE + TABLE_POSITION_Y, CELL_SIZE, CELL_SIZE))
                elif self.missile.rect.center[0] != self.missile_x_border and [column_index, row_index] == self.selected_cell_main_battle_computer_turn:
                    pg.draw.rect(self.screen, YELLOW, (column_index * CELL_SIZE + TABLE_POSITION_X_MAIN_BATTLE_COMPUTER_TURN, row_index * CELL_SIZE + TABLE_POSITION_Y, CELL_SIZE, CELL_SIZE))


    def message_to_screen_main_battle_computer_turn(self, screen):
        line_font = pg.font.Font('freesansbold.ttf', 60)
        list_of_messages = ["Computer's", "turn!", "Player's ships", f"sunk: {self.player_ships_sunk}/5"]
        for index, message in enumerate(list_of_messages):
            line = line_font.render(message, True, YELLOW)
            line_surface = pg.Surface(line.get_size())
            line_surface.fill(BLACK)
            line_surface.blit(line, (0, 0))
            if index == 0:
                self.screen.blit(line_surface, (50, 20))
            elif index == 1:
                self.screen.blit(line_surface, (150, 90))
            elif index == 2:
                self.screen.blit(line_surface, (20, 410))
            else:
                self.screen.blit(line_surface, (90, 480))


    def table_cell_draw_main_battle_computer_turn(self, screen):
        pg.draw.rect(self.screen, BLACK, (TABLE_POSITION_X_MAIN_BATTLE_COMPUTER_TURN, TABLE_POSITION_Y, TABLE_SIZE, TABLE_SIZE), 5)
        for i in range(1, 11):
            pg.draw.line(self.screen, BLACK, (TABLE_POSITION_X_MAIN_BATTLE_COMPUTER_TURN + i * CELL_SIZE, TABLE_POSITION_Y), (TABLE_POSITION_X_MAIN_BATTLE_COMPUTER_TURN + i * CELL_SIZE, TABLE_POSITION_Y + TABLE_SIZE), 5)
            pg.draw.line(self.screen, BLACK, (TABLE_POSITION_X_MAIN_BATTLE_COMPUTER_TURN, TABLE_POSITION_Y + i * CELL_SIZE), (TABLE_POSITION_X_MAIN_BATTLE_COMPUTER_TURN + TABLE_SIZE, TABLE_POSITION_Y + i * CELL_SIZE), 5)

### GAME ENDING SCREENS ###

    def game_lose_screen(self):
        self.final_player_score = len(self.computer_ships_sunk) * 50 - self.player_ships_sunk * 30 + self.player_score
        while self.game_ending_lose:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game_battle_running = False
                    self.game_setup_running = False
                    self.game_open = False
                    self.computer_turn = False
                    self.game_ending_lose = False
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    for i in range(4):
                        if i == 0 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            self.game_ending_lose = False
                            self.game_battle_running = False
                            self.game_setup_running = False
                            self.computer_turn = False
                        elif i == 2 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            self.game_battle_running = False
                            self.game_setup_running = False
                            self.game_open = False
                            self.computer_turn = False
                            self.game_ending_lose = False

            self.draw_game_lose(self.screen)

            pg.display.update()
            self.clock.tick(FPS)


    def draw_game_lose(self, screen):
        self.screen.blit(self.game_over_background, (0, 0))
        self.message_to_screen_game_lose(self.screen)
        self.loading_buttons_on_game_lose_screen(self.screen, self.mouse_position, self.list_of_button_texts, self.buttons_size_x, self.buttons_size_y)


    def message_to_screen_game_lose(self, screen):
        line_font = pg.font.Font('freesansbold.ttf', 60)
        list_of_messages = ["GAME OVER!", f"Your score is {self.final_player_score} points.", "Try harder next time."]
        for index, message in enumerate(list_of_messages):
            line = line_font.render(message, True, YELLOW)
            line_surface = pg.Surface(line.get_size())
            line_surface.fill(BLACK)
            line_surface.blit(line, (0, 0))
            if index == 0:
                self.screen.blit(line_surface, (540, 20))
            elif index == 1:
                self.screen.blit(line_surface, (390, 250))
            else:
                self.screen.blit(line_surface, (440, 430))

    def loading_buttons_on_game_lose_screen(self, screen, mouse_position, list_of_button_texts, buttons_size_x, buttons_size_y):
        self.mouse_position = pg.mouse.get_pos()
        self.list_of_button_texts = ["MAIN", "PAGE", "EXIT", "GAME"]
        self.list_of_button_positions_x = [560, 560, 740, 740]
        self.list_of_button_positions_y = [665, 705, 665, 705]
        self.buttons_size_x = 170
        self.buttons_size_y = 110

        # Button Texts
        for i in range(4):
            if i % 2 == 0 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y: 
                pg.draw.rect(self.screen, RED, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y])
                pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y], 5)
            elif i % 2 == 0: 
                pg.draw.rect(self.screen, GREEN, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y])
                pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y], 5)

            font = pg.font.Font('freesansbold.ttf', 40)
            text_font = font.render(self.list_of_button_texts[i], True, BLACK)
            text_font_width = text_font.get_width()
            text_font_height = text_font.get_height()
            self.screen.blit(text_font, (self.list_of_button_positions_x[i] + (self.buttons_size_x - text_font_width) // 2, self.list_of_button_positions_y[i] + (self.buttons_size_y - text_font_height) // 4))


    def game_win_screen(self):
        self.final_player_score = len(self.computer_ships_sunk) * 50 - self.player_ships_sunk * 30 + self.player_score
        try:
            with open(".highscores.pickle", "rb") as p:
                pickle_objects = pickle.load(p)
            self.list_of_highscores = pickle_objects
            if len(self.list_of_highscores) < 10:
                self.final_player_score_in_highscores = True
            elif len(self.list_of_highscores) >= 10 and self.list_of_highscores[-1][1] < self.final_player_score:
                self.final_player_score_in_highscores = True
            else:
                self.final_player_score_in_highscores = False
        except EOFError:
            self.list_of_highscores = []
            self.final_player_score_in_highscores = True

        while self.game_ending_win:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game_battle_running = False
                    self.game_setup_running = False
                    self.game_open = False
                    self.game_ending_win = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    for i in range(6):
                        if i == 0 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            self.game_battle_running = False
                            self.game_setup_running = False
                            self.computer_turn = False
                            self.game_ending_win = False
                        elif i == 2 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            self.game_battle_running = False
                            self.game_setup_running = False
                            self.game_open = False
                            self.computer_turn = False
                            self.game_ending_win = False
                        elif self.final_player_score_in_highscores != None and self.final_player_score_in_highscores and i == 4 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y:
                            self.list_of_highscores.append(tuple([self.player_name, self.final_player_score]))
                            self.list_of_highscores.sort(reverse = True, key = lambda x: x[1])
                            self.list_of_highscores = self.list_of_highscores[:10]
                            instance_of_PickleHighScore = PickleHighScore(self.list_of_highscores)
                            instance_of_PickleHighScore.saving_highscore_pickle()
                            self.final_player_score_in_highscores = None
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    elif len(self.player_name) < 10:
                        self.player_name += event.unicode

            self.draw_game_win(self.screen)

            pg.display.update()
            self.clock.tick(FPS)


    def draw_game_win(self, screen):
        self.screen.blit(self.game_win_background, (0, 0))
        self.message_to_screen_game_win(self.screen)
        self.loading_buttons_on_game_win_screen(self.screen, self.mouse_position, self.list_of_button_texts, self.buttons_size_x, self.buttons_size_y)


    def message_to_screen_game_win(self, screen):
        first_line_font = pg.font.Font('freesansbold.ttf', 60)
        line_font = pg.font.Font('freesansbold.ttf', 50)
        list_of_messages = ["CONGRATULATIONS!", f"Your score is {self.final_player_score} points."]
        if self.final_player_score_in_highscores:
            list_of_messages.extend(["Your score is in the top 10 highscores.",
            "Type your name by pressing the alphabet letters", 
            "(max. 10 characters) to save your score.",
            f"{self.player_name}"])
        elif self.final_player_score_in_highscores == False:
            list_of_messages.extend(["Unfortunately, your score is not in the", 
            "top 10 highscores. Therefore, your score",
            "cannot be saved. Try harder next time."])
        elif self.final_player_score_in_highscores == None:
            list_of_messages.extend(["Your score has been saved!", "You can check it in the Highscores menu on the main page."])

        for index, message in enumerate(list_of_messages):
            if index == 0:
                line = first_line_font.render(message, True, YELLOW)
            elif self.final_player_score_in_highscores and index == 5:
                line = first_line_font.render(message, True, BLACK)
            else:
                line = line_font.render(message, True, YELLOW)
            line_surface = pg.Surface(line.get_size())
            if self.final_player_score_in_highscores and index == 5:
                line_surface.fill(PINK)
            else:
                line_surface.fill(BLACK)
            line_surface.blit(line, (0, 0))
            if index == 0:
                self.screen.blit(line_surface, (400, 20))
            elif index == 1:
                self.screen.blit(line_surface, (440, 160))
            elif self.final_player_score_in_highscores and index == 5:
                self.screen.blit(line_surface, (480, 540))
            else:
                self.screen.blit(line_surface, (20, 160 + index * 60))


    def loading_buttons_on_game_win_screen(self, screen, mouse_position, list_of_button_texts, buttons_size_x, buttons_size_y):
        self.mouse_position = pg.mouse.get_pos()
        self.list_of_button_texts = ["MAIN", "PAGE", "EXIT", "GAME"]
        self.list_of_button_positions_x = [560, 560, 740, 740]
        self.list_of_button_positions_y = [665, 705, 665, 705]
        self.buttons_size_x = 170
        self.buttons_size_y = 110

        if self.final_player_score_in_highscores:
            self.list_of_button_texts.extend(["SAVE", "SCORE"])
            self.list_of_button_positions_x.extend([1060, 1060])
            self.list_of_button_positions_y.extend([510, 550])
            # Button Texts
            for i in range(4, 6):
                if i % 2 == 0 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y: 
                    pg.draw.rect(self.screen, RED, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y])
                    pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y], 5)
                elif i % 2 == 0: 
                    pg.draw.rect(self.screen, GREEN, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y])
                    pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y], 5)

                font = pg.font.Font('freesansbold.ttf', 40)
                text_font = font.render(self.list_of_button_texts[i], True, BLACK)
                text_font_width = text_font.get_width()
                text_font_height = text_font.get_height()
                self.screen.blit(text_font, (self.list_of_button_positions_x[i] + (self.buttons_size_x - text_font_width) // 2, self.list_of_button_positions_y[i] + (self.buttons_size_y - text_font_height) // 4))

        # Button Texts
        for i in range(4):
            if i % 2 == 0 and self.list_of_button_positions_x[i] <= self.mouse_position[0] <= self.list_of_button_positions_x[i] + self.buttons_size_x and self.list_of_button_positions_y[i] <= self.mouse_position[1] <= self.list_of_button_positions_y[i] + self.buttons_size_y: 
                pg.draw.rect(self.screen, RED, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y])
                pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y], 5)
            elif i % 2 == 0: 
                pg.draw.rect(self.screen, GREEN, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y])
                pg.draw.rect(self.screen, BLACK, [self.list_of_button_positions_x[i], self.list_of_button_positions_y[i], self.buttons_size_x, self.buttons_size_y], 5)

            font = pg.font.Font('freesansbold.ttf', 40)
            text_font = font.render(self.list_of_button_texts[i], True, BLACK)
            text_font_width = text_font.get_width()
            text_font_height = text_font.get_height()
            self.screen.blit(text_font, (self.list_of_button_positions_x[i] + (self.buttons_size_x - text_font_width) // 2, self.list_of_button_positions_y[i] + (self.buttons_size_y - text_font_height) // 4))


if __name__ == "__main__":
    Main().game_start_screen()