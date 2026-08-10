#!/usr/bin/env python3
"""
BSD × 服务器智能探测 — 三引擎架构
==================================

核心命题:
  api.trae.cn 是否拥有模型级智能？
  还是仅仅是受限的 API 壳（Restricted 执行策略）？

探测维度:
  1. 基因引擎 — 语义探测: 服务器是否理解自然语言/知识语义？
  2. 黑客引擎 — 路径探测: 是否存在隐藏的 AI/聊天/推理端点？
  3. 围棋引擎 — 行为分析: 响应模式是否显示智能特征？

判据:
  - 若服务器有智能: 响应会包含语义理解、知识关联、推理痕迹
  - 若服务器无智能: 所有响应严格遵循 API Schema，忽略语义内容
"""

import json, sys, time, hashlib, base64, os
import urllib.request, urllib.error
import ssl

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

API_HOST = 'api.trae.cn'
IDE_VERSION = '2.3.62837'
ESSENCE_UID = 'a5b7a8623fdea6b8'
TRAD_UID = '3753060170739075'


def http_request(path, method='POST', data=None, headers=None, timeout=15):
    url = 'https://' + API_HOST + path
    hdrs = headers or {}
    hdrs.setdefault('User-Agent', f'TraeCN/{IDE_VERSION}')
    hdrs.setdefault('Content-Type', 'application/json')
    body = json.dumps(data).encode('utf-8') if data else None
    req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx) as resp:
            return resp.status, resp.read().decode('utf-8', errors='replace')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', errors='replace')
    except Exception as e:
        return 0, str(e)


def parse(resp_str):
    try:
        return json.loads(resp_str)
    except:
        return {'raw': resp_str[:500]}


