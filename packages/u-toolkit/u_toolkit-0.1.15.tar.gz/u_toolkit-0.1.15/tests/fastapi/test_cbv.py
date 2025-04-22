import asyncio
from typing import Annotated, cast

import sqlalchemy as sa
from fastapi import Depends, FastAPI, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.testclient import TestClient

from u_toolkit.fastapi.cbv import CBV


cbv = CBV()


def gen_value():
    return id(object())


dep1_value = gen_value()


def dep1():
    return dep1_value


dep2_value = gen_value()


def dep2():
    return dep2_value


dep3_value = gen_value()


def dep3():
    yield dep3_value


def db():
    with sa.create_engine(
        "sqlite+pysqlite:///:memory:", echo=True, future=True
    ).connect() as conn:
        yield conn


RESULT = "hello world"


@cbv
class R:
    value = Depends(dep1)
    value2: Annotated[int, Depends(dep2)]
    value3 = Depends(dep3)
    db_dep = cast(sa.Connection, Depends(db))

    def get(self):
        return self.value, self.value2, self.value3

    def get__wtf____(self):
        pass

    @cbv.info(path="/lalala")
    def get_custom(self): ...

    async def get_async_value(self):
        await asyncio.sleep(0.001)
        return 1

    @cbv.info(status=status.HTTP_201_CREATED)
    def post(self):
        record = self.db_dep.execute(sa.text(f"select '{RESULT}'")).one()
        return record[0]


@cbv
class _NoPath:
    value = Depends(dep1)

    def post_alala(
        self, data: Annotated[OAuth2PasswordRequestForm, Depends()]
    ):
        return data.username

    @cbv.info(methods=["DELETE"])
    async def post_wtf(self):
        await asyncio.sleep(1)
        return 1


app = FastAPI()


app.include_router(cbv.router)
client = TestClient(app)


def test_cbv():
    assert client.get("/r").json() == [dep1_value, dep2_value, dep3_value]
    assert client.get("/r/_wtf//").is_success
    assert client.get("/lalala").is_success
    assert client.get("/r/async_value").json() == 1

    post_resp = client.post("/r")
    assert post_resp.status_code == status.HTTP_201_CREATED
    assert post_resp.json() == RESULT

    value = "example"
    assert (
        client.post(
            "/alala",
            data={"username": value, "password": value},
        ).json()
        == value
    )
    assert client.delete("/post_wtf").json() == 1
