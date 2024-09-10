import numpy as np
import random
import pickle
import os
from collections import deque
from tqdm import tqdm
import pygame

class MLAgent:
    def __init__(self, state_size, action_size, learning_rate=0.001, discount_factor=0.95,
                 exploration_rate=1.0, exploration_decay=0.999, exploration_min=0.1):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_min = exploration_min
        self.exploration_decay = exploration_decay
        self.q_table = {}

    def get_action(self, state):
        state_key = tuple(state)
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

    def train(self, game, episodes, max_steps, save_interval=100, visualize=False):
        scores = []
        avg_scores = deque(maxlen=100)

        for episode in tqdm(range(episodes)):
            game.reset()
            state = game.get_state()
            total_reward = 0

            for step in range(max_steps):
                action = self.get_action(state)
                next_state, reward, done = game.step(action)

                self.update_q_table(state, action, reward, next_state, done)
                state = next_state
                total_reward += reward

                if visualize:
                    game.render(episode, step, total_reward, max(avg_scores) if scores else 0)
                    pygame.time.wait(1)

                if done:
                    break

            scores.append(total_reward)
            avg_scores.append(total_reward)

            if (episode + 1) % save_interval == 0:
                self.save_progress(scores, episode + 1)
                self.plot_progress(scores, episode + 1)

        return scores

    def save_progress(self, scores, episode):
        os.makedirs("train_history", exist_ok=True)
        with open(f"train_history/q_table_episode_{episode}.pkl", "wb") as f:
            pickle.dump(self.q_table, f)
        with open(f"train_history/scores_episode_{episode}.pkl", "wb") as f:
            pickle.dump(scores, f)

    def plot_progress(self, scores, episode):
        with open(f"train_history/q_table_episode_{episode}.pkl", "rb") as f:
            q_table = pickle.load(f)
        with open(f"train_history/scores_episode_{episode}.pkl", "rb") as f:
            scores = pickle.load(f)
        return q_table, scores

    def test(self, game, num_games=100, max_steps=25):
        wins = 0
        for _ in range(num_games):
            game.reset()
            for _ in range(max_steps):
                state = game.get_state()
                action = self.get_action(state)
                _, _, done = game.step(action)
                if done:
                    wins += 1
                    break
        return wins / num_games