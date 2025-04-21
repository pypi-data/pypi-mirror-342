from typing import ContextManager, Optional

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol


__all__ = ("Adrenaline", "AdrenalineContext")


#: Type specification for a context that suppresses sleep when entered and restores
#: the previous state when exited
AdrenalineContext = ContextManager[None]


class Adrenaline(Protocol):
    def is_sleep_prevented(self) -> bool:
        pass

    def prevent_sleep(
        self,
        *,
        display: bool = False,
        app_name: Optional[str] = None,
        reason: Optional[str] = None,
    ) -> AdrenalineContext:
        pass
