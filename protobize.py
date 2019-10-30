from setuptools.command.build_py import build_py

class ProtobizeConfiguration():
	"""
	Configuration for protoc
	"""
	def __init__(self, config_file_path):
		pass

class CompileProtoBuffers(build_py):
	"""
	Proto files compiler
	"""

	def find_protoc(self):
		"""
		Find local protoc executable
		"""
		pass

	def download_protoc(self):
		"""
		Download protoc executable
		"""
		pass

	def run(self):
		"""
		- Load protobize configuration
		- Locally search protoc executable or - if not found - download it.
		- Compile proto files.
		"""
		pass

