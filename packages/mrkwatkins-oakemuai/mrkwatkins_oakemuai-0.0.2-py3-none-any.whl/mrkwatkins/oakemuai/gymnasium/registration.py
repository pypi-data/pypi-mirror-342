from os import PathLike

import gymnasium as gym

from mrkwatkins.oakemuai.gymnasium.game_configuration import GameConfiguration
from mrkwatkins.oakemuai.gymnasium.observation_configuration import ObservationConfiguration

registered = set()


def register(game_configuration: GameConfiguration, observation_configuration: ObservationConfiguration):
    gym.register(
        id=game_configuration.name,
        entry_point="mrkwatkins.oakemuai.gymnasium:OakEmuEnv",
        kwargs=dict(
            game_configuration=game_configuration,
            observation_configuration=observation_configuration,
        ),
    )


def ensure_registered(game_configuration_path: str | PathLike, observation_configuration_path: str | PathLike):
    global registered

    game_configuration = GameConfiguration(game_configuration_path)

    if game_configuration.name not in registered:
        observation_configuration = ObservationConfiguration(observation_configuration_path)
        register(game_configuration, observation_configuration)
        registered.add(game_configuration.name)
