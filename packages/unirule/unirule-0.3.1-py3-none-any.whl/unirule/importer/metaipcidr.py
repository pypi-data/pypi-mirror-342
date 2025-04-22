# Copyright (C) 2024 TargetLocked
#
# This file is part of unirule.
#
# unirule is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# unirule is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with unirule.  If not, see <https://www.gnu.org/licenses/>.

import ipaddress
from typing import TextIO, final, override

import yaml

from unirule.exception import InvalidInputError
from unirule.importer import BaseImporter
from unirule.util import minify_rule

# https://wiki.metacubex.one/config/rule-providers/content/#ipcidr


def _trans_ipcidr(value: str) -> str:
    value = value.strip()
    try:
        ipaddress.ip_network(value)
    except ValueError:
        raise InvalidInputError(f"invalid IPCIDR: {value}") from None
    return value


# N rule items -> 1 rule item
def _import_metaipcidr(items: list[str]) -> dict:
    result = {"ip_cidr": [_trans_ipcidr(item) for item in items]}
    return minify_rule(result)


@final
class MetaIpcidrYamlImporter(BaseImporter):
    @override
    def import_(self, stream: TextIO) -> None:
        doc = yaml.load(stream, yaml.Loader)
        # format: { payload: [] }
        self.ir = [_import_metaipcidr(doc["payload"])]


@final
class MetaIpcidrTextImporter(BaseImporter):
    @override
    def import_(self, stream: TextIO) -> None:
        self.ir = [_import_metaipcidr(stream.readlines())]
