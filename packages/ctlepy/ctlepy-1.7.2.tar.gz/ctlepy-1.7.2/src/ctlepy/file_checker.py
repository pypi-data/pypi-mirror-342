# ctle Copyright (c) 2024 Ulrik Lindahl
# Licensed under the MIT license https://github.com/Cooolrik/ctle/blob/main/LICENSE

import os
import re

class line_define:
	'''line_define defines one of the lines to be checked. Positive values of row (1-indexed) are counted from the first row (1 == first row). Negative values are counted from the last row (-1 == last row)'''
	def __init__( self, row:int, line_exp:str, line_example:str=None ):
		self.row = row
		self.line_exp = re.compile( line_exp )
		self.line_example = line_example if line_example != None else line_exp
		if not self.line_exp.match( self.line_example ):
			raise Exception("Invalid setup, the line_exp must be able to match line_example")

def check_file_lines( file_path:str, line_defines:list[line_define] ) -> list[int]:
	'''Checks the file using the line_defines. A list of mismatching defines is returned, or an empty list if all lines match.'''
	
	# read all lines, with whitespace stripped out
	with open(file_path, 'r') as file:
		lines = [line.strip() for line in file.readlines()]
		file.close()

	# remove empty lines in the end of the file
	while not lines[-1].strip():
		lines.pop()

	# check each line in line_defines, make sure it matches
	mismatch_list = []
	for inx,line_def in enumerate(line_defines):
		
		# calculate the row to check
		line_inx = line_def.row - 1
		if line_def.row < 0:
			line_inx = len(lines) + line_def.row
		if line_inx < 0 or line_inx >= len(lines):
			mismatch_list.append(inx)
			continue

		# check the line, using the regular expression
		if not line_def.line_exp.match(lines[line_inx]):
			mismatch_list.append(inx)
			continue

	# return list of mismatches. if it is empty, everything matches
	return mismatch_list
	
def fix_file( file_path:str, line_defines:list[line_define] ) -> bool:
	'''Fixes a file which fails the checks, by inserting the correct lines. Returns False if the line_defines are not correct, or if the file could not be fixed.'''
	
	# read in the file verbatim, but make sure there is a newline at the end of the last line
	with open(file_path, 'r') as file:
		lines = file.readlines()
		file.close()
	lines[-1] = lines[-1].rstrip() + '\n'

	# calculate how many lines to insert at the beginning and end of the file
	insert_lines_begin = 0
	insert_lines_end = 0
	for line_def in line_defines:
		insert_lines_begin = max( line_def.row, insert_lines_begin )
		insert_lines_end = max( -line_def.row, insert_lines_end )

	# allocated the empty lines
	lines = [''] * insert_lines_begin + lines + [''] * insert_lines_end

	# replace the allocated lines with correct ones
	for line_def in line_defines:
		
		# calculate the row to check
		line_inx = line_def.row - 1
		if line_def.row < 0:
			line_inx = len(lines) + line_def.row
		if line_inx < 0 or line_inx >= len(lines):
			print(f"Error: Could not fix file, line index {line_inx} out of range")
			return False

		lines[line_inx] = line_def.line_example + '\n'

	# write the fixed file
	try:
		with open(file_path, 'w') as file:
			file.writelines(lines)
			file.close()
	except:
		print(f"Error: Could not fix file, writing failed")
		return False
	
	return True