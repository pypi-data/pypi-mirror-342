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

import pyroitaly

from pyroitaly import types
from typing import Union

class GetMessageReadParticipants:
    async def get_message_read_participants(
        self: "pyroitaly.Client",
        chat_id: Union[int, str],
        message_id: int
    ):
        """Get the list of users who have read a message.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            message_id (``int``):
                Unique identifier of the target message.

        Returns:
            ``AsyncGenerator``: On success, an async generator yielding :obj:`~pyroitaly.types.ReadParticipant` objects is returned.
        """

        peer = await self.resolve_peer(chat_id)
        r = await self.invoke(
            pyroitaly.raw.functions.messages.GetMessageReadParticipants(
                peer=peer,
                msg_id=message_id
            )
        )
        for read_participant in r:
            yield await types.ReadParticipant._parse(
                client=self,
                read_participant=read_participant
            )
