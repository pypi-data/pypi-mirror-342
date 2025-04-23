import requests
import time
from typing import TypeAlias, Optional, Tuple, Union, Dict
from lattica_common.app_api import HttpClient, LatticaAppAPI

import secrets
import string

from lattica_management_src.lattica_management.lattica_management import LatticaManagement

AppResponse: TypeAlias = Union[str, dict]
WorkerStatus: TypeAlias = Dict[str, str]
ModelId: TypeAlias = str


class LatticaDeploy:
    # license_key is a JWT account token
    def __init__(self, license_key: str):
        """Initialize LatticaDeploy with a license key"""
        self.account_token = license_key
        self.agent_app = LatticaAppAPI(license_key, module_name='lattica_deployer')
        self.http_client = HttpClient(license_key, module_name='lattica_deployer')
        self.management = LatticaManagement(license_key)

    def create_model(
        self, 
        model_name: str, 
    ) -> str:
        return self.management.create_model(model_name)

    def _upload_model(self, model_file_path, model_id):
        print(f'Upload model...')
        response = self.http_client.send_http_request(
            'api/model/get_model_upload_url',
            req_params={'modelId': model_id}
        )
        
        upload_url = response['s3Url']
        key = response['s3Key']
        
        # Check for warning and print it if exists
        if 'warning' in response:
            print(f"Warning: {response['warning']}")

        self.agent_app.upload_file(model_file_path, upload_url)
        return key

    def upload_model_file(self, model_file_path, model_id, homomorphic_params):
        key = self._upload_model(model_file_path, model_id)

        alert_upload_complete = self.agent_app.alert_upload_complete(key, homomorphic_params)
        print(f"Model {model_id} uploaded status is {alert_upload_complete}.")

    def upload_plain_model_file(self, model_file_path: str, model_id: str) -> None:
        self.management.upload_plain_model(model_file_path, model_id)

    def generate_query_token(self, model_id: str, token_name: Optional[str] = None) -> str:
        return self.management.generate_query_token(model_id, token_name)

    def start_worker(self, model_id: str, verbose: bool = False) -> str:
        """Start a new worker session."""

        print(f"Allocate worker for {model_id=}...")
        worker_status = self.management.start_worker(model_id)
        
        if verbose:
            print(f'worker_status: {worker_status}')
        flag = True
        while worker_status['status'] != 'UP' or flag:
            if verbose:
                print(f'waiting for worker to init, '
                    f'last status: {worker_status}')
            time.sleep(1)
            worker_status = self.management.get_worker_status(
                model_id,
                worker_status['workerSessionId']
            )
            flag = False
        if verbose:
            print(f'worker_status: {worker_status}')
        return worker_status['workerSessionId']
