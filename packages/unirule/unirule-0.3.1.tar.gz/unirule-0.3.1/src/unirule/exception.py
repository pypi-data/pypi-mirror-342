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


class InvalidInputError(Exception):
    pass


class IncapableInputError(Exception):
    """It is recommended to use util.incapable_input instead."""

    pass


class IncapableOutputError(Exception):
    """It is recommended to use util.incapable_output instead."""

    pass


class BadIrError(Exception):
    pass
