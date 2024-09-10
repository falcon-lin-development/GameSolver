from collections import deque
from tqdm import tqdm
import pygame
import matplotlib.pyplot as plt

# agent
from ml_agent import QLearningAgent
# Importing the Game class and other necessary components from your original code
from game import Game, Move, Color


WAIT_TIME = 1  # Time in milliseconds to wait between each move
LR = 0.001
DISCOUNT_FACTOR = 0.95
EXPORATION_RATE = 1.0
EXPORATION_RATE_DECAY = 0.999
EXPORATION_RATE_MIN = 0.1

# Add these global variables at the top of your file
pygame.init()
SCREEN = pygame.display.set_mode((600, 600))
FONT = pygame.font.Font(None, 36)


def visualize_training(episodes, max_steps, save_interval=100):
    game = Game()
    agent = QLearningAgent(
        game.state_size,
        game.action_size,
        learning_rate=LR,
        discount_factor=DISCOUNT_FACTOR,
        exploration_rate=EXPORATION_RATE,
        exploration_decay=EXPORATION_RATE_DECAY,
        exploration_min=EXPORATION_RATE_MIN,
    )

    scores = []
    avg_scores = deque(maxlen=100)

    for episode in tqdm(range(episodes)):
        game.reset()
        state = game.get_state()
        total_reward = 0

        for step in range(max_steps):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            action = agent.get_action(state)
            move = Move(action // 3)
            index = action % 3

            game.make_move(move, index)
            next_state = game.get_state()
            reward = get_reward(game)
            done = game.is_game_won() or step == max_steps - 1

            agent.update_q_table(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward

            # Visualize the game state
            best_reward = max(avg_scores) if len(scores) > 0 else 0
            game.draw_game_state(
                SCREEN=SCREEN,
                FONT=FONT,
                move=move,
                index=index,
                episode=episode,
                step=step,
                total_reward=total_reward,
                best_reward=best_reward,
            )
            pygame.time.wait(WAIT_TIME)

            if done:
                break

        scores.append(total_reward)
        avg_scores.append(total_reward)

        if (episode + 1) % save_interval == 0:
            agent.save_progress(scores, episode + 1)
            agent.plot_progress(scores, episode + 1)

        # # Perform cleanup after each episode
        game.cleanup()

    return agent, scores


def get_reward(_game):
    r = -1  # -1 for each move

    # Check if the game is won
    if _game.is_game_won():
        return 100  # +100 for winning

    # Count black cells in the center and non-center faces
    center_blacks = sum(
        sum(1 for cell in row if cell == Color.RED) for row in _game.faces["center"]
    )
    non_center_blacks = sum(
        sum(sum(1 for cell in row if cell == Color.RED) for row in _game.faces[face])
        for face in ["top", "right", "bottom", "left"]
    )

    # +5 for each black in center, -2 for each black not in center
    r += center_blacks * 5
    r -= non_center_blacks * 2

    return r


def test_agent(agent, num_games=100):
    wins = 0
    for _ in range(num_games):
        game = Game()
        for _ in range(25):  # Max 25 moves
            state = game.get_state()
            action = agent.get_action(state)
            move = Move(action // 3)
            index = action % 3
            game.make_move(move, index)
            if game.is_game_won():
                wins += 1
                break
    return wins / num_games


def main():
    episodes = 2000
    max_steps = 25
    save_interval = 100

    try:
        agent, scores = visualize_training(episodes, max_steps, save_interval)
    finally:
        pygame.quit()  # Ensure Pygame is properly quit

    # Test the trained agent
    win_rate = test_agent(agent)
    print(f"Win rate: {win_rate:.2%}")

    # Plot final training progress
    plt.figure(figsize=(10, 5))
    plt.plot(scores)
    plt.title("Final Training Progress")
    plt.xlabel("Episode")
    plt.ylabel("Score")
    plt.savefig("final_training_progress.png")
    plt.close()


if __name__ == "__main__":
    main()
