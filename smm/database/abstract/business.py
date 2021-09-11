from datetime import datetime

from smm.database.abstract import Methods


class Business(Methods):

    async def list_categories(self) -> list:
        raise NotImplemented("")

    async def add_category(self, name: str, category_type: str) -> int:
        raise NotImplemented("")

    async def del_category(self, id: int):
        raise NotImplemented("")

    async def list_clients(self) -> list:
        raise NotImplemented("")

    async def add_client(self, name: str, phone: str, email: str, comments: str) -> int:
        raise NotImplemented("")

    async def update_client(self, id: int, name: str, phone: str, email: str, comments: str):
        raise NotImplemented("")

    async def del_client(self, id: int):
        raise NotImplemented("")

    async def list_incomes(self) -> list:
        raise NotImplemented("")

    async def add_income(self, name: str, price: float, business_clients_id: int, business_categories_id: int,
                         comments: str, dt_provision: datetime) -> int:
        raise NotImplemented("")

    async def update_income(self, id: int, name: str, price: float, business_clients_id: int,
                            business_categories_id: int,
                            comments: str, dt_provision: datetime):
        raise NotImplemented("")

    async def del_income(self, id: int):
        raise NotImplemented("")
