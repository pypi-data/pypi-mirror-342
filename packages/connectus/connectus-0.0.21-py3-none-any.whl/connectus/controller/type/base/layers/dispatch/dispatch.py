from connectus.tools.structure.data import DataRequest, DataCollection
from abc import ABC, abstractmethod
import json, asyncio

class BaseDispatch(ABC):
    def __init__(self):
        pass

    def run(self, request_list: list[DataRequest]):
        if request_list:
            self.controller.device_manager.set(request_list)

    def send_bridge_data(self, data_collection: DataCollection):
        if data_collection.collection:
            for variable_data in data_collection.collection:
                data = {variable_data.name: variable_data.value}
                json_data = json.dumps(data)
                asyncio.create_task(self.controller.node.write([json_data], self.controller.node_params))