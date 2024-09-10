import random
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt


class QLearningAgent:
    def __init__(
        self,
        state_size,
        action_size,
        learning_rate,
        discount_factor,
        exploration_rate,
        exploration_decay,
        exploration_min,
    ):
        # self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_min = exploration_min
        self.exploration_decay = exploration_decay
        self.q_table = {}

    def get_state_key(self, state):
        return tuple(state)

    def get_action(self, state):
        state_key = self.get_state_key(state)
        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.action_size)

        if random.random() < self.exploration_rate:
            return random.randint(0, self.action_size - 1)
        return np.argmax(self.q_table[state_key])

    def update_q_table(self, state, action, reward, next_state, done):
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)

        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.action_size)
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = np.zeros(self.action_size)

        current_q = self.q_table[state_key][action]
        next_max_q = np.max(self.q_table[next_state_key])
        new_q = current_q + self.learning_rate * (
            reward + self.discount_factor * next_max_q - current_q
        )
        self.q_table[state_key][action] = new_q

        if not done:
            self.exploration_rate = max(
                self.exploration_min, self.exploration_rate * self.exploration_decay
            )

    def save_progress(self, scores, episode):
        os.makedirs("train_history", exist_ok=True)
        with open(f"train_history/q_table_episode_{episode}.pkl", "wb") as f:
            pickle.dump(self.q_table, f)
        with open(f"train_history/scores_episode_{episode}.pkl", "wb") as f:
            pickle.dump(scores, f)

    def load_progress(self, episode):
        with open(f"train_history/q_table_episode_{episode}.pkl", "rb") as f:
            q_table = pickle.load(f)
        with open(f"train_history/scores_episode_{episode}.pkl", "rb") as f:
            scores = pickle.load(f)
        return q_table, scores

    @staticmethod
    def plot_progress(scores, episode):
        plt.figure(figsize=(10, 5))
        plt.plot(scores)
        plt.title(f"Training Progress - Episode {episode}")
        plt.xlabel("Episode")
        plt.ylabel("Score")
        os.makedirs("train_history", exist_ok=True)
        plt.savefig(f"train_history/training_progress_episode_{episode}.png")
        plt.close()

