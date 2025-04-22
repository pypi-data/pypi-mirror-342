from dbus_next.service import ServiceInterface, method, signal
from dbus_next import DBusError, ErrorType

from openhydroponics.base.endpoint import (
    Endpoint,
    EndpointClass,
    EndpointInputClass,
    EndpointOutputClass,
    OutputEndpoint,
)


class EndpointInterface(ServiceInterface):
    DBUS_INTERFACE = "com.openhydroponics.EndpointInterface"

    def __init__(self, endpoint: Endpoint):
        super().__init__(self.DBUS_INTERFACE)
        self._endpoint = endpoint
        self._endpoint.on_value_changed.connect(self.ValueChanged)

    @method()
    async def SetConfig(self, config: "a{sv}"):
        try:
            # Unpack variants
            config = {key: variant.value for key, variant in config.items()}
            return await self._endpoint.set_config(config)
        except Exception as e:
            raise DBusError(ErrorType.SERVICE_ERROR, str(e))

    @signal()
    def ValueChanged(self, value: float, scale: int) -> "dy":
        return [value, scale]


class InputEndpointInterface(EndpointInterface):
    DBUS_INTERFACE = "com.openhydroponics.endpoint.InputInterface"


class TemperatureEndpointInterface(InputEndpointInterface):
    DBUS_INTERFACE = "com.openhydroponics.endpoint.TemperatureInterface"


class HumidityEndpointInterface(InputEndpointInterface):
    DBUS_INTERFACE = "com.openhydroponics.endpoint.HumidityInterface"


class ECEndpointInterface(InputEndpointInterface):
    DBUS_INTERFACE = "com.openhydroponics.endpoint.ECInterface"


class PHEndpointInterface(InputEndpointInterface):
    DBUS_INTERFACE = "com.openhydroponics.endpoint.PHInterface"


class OutputEndpointInterface(EndpointInterface):
    DBUS_INTERFACE = "com.openhydroponics.endpoint.OutputInterface"


class VariableOutputEndpointInterface(OutputEndpointInterface):
    DBUS_INTERFACE = "com.openhydroponics.endpoint.VariableOutputInterface"

    @method()
    async def Set(self, value: "d"):
        await self._endpoint.set(value)


def wrap_input_endpoint(endpoint: Endpoint) -> InputEndpointInterface:
    if endpoint.INPUT_CLASS == EndpointInputClass.Temperature:
        return TemperatureEndpointInterface(endpoint)
    if endpoint.INPUT_CLASS == EndpointInputClass.Humidity:
        return HumidityEndpointInterface(endpoint)
    if endpoint.INPUT_CLASS == EndpointInputClass.EC:
        return ECEndpointInterface(endpoint)
    if endpoint.INPUT_CLASS == EndpointInputClass.PH:
        return PHEndpointInterface(endpoint)
    return InputEndpointInterface(endpoint)


def wrap_output_endpoint(endpoint: OutputEndpoint) -> OutputEndpointInterface:
    if endpoint.OUTPUT_CLASS == EndpointOutputClass.Variable:
        return VariableOutputEndpointInterface(endpoint)
    return OutputEndpointInterface(endpoint)


def wrap_endpoint(endpoint: Endpoint) -> EndpointInterface:
    if endpoint.ENDPOINT_CLASS == EndpointClass.Input:
        return wrap_input_endpoint(endpoint)
    if endpoint.ENDPOINT_CLASS == EndpointClass.Output:
        return wrap_output_endpoint(endpoint)
    return EndpointInterface(endpoint)
