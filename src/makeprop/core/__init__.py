import dataclasses
from typing import *

__all__ = ["makeprop"]

DEFAULT = object()


@dataclasses.dataclass
class makeprop:
    var: Optional[str] = None
    hasdeleter: bool = False
    deletervalue: object = None

    def __call__(self: Self, func: Callable) -> property:
        "This magic method implements calling the current instance."
        deletervalue: Any
        kwargs: dict[str, Any]
        var: Any
        if self.var is None:
            var = "_%s" % func.__name__
        else:
            var = self.var
        deletervalue = self.deletervalue
        kwargs = dict(doc=func.__doc__)

        def fget(_self: Self) -> Any:
            return getattr(_self, var)

        kwargs["fget"] = fget

        def fset(_self: Self, value: Any) -> None:
            setattr(_self, var, func(_self, value))

        kwargs["fset"] = fset

        if self.hasdeleter:

            def fdel(_self: Self) -> None:
                setattr(_self, var, func(_self, deletervalue))

            kwargs["fdel"] = fdel

        return property(**kwargs)

    @overload
    def __init__(self: Self, var: Optional[str] = None) -> None:
        "This magic method sets up the current instance."
        ...

    @overload
    def __init__(self: Self, var: Optional[str] = None, *, delete: object) -> None:
        "This magic method sets up the current instance."
        ...

    def __init__(
        self: Self,
        var: Optional[str] = None,
        *,
        delete: object = DEFAULT,
    ) -> None:
        "This magic method sets up the current instance."
        self.var = None if (var is None) else str(var)
        self.hasdeleter = delete is not DEFAULT
        self.deletervalue = delete if self.hasdeleter else None
