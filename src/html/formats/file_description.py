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

# Title of a file
def file_title(hw, filename):
	hw.open_h1()
	hw.put("Documentation for Prolog file: " + filename)
	hw.close_tag()

# Format a string that corresponds to the author of a file
def file_author(hw, author):
	hw.open_paragraph()
	hw.open_bold()
	hw.put("By: ")
	hw.close_tag()
	hw.open_italics()
	hw.put(author)
	hw.close_tag()
	hw.close_tag()

# Format a string that corresponds to the date of creation of a file
def file_date(hw, date):
	hw.open_paragraph()
	hw.open_bold()
	hw.put("On: ")
	hw.close_tag()
	hw.open_italics()
	hw.put(date)
	hw.close_tag()
	hw.close_tag()
