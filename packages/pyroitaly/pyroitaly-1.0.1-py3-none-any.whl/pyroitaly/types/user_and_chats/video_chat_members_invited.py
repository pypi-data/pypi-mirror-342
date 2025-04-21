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

from typing import List, Dict

from pyroitaly import raw, types
from ..object import Object


class VideoChatMembersInvited(Object):
    """A service message about new members invited to a voice chat.


    Parameters:
        users (List of :obj:`~pyroitaly.types.User`):
            New members that were invited to the voice chat.
    """

    def __init__(
        self, *,
        users: List["types.User"]
    ):
        super().__init__()

        self.users = users

    @staticmethod
    def _parse(
        client,
        action: "raw.types.MessageActionInviteToGroupCall",
        users: Dict[int, "raw.types.User"]
    ) -> "VideoChatMembersInvited":
        users = [types.User._parse(client, users[i]) for i in action.users]

        return VideoChatMembersInvited(users=users)
