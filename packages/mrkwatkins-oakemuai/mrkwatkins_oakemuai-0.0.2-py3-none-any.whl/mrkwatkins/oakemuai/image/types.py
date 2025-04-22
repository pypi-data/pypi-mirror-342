import numpy as np
from MrKWatkins.OakEmu.Machines.ZXSpectrum.AI.Image import AIImageStack as DotNetAIImageStack  # noqa
from System import Double as DotNetDouble  # noqa
from System import Half as DotNetHalf  # noqa
from System import Single as DotNetFloat  # noqa
from System import Type as DotNetType  # noqa

type_map = {"Half": np.dtype(np.float16), "Single": np.dtype(np.float32), "Double": np.dtype(np.float64)}


def dot_net_type_to_dtype(dot_net_type: DotNetType) -> np.dtype:
    numpy_type = type_map.get(dot_net_type.Name, None)
    if numpy_type is None:
        raise ValueError(f"The .NET type {dot_net_type.Name} is not supported.")
    return numpy_type
