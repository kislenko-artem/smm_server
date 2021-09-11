import time
from datetime import datetime

from smm.database.abstract import business


class Business(business.Business):

    async def list_categories(self) -> list:
        data = await self.select(
            "SELECT id, name, category_type FROM business_categories", ["id", "name", "category_type"])
        return data

    async def add_category(self, name: str, category_type: str) -> int:
        id = await self.insert(
            '''INSERT INTO business_categories (name, category_type) VALUES ($1, $2) ''',
            (name, category_type))
        return id

    async def del_category(self, id: int):
        await self.execute(
            '''DELETE FROM business_categories WHERE id = $1''', (id,))

    async def list_clients(self) -> list:
        r_data = []
        data = await self.select(
            "SELECT id, name, phone, email, comments, dt_create FROM business_clients",
            ["id", "name", "phone", "email", "comments", "dt_create"])
        for d in r_data:
            r_data.append({
                "dt_create": datetime.utcfromtimestamp(d["dt_create"]),
                "id": d["id"],
                "name": d["name"],
                "phone": d["phone"],
                "email": d["email"],
                "comments": d["comments"],
            })
        return data

    async def add_client(self, name: str, phone: str, email: str, comments: str) -> int:
        id = await self.insert(
            '''INSERT INTO business_clients (name, phone, email, comments, dt_create) VALUES ($1, $2, $3, $4, $5) ''',
            (name, phone, email, comments, time.mktime(datetime.now().timetuple())))
        return id

    async def update_client(self, id: int, name: str, phone: str, email: str, comments: str):
        await self.execute(
            '''UPDATE business_clients SET name=$1, phone=$2, email=$3, comments=$4 WHERE id = $5''',
            (name, phone, email, comments, id,))

    async def del_client(self, id: int):
        await self.execute(
            '''DELETE FROM business_clients WHERE id = $1''', (id,))

    async def list_incomes(self) -> list:
        r_data = []
        data = await self.select(
            "SELECT id, name, price, business_clients_id, business_categories_id, comments, dt_provision, dt_create FROM business_income",
            ["id", "name", "price", "business_clients_id", "business_categories_id", "comments", "dt_provision",
             "dt_create"])
        for d in r_data:
            r_data.append({
                "dt_provision": datetime.utcfromtimestamp(d["dt_provision"]),
                "dt_create": datetime.utcfromtimestamp(d["dt_create"]),
                "id": d["id"],
                "name": d["name"],
                "price": d["price"],
                "business_clients_id": d["business_clients_id"],
                "business_categories_id": d["business_categories_id"],
                "comments": d["comments"],
            })
        return data

    async def add_income(self, name: str, price: float, business_clients_id: int, business_categories_id: int,
                         comments: str, dt_provision: datetime) -> int:
        id = await self.insert(
            '''INSERT INTO business_income (name, price, business_clients_id, business_categories_id, comments, dt_provision, dt_create) VALUES ($1, $2, $3, $4, $5, $6, $7) ''',
            (name, price, business_clients_id, business_categories_id, comments, dt_provision,
             time.mktime(datetime.now().timetuple())))
        return id

    async def update_income(self, id: int, name: str, price: float, business_clients_id: int,
                            business_categories_id: int,
                            comments: str, dt_provision: datetime):
        await self.execute(
            '''UPDATE business_income SET name=$1, price=$2, business_clients_id=$3, business_categories_id=$4, comments=$5, dt_provision=$6 WHERE id = $7''',
            (name, price, business_clients_id, business_categories_id, comments, dt_provision, id,))

    async def del_income(self, id: int):
        await self.execute('''DELETE FROM business_income WHERE id = $1''', (id,))
