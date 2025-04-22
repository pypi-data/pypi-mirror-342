from os import PathLike

from MrKWatkins.OakEmu import BinarySerializer as DotNetBinarySerializer  # noqa
from MrKWatkins.OakEmu.Machines.ZXSpectrum.AI.Configuration.Game import GameConfiguration as DotNetGameConfiguration  # noqa


class GameConfiguration:
    def __init__(self, game_configuration_path: str | PathLike):
        self.dotnet = DotNetGameConfiguration.Load(game_configuration_path)

    @property
    def name(self) -> str:
        return self.dotnet.Name

    def __getstate__(self):
        state = {
            "dotnet": bytes(DotNetBinarySerializer.Serialize(self.dotnet)),
        }
        return state

    def __setstate__(self, state):
        self.dotnet = DotNetBinarySerializer.Deserialize[DotNetGameConfiguration](state["dotnet"])
