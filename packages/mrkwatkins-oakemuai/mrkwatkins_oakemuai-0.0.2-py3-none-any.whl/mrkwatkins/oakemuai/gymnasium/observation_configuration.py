from os import PathLike

from MrKWatkins.OakEmu import BinarySerializer as DotNetBinarySerializer  # noqa
from MrKWatkins.OakEmu.Machines.ZXSpectrum.AI.Configuration.Observation import ObservationConfiguration as DotNetObservationConfiguration  # noqa


class ObservationConfiguration:
    def __init__(self, observation_configuration_path: str | PathLike):
        self.dotnet = DotNetObservationConfiguration.Load(observation_configuration_path)

    @property
    def frame_skip(self) -> int:
        return self.dotnet.FrameSkip

    def __getstate__(self):
        state = {
            "dotnet": bytes(DotNetBinarySerializer.Serialize(self.dotnet)),
        }
        return state

    def __setstate__(self, state):
        self.dotnet = DotNetBinarySerializer.Deserialize[DotNetObservationConfiguration](state["dotnet"])
