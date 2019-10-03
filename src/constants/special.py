"""
docyourprolog - Prolog parser for documentation generation
Copyright (C) 2018 Lluís Alemany Puig

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Contact: Lluís Alemany Puig (lluis.alemany.puig@gmail.com)
"""

"""
Special sequences of characters that should not appear in the
documentation of the code.
"""

# indicate new 'paragraph'
new_line = '\\newline'

# verbatim
open_verbatim = '\\bverbatim'
close_verbatim = '\\everbatim'

# Item list
open_item_list = '\\blist'
close_item_list = '\\elist'
item_list = '\\item'

newlinel = len(new_line)
overbl = len(open_verbatim)
cverbl = len(close_verbatim)
olistl = len(open_item_list)
clistl = len(close_item_list)
liteml = len(item_list)
