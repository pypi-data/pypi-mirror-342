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

import datetime
import pyroitaly
from pyroitaly import raw, utils

from ..object import Object


class BotBusinessConnection(Object):
    """A bot business connection Information.

    Parameters:
        bot_connection_id (``str``):
            The business connection identifier.
        
        user (:obj:`~pyroitaly.types.User`):
            The user that connected to the bot.

        dc_id (``int``):
            The user datacenter.

        date (:py:obj:`~datetime.datetime`):
            Date the connection was established in Unix time.

        can_reply (``bool``, *optional*):
            Whether the bot can reply.

        is_disabled (``bool``, *optional*):
            Whether the connection is disabled.
    """
    def __init__(
        self,
        *,
        client: "pyroitaly.Client" = None,
        bot_connection_id: str,
        user: "pyroitaly.types.User",
        dc_id: int,
        date: "datetime.datetime",
        can_reply: bool = None,
        is_disabled: bool = None
    ):
        super().__init__(client)

        self.bot_connection_id = bot_connection_id
        self.user = user
        self.dc_id = dc_id
        self.date = date
        self.can_reply = can_reply
        self.is_disabled = is_disabled

    @staticmethod
    async def _parse(
        client: "pyroitaly.Client",
        bot_connection: "raw.types.BotBusinessConnection"
    ) -> "BotBusinessConnection":
        return BotBusinessConnection(
            bot_connection_id = bot_connection.connection_id,
            user = await client.get_users(bot_connection.user_id),
            dc_id = bot_connection.dc_id,
            date = utils.timestamp_to_datetime(bot_connection.date),
            can_reply = bot_connection.can_reply,
            is_disabled = bot_connection.disabled,
            client=client
        )
