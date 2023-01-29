from datetime import datetime
from typing import List

from smm.database import get_connection


class Office(object):
    id: int
    name: str

    def __init__(self, id: int = None, name: str = None):
        self.id = id
        self.name = name

    @staticmethod
    async def list() -> List["Office"]:
        c_list: List["Office"] = []

        DB = await get_connection()
        categories = await DB.list_offices()

        for d in categories:
            c_list.append(Office(
                id=d.get("id"),
                name=d.get("name"),
            ))
        return c_list

    async def add(self) -> "Office":
        DB = await get_connection()
        self.id = await DB.add_office(self.name)
        return self

    async def delete(self):
        DB = await get_connection()
        await DB.del_office(self.id)

class Category(object):
    id: int
    name: str
    category_type: str

    def __init__(self, id: int = None, name: str = None, category_type: str = None):
        self.id = id
        self.name = name
        self.category_type = category_type

    @staticmethod
    async def list() -> List["Category"]:
        c_list: List["Category"] = []

        DB = await get_connection()
        categories = await DB.list_categories()

        for d in categories:
            c_list.append(Category(
                id=d.get("id"),
                name=d.get("name"),
                category_type=d.get("category_type"),
            ))
        return c_list

    async def add(self) -> "Category":
        DB = await get_connection()
        self.id = await DB.add_category(self.name, self.category_type)
        return self

    async def delete(self):
        DB = await get_connection()
        await DB.del_category(self.id)


class SubCategory(object):
    id: int
    name: str
    category: Category

    def __init__(self, _id: int = None, name: str = None, category: Category = None):
        self.id = _id
        self.name = name
        self.category = category

    @staticmethod
    async def list() -> List["SubCategory"]:
        c_list: List["SubCategory"] = []

        DB = await get_connection()
        subcategories = await DB.list_subcategories()

        categories_index = {}
        categories = await Category.list()
        for d in categories:
            categories_index[d.id] = d

        for d in subcategories:
            s = SubCategory(
                _id=d.get("id"),
                name=d.get("name"),
            )

            if d.get("business_category_id") and len(categories_index) > 0:
                s.category = categories_index.get(d.get("business_category_id"))

            c_list.append(s)

        return c_list

    async def add(self) -> "SubCategory":
        DB = await get_connection()

        category_id = None
        if self.category:
            category_id = self.category.id

        self.id = await DB.add_subcategory(self.name, category_id)
        return self

    async def delete(self):
        DB = await get_connection()
        await DB.del_subcategory(self.id)


class Client(object):
    id: int
    name: str
    phone: str
    email: str
    comments: str
    dt_create: datetime
    age: int
    dt_appearance: datetime
    category: Category
    subcategory: SubCategory
    type_client: Category
    office: Office

    def __init__(self, id: int = None, name: str = None, phone: str = None, email: str = None, comments: str = None,
                 dt_create: datetime = None, age: int = None, dt_appearance: datetime = None,
                 category: Category = None, subcategory: SubCategory = None, type_client: Category = None, office: Office = None):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.comments = comments
        self.dt_create = dt_create
        self.age = age
        self.dt_appearance = dt_appearance
        self.category = category
        self.subcategory = subcategory
        self.office = office
        self.type_client = type_client

    @staticmethod
    async def list(dt_start: datetime = None, dt_end: datetime = None, office_id: int = None) -> List["Client"]:
        c_list: List["Client"] = []

        DB = await get_connection()
        clients = await DB.list_clients(dt_start, dt_end, office_id)

        offices_index = {}
        offices = await Office.list()
        for d in offices:
            offices_index[d.id] = d

        categories_index = {}
        categories = await Category.list()
        for d in categories:
            categories_index[d.id] = d

        subcategories_index = {}
        subcategories = await SubCategory.list()
        for d in subcategories:
            subcategories_index[d.id] = d

        for d in clients:
            c = Client(
                id=d.get("id"),
                name=d.get("name"),
                comments=d.get("comments"),
                phone=d.get("phone"),
                email=d.get("email"),
                dt_create=d.get("dt_create"),
                age=d.get("age"),
                dt_appearance=d.get("dt_appearance"),
            )
            if d.get("business_categories_id") and len(categories_index) > 0:
                c.category = categories_index.get(d.get("business_categories_id"))
            if d.get("business_subcategories_id") and len(subcategories_index) > 0:
                c.subcategory = subcategories_index.get(d.get("business_subcategories_id"))
            if d.get("type_categories_id") and len(categories_index) > 0:
                c.type_client = categories_index.get(d.get("type_categories_id"))
            if d.get("office_id") and len(offices_index) > 0:
                c.office = offices_index.get(d.get("office_id"))
            c_list.append(c)
        return c_list

    async def add(self) -> "Client":
        DB = await get_connection()
        category_id = None
        if self.category:
            category_id = self.category.id
        subcategory_id = None
        if self.subcategory:
            subcategory_id = self.subcategory.id
        office_id = None
        if self.office:
            office_id = self.office.id
        type_id = None
        if self.type_client:
            type_id = self.type_client.id
        self.id = await DB.add_client(self.name, self.phone, self.email, self.comments, self.age,
                                      self.dt_appearance, category_id, subcategory_id, type_id, office_id)
        return self

    async def delete(self):
        DB = await get_connection()
        await DB.del_client(self.id)

    async def update(self):
        DB = await get_connection()
        category_id = None
        if self.category:
            category_id = self.category.id
        subcategory_id = None
        if self.subcategory:
            subcategory_id = self.subcategory.id
        office_id = None
        if self.office:
            office_id = self.office.id
        type_id = None
        if self.type_client:
            type_id = self.type_client.id
        await DB.update_client(self.id, self.name, self.phone, self.email, self.comments, self.age,
                               self.dt_appearance, category_id, subcategory_id, type_id, office_id)


