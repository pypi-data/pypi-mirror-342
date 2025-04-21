
from dotenv import load_dotenv
import logging
import os
from pydantic import BaseModel, ValidationError
import requests
from requests.exceptions import HTTPError, RequestException

# Carrega o token da variavél de ambiente "API_TOKEN_NIBO"
load_dotenv()
token = os.getenv("API_TOKEN_NIBO")

class ApiParams(BaseModel):
    url_end : str
    params : dict | None


class ApiNibo:

    def __init__(self):
        self.token = token
        self.base_url = "https://api.nibo.com.br/empresas/v1/"


    def api_request(self, url_end: str, params: dict = None) -> dict | None:
        """
            Faz uma requisição GET para a API da Nibo.

            Args:
                url_end: Endpoint específico da API (ex: 'clientes', 'notas').
                params: Parâmetros de query string para a requisição.

            Returns:
                requests.Response.json | None: Dicionário JSON da  resposta da
                    requisição ou None em caso de erro.
            """
        # Valida parâmetros
        parametros_validos = ApiParams(url_end=url_end, params=params)
        url_end = parametros_validos.url_end
        params = parametros_validos.params


        api_url = self.base_url + url_end
        headers = {
            "accept": "application/json",
            "apitoken": self.token,
        }
        try:
            response = requests.get(api_url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()

        # Erros
        except ValidationError as validation_err:
            logging.error(f"Erro de validação: {validation_err}")
        except HTTPError as http_err:
            status = getattr(http_err.response, 'status_code', 'sem status')
            logging.error(
                f"HTTP Nibo ({url_end}): {http_err} - Status code: {status}"
            )
        except RequestException as req_err:
            logging.error(f"requisição Nibo: {req_err}")
        except Exception as err:
            logging.error(f"inesperado na requisição Nibo: {err}")
