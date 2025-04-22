import logging
from typing import Any

from dbus_next import Variant, DBusError

from openhydroponics.base import endpoint as EndpointBase
from openhydroponics.service import endpoint as Service

_LOG = logging.getLogger(__name__)


def variant_from_val(value: Any):
    if isinstance(value, bool):
        return Variant("b", value)
    if isinstance(value, int):
        return Variant("i", value)
    if isinstance(value, float):
        return Variant("d", value)
    if isinstance(value, str):
        return Variant("s", value)
    raise ValueError(f"Unsupported type {type(value)}")


class Endpoint:
    async def set_config(self, config):
        try:
            return await self.dbus_interface.call_set_config(
                {key: variant_from_val(value) for key, value in config.items()}
            )
        except DBusError as e:
            raise Exception(e.text)

    async def init(self):
        self.dbus_interface.on_value_changed(self.on_value_changed)


class VariableOutputEndpoint(EndpointBase.VariableOutputEndpoint):
    async def set(self, value: float):
        await self.dbus_interface.call_set(value)


MAPPING = {
    Service.InputEndpointInterface.DBUS_INTERFACE: EndpointBase.InputEndpoint,
    Service.TemperatureEndpointInterface.DBUS_INTERFACE: EndpointBase.TemperatureEndpoint,
    Service.HumidityEndpointInterface.DBUS_INTERFACE: EndpointBase.HumidityEndpoint,
    Service.ECEndpointInterface.DBUS_INTERFACE: EndpointBase.ECEndpoint,
    Service.PHEndpointInterface.DBUS_INTERFACE: EndpointBase.PHEndpoint,
    Service.OutputEndpointInterface.DBUS_INTERFACE: EndpointBase.OutputEndpoint,
    Service.VariableOutputEndpointInterface.DBUS_INTERFACE: VariableOutputEndpoint,
}


def get_endpoint_class(
    endpoint_interface: str, endpoint_id: int, interface, node
) -> EndpointBase.Endpoint:
    cls = MAPPING.get(endpoint_interface, EndpointBase.Endpoint)
    new_cls = type(cls.__name__, (Endpoint, cls), {})
    obj = new_cls(node, endpoint_id)
    obj.dbus_interface = interface
    return obj
