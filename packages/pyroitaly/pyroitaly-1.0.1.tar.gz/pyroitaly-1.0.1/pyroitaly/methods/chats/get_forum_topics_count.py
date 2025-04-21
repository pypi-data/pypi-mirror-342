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

import logging
from typing import Union, Optional, AsyncGenerator

import pyroitaly
from pyroitaly import raw
from pyroitaly import types

log = logging.getLogger(__name__)


class GetForumTopicsCount:
    async def get_forum_topics_count(
        self: "pyroitaly.Client",
        chat_id: Union[int, str]
    ) -> Optional[AsyncGenerator["types.ForumTopic", None]]:
        """Get forum topics count from a chat.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

        Returns:
            ``int``: On success, the count of forum topics is returned.

        Example:
            .. code-block:: python

                # get all forum topics count
                app.get_forum_topics_count(chat_id)

        Raises:
            ValueError: In case of invalid arguments.
        """

        peer = await self.resolve_peer(chat_id)

        rpc = raw.functions.channels.GetForumTopics(channel=peer, offset_date=0, offset_id=0, offset_topic=0, limit=0)

        r = await self.invoke(rpc, sleep_threshold=-1)

        return r.count
