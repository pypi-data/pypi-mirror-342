from __future__ import annotations

from typing import Annotated, TypeVar


class doc(str):
    """A docstring for a type. Typically used in Annotated"""


T = TypeVar("T")
FieldName = Annotated[str, doc("field name of a class")]
ObjectPath = Annotated[
    str, doc("path of an object (e.g., can be function, class, etc.)")
]
