import distro
from distutils.spawn import find_executable
from setuptools.command.build_py import build_py
import platform
import os
import stat
import subprocess

from io import BytesIO
from zipfile import ZipFile
import urllib.request

class ProtobizeConfiguration():
	"""
	Configuration for protoc
	"""
	def __init__(self):
		pass

class CompileProtoBuffers(build_py):
	"""
	Proto files compiler
	"""
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
		url = urllib.request.urlopen(github_protoc_release)
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
		pass
