import ctypes

import numpy as np
from MrKWatkins.OakEmu.Machines.ZXSpectrum.AI.Image import AIImageStack as DotNetAIImageStack  # noqa

from mrkwatkins.oakemuai.image.types import dot_net_type_to_dtype


# noinspection PyTypeChecker
def ai_image_stack_to_ndarray(image_stack: DotNetAIImageStack) -> np.ndarray:
    element_type = dot_net_type_to_dtype(image_stack.ElementType)

    numpy = np.ndarray((image_stack.Size, image_stack.Height, image_stack.Width), order="C", dtype=element_type)
    destination_pointer = numpy.__array_interface__["data"][0]
    raw_data = image_stack.UnsafeGetRawData()
    try:
        for source_pointer in raw_data:
            ctypes.memmove(destination_pointer, source_pointer.ToInt64(), raw_data.ByteSizeOfImage)
            destination_pointer += raw_data.ByteSizeOfImage
        return numpy
    finally:
        raw_data.Dispose()
