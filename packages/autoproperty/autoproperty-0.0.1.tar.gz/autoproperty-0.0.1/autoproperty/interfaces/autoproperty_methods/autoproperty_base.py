from typing import Protocol
from autoproperty.prop_settings import AutoPropAccessMod


class IAutopropBase(Protocol):
    __auto_prop__: bool
    __prop_attr_name__: str
    __prop_access__: AutoPropAccessMod
    __belongs__: object