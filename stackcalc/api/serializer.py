import inspect
import json

from pydantic import BaseModel

import stackcalc.api.auth.models
import stackcalc.api.engine.models

MODEL_TYPE_TO_MODULE_MAP: dict = {}
for mod in [stackcalc.api.auth.models, stackcalc.api.engine.models]:
    for cls_name, cls_obj in inspect.getmembers(mod):
        if inspect.isclass(cls_obj):
            MODEL_TYPE_TO_MODULE_MAP[cls_name] = mod


class PydanticSerializer(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, BaseModel):
            return o.model_dump() | {"__type__": type(o).__name__}
        else:
            return json.JSONEncoder.default(self, o)


def pydantic_decoder(obj):
    if "__type__" in obj:
        the_type = obj["__type__"]
        if the_type in MODEL_TYPE_TO_MODULE_MAP:
            cls = getattr(MODEL_TYPE_TO_MODULE_MAP[the_type], the_type)
            return cls.parse_obj(obj)
    return obj


def pydantic_dumps(obj):
    return json.dumps(obj, cls=PydanticSerializer)


def pydantic_loads(obj):
    return json.loads(obj, object_hook=pydantic_decoder)
