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
