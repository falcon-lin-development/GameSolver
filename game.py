import random
from enum import Enum
import pygame
import gc

class Color(Enum):
    OTHER = 0
    RED = 1


class Move(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class FiveFacesGame:
    Color = Color
    Move = Move

    @property
    def state_size(self):
        _state_size = 5 * 3 * 3  # 5 faces, each 3x3
        return _state_size

    @property
    def action_size(self):
        _action_size = 12  # 4 moves (UP, DOWN, LEFT, RIGHT) * 3 indexes (0, 1, 2)
        return _action_size

    def __init__(self):
        self.initialize_game()

    def reset(self):
        self.initialize_game()

    def initialize_game(self):
        self.faces = {
            "top": [[Color.OTHER for _ in range(3)] for _ in range(3)],
            "right": [[Color.OTHER for _ in range(3)] for _ in range(3)],
            "bottom": [[Color.OTHER for _ in range(3)] for _ in range(3)],
            "left": [[Color.OTHER for _ in range(3)] for _ in range(3)],
            "center": [[Color.OTHER for _ in range(3)] for _ in range(3)],
        }
        # Create a list of all possible positions
        all_positions = [
            (face, row, col)
            for face in self.faces
            for row in range(3)
            for col in range(3)
        ]

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
            temp = self.faces["top"][0][col]
            # Shift colors from bottom to center
            self.faces["top"][0][col] = self.faces["top"][1][col]
            self.faces["top"][1][col] = self.faces["top"][2][col]
            self.faces["top"][2][col] = self.faces["center"][0][col]
            self.faces["center"][0][col] = self.faces["center"][1][col]
            self.faces["center"][1][col] = self.faces["center"][2][col]
            self.faces["center"][2][col] = self.faces["bottom"][0][col]
            self.faces["bottom"][0][col] = self.faces["bottom"][1][col]
            self.faces["bottom"][1][col] = self.faces["bottom"][2][col]
            self.faces["bottom"][2][col] = temp
        else:  # Move.DOWN
            # Move down: Shift colors downward, rotate bottommost color to the top
            temp = self.faces["bottom"][2][col]
            # Shift colors from top to center
            self.faces["bottom"][2][col] = self.faces["bottom"][1][col]
            self.faces["bottom"][1][col] = self.faces["bottom"][0][col]
            self.faces["bottom"][0][col] = self.faces["center"][2][col]
            self.faces["center"][2][col] = self.faces["center"][1][col]
            self.faces["center"][1][col] = self.faces["center"][0][col]
            self.faces["center"][0][col] = self.faces["top"][2][col]
            self.faces["top"][2][col] = self.faces["top"][1][col]
            self.faces["top"][1][col] = self.faces["top"][0][col]
            self.faces["top"][0][col] = temp

    def _horizontal_move(self, move: Move, row: int):
        if move == Move.LEFT:
            # Move left: Shift colors leftward, rotate leftmost color to the right
            temp = self.faces["left"][row][0]
            # Shift colors from left to center
            self.faces["left"][row][0] = self.faces["left"][row][1]
            self.faces["left"][row][1] = self.faces["left"][row][2]
            self.faces["left"][row][2] = self.faces["center"][row][0]
            self.faces["center"][row][0] = self.faces["center"][row][1]
            self.faces["center"][row][1] = self.faces["center"][row][2]
            self.faces["center"][row][2] = self.faces["right"][row][0]
            self.faces["right"][row][0] = self.faces["right"][row][1]
            self.faces["right"][row][1] = self.faces["right"][row][2]
            self.faces["right"][row][2] = temp

        else:  # Move.RIGHT
            # Move right: Shift colors rightward, rotate rightmost color to the left
            temp = self.faces["right"][row][2]
            # Shift colors from right to center
            self.faces["right"][row][2] = self.faces["right"][row][1]
            self.faces["right"][row][1] = self.faces["right"][row][0]
            self.faces["right"][row][0] = self.faces["center"][row][2]
            self.faces["center"][row][2] = self.faces["center"][row][1]
            self.faces["center"][row][1] = self.faces["center"][row][0]
            self.faces["center"][row][0] = self.faces["left"][row][2]
            self.faces["left"][row][2] = self.faces["left"][row][1]
            self.faces["left"][row][1] = self.faces["left"][row][0]
            self.faces["left"][row][0] = temp

    def print_board(self):
        # Print the top face
        for row in self.faces["top"]:
            print(
                "        " + " ".join("R" if cell == Color.RED else "O" for cell in row)
            )
        print()

        # Print the left, center, and right faces side by side
        for i in range(3):
            left_row = " ".join(
                "R" if cell == Color.RED else "O" for cell in self.faces["left"][i]
            )
            center_row = " ".join(
                "R" if cell == Color.RED else "O" for cell in self.faces["center"][i]
            )
            right_row = " ".join(
                "R" if cell == Color.RED else "O" for cell in self.faces["right"][i]
            )
            print(f"{left_row}   {center_row}   {right_row}")
        print()

        # Print the bottom face
        for row in self.faces["bottom"]:
            print(
                "        " + " ".join("R" if cell == Color.RED else "O" for cell in row)
            )
        print()

    def get_state(self):
        state = []
        for face in ["top", "right", "bottom", "left", "center"]:
            face_state = []
            for row in self.faces[face]:
                face_state.extend([1 if cell == Color.RED else 0 for cell in row])
            state.extend(face_state)
        return state

    def draw_game_state(
        self,
        SCREEN,
        FONT,
        move=None,
        index=None,
        episode=None,
        step=None,
        total_reward=None,
        best_reward=None,
    ):
        SCREEN.fill((255, 255, 255))
        cell_size = 50
        gap = 10
        color = {Color.RED: (255, 0, 0), Color.OTHER: (200, 200, 200)}

        # Draw faces
        positions = {
            "top": (200, 0),
            "left": (0, 200),
            "center": (200, 200),
            "right": (400, 200),
            "bottom": (200, 400),
        }

        for face, pos in positions.items():
            for i, row in enumerate(self.faces[face]):
                for j, cell in enumerate(row):
                    pygame.draw.rect(
                        SCREEN,
                        color[cell],
                        (
                            pos[0] + j * (cell_size + gap),
                            pos[1] + i * (cell_size + gap),
                            cell_size,
                            cell_size,
                        ),
                    )

        # Draw move information
        if move is not None and index is not None:
            text = FONT.render(f"Move: {move.name}, Index: {index}", True, (0, 0, 0))
            SCREEN.blit(text, (10, 560))
            text2 = FONT.render(
                f"Episode: {episode}, Step: {step}, r: {total_reward}, best: {best_reward}",
                True,
                (0, 0, 0),
            )
            SCREEN.blit(text2, (10, 520))

        pygame.display.flip()

    def cleanup(self):
        pygame.event.pump()  # Process event queue to prevent "not responding"
        pygame.display.update()  # Update the display
        pygame.time.wait(1)  # Short wait to allow for event processing
        gc.collect()  # Run the garbage collector


    def is_game_won(self):
        return all(
            all(cell == Color.RED for cell in row) for row in self.faces["center"]
        )


class Game(FiveFacesGame):
    def __init__(self):
        super().__init__()

    def reset(self):
        super().reset()


if __name__ == "__main__":
    # Example usage
    game = Game()
    print("Initial game state:")
    game.print_board()

    # Make some moves
    game.make_move(Move.UP, 0)
    # game.make_move(Move.LEFT, 2)

    print("\nAfter moves:")
    game.print_board()
