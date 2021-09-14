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
            d_list.append(d.__dict__)
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
            comments=request.json.get("comments")
        )
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
            comments=request.json.get("comments")
        )
        d = await data.update()
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
            if income.get("client") is not None:
                income["client"] = income.get("client").__dict__
            if income.get("category") is not None:
                income["category"] = income.get("category").__dict__
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
            name=request.json.get("name"),
            price=request.json.get("price"),
            category_id=request.json.get("category_id"),
            client_id=request.json.get("client_id"),
            comments=request.json.get("comments"),
            dt_provision=datetime.strptime(request.json.get("dt_provision"), "%d-%m-%Y %H:%M:%S")
        )
        d = await income.add()
        return json({"id": d.id}, HTTPStatus.OK)

    async def put(self, request, id):
        if id == "":
            raise InvalidUsage("wrong parameter",
                               status_code=HTTPStatus.BAD_REQUEST)

        income = await business.Income().init(
            id=id,
            name=request.json.get("name"),
            price=request.json.get("price"),
            category_id=request.json.get("category_id"),
            client_id=request.json.get("client_id"),
            comments=request.json.get("comments"),
            dt_provision=datetime.strptime(request.json.get("dt_provision"), "%d-%m-%Y %H:%M:%S")
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
