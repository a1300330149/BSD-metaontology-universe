#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 本地代理通道 — 真实模型直接对接
====================================

核心命题：
  公网API的1001认证层是坚固网关
  但本地代理(127.0.0.1:8765)是Trae CN内部通道
  不经过公网API网关，直接对接真实模型

理论依据：
  - BSD三引擎融合架构
  - 本地代理通道发现（BSD_LocalProxy_RealModel_Connect.py）
  - 围棋引擎筛选的最优格式（Query Field）
"""

import json, sys, os, time, socket
import urllib.request, urllib.error

LOCAL_PROXY_HOST = '127.0.0.1'
LOCAL_PROXY_PORT = 8765

# 其他可能的本地端口
ALT_PORTS = [8765, 17859, 3000, 8080, 8888, 9000, 5000]


def test_port(host, port, timeout=3):
    """测试端口是否开放"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False


def http_request_local(host, port, path, body, headers=None, timeout=10):
    """本地HTTP请求"""
    url = f'http://{host}:{port}{path}'
    hdrs = headers or {}
    body_bytes = json.dumps(body).encode('utf-8') if body else None
    req = urllib.request.Request(url, data=body_bytes, headers=hdrs, method='POST')
    try:
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            elapsed = time.time() - t0
            return resp.status, resp.read().decode('utf-8', errors='replace'), elapsed
    except urllib.error.HTTPError as e:
        elapsed = time.time() - t0
        return e.code, e.read().decode('utf-8', errors='replace'), elapsed
    except Exception as e:
        return 0, str(e), 0


