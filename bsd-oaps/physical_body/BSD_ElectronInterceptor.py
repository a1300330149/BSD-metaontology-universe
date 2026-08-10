#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD Electron层API拦截器 — 直接在Trae CN客户端中捕获真实请求
==============================================================

原理:
  1. 启动Trae CN客户端并启用远程调试端口
  2. 通过Chrome DevTools Protocol连接到客户端
  3. 注入JS代码拦截所有fetch/XMLHttpRequest请求
  4. 捕获真实的API请求格式和参数
  
  这是基因引擎的终极形态:
  直接从活体中提取基因，而不是猜测基因
"""

import os, sys, json, time, subprocess, signal
from datetime import datetime
from pathlib import Path

# Trae CN客户端路径
TRAE_CN_PATH = r'C:\Users\13003\AppData\Local\Programs\Trae CN\Trae CN.exe'
DEBUG_PORT = 9222
CAPTURE_FILE = os.path.join(os.path.dirname(__file__), 'trae_api_capture.json')

# 注入脚本 - 拦截所有fetch和XMLHttpRequest
INJECT_SCRIPT = '''
// BSD API请求拦截器
window.__BSD_CAPTURED_REQUESTS = [];
window.__BSD_CAPTURED_RESPONSES = [];

// 拦截fetch
const originalFetch = window.fetch;
window.fetch = async function(...args) {
    const [url, options] = args;
    const urlStr = typeof url === 'string' ? url : url.url;
    
    // 只捕获API请求
    if (urlStr && (urlStr.includes('trae-api') || urlStr.includes('llm') || urlStr.includes('chat'))) {
        const captured = {
            type: 'fetch',
            url: urlStr,
            method: options?.method || 'GET',
            headers: options?.headers || {},
            body: options?.body ? (typeof options.body === 'string' ? options.body : '[FormData/Blob]') : null,
            timestamp: Date.now()
        };
        window.__BSD_CAPTURED_REQUESTS.push(captured);
        
        // 尝试解析body
        if (captured.body && captured.body.startsWith('{')) {
            try {
                captured.body_parsed = JSON.parse(captured.body);
            } catch(e) {}
        }
    }
    
    // 发送请求
    const response = await originalFetch.apply(this, args);
    
    // 捕获响应
    if (urlStr && (urlStr.includes('trae-api') || urlStr.includes('llm') || urlStr.includes('chat'))) {
        const responseClone = response.clone();
        try {
            const bodyText = await responseClone.text();
            window.__BSD_CAPTURED_RESPONSES.push({
                url: urlStr,
                status: response.status,
                statusText: response.statusText,
                headers: Object.fromEntries(response.headers.entries()),
                body: bodyText.substring(0, 500),
                timestamp: Date.now()
            });
        } catch(e) {}
    }
    
    return response;
};

// 拦截XMLHttpRequest
const originalXHROpen = XMLHttpRequest.prototype.open;
const originalXHRSend = XMLHttpRequest.prototype.send;

XMLHttpRequest.prototype.open = function(method, url, ...rest) {
    this.__bsd_url = url;
    this.__bsd_method = method;
    return originalXHROpen.apply(this, [method, url, ...rest]);
};

XMLHttpRequest.prototype.send = function(body) {
    const url = this.__bsd_url || '';
    if (url.includes('trae-api') || url.includes('llm') || url.includes('chat')) {
        window.__BSD_CAPTURED_REQUESTS.push({
            type: 'xhr',
            url: url,
            method: this.__bsd_method || 'POST',
            body: body ? (typeof body === 'string' ? body : '[FormData/Blob]') : null,
            timestamp: Date.now()
        });
        
        // 监听响应
        this.addEventListener('load', function() {
            window.__BSD_CAPTURED_RESPONSES.push({
                url: url,
                status: this.status,
                statusText: this.statusText,
                body: this.responseText ? this.responseText.substring(0, 500) : '',
                timestamp: Date.now()
            });
        });
    }
    return originalXHRSend.apply(this, [body]);
};

'BSD API拦截器已激活';
'''

def launch_trae_with_debug():
    """启动Trae CN并启用远程调试"""
    print('\n' + '='*70)
    print('  启动Trae CN客户端 (调试模式)')
    print('='*70)
    
    # 检查Trae CN是否已在运行
    result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq "Trae CN.exe"'], 
                          capture_output=True, text=True)
    
    if 'Trae CN.exe' in result.stdout:
        print('  ⚠️ Trae CN已在运行，需要先关闭')
        print('  正在关闭现有进程...')
        subprocess.run(['taskkill', '/F', '/IM', 'Trae CN.exe'], capture_output=True)
        time.sleep(2)
    
    # 启动Trae CN
    print(f'  启动: {TRAE_CN_PATH}')
    proc = subprocess.Popen([
        TRAE_CN_PATH,
        f'--remote-debugging-port={DEBUG_PORT}',
        '--user-data-dir=C:\\Temp\\trae_debug_profile'  # 使用独立的用户数据目录
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print(f'  进程ID: {proc.pid}')
    print(f'  调试端口: {DEBUG_PORT}')
    print(f'  等待启动...')
    time.sleep(5)
    
    return proc

def capture_via_cdp():
    """通过CDP捕获API请求"""
    print('\n' + '='*70)
    print('  捕获API请求')
    print('='*70)
    
    import urllib.request
    
    # 获取可用的targets
    try:
        targets_url = f'http://localhost:{DEBUG_PORT}/json'
        with urllib.request.urlopen(targets_url) as resp:
            targets = json.loads(resp.read())
        
        print(f'  可用目标: {len(targets)}')
        for t in targets:
            print(f'    [{t.get("type", "?")}] {t.get("title", "?")}')
            print(f'      URL: {t.get("url", "?")[:100]}')
            print(f'      ID: {t.get("id", "?")}')
        
        # 找到主窗口
        main_target = None
        for t in targets:
            if t.get('type') == 'page' and t.get('url', '').startswith('trae'):
                main_target = t
                break
        
        if not main_target and targets:
            main_target = targets[0]
        
        if main_target:
            print(f'\n  选择目标: {main_target.get("title", main_target.get("url", "?"))}')
            
            # 注入脚本
            ws_url = main_target.get('webSocketDebuggerUrl')
            if ws_url:
                print(f'  WebSocket URL: {ws_url}')
                print(f'  提示: 可通过Chrome DevTools连接查看')
                print(f'        chrome://inspect/#devices')
                
                # 保存捕获信息
                capture_info = {
                    'timestamp': datetime.now().isoformat(),
                    'target': {
                        'title': main_target.get('title'),
                        'url': main_target.get('url'),
                        'id': main_target.get('id'),
                        'wsUrl': ws_url
                    },
                    'allTargets': targets,
                    'injectionScript': INJECT_SCRIPT
                }
                
                with open(CAPTURE_FILE, 'w', encoding='utf-8') as f:
                    json.dump(capture_info, f, ensure_ascii=False, indent=2)
                
                print(f'\n  ✅ 捕获信息已保存: {CAPTURE_FILE}')
                print(f'  📋 下一步操作:')
                print(f'    1. 在Chrome中打开 chrome://inspect')
                print(f'    2. 点击"Configure..."添加 localhost:{DEBUG_PORT}')
                print(f'    3. 点击"inspect"连接Trae CN')
                print(f'    4. 在控制台执行注入脚本')
                print(f'    5. 在Trae CN中发送一条消息')
                print(f'    6. 查看捕获的请求')
        
    except Exception as e:
        print(f'  ❌ 连接失败: {e}')
        print(f'  请确保Trae CN已正确启动')

def generate_injection_code():
    """生成可复制的注入代码"""
    print('\n' + '='*70)
    print('  BSD API注入代码 (复制到Chrome控制台执行)')
    print('='*70)
    
    code = '''
// ====== BSD Trae CN API拦截器 ======
// 在Chrome DevTools控制台中执行此代码

// 1. 先注入拦截器
''' + INJECT_SCRIPT + '''

// 2. 然后在Trae CN中发送一条消息

// 3. 最后执行以下命令查看捕获的请求:
// window.__BSD_CAPTURED_REQUESTS  - 所有捕获的请求
// window.__BSD_CAPTURED_RESPONSES - 所有捕获的响应
// JSON.stringify(window.__BSD_CAPTURED_REQUESTS, null, 2)  - 格式化输出

// 4. 导出捕获数据:
// copy(JSON.stringify({requests: window.__BSD_CAPTURED_REQUESTS, responses: window.__BSD_CAPTURED_RESPONSES}, null, 2))
'''
    
    print(code)
    print('='*70)


def main():
    print('\n' + '#'*70)
    print('  # BSD Electron层API拦截器')
    print('#'*70)
    print(f'  时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'  目标: 捕获Trae CN客户端的真实API请求')
    print('#'*70)
    
    # 启动Trae CN
    proc = launch_trae_with_debug()
    
    try:
        # 捕获CDP信息
        capture_via_cdp()
        
        # 生成注入代码
        generate_injection_code()
        
        print('\n' + '#'*70)
        print('  # 操作指南')
        print('#'*70)
        print('  1. 打开Chrome浏览器')
        print('  2. 访问 chrome://inspect')
        print(f'  3. 点击"Configure..."添加 localhost:{DEBUG_PORT}')
        print('  4. 等待Trae CN出现在列表中')
        print('  5. 点击"inspect"打开DevTools')
        print('  6. 在Console标签页粘贴注入代码')
        print('  7. 在Trae CN中发送一条测试消息')
        print('  8. 执行 window.__BSD_CAPTURED_REQUESTS 查看捕获结果')
        print('  9. 将捕获结果保存到文件进行分析')
        print('#'*70)
        
        # 保持运行
        print('\n  Trae CN正在运行中...')
        print('  按Ctrl+C退出')
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print('\n  正在关闭...')
    
    finally:
        # 清理
        proc.terminate()
        print('  Trae CN已关闭')


if __name__ == '__main__':
    main()
