import logging
import bluepy.btle

__all__ = ['MagicLightBLE']

logger = logging.getLogger(__name__)


class MagicLightBLEDelegate(bluepy.btle.DefaultDelegate):
    def __init__(self, notification_callback = None):
        bluepy.btle.DefaultDelegate.__init__(self)
        self._notification_callback = notification_callback

    def handleNotification(self, cHandle, data):
        if self._notification_callback is not None:
            self._notification_callback(cHandle, data)


class MagicLightBLE:
    def __init__(self, mac_address):
        self._adapter_num = 0
        self._mac_address = mac_address
        self._address_type = bluepy.btle.ADDR_TYPE_PUBLIC
        self._write_handle = 0x2e
        self._notification_handle = 0x3f
        self._connection = None
        self._power_on = False
        self._mode = 0x00
        self._speed = 0x00
        self._red = 0x00
        self._green = 0x00
        self._blue = 0x00
        self._white = 0x00

    def notification_callback(self, handle, data):
        if handle == 0x3f:
            #TODO: Validate b'6615234123105f0400000799'

            if data[2] == 0x23:
                self._power_on = True
            elif data[2] == 0x24:
                self._power_on = False

            self._mode = data[3]
            self._speed = data[5]
            self._red = data[6]
            self._green = data[7]
            self._blue = data[8]
            self._white = data[9]

    def connect(self):
        self._connection = bluepy.btle.Peripheral(self._mac_address, self._address_type, self._adapter_num)
        self._connection.setDelegate(MagicLightBLEDelegate(self.notification_callback))

    def disconnect(self):
        if self._connection is not None:
            self._connection.disconnect()

    def is_connected(self):
        return self._connection

    def get_status(self):
        msg = bytes(bytearray([0xEF, 0x01, 0x77]))
        self._connection.writeCharacteristic(self._write_handle, msg)
        self._connection.waitForNotifications(1)

    def turn_on(self):
        msg = bytes(bytearray([0xCC, 0x23, 0x33]))
        self._connection.writeCharacteristic(self._write_handle, msg)

    def turn_off(self):
        msg = bytes(bytearray([0xCC, 0x24, 0x33]))
        self._connection.writeCharacteristic(self._write_handle, msg)

    def set_color(self, red, green, blue):
        msg = bytes(bytearray([0x56, red, green, blue, 0x00, 0xF0, 0xAA]))
        self._connection.writeCharacteristic(self._write_handle, msg)

    def set_white(self, white):
        msg = bytes(bytearray([0x56, 0, 0, 0, white, 0x0F, 0xAA]))
        self._connection.writeCharacteristic(self._write_handle, msg)
