## protobufferize

A simple setuptools plugin to compile proto files at build time.

### Installation

Install from PyPI: ```pip3 install protobufferize```


### Configuration

Available configuration parameters:
- `clearOutputDirectory` [default: false]
- `grpcOutputDirectory` [default: None]
- `outputDirectory` [default: ./output]
- `protoSourceRoot` [default: ./protos]
- `protoVersion` [default: 3.10.1]

XML configuration example:

```xml
<ProtobufferizeConfiguration>
	<clearOutputDirectory>false</clearOutputDirectory>
	<grpcOutputDirectory>test_data/grpc_output</grpcOutputDirectory>
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
python3 setup.py protobufferize
```

### Internal details
By default, the specified version of `protoc` binary is downloaded and executed to compile the profo files.

If `grpcOutputDirectory` is set - instead - the latest `grpc-tools` pypi package is used (and the `protoc` version is ignored for compatibility problems).
