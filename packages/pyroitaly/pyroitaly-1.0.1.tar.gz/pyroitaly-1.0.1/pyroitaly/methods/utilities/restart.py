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


class Restart:
    async def restart(
        self: "pyroitaly.Client",
        block: bool = True
    ):
        """Restart the Client.

        This method will first call :meth:`~pyroitaly.Client.stop` and then :meth:`~pyroitaly.Client.start` in a row in
        order to restart a client using a single method.

        Parameters:
            block (``bool``, *optional*):
                Blocks the code execution until the client has been restarted. It is useful with ``block=False`` in case
                you want to restart the own client within an handler in order not to cause a deadlock.
                Defaults to True.

        Returns:
            :obj:`~pyroitaly.Client`: The restarted client itself.

        Raises:
            ConnectionError: In case you try to restart a stopped Client.

        Example:
            .. code-block:: python

                from pyroitaly import Client

                app = Client("my_account")


                async def main():
                    await app.start()
                    ...  # Invoke API methods
                    await app.restart()
                    ...  # Invoke other API methods
                    await app.stop()


                app.run(main())
        """

        async def do_it():
            await self.stop()
            await self.start()

        if block:
            await do_it()
        else:
            self.loop.create_task(do_it())

        return self
