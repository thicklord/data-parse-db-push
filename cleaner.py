import json
import os
import pprint
import re
from collections import OrderedDict
# all termcolor attributes: ["bold","dark","underline","blink","reverse","concealed"]
# text colors: [grey, red, green, yellow, blue, magenta, cyan, white]
# highlight colors: [on_grey, on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan, on_white]
#
from os.path import join as oj


# ————————————————————————————————————————


def dir_mkr(specified_path):
	if not os.path.isdir(specified_path):
		os.makedirs(specified_path)


def walker(mydir):
	for root, dirs, files in os.walk(mydir):
		
		for f in files:
			
			f_abs = oj(root, f)
			
			# skips & removes '.DS_Store' files
			if f.startswith('.'):
				os.remove(f_abs)
				continue


def sort_dict(dct: dict):
	
	return dict(OrderedDict(sorted(dct.items(), key=lambda t: t[0])))


def cleaner(dict_data: dict):
	"""
	cleans data by replacing bad/invalid
	values (i.e. '\n' characters), setting
	all keys to lower case, type setting
	integers from string for all-digit values
	"""
	
	cleaned_data = {}
	
	# iterate over all dictionary keys
	for category_key in list(dict_data.keys()):
		
		cleaned_data[category_key] = []
		
		for c in dict_data[category_key]:
			# # //db&t
			# print(c)
			# break
			# # //db&t
			
			tmp_dct = {}
			
			for k, v in dict(c).items():
				# # //db&t
				# print(k, v, sep=": \t")
				# # //db&t
				
				# convert all keys to lower-case
				k = str(k).lower()
				
				# remove all '\n' characters from description
				if not isinstance(v, int):
					if "\n" in v:
						v = re.sub(r"\n", " ", v, flags=re.DOTALL)
				
				# convert integer values to integers
				if bool(re.match(r"^[0-9]+$", str(v))):
					v = int(v)
				
				# # //db&t
				# # testing if string values are integers or not
				# print(v)
				# print(bool(re.match(r"^[0-9]+$", str(v))))
				# # //db&t
				
				# replaces 'desc' with 'description
				if k == "desc":
					k = "description"
				
				# # cleans data according to database formatting
				# replace 'agent_name' with 'name'
				if category_key == "agents" and k == "agent_name":
					k = "name"
				# replace 'agent_phone' with 'phone'
				if category_key == "agents" and k == "agent_phone":
					k = "phone"
				
				# replace 'agent_code' with 'agent_id'
				# ONLY in listings dictionary as per
				# database column requirments
				if category_key == "listings" and k == "agent_code":
					k = "agent_id"
				# replace 'office_code' with 'office_id'
				# ONLY in listings dictionary as per
				# database column requirments
				if category_key == "listings" and k == "office_code":
					k = "office_id"
				
				
				tmp_dct[str(k).lower()] = v
			
			# remove office code from agent data
			if category_key == "agents":
				tmp_dct.pop("office_code")
			# # //db&t
			# print(tmp_dct)
			# break
			# # //db&t
			cleaned_data[category_key].append(sort_dict(tmp_dct))
			
			pass
	
	# outputs the number of each sub_dict was cleaned
	for category_key in list(cleaned_data.keys()):
		print("%s: %d entries" % (category_key, len(cleaned_data[category_key])))
	
	return cleaned_data
	
	pass


def combiner(d: dict):
	# combines data from all three filetypes
	# and joins them by type value
	combined_data = {'listings': [], 'agents': [], 'offices': []}
	
	# # 3 first layer keys: [csv, json, xml]
	# listings join
	for e in d['csv']['listings']:
		combined_data['listings'].append(e)
	for e in d['xml']['listings']:
		combined_data['listings'].append(e)
	for e in d['json']['listings']:
		combined_data['listings'].append(e)
	
	# agents join
	for e in d['csv']['agents']:
		combined_data['agents'].append(e)
	for e in d['xml']['agents']:
		combined_data['agents'].append(e)
	for e in d['json']['agents']:
		combined_data['agents'].append(e)
	
	# offices join
	for e in d['csv']['offices']:
		combined_data['offices'].append(e)
	for e in d['xml']['offices']:
		combined_data['offices'].append(e)
	for e in d['json']['offices']:
		combined_data['offices'].append(e)
	
	# returns dictionary in format:
	# {'listings': [], 'agents': [], 'offices': []}
	return combined_data
	
	pass


# noinspection PyUnusedLocal,PyUnreachableCode
def query(d: dict):
	"""
	function for testing and viewing data for functional access
	"""
	
	for key in list(d.keys()):
		
		# cleaned_data[key] = []
		
		print(key, d[key][0].keys(), sep=": ")
		
		continue
		
		for c in d[key]:
			# # //db&t
			# print(c)
			# break
			# # //db&t
			c = dict(c)
			
			# print(key, list(c.keys()), sep=": ")
			# continue
			
			if key == "listings":
				print(c["agent_code"], c["office_code"])
			
			# for k, v in dict(c).items():
			# 	# # //db&t
			# 	# print(k, v, sep=": \t")
			# 	# # //db&t
			#
			# 	# convert all keys to lower-case
			# 	k = str(k).lower()
			#
			# 	# remove all '\n' characters from description
			# 	if not isinstance(v, int):
			# 		if "\n" in v:
			# 			v = re.sub(r"\n", " ", v, flags=re.DOTALL)
			#
			# 	# convert integer values to integers
			# 	if bool(re.match(r"^[0-9]+$", str(v))):
			# 		v = int(v)
			#
			# 	# # //db&t
			# 	# # testing if string values are integers or not
			# 	# print(v)
			# 	# print(bool(re.match(r"^[0-9]+$", str(v))))
			# 	# # //db&t
			#
			# 	# replaces 'desc' with 'description
			# 	if k == "desc":
			# 		k = "description"
			#
			# 	tmp_dct[str(k).lower()] = v
			pass
			# # quick check to see what type of values are held in "mls_number"
			# if "mls_number" in c.keys():
			# 	print(c["mls_number"], type(c["mls_number"]), sep=": ")
			
			pass
	
	pass


def main():
	# read file in
	read_file = oj("parsed_data.json")
	
	# read JSON file into dictionary
	with open(read_file, 'r') as fin:
		data = dict(json.load(fin))
	
	# indented printing method
	pp = pprint.PrettyPrinter(indent=4)
	
	# variable to hold combined data results
	cdata = combiner(data)
	
	# variable holder for cleaned data
	squeaky = cleaner(cdata)
	
	# write to file for easier viewing
	with open("cleaned_data.json", 'w') as fout:
		json.dump(squeaky, fout, indent=4)

# # //db&t
# query(squeaky)
# # //db&t


if __name__ == "__main__":
	main()
