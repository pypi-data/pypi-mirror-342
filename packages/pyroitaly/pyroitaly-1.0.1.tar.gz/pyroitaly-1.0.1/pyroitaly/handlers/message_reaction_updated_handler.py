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

from typing import Callable

from .handler import Handler


class MessageReactionUpdatedHandler(Handler):
    """The MessageReactionUpdated handler class.
    Used to handle changes in the reaction of a message.

    It is intended to be used with :meth:`~pyroitaly.Client.add_handler`.

    For a nicer way to register this handler, have a look at the
    :meth:`~pyroitaly.Client.on_message_reaction_updated` decorator.

    Parameters:
        callback (``Callable``):
            Pass a function that will be called when a new MessageReactionUpdated event arrives. It takes
            *(client, message_reaction_updated)* as positional arguments (look at the section below for a detailed
            description).

        filters (:obj:`Filters`):
            Pass one or more filters to allow only a subset of updates to be passed in your callback function.

    Other parameters:
        client (:obj:`~pyroitaly.Client`):
            The Client itself, useful when you want to call other API methods inside the handler.

        message_reaction_updated (:obj:`~pyroitaly.types.MessageReactionUpdated`):
            The received message reaction update.
    """

    def __init__(self, callback: Callable, filters=None):
        super().__init__(callback, filters)