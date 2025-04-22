import json
from typing import Any


def jsonable_encoder(data: Any):
    return json.loads(json.dumps(data, default=str))
