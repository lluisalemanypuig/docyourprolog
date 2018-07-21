
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
