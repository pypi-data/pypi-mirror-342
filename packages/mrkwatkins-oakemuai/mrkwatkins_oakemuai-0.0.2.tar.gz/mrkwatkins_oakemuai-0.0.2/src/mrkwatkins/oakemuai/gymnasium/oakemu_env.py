from typing import Any, Literal

import gymnasium as gym
import numpy as np
import pygame
from MrKWatkins.OakEmu.Machines.ZXSpectrum.AI import Environment as DotNetEnvironment  # noqa

from mrkwatkins.oakemu.zxspectrum import ZXSpectrum
from mrkwatkins.oakemuai.gymnasium.game_configuration import GameConfiguration
from mrkwatkins.oakemuai.gymnasium.observation_configuration import ObservationConfiguration
from mrkwatkins.oakemuai.image.image import ai_image_stack_to_ndarray
from mrkwatkins.oakemuai.image.types import dot_net_type_to_dtype


class OakEmuEnv(gym.Env):
    # TODO: Other properties.
    metadata = {"render_modes": ["human", "rgb_array"]}

    def __init__(
        self,
        game_configuration: GameConfiguration,
        observation_configuration: ObservationConfiguration,
        render_mode: Literal["rgb_array"] | None = None,
    ):
        if render_mode is not None and render_mode not in self.metadata["render_modes"]:
            raise gym.error.Error(f"Invalid render_mode: {render_mode}. Expecting: {', '.join(self.metadata['render_modes'])}.")

        self._environment = DotNetEnvironment(game_configuration.dotnet, observation_configuration.dotnet)
        self._environment.Initialize()

        self.render_mode = render_mode
        self.spectrum = ZXSpectrum(self._environment.Spectrum)

        self.action_space = gym.spaces.Discrete(self._environment.ActionSpace)

        self.observation_space = gym.spaces.Box(
            low=self._environment.ObservationSpace.Low,
            high=self._environment.ObservationSpace.High,
            dtype=dot_net_type_to_dtype(self._environment.ObservationSpace.Type).type,
            shape=(
                self._environment.ObservationSpace.Shape.Frames,
                self._environment.ObservationSpace.Shape.Height,
                self._environment.ObservationSpace.Shape.Width,
            ),
        )

        if render_mode == "human":
            pygame.init()
            pygame.display.init()
            self._screen = pygame.display.set_mode((256, 192))
            self._clock = pygame.time.Clock()
        else:
            self._screen = None
            self._clock = None

    def reset(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[np.ndarray, dict[str, Any]]:
        super().reset(seed=seed, options=options)

        image_stack = self._environment.Reset(seed)

        if self.render_mode == "human":
            self.render()

        return ai_image_stack_to_ndarray(image_stack), {}

    def step(
        self,
        action: int | np.integer,
    ) -> tuple[np.ndarray, float, bool, bool, dict[str, Any]]:
        step_result = self._environment.Step(int(action))

        if self.render_mode == "human":
            self.render()

        return ai_image_stack_to_ndarray(step_result.Observation), step_result.Reward, step_result.Terminated, step_result.Truncated, {}

    def render(self) -> np.ndarray | None:
        if self.render_mode is None:
            return None

        screenshot = self._environment.Spectrum.Screen.get_rgb_sceenshot()

        if self.render_mode == "rgb_array":
            return screenshot
        else:
            screenshot = np.rot90(screenshot)
            screenshot = np.flip(screenshot, axis=0)
            pygame.surfarray.blit_array(self._screen, screenshot)

            pygame.event.pump()
            self._clock.tick(50)
            pygame.display.flip()
            return None

    def close(self):
        if self._screen is not None:
            pygame.display.quit()
            pygame.quit()
