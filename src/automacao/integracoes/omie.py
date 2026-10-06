from abc import ABC, abstractmethod


class ClienteOmie(ABC):
    def __init__(self, cliente: str, cnpj: str):
        self.cliente = cliente
        self.cnpj = cnpj


class AdapteeOmie(ClienteOmie, ABC):
    def __init__(self, cliente: str, cnpj: str):
        super().__init__(cliente, cnpj)

    @abstractmethod
    def adapter(self) -> None:
        pass
