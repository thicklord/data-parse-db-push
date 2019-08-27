import parser
import cleaner
import db_writer
import time
from termcolor import colored
import sys
import os



# @2d0: add functionality to pass a directory path
#  from command line as well as take other args

args = sys.argv[1:]

# if a path is passed as the first argument,
# use that as the scan directory for the parser
if args[0] and os.path.isdir(args[0]):
	parser.main(base_dir=args[0])
	print(colored("parsing complete", "green", "on_white"))
	time.sleep(5)

# if not, use the default path that is set
else:
	parser.main()
	print(colored("parsing complete", "green", "on_white"))
	time.sleep(5)

cleaner.main()
print(colored("data cleaning complete", "yellow", "on_blue"))
time.sleep(5)

db_writer.main()
print(colored("database updated with all of parsed and cleaned data", "blue", "on_white"))




