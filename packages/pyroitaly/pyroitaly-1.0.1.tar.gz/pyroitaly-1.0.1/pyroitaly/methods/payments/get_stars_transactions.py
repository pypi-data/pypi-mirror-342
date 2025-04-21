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
from pyroitaly import types
from typing import Union


class GetStarsTransactions:
    async def get_stars_transactions(
        self: "pyroitaly.Client",
        chat_id: Union[int, str] = "me",
        limit: int = 0,
        offset: str = "",
        is_inbound: bool = None,
        is_outbound: bool = None,
        is_ascending: bool = None
    ) -> "types.StarsStatus":
        """Get stars transactions.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the target user.
                You can also use chat public link in form of *t.me/<username>* (str).
                default to self.
                only for bots.

            limit (``int``, *optional*):
                Limits the number of transactions to be retrieved.

            offset (``str``, *optional*):
                Offset the list of transactions to be retrieved.

            is_inbound (``bool``, *optional*):
                True, if only inbound transactions should be retrieved.

            is_outbound (``bool``, *optional*):
                True, if only outbound transactions should be retrieved.

            is_ascending (``bool``, *optional*):
                True, if transactions should be returned in ascending order.

        Example:
            .. code-block:: python

                # get all transactions
                app.get_stars_transactions()

                # get all inbound transactions
                app.get_stars_transactions(is_inbound=True)

                # get all outbound transactions
                app.get_stars_transactions(is_outbound=True)

                # get all transactions in ascending order
                app.get_stars_transactions(is_ascending=True)

        Returns:
            :obj:`~pyroitaly.types.StarsStatus`: On success, a :obj:`~pyroitaly.types.StarsStatus` object is returned.
        """
        peer = await self.resolve_peer(chat_id)

        r = await self.invoke(
            raw.functions.payments.GetStarsTransactions(
                peer=peer,
                limit=limit,
                offset=offset,
                inbound=is_inbound,
                outbound=is_outbound,
                ascending=is_ascending
            )
        )
        return types.StarsStatus._parse(self, r)
