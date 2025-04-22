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

import copy
import re
from dataclasses import dataclass
from typing import Optional, TextIO, final, override

from unirule.exception import InvalidInputError
from unirule.importer import BaseImporter
from unirule.util import incapable_input, minify_rule, unreachable


@dataclass
class _AdgResult:
    normal_rule: dict
    important_rule: dict
    normal_exception: dict
    important_exception: dict


# (is_exception, is_important, pattern)
def _parse_line(line: str) -> Optional[tuple[bool, bool, str]]:
    line = line.strip()
    # comments or blank lines
    if line.startswith("!") or line.startswith("#") or len(line) == 0:
        return None
    # exception marker
    is_exception = line.startswith("@@")
    line = line.removeprefix("@@")
    # split pattern and modifiers
    if line.startswith("/"):
        # regex, note "/" and "$" are legal in regex
        idx_end = line.rfind("/")
        pattern = line[: idx_end + 1]
        mod_str = line[idx_end + 1 :]
        if mod_str.startswith("$"):
            modifiers = mod_str.removeprefix("$").split(",")
        else:
            modifiers = []
    else:
        idx_mod = line.rfind("$")
        if idx_mod == -1:
            # no mods
            pattern = line
            modifiers = []
        else:
            # has mods
            pattern = line[:idx_mod]
            modifiers = line[idx_mod + 1 :].split(",")
    is_important = False
    for mod in modifiers:
        match mod:
            case "important":
                is_important = True
            case "dnsrewrite=0.0.0.0":
                pass
            case _:
                incapable_input(f"unsupported modifier: {mod}")
                return None
    return is_exception, is_important, pattern


def _any_char_in_text(chars: str, text: str) -> bool:
    for ch in chars:
        if ch in text:
            return True
    return False


def _parse_pattern(pattern: str, result: dict) -> None:
    original_pattern = pattern
    if pattern.startswith("/"):
        result["domain_regex"].append(pattern.removeprefix("/").removesuffix("/"))
    else:
        # "|" as end marker
        is_suffix = pattern.endswith("|")
        pattern = pattern.removesuffix("|")
        # "^"
        is_suffix |= pattern.endswith("^")
        pattern = pattern.removesuffix("^")
        # subdomain
        is_subdomain = pattern.startswith("||")
        pattern = pattern.removeprefix("||")
        # "|" as start marker
        is_prefix = pattern.startswith("|")
        pattern = pattern.removeprefix("|")
        # sb prefix marker
        is_prefix |= pattern.startswith("://")
        pattern = pattern.removeprefix("://")
        # done with "^" and "|", only allow "*"
        if (is_subdomain and is_prefix) or _any_char_in_text("^|", pattern):
            raise InvalidInputError(f"bad pattern: {original_pattern}")
        if "*" in pattern:
            # domain_regex
            regex = r".*".join(re.escape(part) for part in pattern.split("*"))
            if is_suffix:
                regex += r"$"
            if is_prefix:
                regex = r"^" + regex
            if is_subdomain:
                regex = r"^([^\.]+\.)*" + regex
            result["domain_regex"].append(regex)
        else:
            # here is_prefix and is_subdomain cant be both true
            match is_prefix, is_suffix:
                case True, True:
                    # must domain
                    result["domain"].append(pattern)
                case False, True:
                    if is_subdomain or pattern.startswith("."):
                        # must domain_suffix
                        result["domain_suffix"].append(pattern)
                    else:
                        # suffix but not prefix, also not subdomain -> literal suffix
                        result["domain_regex"].append(
                            r"^.*" + re.escape(pattern) + r"$"
                        )
                case False, False:
                    if is_subdomain:
                        # subdomain only -> regex
                        result["domain_regex"].append(
                            r"^([^\.]+\.)*" + re.escape(pattern)
                        )
                    else:
                        # must domain_keyword
                        result["domain_keyword"].append(pattern)
                case True, False:
                    # prefix but not suffix -> regex
                    result["domain_regex"].append(r"^" + re.escape(pattern) + r".*$")
                case _:
                    unreachable()


# N rule lines -> 4 components
def _import_adg(lines: list[str]) -> _AdgResult:
    def unitary_rule():
        return {
            "domain": [],
            "domain_suffix": [],
            "domain_keyword": [],
            "domain_regex": [],
        }

    result = _AdgResult(
        normal_rule=unitary_rule(),
        important_rule=unitary_rule(),
        normal_exception=unitary_rule(),
        important_exception=unitary_rule(),
    )
    for line in lines:
        parsed = _parse_line(line)
        if parsed is None:
            continue
        is_exception, is_important, pattern = parsed
        match is_exception, is_important:
            case True, True:
                _parse_pattern(pattern, result.important_exception)
            case True, False:
                _parse_pattern(pattern, result.normal_exception)
            case False, True:
                _parse_pattern(pattern, result.important_rule)
            case False, False:
                _parse_pattern(pattern, result.normal_rule)
            case _:
                unreachable()
    return _AdgResult(
        normal_rule=minify_rule(result.normal_rule),
        important_rule=minify_rule(result.important_rule),
        normal_exception=minify_rule(result.normal_exception),
        important_exception=minify_rule(result.important_exception),
    )


def _minify_logicial(rule: dict) -> dict:
    new_subrules = [item for item in rule["rules"] if len(item) > 0]
    match len(new_subrules):
        case 0:
            return {}
        case 1:
            return new_subrules[0]
    new_rule = rule.copy()
    new_rule["rules"] = new_subrules
    return new_rule


@final
class AdguardDnsImporter(BaseImporter):
    @override
    def import_(self, stream: TextIO) -> None:
        adgresult = _import_adg(stream.readlines())
        # for multiple output
        self.adg_result = copy.deepcopy(adgresult)
        # add invert
        if len(adgresult.important_exception) > 0:
            adgresult.important_exception["invert"] = True
        if len(adgresult.normal_exception) > 0:
            adgresult.normal_exception["invert"] = True
        # ((normal_rule && !normal_exception) || important_rule) && !important_exception
        merged = _minify_logicial(
            {
                "type": "logical",
                "mode": "and",
                "rules": [adgresult.normal_rule, adgresult.normal_exception],
            }
        )
        merged = _minify_logicial(
            {
                "type": "logical",
                "mode": "or",
                "rules": [merged, adgresult.important_rule],
            }
        )
        merged = _minify_logicial(
            {
                "type": "logical",
                "mode": "and",
                "rules": [merged, adgresult.important_exception],
            }
        )
        self.ir = [merged]
