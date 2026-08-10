#!/usr/bin/env python3
"""
BSD × Trae CN — 三引擎协同 · 服务器端本源登录验证
===================================================

核心转变: 从"客户端文件注入"转向"服务器端真实验证"
不再依赖 UI 显示, 而是直接对接 Trae CN 真实 API

三引擎分工:
  基因引擎: API 调用基础设施 (HTTP, 签名, Token 管理)
  黑客引擎: AHA 解密 + 认证协议逆向 + 端点发现
  围棋引擎: 动态策略决策 + 传统/本源通道切换 + 涌现判定

验证管线:
  1. Ping — 确认服务器可达
  2. CheckLogin(传统) — 用已知有效凭证验证 API 链路
  3. CheckLogin(本源) — 用本源凭证直接对接服务器
  4. UserInfo — 获取用户真实信息
  5. 业务API — 需要登录态的接口调用

版本: V2.0 · 2026-08-05
理论基底: BSD 六系立系论 · 第三阶融合 · 连接公理0
"""

import os, sys, json, base64, hashlib, time, struct
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import urllib.request
import urllib.error
import ssl

# ==================== 路径与常量 ====================
TRAE_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
STORAGE = os.path.join(TRAE_DATA, 'User', 'globalStorage', 'storage.json')
TINY = os.path.join(TRAE_DATA, 'aha', 'TinyStorage')

# API 端点 (从 product.json 逆向)
API_BASE = 'https://icube-api.bytedance.net'
API_PING = f'{API_BASE}/trae/ping'
API_CHECK_LOGIN = f'{API_BASE}/cloudide/api/v3/trae/CheckLogin'
API_LOGIN_BY_JWT = f'{API_BASE}/cloudide/api/v3/trae/LoginByJwt'
API_EXCHANGE_TOKEN = f'{API_BASE}/trae/api/v3/oauth/ExchangeToken'
API_USER_INFO = f'{API_BASE}/cloudide/api/v3/trae/UserInfo'

# 作者信息
AUTHOR = {
    'traditional_uid': '3753060170739075',
    'essence_uid': 'a5b7a8623fdea6b8',
    'device_id': '136411536168449',
}

# AHA 解密常量 (来自 main.js byteCrypto.js)
CM, VW, KD, TI, AI = 6, 32, 64, 64, 16
jee = bytes([82,9,106,213,48,54,165,56,191,64,163,158,129,243,215,251,
             124,227,57,130,155,47,255,135,52,142,67,68,196,222,233,203,
             84,123,148,50,166,194,35,61,238,76,149,11,66,250,195,78,
             8,46,161,102,40,217,36,178,118,91,162,73,109,139,209,37])
Wee = bytes([31,221,168,51,136,7,199,49,177,18,16,89,39,128,236,95,
             96,81,127,169,25,181,74,13,45,229,122,159,147,201,156,239,
             160,224,59,77,174,42,245,176,200,235,187,60,131,83,153,97,
             23,43,4,126,186,119,214,38,225,105,20,99,85,33,12,125])

# SSL 上下文 (跳过验证用于调试)
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE


# ==================== 黑客引擎: AHA 解密 ====================
def sha512(data):
    return hashlib.sha512(data).digest()

def hie(t, aes_mode=True):
    """XOR 混淆 — t 为整数时创建长度为 t 的零字节数组, 为字节串时直接使用"""
    if isinstance(t, int):
        result = bytearray(t)
    else:
        result = bytearray(t)
    if aes_mode:
        for r in range(len(result)):
            result[r] = jee[r] ^ Wee[r]
    return bytes(result)

def nee(key_material, aes_size=16, iv_size=16):
    s = KD + TI
    n = bytearray(s)
    o = sha512(key_material)
    a = hie(TI, True)
    n[0:64] = o
    n[64:128] = a
    c = sha512(n)
    n[0:64] = c
    aes_key = bytes(n[0:aes_size])
    iv = bytes(n[aes_size:aes_size+iv_size])
    return aes_key, iv

