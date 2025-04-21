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
from pyroitaly import raw

from typing import Union

class UpdatePersonalChat:
    async def update_personal_chat(
        self: "pyroitaly.Client",
        chat_id: Union[int, str]
    ) -> bool:
        """Update your birthday details.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int``):
                Unique identifier (int) of the target channel.
                You can also use channel public link in form of *t.me/<username>* (str).

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Update your personal chat
                await app.update_personal_chat(chat_id=-1001234567890)
        """
        chat = await self.resolve_peer(chat_id)
        r = await self.invoke(raw.functions.account.UpdatePersonalChannel(channel=chat))
        if r:
            return True
        return False
