import platform
from contextlib import contextmanager
from typing import Iterator, Optional

from .types import Adrenaline

__all__ = ("get_implementation",)


_implementations = {}  # type: Dict[str, Adrenaline]


def get_implementation(name: Optional[str] = None) -> Adrenaline:
    if name is None:
        name = platform.system()

    name = name.lower()
    impl = _implementations.get(name)
    if impl is None:
        _implementations[name] = impl = import_implementation(name)

    return impl


def import_implementation(name: str) -> Adrenaline:
    if name == "darwin":
        from ._impl.darwin import _enter, _exit, _verify
    elif name == "windows":
        from ._impl.windows import _enter, _exit, _verify
    elif name == "linux":
        from ._impl.linux import _enter, _exit, _verify
    elif name == "dummy":
        from ._impl.dummy import _enter, _exit, _verify
    elif name == "failing":
        from ._impl.failing import _enter, _exit, _verify
    else:
        raise NotImplementedError(f"No such implementation: {name!r}")

    class _AdrenalineImpl(Adrenaline):
        @contextmanager
        def prevent_sleep(
            self,
            *,
            display: bool = False,
            app_name: Optional[str] = None,
            reason: Optional[str] = None,
        ) -> Iterator[None]:
            _enter(
                display=display,
                app_name=app_name or "Python",
                reason=reason or "Python adrenaline module",
            )
            try:
                yield
            finally:
                _exit()

        def is_sleep_prevented(self) -> bool:
            return _verify()

    return _AdrenalineImpl()
