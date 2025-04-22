import requests
import json
import os
import base64
import argparse
import sys
from pathlib import Path

# 定义颜色常量
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

__version__ = "0.1.1"

# 硬编码API配置
DEFAULT_API_URL = "http://pd-adminapi.spark.xd.com:8082/api/v1/update-minigame"
DEFAULT_CONTENT_TYPE = "application/json"

def load_config(config_path):
    """加载配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
            # 确保配置中包含data字段
            if 'data' not in config:
                config['data'] = {}
                
            return config
    except FileNotFoundError:
        print(f"{RED}配置文件不存在: {config_path}{RESET}")
        raise
    except json.JSONDecodeError:
        print(f"{RED}配置文件格式错误: {config_path}{RESET}")
        raise

def image_to_base64(image_path):
    """将图片转换为base64编码"""
    try:
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"图片文件不存在: {image_path}")
        print(f"{RED}请填写正确的文件路径或者删除该属性{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"处理图片时发生错误: {e}")
        sys.exit(1)

def process_folder(folder_path):
    """处理文件夹中的所有文件"""
    try:
        if not os.path.exists(folder_path):
            print(f"文件夹不存在: {folder_path}")
            print(f"{RED}请填写正确的文件路径或者删除该属性{RESET}")
            return None
            
        folder_content = {}
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, folder_path)
                try:
                    # 将文件转换为base64
                    with open(file_path, 'rb') as f:
                        file_content = base64.b64encode(f.read()).decode('utf-8')
                    folder_content[relative_path] = file_content
                except Exception as e:
                    print(f"处理文件 {file_path} 时发生错误: {e}")
                    print(f"{RED}请填写正确的文件路径或者删除该属性{RESET}")
                    continue
                
        return folder_content
    except Exception as e:
        print(f"处理文件夹时发生错误: {e}")
        sys.exit(1)

def process_images(config, config_dir):
    """处理配置文件中的图片和文件夹"""
    try:
        # 处理banner数组
        if 'banner' in config['data'] and isinstance(config['data']['banner'], list):
            banner_base64 = []
            for banner_path in config['data']['banner']:
                full_path = os.path.join(config_dir, banner_path)
                banner_base64.append(image_to_base64(full_path))
            config['data']['banner'] = banner_base64
            
        # 处理icon数组
        if 'icon' in config['data'] and isinstance(config['data']['icon'], list):
            icon_base64 = []
            for icon_path in config['data']['icon']:
                full_path = os.path.join(config_dir, icon_path)
                icon_base64.append(image_to_base64(full_path))
            config['data']['icon'] = icon_base64
            
        # 处理screenshots数组
        if 'screenshots' in config['data'] and isinstance(config['data']['screenshots'], list):
            screenshots_base64 = []
            for screenshot_path in config['data']['screenshots']:
                full_path = os.path.join(config_dir, screenshot_path)
                screenshots_base64.append(image_to_base64(full_path))
            config['data']['screenshots'] = screenshots_base64
            
        # 处理文件夹
        if 'outDirectory' in config['data'] and config['data']['outDirectory']:
            folder_path = os.path.join(config_dir, config['data']['outDirectory'])
            folder_content = process_folder(folder_path)
            if folder_content:
                config['data']['folder_content'] = folder_content
            
        return config
    except Exception as e:
        print(f"处理图片和文件夹时发生错误: {e}")
        print(f"{RED}请填写正确的文件路径或者删除该属性{RESET}")
        sys.exit(1)

def send_request(config, api_url, content_type, token):
    """发送请求"""
    try:
        # 设置请求头
        headers = {
            "Content-Type": content_type,
            "Authorization": token
        }

        data = config['data']

        # 发送请求
        print(f"正在发送请求到: {api_url}")

        response = requests.post(api_url, headers=headers, json=data, verify=False)
        
        # 打印响应信息
        print(f"状态码: {response.status_code}")
        
        # 尝试解析JSON响应
        try:
            response_json = response.json()
            
            # 检查响应中的result字段
            if 'data' in response_json and isinstance(response_json['data'], dict) and 'result' in response_json['data'] and response_json['data']['result'] is False:
                # 只输出msg和url
                if 'msg' in response_json['data']:
                    print(f"{RED}错误: {response_json['data']['msg']}{RESET}")
                if 'url' in response_json['data']:
                    print(f"链接: {response_json['data']['url']}")
            else:
                # 输出完整的响应JSON
                print(f"响应JSON: {json.dumps(response_json, ensure_ascii=False, indent=2)}")
        except json.JSONDecodeError:
            print(f"{RED}响应内容: {response.text}{RESET}")
            
        return response

    except requests.exceptions.RequestException as e:
        print(f"{RED}请求发生错误: {e}{RESET}")
        sys.exit(1)

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='TapTap SCE小游戏自动发布工具')
    parser.add_argument('-c', '--config', 
                        default='minigame_config.json',
                        help='配置文件路径 (默认: minigame_config.json)')
    parser.add_argument('-v', '--version', 
                        action='version', 
                        version=f'sce-minigame-publisher {__version__}')
    parser.add_argument('--verbose', 
                        action='store_true', 
                        help='显示详细日志')
    
    # Add API related parameters
    parser.add_argument('--url', 
                        default=DEFAULT_API_URL,
                        help=f'API URL (default: {DEFAULT_API_URL})')
    parser.add_argument('--content-type', 
                        default=DEFAULT_CONTENT_TYPE,
                        help=f'Content type (default: {DEFAULT_CONTENT_TYPE})')
    
    return parser.parse_args()

def is_latin1_compatible(text):
    """检查文本是否兼容Latin-1编码"""
    try:
        text.encode('latin-1')
        return True
    except UnicodeEncodeError:
        return False

def main():
    """主函数"""
    try:
        # 解析命令行参数
        args = parse_args()
        
        # 获取配置文件绝对路径
        if os.path.isabs(args.config):
            config_path = args.config
        else:
            config_path = os.path.abspath(args.config)
        
        config_dir = os.path.dirname(config_path)
        
        # 加载配置
        print("正在加载配置文件...")
        if args.verbose:
            print(f"配置文件路径: {config_path}")
            
        config = load_config(config_path)
        
        # 从配置文件获取token
        token = config.get('token')
        if not token:
            print(f"{RED}错误: 配置文件中缺少token字段，请在配置文件中设置。{RESET}")
            return False
            
        # 检查token是否包含非Latin-1字符
        if not is_latin1_compatible(token):
            print(f"{RED}错误: token包含非Latin-1字符，请使用ASCII字符（如英文字母、数字和符号）组成的token。{RESET}")
            print(f"{YELLOW}提示: HTTP请求头只能包含Latin-1字符集中的字符。{RESET}")
            return False
        
        # 处理图片
        print("正在处理图片...")
        config = process_images(config, config_dir)
        
        # 发送请求
        response = send_request(config, args.url, args.content_type, token)
        
        return response.status_code == 200

    except Exception as e:
        print(f"{RED}程序执行出错: {e}{RESET}")
        import traceback
        print(traceback.format_exc())  # 打印完整的错误堆栈
        return False

def cli_main():
    """CLI入口点"""
    success = main()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    cli_main() 