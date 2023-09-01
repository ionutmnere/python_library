import sys
import os
import re

# This script work only in windows so far.
# Please configure below constants as you need

SEPARATOR = ", "
OUTPUT_FILE = 'result.csv'
COMMITS_LINK_ROOT_PATH = None
HEADER = "count" + SEPARATOR + "commit" + SEPARATOR + "merge" + SEPARATOR + "author" + SEPARATOR + "date";
MERGE_COMMIT_ENTRY_LEN = 4
NO_MERGE_COMMIT_ENTRY_LEN = 3
index = 0


def add_line_in_output_file(line):
	f = open(OUTPUT_FILE, "a")
	f.write(line + '\n')
	f.close


def construct_line(p_entry, p_merge):
	global index
	index = index+1
	commit = str(p_entry[0])
	commit_short = commit[0:11]
	if COMMITS_LINK_ROOT_PATH is not None:
		commit = '[' + commit_short + '](' + COMMITS_LINK_ROOT_PATH + commit + ')'
	if p_merge:
		merge = p_entry[1]
		author = p_entry[2]
		date = p_entry[3]
	else:
		merge = "N/A"
		author = p_entry[1]
		date = p_entry[2]
	return str(index) + SEPARATOR + commit + SEPARATOR + merge + SEPARATOR + author + SEPARATOR + date

def add_entry_in_csv(entry):
	if MERGE_COMMIT_ENTRY_LEN == len(entry):
		line = construct_line(p_entry = entry, p_merge=True)
	elif NO_MERGE_COMMIT_ENTRY_LEN == len(entry):
		line = construct_line(p_entry = entry, p_merge = False)
	add_line_in_output_file(line)

if len(sys.argv) < 2:
	print("Please provide input file with git history!")
	exit()

print("input file provided: " + sys.argv[1])
if not os.path.isfile(sys.argv[1]):
	print("File " + sys.argv[1] + " does not exist!")
	exit()

print("File exists, processing...")
f = open(sys.argv[1], "r", errors="ignore")
lines = f.readlines()
f.close();
if len(lines) < 1:
	print("File is empty!")
	exit()

print("Content in file: " + str(len(lines)) + " lines.")
str_gen = (str(element) for element in lines)
str_lines = "".join(str_gen)

if os.path.isfile(OUTPUT_FILE):
	os.remove(OUTPUT_FILE)
	add_line_in_output_file(HEADER)
	print("Old entries deleted from " + OUTPUT_FILE)

merge_commits = re.findall(r'commit\s*(\S*)\nMerge:\s*([^\n]*)\n\s*Author:\s*([^\n]*)\n\s*Date: \s*([^\n]*)', str_lines, re.MULTILINE)
if 0 == len(merge_commits):
	print("No merge commits found!")
else:
	print("Found " + str(len(merge_commits)) + " merge commits.")
	for entry in merge_commits:
		add_entry_in_csv(entry);
	print("Merge commits added in output file.")

no_merge_commits = re.findall(r'^commit\s*(\S*)\n\s*Author:\s*([^\n]*)\n\s*Date: \s*([^\n]*)', str_lines, re.MULTILINE)
if 0 == len(no_merge_commits):
	print("No regular commits found!")
else:
	print("Found " + str(len(no_merge_commits)) + " regular commits.")
	for entry in no_merge_commits:
		add_entry_in_csv(entry);
	print("Regular commits added in output file.")
output_full_path = os.path.join(os.getcwd(),  OUTPUT_FILE)
if os.path.isfile(output_full_path):
	os.system("start EXCEL.EXE " + output_full_path)
else:
	print("Warning, something really bad happened: " + OUTPUT_FILE + " not found!")
