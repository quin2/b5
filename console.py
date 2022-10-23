from b5 import B5
import ast
from inspect import signature

commands = {
	"pd": "add_data",
	"gd": "get_data",
	"lk": "list_keys",
	"lt": "list_tables",
	"li": "list_id",
	"lu": "query",
}

def print_help():
	print(help_string)
	return True 

def exit():
	return False

meta_commands = {
	"h": print_help,
	"q": exit
}

help_string = """
b5 database

crud commands:
pd (t) (id) (k) (v)
gd (t) (id) (k)
lt
lk (t)
lv (t)

queryEngine commands:
lu [?dataName] [[query]]
"""

def parse_command(line):
	state = 1
	tokens = line.split()

	#discard blank line
	if len(tokens) == 0:
		return

	#check that we support command
	command = tokens[0]
	if command in meta_commands:
		res = parse_helper(command)
		return res
	elif command in commands:
		parse_dbcommand(command, tokens)
		return True

	print("invalid command")
	return True

def parse_helper(command):
	function = meta_commands[command]
	res = function()
	return res

def parse_dbcommand(command, tokens):
	#now, run command
	function_name = commands[command]
	function_call = getattr(db, function_name)
	function_params = signature(function_call).parameters

	if len(tokens) - 1 != len(function_params):
		print(f'expected {len(function_params)} parameters but got {len(tokens) - 1}')
		return

	res = function_call(*tokens[1:])
	print(res)
	return

def repl():
	cont = True 
	while cont:
		#get input
		line = input("> ")

		cont = parse_command(line)

if __name__ == "__main__":
	global db 
	db = B5("./test.db")

	repl()