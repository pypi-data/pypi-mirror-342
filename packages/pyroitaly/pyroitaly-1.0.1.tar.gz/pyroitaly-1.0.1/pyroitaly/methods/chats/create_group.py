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

from typing import Union, List

import pyroitaly
from pyroitaly import raw
from pyroitaly import types


class CreateGroup:
    async def create_group(
        self: "pyroitaly.Client",
        title: str,
        users: Union[Union[int, str], List[Union[int, str]]]
    ) -> "types.Chat":
        """Create a new basic group.

        .. note::

            If you want to create a new supergroup, use :meth:`~pyroitaly.Client.create_supergroup` instead.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            title (``str``):
                The group title.

            users (``int`` | ``str`` | List of ``int`` or ``str``):
                Users to create a chat with.
                You must pass at least one user using their IDs (int), usernames (str) or phone numbers (str).
                Multiple users can be invited by passing a list of IDs, usernames or phone numbers.

        Returns:
            :obj:`~pyroitaly.types.Chat`: On success, a chat object is returned.

        Example:
            .. code-block:: python

                await app.create_group("Group Title", user_id)
        """
        if not isinstance(users, list):
            users = [users]

        r = await self.invoke(
            raw.functions.messages.CreateChat(
                title=title,
                users=[await self.resolve_peer(u) for u in users]
            )
        )

        return types.Chat._parse_chat(self, r.chats[0])
