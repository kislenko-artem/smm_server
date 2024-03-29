from http import HTTPStatus
from datetime import datetime

from sanic.exceptions import InvalidUsage
from sanic.response import json

from smm.communicator.web.v0.base import Base
from smm.service import business, list_to_dict


class Offices(Base):
    async def get(self, request, id):
        g = await business.Office().list()
        d_list = []
        for d in g:
            d_list.append(d.__dict__)
        data = {
            "results": d_list
        }
        return json(data, HTTPStatus.OK)

    async def post(self, request, id):
        data = business.Office(
            name=request.json.get("name"),
        )
        d = await data.add()
        return json({"id": d.id}, HTTPStatus.OK)

    async def delete(self, request, id):
        if id == "":
            raise InvalidUsage("wrong parameter",
                               status_code=HTTPStatus.BAD_REQUEST)
        await business.Office(id=id).delete()
        return json({"success": True}, HTTPStatus.OK)

class Categories(Base):
    async def get(self, request, id):
        g = await business.Category().list()
        d_list = []
        for d in g:
            if id != "all" and d.category_type != id:
                continue
            d_list.append(d.__dict__)
        data = {
            "results": d_list
        }
        return json(data, HTTPStatus.OK)

    async def post(self, request, id):
        data = business.Category(
            name=request.json.get("name"),
            category_type=request.json.get("category_type")
        )
        d = await data.add()
        return json({"id": d.id}, HTTPStatus.OK)

    async def delete(self, request, id):
        if id == "":
            raise InvalidUsage("wrong parameter",
                               status_code=HTTPStatus.BAD_REQUEST)
        await business.Category(id=id).delete()
        return json({"success": True}, HTTPStatus.OK)


class SubCategories(Base):
    async def get(self, _request, id):
        g = await business.SubCategory().list()
        d_list = []
        for d in g:
            income = d.__dict__
            if income.get("category"):
                income["category"] = income.get("category").__dict__
            d_list.append(income)
        data = {
            "results": d_list
        }
        return json(data, HTTPStatus.OK)

    async def post(self, request, id):
        data = business.SubCategory(
            name=request.json.get("name"),
        )
        categories_index = {}
        categories = await business.Category.list()
        if request.json.get("category_id"):
            for d in categories:
                categories_index[d.id] = d
            data.category = categories_index[request.json.get("category_id")]

        d = await data.add()
        return json({"id": d.id}, HTTPStatus.OK)

    async def delete(self, request, id):
        if id == "":
            raise InvalidUsage("wrong parameter",
                               status_code=HTTPStatus.BAD_REQUEST)
        await business.SubCategory(_id=id).delete()
        return json({"success": True}, HTTPStatus.OK)


