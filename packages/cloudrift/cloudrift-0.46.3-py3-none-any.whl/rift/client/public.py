import datetime
import os
import time
from typing import Optional, Sequence


class PublicApiClient:
    """
    ApiClient is used to interact with the CloudRift API using an API key.
    """

    def __init__(self, client: 'RiftClient'):
        self.client = client

    @property
    def users(self) -> 'UsersClient':
        return UsersClient(self.client)

    @property
    def account(self) -> 'AccountClient':
        return AccountClient(self.client, self.client.public_api_root)

    @property
    def payment_intents(self) -> 'PaymentIntentsClient':
        return PaymentIntentsClient(self.client, self.client.public_api_root)

    @property
    def configuration(self) -> 'ConfigurationClient':
        return ConfigurationClient(self.client)

    @property
    def instance_types(self) -> 'InstanceTypesClient':
        return InstanceTypesClient(self.client)

    @property
    def instances(self) -> 'InstancesClient':
        return InstancesClient(self.client)

    @property
    def providers(self) -> 'ProvidersClient':
        return ProvidersClient(self.client)

    @property
    def recipes(self) -> 'RecipesClient':
        return RecipesClient(self.client)

    @property
    def usage(self) -> 'UsageClient':
        return UsageClient(self.client)

    @property
    def ssh_keys(self) -> 'SshKeysClient':
        return SshKeysClient(self.client)


class UsersClient:
    def __init__(self, client: 'RiftClient'):
        self.client = client
        self.api_root = os.path.join(client.public_api_root, 'users')

    def register(self, name: str, email: str, password: str, invite_code: Optional[str] = None):
        return self.client._make_request('post', url=f"{self.api_root}/register",
                                         data={'name': name,
                                               'email': email,
                                               'password': password,
                                               'invite_code': invite_code})


class AccountClient:
    def __init__(self, client: 'RiftClient', api_root: str):
        self.client = client
        self.api_root = os.path.join(api_root, 'account')

    def info(self):
        return self.client._make_request('post', url=f'{self.api_root}/info')

    @property
    def transactions(self) -> 'TransactionsClient':
        return TransactionsClient(self.client, self.api_root)


class PaymentIntentsClient:
    def __init__(self, client: 'RiftClient', api_root: str):
        self.client = client
        self.api_root = os.path.join(api_root, 'payment-intents')

    def create(self):
        return self.client._make_request('post', url=f'{self.api_root}/create')


class TransactionsClient:
    def __init__(self, client: 'RiftClient', api_root: str):
        self.client = client
        self.api_root = os.path.join(api_root, 'transactions')

    def list(self):
        return self.client._make_request('post', url=f'{self.api_root}/list')

    def promo(self, promo_code: str):
        return self.client._make_request('post', url=f'{self.api_root}/create/promo', data={'promo_code': promo_code})

    def external(self, provider_name: str, amount: int, description: Optional[str] = None):
        data = {
            'account': {'ComputeProvider': {'name': provider_name}},
            'amount': amount,
        }
        if description is not None:
            data['description'] = description
        return self.client._make_request('post', url=f'{self.api_root}/create/external', data=data)


class ConfigurationClient:
    def __init__(self, client: 'RiftClient'):
        self.client = client
        self.api_root = os.path.join(client.public_api_root, 'configuration')

    def list_ip_ranges(self):
        return self.client._make_request('post', url=f'{self.api_root}/ip/ranges/list')['ranges']

    def add_ip_range(self, from_ip: str, to_ip: str):
        return self.client._make_request('post', url=f'{self.api_root}/ip/ranges/add',
                                         data={'from': from_ip, 'to': to_ip})

    def remove_ip_range(self, from_ip: str, to_ip: str):
        return self.client._make_request('post', url=f'{self.api_root}/ip/ranges/remove',
                                         data={'from': from_ip, 'to': to_ip})


class RecipesClient:
    def __init__(self, client: 'RiftClient'):
        self.client = client
        self.api_root = os.path.join(client.public_api_root, 'recipes')

    def list(self):
        return self.client._make_request('post', url=f'{self.api_root}/list')['groups']


class InstanceTypesClient:
    def __init__(self, client: ['RiftClient']):
        self.client = client
        self.api_root = os.path.join(client.public_api_root, 'instance-types')

    def list(self, services: Optional[Sequence[str]] = None, datacenters: Optional[Sequence[str]] = None):
        data = {}
        if services is not None or datacenters is not None:
            selector = {}
            if services is not None:
                selector['services'] = services
            if datacenters is not None:
                selector['datacenters'] = datacenters
            data = {'selector': {'ByServiceAndLocation': selector}}
        return self.client._make_request('post', data=data, url=f'{self.api_root}/list')['instance_types']


