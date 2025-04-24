from connectus.tools.structure.data import DataRequest
from abc import ABC, abstractmethod
import asyncio

class BaseNode(ABC):
    def __init__(self, stop_event: asyncio.Event):
        self.stop_event = stop_event
        self.buffer = []
        self.running = False

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    async def start(self, sample_time: int = 1): ## indicate what is start
        try:
            while not self.stop_event.is_set():
                await self.read() 
                await asyncio.sleep(sample_time)
            await self.stop()
        except Exception as e:
            print('An error occurred during running a node: ', e)

    async def stop(self):
        try:
            self.stop_event.set()
            await self.disconnect()
        except Exception as e:
            print('An error occurred stopping a node: ', e)

    @abstractmethod
    async def read(self, request_list: list[DataRequest] =[]):
        pass

    @abstractmethod
    async def write(self):
        pass
    