import logging

from serde import serde
from pypostcard.types import f32, u8

from openhydroponics.net.msg import ActuatorOutput, EndpointClass
from openhydroponics.base import endpoint as EndpointBase

_LOG = logging.getLogger(__name__)


@serde
class ECConfigCalibration:
    value: f32


@serde
class ECConfigGain:
    value: u8


class ECEndpoint(EndpointBase.ECEndpoint):

    async def set_config(self, config):
        if "high" in config and "low" in config:
            raise ValueError(
                "Cannot not set high and low at the same time, calibration will be wrong"
            )
        if "high" in config:
            await self.node.set_config(
                EndpointBase.ECConfigType.HIGH,
                ECConfigCalibration(value=f32(config["high"])),
            )
        if "low" in config:
            await self.node.set_config(
                EndpointBase.ECConfigType.LOW,
                ECConfigCalibration(value=f32(config["low"])),
            )
        if "gain" in config:
            await self.node.set_config(
                EndpointBase.ECConfigType.GAIN, ECConfigGain(value=u8(config["gain"]))
            )


class VariableOutputEndpoint(EndpointBase.VariableOutputEndpoint):
    async def set(self, value: float):
        self.node.send_msg(
            ActuatorOutput(endpoint_id=u8(self.endpoint_id), value=f32(value))
        )


def get_endpoint_input_class(
    endpoint_input_class: EndpointBase.EndpointInputClass,
) -> EndpointBase.InputEndpoint:
    if endpoint_input_class == EndpointBase.EndpointInputClass.Temperature:
        return EndpointBase.TemperatureEndpoint
    if endpoint_input_class == EndpointBase.EndpointInputClass.Humidity:
        return EndpointBase.HumidityEndpoint
    if endpoint_input_class == EndpointBase.EndpointInputClass.EC:
        return ECEndpoint
    if endpoint_input_class == EndpointBase.EndpointInputClass.PH:
        return EndpointBase.PHEndpoint
    return EndpointBase.InputEndpoint


def get_endpoint_output_class(
    endpoint_output_class: EndpointBase.EndpointOutputClass,
) -> EndpointBase.OutputEndpoint:
    if endpoint_output_class == EndpointBase.EndpointOutputClass.Variable:
        return VariableOutputEndpoint
    return EndpointBase.OutputEndpoint


def get_endpoint_class(
    endpoint_class: EndpointBase.EndpointClass, endpoint_sub_class
) -> EndpointBase.Endpoint:
    if endpoint_class == EndpointClass.Input:
        return get_endpoint_input_class(endpoint_sub_class)
    if endpoint_class == EndpointClass.Output:
        return get_endpoint_output_class(endpoint_sub_class)
    return EndpointBase.Endpoint
