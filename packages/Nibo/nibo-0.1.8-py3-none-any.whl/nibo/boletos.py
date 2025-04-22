from datetime import date

from nibo.api import ApiNibo


def lista_boletos(data: date = date.today()) -> list[dict]:
    """
    Retorna uma lista com os boletos gerados na data informada usando API do Nibo.

    Esta função consulta a API para verificar se existem boletos gerados na data fornecida.
    A data é comparada com o campo `createAt` dos boletos na API, filtrando por ano, mês e dia.

    Args:
        data (date): Data para verificar se existem boletos gerados. Exemplo: date(2024, 12, 25).

    Retruns:
        list[dict]: lista de boletos gerados, onde cada item é um dicionário com informações do boleto.
            Retorna uma lista vazia caso nenhum boleto seja encontrado na data especificada.
    """

    # Formata o filtro para consulta de acordo com a data
    filtro_data = f"year(createAt) eq {data.year} AND month(createAt) eq {data.month} AND day(createAt) eq {data.day}"

    # Configuração da requisição
    boleto_api_url = f"schedules/credit/promise"
    params = {
        "$filter": filtro_data,
    }

    # Requisição
    # response = api_nibo_request(boleto_api_url, params)
    resposta = ApiNibo().api_request(boleto_api_url, params)

    # Resposta itens no formato JSON (dicionário em python)
    boletos_items = resposta["items"]

    return boletos_items
