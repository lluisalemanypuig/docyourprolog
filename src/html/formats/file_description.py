
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
