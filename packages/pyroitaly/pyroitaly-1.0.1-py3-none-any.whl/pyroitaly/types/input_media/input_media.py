#  PyroItaly - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
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

from typing import List, Union, BinaryIO

from ..messages_and_media import MessageEntity
from ..object import Object


class InputMedia(Object):
    """Content of a media message to be sent.

    It should be one of:

    - :obj:`~pyroitaly.types.InputMediaAnimation`
    - :obj:`~pyroitaly.types.InputMediaDocument`
    - :obj:`~pyroitaly.types.InputMediaAudio`
    - :obj:`~pyroitaly.types.InputMediaPhoto`
    - :obj:`~pyroitaly.types.InputMediaVideo`
    """

    def __init__(
        self,
        media: Union[str, BinaryIO],
        caption: str = "",
        parse_mode: str = None,
        caption_entities: List[MessageEntity] = None
    ):
        super().__init__()

        self.media = media
        self.caption = caption
        self.parse_mode = parse_mode
        self.caption_entities = caption_entities
