__all__ = ("_enter", "_exit", "_verify")

from contextlib import closing
from typing import Any, Callable, List

from jeepney import DBusErrorResponse, MessageGenerator, new_method_call
from jeepney.io.blocking import Proxy, open_dbus_connection

from ..errors import NotSupportedError

#: Type specification for power management cookies
PowerManagementCookie = int


class FreedesktopPowerManagement(MessageGenerator):
    interface = "org.freedesktop.PowerManagement"

    def __init__(
        self,
        object_path: str = "/org/freedesktop/PowerManagement",
        bus_name: str = "org.freedesktop.PowerManagement",
    ):
        super().__init__(object_path, bus_name)

    def inhibit(self, app_name: str, reason: str) -> PowerManagementCookie:
        return new_method_call(self, "Inhibit", "ss", (app_name, reason))

    def uninhibit(self, cookie: PowerManagementCookie) -> None:
        return new_method_call(self, "Uninhibit", "u", (cookie,))


class GNOMESessionManager(MessageGenerator):
    interface = "org.gnome.SessionManager"

    TOPLEVEL_XID = 0
    INHIBIT_SUSPEND = 4

    def __init__(
        self,
        object_path: str = "/org/gnome/SessionManager",
        bus_name: str = "org.gnome.SessionManager",
    ):
        super().__init__(object_path, bus_name)

    def inhibit(self, app_name: str, reason: str) -> PowerManagementCookie:
        return new_method_call(
            self,
            "Inhibit",
            "susu",
            (
                app_name,
                GNOMESessionManager.TOPLEVEL_XID,
                reason,
                GNOMESessionManager.INHIBIT_SUSPEND,
            ),
        )

    def uninhibit(self, cookie: PowerManagementCookie) -> None:
        return new_method_call(self, "Uninhibit", "u", (cookie,))

    def is_inhibited(self) -> bool:
        return new_method_call(
            self, "IsInhibited", "u", (GNOMESessionManager.INHIBIT_SUSPEND,)
        )


_connection = None
_disposers: List[Callable[[Any], None]] = []
_interfaces = []

_interface_candidates = [GNOMESessionManager, FreedesktopPowerManagement]


def _enter(*, display: bool, app_name: str, reason: str) -> None:
    global _connection, _disposers, _interfaces, _interface_candidates

    if _connection is None:
        try:
            _connection = open_dbus_connection()
        except Exception:
            raise NotSupportedError("Cannot establish connection to D-Bus") from None

    success = False
    try:
        for cls in _interface_candidates:
            interface = cls()
            try:
                (cookie,) = Proxy(interface, _connection).inhibit(app_name, reason)
                success = True
                break
            except DBusErrorResponse:
                pass
        else:
            raise NotSupportedError(
                "No supported power management DBus interface is available"
            )
    finally:
        if not success and not _disposers and _connection is not None:
            # connection is not needed any more
            _connection.close()
            _connection = None

    def disposer(bus: Any) -> None:
        Proxy(interface, bus).uninhibit(cookie)

    _disposers.append(disposer)
    _interfaces.append(interface)


def _exit() -> None:
    global _connection, _disposers

    assert _connection

    _interfaces.pop()
    disposer = _disposers.pop()
    disposer(_connection)

    if not _disposers:
        # connection is not needed any more
        _connection.close()
        _connection = None


def _verify() -> bool:
    global _interfaces

    if not _interfaces:
        return False

    interface = _interfaces[-1]
    if hasattr(interface, "is_inhibited"):
        with closing(open_dbus_connection()) as bus:
            try:
                (result,) = Proxy(interface, bus).is_inhibited()
                return result
            except DBusErrorResponse:
                pass

    global _disposers
    return bool(_disposers)
