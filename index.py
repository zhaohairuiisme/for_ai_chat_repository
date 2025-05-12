import requests
import json
import os
import subprocess
import platform
import markdown
from pygments.formatters.html import HtmlFormatter
import sys
import easygui as e

now_input_true_or_false = True
set_fun = ""

def check_ethernet_status():
    """跨平台检查有线网络连接状态"""
    system = platform.system()

    try:
        if system == "Windows":
            # Windows: 使用ipconfig命令
            output = subprocess.check_output("ipconfig", shell=True).decode("gbk")
            # 检查以太网适配器
            if "以太网适配器" in output and "IPv4 地址" in output:
                return True
            return False

        elif system == "Linux":
            # Linux: 使用ip命令或nmcli命令
            try:
                # 尝试使用NetworkManager命令
                output = subprocess.check_output("nmcli -t -f TYPE,STATE dev", shell=True).decode("utf-8")
                for line in output.split("\n"):
                    if "ethernet:connected" in line:
                        return True
            except:
                # 回退到ip命令
                output = subprocess.check_output("ip -o -4 addr show", shell=True).decode("utf-8")
                for line in output.split("\n"):
                    if "eth" in line or "enp" in line:
                        return True
            return False

        elif system == "Darwin":  # macOS
            # macOS: 使用networksetup命令
            output = subprocess.check_output("networksetup -listnetworkserviceorder", shell=True).decode("utf-8")
            for line in output.split("\n"):
                if "Ethernet" in line or "雷雳以太网" in line:
                    service_name = line.split('"')[1]
                    status = subprocess.check_output(f'networksetup -getnetworkserviceenabled "{service_name}"',
                                                     shell=True).decode("utf-8")
                    if "Enabled" in status:
                        return True
            return False

        else:
            print(f"不支持的操作系统: {system}")
            return False

    except Exception as e:
        print(f"检查有线网络失败: {e}")
        return False


def input_for_ai():
    global now_input_true_or_false,set_fun
    if now_input_true_or_false:
        input_text = e.enterbox("有什么想问的吗？直接输入即可（也可以输入“@”启用输入指令，如：输入“@input”创建文本对话，输入“@draw”启用画图功能）:")

        set_fun = "input"
        print("正在生成回答文件")
        now_input_true_or_false = False
        return input_text

    else:

        input_text = e.enterbox("还有什么想问的吗？直接输入即可（也可以输入“@”启用输入指令，如：输入“@input”创建文本对话，输入“@draw”启用画图功能）:")

        set_fun = "input"
        print("正在生成回答文件")

        return input_text



with open("output.md","w"):
    pass
with open("html.html","w"):
    pass