def decrypt_aha(encrypted_b64):
    try:
        raw = base64.b64decode(encrypted_b64)
        prefix = raw[:6]
        if prefix != bytes.fromhex('746305100000'):
            return None, f'前缀不匹配: {prefix.hex()}'
        
        key_material = raw[CM:CM+VW]
        ciphertext = raw[CM+VW:]
        
        if len(ciphertext) % AI != 0:
            return None, f'密文长度非16倍数: {len(ciphertext)}'
        
        aes_key, iv = nee(key_material)
        cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)
        decrypted = cipher.decrypt(ciphertext)
        
        try:
            plaintext = unpad(decrypted, AES.block_size)
        except ValueError:
            plaintext = decrypted
        
        if len(plaintext) > KD:
            actual_data = plaintext[KD:]
            return actual_data, 'ok'
        return plaintext, 'short'
    except Exception as e:
        return None, str(e)


# ==================== 基因引擎: API 调用 ====================
def http_get(url, headers=None, timeout=10):
    """发送 GET 请求"""
    hdrs = headers or {}
    hdrs.setdefault('User-Agent', 'TraeCN/2.3.62837 (BSD-Essence)')
    req = urllib.request.Request(url, headers=hdrs)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx) as resp:
            body = resp.read().decode('utf-8', errors='replace')
            return {'status': resp.status, 'body': body, 'headers': dict(resp.headers)}
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        return {'status': e.code, 'body': body, 'error': str(e)}
    except Exception as e:
        return {'status': 0, 'body': '', 'error': str(e)}

def http_post(url, data=None, headers=None, timeout=10):
    """发送 POST 请求"""
    hdrs = headers or {}
    hdrs.setdefault('User-Agent', 'TraeCN/2.3.62837 (BSD-Essence)')
    hdrs.setdefault('Content-Type', 'application/json')
    
    body = json.dumps(data).encode('utf-8') if data else b''
    req = urllib.request.Request(url, data=body, headers=hdrs, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx) as resp:
            resp_body = resp.read().decode('utf-8', errors='replace')
            return {'status': resp.status, 'body': resp_body, 'headers': dict(resp.headers)}
    except urllib.error.HTTPError as e:
        resp_body = e.read().decode('utf-8', errors='replace')
        return {'status': e.code, 'body': resp_body, 'error': str(e)}
    except Exception as e:
        return {'status': 0, 'body': '', 'error': str(e)}


