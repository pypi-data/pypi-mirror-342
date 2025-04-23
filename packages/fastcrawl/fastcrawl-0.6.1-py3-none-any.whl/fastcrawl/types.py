from typing import (
    TYPE_CHECKING,
    Any,
    AsyncIterator,
    Callable,
    Coroutine,
    Mapping,
    Optional,
    Sequence,
    Union,
)

if TYPE_CHECKING:
    from fastcrawl.models import Response  # pragma: no cover

PrimitiveData = Optional[Union[str, int, float, bool]]

RequestCallback = Union[
    Callable[["Response"], Union[Coroutine[Any, Any, Optional[AsyncIterator[Any]]], AsyncIterator[Any]]],
    Callable[["Response", Any], Union[Coroutine[Any, Any, Optional[AsyncIterator[Any]]], AsyncIterator[Any]]],
]
RequestErrback = Callable[["Response"], Union[Coroutine[Any, Any, Optional[AsyncIterator[Any]]], AsyncIterator[Any]]]

QueryParams = Mapping[str, Union[PrimitiveData, Sequence[PrimitiveData]]]
Headers = Mapping[str, str]
Cookies = Mapping[str, str]
FormData = Mapping[str, Any]
JsonData = Any
Files = Mapping[str, bytes]
Auth = tuple[str, str]
