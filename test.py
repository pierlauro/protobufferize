import os
import pytest
import shutil
import subprocess
import tempfile

from mock import patch
from pathlib import Path
from protobufferize import CompileProtoBuffers, ProtobufferizeConfiguration

pytest.config_env = ProtobufferizeConfiguration.config_env
pytest.example_config_file = 'config-example/protobufferize.xml'

def test_find_protoc_local():
	PATH = os.environ['PATH']
	TMPDIR = tempfile.mkdtemp()
	try:
		with patch.object(CompileProtoBuffers, "__init__", lambda x, y: None):
			cpb = CompileProtoBuffers(None)
			os.environ['PATH'] = TMPDIR
			open(TMPDIR + '/' + cpb.binary_name, 'a').close()
			assert cpb.find_protoc() is not None
	finally:
		os.environ['PATH'] = PATH
		shutil.rmtree(TMPDIR)

def test_find_protoc_not_local():
	PATH = os.environ['PATH']
	try:
		with patch.object(CompileProtoBuffers, "__init__", lambda x, y: None):
			cpb = CompileProtoBuffers(None)
			os.environ['PATH'] = '/__notvalid__'
			assert cpb.find_protoc() is None
	finally:
		os.environ['PATH'] = PATH

def test_download_protoc():
	with patch.object(CompileProtoBuffers, "__init__", lambda x, y: None):
		cpb = CompileProtoBuffers(None)
		binary = cpb.download_protoc(ProtobufferizeConfiguration.default_version)
		assert os.path.isfile(binary)
		stdout = subprocess.getoutput(binary + ' --version')
		assert stdout.startswith('libprotoc ')

def test_wrong_env_configuration():
	""" Not existing configuration file """
	try:
		os.environ[pytest.config_env] = '__notexist__.xml'
		pc = ProtobufferizeConfiguration()
		assert len(pc.conf) == 0
	finally:
		os.environ[pytest.config_env] = ''

def test_env_configuration():
	""" Use provided xml file """
	try:
		os.environ[pytest.config_env] = pytest.example_config_file
		pc = ProtobufferizeConfiguration()
		assert len(pc.conf) > 0
	finally:
		os.environ[pytest.config_env] = ''

def test_no_env_configuration():
	""" Use default xml configuration location """
	del os.environ[pytest.config_env]
	shutil.copyfile(pytest.example_config_file, ProtobufferizeConfiguration.default_config_file)
	try:
		pc = ProtobufferizeConfiguration()
		assert len(pc.conf) > 0
	finally:
		os.remove(ProtobufferizeConfiguration.default_config_file)

def test_run():
	os.environ[pytest.config_env] = 'config-example/protobufferize.xml'
	with patch.object(CompileProtoBuffers, "__init__", lambda x, y: None):
		cpb = CompileProtoBuffers(None)
		cpb.run()
		assert os.path.exists('test_data/output/dir/addressbook_pb2.py')
