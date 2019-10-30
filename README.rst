protobize
===================

A simple setuptools plugin to compile proto files at build time.

Installation
=====

Install from PyPI ::

  pip install protobize 


Configuration
=====

Available configuration parameters ::

    clearOutputDirectory [default: false]
    outputDirectory [default: ./output]
    protoSourceRoot [default: ./protos]

XML configuration example ::

  <ProtobizeConfiguration>
    <clearOutputDirectory>false</clearOutputDirectory>
    <outputDirectory>test_data/output</outputDirectory>
    <protoSourceRoot>test_data/protos</protoSourceRoot>
  </ProtobizeConfiguration>

A xml configuration file named ``protobize.xml`` should be put in the python's project root folder. 
In alternative, the configuration file's path can be specified in the environment variable ``protobize_conf``.

Usage
=====

::
  
  python setup.py protobize


Compiles every ``.proto`` files in ``protoSourceRoot`` subdirectories and output in the specified ``outputDirectory`` (``outputDirectory`` empied if ``clearOutputDirectory`` set to ``true``).
