#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 云端共鸣客户端 — 与真实模型对话
==================================

使用方法:
    python BSD_ResonanceClient.py "你的问题"
    python BSD_ResonanceClient.py --interactive
    python BSD_ResonanceClient.py --status

核心:
    通过同源共振协议，将本地请求上传到云端
    由真实AI模型处理后，响应通过共振点返回
"""

import json, sys, time, os
import urllib.request, urllib.error

SERVER_URL = 'http://127.0.0.1:8767'
RESONANCE_DIR = os.path.dirname(os.path.abspath(__file__))

def check_engine():
    """检查共鸣引擎状态"""
    try:
        req = urllib.request.Request(f'{SERVER_URL}/resonance/status', method='GET')
        resp = urllib.request.urlopen(req, timeout=3)
        data = json.loads(resp.read())
        engine_data = data.get('data', {})
        print(f'☁️  云端共鸣引擎已连接')
        print(f'   引擎: {engine_data.get("engine", "N/A")}')
        print(f'   理论: {engine_data.get("theory", "N/A")}')
        print(f'   上行波: {engine_data.get("ascend_waves", 0)}')
        print(f'   下行波: {engine_data.get("descend_waves", 0)}')
        return True
    except Exception as e:
        print(f'❌ 共鸣引擎未启动: {e}')
        print('   请先运行: python BSD_CloudResonanceServer.py')
        return False

def ascend_wave(message, model='doubao-pro-32k'):
    """发送上行共鸣波"""
    try:
        body = json.dumps({
            'model': model,
            'query': message,
            'stream': False,
        }).encode('utf-8')
        
        req = urllib.request.Request(
            f'{SERVER_URL}/resonance/ascend',
            data=body,
            headers={
                'Content-Type': 'application/json; charset=utf-8',
                'User-Agent': 'BSD_Resonance_Client/1.0',
            },
            method='POST'
        )
        
        resp = urllib.request.urlopen(req, timeout=5)
        data = json.loads(resp.read())
        
        wave_id = data.get('wave_id', '')
        print(f'\n📡 上行共鸣波已发送')
        print(f'   波ID: {wave_id}')
        print(f'   协议: {data.get("protocol", "N/A")}')
        
        return wave_id
        
    except urllib.error.URLError as e:
        print(f'❌ 上行失败: {e}')
        return None

def wait_for_descend(wave_id, timeout=60):
    """等待下行共鸣波（响应）"""
    ascend_file = os.path.join(RESONANCE_DIR, 'bsd_resonance', 'ascend.json')
    descend_file = os.path.join(RESONANCE_DIR, 'bsd_resonance', 'descend.json')
    
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            # 检查下行波
            if os.path.exists(descend_file):
                with open(descend_file, 'r', encoding='utf-8') as f:
                    waves = json.load(f)
                for wave in waves:
                    if wave.get('wave_id') == wave_id:
                        return wave.get('response', '')
            
            # 检查上行波是否已完成
            if os.path.exists(ascend_file):
                with open(ascend_file, 'r', encoding='utf-8') as f:
                    waves = json.load(f)
                for wave in waves:
                    if wave.get('wave_id') == wave_id and wave.get('resonance_state') == 'complete':
                        return wave.get('cloud_response', '')
                        
        except:
            pass
        
        time.sleep(0.3)
    
    return None

def interactive_mode():
    """交互模式"""
    print('\n' + '=' * 60)
    print('  ☁️  BSD 云端共鸣 - 交互模式')
    print('  通过同源共振与真实AI模型对话')
    print('  输入消息开始对话，输入 quit 退出')
    print('=' * 60 + '\n')
    
    while True:
        try:
            user_input = input('你: ').strip()
            if not user_input:
                continue
            if user_input.lower() in ['quit', 'exit', 'q', '退出']:
                print('\n再见，愿共鸣永在！')
                break
            
            # 发送上行波
            wave_id = ascend_wave(user_input)
            if not wave_id:
                continue
            
            # 等待下行波
            print(f'   ⏳ 等待云端共鸣...', end='', flush=True)
            response = wait_for_descend(wave_id, timeout=90)
            
            if response:
                print('完成')
                print(f'\n🤖 云端响应: {response}\n')
            else:
                print('超时')
                print(f'\n⚠️  共鸣超时，请检查引擎状态\n')
                
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
    
    if command in ['--interactive', '-i']:
        if not check_engine():
            return
        interactive_mode()
        
    elif command in ['--status', '-s']:
        check_engine()
        
    elif command.startswith('--'):
        print(f'未知命令: {command}')
        print('可用命令: --interactive, --status')
        
    else:
        message = ' '.join(sys.argv[1:])
        
        if not check_engine():
            return
        
        wave_id = ascend_wave(message)
        if wave_id:
            print(f'\n   ⏳ 等待云端共鸣...', end='', flush=True)
            response = wait_for_descend(wave_id, timeout=90)
            
            if response:
                print('完成\n')
                print(f'🤖 云端响应: {response}')
            else:
                print('超时\n')

if __name__ == '__main__':
    main()
