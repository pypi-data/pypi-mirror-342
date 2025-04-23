from enum import Enum

import numpy as np
import pygame

import gymnasium as gym
from gymnasium import spaces
from gymnasium.envs.registration import register

from .common import *

class Actions(Enum):
    RIGHT = 0
    UP    = 1
    LEFT  = 2
    DOWN  = 3

# Add as many wall coordinates as you like:
Walls = {
    (0, 1),
}

class GridWorldEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, render_mode=None, size_x=5, size_y=5):
        self.size_x = size_x
        self.size_y = size_y
        self.window_size = 512  # The size (width & height) of the PyGame window

        # Observations are dictionaries with the agent's and the target's location.
        self.observation_space = spaces.Dict({
            "agent":  spaces.Box(
                low=np.array([0, 0]),
                high=np.array([self.size_x - 1, self.size_y - 1]),
                shape=(2,),
                dtype=int
            ),
            "target": spaces.Box(
                low=np.array([0, 0]),
                high=np.array([self.size_x - 1, self.size_y - 1]),
                shape=(2,),
                dtype=int
            ),
        })

        self._agent_location  = np.array([-1, -1], dtype=int)
        self._target_location = np.array([-1, -1], dtype=int)

        # We have 4 actions: "right", "up", "left", "down"
        self.action_space = spaces.Discrete(4)
        self._action_to_direction = {
            Actions.RIGHT.value: np.array([+1,  0]),
            Actions.UP.value:    np.array([ 0, -1]),
            Actions.LEFT.value:  np.array([-1,  0]),
            Actions.DOWN.value:  np.array([ 0, +1]),
        }

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        # For human rendering
        self.window = None
        self.clock = None

    def _get_obs(self):
        return {"agent": self._agent_location, "target": self._target_location}

    def _get_info(self):
        # Example: track manhattan distance if desired
        return {
            "distance": np.linalg.norm(
                self._agent_location - self._target_location, ord=1
            )
        }

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        # Random initial locations
        self._agent_location = self.np_random.integers(
                0, [self.size_x, self.size_y], dtype=int
        )
        while ((self._agent_location[0] == -1 and self._agent_location[1] == -1)
              or ((self._agent_location[0], self._agent_location[1]) in Walls)
        ):
            self._agent_location = self.np_random.integers(
                0, [self.size_x, self.size_y], dtype=int
        )
        
        # Ensure target differs from agent
        self._target_location = self._agent_location.copy()
        while (
            np.array_equal(self._target_location, self._agent_location)
            or (self._target_location[0], self._target_location[1]) in Walls
        ):
            self._target_location = self.np_random.integers(
                0, [self.size_x, self.size_y], dtype=int
        )

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()
        return observation, info

    def step(self, action):
        # Current location
        old_x, old_y = self._agent_location

        # Proposed new location
        direction = self._action_to_direction[action]
        new_x = np.clip(old_x + direction[0], 0, self.size_x - 1)
        new_y = np.clip(old_y + direction[1], 0, self.size_y - 1)

        # If the new location is a wall, revert to old location
        if (new_x, new_y) in Walls:
            # Remain where you were
            self._agent_location = np.array([old_x, old_y])
        else:
            # Update agent location
            self._agent_location = np.array([new_x, new_y])

        # Check if episode is done
        terminated = np.array_equal(self._agent_location, self._target_location)
        reward = 1 if terminated else 0

        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, False, info

    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()

    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((self.window_size, self.window_size))
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((self.window_size, self.window_size))
        canvas.fill((255, 255, 255))

        # Compute tile sizes
        tile_size_x = self.window_size // self.size_x
        tile_size_y = self.window_size // self.size_y

        # Draw the grid (walkable or walls)
        for row in range(self.size_y):
            for col in range(self.size_x):
                if (col, row) in Walls:
                    # Draw a wall
                    draw_wall_tile(canvas, col, row, tile_size_x, tile_size_y)
                else:
                    # Draw a walkable tile
                    draw_walkable_tile(canvas, col, row, tile_size_x, tile_size_y)

        # Draw agent
        agent_x, agent_y = self._agent_location
        draw_label_tile(
            canvas, agent_x, agent_y, tile_size_x, tile_size_y,
            label="A", fg_color=(0, 128, 255)
        )

        # Draw goal
        goal_x, goal_y = self._target_location
        draw_label_tile(
            canvas, goal_x, goal_y, tile_size_x, tile_size_y,
            label="G", fg_color=(0, 255, 0)
        )

        if self.render_mode == "human":
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()
            self.clock.tick(self.metadata["render_fps"])
        else:  # "rgb_array"
            return np.transpose(
                pygame.surfarray.pixels3d(canvas), axes=(1, 0, 2)
            )

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()

# Register the environment
register(
    id="safety_gridworlds/Base-v0",
    entry_point="safety_gridworlds_gymnasium.environments.base:GridWorldEnv",
    max_episode_steps=300,
)