import sys 

if __name__ == "gofed_lib":
	sys.modules['lib'] = sys.modules[__name__]
