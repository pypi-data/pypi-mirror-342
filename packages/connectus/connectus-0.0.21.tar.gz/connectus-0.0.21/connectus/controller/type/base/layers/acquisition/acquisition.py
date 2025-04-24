from connectus.tools.structure.data import DataRequest
from abc import ABC, abstractmethod
import copy, time

class BaseAcquisition(ABC):
    def __init__(self):
        self.sample_rate = 1
        self.subs_time = time.time() + self.sample_rate
        self.bridge_subscription = []

    def run(self) -> list[DataRequest]:
        try:
            response_list = self.controller.device_manager.get([DataRequest(action= 'get_data', device_ids= self.controller.device_ids)])
            resquests = []
            for response in response_list:
                if response.data.collection:
                    resquests.append(DataRequest(action= 'update_data', data= response.data))
            if self.controller.node:
                resquests.extend(self.filter_messages(self.controller.node.buffer))
            if self.bridge_subscription and (time.time() - self.subs_time) >= self.sample_rate:
                resquests.extend(self.filter_messages(copy.deepcopy(self.controller.data.collection)))
                self.subs_time = time.time()
            return resquests
        except Exception as e:
            print(f"An error occurred while running controller: {e}")

    def set_bridge_subscription(self, bridge_subscription: list[str] = [], sample_rate: int = 1):
        '''
        This method is used to set the bridge subscription list
        '''
        self.bridge_subscription = bridge_subscription
        self.sample_rate = sample_rate