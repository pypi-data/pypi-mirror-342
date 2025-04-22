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

import yaml

from unirule.exception import InvalidInputError
from unirule.importer import BaseImporter
from unirule.util import minify_rule

# https://wiki.metacubex.one/handbook/syntax/#_8


# Wildcard "."
def _trans_special_domain_suffix(value: str, result: dict) -> None:
    if "+" in value:
        raise InvalidInputError(f'rule "{value}": conflicting wildcards "." and "+"')
    if "*" in value:
        raise InvalidInputError(f'rule "{value}": conflicting wildcards "." and "*"')
    result["domain_suffix"].append(value)


# Wildcard "+"
def _trans_general_domain_suffix(value: str, result: dict) -> None:
    new_value = value.removeprefix("+.")
    if "+" in new_value:
        raise InvalidInputError(f'rule "{value}": duplicated wildcards "+"')
    if "*" in new_value:
        raise InvalidInputError(f'rule "{value}": conflicting wildcards "+" and "*"')
    result["domain_suffix"].append(new_value)


# Wildcard "*"
def _trans_domain_regex(value: str, result: dict) -> None:
    if "+" in value:
        raise InvalidInputError(f'rule "{value}": conflicting wildcards "*" and "+"')
    domain_parts = value.split(".")
    # convert wildcard to regex
    domain_parts = [(r"[^\.]+" if part == "*" else part) for part in domain_parts]
    regex = r"\.".join(domain_parts)
    # prevent substring match
    regex = r"^" + regex + r"$"
    result["domain_regex"].append(regex)


# no wildcard
def _trans_domain(value: str, result: dict) -> None:
    if "+" in value:
        raise InvalidInputError(f'rule "{value}": incorrect usage of "+"')
    result["domain"].append(value)


# N rule items -> 1 rule item
def _import_metadomain(items: list[str]) -> dict:
    result = {
        "domain": [],
        "domain_suffix": [],
        "domain_regex": [],
    }
    # We assume the input is legal here.
    # Error handling may go to corresponding functions.
    for item in items:
        # remove EOLs for text format
        item = item.strip()
        if item.startswith("."):
            # "."
            _trans_special_domain_suffix(item, result)
        else:
            if item.startswith("+."):
                # "+"
                _trans_general_domain_suffix(item, result)
            elif "*" in item:
                # "*"
                _trans_domain_regex(item, result)
            else:
                # no wildcard (hopefully)
                _trans_domain(item, result)
    return minify_rule(result)


@final
class MetaDomainYamlImporter(BaseImporter):
    @override
    def import_(self, stream: TextIO) -> None:
        doc = yaml.load(stream, yaml.Loader)
        # format: { payload: [] }
        self.ir = [_import_metadomain(doc["payload"])]


@final
class MetaDomainTextImporter(BaseImporter):
    @override
    def import_(self, stream: TextIO) -> None:
        self.ir = [_import_metadomain(stream.readlines())]
