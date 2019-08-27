import csv
import os
import pprint
from collections import OrderedDict
from os.path import join as oj

import simplejson
import xmltodict
from termcolor import colored, cprint

# @2d0: add functionality to read and parse data from xlsx files


pp = pprint.PrettyPrinter(indent=4)

scan_dir = os.path.join(os.getcwd(), "data")


def dir_mkr(specified_path):
	if not os.path.isdir(specified_path):
		os.makedirs(specified_path)


def walker(mydir):
	# reads directory for files we need
	# then returns a dictionary of file
	# types with file paths as list values per file type
	
	file_list = {"csv": [], "xml": [], "json": []}
	
	for root, dirs, fls in os.walk(mydir):
		
		for f in fls:
			
			f_abs = oj(root, f)
			
			# skips & removes '.DS_Store' fls
			if f.startswith('.'):
				os.remove(f_abs)
				continue
			
			if f_abs.endswith(".csv"):
				file_list["csv"].append(f_abs)
			elif f_abs.endswith(".xml"):
				file_list["xml"].append(f_abs)
			elif f_abs.endswith(".json"):
				file_list["json"].append(f_abs)
	
	return file_list


def data_dump(data_dict):
	
	dump_file = "parsed_data.json"
	
	if os.path.exists(dump_file):
		print(colored("FILE", "red"), colored("EXISTS!", "yellow"))
		print()
		
		# if input(colored("remove existing file?", "sky_blue_2"), colored("y", 'green')) == 'y'
		
		# print('%s%s y/N %s%s' % (colored.fg('orchid'), colored.attr('bold'), colored.attr('reset'), colored.bg('white')))
		
		
		while True:
			ans = input(colored("remove existing file?", "red", "on_grey", attrs=["bold"]) + " ")
			
			print()
			
			if ans.lower() == 'y':
				os.remove(dump_file)
				print(colored("file ", "red", "on_grey", attrs=['underline', 'bold']),
				      colored(" removed", "grey", "on_red", attrs=['underline', 'bold']), sep="")
				break
				
			elif ans.lower() == 'n':
				
				# print('%s%s file preserved %s%s' % (
				# colored.fg('sky_blue_2'), colored.attr('bold'), colored.attr('reset'), colored.bg('white')))
				print(colored("file ", "blue", "on_yellow", attrs=['underline', 'bold']), colored(" preserved", "yellow", "on_blue", attrs=['underline', 'bold']),
				      # colored("(file not deleted, but also no new file written)", "green"),
				      sep="")
				
				return
			
			else:
				cprint("BAD INPUT! TRY AGAIN!", 'red', attrs=['bold'])
				
				continue
	
	print()

	if isinstance(data_dict, dict):
		with open(dump_file, "w") as json_writer:
			simplejson.dump(data_dict, json_writer, indent=4)
		
		json_writer.close()
		print(
			# colored("file saved: ", "magenta"),
			"new file saved: ",
			colored(dump_file, "red", "on_yellow", attrs=["dark", "bold"]),
			sep=""
		)
	
	else:
		cprint("BAD OBJECT TYPE\nDATA DUMP FAILED", 'red', attrs=['bold'])


def csv_parser(csv_files, debug=False):
	
	csv_data = {}
	
	for c_file in csv_files:
		
		if debug:
			print(colored(c_file, "red"))
		
		reader = csv.DictReader(open(c_file, "r"))
		
		dict_list = []
		
		for line in reader:
			dict_list.append(dict(line))
	
		if "DESC" in dict_list[0].keys():
			csv_data['listings'] = dict_list
		
		elif "AGENT_CODE" in dict_list[0].keys():
			csv_data['agents'] = dict_list
		
		elif "OFFICE_CODE" in dict_list[0].keys():
			csv_data['offices'] = dict_list
	
	return csv_data


