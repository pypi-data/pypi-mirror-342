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

from typing import List

from pyroitaly import raw, types

from ..object import Object
from .message import Str


class TranslatedText(Object):
    """A translated text with entities.

    Parameters:
        text (``str``):
            Translated text.

        entities (``str``, *optional*):
            Entities of the text.
    """

    def __init__(
        self,
        *,
        text: str,
        entities: List["types.MessageEntity"] = None
    ):
        self.text = text
        self.entities = entities

    @staticmethod
    def _parse(
        client,
        translate_result: "raw.types.TextWithEntities"
    ) -> "TranslatedText":
        entities = [
            types.MessageEntity._parse(client, entity, {})
            for entity in translate_result.entities
        ]
        entities = types.List(filter(lambda x: x is not None, entities))

        return TranslatedText(
            text=Str(translate_result.text).init(entities) or None, entities=entities or None
        )
