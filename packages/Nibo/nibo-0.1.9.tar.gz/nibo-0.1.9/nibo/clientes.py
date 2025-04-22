from nibo.api import ApiNibo


class ClientesNibo(ApiNibo):

    def __init__(self, id_nibo: str | dict = None):
        super().__init__()
        self.endpoint = "customers"
        self.cliente = None
        if self.cliente:
            self.seleciona_cliente(id_nibo)

    def seleciona_cliente(self, id_nibo):
        filtro_id = f"id eq {id_nibo}"
        params = {"$filter": filtro_id}
        self.cliente = self.api_request(self.endpoint, params)['items'][0]

    @property
    def nome(self):
        return self.cliente["name"] if self.cliente else None

    @property
    def tel(self):
        return self._tel()

    @property
    def email(self):
        return self._email()

    @property
    def cnpj_cpf(self):
        return self._cnpj_cpf()

    def _tel(self):
        try:
            contatos = self.cliente["communication"]
            numero_contato = None
            if contatos:
                telefone = contatos.get("phone")
                celular = contatos.get("cellPhone")
                if telefone:
                    numero_contato = telefone
                elif celular:
                    numero_contato = celular
            return numero_contato
        except Exception as e:
            print(f"Erro no contato - {e}")
            return

    def _email(self):
        try:
            contatos = self.cliente["communication"]
            email = self.cliente.get("email")
            if contatos:
                email = contatos.get("email")
            return email
        except Exception as e:
            print(f"Erro email - {e}")
            return

    def _cnpj_cpf(self):
        try:
            documento = self.cliente["document"]
            if documento:
                cnpj_cpf = documento["number"]
                return cnpj_cpf
        except Exception as e:
            print(f"Erro no documento (cnpj/cpf) - {e}")
            return


def lista_todos_clientes() -> list[dict]:
    # Requisição à API do Nibo
    endpoint = "customers"
    resposta = ApiNibo().api_request(endpoint)

    # Atribui a quantidade total de clientes existentes
    qtd_clientes = resposta["count"]

    # Lista para armazenar todos os clientes encontrados
    todos_os_clientes = []

    # Inicializa a variável página para requisição
    pagina = 0

    # Faz requisição até a quantidade de clientes na lista seja igual à
    # quantidade total de clientes definida na requisição inicial
    while len(todos_os_clientes) != qtd_clientes:

        # Define os parâmetros da requisição (paginamento)
        # "$orderBy" organiza os clientes por nome e "$skip" pula os clientes
        # já retornados na página anterior
        params = {"$orderBy": "name", "$skip": pagina}

        # Faz a requisição para a API e obtém a resposta
        resposta = ApiNibo().api_request(endpoint, params)

        # Armazena os dados da resposta (clientes da página)
        dados = resposta["items"]

        # Adiciona os clientes da página à lista todos_os_clientes
        for item in dados:
            todos_os_clientes.append(item)

        # Atualiza a variável da página para a próxima página de resultados
        # A cada requisição, avança 500 clientes para o próximo lote
        pagina += 500  # 500 é o máximo permitido por página pela API

    return todos_os_clientes

