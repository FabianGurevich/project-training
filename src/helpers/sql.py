from typing import Any

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression
from sqlalchemy.types import Uuid


class random_uuid(expression.FunctionElement):
    type = Uuid()
    inherit_cache = False


@compiles(random_uuid, "postgresql")
def pg_uuid(element: Any, compiler: Any, **kw: Any) -> str:
    return "gen_random_uuid()"
