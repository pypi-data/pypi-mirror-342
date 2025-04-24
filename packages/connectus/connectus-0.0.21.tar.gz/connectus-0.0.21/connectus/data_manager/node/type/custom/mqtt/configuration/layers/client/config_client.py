from ...tools.subscription import MQTTSubscriptionHandler
import paho.mqtt.client as mqtt
import asyncio

class ConfigClient:
    def __init__(self, node_config: dict[str, str]):
        self.node_config = node_config
        self.ip = node_config['ip']
        self.port = node_config['port']
        self.handler = MQTTSubscriptionHandler(self.buffer, self.subscription)
        self.client = mqtt.Client(userdata=self.handler)

    async def create_client(self):
        try:
            self.client.on_connect = self.handler.on_connect
            self.client.on_message = self.handler.on_message
            self.client.on_subscribe = self.handler.on_subscribe
            self.client.connect_async(self.ip, self.port)
            self.client.loop_start()
        except Exception as e:
            print(f"An error occurred while creating OPC client: {e}")