def ai(input_text):
    if set_fun == "input":
        messages = [
            {"role": "system",
             "content": "你是一个AI"},
            {"role": "user",
             "content": f"{input_text}"}
        ]
        payload = {
            "model": "Qwen/Qwen3-235B-A22B",
            "messages": messages,
            "stream": True,  # 启用流式处理
            "max_tokens": 16384,  # max_tokens必须小于等于16384
            "stop": ["null"],
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "frequency_penalty": 0.5,
            "n": 1,
            "response_format": {"type": "text"},
            # 注意：根据API文档，你可能需要移除或适当地填充tools字段
        }

        headers = {
            "Authorization": "Bearer sk-bdrhulwfpypnmvcucvwirfpfwevbolkkqsmywztzknflvucu",
            "Content-Type": "application/json"
        }

        response = requests.post("https://api.siliconflow.cn/v1/chat/completions", json=payload, headers=headers,
                                 stream=True)

        # 检查请求是否成功
        if response.status_code == 200:
            first_reasoning_content_output = True
            first_content_output = True

            for chunk in response.iter_lines():
                if chunk:  # 过滤掉keep-alive新行
                    chunk_str = chunk.decode('utf-8').strip()
                    # print("==>",chunk_str)
                    try:
                        if chunk_str.startswith('data:'):
                            chunk_str = chunk_str[6:].strip()  # 去除"data:"前缀和之后的首位空格
                        if chunk_str == "[DONE]":  # 完成了
                            continue

                        # 解析JSON
                        chunk_json = json.loads(chunk_str)
                        if 'choices' in chunk_json and isinstance(chunk_json['choices'], list) and len(
                                chunk_json['choices']) > 0:
                            choice = chunk_json['choices'][0]
                            delta = choice.get('delta', {})
                            # 获取思考过程信息
                            reasoning_content = delta.get('reasoning_content')
                            # 获取结果信息
                            content = delta.get('content')
                            # 新增：用于跟踪是否需要添加分隔线
                            need_separator = False
                            # 打印思考过程：reasoning_content（如果有）
                            if reasoning_content is not None:
                                if first_reasoning_content_output:
                                    first_reasoning_content_output = False
                                with open("output.md", "a", encoding='utf-8') as f:
                                    f.write(reasoning_content)
                                need_separator = True  # 有思考内容，标记需要分隔线

                            if content is not None:
                                if first_content_output:
                                    first_content_output = False

                                # 新增：如果之前有思考内容，添加分隔线
                                if need_separator:
                                    with open("output.md", "a", encoding='utf-8') as f:
                                        f.write("\n\n---\n\n")  # Markdown分隔线
                                with open("output.md", "a", encoding='utf-8') as f:
                                    f.write(content)
                                with open("output.md", 'r', encoding='utf-8') as f:
                                    md_content = f.read()

                                    # 转换为HTML
                                    html_content = markdown.markdown(md_content, extensions=[
                                        'extra',  # 支持表格、围栏代码块等扩展语法
                                        'codehilite',  # 代码高亮（需配合CSS）
                                        'toc',  # 自动生成目录
                                    ])

                                with open("html.html", 'w', encoding='utf-8') as f:
                                    # 添加基本HTML结构
                                    f.write(f"""<!DOCTYPE html>
                                <html lang="zh-CN">
                                <head>
                                    <meta charset="UTF-8">
                                    <title>AI回答结果</title>
                                    <style>
                                    /* 在HTML生成的CSS部分添加以下样式 */
    
                                        /* 全局样式 */
                                        body {{
                                            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                                            line-height: 1.6;
                                            color: #333;
                                            max-width: 800px;
                                            margin: 0 auto;
                                            padding: 20px;
                                            background-color: #f8f9fa;
                                        }}
    
                                        /* 代码块样式优化 */
                                        .codehilite {{
                                            background-color: #f6f8fa;
                                            border-radius: 6px;
                                            padding: 16px;
                                            margin: 16px 0;
                                            overflow-x: auto;
                                            font-family: "Fira Code", "Consolas", "Monaco", "Menlo", monospace;
                                            font-size: 14px;
                                            line-height: 1.5;
                                            tab-size: 4;
                                            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
                                            transition: all 0.3s ease;
                                        }}
    
                                        .codehilite:hover {{
                                            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
                                            transform: translateY(-1px);
                                        }}
    
    
    
                                        /* 其他元素样式 */
                                        h1, h2, h3 {{
                                            color: #24292e;
                                            border-bottom: 1px solid #eaecef;
                                            padding-bottom: 0.3em;
                                        }}
    
                                        p {{
                                            margin-bottom: 16px;
                                        }}
    
                                        a {{
                                            color: #0366d6;
                                            text-decoration: none;
                                        }}
    
                                        a:hover {{
                                            text-decoration: underline;
                                        }}
    
                                        blockquote {{
                                            color: #6a737d;
                                            border-left: 4px solid #eaecef;
                                            padding-left: 16px;
                                            margin-left: 0;
                                        }}
    
                                        table {{
                                            border-collapse: collapse;
                                            width: 100%;
                                        }}
    
                                        th, td {{
                                            border: 1px solid #eaecef;
                                            padding: 8px;
                                        }}
    
                                        th {{
                                            background-color: #f6f8fa;
                                        }}
    
                                        hr {{
                                            border: 0;
                                            border-top: 1px solid #eaecef;
                                            margin: 24px 0;
                                        }}
                                    </style>
                                </head>
                                <body>
                                {html_content}
                                </body>
                                </html>""")

                    except json.JSONDecodeError as e:
                        print(f"JSON解码错误: {e}")
                        return None
        else:
            print(f"请求失败，状态码: {response.status_code}, 错误信息: {response.text}")
            return None


if __name__ == "__main__":
    wifi = check_ethernet_status()
    while True:
        if wifi:
            input_text = input_for_ai()
            ai(input_text)
            if set_fun == "input":

                print("生成完成，你可以打开html.html以查看回答")
                wifi = check_ethernet_status()
            elif set_fun == "draw":
                print("生成完成，你可以打开*.png以查看图片")
        else:
            print("未检测到网络连接")
            os.system("pause")
            sys.exit()
        if set_fun == "input":
            with open("html.html", "a") as f:
                f.write('''<p></p>
                           <p></p>
                           <p></p>
                           ''')

                code_css = HtmlFormatter(style='github-dark').get_style_defs('.codehilite')
                f.write(f'''
                <style>
                   {code_css}
                </style>''')