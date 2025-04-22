import asyncio
import logging
import time
from typing import Any
from uuid import UUID
from pypostcard.types import List, u8
from pypostcard.serde import to_postcard

from openhydroponics.base import NodeManagerBase, NodeBase
from openhydroponics.signal import signal


from .phyinterface import CanPhyIface
import openhydroponics.net.msg as Msg
from openhydroponics.net.msg import ArbitrationId
from openhydroponics.net.endpoint import get_endpoint_class

_LOG = logging.getLogger(__name__)


class Node(NodeBase):
    def __init__(
        self, node_id: int, uuid: UUID, manager: NodeManagerBase, phy_iface: CanPhyIface
    ):
        super().__init__(uuid)
        self._manager = manager
        self._node_id = node_id
        self._phy_iface = phy_iface
        self._last_heartbeat = time.time()

    async def interview(self):
        """
        Interview the node to gather information about its endpoints.

        This asynchronous method queries the node for its number of endpoints (if not already known),
        then iterates through each endpoint to gather its information.

        This method is called by the NodeManager when the node is first discovered and should normally not be called
        directly by the user.
        The interview process involves sending requests to the node and waiting for responses.
        """
        if self.number_of_endpoints == -1:
            self.send_rtr(Msg.NodeInfo)
            resp = await self.wait_for(Msg.NodeInfo)
            if not resp:
                return
            self.number_of_endpoints = resp.number_of_endpoints
        for endpoint in range(self.number_of_endpoints):
            endpoint_info = await self.send_and_wait(
                Msg.EndpointInfoRequest(endpoint_id=u8(endpoint))
            )
            if not endpoint_info:
                continue
            EndpointClass = get_endpoint_class(
                endpoint_info.endpoint_class, endpoint_info.endpoint_sub_class
            )
            instance = EndpointClass(self, endpoint)
            await instance.interview()
            self.add_endpoint(endpoint, instance)
        self.on_interview_done()

    @property
    def interviewed(self) -> bool:
        """
        Check if all expected endpoints for this node have been interviewed/discovered.

        :returns: True if all expected endpoints have been discovered (number_of_endpoints equals
            the actual count of endpoints), False otherwise.
        """
        return self.number_of_endpoints == len(self.endpoints)

    @property
    def node_id(self) -> int:
        """
        Returns the node id of this node on the CANbus network.

        The node_id is an integer that uniquely identifies this node in the network.

        :returns: The unique identifier of this node.
        """
        return self._node_id

    @signal()
    def on_interview_done(self):
        """
        Signal emitted when the interview process is completed.
        This method is typically used to perform any necessary actions or
        updates after the interview process has finished successfully.
        """

    async def send_and_wait(self, request: Msg.Msg):
        """
        Send a request message and wait for the corresponding response.

        This method sends a request message to the node and waits for the matching response.
        It automatically determines the expected response type based on the request's message ID.

        :param request: The request message to send. Must be of MsgType.Request.
        :returns: The response message received.
        :raises AssertionError: If the request is not of MsgType.Request or if no corresponding
            response message class exists for the request's message ID.
        :raises asyncio.TimeoutError: If the response is not received within the specified timeout period.
        """
        assert request.MSG_TYPE == Msg.MsgType.Request
        response = Msg.Msg.get_msg_cls(request.MSG_ID, Msg.MsgType.Response)
        assert response
        self.send_msg(request)
        return await self.wait_for(response)

    def send_msg(self, msg: Msg.Msg):
        """
        Send a message to the node.
        This method encodes the message using the appropriate arbitration ID and sends it
        through the physical interface.

        :param msg: The message to send. Must be of type Msg.
        """
        arb = ArbitrationId(
            prio=False,
            dst=self._node_id,
            master=True,  # We are the master
            src=self._manager.node_id,
            multiframe=False,
            msg_type=msg.MSG_TYPE,
            msg_id=msg.MSG_ID,
        )
        data = Msg.Msg.encode(msg)
        self._phy_iface.send_message(arb.encode(), data)

    def send_rtr(self, msg: Any):
        """
        Send a remote transmission request (RTR) to the node.
        """
        arb = ArbitrationId(
            prio=False,
            dst=self._node_id,
            master=True,  # We are the master
            src=self._manager.node_id,
            multiframe=False,
            msg_type=Msg.MsgType.Request,
            msg_id=msg.MSG_ID,
        )
        self._phy_iface.send_message(arb.encode(), b"", is_remote=True)

    async def set_config(self, config_no: int, config: Any):
        """
        Set the configuration for the node.
        This method sends a configuration request to the node with the specified configuration number
        and configuration data.

        :param config_no: The configuration number to set.
        :param config: The configuration data to send.
        """
        cfg = to_postcard(config)
        cfg = cfg + bytes([0] * (32 - len(cfg)))
        msg = Msg.EndpointConfigRequest(
            endpoint_id=u8(self.node_id),
            config_no=u8(config_no),
            config=List(list(cfg)),
        )
        self.send_msg(msg)

    async def wait_for(self, msg: Msg.Msg):
        """
        Wait for a specific message type from the node.
        This method listens for incoming messages and returns the first message that matches the
        specified message type.

        :param msg: The message type to wait for. Must be of type Msg.
        :returns: The received message of the specified type.
        :raises asyncio.TimeoutError: If no matching message is received within the specified timeout period.
        """
        arb = ArbitrationId(
            prio=False,
            dst=self._manager.node_id,
            master=False,
            src=self._node_id,
            multiframe=False,
            msg_type=msg.MSG_TYPE,
            msg_id=msg.MSG_ID,
        )
        try:
            frame = await self._phy_iface.wait_for(arb.encode())
            return Msg.Msg.decode(arb, frame.data)
        except asyncio.TimeoutError:
            _LOG.error("Timeout waiting for frame. Arb: %s", arb)
        return None
