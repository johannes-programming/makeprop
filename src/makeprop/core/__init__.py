import dataclasses
from collections.abc import Callable
from typing import Any, Final, Optional, Self, overload

import setdoc

__all__ = ["makeprop"]

DEFAULT: Final[object] = object()


@dataclasses.dataclass
class makeprop:
    var: Optional[str] = None
    hasdeleter: bool = False
    deletervalue: object = None

    @setdoc.basic
    def __call__(self: Self, func: Callable[..., Any]) -> property:
        deletervalue: Any
        kwargs: dict[str, Any]
        var: Any
        if self.var is None:
            var = "_%s" % func.__name__
        else:
            var = self.var
        deletervalue = self.deletervalue
        kwargs = dict(doc=func.__doc__)

        @setdoc.basic
        def fget(_self: Self) -> Any:
            return getattr(_self, var)

        kwargs["fget"] = fget

        @setdoc.basic
        def fset(_self: Self, value: Any) -> None:
            setattr(_self, var, func(_self, value))

        kwargs["fset"] = fset

        if self.hasdeleter:

            @setdoc.basic
            def fdel(_self: Self) -> None:
                setattr(_self, var, func(_self, deletervalue))

            kwargs["fdel"] = fdel

        return property(**kwargs)

    @overload
    @setdoc.basic
    def __init__(self: Self, var: Optional[str] = None) -> None: ...

    @overload
    @setdoc.basic
    def __init__(
        self: Self, var: Optional[str] = None, *, delete: object
    ) -> None: ...

    @setdoc.basic
    def __init__(
        self: Self,
        var: Optional[str] = None,
        *,
        delete: object = DEFAULT,
    ) -> None:
        self.var = None if (var is None) else str(var)
        self.hasdeleter = delete is not DEFAULT
        self.deletervalue = delete if self.hasdeleter else None
