from .symbolsextractor.extractor import GoSymbolsExtractor
from .apidiff.apidiff import GoApiDiff

def api(source_code_directory):
	return GoSymbolsExtractor(source_code_directory).extract().exportedApi()

def project_packages(source_code_directory):
	return GoSymbolsExtractor(source_code_directory).extract().packages()

def apidiff(api1, api2):
	return GoApiDiff(api1, api2).runDiff().apiDiff()

