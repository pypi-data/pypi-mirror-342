import asyncio

class ControllerCreator:
    def __init__(self, controller_manager, device_manager, node_creator, stop_event: asyncio.Event):
        self.controller_manager = controller_manager
        self.device_manager = device_manager
        self.node_creator = node_creator
        self.stop_event = stop_event

    def create(self, instance):
        try:
            self.controller = instance
            self._set_managers()
            if self.controller.node_params:
                self._set_node(self.controller.node_params)
        except Exception as e:
            print("An error occurred while creating controller: ", e)

    def _set_managers(self):
        self.controller.device_manager = self.device_manager
        self.controller_manager.add(self.controller)
        self.controller.stop_event = self.stop_event

    def _set_node(self, node_params: dict[str, str]):
        try:
            node = self.node_creator.create_node(node_params)
            self.controller.node = node
        except Exception as e:
            print('An error occurred while setting the node: ', e)
    