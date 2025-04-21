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

import re
import pyroitaly
from pyroitaly import raw


class ApplyGiftCode:
    async def apply_gift_code(
        self: "pyroitaly.Client",
        link: str,
    ) -> bool:
        """Apply a gift code.
        .. include:: /_includes/usable-by/users.rst
        Parameters:
            link (``str``):
                The gift code link.
        Returns:
            ``bool``: On success, True is returned.
        Raises:
            ValueError: In case the gift code link is invalid.
        Example:
            .. code-block:: python
                # apply a gift code
                app.apply_gift_code("t.me/giftcode/abc1234567def")
        """
        match = re.match(r"^(?:https?://)?(?:www\.)?(?:t(?:elegram)?\.(?:org|me|dog)/(?:giftcode/|\+))([\w-]+)$", link)
        if match:
            slug = match.group(1)
        elif isinstance(link, str):
            slug = link
        else:
            raise ValueError("Invalid gift code link")
        await self.invoke(
            raw.functions.payments.ApplyGiftCode(
                slug=slug
            )
        )
        return True
