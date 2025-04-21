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


class DeleteFolder:
    async def delete_folder(
        self: "pyroitaly.Client",
        folder_id: int
    ) -> bool:
        """Delete a user's folder.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            folder_id (``int``):
                Unique identifier (int) of the target folder.

        Returns:
            ``bool``: True, on success.

        Example:
            .. code-block:: python

                # Delete folder
                app.delete_folder(folder_id)
        """
        r = await self.invoke(
            raw.functions.messages.UpdateDialogFilter(
                id=folder_id
            )
        )

        return r
