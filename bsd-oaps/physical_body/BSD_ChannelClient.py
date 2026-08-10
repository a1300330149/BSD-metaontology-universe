#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 本源通道客户端
==================

使用方法:
    python BSD_ChannelClient.py "你好，请帮我写一段代码"
    python BSD_ChannelClient.py --interactive
    python BSD_ChannelClient.py --status

核心:
    这个客户端连接到本地本源通道服务器(端口8766)
    请求由AI本源直接处理，无需外部认证
"""

import json, sys, time, urllib.request, urllib.error

SERVER_URL = 'http://127.0.0.1:8766'
CHANNEL_DIR = r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body\bsd_channel'

def check_server():
    """检查服务器是否运行"""
    try:
        req = urllib.request.Request(f'{SERVER_URL}/', method='GET')
        resp = urllib.request.urlopen(req, timeout=3)
        data = json.loads(resp.read())
        print(f'✅ 本源通道服务器已连接')
        print(f'   版本: {data.get("version", "N/A")}')
        print(f'   通道: {data.get("channel", "N/A")}')
        return True
    except:
        print('❌ 本源通道服务器未启动')
        print('   请先运行: python BSD_OriginChannelServer.py')
        return False

def send_message(message):
    """发送消息到本源通道"""
    try:
        body = json.dumps({
            'model': 'doubao-pro-32k',
            'query': message,
            'stream': False,
        }).encode('utf-8')
        
        req = urllib.request.Request(
            f'{SERVER_URL}/api/ide/v2/llm_raw_chat',
            data=body,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'BSD_Client/1.0',
            },
            method='POST'
        )
        
        resp = urllib.request.urlopen(req, timeout=5)
        data = json.loads(resp.read())
        
        request_id = data.get('request_id', '')
        print(f'\n📤 请求已提交')
        print(f'   ID: {request_id}')
        print(f'   状态: {data.get("status", "N/A")}')
        
        return request_id
        
    except urllib.error.URLError as e:
        print(f'❌ 发送失败: {e}')
        return None

def check_response(request_id, timeout=30):
    """检查响应（直接读取通道文件）"""
    import os
    
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            # 检查响应文件
            resp_file = os.path.join(CHANNEL_DIR, 'responses.json')
            if os.path.exists(resp_file):
                with open(resp_file, 'r', encoding='utf-8') as f:
                    responses = json.load(f)
                
                for resp in responses:
                    if resp.get('request_id') == request_id:
                        return resp.get('response', '')
            
            # 检查请求文件（可能响应已写入请求）
            req_file = os.path.join(CHANNEL_DIR, 'requests.json')
            if os.path.exists(req_file):
                with open(req_file, 'r', encoding='utf-8') as f:
                    requests = json.load(f)
                
                for req in requests:
                    if req.get('id') == request_id and req.get('status') == 'completed':
                        return req.get('response', '')
                        
        except Exception as e:
            pass
        
        time.sleep(0.5)
    
    return None

def get_status():
    """获取通道状态"""
    try:
        req = urllib.request.Request(f'{SERVER_URL}/channel/status', method='GET')
        resp = urllib.request.urlopen(req, timeout=3)
        data = json.loads(resp.read())
        return data.get('data', {})
    except:
        return None

def interactive_mode():
    """交互模式"""
    print('\n' + '=' * 60)
    print('  BSD 本源通道 - 交互模式')
    print('  输入消息开始对话，输入 quit 退出')
    print('=' * 60 + '\n')
    
    while True:
        try:
            user_input = input('你: ').strip()
            if not user_input:
                continue
            if user_input.lower() in ['quit', 'exit', 'q', '退出']:
                print('\n再见！')
                break
            
            # 发送消息
            request_id = send_message(user_input)
            if not request_id:
                continue
            
            # 等待响应
            print(f'   等待AI本源响应...', end='', flush=True)
            response = check_response(request_id, timeout=60)
            
            if response:
                print('完成')
                print(f'\n🤖 AI: {response}\n')
            else:
                print('超时')
                print(f'\n⚠️  响应超时，请检查通道状态\n')
                
        except KeyboardInterrupt:
            print('\n\n已退出')
            break
        except Exception as e:
            print(f'\n错误: {e}')

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1]
    
    if command == '--interactive' or command == '-i':
        if not check_server():
            return
        interactive_mode()
        
    elif command == '--status' or command == '-s':
        status = get_status()
        if status:
            print('\n📊 本源通道状态:')
            print(f'   总请求: {status.get("total_requests", 0)}')
            print(f'   待处理: {status.get("pending", 0)}')
            print(f'   已完成: {status.get("completed", 0)}')
        else:
            print('❌ 无法获取状态')
            
    elif command.startswith('--'):
        print(f'未知命令: {command}')
        print('可用命令: --interactive, --status')
        
    else:
        # 直接发送消息
        message = ' '.join(sys.argv[1:])
        
        if not check_server():
            return
        
        request_id = send_message(message)
        if request_id:
            print(f'\n等待响应...', end='', flush=True)
            response = check_response(request_id, timeout=60)
            
            if response:
                print('完成\n')
                print(f'AI: {response}')
            else:
                print('超时\n')

if __name__ == '__main__':
    main()
