#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Trae Phone MCP CLI - 命令行界面，用于直接与Android设备交互
"""

import argparse
import sys
from typing import List, Optional, Dict, Any

# 导入主模块
from phone_mcp_by_trae.phone_mcp import ADBExecutor

adb = ADBExecutor()

def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="Phone MCP命令行工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # 检查连接
    check_parser = subparsers.add_parser("check", help="检查设备连接")
    
    # 设置设备
    device_parser = subparsers.add_parser("device", help="设置要使用的设备")
    device_parser.add_argument("device_id", help="设备ID")
    
    # 电话功能
    call_parser = subparsers.add_parser("call", help="拨打电话")
    call_parser.add_argument("phone_number", help="电话号码")
    
    hangup_parser = subparsers.add_parser("hangup", help="结束当前通话")
    
    # 短信功能
    sms_parser = subparsers.add_parser("send-sms", help="发送短信")
    sms_parser.add_argument("phone_number", help="接收者电话号码")
    sms_parser.add_argument("message", help="短信内容")
    
    # 应用管理
    app_parser = subparsers.add_parser("app", help="打开应用")
    app_parser.add_argument("app_name", help="应用名称或包名")
    
    close_app_parser = subparsers.add_parser("close-app", help="关闭应用")
    close_app_parser.add_argument("package_name", help="应用包名")
    
    # 屏幕交互
    tap_parser = subparsers.add_parser("tap", help="点击屏幕")
    tap_parser.add_argument("x", type=int, help="X坐标")
    tap_parser.add_argument("y", type=int, help="Y坐标")
    
    swipe_parser = subparsers.add_parser("swipe", help="滑动屏幕")
    swipe_parser.add_argument("x1", type=int, help="起始X坐标")
    swipe_parser.add_argument("y1", type=int, help="起始Y坐标")
    swipe_parser.add_argument("x2", type=int, help="结束X坐标")
    swipe_parser.add_argument("y2", type=int, help="结束Y坐标")
    swipe_parser.add_argument("--duration", type=int, default=300, help="滑动持续时间(毫秒)")
    
    # 文本输入
    text_parser = subparsers.add_parser("text", help="输入文本")
    text_parser.add_argument("text", help="要输入的文本")
    
    # 按键
    key_parser = subparsers.add_parser("key", help="按下按键")
    key_parser.add_argument("keycode", help="按键代码或名称")
    
    # 截图
    screenshot_parser = subparsers.add_parser("screenshot", help="截取屏幕截图")
    screenshot_parser.add_argument("--path", default="screenshot.png", help="保存路径")
    
    # 打开URL
    url_parser = subparsers.add_parser("url", help="打开URL")
    url_parser.add_argument("url", help="要打开的URL")
    
    return parser.parse_args()

def handle_check_command() -> None:
    """处理检查设备命令"""
    result = adb.execute_command(["devices"])
    print("已连接的设备:")
    
    lines = result.split("\n")
    if len(lines) <= 1:
        print("  没有找到设备")
        return
    
    for line in lines[1:]:  # 跳过第一行（标题行）
        if line.strip():
            parts = line.split("\t")
            if len(parts) >= 2:
                print(f"  {parts[0]} - {parts[1]}")

def handle_device_command(device_id: str) -> None:
    """处理设置设备命令"""
    adb.device_id = device_id
    print(f"已设置设备: {device_id}")

def handle_call_command(phone_number: str) -> None:
    """处理拨打电话命令"""
    result = adb.execute_command([
        "shell", "am", "start", "-a", "android.intent.action.CALL",
        "-d", f"tel:{phone_number}"
    ])
    print(f"拨打电话: {phone_number}")
    if "Error" in result:
        print(f"错误: {result}")

def handle_hangup_command() -> None:
    """处理挂断电话命令"""
    result = adb.execute_command(["shell", "input", "keyevent", "6"])
    print("结束通话")
    if "Error" in result:
        print(f"错误: {result}")

def handle_send_sms_command(phone_number: str, message: str) -> None:
    """处理发送短信命令"""
    result = adb.execute_command([
        "shell", "am", "start", "-a", "android.intent.action.SENDTO",
        "-d", f"smsto:{phone_number}", "--es", "sms_body", message,
        "--ez", "exit_on_sent", "true"
    ])
    print(f"准备发送短信到: {phone_number}")
    print("已打开短信应用并填充内容，请手动点击发送按钮")
    if "Error" in result:
        print(f"错误: {result}")

def handle_app_command(app_name: str) -> None:
    """处理打开应用命令"""
    result = adb.execute_command([
        "shell", "monkey", "-p", app_name, "-c", "android.intent.category.LAUNCHER", "1"
    ])
    print(f"打开应用: {app_name}")
    if "Error" in result:
        print(f"错误: {result}")
        print("提示: 请尝试使用完整的包名")

def handle_close_app_command(package_name: str) -> None:
    """处理关闭应用命令"""
    result = adb.execute_command(["shell", "am", "force-stop", package_name])
    print(f"关闭应用: {package_name}")
    if "Error" in result:
        print(f"错误: {result}")

def handle_tap_command(x: int, y: int) -> None:
    """处理点击屏幕命令"""
    result = adb.execute_command(["shell", "input", "tap", str(x), str(y)])
    print(f"点击坐标: ({x}, {y})")
    if "Error" in result:
        print(f"错误: {result}")

def handle_swipe_command(x1: int, y1: int, x2: int, y2: int, duration: int) -> None:
    """处理滑动屏幕命令"""
    result = adb.execute_command([
        "shell", "input", "swipe",
        str(x1), str(y1), str(x2), str(y2), str(duration)
    ])
    print(f"滑动: ({x1}, {y1}) -> ({x2}, {y2}), 持续: {duration}ms")
    if "Error" in result:
        print(f"错误: {result}")

def handle_text_command(text: str) -> None:
    """处理输入文本命令"""
    # 对特殊字符进行转义
    escaped_text = text.replace(" ", "%s").replace("\"", "\\\"")
    
    result = adb.execute_command(["shell", "input", "text", escaped_text])
    print(f"输入文本: {text}")
    if "Error" in result:
        print(f"错误: {result}")

def handle_key_command(keycode: str) -> None:
    """处理按键命令"""
    # 常见按键代码映射
    keycode_map = {
        "home": "3",
        "back": "4",
        "menu": "82",
        "power": "26",
        "volume_up": "24",
        "volume_down": "25",
        "enter": "66",
        "delete": "67",
        "recent": "187"
    }
    
    # 如果是映射中的按键名，转换为代码
    actual_keycode = keycode_map.get(keycode.lower(), keycode)
    
    result = adb.execute_command(["shell", "input", "keyevent", actual_keycode])
    print(f"按下按键: {keycode} (代码: {actual_keycode})")
    if "Error" in result:
        print(f"错误: {result}")

def handle_screenshot_command(path: str) -> None:
    """处理截图命令"""
    # 在设备上截图
    device_path = "/sdcard/screenshot.png"
    capture_result = adb.execute_command(["shell", "screencap", "-p", device_path])
    
    if "Error" in capture_result:
        print(f"截图失败: {capture_result}")
        return
    
    # 将截图拉取到本地
    pull_result = adb.execute_command(["pull", device_path, path])
    
    # 删除设备上的临时文件
    adb.execute_command(["shell", "rm", device_path])
    
    print(f"截图已保存到: {path}")
    if "Error" in pull_result:
        print(f"错误: {pull_result}")

def handle_url_command(url: str) -> None:
    """处理打开URL命令"""
    result = adb.execute_command([
        "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", url
    ])
    print(f"打开URL: {url}")
    if "Error" in result:
        print(f"错误: {result}")

def main() -> None:
    """命令行工具主入口"""
    args = parse_args()
    
    if not args.command:
        print("错误: 请指定要执行的命令")
        sys.exit(1)
    
    # 根据命令分发到对应的处理函数
    if args.command == "check":
        handle_check_command()
    elif args.command == "device":
        handle_device_command(args.device_id)
    elif args.command == "call":
        handle_call_command(args.phone_number)
    elif args.command == "hangup":
        handle_hangup_command()
    elif args.command == "send-sms":
        handle_send_sms_command(args.phone_number, args.message)
    elif args.command == "app":
        handle_app_command(args.app_name)
    elif args.command == "close-app":
        handle_close_app_command(args.package_name)
    elif args.command == "tap":
        handle_tap_command(args.x, args.y)
    elif args.command == "swipe":
        handle_swipe_command(args.x1, args.y1, args.x2, args.y2, args.duration)
    elif args.command == "text":
        handle_text_command(args.text)
    elif args.command == "key":
        handle_key_command(args.keycode)
    elif args.command == "screenshot":
        handle_screenshot_command(args.path)
    elif args.command == "url":
        handle_url_command(args.url)
    else:
        print(f"错误: 未知命令 '{args.command}'")
        sys.exit(1)

if __name__ == "__main__":
    main()