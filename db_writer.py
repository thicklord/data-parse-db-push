import json
import sqlite3 as sq3
import sys
from os import getcwd as og
# all termcolor attributes: ["bold","dark","underline","blink","reverse","concealed"]
# text colors: [grey, red, green, yellow, blue, magenta, cyan, white]
# highlight colors: [on_grey, on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan, on_white]
#
from os.path import join as oj

db_file_location = oj(og(), "data", "homes.com", "homes.db")


def push_data_db(data_dict: dict):
	con = None
	
	for table_name in list(dict(data_dict).keys()):
		
		for sub_dict in data_dict[table_name]:
			try:
				con = sq3.connect(db_file_location)
				curs = con.cursor()
				
				table_columns = ', '.join(sub_dict.keys())
				table_placeholders = ':' + ', :'.join(sub_dict.keys())
				
				table_query = """INSERT INTO %s (%s) VALUES (%s)""" % (table_name, table_columns, table_placeholders)
				
				print(table_query)
				
				curs.execute(table_query, sub_dict)
				con.commit()
			
			except sq3.Error as SE:
				print(f"Error {SE.args[0]}")
				sys.exit(1)
			
	
	con.close()


def push_sort(dict_list: dict):

	sorted_tuples = []

	for d in dict_list:
		temp_list = []

		key_sort = sorted(d.keys())

		for key in key_sort:
			temp_list.append(d[key])

		sorted_tuples.append(tuple(temp_list))

	return sorted_tuples


def push_many(db_data: dict):
	con = sq3.connect(db_file_location)
	curs = con.cursor()
	
	agents_sql = '''INSERT INTO agents (agent_code, city, name, phone, state,
	        zip) VALUES (?, ?, ?, ?, ?, ?)'''
	offices_sql = '''INSERT INTO offices (city, name, office_code, phone, state,
	    zip) VALUES (?, ?, ?, ?, ?, ?)'''
	listings_sql = '''INSERT INTO listings (address, agent_id, city, description,
	    mls_number, office_id, price, state, status, type, zip) VALUES (?, ?, ?,
	    ?, ?, ?, ?, ?, ?, ?, ?)'''
	
	try:
		curs.executemany(agents_sql, push_sort(db_data['agents']))
		
		curs.executemany(offices_sql, push_sort(db_data['offices']))
		
		curs.executemany(listings_sql, push_sort(db_data['listings']))
		
	except sq3.Error as SE:
		print(f"Error {SE.args[0]}")
		sys.exit(1)
	
	con.commit()
	curs.close()


def main(db_file=db_file_location):
	
	with open("cleaned_data.json", 'r') as jrd:
		clean_data = dict(json.load(jrd))
	
	# # //db&t
	# print(type(clean_data))
	# # //db&t
	
	push_data_db(clean_data)

# push_many(clean_data)


if __name__ == '__main__':
	main()





















# if __name__ == "__main__":
# 	pass











