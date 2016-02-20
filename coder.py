import logging
import json

PREDEFINED_TYPES = ["bool", "byte", "complex64", "complex128", "error", "float32", "float64", "int", "int8", "int16", "int32", "int64", "rune", "string", "uint", "uint8", "uint16", "uint32", "uint64", "uintptr"]

TYPE_IDENT = "ident"
TYPE_ARRAY = "array"
TYPE_SLICE = "slice"
TYPE_INTERFACE = "interface"
TYPE_POINTER = "pointer"
TYPE_SELECTOR = "selector"
TYPE_STRUCT = "struct"
TYPE_METHOD = "method"
TYPE_FUNC = "func"
TYPE_ELLIPSIS = "ellipsis"
TYPE_MAP = "map"
TYPE_CHANNEL = "channel"
TYPE_PARENTHESIS = "parenthesis"

class GoTypeCoder:
	"""
	Serialization of tree-like data types representation
	"""

	def _is_predefined_type(self, type):
		if type in PREDEFINED_TYPES:
			return True
		return False

	def _predefined_type_to_json(self, type):
		return type

	def _is_ident(self, type):
		if type["type"] == TYPE_IDENT:
			return True
		return False

	def _ident_to_json(self, type):
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
		ident_obj = {}
		ident_obj["type"] = "identifier"

		if "name" in type:
			ident_obj["def"] = type["def"]["def"]
		else:
			ident_obj["def"] = type["def"]

		return ident_obj

	def _is_array(self, type):
		if type["type"] == TYPE_ARRAY:
			return True
		return False

	def _array_to_json(self, type):
		# ArrayType   = "[" ArrayLength "]" ElementType .
		# {u'elmtype': {u'type': u'ident', u'def': u'byte'}, u'type': u'array', u'name': u''}
		# "array": {
		# 	"type": "object",
		# 	"description": "Array definition",
		# 	"properties": {
		# 		"type": {
		# 			"type": "string",
		# 			"description": "type identifier",
		# 			"oneof": [
		# 				{"enum": ["array"]}
		# 			]
		# 		},
		# 		"elmtype": {
		# 			"type": "object",
		# 			"description": "element type definition",
		# 			"oneof": [
		#				TYPEDEF
		# 			]
		# 		}
		# 	},
		# 	"properties": ["type", "elmtype"]
		# }
		array_obj = {}
		array_obj["type"] = "array"
		array_obj["elmtype"] = self._type_to_json(type["elmtype"])

		return array_obj

	def _is_slice(self, type):
		if type["type"] == TYPE_SLICE:
			return True
		return False

	def _slice_to_json(self, type):
		# SliceType = "[" "]" ElementType .
		# "slice": {
		# 	"type": "object",
		# 	"description": "Slice definition",
		# 	"properties": {
		# 		"type": {
		# 			"type": "string",
		# 			"description": "Type identifier",
		# 			"oneOf": [
		# 				{"enum": ["slice"]}
		# 			]
		# 		},
		# 		"elmtype": {
		# 			"type": "object",
		# 			"description": "Element type definition",
		# 			"oneOf": [
		#				TYPEDEF
		# 			]
		# 		}
		# 	},
		# 	"properties": ["type", "elmtype"]
		# }
		slice_obj = {}
		slice_obj["type"] = "slice"
		slice_obj["elmtype"] = self._type_to_json(type["elmtype"])

		return slice_obj

	def _is_struct(self, type):
		if type["type"] == TYPE_STRUCT:
			return True
		return False

	def _struct_to_json(self, type):
		# "struct": {
		# 	"type": "object",
		# 	"description": "Struct definition",
		# 	"properties": {
		# 		"type": {
		# 			"type": "string",
		# 			"description": "Type identifier"
		# 		},
		# 		"fields": {
		# 			"type": "array",
		# 			"description": "Definition of fields",
		# 			"items": {
		# 				"type": "object",
		# 				"description": "Field definition",
		# 				"properties": {
		# 					"name": {
		# 						"type": "string",
		# 						"description": "Field name. Anonymous if omited.",
		# 						"minLength": 1
		# 					},
		# 					"def": {
		# 						"type": "object",
		# 						"description": "Type definition",
		# 						"oneof": [
		# 							TYPEDEF
		# 						]
		# 					}
		# 				},
		# 				"required": ["def"]
		# 			},
		# 			"uniqueItems": true
		# 		}
		# 	},
		# 	"required": ["type", "def"]
		# }
		fields_objs = []

		for field in type["def"]:
			field_obj = {}
			field_obj["name"] = field["name"]
			field_obj["def"] = self._type_to_json(field["def"])
			fields_objs.append(field_obj)

		struct_obj = {}
		struct_obj["type"] = "struct"
		struct_obj["fields"] = fields_objs

		return struct_obj

	def _is_selector(self, type):
		if type["type"] == TYPE_SELECTOR:
			return True
		return False

	def _selector_to_json(self, type):
		# {u'item': u'Writer', u'prefix': {u'type': u'ident', u'def': u'io'}, u'type': u'selector'}
		# "selector": {
		# 	"type": "object",
		# 	"description": "Identifier definition",
		# 	"properties": {
		# 		"type": {
		# 			"type": "string",
		# 			"description": "Type identifier",
		# 			"oneOf": [
		# 				{"enum": ["selector"]}
		# 			]
		# 		},
		# 		"prefix": {
		# 			"type": "object",
		# 			"description": "Prefix definition",
		# 			"oneOf": [
		# 				TYPEDEF
		# 			]
		# 		},
		# 		"item": {
		# 			"type": "string",
		# 			"description": "Item identifier",
		# 			"minLength": 1
		# 		}
		# 	},
		# 	"required": ["type", "prefix", "item"]
		# }
		#

		selector_obj = {}
		selector_obj["type"] = "selector"

		# {u'type': u'selector', u'name': u'URLsValue', u'def': {u'item': u'URLs', u'prefix': {u'type': u'ident', u'def': u'types'}, u'type': u'selector'}}
		if "name" in type:
			selector_obj["prefix"] = self._type_to_json(type["def"]["prefix"])
			selector_obj["item"] = type["def"]["item"]
		else:
			selector_obj["prefix"] = self._type_to_json(type["prefix"])
			selector_obj["item"] = type["item"]

		return selector_obj

	def _is_function_type(self, type):
		if type["type"] == TYPE_FUNC:
			return True
		return False

	def _function_to_json(self, type):
		# {u'name': u'emit', u'def': {u'params': [{u'type': u'ident', u'def': u'HeaderField'}], u'type': u'func', u'results': []}
		#
		# func NAME {TYPE[,TYPE]*} {TYPE[,TYPE]*}

		# "function": {
		# 	"type": "object",
		# 	"description": "Function definition",
		# 	"properties": {
		# 		"type": {
		# 			"type": "string",
		# 			"description": "Type identifier",
		# 			"oneof": [
		# 				{"enum": ["method"]}
		# 			]
		# 		},
		# 		"params": {
		# 			"type": "array",
		# 			"description": "List of parameters",
		# 			"items": {
		# 				"type": "object",
		# 				"description": "Parameter type definition",
		# 				"oneof": [
		# 					TYPEDEF
		# 				]
		# 			}
		# 		},
		# 		"results": {
		# 			"type": "array",
		# 			"description": "List of results",
		# 			"items": {
		# 				"type": "object",
		# 				"description": "Results type definition",
		# 				"oneof": [
		# 					TYPEDEF
		# 				]
		# 			}
		# 		}
		# 	},
		# 	"properties": ["type", "params", "results"]
		# }
		function_obj = {}
		function_obj["type"] = "function"

		params_objs = []
		results_objs = []

		# high level definition of function type
		# E.g. {u'type': u'func', u'name': u'EntryFormatter', u'def': {u'params': [{u'elmtype': {u'type': u'ident', u'def': u'byte'}, u'type': u'slice', u'name': u''}], u'type': u'func', u'results': [{u'type': u'ident', u'def': u'string'}]}}
		if "name" in type:
			type = type["def"]

		for param in type["params"]:
			params_objs.append(self._type_to_json(param))

		for param in type["results"]:
			results_objs.append(self._type_to_json(param))

		function_obj["params"] = params_objs
		function_obj["results"] = results_objs

		return function_obj

	def _is_map(self, type):
		if type["type"] == TYPE_MAP:
			return True

		return False

	def _map_to_json(self, type):
		# {u'type': u'map', u'name': u'', u'def': {u'keytype': {u'type': u'ident', u'def': u'string'}, u'valuetype': {u'elmtype': {u'type': u'pointer', u'def': {u'type': u'ident', u'def': u'clientConn'}}, u'type': u'slice', u'name': u''}}}
		# "map": {
		# 	"type": "object",
		# 	"description": "Map definition",
		# 	"properties": {
		# 		"type": {
		# 			"type": "string",
		# 			"description": "type identifier",
		# 			"oneof": [
		# 				{"enum": ["map"]}
		# 			]
		# 		},
		# 		"keytype": {
		# 			"type": "object",
		# 			"description": "Key type definition",
		# 			"oneof": [
		# 				TYPEDEF
		# 			]
		# 		},
		# 		"valuetype": {
		# 			"type": "object",
		# 			"description": "Key type definition",
		# 			"oneof": [
		# 				TYPEDEF
		# 			]
		# 		}
		# 	},
		# 	"properties": ["type", "keytype", "valuetype"]
		# }
		map_obj = {}
		map_obj["type"] = "map"
		map_obj["keytype"] = self._type_to_json(type["def"]["keytype"])
		map_obj["valuetype"] = self._type_to_json(type["def"]["valuetype"])

		return map_obj

	def _is_pointer(self, type):
		if type["type"] == TYPE_POINTER:
			return True
		return False

	def _pointer_to_json(self, type):
		# {u'type': u'pointer', u'def': {u'type': u'ident', u'def': u'clientConn'}}
		# "pointer": {
		# 	"type": "object",
		# 	"description": "Pointer definition",
		# 	"properties": {
		# 		"type": {
		# 			"type": "string",
		# 			"description": "type identifier",
		# 			"oneof": [
		# 				{"enum": ["pointer"]}
		# 			]
		# 		},
		# 		"def": {
		# 			"type": "object",
		# 			"description": "Pointed type definition",
		# 			"oneof": [
		#				TYPEDEF
		# 			]
		# 		}
		# 	},
		# 	"properties": ["type", "def"]
		# }
		pointer_obj = {}
		pointer_obj["type"] = "pointer"
		pointer_obj["def"] = self._type_to_json(type["def"])

		return pointer_obj

	def _is_method(self, type):
		if type["type"] == TYPE_METHOD:
			return True
		return False

	def _method_to_json(self, type):
		# {u'type': u'method', u'name': u'Header', u'def': {u'params': [], u'type': u'func', u'results': [{u'type': u'ident', u'def': u'FrameHeader'}]}}
		# Method appears only when a function on the highest level is defined.
		# Method in here comes from interface definition.
		#
		# "function": {
		# 	"type": "object",
		# 	"description": "Function definition",
		# 	"properties": {
		# 		"type": {
		# 			"type": "string",
		# 			"description": "Type identifier",
		# 			"oneof": [
		# 				{"enum": ["method"]}
		# 			]
		# 		},
		# 		"params": {
		# 			"type": "array",
		# 			"description": "List of parameters",
		# 			"items": {
		# 				"type": "object",
		# 				"description": "Parameter type definition",
		# 				"oneof": [
		# 					TYPEDEF
		# 				]
		# 			}
		# 		},
		# 		"results": {
		# 			"type": "array",
		# 			"description": "List of results",
		# 			"items": {
		# 				"type": "object",
		# 				"description": "Results type definition",
		# 				"oneof": [
		# 					TYPEDEF
		# 				]
		# 			}
		# 		}
		# 	},
		# 	"properties": ["type", "params", "results"]
		# }

		function_obj = {}
		function_obj["type"] = "function"

		params_objs = []
		for param in type["def"]["params"]:
			params_objs.append(self._type_to_json(param))

		results_objs = []
		for result in type["def"]["results"]:
			results_objs.append(self._type_to_json(result))

		function_obj["params"] = params_objs
		function_obj["results"] = results_objs

		return function_obj

	def _is_interface(self, type):
		if type["type"] == TYPE_INTERFACE:
			return True

		return False

	def _interface_to_json(self, type):
		# {u'type': u'interface', u'name': u'Frame', u'def': [{u'type': u'method', u'name': u'Header', u'def': {u'params': [], u'type': u'func', u'results': [{u'type': u'ident', u'def': u'FrameHeader'}]}}, {u'type': u'method', u'name': u'invalidate', u'def': {u'type': u'func', u'params': [], u'results': []}}]}
		# "interface": {
		# 	"type": "object",
		# 	"description": "Interface definition",
		# 	"properties": {
		# 		"type": {
		# 			"type": "string",
		# 			"description": "type identifier",
		# 			"oneof": [
		# 				{"enum": ["interface"]}
		# 			]
		# 		},
		# 		"methods": {
		# 			"type": "array",
		# 			"description": "List of methods",
		# 			"items": {
		# 				"type": "object",
		# 				"description": "Method definition",
		# 				"properties": {
		# 					"name": {
		# 						"type": "string",
		# 						"description": "Method name",
		# 						"minLength": 1
		# 					},
		# 					"def": {
		# 						"type": "object",
		# 						"description": "Function type definition",
		# 						"oneof": [
		# 							{ "$ref": "#/definitions/function" }
		# 						]	
		# 					}
		# 				},
		# 				"required": ["name", "def"]
		# 			},
		# 			"uniqueItems": true
		# 		}
		# 	},
		# 	"properties": ["type", "methods"]
		# }

		interface_obj = {}
		interface_obj["type"] = "interface"

		method_objs = []

		for fnc in type["def"]:
			method_obj = {}
			method_obj["name"] = fnc["name"]
			method_obj["def"] = self._method_to_json(fnc)
			method_objs.append(method_obj)

		interface_obj["methods"] = method_objs

		return interface_obj

	def _is_ellipses(self, type):
		if type["type"] == TYPE_ELLIPSIS:
			return True

		return False

	def _ellipses_to_json(self, type):
		# {u'type': u'ellipsis', u'elt': TYPEDEF}
		# "ellipses": {
		# 	"type": "object",
		# 	"description": "Pointer definition",
		# 	"properties": {
		# 		"type": {
		# 			"type": "string",
		# 			"description": "type identifier",
		# 			"oneOf": [
		# 				{"enum": ["ellipses"]}
		# 			]
		# 		},
		# 		"def": {
		# 			"type": "object",
		# 			"description": "Ellipses type definition",
		# 			"anyOf": [
		# 				TYPEDEF
		# 			]
		# 		}
		# 	},
		# 	"required": ["type", "def"]
		# }
		ellipses_obj = {}
		ellipses_obj["type"] = TYPE_ELLIPSIS
		ellipses_obj["def"] = self._type_to_json(type["elt"])
		return ellipses_obj

	def _is_channel(self, type):
		if type["type"] == TYPE_CHANNEL:
			return True

		return False

	def _channel_to_json(self, type):
		# {u'type': u'channel', u'value': {u'type': u'ident', u'def': u'Ready'}, u'dir': u'2'}
		# "channel": {
		# 	"type": "object",
		# 	"description": "Channel definition",
		# 	"properties": {
		# 		"type": {
		# 			"type": "string",
		# 			"description": "Type identifier",
		# 			"oneOf": [
		# 				{"enum": ["channel"]}
		# 			]
		# 		},
		# 		"dir": {
		# 			"type": "string",
		# 			"description": "Direction specification",
		# 			"oneOf": [
		# 				{"enum": ["1", "2", "3"]}
		# 			]
		# 		},
		# 		"value": {
		# 			"type": "object",
		# 			"description": "Value definition",
		# 			"oneOf": [
		# 				TYPEDEF
		# 			]
		# 		}
		# 	},
		# 	"required": ["type", "dir", "value"]
		# }
		channel_obj = {}
		channel_obj["type"] = "channel"

		if "def" in type:
			channel_obj["dir"] = type["def"]["dir"]
			channel_obj["value"] = self._type_to_json(type["def"]["value"])
		else:
			channel_obj["dir"] = type["dir"]
			channel_obj["value"] = self._type_to_json(type["value"])

		return channel_obj

	def _function_with_receiver_to_json(self, type):
		# {u'name': u'Wait', u'def': {u'params': [], u'returns': [], u'recv': [{u'type': u'ident', u'def': u'closeWaiter'}]}}
		# "method": {
		# 	"type": "object",
		# 	"description": "Method definition",
		# 	"properties": {
		# 		"type": {
		# 			"type": "string",
		# 			"description": "type identifier",
		# 			"oneOf": [
		# 				{"enum": ["method"]}
		# 			]
		# 		},
		# 		"receiver": {
		# 			"type": "object",
		# 			"description": "Receiver type definition",
		# 			"anyOf": [
		# 				{ "$ref": "#/definitions/identifier" },
		# 				{ "$ref": "#/definitions/selector" },
		# 				{ "$ref": "#/definitions/pointer" }
		# 			]
		# 		},
		# 		"def": {
		# 			"type": "object",
		# 			"description": "Function type definition",
		# 			"oneOf": [
		# 				{ "$ref": "#/definitions/function" }
		# 			]
		# 		}
		# 	},
		# 	"required": ["receiver", "def"]
		# }
		function_obj = {}
		function_obj["type"] = "method"
		function_obj["receiver"] = self._type_to_json(type["recv"][0])
		function_obj["def"] = self._function_to_json(type)

		return function_obj

	def _type_to_json(self, type):
		if self._is_struct(type):
			return self._struct_to_json(type)
		if self._is_ident(type):
			return self._ident_to_json(type)
		if self._is_selector(type):
			return self._selector_to_json(type)
		if self._is_slice(type):
			return self._slice_to_json(type)
		if self._is_function_type(type):
			return self._function_to_json(type)
		if self._is_array(type):
			return self._array_to_json(type)
		if self._is_map(type):
			return self._map_to_json(type)
		if self._is_pointer(type):
			return self._pointer_to_json(type)
		if self._is_interface(type):
			return self._interface_to_json(type)
		if self._is_ellipses(type):
			return self._ellipses_to_json(type)
		if self._is_channel(type):
			return self._channel_to_json(type)

		logging.error("%s type not implemented" % type["type"])
		logging.error(type)

		return {}

	def __init__(self, type):
		self.type = type

	def codeDataType(self):
		# the highest definition must carry data type name
		if "name" not in self.type:
			logging.error("Missing data type name for %s" % json.dumps(self.type))
			return {}

		o_json = {}
		o_json["name"] = self.type["name"]
		o_json["def"] = self._type_to_json(self.type)

		return o_json

	def codeFunctionType(self):
		# the highest definition must carry function name
		if "name" not in self.type:
			logging.error("Missing function name for %s" % json.dumps(self.type))

		o_json = {}
		o_json["name"] = self.type["name"]
		# {u'name': u'Wait', u'def': {u'params': [], u'returns': [], u'recv': [{u'type': u'ident',     u'def': u'closeWaiter'}]}}
		if "recv" in self.type["def"]:
			if len(self.type["def"]["recv"]) > 0:
				o_json["def"] = self._function_with_receiver_to_json(self.type["def"])
			else:
				o_json["def"] = self._function_to_json(self.type["def"])
		else:
			o_json["def"] = self._function_to_json(self.type["def"])

		return o_json

	def codeVariableType(self):
		# atm each type as variable name
		o_json = {}
		o_json["name"] = self.type

		return o_json
