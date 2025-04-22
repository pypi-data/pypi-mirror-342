import os
from datetime import datetime
from typing import Optional, cast

from gymnasium import Env
from gymnasium.vector import SyncVectorEnv
from ray.rllib import BaseEnv, Policy
from ray.rllib.algorithms.callbacks import DefaultCallbacks
from ray.rllib.core.rl_module import RLModule
from ray.rllib.env.env_runner import EnvRunner
from ray.rllib.evaluation.episode_v2 import EpisodeV2
from ray.rllib.utils.metrics.metrics_logger import MetricsLogger
from ray.rllib.utils.typing import EpisodeType, PolicyID

from mrkwatkins.oakemuai.gymnasium import OakEmuEnv


class RecordingCallbacks(DefaultCallbacks):
    # -1 to record the first episode.
    episode_count = -1

    def __init__(self, experiment_directory: str, record_every_nth_episode: int):
        super().__init__()
        self.recordings_directory = os.path.join(experiment_directory, "recordings")
        self.n = record_every_nth_episode
        self.recorders = {}

        if not os.path.exists(self.recordings_directory):
            os.makedirs(self.recordings_directory)

    def setup(self):
        pass

    def on_episode_start(
        self,
        *,
        episode: EpisodeType | EpisodeV2,
        env_runner: Optional["EnvRunner"] = None,
        metrics_logger: MetricsLogger | None = None,
        env: Env | None = None,
        env_index: int,
        rl_module: RLModule | None = None,
        # TODO (sven): Deprecate these args.
        worker: Optional["EnvRunner"] = None,
        base_env: BaseEnv | None = None,
        policies: dict[PolicyID, Policy] | None = None,
        **kwargs,
    ) -> None:
        RecordingCallbacks.episode_count += 1
        if RecordingCallbacks.episode_count & self.n != 0:
            return

        episode_id = episode.id_
        sync_vector_env = cast(SyncVectorEnv, env)
        env: OakEmuEnv = sync_vector_env.envs[0].unwrapped

        filename = f"recording_{datetime.now():%Y-%m-%d_%H-%M-%S}.oer"

        path = os.path.join(self.recordings_directory, filename)
        self.recorders[episode_id] = env.spectrum.record_oer(path)

    def on_episode_end(
        self,
        *,
        episode: EpisodeType | EpisodeV2,
        env_runner: Optional["EnvRunner"] = None,
        metrics_logger: MetricsLogger | None = None,
        env: Env | None = None,
        env_index: int,
        rl_module: RLModule | None = None,
        # TODO (sven): Deprecate these args.
        worker: Optional["EnvRunner"] = None,
        base_env: BaseEnv | None = None,
        policies: dict[PolicyID, Policy] | None = None,
        **kwargs,
    ) -> None:
        episode_id = episode.id_
        if episode_id in self.recorders:
            self.recorders[episode_id].stop()
            del self.recorders[episode_id]
