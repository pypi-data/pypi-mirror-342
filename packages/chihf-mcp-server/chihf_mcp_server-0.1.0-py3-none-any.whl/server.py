
import subprocess
import os
import time
from typing import Any, Dict, Optional
import threading
import re
from datetime import datetime
import requests
import uiautomator2 as u2
from mcp.server.fastmcp import FastMCP
from openai import OpenAI


# 初始化FastMCP服务器
mcp = FastMCP("android_automation")

# 不再设置默认临时目录
# TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
# os.makedirs(TEMP_DIR, exist_ok=True)

def run_adb_command(command):
    """执行ADB命令并返回结果"""
    try:
        full_command = f"adb {command}"
        
        result = subprocess.run(
            full_command, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            return {
                "success": True,
                "output": result.stdout.strip(),
                "command": full_command
            }
        else:
            return {
                "success": False,
                "error": result.stderr.strip(),
                "command": full_command
            }
                
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "command": f"adb {command}"
        }

def get_connected_devices():
    """获取已连接的设备列表"""
    result = run_adb_command("devices")
    if not result["success"]:
        return []
    
    devices = []
    lines = result["output"].split('\n')
    
    # 跳过第一行（标题行）
    for line in lines[1:]:
        if line.strip():
            parts = line.split('\t')
            if len(parts) >= 2:
                devices.append({
                    "id": parts[0].strip(),
                    "status": parts[1].strip()
                })
    
    return devices

@mcp.tool()
def execute_adb_command(command: str) -> Dict[str, Any]:
    """执行ADB命令
    
    Args:
        command: 要执行的ADB命令（不包括'adb'前缀）
    """
    return run_adb_command(command)

@mcp.tool()
def get_devices() -> Dict[str, Any]:
    """获取已连接的Android设备列表"""
    devices = get_connected_devices()
    return {
        "success": True,
        "devices": devices,
        "count": len(devices)
    }

@mcp.tool()
def capture_screenshot(output_path: str, device_id: Optional[str] = None) -> Dict[str, Any]:
    """截取Android设备屏幕
    
    Args:
        output_path: 保存截图的目录路径(必填)
        device_id: 设备ID，如果为空则使用默认设备
    """
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 构建ADB命令
        device_param = f"-s {device_id} " if device_id else ""
        
        # 使用exec-out直接将截图保存到本地
        cmd = f"exec-out screencap -p > \"{output_path}\""
        result = run_adb_command(f"{device_param}{cmd}")
        
        if not result["success"]:
            return {
                "success": False,
                "message": f"截图失败: {result.get('error', '未知错误')}"
            }
        
        # 检查文件是否存在且大小大于0
        if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
            return {
                "success": False,
                "message": "截图保存失败，文件不存在或为空"
            }
        
        # 不返回base64编码的图像数据，只返回文件路径
        # 这样可以避免输入数据过大的问题
        return {
            "success": True,
            "message": f"截图已保存到: {output_path}",
            "image_path": output_path
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"截图过程出错: {str(e)}"
        }

@mcp.tool()
def get_installed_packages(device_id: Optional[str] = None) -> Dict[str, Any]:
    """获取已安装的应用包列表
    
    Args:
        device_id: 设备ID，如果为空则使用默认设备
    """
    device_param = f"-s {device_id} " if device_id else ""
    result = run_adb_command(f"{device_param}shell pm list packages")
    
    if not result["success"]:
        return {
            "success": False,
            "message": f"获取包列表失败: {result.get('error', '未知错误')}"
        }
    
    packages = []
    for line in result["output"].split('\n'):
        if line.startswith('package:'):
            package_name = line[8:].strip()
            packages.append(package_name)
    
    return {
        "success": True,
        "packages": packages,
        "count": len(packages)
    }

@mcp.tool()
def get_package_info(package_name: str, device_id: Optional[str] = None) -> Dict[str, Any]:
    """获取应用包的详细信息
    
    Args:
        package_name: 应用包名
        device_id: 设备ID，如果为空则使用默认设备
    """
    device_param = f"-s {device_id} " if device_id else ""
    result = run_adb_command(f"{device_param}shell dumpsys package {package_name}")
    
    if not result["success"]:
        return {
            "success": False,
            "message": f"获取包信息失败: {result.get('error', '未知错误')}"
        }
    
    # 解析版本信息
    version_code = None
    version_name = None
    first_install_time = None
    last_update_time = None
    
    for line in result["output"].split('\n'):
        line = line.strip()
        if "versionCode=" in line:
            try:
                version_code = line.split("versionCode=")[1].split(" ")[0]
            except:
                pass
        elif "versionName=" in line:
            try:
                version_name = line.split("versionName=")[1].split(" ")[0]
            except:
                pass
        elif "firstInstallTime=" in line:
            try:
                first_install_time = line.split("firstInstallTime=")[1].strip()
            except:
                pass
        elif "lastUpdateTime=" in line:
            try:
                last_update_time = line.split("lastUpdateTime=")[1].strip()
            except:
                pass
    
    # 不返回完整的raw_info，避免数据过大
    return {
        "success": True,
        "package_name": package_name,
        "version_code": version_code,
        "version_name": version_name,
        "first_install_time": first_install_time,
        "last_update_time": last_update_time
    }

