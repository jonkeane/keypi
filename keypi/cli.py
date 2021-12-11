import click
import os
import sys

from .client import client as clnt
from .server import server as srvr

@click.group()
def keypi():
    """keypi: Keyboard emulator for Raspberry Pi"""
    pass

@keypi.group()
def input():
    """keypi client for accepting input"""
    pass

@input.command(name="open")
def input_open():
    """Shortcut to open an iPhone"""
    kb = clnt.Kbrd()
    kb.space_space()

@input.command(name="close")
def input_close():
    """Shortcut to close an iPhone"""
    kb = clnt.Kbrd()
    kb.meta_ctrl_q()

@input.command(name="custom")
def input_custom():
    """Send custom input to the device"""
    kb = clnt.Kbrd()
    kb.custom_input()


@keypi.group()
def server():
    """keypi server for starting the keypi emulator itself"""
    pass

@server.command(name="start")
def input_custom():
    """Start the server"""
    srvr.start()