import Adafruit_DHT
from threading import Thread

DTH_MODEL = 11


class ClimateReport:
    def __init__(self, humidity, temperature):
        self.humidity = humidity
        self.temperature = temperature


class ClimatePoller(Thread):
    def __init__(self, pin):
        Thread.__init__(self)
        self.pin = pin
        self.current_report = None

    def run(self):
        while True:
            self.current_report = Adafruit_DHT.read_retry(DTH_MODEL, self.pin)


class ClimateSensor:
    def __init__(self, pin):
        self.poller = ClimatePoller(pin)
        self.poller.start()

    def next_report(self):
        if self.poller.current_report:
            humidity, temperature = self.poller.current_report
            return ClimateReport(
                temperature=temperature,
                humidity=humidity
            )
        else:
            return ClimateReport(None, None)