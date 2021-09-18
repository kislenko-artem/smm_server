from http import HTTPStatus
from datetime import datetime

from sanic.exceptions import InvalidUsage
from sanic.response import json

from smm.communicator.web.v0.base import Base
from smm.service import business


class Categories(Base):
    async def get(self, request, id):
        g = await business.Category().list()
        d_list = []
        for d in g:
            if d.category_type != id:
                continue
            d_list.append(d.__dict__)
        data = {
            "results": d_list
        }
        return json(data, HTTPStatus.OK)

    async def post(self, request, id):
        if id != "":
            raise InvalidUsage("wrong parameter",
                               status_code=HTTPStatus.BAD_REQUEST)

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


class Clients(Base):
    async def get(self, request, id):
        g = await business.Client().list()
        d_list = []
        for d in g:
            income = d.__dict__
            if income.get("category"):
                income["category"] = income.get("category").__dict__
            if income.get("dt_appearance"):
                income["dt_appearance"] = income.get("dt_appearance").isoformat()
            if income.get("dt_create"):
                income["dt_create"] = income.get("dt_create").isoformat()
            d_list.append(income)
        data = {
            "results": d_list
        }
        return json(data, HTTPStatus.OK)

    async def post(self, request, id):
        if id != "":
            raise InvalidUsage("wrong parameter",
                               status_code=HTTPStatus.BAD_REQUEST)

        data = business.Client(
            name=request.json.get("name"),
            phone=request.json.get("phone"),
            email=request.json.get("email"),
            comments=request.json.get("comments"),
            age=request.json.get("age"),
            note=request.json.get("note"),
        )
        if request.json.get("dt_appearance"):
            data.dt_appearance = datetime.strptime(request.json.get("dt_appearance"), "%Y-%m-%d %H:%M:%S")
        if request.json.get("category_id"):
            categories_index = {}
            categories = await business.Category.list()
            for d in categories:
                categories_index[d.id] = d
            data.category = categories_index[request.json.get("category_id")]
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
            note=request.json.get("note"),
        )
        if request.json.get("dt_appearance"):
            data.dt_appearance = datetime.strptime(request.json.get("dt_appearance"), "%Y-%m-%d %H:%M:%S")
        if request.json.get("category_id") is not None:
            categories_index = {}
            categories = await business.Category.list()
            for d in categories:
                categories_index[d.id] = d
            data.category = categories_index[request.json.get("category_id")]

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
        g = await business.Income().list()
        d_list = []
        for d in g:
            income = d.__dict__
            if income.get("client"):
                if isinstance(income.get("client"), dict) is False:
                    income["client"] = income.get("client").__dict__
                if isinstance(income["client"].get("category"), dict) is False:
                    income["client"]["category"] = income["client"].get("category").__dict__
                if isinstance(income["client"].get("dt_appearance"), str) is False:
                    income["client"]["dt_appearance"] = income["client"].get("dt_appearance").isoformat()
                if isinstance(income["client"].get("dt_create"), str) is False:
                    income["client"]["dt_create"] = income["client"].get("dt_create").isoformat()
            if income.get("category"):
                income["category"] = income.get("category").__dict__
            if income.get("dt_provision"):
                income["dt_provision"] = income.get("dt_provision").isoformat()
            if income.get("dt_create"):
                income["dt_create"] = income.get("dt_create").isoformat()
            d_list.append(income)
        data = {
            "results": d_list
        }
        return json(data, HTTPStatus.OK)

    async def post(self, request, id):
        if id != "":
            raise InvalidUsage("wrong parameter",
                               status_code=HTTPStatus.BAD_REQUEST)

        income = await business.Income().init(
            price=request.json.get("price"),
            category_id=request.json.get("category_id"),
            client_id=request.json.get("client_id"),
            comments=request.json.get("comments"),
            duration=request.json.get("duration"),
            dt_provision=datetime.strptime(request.json.get("dt_provision"), "%Y-%m-%d %H:%M:%S")
        )
        d = await income.add()
        return json({"id": d.id}, HTTPStatus.OK)

    async def put(self, request, id):
        if id == "":
            raise InvalidUsage("wrong parameter",
                               status_code=HTTPStatus.BAD_REQUEST)

        income = await business.Income().init(
            id=id,
            price=request.json.get("price"),
            category_id=request.json.get("category_id"),
            client_id=request.json.get("client_id"),
            comments=request.json.get("comments"),
            duration=request.json.get("duration"),
            dt_provision=datetime.strptime(request.json.get("dt_provision"), "%Y-%m-%d %H:%M:%S")
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