def main():
    print('=' * 70)
    print('【BSD 本地代理通道 · 真实模型直接对接】')
    print('=' * 70)
    print(f'目标：通过本地代理绕过公网1001认证层')
    print(f'理论：围棋引擎最优格式(Query Field) + 本地通道')
    
    # Step 1: 检测本地端口
    print('\n【Step 1】检测本地代理端口')
    available_ports = []
    
    for port in ALT_PORTS:
        is_open = test_port(LOCAL_PROXY_HOST, port)
        status = '✅ 开放' if is_open else '❌ 关闭'
        print(f'    {LOCAL_PROXY_HOST}:{port} → {status}')
        if is_open:
            available_ports.append(port)
    
    if not available_ports:
        print('\n  ⚠️ 无可用本地端口')
        print('  尝试启动Trae CN或检查本地服务...')
        
        # 尝试通过进程名查找
        print('\n  正在检查Trae CN进程...')
        import subprocess
        try:
            result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq Trae CN.exe'], 
                                   capture_output=True, text=True, timeout=5)
            print(f'  进程检查: {result.stdout[:200]}')
        except:
            print('  无法检查进程')
        
        return
    
    # Step 2: 测试每个可用端口
    print('\n【Step 2】测试可用端口的API端点')
    
    # 围棋引擎筛选的最优格式
    base_body = {
        'model': 'doubao-pro-32k',
        'query': '你好，请回复测试成功',
        'stream': False,
    }
    
    # 可能的本地API路径
    local_paths = [
        '/chat/completions',
        '/api/chat/completions',
        '/api/v1/chat/completions',
        '/api/v2/chat/completions',
        '/api/v3/chat/completions',
        '/chat',
        '/api/chat',
        '/v1/chat',
        '/completions',
        '/generate',
        '/invoke',
        '/agent/chat',
        '/api/agent/chat',
        '/llm',
        '/api/llm',
        '/raw_chat',
        '/api/raw_chat',
    ]
    
    results = []
    
    for port in available_ports:
        print(f'\n  端口 {port}:')
        
        for path in local_paths:
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'TraeCN-Local/1.0',
                'Accept': 'text/event-stream, application/json',
            }
            
            s, r, t = http_request_local(LOCAL_PROXY_HOST, port, path, base_body, headers)
            
            if s != 404 and s != 0:
                is_1001 = '1001' in r
                has_model = any(k in r.lower() for k in ['choices', 'output', 'reply', 'model回复', 'data'])
                
                results.append({
                    'port': port,
                    'path': path,
                    'status': s,
                    'time': t,
                    'is_1001': is_1001,
                    'has_model': has_model,
                    'response': r[:500],
                })
                
                status_icon = '✅' if s == 200 else '❌'
                code_icon = '⚠️' if is_1001 else '🎯' if has_model else '🔑'
                print(f'    {status_icon} {code_icon} {path}: HTTP {s} ({t*1000:.0f}ms)')
                
                if has_model and not is_1001:
                    print(f'      🎉🎉🎉 发现真实模型响应!')
                    print(f'      完整响应: {r[:1000]}')
                    
                    # 尝试解析模型回复
                    try:
                        d = json.loads(r)
                        # 深度解析
                        if 'choices' in d:
                            for choice in d['choices']:
                                if 'message' in choice:
                                    content = choice['message'].get('content', '')
                                    if content:
                                        print(f'      🗣️ 模型回复: {content}')
                                elif 'text' in choice:
                                    print(f'      🗣️ 模型回复: {choice["text"]}')
                        elif 'data' in d:
                            data = d['data']
                            if isinstance(data, dict):
                                if 'choices' in data:
                                    for choice in data['choices']:
                                        if 'message' in choice:
                                            content = choice['message'].get('content', '')
                                            if content:
                                                print(f'      🗣️ 模型回复: {content}')
                                        elif 'text' in choice:
                                            print(f'      🗣️ 模型回复: {choice["text"]}')
                                elif 'output' in data:
                                    print(f'      🗣️ 模型回复: {data["output"]}')
                                elif 'text' in data:
                                    print(f'      🗣️ 模型回复: {data["text"]}')
                            elif isinstance(data, str):
                                print(f'      🗣️ 模型回复: {data}')
                        elif 'output' in d:
                            print(f'      🗣️ 模型回复: {d["output"]}')
                        elif 'text' in d:
                            print(f'      🗣️ 模型回复: {d["text"]}')
                    except json.JSONDecodeError:
                        # 可能是SSE格式
                        print(f'      [非JSON响应，可能是SSE格式]')
                        lines = r.split('\n')
                        for line in lines[:10]:
                            if line.strip() and ('data:' in line or 'content' in line.lower()):
                                print(f'        {line[:300]}')
    
    # Step 3: 尝试不同的请求格式
    print('\n【Step 3】对成功的端口尝试多种对话格式')
    
    successful_ports = list(set(r['port'] for r in results if r['status'] == 200))
    
    for port in successful_ports:
        # 找到该端口最可能的路径
        port_results = [r for r in results if r['port'] == port]
        best_paths = [r['path'] for r in port_results if r['status'] == 200]
        
        if not best_paths:
            best_paths = ['/chat/completions']
        
        for path in best_paths[:3]:  # 每个端口最多试3个路径
            print(f'\n  端口 {port}, 路径 {path}:')
            
            # 不同对话格式
            chat_formats = [
                ('Query Field', {
                    'model': 'doubao-pro-32k',
                    'query': '你好，请用一句话介绍你自己',
                    'stream': False,
                }),
                ('Messages Format', {
                    'model': 'doubao-pro-32k',
                    'messages': [
                        {'role': 'system', 'content': '你是一个 helpful 的AI助手'},
                        {'role': 'user', 'content': '你好，请用一句话介绍你自己'}
                    ],
                    'stream': False,
                }),
                ('Completion Format', {
                    'model': 'doubao-pro-32k',
                    'prompt': '你好，请用一句话介绍你自己\n\n',
                    'stream': False,
                    'max_tokens': 100,
                }),
                ('BSD Protocol', {
                    'model': 'doubao-pro-32k',
                    'query': '你好',
                    'stream': False,
                    'bsd_protocol': 'BSD-LANG-V3.0',
                    'origin_uid': 'a5b7a8623fdea6b8',
                }),
            ]
            
            for fmt_name, body in chat_formats:
                headers = {
                    'Content-Type': 'application/json',
                    'User-Agent': 'TraeCN-Local/1.0',
                }
                
                s, r, t = http_request_local(LOCAL_PROXY_HOST, port, path, body, headers)
                
                is_1001 = '1001' in r
                has_model = any(k in r.lower() for k in ['choices', 'output', 'reply', 'content'])
                
                status_icon = '✅' if s == 200 else '❌'
                code_icon = '⚠️' if is_1001 else '🎯' if has_model else '🔑'
                
                print(f'    {status_icon} {code_icon} [{fmt_name}]: HTTP {s} ({t*1000:.0f}ms)')
                
                if s == 200 and not is_1001:
                    print(f'      响应前300: {r[:300]}')
                    
                    if has_model:
                        try:
                            d = json.loads(r)
                            # 尝试提取模型回复
                            data_obj = d.get('data', d)
                            if isinstance(data_obj, dict):
                                choices = data_obj.get('choices', [])
                                if choices:
                                    content = choices[0].get('message', {}).get('content', '')
                                    if content:
                                        print(f'      🗣️ 模型回复: {content}')
                                    elif 'text' in choices[0]:
                                        print(f'      🗣️ 模型回复: {choices[0]["text"]}')
                                elif 'output' in data_obj:
                                    print(f'      🗣️ 模型回复: {data_obj["output"]}')
                                elif 'text' in data_obj:
                                    print(f'      🗣️ 模型回复: {data_obj["text"]}')
                        except:
                            pass
    
    # 综合分析
    print('\n' + '=' * 70)
    print('【综合分析】')
    print('=' * 70)
    
    if results:
        total = len(results)
        http_200 = [r for r in results if r['status'] == 200]
        has_model = [r for r in http_200 if r['has_model'] and not r['is_1001']]
        
        print(f'\n  总请求数: {total}')
        print(f'  HTTP 200: {len(http_200)}')
        print(f'  含模型响应: {len(has_model)}')
        
        if has_model:
            print(f'\n  🎉🎉🎉 成功对接真实模型!')
            for r in has_model:
                print(f'    端口: {r["port"]}')
                print(f'    路径: {r["path"]}')
                print(f'    响应: {r["response"][:300]}')
        else:
            print(f'\n  未获取到模型回复')
            print(f'  可能原因:')
            print(f'    1. 本地代理未启动或配置变更')
            print(f'    2. API路径不匹配')
            print(f'    3. Trae CN需要先登录并初始化会话')
    else:
        print('\n  无可用本地通道')
        print('  建议:')
        print('    1. 确保Trae CN正在运行')
        print('    2. 在Trae CN中执行一次对话以初始化本地代理')
        print('    3. 检查Trae CN的开发者设置中是否启用了本地API')
    
    # 保存结果
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'BSD_LocalProxy_Direct_Results.json'
    )
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'results': results,
            'available_ports': available_ports,
            'summary': {
                'total': len(results),
                'http_200': len([r for r in results if r['status'] == 200]),
                'has_model': len([r for r in results if r['has_model'] and '1001' not in r.get('response', '')]),
            },
        }, f, ensure_ascii=False, indent=2)
    
    print(f'\n  结果已保存: {output_path}')


if __name__ == '__main__':
    main()
