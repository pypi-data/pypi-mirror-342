#  PyroItaly - Telegram MTProto API Client Library for Python
#  Copyright (C) 2020 Cezar H. <https://github.com/usernein>
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
from pyroitaly.types import Listener

class RemoveListener:
    def remove_listener(
        self: "pyroitaly.Client",
        listener: Listener
    ):
        """Removes a listener from the :meth:`~pyroitaly.Client.listeners` dictionary.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            listener (:obj:`~pyroitaly.types.Listener`):
                The listener to remove.
        """
        try:
            self.listeners[listener.listener_type].remove(listener)
        except ValueError:
            pass
