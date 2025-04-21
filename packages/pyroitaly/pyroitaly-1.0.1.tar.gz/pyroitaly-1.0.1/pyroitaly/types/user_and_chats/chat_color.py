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

from typing import Optional, Union

from pyroitaly import raw
from pyroitaly import enums
from ..object import Object


class ChatColor(Object):
    """Reply or profile color status.

    Parameters:
        color (:obj:`~pyroitaly.enums.ReplyColor` | :obj:`~pyroitaly.enums.ProfileColor`, *optional*):
            Color type.

        background_emoji_id (``int``, *optional*):
            Unique identifier of the custom emoji.
    """

    def __init__(
        self,
        *,
        color: Union["enums.ReplyColor", "enums.ProfileColor"] = None,
        background_emoji_id: int = None
    ):
        self.color = color
        self.background_emoji_id = background_emoji_id

    @staticmethod
    def _parse(color: "raw.types.PeerColor" = None) -> Optional["ChatColor"]:
        if not color:
            return None

        return ChatColor(
            color=enums.ReplyColor(color.color) if getattr(color, "color", None) else None,
            background_emoji_id=getattr(color, "background_emoji_id", None)
        )

    @staticmethod
    def _parse_profile_color(color: "raw.types.PeerColor" = None) -> Optional["ChatColor"]:
        if not color:
            return None

        return ChatColor(
            color=enums.ProfileColor(color.color) if getattr(color, "color", None) else None,
            background_emoji_id=getattr(color, "background_emoji_id", None)
        )