from connectus.tools.structure.data import DataRequest
from connectus.data_manager.node.type.base import BaseNode
from .configuration import Configuration
import asyncio

class MQTT(BaseNode, Configuration):
    def __init__(self, node_config: dict[str, str], stop_event: asyncio.Event):
        BaseNode.__init__(self, stop_event)
        Configuration.__init__(self, node_config)
    
    async def connect(self):
        try:
            await self.create_client()
            self.running = True
        except Exception as e:
            raise ConnectionError(f"An error occurred while connecting to the OPC server: {e}")
        
    def add_subscription(self, subscription: list[DataRequest] = []):
        try:
            if subscription:
                topics = []
                for request in subscription:
                    for variable in request.data.collection:
                        self.subscription.append(variable.name)
                        topics.append((variable.name, 0))
            self.client.subscribe(topics)
        except Exception as e:
            print(f"An error occurred while adding the subscription: {e}")
        
    async def disconnect(self):
        try:
            self.client.disconnect()
        except Exception as e:
            print(f"An error occurred while disconnecting from the OPC server: {e}")

    async def read(self, request_list: list[DataRequest] =[]):
        try:
            pass
        except Exception as e:
            print(f"An error occurred while reading the data: {e}")

    async def write(self, request_list: list[DataRequest], node_params: dict[str, any]= None): ## include check if variable exists in the server/device
        try:
            if request_list:
                for request in request_list:
                    for variable in request.data.collection:
                        await self.client.publish(variable.name, variable.value)        
        except Exception as e:
            print(f"An error occurred while writing the data: {e}")

