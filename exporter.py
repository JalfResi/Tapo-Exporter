"""Application exporter"""

import os
import time
from prometheus_client import start_http_server, Gauge, Enum
from PyP100 import PyP110


class AppMetrics:
    """
    Representation of Prometheus metrics and loop to fetch and transform
    application metrics into Prometheus metrics.
    """

    def __init__(self, ipAddress, email, password, polling_interval_seconds=5):
        self.ipAddress = ipAddress
        self.email = email
        self.password = password
        self.polling_interval_seconds = polling_interval_seconds

        # Prometheus metrics to collect
        self.today_runtime = Gauge("today_runtime", "Today Runtime")
        self.month_runtime = Gauge("month_runtime", "Month Runtime")
        self.today_energy = Gauge("today_energy", "Today Energy")

    def run_metrics_loop(self):
        """Metrics fetching loop"""

        while True:
            self.fetch()
            time.sleep(self.polling_interval_seconds)

    def fetch(self):
        """
        Get metrics from application and refresh Prometheus metrics with
        new values.
        """

        # Fetch raw status data from the application
        p110 = PyP110.P110(self.ipAddress, self.email, self.password)  # Creating a P110 plug object
        p110.handshake()  # Creates the cookies required for further methods
        p110.login()  # Sends credentials to the plug and creates AES Key and IV for further methods

        # PyP110 has all PyP100 functions and additionally allows to query energy usage infos
        status_data = p110.getEnergyUsage()  # Returns dict with all the energy usage

        print(status_data)

        # Update Prometheus metrics with application metrics
        self.today_runtime.set(status_data["result"]["today_runtime"])
        self.month_runtime.set(status_data["result"]["month_runtime"])
        self.today_energy.set(status_data["result"]["today_energy"])


def main():
    """Main entry point"""

    ipAddress = os.getenv("TAPO_EXPORTER_IP_ADDRESS", "")
    email = os.getenv("TAPO_EXPORTER_EMAIL", "")
    password = os.getenv("TAPO_EXPORTER_PASSWORD", "")
    polling_interval_seconds = int(os.getenv("TAPO_EXPORTER_POLLING_INTERVAL_SECONDS", "5"))
    exporter_port = int(os.getenv("TAPO_EXPORTER_PORT", "9877"))

    app_metrics = AppMetrics(
        ipAddress=ipAddress,
        email=email,
        password=password,
        polling_interval_seconds=polling_interval_seconds
    )
    start_http_server(exporter_port)
    app_metrics.run_metrics_loop()


if __name__ == "__main__":
    main()
