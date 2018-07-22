"""
Special sequences of characters that should not appear in the
documentation of the code.
"""

# indicate new 'paragraph'
new_line = '<!*>'

# verbatim
open_verbatim = '<--'
close_verbatim = '-->'

# Item list
open_item_list = '<++'
close_item_list = '++>'
item_list = '!>'

newlinel = len(new_line)
overbl = len(open_verbatim)
cverbl = len(close_verbatim)
olistl = len(open_item_list)
clistl = len(close_item_list)
liteml = len(item_list)
