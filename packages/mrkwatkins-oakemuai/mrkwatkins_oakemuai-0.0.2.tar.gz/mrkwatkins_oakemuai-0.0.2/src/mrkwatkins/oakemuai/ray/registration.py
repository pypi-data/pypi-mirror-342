from os import PathLike

from ray import tune

from mrkwatkins.oakemuai.gymnasium import OakEmuEnv
from mrkwatkins.oakemuai.gymnasium.game_configuration import GameConfiguration
from mrkwatkins.oakemuai.gymnasium.observation_configuration import ObservationConfiguration

registered = set()


def register(game_configuration: GameConfiguration, observation_configuration: ObservationConfiguration):
    tune.register_env(game_configuration.name, lambda _: OakEmuEnv(game_configuration, observation_configuration))


def ensure_registered(game_configuration_path: str | PathLike, observation_configuration_path: str | PathLike):
    global registered

    game_configuration = GameConfiguration(game_configuration_path)

    if game_configuration.name not in registered:
        observation_configuration = ObservationConfiguration(observation_configuration_path)
        register(game_configuration, observation_configuration)
        registered.add(game_configuration.name)
