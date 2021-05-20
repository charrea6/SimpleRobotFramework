from simplerobot import utils
from simplerobot.mqtt import Component
import asyncio

try:
    from gpiozero.pins.pigpio import PiGPIOFactory
    from gpiozero import DistanceSensor

except:
    class DistanceSensor:
        def __init__(self, echo, trigger, max_distance=1, pin_factory=None):
            self.distance = 0

    class PiGPIOFactory:
        pass


class DistanceSensorController(Component):
    def __init__(self, config: dict):
        super().__init__("distancesensors")
        self.sensors = {}
        for name, sensor in config['sensors'].items():
            self.sensors[name] = DistanceSensor(sensor['echo'], sensor['trigger'], max_distance=sensor['max_distance'],
                                                pin_factory=PiGPIOFactory())

    async def start(self):
        asyncio.create_task(self.measure())
        await super().start()

    async def measure(self):
        while True:
            await asyncio.sleep(1)
            self.update_state()

    @property
    def state(self):
        return {name: {"distance": sensor.distance} for name, sensor in self.sensors.items()}


if __name__ == "__main__":
    controller = DistanceSensorController()
    asyncio.run(controller.start())