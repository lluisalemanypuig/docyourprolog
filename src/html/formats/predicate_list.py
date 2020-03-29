"""
docyourprolog - Prolog parser for documentation generation
Copyright (C) 2018,2019,2020 Lluís Alemany Puig

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

# Format a string 'label' as an element in the predicate list
# at the beginning of each file with a hyperlink 'href'.
def predicate_in_list(hw, label, href):
	hw.open_list_element()
	hw.open_paragraph()
	hw.open_a({"href" : "#" + href})
	hw.put(label)
	hw.close_tag()
	hw.close_tag()
	hw.close_tag()
