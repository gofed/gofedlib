import logging

TYPE_IDENT = "identifier"
TYPE_ARRAY = "array"
TYPE_SLICE = "slice"
TYPE_INTERFACE = "interface"
TYPE_POINTER = "pointer"
TYPE_SELECTOR = "selector"
TYPE_STRUCT = "struct"
TYPE_METHOD = "method"
TYPE_FUNC = "function"
TYPE_ELLIPSIS = "ellipsis"
TYPE_MAP = "map"
TYPE_CHANNEL = "channel"
TYPE_PARENTHESIS = "parenthesis"

def apidiff(api1, api2):
	obj = GoApiDiff(api1, api2)
	obj.runDiff()
	return obj.getProjectsApiDiff()

class GoApiDiff(object):
	"""
	Input:
	- exported API of a project for a given commit1
	- exported API of a project for a given commit2
	E.g.
	{"exported_api_1": JSON, "exported_api_2": JSON}
	Output:

	Algorithm:
	- both APIs must be of the same project
	"""

	def __init__(self, api1, api2):
		self.exported_api_1 = api1
		self.exported_api_2 = api2

		# extracted data
		self.new_packages = []
		self.removed_packages = []
		self.diffs = []

		self.data = {}

	def getProjectsApiDiff(self):
		return self.data

	def runDiff(self):
		self._compareApis()
		return True

	def _compareApis(self):
		ip1 = []
		ip2 = []

		packages1 = {}
		packages2 = {}

		for pkg in self.exported_api_1["packages"]:
			ip1.append(pkg["package"])
			packages1[pkg["package"]] = pkg

		for pkg in self.exported_api_2["packages"]:
			ip2.append(pkg["package"])
			packages2[pkg["package"]] = pkg

		ip1_set = set(ip1)
		ip2_set = set(ip2)

		new_packages = list( ip2_set - ip1_set )
		rem_packages = list( ip1_set - ip2_set )
		com_packages = sorted(list( ip1_set & ip2_set ))

		self.data = {}

		if new_packages != []:
			self.data["newpackages"] = new_packages

		if rem_packages != []:
			self.data["removedpackages"] = rem_packages

		updated_packages = []
		for pkg in com_packages:
			pkg_obj = self._comparePackages(packages1[pkg], packages2[pkg])
			if pkg_obj != {}:
				pkg_obj["package"] = pkg
				updated_packages.append(pkg_obj)

		if updated_packages != []:
			self.data["updatedpackages"] = updated_packages

	def _comparePackages(self, definition1, definition2):
		diff_data_types = {}
		diff_func_types = {}
		diff_vars_types = {}

		# compare data types
		types1_in = "datatypes" in definition1
		types2_in = "datatypes" in definition2
		if types1_in and types2_in:
			diff_data_types = self._compareDataTypes(definition1["datatypes"], definition2["datatypes"])

		if types1_in and not types2_in:
			logging.error("definition2: datatypes field missing")
			return False

		if not types1_in and types2_in:
			logging.error("definition1: datatypes field missing")
			return False

		# compare functions types
		types1_in = "functions" in definition1
		types2_in = "functions" in definition2
		if types1_in and types2_in:
			diff_func_types = self._compareFuncTypes(definition1["functions"], definition2["functions"])

		if types1_in and not types2_in:
			logging.error("definition2: functions field missing")
			return False

		if not types1_in and types2_in:
			logging.error("definition1: functions field missing")
			return False

		# compare variables types
		types1_in = "variables" in definition1
		types2_in = "variables" in definition2
		if types1_in and types2_in:
			diff_vars_types = self._compareVariables(definition1["variables"], definition2["variables"])

		if types1_in and not types2_in:
			logging.error("definition2: variables field missing")
			return False

		if not types1_in and types2_in:
			logging.error("definition1: variables field missing")
			return False

		pkg_obj = {}

		if diff_data_types != {}:
			pkg_obj["types"] = diff_data_types

		if diff_func_types != {}:
			pkg_obj["functions"] = diff_func_types

		if diff_vars_types != {}:
			pkg_obj["variables"] = diff_vars_types

		return pkg_obj

	def _compareDataTypes(self, data_types1, data_types2):
		types1_ids = []
		types2_ids = []

		types1 = {}
		types2 = {}

		for datatype in data_types1:
			types1_ids.append(datatype["name"])
			types1[datatype["name"]] = datatype

		for datatype in data_types2:
			types2_ids.append(datatype["name"])
			types2[datatype["name"]] = datatype

		types1_ids_set = set(types1_ids)
		types2_ids_set = set(types2_ids)

		new_type_ids = list(types2_ids_set - types1_ids_set)
		rem_type_ids = list(types1_ids_set - types2_ids_set)
		com_type_ids = list(types1_ids_set & types2_ids_set)

		diffs_obj = {}

		if new_type_ids != []:
			diffs_obj["new"] = new_type_ids

		if rem_type_ids != []:
			diffs_obj["removed"] = rem_type_ids

		self.diffs = []
		for type_id in com_type_ids:
			self._compareDataType(types1[type_id]["def"], types2[type_id]["def"])

		if self.diffs != []:
			diffs_obj["updated"] = self.diffs

		return diffs_obj

	def _compareDataType(self, data_type1, data_type2):
		#
		# TODO(jchaloup): add better location of different.
		#  E.g. struct(name):interface:method:struct:int
		#  old in file *** on line ***
		#  new in file *** on line ***
		if data_type1["type"] != data_type2["type"]:
			self.diffs.append("-type differs: %s != %s" % (data_type1["type"], data_type2["type"]))
			return
		type = data_type1["type"]

		if type == TYPE_IDENT:
			self._compareIdentifiers(data_type1, data_type2)
			return
		if type == TYPE_STRUCT:
			self._compareStructs(data_type1, data_type2)
			return
		if type == TYPE_INTERFACE:
			self._compareInterfaces(data_type1, data_type2)
			return
		if type == TYPE_FUNC:
			self._compareFunctions(data_type1, data_type2)
			return
		if type == TYPE_SELECTOR:
			self._compareSelectors(data_type1, data_type2)
			return
		if type == TYPE_SLICE:
			self._compareSlices(data_type1, data_type2)
			return
		if type == TYPE_ARRAY:
			self._compareArrays(data_type1, data_type2)
			return
		if type == TYPE_POINTER:
			self._comparePointers(data_type1, data_type2)
			return
		if type == TYPE_CHANNEL:
			self._compareChannels(data_type1, data_type2)
			return
		if type == TYPE_ELLIPSIS:
			self._compareEllipses(data_type1, data_type2)
			return
		if type == TYPE_MAP:
			self._compareMaps(data_type1, data_type2)
			return
		if type == TYPE_METHOD:
			self._compareMethods(data_type1, data_type2)
			return

		logging.error("%s type not implemented yet" % type)
		return

	def _constructTypeQualifiedName(self, type, full=False):
		"""
		For given type construct its full qualified name.

		AnonymousField = [ "*" ] TypeName .
		TypeName  = identifier | QualifiedIdent .
		QualifiedIdent = PackageName "." identifier .
		"""
		t = type["type"]
		if t == TYPE_IDENT:
			return type["def"]
		elif t == TYPE_POINTER:
			return self._constructTypeQualifiedName(type["def"])
		elif t == TYPE_SELECTOR:
			if full:
				return "%s.%s" % (type["prefix"], type["item"])
			else:
				return type["item"]
		else:
			logging.error("Type %s can not be used for FQN" % t)
			return ""

	def _compareStructs(self, struct1, struct2, name = ""):
		fields1 = []
		fields2 = []

		fields1_types = {}
		fields2_types = {}

		for field in struct1["fields"]:
			if "name" not in field or field["name"] == "":
				name = self._constructTypeQualifiedName(field["def"])
			else:
				name = field["name"]

			fields1.append(name)
			fields1_types[name] = field

		for field in struct2["fields"]:
			if "name" not in field or field["name"] == "":
				name = self._constructTypeQualifiedName(field["def"])
			else:
				name = field["name"]

			fields2.append(name)
			fields2_types[name] = field

		fields1_set = set(fields1)
		fields2_set = set(fields2)

		new_fields = list(fields2_set - fields1_set)
		rem_fields = list(fields1_set - fields2_set)
		com_fields = list(fields1_set & fields2_set)

		for field in new_fields:
			self.diffs.append("+struct %s: new field '%s'" % (name, field))

		for field in rem_fields:
			self.diffs.append("-struct %s: '%s' field removed" % (name, field))

		for field in com_fields:
			self._compareDataType(fields1_types[field]["def"], fields2_types[field]["def"])

	def _compareIdentifiers(self, ident1, ident2):
		# "identifier": {
		# 	"type": "object",
		# 	"description": "Identifier definition",
		# 	"properties": {
		# 		"type": {
		# 			"type": "string",
		# 			"description": "Type identifier",
		# 			"oneOf": [
		# 				{"enum": ["identifier"]}
		# 			]
		# 		},
		# 		"def": {
		# 			"type": "string",
		# 			"description": "Primitive type or ID",
		# 			"minLength": 1
		# 		}
		# 	},
		# 	"required": ["type", "def"]
		# },
		if ident1["def"] != ident2["def"]:
			self.diffs.append("-identifiers differ in type: %s != %s" % (ident1["def"], ident2["def"]))

	def _compareSelectors(self, selector1, selector2):
		#
		if selector1["item"] != selector2["item"]:
			self.diffs.append("-Selector differs in expression: %s != %s" % (selector1["item"], selector2["item"]))

		self._compareDataType(selector1["prefix"], selector2["prefix"])

	def _compareFunctions(self, function1, function2, name = ""):
		# compare params
		l1 = len(function1["params"])
		l2 = len(function2["params"])
		if l1 != l2:
			self.diffs.append("-function %s: parameter count changed: %s -> %s" % (name, l1, l2))
			return

		for i in range(0, l1):
			self._compareDataType(function1["params"][i], function2["params"][i])

		# compare results
		l1 = len(function1["results"])
		l2 = len(function2["results"])
		if l1 != l2:
			self.diffs.append("-function %s: results count changed: %s -> %s" % (name, l1, l2))
			return

		for i in range(0, l1):
			self._compareDataType(function1["results"][i], function2["results"][i])

	def _compareMethods(self, method1, method2):
		self._compareDataType(method1["receiver"], method2["receiver"])
		self._compareDataType(method1["def"], method2["def"])

	def _compareSlices(self, slice1, slice2):
		self._compareDataType(slice1["elmtype"], slice2["elmtype"])

	def _compareSlices(self, slice1, slice2):
		self._compareDataType(slice1["elmtype"], slice2["elmtype"])

	def _compareArrays(self, array1, array2):
		self._compareDataType(array1["elmtype"], array2["elmtype"])

	def _comparePointers(self, pointer1, pointer2):
		self._compareDataType(pointer1["def"], pointer2["def"])

	def _compareChannels(self, channel1, channel2):
		if channel1["dir"] != channel2["dir"]:
			self.diffs.append("-Channels has different direction: %s -> %s" % (channel1["dir"], channel2["dir"]))

		self._compareDataType(channel1["value"], channel2["value"])

	def _compareEllipses(self, ellipse1, ellipse2):
		self._compareDataType(ellipse1["def"], ellipse2["def"])

	def _compareMaps(self, map1, map2):
		self._compareDataType(map1["keytype"], map2["keytype"])
		self._compareDataType(map1["valuetype"], map2["valuetype"])

	def _compareInterfaces(self, interface1, interface2, name = ""):
		methods1 = []
		methods2 = []

		methods1_types = {}
		methods2_types = {}

		for method in interface1["methods"]:
			methods1.append(method["name"])
			methods1_types[method["name"]] = method["def"]

		for method in interface2["methods"]:
			methods2.append(method["name"])
			methods2_types[method["name"]] = method["def"]

		methods1_set = set(methods1)
		methods2_set = set(methods2)

		new_methods = list(methods2_set - methods1_set)
		rem_methods = list(methods1_set - methods2_set)
		com_methods = list(methods1_set & methods2_set)

		for method in new_methods:
			self.diffs.append("+interface %s: new method: %s" % (name, method))
		for method in rem_methods:
			self.diffs.append("-interface %s: %s method removed" % (name, method))

		for method in com_methods:
			self._compareDataType(methods1_types[method], methods2_types[method])

	def _constructMethodName(self, method_def):
		# Receiver type must be of the form T or *T (possibly using parentheses) where T is a type name.
		# The type denoted by T is called the receiver base type;
		# it must not be a pointer or interface type and it must be declared
		# in the same package as the method.

		# if def has not receiver, return the name
		if method_def["def"]["type"] == TYPE_FUNC:
			return method_def["name"]

		# else construct receiver.method_name
		receiver = self._constructTypeQualifiedName(method_def["def"]["receiver"])
		return "%s.%s" % (receiver, method_def["name"])

	def _compareFuncTypes(self, func_types1, func_types2):
		func1_ids = []
		func2_ids = []

		func1_types = {}
		func2_types = {}

		for functype in func_types1:
			name = self._constructMethodName(functype)
			func1_ids.append(name)
			func1_types[name] = functype["def"]

		for functype in func_types2:
			name = self._constructMethodName(functype)
			func2_ids.append(name)
			func2_types[name] = functype["def"]

		func1_ids_set = set(func1_ids)
		func2_ids_set = set(func2_ids)

		new_func_ids = list(func2_ids_set - func1_ids_set)
		rem_func_ids = list(func1_ids_set - func2_ids_set)
		com_func_ids = list(func1_ids_set & func2_ids_set)

		diffs_obj = {}

		if new_func_ids != []:
			diffs_obj["new"] = new_func_ids

		if rem_func_ids != []:
			diffs_obj["removed"] = rem_func_ids

		self.diffs = []
		for func in com_func_ids:
			self._compareDataType(func1_types[func], func2_types[func])

		if self.diffs != []:
			diffs_obj["updated"] = self.diffs

		return diffs_obj

	def _compareVariables(self, vars1, vars2):
		var1_ids = []
		var2_ids = []

		for var in vars1:
			var1_ids.append(var["name"])

		for var in vars2:
			var2_ids.append(var["name"])

		var1_ids_set = set(var1_ids)
		var2_ids_set = set(var2_ids)

		new_vars = list(var2_ids_set - var1_ids_set)
		rem_vars = list(var1_ids_set - var2_ids_set)
		com_vars = list(var1_ids_set & var2_ids_set)

		diffs_obj = {}

		if new_vars:
			diffs_obj["new"] = new_vars

		if rem_vars:
			diffs_obj["removed"] = rem_vars

		#self.diffs = []
		#diffs_obj["updated"] = []

		return diffs_obj
