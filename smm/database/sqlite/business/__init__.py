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

    async def list_clients(self, dt_start: datetime = None, dt_end: datetime = None) -> list:
        r_data = []
        params = []
        conditions = []
        if dt_start:
            params.append(time.mktime(dt_start.timetuple()))
            conditions.append("dt_create > ${}".format(len(params)))
        if dt_end:
            params.append(time.mktime(dt_end.timetuple()))
            conditions.append("dt_create < ${}".format(len(params)))
        query = "SELECT id, name, phone, email, comments, dt_create, age, dt_appearance, business_categories_id, note, type_categories_id FROM business_clients "
        if conditions:
            query += "WHERE {}".format(" AND ".join(conditions))
        query += " ORDER BY dt_create DESC"
        data = await self.select(query,
                                 ["id", "name", "phone", "email", "comments", "dt_create", "age", "dt_appearance",
                                  "business_categories_id", "note", "type_categories_id"],
                                 params)
        for d in data:
            item = {
                "dt_create": datetime.utcfromtimestamp(d["dt_create"]),
                "id": d["id"],
                "name": d["name"],
                "phone": d["phone"],
                "email": d["email"],
                "comments": d["comments"],
                "age": d["age"],
                "business_categories_id": d.get("business_categories_id"),
                "type_categories_id": d.get("type_categories_id"),
                "note": d["note"],
            }
            if d["dt_appearance"] is not None:
                item["dt_appearance"] = datetime.utcfromtimestamp(d["dt_appearance"])
            r_data.append(item)

        return r_data

    async def add_client(self, name: str, phone: str, email: str, comments: str, age: int = None,
                         dt_appearance: datetime = None, business_categories_id: int = None, note: int = None,
                         type_categories_id: int = None) -> int:
        dt_appearance_int = None
        if dt_appearance is not None:
            dt_appearance_int = time.mktime(dt_appearance.timetuple())
        id = await self.insert(
            '''INSERT INTO business_clients 
            (name, phone, email, comments, dt_create, age, dt_appearance, business_categories_id, type_categories_id, note) 
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10) ''',
            (name, phone, email, comments, time.mktime(datetime.now().timetuple()), age, dt_appearance_int,
             business_categories_id, type_categories_id, note))
        return id

    async def update_client(self, id: int, name: str, phone: str, email: str, comments: str, age: int = None,
                            dt_appearance: datetime = None, business_categories_id: int = None, note: int = None,
                            type_categories_id: int = None):
        dt_appearance_int = None
        if dt_appearance is not None:
            dt_appearance_int = time.mktime(dt_appearance.timetuple())
        await self.execute(
            '''UPDATE business_clients 
            SET name=$1, phone=$2, email=$3, comments=$4, age=$5, 
                dt_appearance=$6, business_categories_id=$7, type_categories_id=$8, note=$9 
            WHERE id = $10''',
            (name, phone, email, comments, age, dt_appearance_int, business_categories_id, type_categories_id, note,
             id,))

    async def del_client(self, id: int):
        await self.execute(
            '''DELETE FROM business_clients WHERE id = $1''', (id,))

    async def list_incomes(self, dt_start: datetime = None, dt_end: datetime = None) -> list:
        r_data = []
        params = []
        conditions = []
        query = "SELECT id, price, business_clients_id, business_categories_id, comments, dt_provision, dt_create, duration FROM business_income "
        if dt_start:
            params.append(time.mktime(dt_start.timetuple()))
            conditions.append("dt_provision > ${}".format(len(params)))
        if dt_end:
            params.append(time.mktime(dt_end.timetuple()))
            conditions.append("dt_provision < ${}".format(len(params)))
        if conditions:
            query += "WHERE {}".format(" AND ".join(conditions))
        query += " ORDER BY dt_provision DESC"
        data = await self.select(
            query,
            ["id", "price", "business_clients_id", "business_categories_id", "comments", "dt_provision",
             "dt_create", "duration"], params)
        for d in data:
            r_data.append({
                "dt_provision": datetime.utcfromtimestamp(d["dt_provision"]),
                "dt_create": datetime.utcfromtimestamp(d["dt_create"]),
                "id": d["id"],
                "price": d["price"],
                "business_clients_id": d["business_clients_id"],
                "business_categories_id": d["business_categories_id"],
                "comments": d["comments"],
                "duration": d["duration"],
            })
        return r_data

    async def add_income(self, price: float, business_clients_id: int, business_categories_id: int,
                         comments: str, dt_provision: datetime, duration: float = None) -> int:
        dt_provision_int = None
        if dt_provision is not None:
            dt_provision_int = time.mktime(dt_provision.timetuple())
        id = await self.insert(
            '''INSERT INTO business_income 
            (price, business_clients_id, business_categories_id, comments, dt_provision, dt_create, duration) 
            VALUES ($1, $2, $3, $4, $5, $6, $7) ''',
            (price, business_clients_id, business_categories_id, comments, dt_provision_int,
             time.mktime(datetime.now().timetuple()), duration))
        return id

    async def update_income(self, id: int, price: float, business_clients_id: int,
                            business_categories_id: int,
                            comments: str, dt_provision: datetime, duration: float = None):
        dt_provision_int = None
        if dt_provision is not None:
            dt_provision_int = time.mktime(dt_provision.timetuple())
        await self.execute(
            '''UPDATE business_income SET 
            price=$1, business_clients_id=$2, business_categories_id=$3, comments=$4, dt_provision=$5 , duration=$6 WHERE id = $7''',
            (price, business_clients_id, business_categories_id, comments, dt_provision_int, duration, id,))

    async def del_income(self, id: int):
        await self.execute('''DELETE FROM business_income WHERE id = $1''', (id,))
