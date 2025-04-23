#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Trae Phone MCP - 一个通过ADB命令控制Android手机的MCP插件
"""

from .phone_mcp import ADBExecutor, app, check_connection, set_device, call, hangup, send_sms, open_app, close_app, tap, swipe, input_text, press_key, take_screenshot, open_url, main
from .phone_cli import main as cli_main

__all__ = [
    'ADBExecutor', 'app', 'main', 'cli_main',
    'check_connection', 'set_device', 'call', 'hangup', 'send_sms',
    'open_app', 'close_app', 'tap', 'swipe', 'input_text', 'press_key',
    'take_screenshot', 'open_url'
]