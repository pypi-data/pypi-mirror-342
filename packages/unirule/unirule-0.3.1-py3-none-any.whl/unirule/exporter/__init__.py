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


from typing import TextIO


class BaseExporter:
    def __init__(self) -> None:
        self.ir: list[dict] = []

    def set_ir(self, ir: list[dict]) -> None:
        self.ir = ir

    def export(self, stream: TextIO) -> None:
        """Export something according to the IR.

        Arguments:
            stream -- TextIO object to write in

        Raises:
            NotImplementedError: when directly called on BaseExporter
        """
        raise NotImplementedError()
