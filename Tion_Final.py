import sys
import speech_recognition as sr
import pygame
import time

from helpers.constants import Constants
from maze import Maze





class Game:
    def __init__(self):
        pygame.init()
        self.size = (Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT)
        self.screen = pygame.display.set_mode(self.size)
        self.maze = Maze(Constants.GRID_COLS, Constants.GRID_ROWS, self.size)
        self.maze.generate_maze()
        self.cat_image = pygame.image.load("cat4.png")
        self.cat_image = pygame.transform.scale(self.cat_image, (30, 30))
        self.mouse_image = pygame.image.load("mouse4.png")
        self.mouse_image = pygame.transform.scale(self.mouse_image, (20, 20))
        self.blackscreen = pygame.image.load("gameover.jpg")
        self.blackscreen = pygame.transform.scale(self.blackscreen, (self.size))
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def game_loop(self):
        self.handle_events()
        self.update_game()
        self.draw_components()



    def update_game(self):
        #self.gameover_handling()
        self.maze.update()

    def draw_components(self):
        if self.maze.active:
            self.screen.fill([64, 64, 64])
            self.maze.draw_maze(self.screen, self.cat_image, self.mouse_image)
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
            self.recognize_speech()
        if event.key == pygame.K_o:
            print("Generating Obstacle")
            self.maze.generate_obstacles()
        if event.key == pygame.K_r:
            print("Generating Rooms")
            self.maze.generate_room()
        if event.key == pygame.K_UP:
            #print("UP")
            self.maze.move_mouse(0, -1)
        if event.key == pygame.K_DOWN:
            #print("DOWN")
            self.maze.move_mouse(0, 1)
        if event.key == pygame.K_LEFT:
            #print("LEFT")
            self.maze.move_mouse(-1, 0)
        if event.key == pygame.K_RIGHT:
            #print("RIGHT")
            self.maze.move_mouse(1, 0)

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

    def recognize_speech(self):
        print("Speech recognition activated ")
        with self.microphone as listen:
            self.recognizer.adjust_for_ambient_noise(listen)
            print("Say something:")
            audio = self.recognizer.listen(listen, timeout=2, phrase_time_limit=3)  # Adjust timeout as needed
        try:
            speech = self.recognizer.recognize_google(audio)
            print("You said:", speech)
            if "down" in speech:
                print("Recognized down")
                self.maze.move_mouse(0, 1)
            if "up" in speech:
                print("Recognized up")
                self.maze.move_mouse(0, -1)
            if "right" in speech:
                print("Recognized right")
                self.maze.move_mouse(1, 0)
            if "left" in speech:
                print("Recognized left")
                self.maze.move_mouse(-1, 0)
        except sr.WaitTimeoutError:
            print("Too slow talking")
        except sr.RequestError as e:
            print(f"Could not connect to the Google Speech Recognition API: {e}")
        except sr.UnknownValueError:
            print("Couldn't understand")

    def gameover_handling(self):
        self.maze.gameover()
        # Display the black screen
        self.screen.blit(self.blackscreen, (0, 0))
        pygame.display.flip()
        time.sleep(3)
        sys.exit()

if __name__ == "__main__":
    game = Game()
    while True:
        game.game_loop()
