from influxdb_client import InfluxDBClient
from influxdb_client.client.health_api import HealthCheckFailedError
from ..base_checker import BaseChecker

class InfluxDB(BaseChecker):
    def __init__(self, url):
        self.url = url

    def check(self):
        try:
            with InfluxDBClient(url=self.url, token="", org="-") as client:
                health = client.health()
                if health.status == "pass":
                    return True
                else:
                    return (False, health.message)
        except HealthCheckFailedError as e:
            return (False, str(e))
        except Exception:
            return (False, "pihace: log are unavailable")
