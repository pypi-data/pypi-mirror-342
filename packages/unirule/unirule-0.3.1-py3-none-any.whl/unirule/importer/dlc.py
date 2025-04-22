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

from typing import TextIO, final, override

from unirule.importer import BaseImporter
from unirule.util import Registry, minify_rule

# for line prefix
_reg = Registry()


@_reg.key_handler("domain")
def _trans_domain_suffix(value: str, result: dict) -> None:
    result["domain_suffix"].append(value)


@_reg.key_handler("full")
def _trans_domain(value: str, result: dict) -> None:
    result["domain"].append(value)


@_reg.key_handler("keyword")
def _trans_domain_keyword(value: str, result: dict) -> None:
    result["domain_keyword"].append(value)


@_reg.key_handler("regexp")
def _trans_domain_regex(value: str, result: dict) -> None:
    result["domain_regex"].append(value)


# N rule lines -> 1 rule item
def _import_dlc(lines: list[str]) -> dict:
    result = {
        "domain": [],
        "domain_suffix": [],
        "domain_keyword": [],
        "domain_regex": [],
    }
    for line in lines:
        # remove EOLs
        line = line.strip()
        # remove attributes
        for idx in [line.find(sep) for sep in (" @", ":@")]:
            if idx != -1:
                line = line[:idx].strip()
        if ":" not in line:
            # default
            prefix = "domain"
            content = line
        else:
            prefix, content = line.split(":")
        # translate
        trans_func = _reg.get(prefix)
        trans_func(content, result)
    return minify_rule(result)


@final
class DlcImporter(BaseImporter):
    @override
    def import_(self, stream: TextIO) -> None:
        self.ir = [_import_dlc(stream.readlines())]
