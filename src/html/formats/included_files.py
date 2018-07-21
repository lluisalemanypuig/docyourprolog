
# Format string 'f' so that it opens the html file corresponding to
# the html documentation of the source file 'f'.pl
def included_file(hw, f, href):
	hw.open_list_element()
	hw.open_paragraph()
	hw.open_a({"href" : href})
	hw.put(f)
	hw.close_tag()
	hw.close_tag()
	hw.close_tag()
