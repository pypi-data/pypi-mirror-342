#  PyroItaly - Telegram MTProto API Client Library for Python
#  Copyright (C) 2022-present ItalyMusic <https://github.com/ItalyMusic>
#
#  This file is part of PyroItaly.
#
#  PyroItaly is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PyroItaly is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with PyroItaly.  If not, see <http://www.gnu.org/licenses/>.

from pyroitaly import types

from ..object import Object


class InputMediaArea(Object):
    """Content of a media area to be included in story.

    PyroItaly currently supports the following types:

    - :obj:`~pyroitaly.types.InputMediaAreaChannelPost`
    """

    # TODO: InputMediaAreaVenue

    def __init__(
        self,
        coordinates: "types.MediaAreaCoordinates"
    ):
        super().__init__()

        self.coordinates = coordinates
