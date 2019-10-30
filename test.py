import os
import shutil
import subprocess
import tempfile

from pathlib import Path
from protobize import CompileProtoBuffers 

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
