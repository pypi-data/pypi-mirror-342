import os
from abc import abstractmethod
from typing import Optional, Mapping, Any, Union
from .internal import InternalApiClient
from .public import PublicApiClient

import requests
from requests import HTTPError

PUBLIC_API_VERSION = '~upcoming'


class RiftClient:
    def __init__(self,
                 server_address='https://cloudrift.ai',
                 user_email: Optional[str] = None,
                 user_password: Optional[str] = None,
                 token: Optional[str] = None,
                 api_key: Optional[str] = None):
        self.server_address = server_address
        self.public_api_root = os.path.join(server_address, 'api/v1')
        self.internal_api_root = os.path.join(server_address, 'internal')
        self.token = token
        self.pat = None
        if user_email is not None and user_password is not None:
            if self.token is not None:
                raise ValueError("Cannot provide both user_email and token")
            self.login(user_email, user_password)
        self.api_key = api_key

    def _make_request(self,
                      method: str,
                      url: str,
                      data: Optional[Mapping[str, Any]] = None,
                      version: Optional[str] = None,
                      **kwargs) -> Union[Mapping[str, Any], str, None]:
        headers = {}
        if self.api_key is not None:
            headers['X-API-Key'] = self.api_key
        if self.token is not None:
            headers['Authorization'] = f"Bearer {self.token}"

        if version is None and self.public_api_root in url:
            version = PUBLIC_API_VERSION

        if version is not None and data is not None:
            response = requests.request(method, url, headers=headers,
                                        json={"version": version, "data": data}, **kwargs)
        else:
            if data is not None:
                kwargs['data'] = data
            response = requests.request(method, url, headers=headers, **kwargs)
        if not response.ok:
            raise HTTPError(f"{response.reason}: {response.text}", response=response)
        try:
            response_json = response.json()
            if isinstance(response_json, str):
                return response_json
            if version is not None:
                assert version >= response_json['version']
            return response_json['data']
        except requests.exceptions.JSONDecodeError:
            return None

    def login(self, email: str, password: str):
        resp = self._make_request('post', f'{self.public_api_root}/auth/login',
                                  data={"email": email, "password": password})
        self.token = resp["token"]
        self.pat = resp['pat']
        return resp

    def logout(self):
        self._make_request('post', f'{self.public_api_root}/auth/logout')
        self.token = None

    def me(self):
        return self._make_request('post', f'{self.public_api_root}/auth/me')

    def internal(self):
        return InternalApiClient(self)

    def public(self):
        return PublicApiClient(self)
