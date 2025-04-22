# Language Independent Interface Types For INSIGHT

The proto files can be consumed as GIT submodules or copied and built directly in the consumer project.

The compiled files are published to central repositories (Maven, ...).

## Generate gRPC Client Libraries

To generate the raw gRPC client libraries, use `make gen-${LANGUAGE}`. Currently supported languages are:

* python
* golang

# Releasing

To release this we use GitHub Actions when a new release is tagged via GitHub.
