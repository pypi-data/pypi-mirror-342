"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2022
SEE COPYRIGHT NOTICE BELOW
"""

import typing as h

import numpy as nmpy

try:
    import matplotlib.colors as colr
except ModuleNotFoundError:
    colr = None
else:
    AsHex = lambda _: colr.to_hex(_).upper()
    AsRGB1 = colr.to_rgb
    AsRGB255 = lambda _: nmpy.round(255.0 * nmpy.array(colr.to_rgb(_))).astype(
        nmpy.uint8
    )


assert colr, "No module found for color conversion."


array_t = nmpy.ndarray

_FORMAT_FROM_LENGTH = {1: "g", 2: "ga", 3: "rgb", 4: "rgba"}


def NColorsAndFormat(color: h.Any, /) -> tuple[int, str]:
    """"""
    if isinstance(color, str):
        if color[0] == "#":
            format_ = "hex"
        else:
            format_ = "name"
        return 1, format_

    # Note: array_t's are not typing sequences.
    if isinstance(color, h.Sequence):  # i.e. true sequence, not str.
        first_color = color[0]  # or first component of color if just one.

        if isinstance(first_color, h.Sequence | array_t):  # including str.
            _, format_ = NColorsAndFormat(first_color)
            return color.__len__(), format_

        format_length = color.__len__()
        if isinstance(first_color, int):
            format_max = 255
        else:
            format_max = 1
        return 1, f"{_FORMAT_FROM_LENGTH[format_length]}{format_max}"

    if isinstance(color, array_t):
        if color.ndim == 1:
            format_length = color.size
            if nmpy.issubdtype(color.dtype, nmpy.integer):
                format_max = 255
            else:
                format_max = 1
            return 1, f"{_FORMAT_FROM_LENGTH[format_length]}{format_max}"

        assert color.ndim == 2

        _, format_ = NColorsAndFormat(color[0, :])
        return color.shape[0], format_

    raise ValueError(f"Unknown color format {color}.")


def NewConvertedColor(
    color: h.Any | h.Sequence[h.Any],
    format_color: h.Literal["hex", "rgb1", "rgb255"],
    /,
    *,
    sequence_or_reduction: (
        int | h.Literal["min", "mean", "median", "max"] | type | h.Callable | None
    ) = None,
) -> h.Any:
    """"""
    # TODO: Full implementation, i.e. including with several colors output.
    if format_color == "rgb1":
        AsOutputFormat = AsRGB1
    elif format_color == "rgb255":
        AsOutputFormat = AsRGB255
    elif format_color == "hex":
        AsOutputFormat = AsHex
    else:
        raise ValueError(f"Unknown output format {format_color}.")

    if (
        (not isinstance(color, str))
        and (isinstance(color, h.Sequence) and isinstance(color[0], h.Sequence))
    ) or (isinstance(color, array_t) and (color.ndim == 2)):
        # Notes: The first h.Sequence is implicitly tuple | list, or other "true" (i.e.
        # not str) sequence types, and color can be of any length.
        # The second h.Sequence is implicitly tuple | list, other "true" sequence types,
        # or str. If str and the color is in Hex format, its length is either 4 (e.g.,
        # #RGB <=> #RRGGBB), 5 (e.g., #RGBA <=> #RRGGBBAA), 7 (e.g., #RRGGBB) or 9
        # (e.g., #RRGGBBAA). If not str, then color is a sequence of 3 or 4 integers in
        # [0, 255] or floats in [0, 1].
        if isinstance(sequence_or_reduction, int):
            return AsOutputFormat(color[sequence_or_reduction])
        elif isinstance(sequence_or_reduction, str):
            raise NotImplementedError
        return sequence_or_reduction(tuple(AsOutputFormat(_) for _ in color))

    return AsOutputFormat(color)


"""
COPYRIGHT NOTICE

This software is governed by the CeCILL  license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights,  and the successive licensors  have only  limited
liability.

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or
data to be ensured and,  more generally, to use and operate it in the
same conditions as regards security.

The fact that you are presently reading this means that you have had
knowledge of the CeCILL license and that you accept its terms.

SEE LICENCE NOTICE: file README-LICENCE-utf8.txt at project source root.

This software is being developed by Eric Debreuve, a CNRS employee and
member of team Morpheme.
Team Morpheme is a joint team between Inria, CNRS, and UniCA.
It is hosted by the Centre Inria d'Université Côte d'Azur, Laboratory
I3S, and Laboratory iBV.

CNRS: https://www.cnrs.fr/index.php/en
Inria: https://www.inria.fr/en/
UniCA: https://univ-cotedazur.eu/
Centre Inria d'Université Côte d'Azur: https://www.inria.fr/en/centre/sophia/
I3S: https://www.i3s.unice.fr/en/
iBV: http://ibv.unice.fr/
Team Morpheme: https://team.inria.fr/morpheme/
"""
