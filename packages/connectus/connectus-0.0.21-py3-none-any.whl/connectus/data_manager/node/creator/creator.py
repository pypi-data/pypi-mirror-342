from ..type.custom import UART, UDP, InfluxDB, OPC, TimeScaleDB, VISA, MQTT
import asyncio

class NodeCreator:
    def __init__(self, data_manager, stop_event: asyncio.Event):
        self.stop_event = stop_event
        self.data_manager = data_manager
        self.id = 0

    def create_node(self, node_config: dict[str, str]): # Check if already exists the node and use the same
        node_config['id'] = self.id
        name = node_config['name']
        node = self._check_if_node_exists(node_config)
        if node:
            print(f"Node {name} already exists, using existing instance.")
            return node
        elif name == 'uart':
            node = UART(node_config, self.stop_event)
        elif name == 'udp':
            node = UDP(node_config, self.stop_event)
        # elif name == 'influxdb':
        #     node = InfluxDB(node_config, self.stop_event)
        elif name == 'opc':
            node = OPC(node_config, self.stop_event)
        elif name == 'timescaledb':
            node = TimeScaleDB(node_config, self.stop_event)
        elif name == 'visa':
            node = VISA(node_config, self.stop_event)
        elif name == 'mqtt':
            node = MQTT(node_config, self.stop_event)
        else:
            raise ValueError(f"Node type {name} not supported")
        self.data_manager.add(node)
        self.id += 1
        return node
    
    def _check_if_node_exists(self, node_config: dict[str, str]) -> classmethod:
        nodes = self.data_manager.get_all_nodes()
        for node in nodes:
            if node.id == node_config['name']:
                if node.id == 'uart' and node_config.get('port') == node.port:
                    return node
                elif node.id == 'udp' and node_config.get('ip') == node.server_ip and node_config.get('port') == node.server_port:
                    return node
                elif node.id == 'opc' and node_config.get('url') == node.url:
                    return node
                elif node.id == 'timescaledb' and node_config.get('url') == node.url:
                    return node
                elif node.id == 'visa' and node_config.get('resource_name') == node.resource_name:
                    return node
                elif node.id == 'mqtt' and node_config.get('ip') == node.ip and node_config.get('port') == node.port:
                    return node
        return None
                