class Clients(Base):
    async def get(self, request, id):
        dt_start = None
        dt_end = None
        office_id = None
        if request.args.get("dt_start"):
            dt_start = datetime.strptime(request.args.get("dt_start"), "%Y-%m-%dT%H:%M:%S")
        if request.args.get("dt_end"):
            dt_end = datetime.strptime(request.args.get("dt_end"), "%Y-%m-%dT%H:%M:%S")
        if request.args.get("office_id"):
            office_id = int(request.args.get("office_id"))
        g = await business.Client().list(dt_start, dt_end, office_id)
        d_list = list_to_dict(g)
        data = {
            "results": d_list
        }
        return json(data, HTTPStatus.OK)

    async def post(self, request, id):
        data = business.Client(
            name=request.json.get("name"),
            phone=request.json.get("phone"),
            email=request.json.get("email"),
            comments=request.json.get("comments"),
            age=request.json.get("age"),
        )
        if request.json.get("dt_appearance"):
            try:
                dt = datetime.strptime(request.json.get("dt_appearance"), "%Y-%m-%d %H:%M:%S")
            except ValueError:
                dt = datetime.strptime(request.json.get("dt_appearance"), "%Y-%m-%d %H:%M:%S:00")
            data.dt_appearance = dt
        categories_index = {}
        categories = await business.Category.list()
        if request.json.get("category_id"):
            for d in categories:
                categories_index[d.id] = d
            data.category = categories_index[request.json.get("category_id")]
        subcategories_index = {}
        subcategories = await business.SubCategory.list()
        if request.json.get("subcategory_id") is not None:
            for d in subcategories:
                subcategories_index[d.id] = d
            data.subcategory = subcategories_index[request.json.get("subcategory_id")]
        if request.json.get("type_client_id"):
            for d in categories:
                categories_index[d.id] = d
            data.type_client = categories_index[request.json.get("type_client_id")]
        offices_index = {}
        offices = await business.Office.list()
        if request.json.get("office_id") is not None:
            for d in offices:
                offices_index[d.id] = d
            data.office = offices_index[request.json.get("office_id")]
        d = await data.add()
        return json({"id": d.id}, HTTPStatus.OK)

    async def put(self, request, id):
        if id == "":
            raise InvalidUsage("wrong parameter",
                               status_code=HTTPStatus.BAD_REQUEST)

        data = business.Client(
            id=id,
            name=request.json.get("name"),
            phone=request.json.get("phone"),
            email=request.json.get("email"),
            comments=request.json.get("comments"),
            age=request.json.get("age"),
        )
        if request.json.get("dt_appearance"):
            try:
                dt = datetime.strptime(request.json.get("dt_appearance"), "%Y-%m-%d %H:%M:%S")
            except ValueError:
                dt = datetime.strptime(request.json.get("dt_appearance"), "%Y-%m-%d %H:%M:%S:00")
            data.dt_appearance = dt
        categories_index = {}
        categories = await business.Category.list()
        if request.json.get("category_id") is not None:
            for d in categories:
                categories_index[d.id] = d
            data.category = categories_index[request.json.get("category_id")]
        subcategories_index = {}
        subcategories = await business.SubCategory.list()
        if request.json.get("subcategory_id") is not None:
            for d in subcategories:
                subcategories_index[d.id] = d
            data.subcategory = subcategories_index[request.json.get("subcategory_id")]
        if request.json.get("type_client_id"):
            for d in categories:
                categories_index[d.id] = d
            data.type_client = categories_index[request.json.get("type_client_id")]
        offices_index = {}
        offices = await business.Office.list()
        if request.json.get("office_id") is not None:
            for d in offices:
                offices_index[d.id] = d
            data.office = offices_index[request.json.get("office_id")]

        await data.update()
        return json({"success": True}, HTTPStatus.OK)

    async def delete(self, request, id):
        if id == "":
            raise InvalidUsage("wrong parameter",
                               status_code=HTTPStatus.BAD_REQUEST)
        await business.Client(id=id).delete()
        return json({"success": True}, HTTPStatus.OK)


class Incomes(Base):
    async def get(self, request, id):
        dt_start = None
        dt_end = None
        office_id = None
        if request.args.get("dt_start"):
            dt_start = datetime.strptime(request.args.get("dt_start"), "%Y-%m-%dT%H:%M:%S")
        if request.args.get("dt_end"):
            dt_end = datetime.strptime(request.args.get("dt_end"), "%Y-%m-%dT%H:%M:%S")
        if request.args.get("office_id"):
            office_id = int(request.args.get("office_id"))
        g = await business.Income().list(dt_start, dt_end, office_id)
        d_list = list_to_dict(g)
        data = {
            "results": d_list
        }
        return json(data, HTTPStatus.OK)

    async def post(self, request, id):
        try:
            dt = datetime.strptime(request.json.get("dt_provision"), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            dt = datetime.strptime(request.json.get("dt_provision"), "%Y-%m-%d %H:%M:%S:00")
        income = await business.Income().init(
            price=request.json.get("price"),
            category_id=request.json.get("category_id"),
            subcategory_id=request.json.get("subcategory_id"),
            office_id=request.json.get("office_id"),
            client_id=request.json.get("client_id"),
            comments=request.json.get("comments"),
            duration=request.json.get("duration"),
            dt_provision=dt
        )
        d = await income.add()
        return json({"id": d.id}, HTTPStatus.OK)

    async def put(self, request, id):
        if id == "":
            raise InvalidUsage("wrong parameter",
                               status_code=HTTPStatus.BAD_REQUEST)
        try:
            dt = datetime.strptime(request.json.get("dt_provision"), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            dt = datetime.strptime(request.json.get("dt_provision"), "%Y-%m-%d %H:%M:%S:00")

        income = await business.Income().init(
            id=id,
            price=request.json.get("price"),
            category_id=request.json.get("category_id"),
            subcategory_id=request.json.get("subcategory_id"),
            office_id=request.json.get("office_id"),
            client_id=request.json.get("client_id"),
            comments=request.json.get("comments"),
            duration=request.json.get("duration"),
            dt_provision=dt
        )
        await income.update()
        return json({"success": True}, HTTPStatus.OK)

    async def delete(self, request, id):
        if id == "":
            raise InvalidUsage("wrong parameter",
                               status_code=HTTPStatus.BAD_REQUEST)

        income = await business.Income().init(id=id)
        await income.delete()
        return json({"success": True}, HTTPStatus.OK)
