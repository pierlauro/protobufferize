from setuptools import setup

setup(
	name='protobize',
	version='1.0-alpha',
	license = 'GNU Affero General Public License v3.0',

	author="Pierlauro Sciarelli",
	author_email="foss@pstux.dev",

	description='Compile protobuffers at package build time',
	long_description=open('README.rst').read(),
	url='https://github.com/pierlauro/protonize',

	py_modules=['protobize'],
	entry_points = {
		"distutils.commands": [
			"protobize = protobize:CompileProtoBuffers",
		],
	}
)
