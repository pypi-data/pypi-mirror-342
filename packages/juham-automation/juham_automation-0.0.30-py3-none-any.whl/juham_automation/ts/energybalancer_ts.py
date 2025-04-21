import json
from typing import Any
from typing_extensions import override

from masterpiece.mqtt import MqttMsg

from juham_core import JuhamTs
from juham_core.timeutils import epoc2utc


class EnergyBalancerTs(JuhamTs):
    """Heating optimizer diagnosis.

    This class listens the "energybalance" MQTT topic and records the
    messages to time series database.
    """

    def __init__(self, name: str = "energybalancer_ts") -> None:
        """Construct record object with the given name."""

        super().__init__(name)
        self.topic_name = self.make_topic_name("energybalance")

    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        super().on_connect(client, userdata, flags, rc)
        self.subscribe(self.topic_name)
        self.debug(f"Subscribed to {self.topic_name}")

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        """Standard mqtt message notification method.

        This method is called upon new arrived message.
        """

        m = json.loads(msg.payload.decode())
        point = (
            self.measurement("energybalance")
            .tag("Unit", m["Unit"])
            .field("Mode", m["Mode"])
            .field("Rc", m["Rc"])
            .field("CurrentBalance", m["CurrentBalance"])
            .field("NeededBalance", m["NeededBalance"])
            .time(epoc2utc(m["Timestamp"]))
        )
        self.write(point)
