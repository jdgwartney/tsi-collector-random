from __future__ import division
import platform
import time
import random
import socket

from bmcpyagent.core.collector import BaseCollector
from bmcpyagent.logging.logger import Logger
# from bmcpyagent.util import util
# from bmcpyagent.util.util import Util
from bmcpyagent.configuration.configuration import Configuration
# from bmcpyagent.error.exception import ConfigurationError


class RandomCollector(BaseCollector):
    def __init__(self, collector_name):
        BaseCollector.__init__(self)
        self._type_name = None
        self._name = None
        logger = Logger()
        global log
        log = logger.get_logger(collector_name)

#        global config
#        config = Configuration()

        self.collector_name = collector_name

        self.entity_type_name = "random"
        self.entity_name = "random"

    def register(self):
        # Fetching OS details - SUPPORTS ONLY LINUX
        os_name = platform.linux_distribution()[0]
        os_family = platform.system()
        os_version = platform.linux_distribution()[1]

        cfg_attr_values = {"sensor_name": "thermo-c40000065bc79728",
                           "os_name": os_name,
                           "os_version": os_version, "type": os_family,
                           "usage": "", "serial": "", "mac_addr": "", "type": "", "aliases": []}

        fqdn = "192.168.1.50"

        self.shell.create_entity("DEVICE", socket.gethostbyname(), self.entity_name, cfg_attr_values=cfg_attr_values)
        self.shell.create_entity(self.entity_type_name, self.entity_name, "Kegbot Monitor",
                                 parent_entity_type_id="DEVICE", parent_entity_id=fqdn)

    def collect(self):
        now = int(time.time())
        timestamp = int(now.strftime("%s"))
        log.debug("Starting Collection at time {1}".format(now))

        value = random.randrange(1,100)
        log.info("timestamp: {0}, value: {1}".format(timestamp, value))

        payload = {current_time: celcius}
        self.check_and_publish_metric("degreesc", payload)

        payload = {current_time: farenheit}
        self.check_and_publish_metric("degreesf", payload)

    def check_and_publish_metric(self, metric_id, payload):
        metrics = config.get_config_section(self.collector_name, Configuration.SECTION_METRICS)
        if any(metric['id'] == metric_id for metric in metrics):
            self.shell.publish_data(self.entity_type_name, self.entity_name, metric_id, payload)
