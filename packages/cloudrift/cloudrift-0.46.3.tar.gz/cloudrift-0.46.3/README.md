# CloudRift Python Client

Rift is a Python client for [CloudRift](https://cloudrift.ai) API.
It allows to schedule jobs, monitor their status and retrieve results.

### Creating CloudRift Account

To use CloudRift Python Client you need to have a CloudRift account.
Please sign up at https://cloudrift.ai.

### Launching a job

To launch a job, create a `RiftClient` instance and call `run` method.

```python
from rift import AuthenticatedClient

client = AuthenticatedClient('https://cloudrift.ai', '<email>', '<password>')
client.run(image='alpine', command=['echo', 'hello cloudrift'])
```

## Developing CloudRift

This section is for developers of CloudRift Python client library.

### Prerequisites

Create virtual environment and install requirements.

```shell
python3 -m venv venv --prompt rift
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Testing

By default, testing is done against client running on localhost,
so you need to start the server and at least one compute node locally.
To start the server locally see https://github.com/faircompute/cloudrift#running-locally.

Project is using [pytest](https://docs.pytest.org/en/latest/) for testing. To run all tests:

```shell
pytest
```

To run tests against remote server, set `CLOUDRIFT_API_URL`, `FAIRCOMPUTE_USER_EMAIL`
and `FAIRCOMPUTE_USER_PASSWORD` environment variables:

```shell
CLOUDRIFT_API_URL="https://api.cloudrift.ai" FAIRCOMPUTE_USER_EMAIL=<email> FAIRCOMPUTE_USER_PASSWORD=<password> pytest
```

### Uploading to PyPI

Please follow the instructions at https://packaging.python.org/tutorials/packaging-projects/

```shell
rm -rf dist
python3 -m build
python3 -m twine upload --repository testpypi dist/*
python3 -m twine upload dist/*
```
