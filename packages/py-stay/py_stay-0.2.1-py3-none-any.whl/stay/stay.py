from argparse import ArgumentParser, Namespace
from typing import TYPE_CHECKING, Any, ClassVar, Generic, Optional, Sequence, Type, TypeVar

from typing_extensions import override

_T = TypeVar("_T", bound="Stayspace")
_U = TypeVar("_U", bound="Stayspace")


class InvalidParentParserError(Exception):
    def __init__(self, this_parser: "StayParser[_T]", parent_parser: "StayParser[_U]") -> None:
        super().__init__(
            f"Incompatible parent parser {parent_parser}. "
            f"{parent_parser._namespace_cls} is not a superclass of {this_parser._namespace_cls}."  # noqa: SLF001
        )


class Stayspace(Namespace):
    if TYPE_CHECKING:
        # This prevents the type checker from allowing any field from working
        __getattr__: ClassVar[None]  # type: ignore
        __setattr__: ClassVar[None]  # type: ignore


class StayParser(ArgumentParser, Generic[_T]):
    _namespace_cls: Type[_T]

    @override
    def __init__(
        self,
        *args: Any,
        namespace_cls: Type[_T],
        parents: Sequence[ArgumentParser] = [],  # Why python...
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, parents=parents, **kwargs)  # type: ignore

        self._namespace_cls = namespace_cls

        for p in parents:
            if isinstance(p, StayParser):  # noqa: SIM102
                if not issubclass(self._namespace_cls, p._namespace_cls):  # noqa: SLF001
                    raise InvalidParentParserError(self, p)

    @override
    def parse_args(  # type: ignore
        self,
        args: Optional[Sequence[str]] = None,
        namespace: Optional[Type[_T]] = None,
    ) -> _T:
        ns = self._namespace_cls
        return super().parse_args(args=args, namespace=ns())
