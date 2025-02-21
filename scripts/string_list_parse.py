# Michael Johnson - Feb 2024
# Simple Python Script to convert from lines of lists to just string text (seperated by lines of values from lists)

import sys
import ast

full_file_string = (sys.argv[1])

working_string = ""

lines_of_file = full_file_string.splitlines()

for list in lines_of_file:
    list_value = ast.literal_eval(list)
    working_string += list_value[0]
    working_string += "\n"

print(working_string)
