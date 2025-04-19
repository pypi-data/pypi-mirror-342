import random
import os
import sys
from time import sleep
from typing import Sequence, Union, Optional, Mapping, Any
from urllib.parse import quote_plus

import requests

POLL_TIMEOUT = 0.1


class InternalApiClient:
    """
    Client that authenticates a user with the FairCompute server and provides methods accessible to authenticated users.
    """

    def __init__(self, client: 'RiftClient'):
        self.client = client
        self.api_root = client.internal_api_root

    def _pick_executor(self, cluster_name: str) -> str:
        executors = self.cluster(cluster_name).executors.list()
        for ex in executors:
            if ex['status'] == 'Active' and ex['node_status'] == 'Ready':
                return ex['name']
        raise RuntimeError(f"No ready executors in cluster {cluster_name}")

    def run(self,
            image: str,
            command: Sequence[str] = tuple(),
            ports: Sequence[tuple[int, int]] = tuple(),
            volumes: Sequence[tuple[str, str]] = tuple(),
            network: str = 'bridge',
            cluster_name: str = 'default',
            executor_name: Optional[str] = None,
            detach: bool = False,
            name: Optional[str] = None,
            rm: bool = False,
            cpus: str = 'All',
            gpus: str = 'All'):
        if executor_name is None or executor_name == 'any':
            executor_name = self._pick_executor(cluster_name)
        return self._run_program(cluster_name, executor_name, image, command, ports=ports, cpus=cpus, gpus=gpus,
                                 network=network, volumes=volumes, detach=detach, rm=rm, name=name)

    def run_command(self,
                    command: Mapping[str, Any],
                    cluster_name: str = 'default',
                    executor_name: Optional[str] = None,
                    command_type: str = 'Docker',
                    stream_output: bool = False):
        if executor_name is None or executor_name == 'any':
            executor_name = self._pick_executor(cluster_name)

        resp = self.put_command(cluster_name, executor_name, command, command_type)
        program_id = resp['command_id']
        bucket_id = resp['bucket_id']

        # upload stdin (empty for now)
        self.bucket(bucket_id).put_file_eof('#stdin')

        # wait for program to get scheduled
        while True:
            program_info = self.get_command_info(cluster_name, executor_name, program_id)
            if program_info['status'] in 'Queued':
                sleep(POLL_TIMEOUT)
            elif program_info['status'] in ('Processing', 'Completed'):
                break
            elif program_info['status'] == 'NotResponding':
                raise RuntimeError("Program is not responding")
            else:
                raise RuntimeError("Unexpected program status: {}".format(program_info['status']))

        if stream_output:
            self._poll_output(bucket_id, cluster_name, executor_name, program_id)

        # wait for job to complete
        while True:
            job = self.get_command_info(cluster_name, executor_name, program_id)
            if job['status'] == 'Completed':
                break
            elif job['status'] == 'NotResponding':
                raise RuntimeError("Program is not responding")
            else:
                sleep(POLL_TIMEOUT)

        # get result
        result = self.get_command_result(cluster_name, executor_name, program_id)
        if 'Ok' in result:
            return result['Ok'][command_type]['data']
        else:
            raise RuntimeError(f"Command failed: {result}")

    def _run_program(self,
                     cluster_name: str,
                     executor_name: str,
                     image: str,
                     command: Sequence[str] = tuple(),
                     ports: Sequence[tuple[int, int]] = tuple(),
                     env: Sequence[tuple[str, str]] = tuple(),
                     volumes: Sequence[tuple[str, str]] = tuple(),
                     network: str = 'bridge',
                     privileged: bool = False,
                     detach: bool = False,
                     name: Optional[str] = None,
                     rm: bool = False,
                     cpus: str = 'All',
                     gpus: str = 'All'
                     ):
        self.run_command(
            cluster_name=cluster_name,
            executor_name=executor_name,
            command={
                'type': 'PullImage',
                'image': image
            }
        )

        container = self.run_command(
            cluster_name=cluster_name,
            executor_name=executor_name,
            command={
                'type': 'CreateContainer',
                'image': image,
                'ports': [[{"port": host_port, "ip": 'null'}, {"port": container_port, "protocol": "Tcp"}] for
                          (host_port, container_port) in ports],
                'env': env,
                'command': command,
                'open_stdin': False,
                'stdin_once': False,
                'attach_stdin': False,
                'attach_stdout': True,
                'attach_stderr': True,
                'tty': False,
                'host_config': {
                    'network_mode': network,
                    'privileged': privileged,
                    'cpus': cpus,
                    'gpus': gpus,
                },
                'rm': rm,
                'name': name or '',
            }
        )['container_id']

        if volumes:
            bucket_id = self.buckets.create()
            bucket_client = self.bucket(bucket_id)
            for (local_path, remote_path) in volumes:
                with open(local_path) as f:
                    data = f.read()
                    bucket_client.put_file_data(file_name=remote_path, data=data)
                    bucket_client.put_file_eof(file_name=remote_path)
                self.run_command(
                    cluster_name=cluster_name,
                    executor_name=executor_name,
                    command={
                        'type': 'CopyIntoContainer',
                        'container': container,
                        'bucket_id': bucket_id,
                        'remote_key': remote_path,  # we use remote_path as key to reference the file in the bucket
                        # key is an arbitrary string
                        'local_path': remote_path
                    },
                )
            self.bucket(bucket_id).remove()

        result = self.run_command(
            cluster_name=cluster_name,
            executor_name=executor_name,
            command={
                'type': 'StartContainer',
                'container': container,
                'detach': detach,
            },
            stream_output=True
        )

        if detach:
            return container
        else:
            return result['exit_code']

    def _poll_output(self, bucket_id: int, cluster_name: str, executor_name: str, program_id: int):
        # print stdout and stderr
        bucket_client = self.bucket(bucket_id)
        stdout_data = bucket_client.get_file_data('#stdout')
        stderr_data = bucket_client.get_file_data('#stderr')
        while stdout_data is not None or stderr_data is not None:
            data_received = False
            if stdout_data:
                try:
                    data = next(stdout_data)
                    if data:
                        sys.stdout.write(data.decode('utf-8'))
                        data_received = True
                except StopIteration:
                    stdout_data = None
            if stderr_data:
                try:
                    data = next(stderr_data)
                    if data:
                        sys.stderr.write(data.decode('utf-8'))
                        data_received = True
                except StopIteration:
                    stderr_data = None

            job = self.get_command_info(cluster_name, executor_name, program_id)
            if job['status'] == 'NotResponding':
                raise RuntimeError("Program is not responding")

            if not data_received:
                sleep(POLL_TIMEOUT)

    def put_command(self,
                    cluster_name: str,
                    executor_name: str,
                    command: Mapping[str, Any],
                    command_type: str = 'Docker'):
        return self.client._make_request('put',
                                         url=f"{self.api_root}/clusters/{cluster_name}/executors/{executor_name}/commands",
                                         version='~upcoming',
                                         data={command_type: {'version': '~upcoming', 'data': command}})

    def get_command_info(self, cluster_name: str, executor_name: str, command_id: int):
        return self.client._make_request('get',
                                         url=f"{self.api_root}/clusters/{cluster_name}/executors/{executor_name}/commands/{command_id}/info")

    def get_command_result(self, cluster_name: str, executor_name: str, command_id: int):
        resp = self.client._make_request('get',
                                         url=f"{self.api_root}/clusters/{cluster_name}/executors/{executor_name}/commands/{command_id}/result")
        return resp['result']

    @property
    def executors(self) -> 'ExecutorsClient':
        return ExecutorsClient(self.client)

    def cluster(self, name: str = 'default') -> 'ClusterClient':
        return ClusterClient(self.client, name)

    @property
    def clusters(self) -> 'ClustersClient':
        return ClustersClient(self.client)

    @property
    def buckets(self) -> 'BucketsClient':
        return BucketsClient(self.client)

    def bucket(self, bucket_id: int) -> 'BucketClient':
        return BucketClient(self.client, bucket_id)


