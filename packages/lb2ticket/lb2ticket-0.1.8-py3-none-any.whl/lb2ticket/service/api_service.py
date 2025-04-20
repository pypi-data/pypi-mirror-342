import requests
from lb2ticket.decrypt_utils import decrypt 
import base64
import json


def create_config(token):
    client_token = token
   
    try:
        decoded = base64.b64decode(client_token).decode()
        values = decoded.split(":")
        json_str = decrypt(values[0], values[1])
        json_obj = json.loads(json_str)
        token = json_obj.get("st_as2asdfa2221")
        agent_client_id = json_obj.get("clientId")
        company_id = json_obj.get("companyId")
        return AppConfig(token, agent_client_id, company_id)

    except Exception as e:
        print(f"Error decoding token: {e}")

class ApiException(Exception):
    pass


class AppConfig:
    def __init__(self, client_token: str, client_id: str, company_id: str):
        self.client_token = client_token
        self.client_id = client_id
        self.company_id = company_id
        self.workestre_url = "https://api-workestre.lb2.com.br/api/monitoring/agent/"


class APIService:
    def __init__(self, application_config: AppConfig):
        self.server_url = application_config.workestre_url
        self.base_url = "/v1/"
        self.auth_token = application_config.client_token
        self.client_id = application_config.client_id
        self.company_id = application_config.company_id

    def mount_headers(self) -> dict:
        return {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.auth_token}",
            "requested-client-x": self.client_id,
            "requester-company-x": self.company_id,
        }

    def mount_api_error(self, e: Exception) -> str:
        return f"Erro na comunicação com o servidor: {str(e)}"

    def post(self, obj, path = ""):
        try:
            url = f"{self.server_url}{self.base_url}{path}"
            headers = self.mount_headers()
            response = requests.post(url, json=obj, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise ApiException(self.mount_api_error(e))

    def put(self, obj= None, path= ""):
        try:
            url = f"{self.server_url}{self.base_url}{path}"
            headers = self.mount_headers()
            response = requests.put(url, json=obj, headers=headers)
            response.raise_for_status()
        except Exception as e:
            raise ApiException(self.mount_api_error(e))

    def get(self, path: str):
        try:
            url = f"{self.server_url}{self.base_url}{path}"
            headers = self.mount_headers()
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            if response.content and response.content.strip():
                return response.json()
            else:
                return None
        except Exception as e:
            raise ApiException(self.mount_api_error(e))

    def get_list(self, path: str):
        try:
            url = f"{self.server_url}{self.base_url}{path}"
            headers = self.mount_headers()
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            if response.content and response.content.strip():
                return response.json()
            else:
                return None
        except Exception as e:
            raise ApiException(self.mount_api_error(e))
