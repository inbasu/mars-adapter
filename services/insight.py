from typing import Any

from .connection import Client
from .schemas import (AttrValue, FieldScheme, GetObjectData, ObjectAttr,
                      ObjectResponse)


class Insight:    
    @classmethod
    def form_json(cls, scheme: int, iql: str,result_per_page:int ,page: int, deep: int=1) -> dict[str, Any]:
        return {
                "scheme": scheme,
                "iql": iql,
                "options": {
                    "page": page,
                    "resultPerPage": result_per_page,
                    "includeAttributes": True,
                    "includeAttributesDeep": deep,
                    },
                }



    @classmethod
    async def get_object(cls, client: Client, data: GetObjectData, fields:dict[int, FieldScheme]) -> ObjectResponse | None:
        # перенести fields внутрь локиги класса
        json =  cls.form_json(scheme=data.scheme, iql=f"objectId = {data.object_id}", page=1, result_per_page=1)
        result = await client.post('iql/run',data=json)
        raw_object = result.json()
        return cls.decode(raw_object["objectEntries"][0], fields) if raw_object.get("objectEntries", None) else None


    @classmethod
    async def get_object_fields(cls, client: Client, data: GetObjectData):
        json = {"scheme": data.scheme, "method": "attributes", "objectTypeId": data.object_id}
        result = await client.post("objects/run", data=json)
        return [cls.decode_field(field) for field in result.json()]




    @classmethod
    def decode(cls, raw_object: dict, fields: dict[int, FieldScheme]) -> ObjectResponse:
        obj = ObjectResponse(id=raw_object["id"], attrs=[])
        for attr in raw_object["attributes"]:
            object_attr = ObjectAttr(id=attr["objectTypeAttributeId"], 
                                     name=fields[attr["objectTypeAttributeId"]].name, 
                                     ref=fields[attr["objectTypeAttributeId"]].ref, values=[])      
            for val in attr["objectAttributeValues"]:
                object_attr.values.append(AttrValue(id=val["referencedObject"]['id'] if object_attr.ref else None, 
                                                    label=val["displayValue"]))
            obj.attrs.append(object_attr)
        return obj


    @classmethod
    def decode_field(cls, field: dict) -> FieldScheme:
        return FieldScheme(id=field["id"], name=field["name"], ref=field.get("referenceObjectTypeId", None))
    


