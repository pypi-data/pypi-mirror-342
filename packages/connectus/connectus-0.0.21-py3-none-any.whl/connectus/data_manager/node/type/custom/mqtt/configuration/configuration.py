from .layers import ConfigClient

class Configuration(ConfigClient): ## optimize this
    def __init__(self, node_config: dict[str, str]):
        self.subscription = []
        ConfigClient.__init__(self, node_config)
        self.type = 'communication'
        self.id = 'mqtt'