class InstancesClient:
    def __init__(self, client: ['RiftClient']):
        self.client = client
        self.api_root = os.path.join(client.public_api_root, 'instances')

    def rent(self,
             instance: str,
             with_public_ip: bool = False,
             vm: Optional[dict] = None,
             docker: Optional[dict] = None,
             node_id: Optional[str] = None,
             blocking: bool = True,
             timeout: int = 10):
        if self.client.api_key is None:
            raise RuntimeError("API key is required for renting an executor")
        if self.client.token is None:
            raise RuntimeError("Token is required for renting an executor")

        if node_id is None:
            request = {
                'selector': {'ByInstanceTypeAndLocation': {'instance_type': instance}},
                'with_public_ip': with_public_ip
            }
        else:
            request = {
                'selector': {'ByNodeId': { 'node_id': node_id, 'instance_type' : instance }},
                'with_public_ip': with_public_ip
            } 

        if vm is not None and docker is not None:
            raise ValueError("Only one of vm or docker can be specified")
        elif vm is not None:
            if 'cloudinit_config' not in vm:
                vm['cloudinit_config'] = 'Auto'
            request['config'] = {'VirtualMachine': vm}
        else:
            request['config'] = {'Docker': {'image': None}} if docker is None else {'Docker': docker}

        instance_id = self.client._make_request('post', url=f'{self.api_root}/rent',
                                                data=request)['instance_ids'][0]
        if not blocking:
            return instance_id

        start = time.time()
        while time.time() - start < timeout:
            instance_info = self.info(instance_id=instance_id)
            if instance_info is not None and instance_info['status'] == 'Active':
                return instance_id
            time.sleep(1)

        raise TimeoutError(f"Instance {instance_id} hasn't started")

    def _list(self, selector):
        return self.client._make_request('post', url=f"{self.api_root}/list", data={'selector': selector})['instances']

    def info(self, instance_id: str):
        instances = self._list(selector={'ById': [instance_id]})
        if len(instances) == 0:
            return None
        return instances[0]

    def list(self, all=False):
        if all:
            status = ['Initializing', 'Active', 'Deactivating', 'Inactive']
        else:
            status = ['Initializing', 'Active', 'Deactivating']
        return self._list(selector={'ByStatus': status})

    def terminate(self, instance_id, blocking=True, timeout=10.0):
        self._terminate(selector={'ById': [instance_id]}, blocking=blocking, timeout=timeout)

    def terminate_all(self, blocking=True, timeout=10.0):
        self._terminate(selector={'ByStatus': ['Initializing', 'Active']}, blocking=blocking, timeout=timeout)

    def _terminate(self, selector, blocking=True, timeout=10.0):
        terminated = self.client._make_request('post', url=f"{self.api_root}/terminate", data={'selector': selector})['terminated']
        if not blocking:
            return

        start = time.time()
        while time.time() - start < timeout:
            instances = self._list(selector={'ById': [t['id'] for t in terminated]})
            if all(inst['status'] == 'Inactive' for inst in instances):
                return
            time.sleep(1)

        raise TimeoutError(f"Some of the instances haven't stopped")


class ProvidersClient:
    def __init__(self, client: ['RiftClient']):
        self.client = client
        self.api_root = os.path.join(client.public_api_root, 'providers')

    def list(self, names: Optional[Sequence[str]] = None):
        if names is None:
            data = {}
        else:
            data = {'selector': {'ByName': names}}
        return self.client._make_request('post', data=data, url=f'{self.api_root}/list')['providers']

    def list_nodes(self):
        return self.client._make_request('post', url=f'{self.api_root}/nodes/list')['nodes']


class UsageClient:
    def __init__(self, client: ['RiftClient']):
        self.client = client
        self.api_root = os.path.join(client.public_api_root, 'providers/usage')

    def summary(self, date_from: datetime.datetime, date_to: datetime.datetime):
        assert date_from.tzinfo is not None and date_to.tzinfo is not None, \
            "Timezones are required, add it to timestamp via ts.replace(tzinfo=datetime.timezone.utc)"
        date_from = date_from.isoformat()
        date_to = date_to.isoformat()
        return self.client._make_request('post', url=f'{self.api_root}/summary',
                                         data={'from': date_from, 'to': date_to})

    def node_summary(self, date_from: datetime.datetime, date_to: datetime.datetime):
        assert date_from.tzinfo is not None and date_to.tzinfo is not None, \
            "Timezones are required, add it to timestamp via ts.replace(tzinfo=datetime.timezone.utc)"
        date_from = date_from.isoformat()
        date_to = date_to.isoformat()
        return self.client._make_request('post', url=f'{self.api_root}/node_summary',
                                         data={'from': date_from, 'to': date_to})

    def user_breakdown(self, machine_id: str, date_from: datetime.datetime, date_to: datetime.datetime):
        assert date_from.tzinfo is not None and date_to.tzinfo is not None, \
            "Timezones are required, add it to timestamp via ts.replace(tzinfo=datetime.timezone.utc)"
        date_from = date_from.isoformat()
        date_to = date_to.isoformat()
        return self.client._make_request('post', url=f'{self.api_root}/user_breakdown',
                                        data={'machine_id': machine_id, 'from': date_from, 'to': date_to})
    

class SshKeysClient:
    def __init__(self, client: ['RiftClient']):
        self.client = client
        self.api_root = os.path.join(client.public_api_root, 'ssh-keys')

    def list(self):
        return self.client._make_request('post', url=f'{self.api_root}/list')['keys']

    def add(self, name: str, public_key: Optional[str] = None):
        data = {'name': name}
        if public_key is not None:
            data['public_key'] = public_key
        else:
            data['public_key'] = None
        return self.client._make_request('post', url=f'{self.api_root}/add', data=data)

    def delete(self, key_id: str):
        return self.client._make_request('delete', url=f'{self.api_root}/{key_id}')
    
    def delete_by_name(self, key_name: str):
        return self.client._make_request('post', url=f'{self.api_root}/delete', data={'selector': {'ByName': [key_name]}})
    
    def delete_all(self):
        return self.client._make_request('post', url=f'{self.api_root}/delete', data={'selector': 'All'})