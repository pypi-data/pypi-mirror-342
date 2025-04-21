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

from typing import Union

import pyroitaly
from pyroitaly import raw
from pyroitaly import enums

class UpdateColor:
    async def update_color(
        self: "pyroitaly.Client",
        chat_id: Union[int, str],
        color: Union["enums.ReplyColor", "enums.ProfileColor"],
        background_emoji_id: int = None
    ) -> bool:
        """Update color

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            color (:obj:`~pyroitaly.enums.ReplyColor` | :obj:`~pyroitaly.enums.ProfileColor`):
                Color type.
                Profile color can only be set for the user.

            background_emoji_id (``int``, *optional*):
                Unique identifier of the custom emoji.

        Returns:
            ``bool``: On success, in case the passed-in session is authorized, True is returned.

        Example:
            .. code-block:: python

                await app.update_color(chat_id, enums.ReplyColor.RED)
        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerSelf):
            r = await self.invoke(
                raw.functions.account.UpdateColor(
                    for_profile=isinstance(color, enums.ProfileColor),
                    color=color.value,
                    background_emoji_id=background_emoji_id
                )
            )
        else:
            r = await self.invoke(
                raw.functions.channels.UpdateColor(
                    channel=peer,
                    color=color.value,
                    background_emoji_id=background_emoji_id
                )
            )

        return bool(r)