from fastapi import APIRouter

from services.insight import Insight
from services.schemas.insight_schemas import GetIQLData, GetJoinedData, GetObjectData, UpdateObjectData
from settings import insight_mars_client

insight_router = APIRouter()


@insight_router.post("/get")
async def get_object(data: GetObjectData):
    return await Insight.get_object(client=insight_mars_client, data=data)


@insight_router.post("/iql")
async def get_objects(data: GetIQLData):
    return await Insight.get_objects(client=insight_mars_client, data=data)


@insight_router.post("/iql/join")
async def get_joined(data: GetJoinedData):
    result = await Insight.get_joined(client=insight_mars_client, data=data)
    for item in result:
        item.joined = sorted(item.joined, key=lambda i: i.id)
    return result


@insight_router.post("/update")
async def update_object(data: UpdateObjectData):
    return await Insight.update_object(client=insight_mars_client, data=data)
