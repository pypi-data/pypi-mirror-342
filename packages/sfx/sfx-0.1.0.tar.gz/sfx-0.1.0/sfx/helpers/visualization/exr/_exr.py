"""Helpers to read/write gtlf/glb files."""

import jax
import jax.numpy as jnp
from typing import List, Optional, Tuple

try:
    import OpenEXR
    import Imath
except ImportError as e:
    __all__ = []
    raise e
else:
    __all__ = ["data_to_exr"]
finally:
    pass


def data_to_exr(
    *data: jax.Array,
    data_channels: Optional[List[str] | Tuple[str]] = None,
    filenames: Optional[List[str] | Tuple[str]] = None,
):

    if data_channels is None:
        data_channels = ["R", "G", "B", "A", "Z"]

    if filenames is None:
        nbdigit = len(str(len(data)))
        filenames = [
            f"image_{{i:0<{nbdigit}d}}".format(i=i) for i, _ in enumerate(data)
        ]

    for datum, channels, filename in zip(data, data_channels, filenames):
        width, height, nbchan = datum.shape
        header = OpenEXR.Header(width, height)
        header["channels"] = {
            channel: Imath.Channel(Imath.PixelType(Imath.PixelType.FLOAT))
            for channel, _ in zip(channels, range(nbchan))
        }
        header["compression"] = Imath.Compression(Imath.Compression.DWAA_COMPRESSION)

        out = OpenEXR.OutputFile(f"{filename}.exr", header)
        out.writePixels(
            {
                channel: datum[..., c].astype(jnp.float32).tobytes()
                for c, channel in enumerate(channels)
            }
        )
        out.close()
    return None


if __name__ == "__main__":
    pass
