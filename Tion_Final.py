import sys

import pygame
import time

from helpers.constants import Constants
from maze import Maze
from speechrecognition import Speechrecognition

class Game:
    def __init__(self):
        pygame.init()
        self.size = (Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode(self.size)
        self.maze = Maze(Constants.GRID_COLS, Constants.GRID_ROWS, self.size)
        self.maze.generate_maze()
        self.sr = Speechrecognition()
        self.black_screen = pygame.image.load("gameover.jpg")
        self.black_screen = pygame.transform.scale(self.black_screen, (self.size))


    def game_loop(self):
        self.handle_events()
        self.update_game()
        self.draw_components()



    def update_game(self):
        self.maze.update()
        self.gameover_handling()

    def draw_components(self):
        if self.maze.active:
            self.screen.fill([64, 64, 64])
            self.maze.draw_maze(self.screen)
            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.handle_key_down(event)
            if event.type == pygame.KEYUP:
                self.handle_key_up(event)
            if event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_pressed(event)
            if event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_released(event)

    def handle_key_down(self, event):
        if event.key == pygame.K_m:
            print("Generating Maze")
            self.maze.generate_maze()
        if event.key == pygame.K_t:
            #self.sr.recognize_speech()
            self.action_list = self.sr.recognize_speech()
        if event.key == pygame.K_o:
            print("Generating Obstacle")
            self.maze.generate_obstacles()
        if event.key == pygame.K_r:
            print("Generating Rooms")
            self.maze.generate_room()
        if event.key == pygame.K_UP:
            #print("UP")
            #self.maze.move_mouse(0, -1)
            self.action_list = [[0,-1]]
        if event.key == pygame.K_DOWN:
            #print("DOWN")
            #self.maze.move_mouse(0, 1)
            self.action_list = [[0,1]]
        if event.key == pygame.K_LEFT:
            #print("LEFT")
            #self.maze.move_mouse(-1, 0)
            self.action_list = [[-1,0]]
        if event.key == pygame.K_RIGHT:
            #print("RIGHT")
            #self.maze.move_mouse(1, 0)
            self.action_list = [[1,0]]

        if (self.action_list):
            for move in self.action_list:
                x = move[0]
                y = move[1]
                self.maze.move_mouse(x,y)
    def handle_key_up(self, event):
        pass

    def handle_mouse_motion(self, event):
        pass

    def handle_mouse_pressed(self, event):
            x = int(event.pos[0] / self.maze.cell_width)
            y = int(event.pos[1] / self.maze.cell_height)
            # if event.button == 1:
            #     self.maze.set_cat(self.maze.grid[x][y])
            if event.button == 3:
                self.maze.set_mouse(self.maze.grid[x][y])

    def handle_mouse_released(self, event):
        pass

    # def recognize_speech(self):
    #     print("Speech recognition activated ")
    #     with self.microphone as listen:
    #         self.recognizer.adjust_for_ambient_noise(listen)
    #         print("Say something:")
    #         audio = self.recognizer.listen(listen, timeout=2, phrase_time_limit=5)  # Adjust timeout as needed
    #     try:
    #         speech = self.recognizer.recognize_google(audio)
    #         print("You said:", speech)
    #
    #         words_list = speech.split()
    #         print(words_list)
    #         for word in words_list:
    #             if word in self.DOWN:
    #                 print("Recognized down")
    #                 self.maze.move_mouse(0, 1)
    #             if word in self.UP:
    #                 print("Recognized up")
    #                 self.maze.move_mouse(0, -1)
    #             if word in self.RIGHT:
    #                 print("Recognized right")
    #                 self.maze.move_mouse(1, 0)
    #             if word in self.LEFT:
    #                 print("Recognized left")
    #                 self.maze.move_mouse(-1, 0)
    #
    #     except sr.WaitTimeoutError:
    #         print("Too slow talking")
    #     except sr.RequestError as e:
    #         print(f"Could not connect to the Google Speech Recognition API: {e}")
    #     except sr.UnknownValueError:
    #         print("Couldn't understand")

    def gameover_handling(self):
        if self.maze.is_game_over():
            # Display the black screen
            self.screen.blit(self.black_screen, (0, 0))
            pygame.display.flip()
            time.sleep(3)
            sys.exit()

if __name__ == "__main__":
    game = Game()
    while True:
        game.game_loop()
