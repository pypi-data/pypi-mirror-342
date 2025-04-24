from ...base import BaseNode
from .configuration import Configuration
from connectus.tools.structure.data import VariableData, DataRequest
import asyncio
import socket
import datetime

class UDP(BaseNode, Configuration):
    def __init__(self, node_config: dict[str, str], stop_event: asyncio.Event):
        BaseNode.__init__(self, stop_event)
        Configuration.__init__(self, node_config)

    async def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((self.server_ip, self.server_port))
            self.sock.setblocking(False)
            self.sock.settimeout(self.timeout)
            print("UDP Server started with IP:", self.server_ip, "and port:", self.server_port)
            self.running = True
        except Exception as e:
            print("An error occurred while starting UDP:", e)
    
    async def disconnect(self):
        self.sock.close()

    async def write(self, data: list[str], node_params: dict[str, any]):
        try:
            addr = (node_params['ip_client'], node_params['port_client'])
            for msg in data:
                self.sock.sendto(msg.encode(), addr)
        except Exception as e:
            print("An error occurred while sending data with UDP protocol:", e)

    async def read(self, request_list: list[DataRequest] =[]):
        try:
            msg, addr = self.sock.recvfrom(1024)
            data=VariableData(
                source=addr,
                name=msg,
                timestamp=datetime.datetime.now(datetime.timezone.utc))
            self.buffer.append(data)
        except socket.timeout:
            pass
        except TimeoutError:
            pass
        except asyncio.TimeoutError:
            pass
        except ConnectionResetError:
            pass
        except Exception as e:
            print("An error occurred while receiving data with UDP protocol:", e)
