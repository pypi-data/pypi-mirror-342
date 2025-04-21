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

from uuid import uuid4

import pyroitaly
from pyroitaly import types
from ..object import Object


class InlineQueryResult(Object):
    """One result of an inline query.

    - :obj:`~pyroitaly.types.InlineQueryResultCachedAudio`
    - :obj:`~pyroitaly.types.InlineQueryResultCachedDocument`
    - :obj:`~pyroitaly.types.InlineQueryResultCachedAnimation`
    - :obj:`~pyroitaly.types.InlineQueryResultCachedPhoto`
    - :obj:`~pyroitaly.types.InlineQueryResultCachedSticker`
    - :obj:`~pyroitaly.types.InlineQueryResultCachedVideo`
    - :obj:`~pyroitaly.types.InlineQueryResultCachedVoice`
    - :obj:`~pyroitaly.types.InlineQueryResultArticle`
    - :obj:`~pyroitaly.types.InlineQueryResultAudio`
    - :obj:`~pyroitaly.types.InlineQueryResultContact`
    - :obj:`~pyroitaly.types.InlineQueryResultDocument`
    - :obj:`~pyroitaly.types.InlineQueryResultAnimation`
    - :obj:`~pyroitaly.types.InlineQueryResultLocation`
    - :obj:`~pyroitaly.types.InlineQueryResultPhoto`
    - :obj:`~pyroitaly.types.InlineQueryResultVenue`
    - :obj:`~pyroitaly.types.InlineQueryResultVideo`
    - :obj:`~pyroitaly.types.InlineQueryResultVoice`
    """

    def __init__(
        self,
        type: str,
        id: str,
        input_message_content: "types.InputMessageContent",
        reply_markup: "types.InlineKeyboardMarkup"
    ):
        super().__init__()

        self.type = type
        self.id = str(uuid4()) if id is None else str(id)
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup

    async def write(self, client: "pyroitaly.Client"):
        pass