class ClustersClient:
    def __init__(self, client: 'RiftClient'):
        self.client = client
        self.api_root = os.path.join(client.internal_api_root, 'clusters')

    def create(self, cluster_name: str, public: bool):
        return self.client._make_request('post', url=f"{self.api_root}/create",
                                         version='V029',
                                         data={'name': cluster_name, 'public': public})

    def remove(self, cluster_name: str):
        return self.client._make_request('post', url=f"{self.api_root}/remove",
                                         version='V029',
                                         data={'name': cluster_name})

    def list(self):
        return self.client._make_request('post', url=f"{self.api_root}/list")["clusters"]


class ClusterExecutorsClient:
    def __init__(self, client: 'RiftClient', cluster_name: str):
        self.client = client
        self.api_root = os.path.join(client.internal_api_root, 'clusters', cluster_name, 'executors')

    def list(self):
        return self.client._make_request('post', url=f"{self.api_root}/list")["executors"]

    def add(self, name: str, executor_id: str):
        return self.client._make_request('post', url=f"{self.api_root}/add",
                                         version='V029',
                                         data={'executor_name': name, 'executor_id': executor_id})

    def remove(self, name: str):
        return self.client._make_request('post', url=f"{self.api_root}/remove",
                                         version='V029',
                                         data={'name': name})

    def rename(self, name_or_id: str, new_name: str):
        executor = next(
            executor for executor in self.list() if executor['name'] == name_or_id or executor['id'] == name_or_id)
        self.remove(executor['name'])
        self.add(new_name, executor['id'])


class ClusterClient:
    def __init__(self, client: 'RiftClient', cluster_name: str):
        self.client = client
        self.cluster_name = cluster_name

    @property
    def executors(self) -> ClusterExecutorsClient:
        return ClusterExecutorsClient(self.client, self.cluster_name)


class BucketsClient:
    def __init__(self, client: 'RiftClient'):
        self.client = client
        self.api_root = os.path.join(client.internal_api_root, 'buckets')

    def create(self):
        return self.client._make_request('post', url=f"{self.api_root}/create")["bucket_id"]


class BucketClient:
    def __init__(self, client: 'RiftClient', bucket_id: int):
        self.client = client
        self.bucket_id = bucket_id
        self.api_root = os.path.join(client.internal_api_root, 'buckets', str(bucket_id))

    def get_file_data(self, file_name: str):
        session = requests.Session()
        with session.get(url=f"{self.api_root}/{quote_plus(file_name)}",
                         headers={'Authorization': f'Bearer {self.client.token}'}, stream=True) as resp:
            for line in resp.iter_lines():
                yield line

    def put_file_data(self, file_name: str, data: Union[str, bytes]):
        return self.client._make_request('put', url=f"{self.api_root}/{quote_plus(file_name)}", data=data)

    def put_file_eof(self, file_name: str):
        return self.client._make_request('put', url=f"{self.api_root}/{quote_plus(file_name)}/eof")

    def remove(self):
        return self.client._make_request('post', url=f"{self.api_root}/delete")
