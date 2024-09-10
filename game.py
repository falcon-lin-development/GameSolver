import random
from enum import Enum
import pygame

class Color(Enum):
    OTHER = 0
    RED = 1

class Move(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Game:
    def __init__(self):
        self.faces = {
            'top': [[Color.OTHER for _ in range(3)] for _ in range(3)],
            'right': [[Color.OTHER for _ in range(3)] for _ in range(3)],
            'bottom': [[Color.OTHER for _ in range(3)] for _ in range(3)],
            'left': [[Color.OTHER for _ in range(3)] for _ in range(3)],
            'center': [[Color.OTHER for _ in range(3)] for _ in range(3)]
        }
        self.initialize_game()
        self.setup_pygame()

    def initialize_game(self):
        # Create a list of all possible positions
        all_positions = [(face, row, col) 
                         for face in self.faces 
                         for row in range(3) 
                         for col in range(3)]
        
        # Randomly choose 9 positions for red colors
        red_positions = random.sample(all_positions, 9)
        
        # Place red colors in the chosen positions
        for face, row, col in red_positions:
            self.faces[face][row][col] = Color.RED

    def make_move(self, move: Move, row_col: int):
        if move in [Move.UP, Move.DOWN]:
            self._vertical_move(move, row_col)
        elif move in [Move.LEFT, Move.RIGHT]:
            self._horizontal_move(move, row_col)

    def _vertical_move(self, move: Move, col: int):
        if move == Move.UP:
            # Move up: Shift colors upward, rotate topmost color to the bottom
            temp = self.faces['top'][0][col]
            # Shift colors from bottom to center
            self.faces['top'][0][col] = self.faces['top'][1][col]
            self.faces['top'][1][col] = self.faces['top'][2][col]
            self.faces['top'][2][col] = self.faces['center'][0][col]
            self.faces['center'][0][col] = self.faces['center'][1][col]
            self.faces['center'][1][col] = self.faces['center'][2][col]
            self.faces['center'][2][col] = self.faces['bottom'][0][col]
            self.faces['bottom'][0][col] = self.faces['bottom'][1][col]
            self.faces['bottom'][1][col] = self.faces['bottom'][2][col]
            self.faces['bottom'][2][col] = temp
        else:  # Move.DOWN
            # Move down: Shift colors downward, rotate bottommost color to the top
            temp = self.faces['bottom'][2][col]
            # Shift colors from top to center
            self.faces['bottom'][2][col] = self.faces['bottom'][1][col]
            self.faces['bottom'][1][col] = self.faces['bottom'][0][col]
            self.faces['bottom'][0][col] = self.faces['center'][2][col]
            self.faces['center'][2][col] = self.faces['center'][1][col]
            self.faces['center'][1][col] = self.faces['center'][0][col]
            self.faces['center'][0][col] = self.faces['top'][2][col]
            self.faces['top'][2][col] = self.faces['top'][1][col]
            self.faces['top'][1][col] = self.faces['top'][0][col]
            self.faces['top'][0][col] = temp


    def _horizontal_move(self, move: Move, row: int):
        if move == Move.LEFT:
            # Move left: Shift colors leftward, rotate leftmost color to the right
            temp = self.faces['left'][row][0]
            # Shift colors from left to center
            self.faces['left'][row][0] = self.faces['left'][row][1]
            self.faces['left'][row][1] = self.faces['left'][row][2]
            self.faces['left'][row][2] = self.faces['center'][row][0]
            self.faces['center'][row][0] = self.faces['center'][row][1]
            self.faces['center'][row][1] = self.faces['center'][row][2]
            self.faces['center'][row][2] = self.faces['right'][row][0]
            self.faces['right'][row][0] = self.faces['right'][row][1]
            self.faces['right'][row][1] = self.faces['right'][row][2]
            self.faces['right'][row][2] = temp

        else:  # Move.RIGHT
            # Move right: Shift colors rightward, rotate rightmost color to the left
            temp = self.faces['right'][row][2]
            # Shift colors from right to center
            self.faces['right'][row][2] = self.faces['right'][row][1]
            self.faces['right'][row][1] = self.faces['right'][row][0]
            self.faces['right'][row][0] = self.faces['center'][row][2]
            self.faces['center'][row][2] = self.faces['center'][row][1]
            self.faces['center'][row][1] = self.faces['center'][row][0]
            self.faces['center'][row][0] = self.faces['left'][row][2]
            self.faces['left'][row][2] = self.faces['left'][row][1]
            self.faces['left'][row][1] = self.faces['left'][row][0]
            self.faces['left'][row][0] = temp
            


    def print_board(self):
        # Print the top face
        for row in self.faces['top']:
            print("        " + " ".join("R" if cell == Color.RED else "O" for cell in row))
        print()

        # Print the left, center, and right faces side by side
        for i in range(3):
            left_row = " ".join("R" if cell == Color.RED else "O" for cell in self.faces['left'][i])
            center_row = " ".join("R" if cell == Color.RED else "O" for cell in self.faces['center'][i])
            right_row = " ".join("R" if cell == Color.RED else "O" for cell in self.faces['right'][i])
            print(f"{left_row}   {center_row}   {right_row}")
        print()
        
        # Print the bottom face
        for row in self.faces['bottom']:
            print("        " + " ".join("R" if cell == Color.RED else "O" for cell in row))
        print()

    def setup_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        self.font = pygame.font.Font(None, 36)

    def render(self, episode, step, total_reward, best_reward):
        self.screen.fill((255, 255, 255))

        # Draw the top face
        for i in range(3):
            for j in range(3):
                color = (255, 0, 0) if self.faces['top'][i][j] == Color.RED else (0, 0, 0)
                pygame.draw.rect(self.screen, color, (200 + j * 50, 50 + i * 50, 50, 50))

        # Draw the left, center, and right faces
        for i in range(3):
            for j in range(3):
                color = (255, 0, 0) if self.faces['left'][i][j] == Color.RED else (0, 0, 0)
                pygame.draw.rect(self.screen, color, (50 + j * 50, 200 + i * 50, 50, 50))

                color = (255, 0, 0) if self.faces['center'][i][j] == Color.RED else (0, 0, 0)
                pygame.draw.rect(self.screen, color, (200 + j * 50, 200 + i * 50, 50, 50))

                color = (255, 0, 0) if self.faces['right'][i][j] == Color.RED else (0, 0, 0)
                pygame.draw.rect(self.screen, color, (350 + j * 50, 200 + i * 50, 50, 50))

        # Draw the bottom face
        for i in range(3):
            for j in range(3):
                color = (255, 0, 0) if self.faces['bottom'][i][j] == Color.RED else (0, 0, 0)
                pygame.draw.rect(self.screen, color, (200 + j * 50, 350 + i * 50, 50, 50))

        # Draw episode, step, total reward, and best reward
        episode_text = self.font.render(f"Episode: {episode}", True, (0, 0, 0))
        step_text = self.font.render(f"Step: {step}", True, (0, 0, 0))
        total_reward_text = self.font.render(f"Total Reward: {total_reward}", True, (0, 0, 0))
        best_reward_text = self.font.render(f"Best Reward: {best_reward}", True, (0, 0, 0))

        self.screen.blit(episode_text, (10, 10))
        self.screen.blit(step_text, (10, 40))
        self.screen.blit(total_reward_text, (10, 70))
        self.screen.blit(best_reward_text, (10, 100))

        pygame.display.flip()

    def get_state(self):
        state = []
        for face in ["top", "right", "bottom", "left", "center"]:
            state.extend([1 if cell == Color.RED else 0 for row in self.faces[face] for cell in row])
        return state

    def step(self, action):
        move = Move(action // 3)
        index = action % 3
        self.make_move(move, index)
        next_state = self.get_state()
        reward = self.get_reward()
        done = self.is_game_won()
        return next_state, reward, done

    def get_reward(self):
        # Default reward function (can be overridden in working_panel.py)
        r = 0
        center_reds = sum(sum(1 for cell in row if cell == Color.RED) for row in self.faces["center"])
        r += center_reds * 5
        for face in ["top", "right", "bottom", "left"]:
            face_reds = sum(sum(5 for cell in row if cell == Color.RED) for row in self.faces[face])
            r -= face_reds
        return r

    def is_game_won(self):
        return all(all(cell == Color.RED for cell in row) for row in self.faces["center"])

    def reset(self):
        self.initialize_game()

    @staticmethod
    def get_action_size():
        return 12  # 4 moves * 3 indexes

    @staticmethod
    def get_state_size():
        return 5 * 3 * 3  # 5 faces, each 3x3