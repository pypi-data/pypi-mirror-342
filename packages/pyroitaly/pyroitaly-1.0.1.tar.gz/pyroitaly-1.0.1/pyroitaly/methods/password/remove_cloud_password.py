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
from pyroitaly import raw
from pyroitaly.utils import compute_password_check


class RemoveCloudPassword:
    async def remove_cloud_password(
        self: "pyroitaly.Client",
        password: str
    ) -> bool:
        """Turn off the Two-Step Verification security feature (Cloud Password) on your account.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            password (``str``):
                Your current password.

        Returns:
            ``bool``: True on success.

        Raises:
            ValueError: In case there is no cloud password to remove.

        Example:
            .. code-block:: python

                await app.remove_cloud_password("password")
        """
        r = await self.invoke(raw.functions.account.GetPassword())

        if not r.has_password:
            raise ValueError("There is no cloud password to remove")

        await self.invoke(
            raw.functions.account.UpdatePasswordSettings(
                password=compute_password_check(r, password),
                new_settings=raw.types.account.PasswordInputSettings(
                    new_algo=raw.types.PasswordKdfAlgoUnknown(),
                    new_password_hash=b"",
                    hint=""
                )
            )
        )

        return True
