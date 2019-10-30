import distro
import errno
import platform
import os
import shutil
import stat
import subprocess
import xmltodict

from distutils.spawn import find_executable
from io import BytesIO
from setuptools.command.build_py import build_py
from urllib import request
from zipfile import ZipFile

class ProtobizeConfiguration():
	"""
	Configuration for protoc
	"""
	def __init__(self):
		try:
			config_file = os.environ['protobize_conf']
		except KeyError:
			config_file = 'protobize.xml'

		try:
			with open(config_file) as fd:
				self.conf = dict(xmltodict.parse(fd.read())['ProtobizeConfiguration'])
		except FileNotFoundError:
			self.conf = dict()

	def get_proto_source_root(self):
		return self.conf['protoSourceRoot'] or 'src/main/proto'

	def get_output_directory(self):
		return self.conf['outputDirectory'] or 'generated-sources/protobuf/python'

	def get_clear_output_directory(self):
		if self.conf['clearOutputDirectory']:
			return self.conf['clearOutputDirectory'].lower() == 'true'
		return False


class CompileProtoBuffers(build_py):
	"""
	Proto files compiler
	"""

	## TODO remove init
	def __init__(self):
		pass

	binary_name = 'protoc'

	def download_protoc(self):
		"""
		Download protoc binary and return its absolute path
		"""
		binary_relative_path = 'bin/' + self.binary_name
		protobize_path = '/tmp/.protobize'
		binary_absolute_path = protobize_path + '/' + binary_relative_path

		# Build download URI based on os and architecture
		if distro.linux_distribution()[0]:
			operative_system = 'linux'
		elif platform.mac_ver()[0]:
			operative_system = 'osx'
		elif platform.win32_ver()[0]:
			operative_system = 'win'
		os_arch = operative_system + '-' + platform.machine()
		github_protoc_release = 'https://github.com/protocolbuffers/protobuf/releases/download/v3.10.1/protoc-3.10.1-' + os_arch + '.zip'

		# Download and unzip protoc binary
		url = request.urlopen(github_protoc_release)
		zf = ZipFile(BytesIO(url.read()))
		zf.extract(binary_relative_path, protobize_path)

		# Give execution permissions
		st_mode = os.stat(binary_absolute_path).st_mode
		os.chmod(binary_absolute_path, st_mode | stat.S_IEXEC)

		return binary_absolute_path

	def find_protoc(self):
		"""
		Find local protoc binary and return its absolute path
		"""
		return find_executable(self.binary_name)

	def get_protoc(self):
		"""
		Get the protoc binary locally or remotely and return its absolute path
		"""
		return self.find_protoc() or self.download_protoc()

	def run(self):
		"""
		- Load protobize configuration.
		- Locally search protoc binary or - if not found - download it.
		- Compile proto files with parameters specified in Configuration.
		"""
		self.conf = ProtobizeConfiguration()
		src = self.conf.get_proto_source_root()
		dst = self.conf.get_output_directory()

		if self.conf.get_clear_output_directory():
			shutil.rmtree(dst, ignore_errors=True)

		try:
			os.mkdir(dst)
		except OSError as exc:
			if exc.errno != errno.EEXIST or not os.path.isdir(dst):
				raise

		for path, subdirs, files in os.walk(src):
			for filename in files:
				if filename.endswith('.proto'):
					subprocess.check_call([
						self.find_protoc(),
						'-I=' + src,
						'--python_out=' + dst,
						os.path.join(path, filename)
					])
