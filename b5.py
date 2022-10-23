import copy
import time
import json
import os

class B5:
	data = []

	def __init__(self, filename):
		self.filename = filename
		with open(self.filename, "r") as f:

			if os.stat(self.filename).st_size != 0:
				self.raw = json.load(f)
			else:
				self.raw = {}

			if "slices" in self.raw:
				self.db = self.raw['slices']
			else:
				self.db = []

	#I think context is the initial/shared value
	def match_pattern(self, pattern, quad, context):
		out = copy.deepcopy(context)
		for idx, pattern_part in enumerate(pattern):
			quad_part = quad[idx]
			out = self.match_part(pattern_part, quad_part, out)

		return out


	def match_part(self, pattern_part, quad_part, context):
		if context == None:
			return None

		if self.is_variable(pattern_part):
			return self.match_variable(pattern_part, quad_part, context)

		return context if pattern_part == quad_part else None

	def is_variable(self, x):
		return isinstance(x, str) and len(x) >=1 and x[0] == "?" 

	def match_variable(self, variable, quad_part, context):
		if variable in context:
			bound = context[variable]
			return this.match_part(bound, quad_part, context)

		context[variable] = quad_part
		return context

	def query_single(self, pattern, db, context):
		matched_lines = list(map(lambda quad: self.match_pattern(pattern, quad, context), db))
		return list(filter(lambda match: match is not None, matched_lines))

	def query_where(self, patterns, db):
		next_ctx = {}
		for pattern in patterns:
			next_ctx = self.query_single(pattern, db, next_ctx)
			#next_ctx = {k: v for d in next_ctx for k, v in d.items()} #flatten list of dicts into single mega-dict
		
		return next_ctx

	#helper
	def flatten(self, list):
		return [item for sublist in list for item in sublist]

	def query(self, find, where):
		contexts = self.query_where(where, self.db)
		return list(map(lambda context: self.actualize(context, find), contexts))


	def actualize(self, context, find):
		return list(map(lambda part: context[part] if self.is_variable(part) else part, find))

	#ec, so no removal, only adding
	#every update timestamped
	def add_data(self, table, id, key, value):
		data = [table, id, time.time(), key, value]
		self.db.append(data)
		self.write_file()
		return data

	#should be called less often
	def write_file(self):
		with open(self.filename, "w") as f:
			self.raw["slices"] = self.db
			f.write(json.dumps(self.raw))

	def get_data_ts(self, table, id, ts, key):
		for entry in self.db:
			if entry[0] == table and entry[1] == id and entry[2] == ts and entry[3] == key:
				return entry[4]

		return None

	def get_data(self, table, id, key):
		#find all that match
		result = []
		for entry in self.db:
			if entry[0] == table and entry[1] == id and entry[3] == key:
				result.append(entry)

		if len(result) == 0:
			return None			

		#sort by
		best = result[0]
		for entry in result:
			if(entry[2] > best[2]):
				best = entry

		return best


	def list_tables(self):
		#colliate in dict
		tables = {}
		for entry in self.db:
			tables[entry[0]] = 1

		return list(tables.keys())

	def list_id(self, table):
		ids = {}
		for entry in self.db:
			if entry[0] == table:
				ids[entry[1]] = 1

		return list(ids.keys())

	def list_keys(self, table):
		ids = {}
		for entry in self.db:
			if entry[0] == table:
				ids[entry[3]] = 1

		return list(ids.keys())
