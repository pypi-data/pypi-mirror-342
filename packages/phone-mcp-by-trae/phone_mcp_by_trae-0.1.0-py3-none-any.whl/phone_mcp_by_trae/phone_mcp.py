#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Trae Phone MCP - 一个通过ADB命令控制Android手机的MCP插件
"""

import json
import subprocess
import sys
from typing import Dict, List, Optional, Any, Union

# 尝试导入MCP库，如果不存在则提供基本实现
try:
    from mcp.server import FastMCP
    HAS_MCP = True
except ImportError:
    HAS_MCP = False
    print("警告: MCP库未安装，使用基本实现")
    
    # 基本MCP服务器实现
    class FastMCP:
        def __init__(self, name):
            self.name = name
            self.tools = {}
            
        def tool(self):
            def decorator(func):
                self.tools[func.__name__] = func
                return func
            return decorator
            
        def run(self, transport='stdio'):
            if transport != 'stdio':
                print(f"警告: 仅支持stdio传输，忽略{transport}")
                
            # 简单的JSON-RPC处理循环
            while True:
                try:
                    line = sys.stdin.readline().strip()
                    if not line:
                        break
                        
                    request = json.loads(line)
                    method = request.get('method')
                    params = request.get('params', {})
                    request_id = request.get('id')
                    
                    if method == 'initialize':
                        response = {
                            'jsonrpc': '2.0',
                            'id': request_id,
                            'result': {
                                'capabilities': {
                                    'tools': [
                                        {
                                            'name': name,
                                            'description': func.__doc__ or '',
                                            'schema': {}
                                        } for name, func in self.tools.items()
                                    ]
                                }
                            }
                        }
                        print(json.dumps(response))
                        sys.stdout.flush()
                    elif method in self.tools:
                        try:
                            result = self.tools[method](**params)
                            response = {
                                'jsonrpc': '2.0',
                                'id': request_id,
                                'result': result
                            }
                        except Exception as e:
                            response = {
                                'jsonrpc': '2.0',
                                'id': request_id,
                                'error': {
                                    'code': -32000,
                                    'message': str(e)
                                }
                            }
                        print(json.dumps(response))
                        sys.stdout.flush()
                    else:
                        response = {
                            'jsonrpc': '2.0',
                            'id': request_id,
                            'error': {
                                'code': -32601,
                                'message': f'方法 {method} 不存在'
                            }
                        }
                        print(json.dumps(response))
                        sys.stdout.flush()
                except Exception as e:
                    response = {
                        'jsonrpc': '2.0',
                        'id': None,
                        'error': {
                            'code': -32700,
                            'message': f'解析错误: {str(e)}'
                        }
                    }
                    print(json.dumps(response))
                    sys.stdout.flush()

# ADB执行器类
class ADBExecutor:
    """ADB命令执行器"""
    
    def __init__(self):
        """初始化ADB执行器"""
        self.device_id = None
        
    def execute_command(self, command: List[str]) -> str:
        """执行ADB命令并返回输出"""
        try:
            if self.device_id:
                # 如果设置了设备ID，添加-s参数
                full_command = ['adb', '-s', self.device_id] + command
            else:
                full_command = ['adb'] + command
                
            result = subprocess.run(
                full_command,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            error_message = f"ADB命令执行失败: {e.stderr.strip()}"
            print(error_message, file=sys.stderr)
            return error_message
        except Exception as e:
            error_message = f"执行ADB命令时出错: {str(e)}"
            print(error_message, file=sys.stderr)
            return error_message

# 创建ADB执行器实例
adb_executor = ADBExecutor()

# 创建MCP应用实例
app = FastMCP("trae_phone_mcp")

@app.tool()
def check_connection() -> Dict[str, Any]:
    """检查ADB连接状态并返回已连接的设备"""
    devices_output = adb_executor.execute_command(['devices'])
    lines = devices_output.split('\n')
    
    # 跳过第一行（标题行）
    device_lines = [line.strip() for line in lines[1:] if line.strip()]
    
    devices = []
    for line in device_lines:
        parts = line.split('\t')
        if len(parts) >= 2:
            devices.append({
                'id': parts[0],
                'status': parts[1]
            })
    
    return {
        'devices': devices,
        'count': len(devices),
        'message': f"找到 {len(devices)} 个设备"
    }

@app.tool()
def set_device(device_id: str) -> Dict[str, Any]:
    """设置要使用的Android设备
    
    Args:
        device_id: 要使用的设备ID
        
    Returns:
        设置结果消息
    """
    adb_executor.device_id = device_id
    return {
        'success': True,
        'message': f"已设置设备: {device_id}"
    }

@app.tool()
def call(phone_number: str) -> Dict[str, Any]:
    """拨打电话
    
    Args:
        phone_number: 要拨打的电话号码
        
    Returns:
        操作结果消息
    """
    result = adb_executor.execute_command([
        'shell', 'am', 'start', '-a', 'android.intent.action.CALL',
        '-d', f"tel:{phone_number}"
    ])
    
    return {
        'success': 'Error' not in result,
        'message': f"拨打电话: {phone_number}",
        'details': result
    }

@app.tool()
def hangup() -> Dict[str, Any]:
    """结束当前通话
    
    Returns:
        操作结果消息
    """
    # 使用按键事件模拟挂断电话（KEYCODE_ENDCALL = 6）
    result = adb_executor.execute_command(['shell', 'input', 'keyevent', '6'])
    
    return {
        'success': 'Error' not in result,
        'message': "结束通话",
        'details': result
    }

@app.tool()
def send_sms(phone_number: str, message: str) -> Dict[str, Any]:
    """发送短信
    
    Args:
        phone_number: 接收者电话号码
        message: 短信内容
        
    Returns:
        操作结果消息
    """
    # 使用am start命令打开短信应用并填充收件人和内容
    result = adb_executor.execute_command([
        'shell', 'am', 'start', '-a', 'android.intent.action.SENDTO',
        '-d', f"smsto:{phone_number}", '--es', 'sms_body', message,
        '--ez', 'exit_on_sent', 'true'
    ])
    
    # 注意：这只会打开短信应用并填充内容，用户仍需手动发送
    # 自动发送需要更高权限或特定应用支持
    
    return {
        'success': 'Error' not in result,
        'message': f"准备发送短信到: {phone_number}",
        'details': result,
        'note': "已打开短信应用并填充内容，请手动点击发送按钮"
    }

@app.tool()
def open_app(app_name: str) -> Dict[str, Any]:
    """打开应用
    
    Args:
        app_name: 应用名称或包名
        
    Returns:
        操作结果消息
    """
    # 尝试作为包名启动
    result = adb_executor.execute_command([
        'shell', 'monkey', '-p', app_name, '-c', 'android.intent.category.LAUNCHER', '1'
    ])
    
    # 如果失败，可能需要先获取包名列表并匹配
    if 'Error' in result:
        return {
            'success': False,
            'message': f"无法打开应用: {app_name}",
            'details': result,
            'suggestion': "请尝试使用完整的包名"
        }
    
    return {
        'success': True,
        'message': f"已打开应用: {app_name}",
        'details': result
    }

@app.tool()
def close_app(package_name: str) -> Dict[str, Any]:
    """关闭应用
    
    Args:
        package_name: 应用包名
        
    Returns:
        操作结果消息
    """
    result = adb_executor.execute_command(['shell', 'am', 'force-stop', package_name])
    
    return {
        'success': 'Error' not in result,
        'message': f"已关闭应用: {package_name}",
        'details': result
    }

@app.tool()
def tap(x: int, y: int) -> Dict[str, Any]:
    """点击屏幕
    
    Args:
        x: X坐标
        y: Y坐标
        
    Returns:
        操作结果消息
    """
    result = adb_executor.execute_command(['shell', 'input', 'tap', str(x), str(y)])
    
    return {
        'success': 'Error' not in result,
        'message': f"点击坐标: ({x}, {y})",
        'details': result
    }

@app.tool()
def swipe(x1: int, y1: int, x2: int, y2: int, duration: int = 300) -> Dict[str, Any]:
    """滑动屏幕
    
    Args:
        x1: 起始X坐标
        y1: 起始Y坐标
        x2: 结束X坐标
        y2: 结束Y坐标
        duration: 滑动持续时间(毫秒)
        
    Returns:
        操作结果消息
    """
    result = adb_executor.execute_command([
        'shell', 'input', 'swipe',
        str(x1), str(y1), str(x2), str(y2), str(duration)
    ])
    
    return {
        'success': 'Error' not in result,
        'message': f"滑动: ({x1}, {y1}) -> ({x2}, {y2}), 持续: {duration}ms",
        'details': result
    }

@app.tool()
def input_text(text: str) -> Dict[str, Any]:
    """输入文本
    
    Args:
        text: 要输入的文本
        
    Returns:
        操作结果消息
    """
    # 对特殊字符进行转义
    escaped_text = text.replace(' ', '%s').replace('"', '\\"')
    
    result = adb_executor.execute_command(['shell', 'input', 'text', escaped_text])
    
    return {
        'success': 'Error' not in result,
        'message': f"输入文本: {text}",
        'details': result
    }

@app.tool()
def press_key(keycode: str) -> Dict[str, Any]:
    """按下按键
    
    Args:
        keycode: 按键代码
        
    Returns:
        操作结果消息
    """
    # 常见按键代码映射
    keycode_map = {
        'home': '3',
        'back': '4',
        'menu': '82',
        'power': '26',
        'volume_up': '24',
        'volume_down': '25',
        'enter': '66',
        'delete': '67',
        'recent': '187'
    }
    
    # 如果是映射中的按键名，转换为代码
    actual_keycode = keycode_map.get(keycode.lower(), keycode)
    
    result = adb_executor.execute_command(['shell', 'input', 'keyevent', actual_keycode])
    
    return {
        'success': 'Error' not in result,
        'message': f"按下按键: {keycode} (代码: {actual_keycode})",
        'details': result
    }

@app.tool()
def take_screenshot(local_path: str = "screenshot.png") -> Dict[str, Any]:
    """截取屏幕截图
    
    Args:
        local_path: 本地保存路径
        
    Returns:
        操作结果消息
    """
    # 在设备上截图
    device_path = "/sdcard/screenshot.png"
    capture_result = adb_executor.execute_command(['shell', 'screencap', '-p', device_path])
    
    if 'Error' in capture_result:
        return {
            'success': False,
            'message': "截图失败",
            'details': capture_result
        }
    
    # 将截图拉取到本地
    pull_result = adb_executor.execute_command(['pull', device_path, local_path])
    
    # 删除设备上的临时文件
    adb_executor.execute_command(['shell', 'rm', device_path])
    
    return {
        'success': 'Error' not in pull_result,
        'message': f"截图已保存到: {local_path}",
        'details': pull_result
    }

@app.tool()
def open_url(url: str) -> Dict[str, Any]:
    """打开URL
    
    Args:
        url: 要打开的URL
        
    Returns:
        操作结果消息
    """
    result = adb_executor.execute_command([
        'shell', 'am', 'start', '-a', 'android.intent.action.VIEW', '-d', url
    ])
    
    return {
        'success': 'Error' not in result,
        'message': f"已打开URL: {url}",
        'details': result
    }

def main():
    """MCP服务器主入口"""
    app.run(transport='stdio')

if __name__ == "__main__":
    main()