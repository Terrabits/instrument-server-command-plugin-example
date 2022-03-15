from instrument_server.command import Base


class IsRsDevices(Base):
    def is_match(self, received_command):
        return received_command.strip() == b'is_rs_devices?'

    def execute(self, received_command):
        # self.devices[name] => device
        for device in self.devices.values():
            id_string = device.query(b'*IDN?\n').strip()
            if b'ROHDE' not in id_string.upper():
                # not R&S instrument
                return b'false'
        # all devices R&S
        return b'true'


# export plugin
IS_COMMAND_PLUGIN = True
plugin            = IsRsDevices
