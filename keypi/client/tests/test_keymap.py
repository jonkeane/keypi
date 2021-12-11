from .. import keymap

import pytest

def test_converter():
    assert keymap.convert("KEY_P") == 19

def test_modkey():
    assert keymap.modkey("KEY_RIGHTCTRL") == 3

def test_modkey_not_found():
    assert keymap.modkey("KEY_I") == -1

def test_string_to_keys():
    assert keymap.string_to_keys("AB") == ["KEY_A", "KEY_B"]

def test_string_to_keys_lower():
    assert keymap.string_to_keys("cd") == ["KEY_C", "KEY_D"]

def test_string_to_keys_chords():
    assert keymap.string_to_keys("EF{ctrl|g}") == ["KEY_E", "KEY_F", ["KEY_LEFTCTRL", "KEY_G"]]

def test_string_to_keys_single_meta():
    assert keymap.string_to_keys("{enter}") == [["KEY_ENTER"]]

def test_string_to_keys_swaps():
    assert keymap.string_to_keys("H I\tJ{enter}") == ["KEY_H", "KEY_SPACE", "KEY_I", "KEY_TAB", "KEY_J", ["KEY_ENTER"] ]