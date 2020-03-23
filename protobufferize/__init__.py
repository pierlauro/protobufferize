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

class ProtobufferizeConfiguration():
	"""
	Configuration for protoc
	"""

	default_version = '3.10.1'
	default_proto_source_root = 'protos'
	default_output_directory = 'output'
	default_config_file = 'protobufferize.xml'
	config_env = 'protobufferize_conf'

	def __init__(self):
		try:
			config_file = os.environ[self.config_env]
		except KeyError:
			config_file = self.default_config_file

		try:
			with open(config_file) as fd:
				self.conf = dict(xmltodict.parse(fd.read())['ProtobufferizeConfiguration'])
		except FileNotFoundError:
			self.conf = dict()

	def get_proto_source_root(self):
		return self.conf.get('protoSourceRoot') or self.default_proto_source_root

	def get_output_directory(self):
		return self.conf.get('outputDirectory') or self.default_output_directory

	def get_grpc_output_directory(self):
		return self.conf.get('grpcOutputDirectory') or None

	def get_clear_output_directory(self):
		if self.conf['clearOutputDirectory']:
			return self.conf.get('clearOutputDirectory').lower() == 'true'
		return False

	def get_version(self):
		return self.conf.get('protocVersion') or self.default_version

class CompileProtoBuffers(build_py):
	"""
	Proto files compiler
	"""
	binary_name = 'protoc'

	def download_protoc(self, version):
		"""
		Download protoc binary and return its absolute path
		"""
		binary_relative_path = 'bin/' + self.binary_name
		protobufferize_path = '/tmp/.protobufferize'
		binary_absolute_path = protobufferize_path + '/' + binary_relative_path

		# Build download URI based on os and architecture
		if distro.linux_distribution()[0]:
			operative_system = 'linux'
		elif platform.mac_ver()[0]:
			operative_system = 'osx'
		elif platform.win32_ver()[0]:
			operative_system = 'win'
		os_arch = operative_system + '-' + platform.machine()
		github_protoc_release = 'https://github.com/protocolbuffers/protobuf/releases/download/v' + version + '/protoc-' + version + '-' + os_arch + '.zip'

		# Download and unzip protoc binary
		url = request.urlopen(github_protoc_release)
		zf = ZipFile(BytesIO(url.read()))
		zf.extract(binary_relative_path, protobufferize_path)

		# Give execution permissions
		st_mode = os.stat(binary_absolute_path).st_mode
		os.chmod(binary_absolute_path, st_mode | stat.S_IEXEC)

		return binary_absolute_path

	def find_protoc(self):
		"""
		Find local protoc binary and return its absolute path
		"""
		return find_executable(self.binary_name)

	def get_protoc(self, version):
		"""
		Get the protoc binary locally or remotely and return its absolute path
		"""
		binary = self.find_protoc()
		if binary and version == subprocess.getoutput(binary + ' --version'):
			return binary
		return self.download_protoc(version)

	def run(self):
		"""
		- Load protobufferize configuration.
		- Locally search protoc binary or - if not found - download it.
		- Compile proto files with parameters specified in Configuration.
		"""
		self.conf = ProtobufferizeConfiguration()
		src = self.conf.get_proto_source_root()
		dst = self.conf.get_output_directory()
		grpc = self.conf.get_grpc_output_directory()
		version = self.conf.get_version()

		if self.conf.get_clear_output_directory():
			shutil.rmtree(dst, ignore_errors=True)

		try:
			os.mkdir(dst)
		except OSError as exc:
			if exc.errno != errno.EEXIST or not os.path.isdir(dst):
				raise

		command = [self.get_protoc(version)] if grpc is None else ['python3', '-m', 'grpc.tools.protoc', '--grpc_python_out=' + grpc]

		for path, subdirs, files in os.walk(src):
			for filename in files:
				if filename.endswith('.proto'):
					subprocess.check_call( command + [
						'-I=' + src,
						'--python_out=' + dst,
						os.path.join(path, filename)
					])