def json_parser(json_files, debug=False):
	
	json_data = {'listings': [], 'agents': [], 'offices': []}
	
	for f in json_files:
		
		with open(f) as j_file:
			data = simplejson.load(j_file)
		
		for d in data:
			json_data['listings'] += [{"mls_number": d['mls_number'],
			                 "address": d['street_address'],
			                 "city": d['city'],
			                 "state": d['state'],
			                 "zip": d['zip'],
			                 "price": d['price'],
			                 "status": d['status'],
			                 "type": d['type'],
			                 "agent_code": d['agent_code'],
			                 "office_code": d['office_code'],
			                 "description": d['description']}]
			
			json_data['agents'] += [
				{"name": d["agent_name"],
				"agent_code": d["agent_code"],
				"office_code": d["office_code"],
				"phone": d["office_phone"],
				"city": d["city"],
				"state": d["state"],
				"zip": d["zip"]}
			]
			
			json_data['offices'] += [
				{"name": d["office_name"],
				 "office_code": d["office_code"],
				 "phone": d["office_phone"],
				 "city": d["city"],
				 "state": d["state"],
				 "zip": d["zip"]
				 }
			]
	
	# # standard print
	# print(json_data)

	if debug:
		# pretty printer
		pprnt = pprint.PrettyPrinter(indent=4)
		pprnt.pprint(json_data)
	
	return json_data
	
	pass


def xml_parser(xml_files, debug=False):
	
	for xf in xml_files:
		
		with open(xf) as fd:
			doc = dict(xmltodict.parse(fd.read()))
		
		data = list(doc['listings']['listing'])
		
		master_data = {"listings": []}
		
		# go through all listings data
		for d in data:
			d = dict(d)
			
			tmp_dict = {}
			
			for key, val in d.items():
				
				if isinstance(val, OrderedDict):
					
					if debug:
						# //db&t
						print(key, end=":\t")
						print(dict(val))
						# //db&tt
					
					tmp_dict[key] = dict(val)
					
				
				else:
					if debug:
						# //db&t
						print(key, val, sep=":\t")
						# //db&t
					tmp_dict[key] = val
			
			master_data['listings'].append(tmp_dict)
		
		xml_data = {"listings": [], "agents": [], "offices": []}
		
		for e, data in enumerate(master_data['listings']):
			td = {}
			
			# flatten out data to a single dictionary
			td['address'] = data['address']['street']
			td['city'] = data['address']['city']
			td['zip'] = data['address']['zip']
			td['state'] = data['address']['state']
			td['price'] = data['price']
			td['description'] = data['description']
			td['status'] = data['status']
			td['type'] = data['type']
			td['office_code'] = data['broker']['code']
			td['office_phone'] = data['broker']['phone']
			td['office_name'] = data['broker']['name']
			td['agent_name'] = data['agent']['name']
			td['agent_phone'] = data['agent']['phone']
			td['agent_code'] = data['agent']['code']
			td['mls_number'] = data['mls_number']
			
			# # extract data for offices
			# xml_data['offices'].append({
			# 	"office_code": td['office_code'],
			# 	"name": td['office_name'],
			# 	"phone": td['office_phone'],
			# 	"city": td['city'],
			# 	"state": td['state'],
			# 	"zip": td['zip'],
			#
			# 	# # technically office city/state/zip aren't
			# 	# # specified in the XML data, so in case
			# 	# # it's not supposed to be assumed: USE BELOW
			# 	# # otherwise, use above data
			# 	# "city": "N/A",
			# 	# "state": "N/A",
			# 	# "zip": "N/A",
			# })
			
			# # extract data for agents
			# xml_data['agents'].append({
			# 	'agent_name': td['agent_name'],
			# 	'agent_code': td['agent_code'],
			# 	'office_code': td['office_code'],
			# 	'agent_phone': td['agent_phone'],
			# 	'city': td['city'],
			# 	'state': td['state'],
			# 	'zip': td['zip'],
			#
			# 	# # technically agent city/state/zip aren't
			# 	# # specified in the XML data, so in case
			# 	# # it's not supposed to be assumed: USE BELOW
			# 	# # otherwise, use above data
			# 	# "city": "N/A",
			# 	# "state": "N/A",
			# 	# "zip": "N/A",
			# })
			
			# extract data for listings
			
			xml_data['listings'].append({
				'mls_number': td['mls_number'],
				'address': td['address'],
				'city': td['city'],
				'state': td['state'],
				'zip': td['zip'],
				'price': td['price'],
				'status': td['status'],
				'type': td['type'],
				'agent_code': td['agent_code'],
				'office_code': td['office_code'],
				'description': td['description'],
			})
			
			
			
			
			
			pass
		
		return xml_data


def main(base_dir=scan_dir, debug=False):
	
	files = walker(base_dir)
	
	all_parsed_data = {
		'csv': csv_parser(files['csv']),
		'json': json_parser(files['json']),
		'xml': xml_parser(files['xml'])
	}
	
	if debug:
		pprint.pprint(all_parsed_data, indent=4)
	
	data_dump(all_parsed_data)




if __name__ == "__main__":
	
	main()













