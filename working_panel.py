from ml_agent import MLAgent
from game import Game

def custom_reward_function(game):
    # Custom reward function
    r = 0
    center_reds = sum(sum(1 for cell in row if cell == game.Color.RED) for row in game.faces["center"])
    r += center_reds * 10  # Increased reward for center reds
    for face in ["top", "right", "bottom", "left"]:
        face_reds = sum(sum(3 for cell in row if cell == game.Color.RED) for row in game.faces[face])
        r -= face_reds  # Decreased penalty for non-center reds
    return r

def main():
    game = Game()
    
    # Override the default reward function
    game.get_reward = lambda: custom_reward_function(game)

    # Initialize the MLAgent
    agent = MLAgent(game.get_state_size(), game.get_action_size())

    # Train the agent
    episodes = 2000
    max_steps = 25
    save_interval = 100
    scores = agent.train(game, episodes, max_steps, save_interval, visualize=True)

    # Test the trained agent
    win_rate = agent.test(game)
    print(f"Win rate: {win_rate:.2%}")

    # Plot final training progress
    agent.plot_progress(scores, episodes)

if __name__ == "__main__":
    main()