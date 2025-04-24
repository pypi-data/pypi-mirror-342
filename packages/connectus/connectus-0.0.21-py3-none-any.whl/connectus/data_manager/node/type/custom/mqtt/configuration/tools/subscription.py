from connectus.tools.structure.data import VariableData
from datetime import timezone, datetime

class SubscriptionHandler(object):
    """
    Subscription Handler. To receive events from server for a subscription
    This class is just a sample class. Whatever class having these methods can be used
    """
    def __init__(self, changes_buffer):    
        self.buffer = changes_buffer  # To store updates

    def data_change(self, handle, node, value, attr):
        """
        Deprecated, use datachange_notification
        """
        pass

    def datachange_notification(self, node, value, data):
        """
        called for every datachange notification from server
        """
        item = VariableData(
            source= "opcua",
            name= node.nodeid.Identifier,
            value= value,
            timestamp= data.monitored_item.Value.SourceTimestamp.replace(tzinfo=timezone.utc),
            value_type= type(value).__name__,
        )

        self.buffer.append(item)

    def event_notification(self, event):
        """
        called for every event notification from server
        """
        pass

    def status_change_notification(self, status):
        """
        called for every status change notification from server
        """
        pass

class MQTTSubscriptionHandler():
    """
    Subscription Handler for MQTT. To receive events from server for a subscription
    This class is just a sample class. Whatever class having these methods can be used
    """
    def __init__(self, changes_buffer, subscription: list[str]):
        self.subscription = subscription    
        self.buffer = changes_buffer
    
    def on_connect(self, client, userdata, flags, rc):
        """Callback when the client connects to the broker."""
        pass

    def on_message(self, client, userdata, msg):
        """Callback when a message is received on the subscribed topic."""
        item = VariableData(
            source= "mqtt",
            name= msg.topic,
            value= msg.payload.decode(),
            timestamp= datetime.fromtimestamp(msg.timestamp, timezone.utc),
            value_type= type(msg.payload).__name__,
        )
        self.buffer.append(item)

    def on_subscribe(self, client, userdata, mid, granted_qos):
        """Callback when the client successfully subscribes to a topic."""
        pass
