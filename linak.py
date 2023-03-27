# -*- coding: utf-8 -*-
"""
Linak class is used for the dialogue between an linak lifting column and a Doosan robot.
Please read the README.md file before use.
"""
import time

__author__ = "Bezamat Jérémy"
__copyright__ = "Copyright (C) 2023 HumaRobotics"
__email__ = "support@humarobotics.com"
__version__ = "0.1.0"
__license__ = """
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


class Linak:
    """
    Interface to use Linak with Doosan
    """

    DEFAULT_VALUE = 251

    def __init__(self, ip="192.168.1.10", port=502):
        """
        Initialize the connection between the Linak pillar and the Doosan robot.

        Params:\n
            - 'ip': ip of the Linak column
            - 'port': port of the Linak column
        """

        self.ip = ip
        self.port = port
        self.current_hearbeat = 0

        # Define the modbus table
        add_modbus_signal(self.ip, self.port, "heartbeat",
                          reg_type=DR_HOLDING_REGISTER, index=8193, value=0, slaveid=255)
        add_modbus_signal(self.ip, self.port, "position",
                          reg_type=DR_HOLDING_REGISTER, index=8194, value=0, slaveid=255)
        add_modbus_signal(self.ip, self.port, "current",
                          reg_type=DR_HOLDING_REGISTER, index=8195, value=0, slaveid=255)
        add_modbus_signal(self.ip, self.port, "speed",
                          reg_type=DR_HOLDING_REGISTER, index=8196, value=0, slaveid=255)
        add_modbus_signal(self.ip, self.port, "soft_start",
                          reg_type=DR_HOLDING_REGISTER, index=8197, value=0, slaveid=255)
        add_modbus_signal(self.ip, self.port, "soft_stop",
                          reg_type=DR_HOLDING_REGISTER, index=8198, value=0, slaveid=255)

        add_modbus_signal(self.ip, self.port, "gposition",
                          reg_type=DR_HOLDING_REGISTER, index=8449, value=0, slaveid=255)
        add_modbus_signal(self.ip, self.port, "gcurrent",
                          reg_type=DR_HOLDING_REGISTER, index=8450, value=0, slaveid=255)

    def close_connexion(self):
        """
        Close the modbus signal/connexion created during the init.
        """

        del_modbus_signal("heartbeat")
        del_modbus_signal("position")
        del_modbus_signal("current")
        del_modbus_signal("speed")
        del_modbus_signal("soft_start")
        del_modbus_signal("soft_stop")

    def heartbeat(self):
        # Run this with a thread
        self.current_hearbeat += 1
        if self.current_hearbeat == 256:
            self.current_hearbeat = 0
        set_modbus_output("heartbeat", self.current_hearbeat)
        time.sleep(0.1)
        return 0

    def stop_motion(self):
        set_modbus_output("position", 64259)  # Stop

    def move_to(self, pos_mm, speed=50):
        pos = round(pos_mm * 10)
        speed = round(speed * 2)
        set_modbus_output("current", Linak.DEFAULT_VALUE)
        set_modbus_output("speed", speed)
        set_modbus_output("soft_start", Linak.DEFAULT_VALUE)
        set_modbus_output("soft_stop", Linak.DEFAULT_VALUE)
        self.stop_motion()
        set_modbus_output("position", pos)
        time.sleep(0.5)
        # Wait until the lifting column stop moving:
        while self.get_current() != 0: #TODO: Use Running out and Running in instead of Current
            time.sleep(0.1)

    def get_position(self):
        current_pos = get_modbus_input("gposition")
        current_pos = current_pos/10
        return current_pos

    def get_current(self):
        current = get_modbus_input("gcurrent")
        return current
