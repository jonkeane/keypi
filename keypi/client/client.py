import dbus

from . import keymap

import argparse
from time import sleep

HID_DBUS = 'com.jonkeane.keypiservice'
HID_SRVC = '/com/jonkeane/keypiservice'


class Kbrd:
    """
    Emulate a keyboard and send the
    HID messages to the keyboard D-Bus server.
    """
    def __init__(self):
        self.target_length = 6
        self.mod_keys = 0b00000000
        self.pressed_keys = []
        self.dev = None
        self.bus = dbus.SystemBus()
        self.btkobject = self.bus.get_object(HID_DBUS,
                                             HID_SRVC)
        self.btk_service = dbus.Interface(self.btkobject,
                                          HID_DBUS)

    def update_mod_keys(self, mod_key, value):
        """
        Which modifier keys are active is stored in an 8 bit number.
        Each bit represents a different key. This method takes which bit
        and its new value as input
        :param mod_key: The value of the bit to be updated with new value
        :param value: Binary 1 or 0 depending if pressed or released
        """
        bit_mask = 1 << (7-mod_key)
        if value: # set bit
            self.mod_keys |= bit_mask
        else: # clear bit
            self.mod_keys &= ~bit_mask

    def update_keys(self, norm_key, value):
        if value < 1:
            self.pressed_keys.remove(norm_key)
        elif norm_key not in self.pressed_keys:
            self.pressed_keys.insert(0, norm_key)
        len_delta = self.target_length - len(self.pressed_keys)
        if len_delta < 0:
            self.pressed_keys = self.pressed_keys[:len_delta]
        elif len_delta > 0:
            self.pressed_keys.extend([0] * len_delta)

    @property
    def state(self):
        """
        property with the HID message to send for the current keys pressed
        on the keyboards
        :return: bytes of HID message
        """
        return [0xA1, 0x01, self.mod_keys, 0, *self.pressed_keys]

    def send_keys(self):
        self.btk_service.send_keys(self.state)

    def custom_input(self):
        """
        Take custom input, and send it
        """
        val = input("Enter your value: ")
        print('blasting...')
        for char in keymap.string_to_keys(val):
            if isinstance(char, list):
                # this is a chord, so send all of those at once
                for sub_char in char:
                    self.update_keys(keymap.convert(char), 1)
                self.send_keys()
                for sub_char in char:
                    self.update_keys(keymap.convert(char), 0)
                self.send_keys()
            else:
                self.update_keys(keymap.convert(char), 1)
                self.send_keys()
                self.update_keys(keymap.convert(char), 0)
                self.send_keys()

    def space_space(self, sleep_time = 0.5):
        self.update_keys(keymap.convert("KEY_SPACE"), 1)
        self.send_keys()
        self.update_keys(keymap.convert("KEY_SPACE"), 0)
        self.send_keys()

        sleep(sleep_time)

        self.update_keys(keymap.convert("KEY_SPACE"), 1)
        self.send_keys()
        self.update_keys(keymap.convert("KEY_SPACE"), 0)
        self.send_keys()

    def meta_ctrl_q(self):
        self.update_mod_keys(keymap.modkey("KEY_LEFTMETA"), 1)
        self.update_mod_keys(keymap.modkey("KEY_LEFTCTRL"), 1)
        self.update_keys(keymap.convert("KEY_Q"), 1)
        self.send_keys()

        self.update_mod_keys(keymap.modkey("KEY_LEFTMETA"), 0)
        self.update_mod_keys(keymap.modkey("KEY_LEFTCTRL"), 0)
        self.update_keys(keymap.convert("KEY_Q"), 0)
        self.send_keys()