class Income(object):
    id: int
    price: float
    client: Client
    category: Category
    subcategory: SubCategory
    office: Office
    comments: str
    dt_provision: datetime
    dt_create: datetime
    duration: float

    def __init__(self, id: int = None, price: float = None, dt_provision: datetime = None,
                 dt_create: datetime = None, comments: str = None,
                 category: "Category" = None, subcategory: "SubCategory" = None, client: "Client" = None,
                 duration: float = None, office: "Office" = None,):
        self.id = id
        self.price = price
        self.dt_provision = dt_provision
        self.comments = comments
        self.category = category
        self.subcategory = subcategory
        self.client = client
        self.dt_create = dt_create
        self.duration = duration
        self.office = office

    async def init(self, id: int = None, price: float = None, dt_provision: datetime = None,
                   comments: str = None, category_id: int = None, subcategory_id: int = None, client_id: int = None,
                   duration: float = None, office_id: int = None) -> "Income":

        self.id = id
        self.price = price
        self.dt_provision = dt_provision
        self.comments = comments
        self.duration = duration
        if office_id is not None:
            office_index = {}
            offices = await Office.list()
            for d in offices:
                office_index[d.id] = d
            self.office = office_index.get(office_id)
        if client_id is not None:
            clients_index = {}
            clients = await Client.list()
            for d in clients:
                clients_index[d.id] = d
            self.client = clients_index.get(client_id)
        if category_id is not None:
            categories_index = {}
            categories = await Category.list()
            for d in categories:
                categories_index[d.id] = d
            self.category = categories_index[category_id]
        if subcategory_id is not None:
            subcategories_index = {}
            subcategories = await SubCategory.list()
            for d in subcategories:
                subcategories_index[d.id] = d
            self.subcategory = subcategories_index.get(subcategory_id)
        return self

    @staticmethod
    async def list(dt_start: datetime = None, dt_end: datetime = None, office_id: int = None) -> List["Income"]:
        c_list: List["Income"] = []

        DB = await get_connection()
        incomes = await DB.list_incomes(dt_start, dt_end, office_id)

        offices_index = {}
        offices = await Office.list()
        for d in offices:
            offices_index[d.id] = d

        categories_index = {}
        categories = await Category.list()
        for d in categories:
            categories_index[d.id] = d

        clients_index = {}
        clients = await Client.list()
        for d in clients:
            clients_index[d.id] = d

        subcategories_index = {}
        subcategories = await SubCategory.list()
        for d in subcategories:
            subcategories_index[d.id] = d

        for d in incomes:
            in_data = Income(
                id=d.get("id"),
                price=d.get("price"),
                category=categories_index.get(d.get("business_categories_id")),
                subcategory=subcategories_index.get(d.get("business_subcategories_id")),
                office=offices_index.get(d.get("office_id")),
                comments=d.get("comments"),
                dt_provision=d.get("dt_provision"),
                dt_create=d.get("dt_create"),
                duration=d.get("duration"),
            )
            if d.get("business_clients_id") is not None:
                in_data.client = clients_index.get(d.get("business_clients_id"))
            c_list.append(in_data)
        return c_list

    async def add(self) -> "Client":
        DB = await get_connection()
        client_id = None
        if self.client is not None:
            client_id = self.client.id
        subcategory_id = None
        if self.subcategory:
            subcategory_id = self.subcategory.id
        office_id = None
        if self.office:
            office_id = self.office.id
        self.id = await DB.add_income(self.price, client_id, self.category.id, self.comments,
                                      self.dt_provision, subcategory_id, self.duration, office_id)
        return self

    async def delete(self):
        DB = await get_connection()
        await DB.del_income(self.id)

    async def update(self):
        DB = await get_connection()
        client_id = None
        if self.client is not None:
            client_id = self.client.id
        subcategory_id = None
        if self.subcategory:
            subcategory_id = self.subcategory.id
        office_id = None
        if self.office:
            office_id = self.office.id
        await DB.update_income(self.id, self.price, client_id, self.category.id, self.comments,
                               self.dt_provision, subcategory_id, self.duration, office_id)
