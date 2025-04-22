from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable

__all__ = "MockObject", "MockToken"


class MockObject:
    def __init__(self, text: str) -> None:
        self.__error_text__ = text

    def __getattribute__(self, name: str) -> Any:
        if name == "__error_text__":
            return super().__getattribute__(name)

        raise RuntimeError(self.__error_text__)


def _premade(msg: str) -> Callable[[], MockObject]:
    class PremadeMockObject(MockObject):
        def __init__(self) -> None:
            super().__init__(msg)

    return PremadeMockObject


if TYPE_CHECKING:
    from .native_context import NativeContext
    from .tokens import Token

    class MockToken(Token):
        def __init__(self) -> None: ...

    class MockNativeContext(NativeContext):
        def __init__(self) -> None: ...

else:
    MockToken = _premade("Token was not provided to error")
    MockNativeContext = _premade("native context was not provided")
