from .symbolsextractor.extractor import GoSymbolsExtractor
from .apidiff.apidiff import GoApiDiff

def api(source_code_directory):
	return GoSymbolsExtractor(source_code_directory).extract().exportedApi()

def project_packages(source_code_directory, skip_errors=False):
	return GoSymbolsExtractor(source_code_directory, skip_errors=skip_errors).extract().packages()

def apidiff(api1, api2):
	return GoApiDiff(api1, api2).runDiff().apiDiff()

