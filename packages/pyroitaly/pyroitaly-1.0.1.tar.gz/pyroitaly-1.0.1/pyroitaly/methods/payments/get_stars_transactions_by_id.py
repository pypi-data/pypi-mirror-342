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
from typing import Union, List


class GetStarsTransactionsById:
    async def get_stars_transactions_by_id(
        self: "pyroitaly.Client",
        transaction_ids: Union[
            "types.InputStarsTransaction",
            List["types.InputStarsTransaction"]
        ],
        chat_id: Union[int, str] = "me"
    ) -> "types.StarsStatus":
        """Get stars transactions by transaction id.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            transaction_ids (:obj:`~pyroitaly.types.InputStarsTransaction` | List of :obj:`~pyroitaly.types.InputStarsTransaction`):
                Pass a single transaction identifier or an iterable of transaction ids (as integers) to get the content of the
                transaction themselves

            chat_id (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the target user.
                You can also use chat public link in form of *t.me/<username>* (str).
                default to self.
                only for bots.

        Example:
            .. code-block:: python

                # get one transaction by id
                from pyroitaly.types import InputStarsTransaction
                app.get_stars_transactions_by_id(InputStarsTransaction(id="transaction_id"))

                # get multiple transactions by id
                from pyroitaly.types import InputStarsTransaction
                app.get_stars_transactions_by_id([
                    InputStarsTransaction(id="transaction_id_1"),
                    InputStarsTransaction(id="transaction_id_2")
                ])

                # get one transaction by id from a specific user
                from pyroitaly.types import InputStarsTransaction
                app.get_stars_transactions_by_id(InputStarsTransaction(id="transaction_id"), chat_id="username")

                # get multiple transaction by id from a specific user
                from pyroitaly.types import InputStarsTransaction
                app.get_stars_transactions_by_id([
                    InputStarsTransaction(id="transaction_id_1"),
                    InputStarsTransaction(id="transaction_id_2")
                ], chat_id="username")

        Returns:
            :obj:`~pyroitaly.types.StarsStatus`: On success, a :obj:`~pyroitaly.types.StarsStatus` object is returned.
        """
        peer = await self.resolve_peer(chat_id)
        is_iterable = not isinstance(transaction_ids, types.InputStarsTransaction)
        ids = [await transaction_ids.write()] if not is_iterable else [await x.write() for x in transaction_ids]

        r = await self.invoke(
            raw.functions.payments.GetStarsTransactionsByID(
                peer=peer,
                id=ids
            )
        )
        return types.StarsStatus._parse(self, r)
