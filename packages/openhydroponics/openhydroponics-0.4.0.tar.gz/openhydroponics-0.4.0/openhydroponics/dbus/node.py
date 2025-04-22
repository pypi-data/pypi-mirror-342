from typing import Union
from uuid import UUID

from dbus_next.aio import MessageBus, ProxyObject

from openhydroponics.base import NodeBase
from openhydroponics.base import endpoint as EndpointBase
from openhydroponics.dbus.endpoint import get_endpoint_class

BUS_NAME = "com.openhydroponics"


class Node(NodeBase):
    def __init__(self, uuid: UUID, proxy_object: ProxyObject):
        super().__init__(uuid)
        self._proxy_object = proxy_object
        self._interface = proxy_object.get_interface(
            "com.openhydroponics.NodeInterface"
        )

    def get_endpoint(self, endpoint_id: int) -> Union[EndpointBase.Endpoint, None]:
        endpoint = self._endpoints.get(endpoint_id)
        if not endpoint:
            return None
        return endpoint

    async def init(self, bus: MessageBus, introspection):
        for child in introspection.nodes:
            path = f"{introspection.name}/{child.name}"
            await self._add_endpoint_from_path(bus, path)
        # Resort endpoints
        self._endpoints = dict(sorted(self._endpoints.items()))

    async def _add_endpoint_from_path(self, bus: MessageBus, path: str):
        introspection = await bus.introspect(BUS_NAME, path)
        proxy_object = bus.get_proxy_object(BUS_NAME, path, introspection)

        interface = proxy_object.get_interface(
            "com.openhydroponics.EndpointMetaDataInterface"
        )

        endpoint_id = await interface.get_endpoint_id()

        endpoint_interface_name = await interface.get_endpoint_interface()
        endpoint_interface = proxy_object.get_interface(endpoint_interface_name)
        endpoint = get_endpoint_class(
            endpoint_interface_name, endpoint_id, endpoint_interface, self
        )
        await endpoint.init()
        self.add_endpoint(endpoint_id, endpoint)