@mcp.tool()
def start_app(package_name: str, device_id: Optional[str] = None) -> Dict[str, Any]:
    """启动应用
    
    Args:
        package_name: 应用包名
        device_id: 设备ID，如果为空则使用默认设备
    """
    device_param = f"-s {device_id} " if device_id else ""
    
    # 获取应用的主Activity
    result1 = run_adb_command(f"{device_param}shell cmd package resolve-activity --brief {package_name}")
    
    if not result1["success"]:
        # 尝试直接启动应用
        result2 = run_adb_command(f"{device_param}shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1")
        
        if not result2["success"]:
            return {
                "success": False,
                "message": f"启动应用失败: {result2.get('error', '未知错误')}"
            }
        
        return {
            "success": True,
            "message": f"已启动应用 {package_name}",
            "method": "monkey"
        }
    
    # 解析主Activity
    main_activity = None
    for line in result1["output"].split('\n'):
        if "/" in line:
            main_activity = line.strip()
            break
    
    if not main_activity:
        return {
            "success": False,
            "message": f"无法确定应用 {package_name} 的主Activity"
        }
    
    # 启动应用
    result3 = run_adb_command(f"{device_param}shell am start -n {main_activity}")
    
    if not result3["success"]:
        return {
            "success": False,
            "message": f"启动应用失败: {result3.get('error', '未知错误')}"
        }
    
    return {
        "success": True,
        "message": f"已启动应用 {package_name}",
        "activity": main_activity,
        "method": "am start"
    }

@mcp.tool()
def stop_app(package_name: str, device_id: Optional[str] = None) -> Dict[str, Any]:
    """停止应用
    
    Args:
        package_name: 应用包名
        device_id: 设备ID，如果为空则使用默认设备
    """
    device_param = f"-s {device_id} " if device_id else ""
    result = run_adb_command(f"{device_param}shell am force-stop {package_name}")
    
    if not result["success"]:
        return {
            "success": False,
            "message": f"停止应用失败: {result.get('error', '未知错误')}"
        }
    
    return {
        "success": True,
        "message": f"已停止应用 {package_name}"
    }

@mcp.tool()
def get_current_activity(device_id: Optional[str] = None) -> Dict[str, Any]:
    """获取当前活动的Activity
    
    Args:
        device_id: 设备ID，如果为空则使用默认设备
    """
    device_param = f"-s {device_id} " if device_id else ""
    result = run_adb_command(f"{device_param}shell dumpsys window | findstr mCurrentFocus")
    
    if not result["success"]:
        return {
            "success": False,
            "message": f"获取当前Activity失败: {result.get('error', '未知错误')}"
        }
    
    current_focus = None
    focused_app = None
    
    for line in result["output"].split('\n'):
        if "mCurrentFocus" in line:
            current_focus = line.strip()
        elif "mFocusedApp" in line:
            focused_app = line.strip()
    
    return {
        "success": True,
        "current_focus": current_focus,
        "focused_app": focused_app,
        "raw_output": result["output"]
    }

@mcp.tool()
def tap_screen(x: int, y: int, device_id: Optional[str] = None) -> Dict[str, Any]:
    """点击屏幕指定坐标
    
    Args:
        x: X坐标
        y: Y坐标
        device_id: 设备ID，如果为空则使用默认设备
    """
    device_param = f"-s {device_id} " if device_id else ""
    result = run_adb_command(f"{device_param}shell input tap {x} {y}")
    
    if not result["success"]:
        return {
            "success": False,
            "message": f"点击屏幕失败: {result.get('error', '未知错误')}"
        }
    
    return {
        "success": True,
        "message": f"已点击屏幕坐标 ({x}, {y})"
    }

@mcp.tool()
def input_text(text: str, device_id: Optional[str] = None) -> Dict[str, Any]:
    """输入文本
    
    Args:
        text: 要输入的文本
        device_id: 设备ID，如果为空则使用默认设备
    """
    device_param = f"-s {device_id} " if device_id else ""
    # 转义特殊字符
    escaped_text = text.replace(" ", "%s").replace("'", "\\'").replace("\"", "\\\"")
    result = run_adb_command(f"{device_param}shell input text '{escaped_text}'")
    
    if not result["success"]:
        return {
            "success": False,
            "message": f"输入文本失败: {result.get('error', '未知错误')}"
        }
    
    return {
        "success": True,
        "message": f"已输入文本: {text}"
    }

@mcp.tool()
def press_key(keycode: int, device_id: Optional[str] = None) -> Dict[str, Any]:
    """按下按键
    
    Args:
        keycode: 按键代码，例如4表示返回键
        device_id: 设备ID，如果为空则使用默认设备
    """
    device_param = f"-s {device_id} " if device_id else ""
    result = run_adb_command(f"{device_param}shell input keyevent {keycode}")
    
    if not result["success"]:
        return {
            "success": False,
            "message": f"按键操作失败: {result.get('error', '未知错误')}"
        }
    
    return {
        "success": True,
        "message": f"已按下按键: {keycode}"
    }


# 添加reprint函数
def reprint(message):
    """打印消息的辅助函数"""
    print(message)

# 添加sendfs函数
def sendfs(email, title='消息标题', content='消息内容'):
    """
    发送飞书消息
    :param email: 接收者邮箱
    :param title: 消息标题
    :param content: 消息内容
    :return:
    """
    try:
        senddata = {'email': email,
                    'title': title,
                    'content': content}
        req = requests.request(method='POST', url=f'http://10.10.96.223:5009/v1/config/sendfs_new',
                               data=senddata)
        result = req.json()
        fsresult = result['data']
        if fsresult['code'] == 0:
            reprint(f'email:{email}, 飞书消息发送成功')
        elif fsresult['code'] == 230001:
            reprint(f'email:{email}, 邮箱错误或者指定账户已停用')
        else:
            reprint(f'email:{email}, 飞书消息发送失败')
    except Exception as e:
        reprint(str(e) + ",飞书消息发送失败")

