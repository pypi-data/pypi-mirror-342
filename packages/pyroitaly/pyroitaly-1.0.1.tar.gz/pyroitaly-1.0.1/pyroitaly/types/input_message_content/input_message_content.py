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

import pyroitaly

from ..object import Object


class InputMessageContent(Object):
    """Content of a message to be sent as a result of an inline query.

    Telegram clients currently support the following 5 types:

    - :obj:`~pyroitaly.types.InputTextMessageContent`
    - :obj:`~pyroitaly.types.InputLocationMessageContent`
    - :obj:`~pyroitaly.types.InputVenueMessageContent`
    - :obj:`~pyroitaly.types.InputContactMessageContent`
    - :obj:`~pyroitaly.types.InputInvoiceMessageContent`

    """

    def __init__(self):
        super().__init__()

    async def write(self, client: "pyroitaly.Client", reply_markup):
        raise NotImplementedError
