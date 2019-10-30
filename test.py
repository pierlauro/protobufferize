import os
import shutil
import subprocess
import tempfile

from pathlib import Path
from protobize import CompileProtoBuffers, ProtobizeConfiguration

def test_find_protoc_local():
	PATH = os.environ['PATH']
	TMPDIR = tempfile.mkdtemp()
	try:
		cpb = CompileProtoBuffers()
		os.environ['PATH'] = TMPDIR
		open(TMPDIR + '/' + cpb.binary_name, 'a').close()
		assert cpb.find_protoc() is not None
	finally:
		os.environ['PATH'] = PATH
		shutil.rmtree(TMPDIR)

def test_find_protoc_not_local():
	PATH = os.environ['PATH']
	try:
		cpb = CompileProtoBuffers()
		os.environ['PATH'] = '/__notvalid__'
		assert cpb.find_protoc() is None
	finally:
		os.environ['PATH'] = PATH

def test_download_protoc():
	cpb = CompileProtoBuffers()
	binary = cpb.download_protoc()
	assert os.path.isfile(binary)
	stdout = subprocess.getoutput(binary + ' --version')
	assert stdout.startswith('libprotoc ')

def test_run():
	cpb = CompileProtoBuffers()
	cpb.run()

def test_wrong_env_configuration():
	""" Not existing configuration file """
	try:
		os.environ['protobize_conf'] = '__notexist__.xml'
		pc = ProtobizeConfiguration()
		assert len(pc.conf) == 0
	finally:
		os.environ['protobize_conf'] = ''

def test_env_configuration():
	""" Use provided xml file """
	try:
		os.environ['protobize_conf'] = 'protobize.xml'
		pc = ProtobizeConfiguration()
		assert len(pc.conf) > 0
	finally:
		os.environ['protobize_conf'] = ''

def test_no_env_configuration():
	""" Use default protobize.xml """
	del os.environ['protobize_conf']
	pc = ProtobizeConfiguration()
	assert len(pc.conf) > 0