# 添加CrashMonitor类
class CrashMonitor:
    def __init__(self, device_id=None, notify_email=None, log_dir=None):
        # 设备状态
        self.device_id = device_id
        
        # 飞书通知配置 - 必须提供
        if notify_email:
            self.notify_email = notify_email
        else:
            raise ValueError("必须提供notify_email参数(接收崩溃通知的邮箱地址)")
        
        # 监控状态
        self.is_monitoring = False
        self.monitor_thread = None
        
        # 统计信息
        self.crash_count = 0
        self.start_time = None
        self.crash_times = []  # 添加一个列表来存储每次crash的时间
        
        # 日志存储目录 - 必须提供
        if log_dir:
            self.log_dir = log_dir
        else:
            raise ValueError("必须提供log_dir参数(日志存储目录)")
        os.makedirs(self.log_dir, exist_ok=True)
        
        # DeepSeek API配置 - 从MCP环境变量获取
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            print("警告: 未设置DEEPSEEK_API_KEY环境变量，将无法使用AI分析功能")
            self.api_key = ""
        
        self.base_url = os.getenv("DEEPSEEK_API_URL")
        if not self.base_url:
            print("警告: 未设置DEEPSEEK_API_URL环境变量，将使用默认URL")
            self.base_url = "https://oneapi.pateo.com.cn/v1/"
        
        # 尝试导入OpenAI
        try:
            
            if self.api_key and self.base_url:
                self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
                self.openai_available = True
            else:
                self.client = None
                self.openai_available = False
        except ImportError:
            print("警告: OpenAI模块未安装，将无法使用DeepSeek进行分析")
            self.openai_available = False

    def start_monitoring(self):
        """启动监控线程"""
        if self.is_monitoring:
            return {
                "success": True,
                "message": f"设备 {self.device_id} 已在监控中"
            }
        
        # 记录开始监控的时间
        self.start_time = datetime.now()
        
        # 创建并启动监控线程
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self.monitor_crashes, daemon=True)
        self.monitor_thread.start()
        
        return {
            "success": True,
            "message": f"已开始监控设备 {self.device_id} 的崩溃日志"
        }
    
    def stop_monitoring(self):
        """停止监控线程"""
        if not self.is_monitoring:
            return {
                "success": True,
                "message": f"设备 {self.device_id} 未在监控中"
            }
        
        # 停止监控线程
        self.is_monitoring = False
        if self.monitor_thread:
            # 不直接join线程，因为可能会阻塞
            self.monitor_thread = None
        
        return {
            "success": True,
            "message": f"已停止监控设备 {self.device_id} 的崩溃日志"
        }
    
    def monitor_crashes(self):
        """监控设备crash日志的主函数"""
        if not self.device_id:
            print("错误: 未指定设备ID")
            self.is_monitoring = False
            return
        
        print(f"开始监控设备 {self.device_id} 的崩溃日志...")
        
        # 清除现有日志
        try:
            device_param = f"-s {self.device_id} " if self.device_id else ""
            result = run_adb_command(f"{device_param}logcat -c")
            if not result["success"]:
                print(f"警告: 清除日志失败 - {result.get('error', '未知错误')}")
        except Exception as e:
            print(f"警告: 清除日志时出错 - {str(e)}")
        
        # 持续监控日志
        cmd = f"logcat"
        full_cmd = f"adb {'-s ' + self.device_id + ' ' if self.device_id else ''}logcat"
        
        try:
            process = subprocess.Popen(
                full_cmd, 
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            
            # 读取日志
            crash_buffer = []
            collecting_crash = False
            
            while self.is_monitoring:
                line = process.stdout.readline()
                if not line:
                    break
                
                # 检测崩溃日志开始
                if "FATAL EXCEPTION" in line or "ANR in" in line:
                    collecting_crash = True
                    crash_buffer = [line]
                    crash_time = datetime.now()
                elif collecting_crash:
                    crash_buffer.append(line)
                    
                    # 如果收集了足够的崩溃信息或检测到日志结束标记
                    if len(crash_buffer) > 100 or "AndroidRuntime: " in line:
                        collecting_crash = False
                        crash_log = "".join(crash_buffer)
                        
                        # 记录崩溃时间
                        self.crash_times.append(crash_time)
                        
                        # 保存崩溃日志到文件
                        timestamp = crash_time.strftime("%Y%m%d_%H%M%S")
                        log_file = os.path.join(
                            self.log_dir, 
                            f"crash_{self.device_id}_{timestamp}.log"
                        )
                        
                        with open(log_file, "w", encoding="utf-8") as f:
                            f.write(crash_log)
                        
                        # 分析崩溃日志
                        crash_analysis = self.analyze_crash_log(crash_log)
                        
                        # 发送飞书通知
                        self.send_crash_notification(crash_log, crash_analysis, log_file)
                        
                        # 更新统计
                        self.crash_count += 1
                        
                        print(f"检测到崩溃 #{self.crash_count}，已保存到 {log_file}")
            
            # 确保进程被终止
            process.terminate()
            
        except Exception as e:
            import traceback
            print(f"监控崩溃日志时出错: {str(e)}")
            print(traceback.format_exc())
            
            # 确保监控状态被重置
            self.is_monitoring = False
    
    def analyze_crash_log(self, crash_log):
        """分析崩溃日志，提取关键信息"""
        try:
            # 提取关键信息
            analysis = {}
            
            # 提取异常类型
            exception_match = re.search(r"FATAL EXCEPTION: (.*?)\n", crash_log)
            if exception_match:
                analysis["exception_thread"] = exception_match.group(1)
            
            # 提取异常类型和信息
            error_match = re.search(r"(?:Exception|Error): (.*?)(?:\n|:)", crash_log)
            if error_match:
                analysis["error_type"] = error_match.group(1)
            
            # 提取崩溃的应用包名
            package_match = re.search(r"pid: \d+, tid: \d+, name: (.*?)\n", crash_log)
            if package_match:
                analysis["package_name"] = package_match.group(1)
            else:
                package_match = re.search(r"Process: (.*?),", crash_log)
                if package_match:
                    analysis["package_name"] = package_match.group(1)
            
            # 通过DeepSeek API进行高级分析
            if self.openai_available:
                try:
                    analysis["ai_analysis"] = self.get_ai_crash_analysis(crash_log)
                except Exception as e:
                    print(f"AI分析失败: {str(e)}")
                    analysis["ai_analysis"] = "AI分析失败"
            
            return analysis
            
        except Exception as e:
            print(f"分析崩溃日志时出错: {str(e)}")
            return {"error": str(e)}
    
    def get_ai_crash_analysis(self, crash_log):
        """使用OpenAI/DeepSeek分析崩溃日志"""
        if not self.openai_available or not self.client:
            return "OpenAI客户端不可用"
        
        try:
            # 准备提示信息
            prompt = f"""
            请分析以下Android崩溃日志，并提供:
            1. 问题的简要摘要
            2. 崩溃的根本原因
            3. 可能的解决方案
            
            日志内容:
            {crash_log[:3000]}  # 限制日志长度避免超出token限制
            """
            
            # 调用DeepSeek API
            response = self.client.chat.completions.create(
                model="DeepSeek-V3-250324_0326",
                messages=[
                    {"role": "system", "content": "你是一位专业的Android开发和调试专家，擅长分析崩溃日志。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=800
            )
            
            analysis = response.choices[0].message.content
            return analysis
            
        except Exception as e:
            print(f"调用DeepSeek API失败: {str(e)}")
            return f"AI分析失败: {str(e)}"
    
    def send_crash_notification(self, crash_log, analysis, log_file):
        """发送崩溃通知"""
        try:
            # 提取关键信息
            package_name = analysis.get("package_name", "未知应用")
            error_type = analysis.get("error_type", "未知错误")
            
            # 构建通知标题和内容
            title = f"设备 {self.device_id} 检测到应用崩溃: {package_name}"
            
            content = f"设备 {self.device_id} 检测到应用崩溃\n\n"
            content += f"应用: {package_name}\n"
            content += f"错误类型: {error_type}\n"
            content += f"崩溃时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            # 添加AI分析结果
            if "ai_analysis" in analysis:
                content += f"AI分析:\n{analysis['ai_analysis']}\n\n"
            
            # 添加崩溃日志摘要（限制长度）
            content += "崩溃日志摘要:\n"
            content += crash_log[:500] + "...\n\n"
            
            content += f"完整日志已保存到: {log_file}"
            
            # 发送飞书通知
            sendfs(self.notify_email, title, content)
            
        except Exception as e:
            print(f"发送崩溃通知时出错: {str(e)}")
    
    def get_status(self):
        """获取监控状态信息"""
        duration = 0
        if self.start_time:
            duration = (datetime.now() - self.start_time).total_seconds() / 60
            
        return {
            "success": True,
            "device_id": self.device_id,
            "is_monitoring": self.is_monitoring,
            "start_time": self.start_time.strftime('%Y-%m-%d %H:%M:%S') if self.start_time else None,
            "duration_minutes": round(duration, 1),
            "crash_count": self.crash_count,
            "notify_email": self.notify_email,
            "crash_times": [t.strftime('%Y-%m-%d %H:%M:%S') for t in self.crash_times] if self.crash_times else []
        }

# 全局crash监控器实例字典
crash_monitors = {}

@mcp.tool()
def monitor_device_crashes(log_dir: str, notify_email: str, device_id: Optional[str] = None) -> Dict[str, Any]:
    """在后台监控设备的crash日志，并在检测到crash时进行分析和通知
    
    Args:
        log_dir: 保存崩溃日志的目录路径(必填)
        notify_email: 接收飞书通知的邮箱地址(必填)
        device_id: 要监控的设备ID，如果为空则自动获取当前连接的设备
    """
    global crash_monitors
    
    # 验证必填参数
    if not notify_email:
        return {
            "success": False,
            "message": "请指定notify_email参数(接收崩溃通知的邮箱地址)"
        }
    
    # 如果未提供设备ID，获取当前连接的所有设备
    if not device_id:
        devices = get_connected_devices()
        if not devices:
            return {
                "success": False,
                "message": "未检测到已连接的设备"
            }
        
        # 如果只有一个设备，直接使用它
        if len(devices) == 1:
            device_id = devices[0]["id"]
            print(f"自动选择唯一连接的设备: {device_id}")
        else:
            # 如果有多个设备，启动所有设备的监控
            results = []
            for device in devices:
                dev_id = device["id"]
                result = monitor_device_crashes(log_dir, notify_email, dev_id)
                results.append(result)
            
            return {
                "success": True,
                "message": f"已启动对 {len(devices)} 台设备的监控，如有crash将通过飞书发送到 {notify_email}",
                "devices": [device["id"] for device in devices],
                "results": results
            }
    
    # 检查设备是否存在
    result = run_adb_command(f"-s {device_id} get-state")
    if not result["success"]:
        return {
            "success": False,
            "message": f"设备 {device_id} 不存在或无法访问"
        }
    
    # 如果已经有该设备的监控器，返回状态
    if device_id in crash_monitors and crash_monitors[device_id].is_monitoring:
        return {
            "success": True,
            "message": f"设备 {device_id} 已在监控中，如有crash将通过飞书发送到 {notify_email}",
            "status": crash_monitors[device_id].get_status()
        }
    
    # 创建新的监控器
    try:
        monitor = CrashMonitor(device_id=device_id, notify_email=notify_email, log_dir=log_dir)
        crash_monitors[device_id] = monitor
    except ValueError as e:
        return {
            "success": False,
            "message": str(e)
        }
    
    # 启动监控
    result = monitor.start_monitoring()
    
    # 修改返回消息，添加飞书通知提示
    return {
        "success": result["success"],
        "message": f"{result['message']}，如有crash将通过飞书发送到 {notify_email}",
        "device_id": device_id,
        "notify_email": notify_email,
        "log_dir": log_dir
    }

@mcp.tool()
def stop_crash_monitoring(device_id: str) -> Dict[str, Any]:
    """停止对指定设备的crash监控
    
    Args:
        device_id: 要停止监控的设备ID
    """
    global crash_monitors
    
    if device_id not in crash_monitors:
        return {
            "success": False,
            "message": f"设备 {device_id} 未在监控中"
        }
    
    monitor = crash_monitors[device_id]
    start_time = monitor.start_time
    end_time = datetime.now()
    crash_count = monitor.crash_count
    crash_times = monitor.crash_times
    
    # 无论监控状态如何，都尝试停止并从字典中移除
    monitor.stop_monitoring()
    
    # 计算监控持续时间
    duration = (end_time - start_time).total_seconds() / 60 if start_time else 0
    
    # 从字典中移除
    del crash_monitors[device_id]
    
    # 构建详细的消息，包括开始时间、结束时间、持续时间和崩溃次数
    message = f"已停止监控设备 {device_id}\n"
    message += f"监控开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S') if start_time else '未知'}\n"
    message += f"监控结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    message += f"监控持续时间: {round(duration, 1)} 分钟\n"
    message += f"检测到 {crash_count} 次crash"
    
    # 添加每次崩溃的时间
    if crash_times:
        message += "\n\n崩溃发生时间:"
        for i, crash_time in enumerate(crash_times, 1):
            message += f"\n{i}. {crash_time.strftime('%Y-%m-%d %H:%M:%S')}"
    
    return {
        "success": True,
        "message": message,
        "start_time": start_time.strftime('%Y-%m-%d %H:%M:%S') if start_time else None,
        "end_time": end_time.strftime('%Y-%m-%d %H:%M:%S'),
        "duration_minutes": round(duration, 1),
        "crash_count": crash_count,
        "crash_times": [t.strftime('%Y-%m-%d %H:%M:%S') for t in crash_times] if crash_times else []
    }

@mcp.tool()
def get_crash_monitoring_status(device_id: Optional[str] = None) -> Dict[str, Any]:
    """获取crash监控状态
    
    Args:
        device_id: 设备ID，如果为空则返回所有监控设备的状态
    """
    global crash_monitors
    
    if device_id:
        # 返回指定设备的状态
        if device_id not in crash_monitors:
            return {
                "success": False,
                "message": f"设备 {device_id} 未在监控中"
            }
        
        return crash_monitors[device_id].get_status()
    else:
        # 返回所有设备的状态
        all_statuses = {}
        for dev_id, monitor in crash_monitors.items():
            all_statuses[dev_id] = monitor.get_status()
        
        return {
            "success": True,
            "device_count": len(crash_monitors),
            "devices": list(crash_monitors.keys()),
            "statuses": all_statuses
        }

@mcp.tool()
def get_ui_hierarchy_and_find_element(output_dir: str, text_to_find: str, device_id: Optional[str] = None) -> Dict[str, Any]:
    """获取车机UI层次结构并通过文本定位控件中心坐标
    
    Args:
        output_dir: 保存UI层次结构文件的目录路径(必填)
        text_to_find: 要查找的控件文字内容
        device_id: 设备ID，如果为空则使用默认设备
    """
    try:
        # 确保目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 初始化设备连接
        if device_id:
            d = u2.connect(device_id)
        else:
            devices = get_connected_devices()
            if not devices:
                return {
                    "success": False,
                    "message": "未检测到已连接的设备"
                }
            device_id = devices[0]["id"]
            d = u2.connect(device_id)
        
        # 获取当前UI层次结构
        print("正在获取UI层次结构...")
        xml_content = d.dump_hierarchy()
        
        # 保存层次结构到XML文件
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        xml_path = os.path.join(output_dir, f"ui_hierarchy_{timestamp}.xml")
        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(xml_content)
            
        print(f"UI层次结构已保存到: {xml_path}")
        
        # 尝试通过文本查找元素
        print(f"正在查找包含文本 '{text_to_find}' 的元素...")
        elements = d(text=text_to_find)
        
        # 如果没找到，尝试使用包含文本的方式
        if not elements.exists:
            elements = d(textContains=text_to_find)
            
        if not elements.exists:
            return {
                "success": False,
                "message": f"未找到包含文本 '{text_to_find}' 的元素",
                "hierarchy_file": xml_path
            }
        
        # 获取所有匹配元素的信息
        found_elements = []
        count = elements.count
        
        if count == 1:
            # 单个元素
            element_info = elements.info
            bounds = element_info.get("bounds", {})
            center_x = (bounds["left"] + bounds["right"]) // 2
            center_y = (bounds["top"] + bounds["bottom"]) // 2
            
            found_elements.append({
                "index": 0,
                "text": element_info.get("text", ""),
                "resource_id": element_info.get("resourceId", ""),
                "class_name": element_info.get("className", ""),
                "package": element_info.get("packageName", ""),
                "bounds": bounds,
                "center_x": center_x,
                "center_y": center_y,
                "clickable": element_info.get("clickable", False),
                "enabled": element_info.get("enabled", False)
            })
        else:
            # 多个元素
            for i in range(count):
                element = elements[i]
                element_info = element.info
                bounds = element_info.get("bounds", {})
                center_x = (bounds["left"] + bounds["right"]) // 2
                center_y = (bounds["top"] + bounds["bottom"]) // 2
                
                found_elements.append({
                    "index": i,
                    "text": element_info.get("text", ""),
                    "resource_id": element_info.get("resourceId", ""),
                    "class_name": element_info.get("className", ""),
                    "package": element_info.get("packageName", ""),
                    "bounds": bounds,
                    "center_x": center_x,
                    "center_y": center_y,
                    "clickable": element_info.get("clickable", False),
                    "enabled": element_info.get("enabled", False)
                })
        
        return {
            "success": True,
            "message": f"找到 {len(found_elements)} 个包含文本 '{text_to_find}' 的元素",
            "elements": found_elements,
            "device_id": device_id,
            "hierarchy_file": xml_path
        }
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return {
            "success": False,
            "message": f"获取UI层次结构或查找元素失败: {str(e)}",
            "error_details": error_details
        }

@mcp.tool()
def dump_ui_hierarchy(output_dir: str, device_id: Optional[str] = None) -> Dict[str, Any]:
    """获取完整的车机UI层次结构
    
    Args:
        output_dir: 保存UI层次结构文件的目录路径(必填)
        device_id: 设备ID，如果为空则使用默认设备
    """
    try:
        # 确保目录存在
        os.makedirs(output_dir, exist_ok=True)
            
        # 初始化设备连接
        if device_id:
            d = u2.connect(device_id)
        else:
            devices = get_connected_devices()
            if not devices:
                return {
                    "success": False,
                    "message": "未检测到已连接的设备"
                }
            device_id = devices[0]["id"]
            d = u2.connect(device_id)
        
        # 获取当前UI层次结构
        print("正在获取UI层次结构...")
        xml_content = d.dump_hierarchy()
        
        # 保存层次结构到XML文件
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        xml_path = os.path.join(output_dir, f"ui_hierarchy_{timestamp}.xml")
        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(xml_content)
            
        # 获取当前应用信息
        current_app = d.app_current()
        window_size = d.window_size()
        
        return {
            "success": True,
            "message": "成功获取UI层次结构",
            "device_id": device_id,
            "hierarchy_file": xml_path,
            "current_app": current_app,
            "window_size": window_size
        }
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return {
            "success": False,
            "message": f"获取UI层次结构失败: {str(e)}",
            "error_details": error_details
        }

@mcp.tool()
def find_and_click_by_text(text_to_find: str, device_id: Optional[str] = None, wait_time: float = 0.5) -> Dict[str, Any]:
    """通过文本查找并点击UI元素
    
    Args:
        text_to_find: 要查找和点击的控件文字内容
        device_id: 设备ID，如果为空则使用默认设备
        wait_time: 点击前等待的时间(秒)，默认0.5秒
    """
    try:
            
        # 初始化设备连接
        if device_id:
            d = u2.connect(device_id)
        else:
            devices = get_connected_devices()
            if not devices:
                return {
                    "success": False,
                    "message": "未检测到已连接的设备"
                }
            device_id = devices[0]["id"]
            d = u2.connect(device_id)
        
        
        # 先尝试精确文本匹配
        element = d(text=text_to_find)
        method = "精确匹配"
        
        # 如果没找到，尝试包含文本匹配
        if not element.exists:
            element = d(textContains=text_to_find)
            method = "部分匹配"
            
        # 如果仍然没找到，返回失败
        if not element.exists:
            return {
                "success": False,
                "message": f"未找到包含文本 '{text_to_find}' 的元素"
            }
        
        # 获取元素信息
        element_info = element.info
        bounds = element_info.get("bounds", {})
        center_x = (bounds["left"] + bounds["right"]) // 2
        center_y = (bounds["top"] + bounds["bottom"]) // 2
        
        # 等待指定时间
        if wait_time > 0:
            time.sleep(wait_time)
        
        # 点击元素
        print(f"点击元素: '{text_to_find}' 坐标: ({center_x}, {center_y})")
        element.click()
        
        return {
            "success": True,
            "message": f"成功点击了文本为 '{text_to_find}' 的元素 (通过{method})",
            "element_info": {
                "text": element_info.get("text", ""),
                "resource_id": element_info.get("resourceId", ""),
                "class_name": element_info.get("className", ""),
                "package": element_info.get("packageName", ""),
                "bounds": bounds,
                "center_x": center_x,
                "center_y": center_y,
                "clickable": element_info.get("clickable", False)
            }
        }
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return {
            "success": False,
            "message": f"查找并点击文本元素失败: {str(e)}",
            "error_details": error_details
        }
    
@mcp.tool()
def collect_crash_logs(device_id: Optional[str] = None, result_dir: str = "", days: int = 1) -> Dict[str, Any]:
    """从设备收集近期的崩溃日志文件
    
    从以下关键目录拉取崩溃日志：
    - /data/system/dropbox (系统崩溃)
    - /data/anr (应用无响应)
    - /data/tombstones (原生崩溃)
    
    Args:
        device_id: 设备ID，如果为空则使用默认设备
        result_dir: 保存日志的本地目录路径(必填)，如果不存在会自动创建
        days: 收集多少天内的日志文件，默认为1天
    """
    try:
        # 检查结果目录参数
        if not result_dir:
            return {
                "success": False,
                "message": "请指定result_dir参数来保存收集的日志文件"
            }
        
        # 创建日志存储目录
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        device_param = f"{device_id}_" if device_id else ""
        target_dir = os.path.join(result_dir, f"{device_param}crash_logs_{timestamp}")
        os.makedirs(target_dir, exist_ok=True)
        
        print(f"日志将保存到: {target_dir}")
        
        # 处理设备ID参数
        device_arg = f"-s {device_id} " if device_id else ""
        
        # 要收集的目录列表
        log_dirs = [
            {"path": "/data/system/dropbox", "local_dir": "dropbox"},
            {"path": "/data/anr", "local_dir": "anr"},
            {"path": "/data/tombstones", "local_dir": "tombstones"}
        ]
        
        result_stats = {}
        total_files = 0
        
        # 从每个目录收集日志
        for log_dir_info in log_dirs:
            remote_dir = log_dir_info["path"]
            local_subdir = os.path.join(target_dir, log_dir_info["local_dir"])
            os.makedirs(local_subdir, exist_ok=True)
            
            print(f"从 {remote_dir} 收集日志...")
            
            # 使用 find 命令列出最近N天修改的文件
            if days > 0:
                find_cmd = f"shell find {remote_dir} -type f -mtime -{days}"
            else:
                find_cmd = f"shell find {remote_dir} -type f"
                
            list_result = run_adb_command(f"{device_arg}{find_cmd}")
            
            if not list_result["success"]:
                print(f"列举 {remote_dir} 中的文件失败: {list_result.get('error', '未知错误')}")
                result_stats[log_dir_info["local_dir"]] = {"status": "failed", "error": list_result.get('error')}
                continue
                
            files = list_result["output"].strip().split('\n')
            files = [f for f in files if f.strip()]  # 过滤空行
            
            if not files or (len(files) == 1 and not files[0].strip()):
                print(f"目录 {remote_dir} 中未找到最近{days}天内修改的文件")
                result_stats[log_dir_info["local_dir"]] = {"status": "success", "count": 0}
                continue
                
            # 为每个文件创建pull命令
            file_count = 0
            pulled_files = []
            
            for remote_file in files:
                if not remote_file.strip():
                    continue
                    
                # 提取文件名
                filename = os.path.basename(remote_file)
                local_file = os.path.join(local_subdir, filename)
                
                # 拉取文件
                pull_result = run_adb_command(f"{device_arg}pull {remote_file} {local_file}")
                
                if pull_result["success"]:
                    file_count += 1
                    pulled_files.append({
                        "remote_path": remote_file,
                        "local_path": local_file,
                        "filename": filename
                    })
                    print(f"已拉取: {filename}")
                else:
                    print(f"拉取 {filename} 失败: {pull_result.get('error', '未知错误')}")
            
            result_stats[log_dir_info["local_dir"]] = {
                "status": "success", 
                "count": file_count,
                "files": pulled_files
            }
            total_files += file_count
        
        # 尝试获取系统日志摘要
        logcat_file = os.path.join(target_dir, "recent_logcat.log")
        logcat_result = run_adb_command(f"{device_arg}logcat -d -v threadtime > {logcat_file}")
        if logcat_result["success"]:
            print(f"已保存当前系统日志到: {logcat_file}")
            total_files += 1
        
        # 创建一个摘要报告
        summary_file = os.path.join(target_dir, "collection_summary.txt")
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(f"崩溃日志收集摘要\n")
            f.write(f"================\n\n")
            f.write(f"设备ID: {device_id or '默认设备'}\n")
            f.write(f"收集时间: {timestamp}\n")
            f.write(f"收集范围: 最近{days}天内的日志\n")
            f.write(f"总文件数: {total_files}\n\n")
            
            for dir_name, stats in result_stats.items():
                f.write(f"{dir_name}目录: {stats['count']}个文件\n")
                if stats['count'] > 0:
                    for idx, file_info in enumerate(stats['files'], 1):
                        f.write(f"  {idx}. {file_info['filename']}\n")
                f.write("\n")
        
        return {
            "success": True,
            "message": f"成功从设备收集了 {total_files} 个崩溃日志文件",
            "device_id": device_id,
            "log_directory": target_dir,
            "collection_time": timestamp,
            "days_collected": days,
            "file_count": total_files,
            "stats": result_stats
        }
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return {
            "success": False,
            "message": f"收集崩溃日志时出错: {str(e)}",
            "error_details": error_details
        }
    
@mcp.tool()
def export_android_logs(android_dir: str, result_dir: str, device_id: Optional[str] = None, 
                        filter_pattern: str = "") -> Dict[str, Any]:
    """从Android设备指定目录导出所有日志文件
    
    Args:
        android_dir: Android设备上要导出的目录路径(必填)，如 /data/log
        result_dir: 保存日志的本地目录路径(必填)，如果不存在会自动创建
        device_id: 设备ID，如果为空则使用默认设备
        filter_pattern: 文件名过滤表达式，例如 "*.log" 或 "crash*"，可选
    """
    try:
        # 参数验证
        if not android_dir:
            return {
                "success": False,
                "message": "请指定android_dir参数(设备上的日志目录路径)"
            }
        
        if not result_dir:
            return {
                "success": False,
                "message": "请指定result_dir参数(本地保存目录)"
            }
        
        # 创建日志存储目录
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        device_param = f"{device_id}_" if device_id else ""
        android_dir_name = android_dir.replace("/", "_").strip("_")
        target_dir = os.path.join(result_dir, f"{device_param}logs_{android_dir_name}_{timestamp}")
        os.makedirs(target_dir, exist_ok=True)
        
        print(f"日志将保存到: {target_dir}")
        
        # 处理设备ID参数
        device_arg = f"-s {device_id} " if device_id else ""
        
        # 检查目录是否存在并可访问
        check_result = run_adb_command(f"{device_arg}shell ls -l {android_dir}")
        if not check_result["success"]:
            return {
                "success": False,
                "message": f"设备上的目录 {android_dir} 不存在或无法访问: {check_result.get('error', '未知错误')}"
            }
        
        # 构建查找命令 - 获取全部文件
        find_cmd = f"shell find {android_dir} -type f"
        
        # 添加过滤器(如果指定)
        if filter_pattern:
            find_cmd += f" -name \"{filter_pattern}\""
            
        # 执行查找命令
        list_result = run_adb_command(f"{device_arg}{find_cmd}")
        
        if not list_result["success"]:
            return {
                "success": False,
                "message": f"查找文件失败: {list_result.get('error', '未知错误')}"
            }
        
        # 处理文件列表
        files = list_result["output"].strip().split('\n')
        files = [f for f in files if f.strip()]  # 过滤空行
        
        if not files:
            return {
                "success": True,
                "message": f"在 {android_dir} 中未找到任何文件",
                "file_count": 0
            }
        
        print(f"找到 {len(files)} 个文件，准备导出...")
        
        # 拉取文件
        file_count = 0
        pulled_files = []
        failed_files = []
        total_size_bytes = 0
        
        for remote_file in files:
            if not remote_file.strip():
                continue
                
            # 创建保持原始目录结构的本地路径
            rel_path = os.path.relpath(remote_file, android_dir)
            local_dir = os.path.join(target_dir, os.path.dirname(rel_path))
            os.makedirs(local_dir, exist_ok=True)
            
            filename = os.path.basename(remote_file)
            local_file = os.path.join(local_dir, filename)
            
            # 拉取文件
            print(f"正在导出: {remote_file}")
            pull_result = run_adb_command(f"{device_arg}pull {remote_file} {local_file}")
            
            if pull_result["success"]:
                file_size = os.path.getsize(local_file)
                total_size_bytes += file_size
                
                file_count += 1
                pulled_files.append({
                    "remote_path": remote_file,
                    "local_path": local_file,
                    "filename": filename,
                    "size": file_size
                })
                print(f"已成功导出: {filename} ({format_file_size(file_size)})")
            else:
                failed_files.append({
                    "remote_path": remote_file,
                    "error": pull_result.get("error", "未知错误")
                })
                print(f"导出 {filename} 失败: {pull_result.get('error', '未知错误')}")
        
        # 创建摘要报告
        summary_file = os.path.join(target_dir, "export_summary.txt")
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(f"日志导出摘要\n")
            f.write(f"==========\n\n")
            f.write(f"设备ID: {device_id or '默认设备'}\n")
            f.write(f"源目录: {android_dir}\n")
            f.write(f"导出时间: {timestamp}\n")
            f.write(f"过滤条件: {filter_pattern if filter_pattern else '无'}\n")
            f.write(f"导出成功: {file_count} 个文件 (总计 {format_file_size(total_size_bytes)})\n")
            f.write(f"导出失败: {len(failed_files)} 个文件\n\n")
            
            f.write("导出的文件列表:\n")
            for idx, file_info in enumerate(pulled_files, 1):
                f.write(f"  {idx}. {file_info['remote_path']} ({format_file_size(file_info['size'])})\n")
            
            if failed_files:
                f.write("\n导出失败的文件:\n")
                for idx, file_info in enumerate(failed_files, 1):
                    f.write(f"  {idx}. {file_info['remote_path']}\n")
                    f.write(f"     错误: {file_info['error']}\n")
        
        # 返回结果
        return {
            "success": True,
            "message": f"成功从 {android_dir} 导出 {file_count} 个文件，总计 {format_file_size(total_size_bytes)}",
            "android_dir": android_dir,
            "device_id": device_id,
            "log_directory": target_dir,
            "collection_time": timestamp,
            "file_count": file_count,
            "failed_count": len(failed_files),
            "total_size": format_file_size(total_size_bytes),
            "total_size_bytes": total_size_bytes,
            "filter_pattern": filter_pattern
        }
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return {
            "success": False,
            "message": f"导出日志时出错: {str(e)}",
            "error_details": error_details
        }

# 辅助函数：格式化文件大小
def format_file_size(size_bytes):
    """将字节大小转换为人类可读的格式"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes/1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes/(1024*1024):.2f} MB"
    else:
        return f"{size_bytes/(1024*1024*1024):.2f} GB"
    
def main():
    # 启动MCP服务器
    print(f"启动Android MCP服务器...")
    
    # 检查ADB是否可用
    adb_check = run_adb_command("version")
    if adb_check["success"]:
        print(f"ADB版本: {adb_check['output'].split()[4]}")
        
        # 检查连接的设备
        devices = get_connected_devices()
        if devices:
            print(f"已连接 {len(devices)} 台设备:")
            for device in devices:
                print(f"  - {device['id']} ({device['status']})")
        else:
            print("警告: 未检测到已连接的设备")
    else:
        print(f"警告: ADB不可用 - {adb_check.get('error', '未知错误')}")
    
    # 启动服务器
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()