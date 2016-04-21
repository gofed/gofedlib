from .symbolsextractor.extractor import GoSymbolsExtractor

def api(source_code_directory):
	return GoSymbolsExtractor(source_code_directory).extract().exportedApi()

def project_packages(source_code_directory):
	return GoSymbolsExtractor(source_code_directory).extract().packages()

