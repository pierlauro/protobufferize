## protobufferize

A simple setuptools plugin to compile proto files at build time.

### Installation

Install from PyPI: ```pip install protobufferize```


### Configuration

Available configuration parameters:
- `clearOutputDirectory` [default: false]
- `outputDirectory` [default: ./output]
- `protoSourceRoot` [default: ./protos]
- `protoVersion` [default: 3.10.1]

XML configuration example:

```xml
<ProtobufferizeConfiguration>
	<clearOutputDirectory>false</clearOutputDirectory>
	<outputDirectory>test_data/output</outputDirectory>
	<protoSourceRoot>test_data/protos</protoSourceRoot>
	<protoVersion>3.10.1</protoVersion>
</ProtobufferizeConfiguration>
```

A xml configuration file named `protobufferize.xml` should be put in the python's project root folder. 
In alternative, the configuration file's path can be specified in the environment variable `protobufferize_conf`.

### Usage

Compile every `.proto` file in `protoSourceRoot` subdirectories and output in the specified `outputDirectory` (`outputDirectory` gets emptied beforewards if `clearOutputDirectory` set to `true`).

```sh
python setup.py protobufferize
```

