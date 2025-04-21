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

from typing import List, Union

import pyroitaly
from pyroitaly import raw


class GetSimilarBots:
    async def get_similar_bots(
        self: "pyroitaly.Client",
        bot: Union[int, str]
    ) -> List["pyroitaly.types.User"]:
        """Get a list of bots similar to the target bot.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            bot (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target bot.

        Returns:
            List of :obj:`~pyroitaly.types.User`: On success.
        """
        peer = await self.resolve_peer(bot)
        r = await self.invoke(raw.functions.bots.GetBotRecommendations(bot=peer))
        return pyroitaly.types.List([
            pyroitaly.types.User._parse(self, u)
            for u in r.users
        ])
