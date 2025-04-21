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
from pyroitaly import raw, types, utils
from ..object import Object


class StoryForwardHeader(Object):
    """Contains information about origin of forwarded story.


    Parameters:
        user (:obj:`~pyroitaly.types.User`, *optional*):
            Sender of the story.

        sender_name (``str``, *optional*):
            For stories forwarded from users who have hidden their accounts, name of the user.
        
        chat (:obj:`~pyroitaly.types.Chat`, *optional*):
            Sender of the story. If the story is from channel.

        story_id (``int``):
            Unique identifier for the original story.

        is_modified (``bool``):
            True, if the story is modified.
    """

    def __init__(
        self, *,
        user: "types.User" = None,
        sender_name: str = None,
        chat: "types.Chat" = None,
        story_id: int = None,
        is_modified: bool = None
    ):
        super().__init__()

        self.user = user
        self.sender_name = sender_name
        self.chat = chat
        self.story_id = story_id
        self.is_modified = is_modified

    async def _parse(
        client: "pyroitaly.Client",
        fwd_header: "raw.types.StoryFwdHeader"
    ) -> "StoryForwardHeader":
        user = None
        chat = None
        if fwd_header.from_peer is not None:
            if isinstance(fwd_header.from_peer, raw.types.PeerChannel):
                chat = await client.get_chat(utils.get_channel_id(fwd_header.from_peer.channel_id))
            elif isinstance(fwd_header.from_peer, raw.types.InputPeerSelf):
                user = client.me
            else:
                user = await client.get_users(fwd_header.from_peer.user_id)
        
        return StoryForwardHeader(
            user=user,
            sender_name=fwd_header.from_name,
            chat=chat,
            story_id=fwd_header.story_id,
            is_modified=fwd_header.modified
        )