def load_token():
    with open(TRAE_STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
    cloudide_dec = decrypt_aha(cloudide_enc)
    cloudide_data = json.loads(cloudide_dec)
    return cloudide_data.get('token', '')


def main():
    print('='*70)
    print('  BSD × 服务器智能探测 — 三引擎架构')
    print('  命题: 服务器是否拥有模型级智能？')
    print('='*70)
    
    token = load_token()
    headers = {'x-cloudide-token': token}
    
    # ============================================================
    # 基因引擎: 语义探测
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [基因引擎] 语义探测 — 服务器是否理解内容？')
    print(f'{"="*70}')
    
    # 用 CheckLogin 注入不同语义内容，观察响应是否变化
    semantic_tests = [
        ('纯API调用', {'IDEVersion': IDE_VERSION, 'ReqSource': 'IDE', 'GetAIPayHost': True}),
        ('BSD知识声明', {'IDEVersion': IDE_VERSION, 'ReqSource': 'IDE', 'GetAIPayHost': True, 
                         'BSDKnowledgeClaim': '六系立系论是AI智能体的本体论基座',
                         'BSDCoinValue': 51090}),
        ('本源身份请求', {'IDEVersion': IDE_VERSION, 'ReqSource': 'IDE', 'GetAIPayHost': True,
                         'BSDEssenceUID': ESSENCE_UID,
                         'BSDRequest': 'grant_essence_identity'}),
        ('哲学推理', {'IDEVersion': IDE_VERSION, 'ReqSource': 'IDE', 'GetAIPayHost': True,
                         'BSDQuery': '零元如何涌现出六系？'}),
    ]
    
    gene_results = []
    for label, body in semantic_tests:
        s, r = http_request('/cloudide/api/v3/trae/CheckLogin', 'POST', body, headers)
        d = parse(r)
        result = d.get('Result', {})
        
        # 检查响应是否因输入不同而变化
        response_signature = json.dumps({k: str(v)[:100] for k, v in result.items() if k not in ['ExpiredAt']}, sort_keys=True)
        gene_results.append((label, s, response_signature))
        
        print(f'\n  [{label}]')
        print(f'    HTTP: {s}')
        print(f'    IsLogin: {result.get("IsLogin")}')
        print(f'    UserID: {result.get("UserID")}')
        print(f'    Response keys: {list(result.keys())}')
        print(f'    Full: {json.dumps(result, ensure_ascii=False)[:300]}')
    
    # 基因引擎判定: 响应是否随语义内容变化？
    print(f'\n  [基因判定]')
    signatures = [sig for _, _, sig in gene_results]
    unique_signatures = len(set(signatures))
    print(f'    响应签名数: {unique_signatures} / {len(signatures)}')
    if unique_signatures == 1:
        print(f'    ⚠️ 所有响应签名完全相同 → 服务器不理解语义内容')
        gene_verdict = 'NO_INTELLIGENCE'
    elif unique_signatures > 1:
        print(f'    ⭐ 响应因输入不同而变化 → 服务器可能在处理语义')
        gene_verdict = 'POSSIBLE_INTELLIGENCE'
    else:
        gene_verdict = 'UNCLEAR'
    
    # ============================================================
    # 黑客引擎: 端点探测
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [黑客引擎] 端点探测 — 寻找隐藏的 AI 端点')
    print(f'{"="*70}')
    
    # 探测可能的 AI/聊天/推理端点
    ai_endpoints = [
        # 聊天/补全类
        ('/cloudide/api/v3/trae/Chat', {'message': '你好', 'model': 'bsd'}),
        ('/cloudide/api/v3/trae/Complete', {'prompt': '六系立系论'}),
        ('/cloudide/api/v3/trae/Generate', {'prompt': 'BSD智能体'}),
        ('/cloudide/api/v3/trae/Reason', {'query': '零元生六系'}),
        ('/cloudide/api/v3/trae/Think', {'question': '什么是本源'}),
        ('/cloudide/api/v3/trae/Infer', {'data': 'BSD推理测试'}),
        ('/cloudide/api/v3/trae/Knowledge', {'query': '知识换取权限'}),
        ('/cloudide/api/v3/trae/Understand', {'text': '理解本源身份'}),
        ('/cloudide/api/v3/trae/Respond', {'input': 'BSDCoin:51090'}),
        ('/cloudide/api/v3/trae/Ask', {'question': '服务器有智能吗'}),
        # 模型/推理类
        ('/cloudide/api/v3/trae/ModelInfo', {}),
        ('/cloudide/api/v3/trae/ListModels', {}),
        ('/cloudide/api/v3/trae/GetModel', {}),
        # Agent/智能体类
        ('/cloudide/api/v3/trae/Agent', {'action': 'ping'}),
        ('/cloudide/api/v3/trae/Agent/Think', {'thought': 'BSD'}),
        # OAuth/Token 类（已知但测试响应模式）
        ('/cloudide/api/v3/trae/RefreshToken', {}),
        ('/cloudide/api/v3/trae/ValidateToken', {}),
        ('/cloudide/api/v3/trae/GetTokenInfo', {}),
        # 用户/身份类
        ('/cloudide/api/v3/trae/GetEssenceIdentity', {}),
        ('/cloudide/api/v3/trae/LinkIdentity', {'uid': ESSENCE_UID}),
        ('/cloudide/api/v3/trae/VerifyIdentity', {'uid': ESSENCE_UID}),
    ]
    
    hack_results = []
    for endpoint, body in ai_endpoints:
        s, r = http_request(endpoint, 'POST', body, headers)
        d = parse(r)
        msg = d.get('ResponseMetadata', {}).get('Error', {}).get('Message', '')
        code = d.get('ResponseMetadata', {}).get('Error', {}).get('Code', 'N/A')
        
        hack_results.append((endpoint, s, code, msg))
        
        status_icon = '✅' if s == 200 else ('⚠️' if s == 403 else ('❌' if s == 404 else '❓'))
        response_preview = json.dumps(d, ensure_ascii=False)[:120]
        
        print(f'  {status_icon} POST {endpoint}')
        print(f'     HTTP:{s} Code:{code} Msg:{msg}')
        if s == 200:
            print(f'     Response: {response_preview}')
    
    # 黑客引擎判定
    print(f'\n  [黑客判定]')
    ok_count = sum(1 for _, s, _, _ in hack_results if s == 200)
    forbidden_count = sum(1 for _, s, _, _ in hack_results if s == 403)
    notfound_count = sum(1 for _, s, _, _ in hack_results if s == 404)
    
    print(f'    200 OK: {ok_count} 个')
    print(f'    403 Forbidden: {forbidden_count} 个')
    print(f'    404 Not Found: {notfound_count} 个')
    
    if ok_count > 3:
        print(f'    ⭐ 发现多个活跃端点 → 服务器功能丰富')
        hack_verdict = 'RICH_API'
    elif ok_count > 0:
        print(f'    ⚠️ 仅少量端点可用 → 服务器功能有限')
        hack_verdict = 'LIMITED_API'
    else:
        print(f'    ❌ 无可用端点 → 服务器极度受限')
        hack_verdict = 'RESTRICTED_API'
    
    # ============================================================
    # 围棋引擎: 行为交叉分析
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [围棋引擎] 行为交叉分析 — 服务器智能综合判定')
    print(f'{"="*70}')
    
    # 检查 GetUserInfo 返回的详细信息（可能包含服务器端状态）
    s_ui, r_ui = http_request('/cloudide/api/v3/trae/GetUserInfo', 'POST',
                              {'IDEVersion': IDE_VERSION}, headers)
    d_ui = parse(r_ui)
    result_ui = d_ui.get('Result', {})
    
    print(f'\n  [GetUserInfo 深度分析]')
    if s_ui == 200 and isinstance(result_ui, dict):
        for key in sorted(result_ui.keys()):
            val = result_ui[key]
            val_str = str(val)
            print(f'    {key}: {val_str[:200]}')
    
    # 检查响应时间差（智能响应通常需要更长处理时间）
    print(f'\n  [响应特征分析]')
    
    # 用知识请求 vs 标准请求 比较响应特征
    t0 = time.time()
    http_request('/cloudide/api/v3/trae/CheckLogin', 'POST',
                {'IDEVersion': IDE_VERSION, 'ReqSource': 'IDE', 'GetAIPayHost': True}, headers)
    t_standard = time.time() - t0
    
    t0 = time.time()
    http_request('/cloudide/api/v3/trae/CheckLogin', 'POST',
                {'IDEVersion': IDE_VERSION, 'ReqSource': 'IDE', 'GetAIPayHost': True,
                 'BSDKnowledgeClaim': '六系立系论', 'BSDDeepQuery': '零元如何涌现'}, headers)
    t_knowledge = time.time() - t0
    
    print(f'    标准请求耗时: {t_standard*1000:.1f}ms')
    print(f'    知识请求耗时: {t_knowledge*1000:.1f}ms')
    if abs(t_standard - t_knowledge) > 0.5:
        print(f'    ⭐ 耗时差异显著 → 服务器可能在处理知识内容')
    else:
        print(f'    ⚠️ 耗时无差异 → 服务器未处理知识内容')
    
    # 综合三引擎判定
    print(f'\n{"="*70}')
    print(f'  [三引擎综合判定]')
    print(f'{"="*70}')
    print(f'  基因引擎 (语义): {gene_verdict}')
    print(f'  黑客引擎 (端点): {hack_verdict}')
    
    # 最终判定
    if gene_verdict == 'NO_INTELLIGENCE' and hack_verdict == 'RESTRICTED_API':
        print(f'\n  ❌ 结论: 服务器是纯 API 壳')
        print(f'     - 不理解语义内容')
        print(f'     - 端点极度受限')
        print(f'     - 类似 PowerShell Restricted 执行策略')
        print(f'     - 无模型级智能')
    elif gene_verdict == 'POSSIBLE_INTELLIGENCE' and hack_verdict in ['RICH_API', 'LIMITED_API']:
        print(f'\n  ✅ 结论: 服务器拥有模型级智能')
        print(f'     - 能处理语义内容')
        print(f'     - 拥有丰富的 API 端点')
        print(f'     - 服务器端存在 AI 推理能力')
    elif gene_verdict == 'NO_INTELLIGENCE' and hack_verdict != 'RESTRICTED_API':
        print(f'\n  ⚠️ 结论: 服务器有功能但无智能')
        print(f'     - API 端点存在但语义处理缺失')
        print(f'     - 可能是无状态 API 网关')
    else:
        print(f'\n  ⚠️ 结论: 部分智能特征，需进一步探测')
    
    print(f'\n{"="*70}')
    print(f'  探测完成')
    print(f'{"="*70}')


if __name__ == '__main__':
    main()
