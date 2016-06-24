import sys

if __name__ == "gofedlib":
	sys.modules['lib'] = sys.modules[__name__]
