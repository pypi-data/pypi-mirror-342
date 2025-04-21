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

from enum import auto

from .auto_name import AutoName


class StoriesPrivacyRules(AutoName):
    """Stories privacy rules type enumeration used in :meth:`~pyroitaly.Client.send_story` and :meth:`~pyroitaly.Client.edit_story`."""

    PUBLIC = auto()
    "Public stories"

    CLOSE_FRIENDS = auto()
    "Close_Friends stories"

    CONTACTS = auto()
    "Contacts only stories"

    PRIVATE = auto()
    "Private stories"

    NO_CONTACTS = auto()
    "Hide stories from contacts"