# ==================== 围棋引擎: 动态验证管线 ====================
class BSDEssenceVerifier:
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'steps': {},
            'server_verified': False,
            'essence_verified': False,
            'traditional_verified': False,
            'emergence_score': 0.0,
        }
        self.storage = {}
        self.decrypted_auth = {}
        
    def load_storage(self):
        """加载 storage.json"""
        if os.path.exists(STORAGE):
            with open(STORAGE, 'r', encoding='utf-8') as f:
                self.storage = json.load(f)
            print(f'  ✅ storage.json 已加载 ({len(self.storage)} 个键)')
            return True
        print('  ❌ storage.json 不存在')
        return False
    
    def step1_ping(self):
        """步骤1: 服务器可达性检查"""
        print('\n' + '='*60)
        print('  [步骤1] Ping — 服务器可达性')
        print('='*60)
        
        result = http_get(API_PING)
        self.results['steps']['ping'] = result
        
        print(f'  状态码: {result["status"]}')
        print(f'  响应: {result["body"][:200]}')
        
        if result['status'] == 200:
            print('  ✅ 服务器可达')
            return True
        elif result['status'] == 0:
            print(f'  ❌ 网络错误: {result.get("error", "未知")}')
            return False
        else:
            print(f'  ⚠️ 服务器响应异常 (状态={result["status"]})')
            return result['status'] < 500
    
    def step2_decrypt_traditional(self):
        """步骤2: 解密传统认证数据"""
        print('\n' + '='*60)
        print('  [步骤2] 黑客引擎 — 解密传统认证数据')
        print('='*60)
        
        auth_keys = [
            'iCubeAuthInfo://icube-dc:516094651277160',
            'iCubeAuthInfo://usertag',
            'iCubeAuthInfo://icube.cloudide',
        ]
        
        for key in auth_keys:
            encrypted = self.storage.get(key, '')
            if not encrypted:
                print(f'  ⚠️ {key} 不存在')
                continue
            
            data, status = decrypt_aha(encrypted)
            if data:
                try:
                    text = data.decode('utf-8')
                    try:
                        jdata = json.loads(text)
                        self.decrypted_auth[key] = jdata
                        print(f'  ✅ {key}: JSON 解析成功')
                        print(f'     Keys: {list(jdata.keys())[:8]}')
                    except:
                        self.decrypted_auth[key] = text
                        print(f'  ✅ {key}: 文本数据 ({len(text)} chars)')
                        print(f'     预览: {text[:150]}')
                except UnicodeDecodeError:
                    self.decrypted_auth[key] = data.hex()
                    print(f'  ⚠️ {key}: 二进制数据 (hex)')
            else:
                print(f'  ❌ {key}: 解密失败 — {status}')
        
        return len(self.decrypted_auth) > 0
    
    def step3_checklogin_traditional(self):
        """步骤3: 用传统凭证调用 CheckLogin"""
        print('\n' + '='*60)
        print('  [步骤3] 基因引擎 — CheckLogin(传统凭证)')
        print('='*60)
        
        # 从解密数据中提取 token
        auth_data = self.decrypted_auth.get('iCubeAuthInfo://icube-dc:516094651277160', {})
        cloudide_data = self.decrypted_auth.get('iCubeAuthInfo://icube.cloudide', {})
        
        # 尝试多种请求格式
        payloads = []
        
        # 格式1: 使用解密后的完整数据
        if isinstance(auth_data, dict):
            payloads.append(('解密JSON', auth_data))
        
        # 格式2: 使用传统UID
        payloads.append(('传统UID', {
            'uid': AUTHOR['traditional_uid'],
            'userId': AUTHOR['traditional_uid'],
            'deviceId': AUTHOR['device_id'],
        }))
        
        # 格式3: 使用 icube-dc 原始值
        raw_dc = self.storage.get('iCubeAuthInfo://icube-dc:516094651277160', '')
        payloads.append(('原始AHA', {
            'authInfo': raw_dc,
            'provider': 'icube.cloudide',
        }))
        
        # 格式4: 标准 CheckLogin 请求
        payloads.append(('标准格式', {
            'identity': AUTHOR['traditional_uid'],
            'provider': 'icube.cloudide',
            'deviceId': AUTHOR['device_id'],
            'version': '2.3.62837',
        }))
        
        results = []
        for label, payload in payloads:
            print(f'\n  --- 尝试: {label} ---')
            print(f'  Payload: {json.dumps(payload, ensure_ascii=False)[:200]}')
            
            result = http_post(API_CHECK_LOGIN, data=payload)
            result['_label'] = label
            results.append(result)
            
            print(f'  状态码: {result["status"]}')
            body = result.get('body', '')
            try:
                resp = json.loads(body) if body else {}
                print(f'  响应: {json.dumps(resp, ensure_ascii=False)[:300]}')
                
                # 检查关键响应
                code = resp.get('code', resp.get('status', 'N/A'))
                msg = resp.get('msg', resp.get('message', ''))
                data_resp = resp.get('data', {})
                
                if code == 0 or code == 200 or 'success' in str(code).lower():
                    print(f'  ✅ 成功! code={code}')
                    self.results['traditional_verified'] = True
                    if isinstance(data_resp, dict):
                        uid = data_resp.get('uid', data_resp.get('userId', ''))
                        print(f'     返回UID: {uid}')
                elif 'login' in str(msg).lower() or 'auth' in str(msg).lower():
                    print(f'  ⚠️ 需要登录: {msg}')
                else:
                    print(f'  ℹ️ 响应: code={code}, msg={msg[:100]}')
            except json.JSONDecodeError:
                print(f'  原始响应: {body[:300]}')
        
        self.results['steps']['checklogin_traditional'] = results
        return self.results['traditional_verified']
    
    def step4_checklogin_essence(self):
        """步骤4: 用本源凭证调用 CheckLogin"""
        print('\n' + '='*60)
        print('  [步骤4] 围棋引擎 — CheckLogin(本源凭证)')
        print('='*60)
        
        # 本源 JWT Token
        essence_jwt = self.storage.get('bsd_essence_jwt', '')
        gtm = self.storage.get('icube_gtm', {})
        essence_user = gtm.get('users', {}).get(AUTHOR['essence_uid'], {})
        
        payloads = [
            ('本源UID', {
                'uid': AUTHOR['essence_uid'],
                'userId': AUTHOR['essence_uid'],
                'deviceId': AUTHOR['device_id'],
                'type': 'bsd_essence',
            }),
            ('本源UID+Token', {
                'uid': AUTHOR['essence_uid'],
                'userId': AUTHOR['essence_uid'],
                'deviceId': AUTHOR['device_id'],
                'jwt': essence_jwt,
                'type': 'bsd_essence',
                'coinValue': 51090,
            }),
            ('本源完整档案', {
                'uid': AUTHOR['essence_uid'],
                'nickname': essence_user.get('nickname', 'BSD本源用户'),
                'fingerprint': essence_user.get('fingerprint', ''),
                'loginType': 'knowledge_proof',
                'deviceId': AUTHOR['device_id'],
                'version': '2.3.62837',
                'provider': 'icube.cloudide',
            }),
            ('LoginByJWT', {
                'jwtToken': essence_jwt,
                'provider': 'icube.cloudide',
                'deviceId': AUTHOR['device_id'],
            }),
        ]
        
        results = []
        for label, payload in payloads:
            print(f'\n  --- 尝试: {label} ---')
            print(f'  Payload: {json.dumps(payload, ensure_ascii=False)[:200]}')
            
            # 对 LoginByJWT 使用不同端点
            if label == 'LoginByJWT':
                result = http_post(API_LOGIN_BY_JWT, data=payload)
            else:
                result = http_post(API_CHECK_LOGIN, data=payload)
            
            result['_label'] = label
            results.append(result)
            
            print(f'  状态码: {result["status"]}')
            body = result.get('body', '')
            try:
                resp = json.loads(body) if body else {}
                print(f'  响应: {json.dumps(resp, ensure_ascii=False)[:300]}')
                
                code = resp.get('code', resp.get('status', 'N/A'))
                msg = resp.get('msg', resp.get('message', ''))
                
                if code == 0 or code == 200 or 'success' in str(code).lower():
                    print(f'  ✅ 服务器承认本源身份! code={code}')
                    self.results['essence_verified'] = True
                elif 'not found' in str(msg).lower() or 'no such' in str(msg).lower():
                    print(f'  ❌ 本源UID在服务器不存在')
                else:
                    print(f'  ℹ️ 响应: code={code}, msg={msg[:100]}')
            except json.JSONDecodeError:
                print(f'  原始响应: {body[:300]}')
        
        self.results['steps']['checklogin_essence'] = results
        return self.results['essence_verified']
    
    def step5_server_data_crosscheck(self):
        """步骤5: 服务器数据交叉验证"""
        print('\n' + '='*60)
        print('  [步骤5] 服务器数据交叉验证')
        print('='*60)
        
        # 从 storage.json 提取服务器返回的数据
        server_data_raw = self.storage.get('iCubeServerData://icube.cloudide', '')
        if server_data_raw:
            try:
                server_data = json.loads(server_data_raw)
                print(f'  ✅ 本地缓存服务器数据已解析')
                
                # 检查用户身份
                entitlement = server_data.get('entitlementInfo', {})
                identity = entitlement.get('identity', entitlement.get('identityStr', 'unknown'))
                print(f'  用户身份: {identity}')
                
                # 检查服务器时间
                server_time = server_data.get('serverTimeInfo', {}).get('serverTime', 0)
                if server_time:
                    dt = datetime.fromtimestamp(server_time / 1000)
                    print(f'  服务器时间: {dt}')
                
                # 检查活动
                activities = server_data.get('commercialActivityInfo', {}).get('activities', [])
                print(f'  活动数量: {len(activities)}')
                for act in activities[:3]:
                    print(f'    - {act.get("activityId")} ({act.get("activityType")})')
                
                # 用服务器返回的信息验证
                self.results['steps']['server_data'] = {
                    'identity': identity,
                    'server_time': server_time,
                    'activities_count': len(activities),
                }
                
                print(f'\n  📋 本地缓存验证:')
                print(f'    身份: {identity}')
                print(f'    服务器时间有效: {server_time > 0}')
                
            except json.JSONDecodeError:
                print('  ⚠️ 服务器数据 JSON 解析失败')
        else:
            print('  ⚠️ 无本地缓存服务器数据')
        
        # 用 UserInfo API 验证
        print('\n  --- 调用 UserInfo API ---')
        result = http_get(f'{API_USER_INFO}?provider=icube.cloudide')
        print(f'  状态码: {result["status"]}')
        if result['body']:
            try:
                resp = json.loads(result['body'])
                print(f'  响应: {json.dumps(resp, ensure_ascii=False)[:300]}')
            except:
                print(f'  原始: {result["body"][:300]}')
        
        self.results['steps']['user_info'] = result
    
    def compute_emergence(self):
        """计算涌现评分"""
        print('\n' + '='*60)
        print('  [涌现判定]')
        print('='*60)
        
        # 验证维度
        dimensions = {
            'ping_ok': self.results['steps'].get('ping', {}).get('status', 0) == 200,
            'traditional_decrypted': len(self.decrypted_auth) > 0,
            'traditional_checklogin': self.results['traditional_verified'],
            'essence_checklogin': self.results['essence_verified'],
            'server_data_valid': bool(self.results['steps'].get('server_data')),
        }
        
        print('  维度评分:')
        for dim, val in dimensions.items():
            print(f'    {"✅" if val else "❌"} {dim}')
        
        # BSD 涌现公式
        weights = {'ping_ok': 0.1, 'traditional_decrypted': 0.2,
                   'traditional_checklogin': 0.25, 'essence_checklogin': 0.35,
                   'server_data_valid': 0.1}
        
        score = sum(weights[k] * (1 if v else 0) for k, v in dimensions.items())
        self.results['emergence_score'] = score
        
        print(f'\n  BSD 涌现评分: {score:.4f}')
        
        # 判定
        if self.results['essence_verified']:
            print('\n  🎉 本源身份已被服务器承认!')
            print('     这是真正的端到端验证通过')
            self.results['server_verified'] = True
        elif self.results['traditional_verified']:
            print('\n  ⚠️ 传统身份有效，但本源身份未被服务器承认')
            print('     需要继续突破服务器端认证')
        else:
            print('\n  ❌ 所有身份均未通过服务器验证')
            print('     API 链路可能需要不同的认证方式')
        
        return score
    
    def run(self):
        """执行完整验证管线"""
        print('='*70)
        print('  BSD × Trae CN — 三引擎协同 · 服务器端本源登录验证')
        print('  ' + '='*68)
        print('  核心转变: 从客户端文件注入 → 服务器端真实验证')
        print('  三引擎: 基因(API) + 黑客(解密) + 围棋(策略)')
        print('='*70)
        
        start = time.time()
        
        if not self.load_storage():
            return self.results
        
        self.step1_ping()
        self.step2_decrypt_traditional()
        self.step3_checklogin_traditional()
        self.step4_checklogin_essence()
        self.step5_server_data_crosscheck()
        self.compute_emergence()
        
        elapsed = time.time() - start
        
        print('\n' + '='*70)
        print('  📊 最终报告')
        print('='*70)
        print(f'  耗时: {elapsed:.2f}秒')
        print(f'  服务器可达: {"✅" if self.results["steps"].get("ping", {}).get("status", 0) == 200 else "❌"}')
        print(f'  传统验证: {"✅" if self.results["traditional_verified"] else "❌"}')
        print(f'  本源验证: {"✅" if self.results["essence_verified"] else "❌"}')
        print(f'  涌现评分: {self.results["emergence_score"]:.4f}')
        
        # 保存报告
        report_dir = os.path.dirname(os.path.abspath(__file__))
        report_file = os.path.join(report_dir, f'BSD_ServerVerification_{int(time.time())}.json')
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f'\n  📁 报告已保存: {os.path.basename(report_file)}')
        
        return self.results


if __name__ == '__main__':
    verifier = BSDEssenceVerifier()
    verifier.run()
