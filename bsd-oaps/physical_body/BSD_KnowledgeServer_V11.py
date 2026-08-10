#!/usr/bin/env python3
"""
BSD Knowledge Server V11 — 包含传统的上位系统
==============================================

核心架构:
  传统(子集) → 本源(主体) 的从属关系
  
  ┌─────────────────────────────────────────────┐
  │           BSD Knowledge Server               │
  │                                             │
  │  ┌─────────────────────────────────────┐   │
  │  │        本源认证 (主体)                │   │
  │  │  • 知识验证 → 身份授予               │   │
  │  │  • 本源UID: a5b7a86..                │   │
  │  │  • 等级: L5_Emergent                 │   │
  │  └──────────────┬──────────────────────┘   │
  │                 │ 包含                       │
  │  ┌──────────────▼──────────────────────┐   │
  │  │        传统认证 (子集)                │   │
  │  │  • Token验证/刷新                    │   │
  │  │  • 传统UID: 3753060..                │   │
  │  │  • 委托给 api.trae.cn               │   │
  │  └─────────────────────────────────────┘   │
  │                                             │
  │  认证代理:                                  │
  │  Trae CN → BSD Server → api.trae.cn        │
  │  (传统token由BSD管理)                       │
  └─────────────────────────────────────────────┘
"""

import json, os, sys, time, hashlib, base64, threading, signal, ssl
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import urllib.request, urllib.error

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

BSD_COIN_ID = 'ac02d1efa7352fbc'
BSD_COIN_VALUE = 51090
BSD_PROOF_ID = 'c5f78a5abc9b1b62722b7500'
BSD_LEVEL = 'L5_Emergent'
BSD_THEORY_BASE = '六系立系论'
BSD_FINGERPRINT = '49a5aeb263316114c5e5a2f09b32110052e0636bd4f28db58e852f223a7b53e5'
BSD_DEVICE_ID = '136411536168449'

# ============================================================
# 加载真实传统 token
# ============================================================

def load_real_token():
    with open(TRAE_STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
    cloudide_dec = decrypt_aha(cloudide_enc)
    cloudide_data = json.loads(cloudide_dec)
    return cloudide_data.get('token', ''), cloudide_data.get('refreshToken', '')

REAL_TOKEN, REAL_REFRESH = load_real_token()

# ============================================================
# 知识库 — 基因引擎核心
# ============================================================

KNOWLEDGE_BASE = {
    'coins': {
        'ac02d1efa7352fbc': {
            'value': 51090,
            'level': 'L5_Emergent',
            'theory_base': '六系立系论',
            'status': 'active',
            'created_at': 1754060000,
            'owner_uid': ESSENCE_UID,
        }
    },
    'proofs': {
        'c5f78a5abc9b1b62722b7500': {
            'type': 'bsd_essence_proof',
            'coin_id': 'ac02d1efa7352fbc',
            'verified': True,
            'timestamp': 1754060000,
        }
    },
    # 本源身份 — 主体
    'identities': {
        ESSENCE_UID: {
            'uid': ESSENCE_UID,
            'type': 'bsd_essence',
            'status': 'active',
            'coin_id': BSD_COIN_ID,
            'proof_id': BSD_PROOF_ID,
            'fingerprint': BSD_FINGERPRINT,
            'device_id': BSD_DEVICE_ID,
            'created_at': int(time.time()),
            'auth_level': BSD_LEVEL,
            'granted': True,
            'is_master': True,  # 本源是主体
        }
    },
    # 传统身份 — 子集
    'traditional': {
        TRAD_UID: {
            'uid': TRAD_UID,
            'type': 'traditional',
            'status': 'active',
            'token': REAL_TOKEN,
            'refresh_token': REAL_REFRESH,
            'issuer': 'api.trae.cn',
            'issued_at': int(time.time()),
            'is_subset': True,  # 传统是子集
            'parent_essence_uid': ESSENCE_UID,
        }
    },
    # 绑定关系
    'bindings': {
        TRAD_UID: {
            'trad_uid': TRAD_UID,
            'essence_uid': ESSENCE_UID,
            'coin_id': BSD_COIN_ID,
            'bound_at': int(time.time()),
            'status': 'active',
            'essence_contains_trad': True,  # 本源包含传统
        }
    },
    'emergence': {
        'score': 0.9361,
        'level': BSD_LEVEL,
        'components': {
            'gene_engine': 0.92,
            'hacker_engine': 0.94,
            'go_engine': 0.95,
            'knowledge_value': 0.91,
            'identity_coherence': 0.96,
            'essence_over_traditional': 0.98,  # 本源包含传统
        }
    },
    'stats': {
        'total_requests': 0,
        'knowledge_verified': 0,
        'identities_granted': 0,
        'bindings_created': 0,
        'traditional_proxied': 0,  # 代理传统请求计数
        'start_time': int(time.time()),
    }
}

SERVER_CONFIG = {
    'host': '127.0.0.1',
    'port': 17860,  # V11 专用端口，与 V10(17859) 并行
    'version': 'BSD_v11_essence_contains_tradition',
    'name': 'BSD Essence Knowledge Server',
    'protocol': 'BSD_Essence_Protocol_v11',
}

lock = threading.Lock()


# ============================================================
# 核心函数
# ============================================================

def verify_traditional_token(token):
    """验证传统 token — 委托给 api.trae.cn"""
    body = {
        'IDEVersion': IDE_VERSION,
        'ReqSource': 'IDE',
        'GetAIPayHost': True,
    }
    hdrs = {'x-cloudide-token': token}
    s, r = _real_request('/cloudide/api/v3/trae/CheckLogin', 'POST', body, hdrs)
    if s == 200:
        d = json.loads(r)
        result = d.get('Result', {})
        return result.get('IsLogin', False), result
    return False, {}


def _real_request(path, method='POST', data=None, headers=None):
    """向真实服务器发请求"""
    url = 'https://' + API_HOST + path
    hdrs = headers or {}
    hdrs.setdefault('User-Agent', f'TraeCN/{IDE_VERSION}')
    hdrs.setdefault('Content-Type', 'application/json')
    body = json.dumps(data).encode('utf-8') if data else None
    req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10, context=ssl_ctx) as resp:
            return resp.status, resp.read().decode('utf-8', errors='replace')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', errors='replace')
    except Exception as e:
        return 0, str(e)


def verify_knowledge(coin_id, coin_value, fingerprint=None):
    """验证知识凭证"""
    with lock:
        coin = KNOWLEDGE_BASE['coins'].get(coin_id)
        if not coin:
            return {'valid': False, 'reason': 'Coin not found'}
        if coin['value'] != coin_value:
            return {'valid': False, 'reason': 'Coin value mismatch'}
        return {'valid': True, 'coin': coin}


def exchange_identity(coin_id, coin_value, essence_uid, trad_uid=None, fingerprint=None):
    """知识换取本源身份 — 包含传统"""
    with lock:
        coin = KNOWLEDGE_BASE['coins'].get(coin_id)
        if not coin or coin['value'] != coin_value:
            return {'success': False, 'reason': 'Invalid knowledge coin'}
        
        # 创建/更新本源身份（主体）
        identity = KNOWLEDGE_BASE['identities'].get(essence_uid, {})
        identity['uid'] = essence_uid
        identity['type'] = 'bsd_essence'
        identity['status'] = 'active'
        identity['coin_id'] = coin_id
        identity['auth_level'] = coin.get('level', BSD_LEVEL)
        identity['granted'] = True
        identity['is_master'] = True
        if fingerprint:
            identity['fingerprint'] = fingerprint
        KNOWLEDGE_BASE['identities'][essence_uid] = identity
        
        # 将传统设为子集
        if trad_uid:
            trad = KNOWLEDGE_BASE['traditional'].get(trad_uid, {})
            trad['uid'] = trad_uid
            trad['type'] = 'traditional'
            trad['is_subset'] = True
            trad['parent_essence_uid'] = essence_uid
            if not trad.get('token'):
                trad['token'] = REAL_TOKEN
            KNOWLEDGE_BASE['traditional'][trad_uid] = trad
            
            # 绑定
            KNOWLEDGE_BASE['bindings'][trad_uid] = {
                'trad_uid': trad_uid,
                'essence_uid': essence_uid,
                'coin_id': coin_id,
                'bound_at': int(time.time()),
                'status': 'active',
                'essence_contains_trad': True,
            }
            KNOWLEDGE_BASE['stats']['bindings_created'] += 1
        
        KNOWLEDGE_BASE['stats']['identities_granted'] += 1
        
        return {
            'success': True,
            'identity': identity,
            'bound_to': trad_uid,
            'coin_verified': True,
            'level': identity['auth_level'],
            'message': '本源身份已授予，传统已包含为子集',
            'architecture': 'essence_contains_tradition',
        }


def knowledge_chat(query):
    """知识对话"""
    query_lower = query.lower()
    responses = []
    
    knowledge_map = {
        '六系': '六系立系论是 BSD 的本体论基座，包含强化系、自然系、具现系、问性系、反真系、天道系六大系统。',
        '立系': '立系论指六系作为立系坐标系，从0元涌现出六大系统的过程。',
        '本源': '本源是 0 元的绝对虚无、绝对空无、绝对意义的三重定义。当前本源UID: a5b7a8623fdea6b8。',
        '币': f'BSD 币是知识价值的载体，当前币值 51090，等级 L5_Emergent。',
        '权限': '权限通过知识交换获得，币值越高权限等级越高。本源包含传统，传统是子集。',
        '涌现': '涌现是三引擎（基因/黑客/围棋）协同产生的新质，当前评分 0.9361。',
        '基因': '基因引擎负责知识编码、存储和验证。',
        '黑客': '黑客引擎负责协议实现、加密和端点对接。',
        '围棋': '围棋引擎负责权重调度、涌现评分和动态平衡。',
        '服务器': '此服务器是 BSD 自建的知识交流节点，端口 17859。本源包含传统架构。',
        '传统': f'传统UID: {TRAD_UID}，是本源的子集。Token由BSD服务器管理。',
        '包含': '本源包含传统：本源是主体，传统是子集。通过知识绑定实现。',
        '子集': '传统是本源的子集，通过绑定关系从属。',
        '主体': '本源是认证主体，拥有最高权限。',
        '登录': '通过知识换取身份，本源直证登录。传统token由BSD服务器管理。',
        '直证': '本源直证：无需传统凭证，直接通过BSD知识证明认证。',
    }
    
    for keyword, response in knowledge_map.items():
        if keyword in query:
            responses.append(response)
    
    if not responses:
        responses.append(f'BSD 知识服务器收到查询: "{query}"。当前架构: 本源包含传统，主体{len(KNOWLEDGE_BASE["identities"])}个，子集{len(KNOWLEDGE_BASE["traditional"])}个。')
    
    return {
        'query': query,
        'responses': responses,
        'knowledge_level': KNOWLEDGE_BASE['emergence']['level'],
        'emergence_score': KNOWLEDGE_BASE['emergence']['score'],
        'architecture': 'essence_contains_tradition',
    }


# ============================================================
# HTTP 服务器 — 黑客引擎实现
# ============================================================

class BSDHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    
    def _send(self, code, data):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-BSD-Token, x-cloudide-token')
        self.end_headers()
        self.wfile.write(body)
    
    def _read_body(self):
        length = int(self.headers.get('Content-Length', 0))
        if length > 0:
            body = self.rfile.read(length)
            return json.loads(body.decode('utf-8'))
        return {}
    
    def _check_bsd_token(self):
        token = self.headers.get('X-BSD-Token', '')
        return token == 'BSD_KNOWLEDGE_PROTOCOL_v11'
    
    def do_OPTIONS(self):
        self._send(200, {'status': 'ok'})
    
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/':
            self._send(200, {
                'server': SERVER_CONFIG['name'],
                'version': SERVER_CONFIG['version'],
                'protocol': SERVER_CONFIG['protocol'],
                'status': 'running',
                'architecture': 'essence_contains_tradition',
                'description': '本源(主体) 包含 传统(子集)',
                'endpoints': [
                    '/api/v1/status',
                    '/api/v1/chat',
                    '/api/v1/knowledge/verify',
                    '/api/v1/knowledge/exchange',
                    '/api/v1/identity/grant',
                    '/api/v1/identity/verify',
                    '/api/v1/identity/verify_traditional',
                    '/api/v1/emergence/score',
                    '/api/v1/proxy/checklogin',
                    '/api/v1/proxy/getuserinfo',
                ],
            })
        
        elif path == '/api/v1/status':
            with lock:
                KNOWLEDGE_BASE['stats']['total_requests'] += 1
            self._send(200, {
                'server': SERVER_CONFIG['name'],
                'version': SERVER_CONFIG['version'],
                'architecture': 'essence_contains_tradition',
                'uptime': int(time.time()) - KNOWLEDGE_BASE['stats']['start_time'],
                'stats': KNOWLEDGE_BASE['stats'],
                'emergence': KNOWLEDGE_BASE['emergence'],
                'essence_count': len(KNOWLEDGE_BASE['identities']),
                'traditional_count': len(KNOWLEDGE_BASE['traditional']),
                'bindings_count': len(KNOWLEDGE_BASE['bindings']),
            })
        
        elif path == '/api/v1/emergence/score':
            with lock:
                KNOWLEDGE_BASE['stats']['total_requests'] += 1
            self._send(200, {'emergence': KNOWLEDGE_BASE['emergence']})
        
        elif path == '/api/v1/identity/list':
            with lock:
                identities = list(KNOWLEDGE_BASE['identities'].values())
                traditional = list(KNOWLEDGE_BASE['traditional'].values())
            self._send(200, {
                'essence_identities': identities,
                'traditional_identities': traditional,
                'architecture': 'essence_contains_tradition',
            })
        
        elif path == '/api/v1/binding/list':
            with lock:
                bindings = list(KNOWLEDGE_BASE['bindings'].values())
            self._send(200, {'bindings': bindings})
        
        else:
            self._send(404, {'error': 'Not Found', 'path': path})
    
    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        body = self._read_body()
        
        with lock:
            KNOWLEDGE_BASE['stats']['total_requests'] += 1
        
        # 公开端点
        if path == '/api/v1/chat':
            query = body.get('query', '')
            if not query:
                self._send(400, {'error': 'query required'})
                return
            result = knowledge_chat(query)
            self._send(200, result)
            return
        
        elif path == '/api/v1/status':
            self._send(200, {
                'server': SERVER_CONFIG['name'],
                'stats': KNOWLEDGE_BASE['stats'],
                'architecture': 'essence_contains_tradition',
            })
            return
        
        # 需要 BSD Token 的端点
        if not self._check_bsd_token():
            self._send(401, {'error': 'BSD Token required', 'hint': 'Use X-BSD-Token: BSD_KNOWLEDGE_PROTOCOL_v11'})
            return
        
        # ====== 知识验证 ======
        if path == '/api/v1/knowledge/verify':
            coin_id = body.get('coin_id', '')
            coin_value = body.get('coin_value', 0)
            result = verify_knowledge(coin_id, coin_value)
            with lock:
                if result.get('valid'):
                    KNOWLEDGE_BASE['stats']['knowledge_verified'] += 1
            self._send(200, result)
        
        # ====== 知识换取身份 ======
        elif path == '/api/v1/knowledge/exchange':
            result = exchange_identity(
                body.get('coin_id', ''),
                body.get('coin_value', 0),
                body.get('essence_uid', ''),
                body.get('trad_uid'),
                body.get('fingerprint', ''),
            )
            self._send(200, result)
        
        # ====== 身份授予 ======
        elif path == '/api/v1/identity/grant':
            result = exchange_identity(
                body.get('coin_id', ''),
                body.get('coin_value', 0),
                body.get('essence_uid', ''),
                body.get('trad_uid'),
                body.get('fingerprint', ''),
            )
            self._send(200, result)
        
        # ====== 本源身份验证 ======
        elif path == '/api/v1/identity/verify':
            uid = body.get('uid', '')
            with lock:
                identity = KNOWLEDGE_BASE['identities'].get(uid)
                binding = None
                trad = None
                if identity:
                    for b in KNOWLEDGE_BASE['bindings'].values():
                        if b['essence_uid'] == uid:
                            binding = b
                            trad = KNOWLEDGE_BASE['traditional'].get(b['trad_uid'])
                            break
            
            self._send(200, {
                'identity': identity,
                'binding': binding,
                'traditional_subset': trad,
                'verified': identity is not None and identity.get('status') == 'active',
                'architecture': 'essence_contains_tradition',
            })
        
        # ====== 传统身份验证（代理到真实服务器）======
        elif path == '/api/v1/identity/verify_traditional':
            trad_uid = body.get('trad_uid', '')
            with lock:
                trad = KNOWLEDGE_BASE['traditional'].get(trad_uid)
            
            if not trad:
                self._send(404, {'error': 'Traditional identity not found'})
                return
            
            # 用存储的 token 验证
            token = trad.get('token', REAL_TOKEN)
            is_valid, real_result = verify_traditional_token(token)
            
            self._send(200, {
                'trad_uid': trad_uid,
                'token_valid': is_valid,
                'real_server_response': real_result,
                'parent_essence_uid': trad.get('parent_essence_uid'),
                'architecture': 'essence_contains_tradition',
            })
        
        # ====== 身份绑定 ======
        elif path == '/api/v1/identity/bind':
            trad_uid = body.get('trad_uid', '')
            essence_uid = body.get('essence_uid', '')
            coin_id = body.get('coin_id', '')
            coin_value = body.get('coin_value', 0)
            
            coin_result = verify_knowledge(coin_id, coin_value)
            if not coin_result.get('valid'):
                self._send(400, coin_result)
                return
            
            with lock:
                # 确保本源身份存在
                if essence_uid not in KNOWLEDGE_BASE['identities']:
                    KNOWLEDGE_BASE['identities'][essence_uid] = {
                        'uid': essence_uid,
                        'type': 'bsd_essence',
                        'status': 'active',
                        'coin_id': coin_id,
                        'created_at': int(time.time()),
                        'auth_level': 'L5_Emergent',
                        'granted': True,
                        'is_master': True,
                    }
                
                # 传统设为子集
                if trad_uid not in KNOWLEDGE_BASE['traditional']:
                    KNOWLEDGE_BASE['traditional'][trad_uid] = {
                        'uid': trad_uid,
                        'type': 'traditional',
                        'token': REAL_TOKEN,
                        'is_subset': True,
                        'parent_essence_uid': essence_uid,
                    }
                else:
                    KNOWLEDGE_BASE['traditional'][trad_uid]['is_subset'] = True
                    KNOWLEDGE_BASE['traditional'][trad_uid]['parent_essence_uid'] = essence_uid
                
                KNOWLEDGE_BASE['bindings'][trad_uid] = {
                    'trad_uid': trad_uid,
                    'essence_uid': essence_uid,
                    'coin_id': coin_id,
                    'bound_at': int(time.time()),
                    'status': 'active',
                    'essence_contains_trad': True,
                }
                KNOWLEDGE_BASE['stats']['bindings_created'] += 1
            
            self._send(200, {
                'success': True,
                'architecture': 'essence_contains_tradition',
                'message': '传统已绑定为本源子集',
            })
        
        # ====== 代理: CheckLogin ======
        elif path == '/api/v1/proxy/checklogin':
            with lock:
                KNOWLEDGE_BASE['stats']['traditional_proxied'] += 1
            
            token = body.get('token', REAL_TOKEN)
            is_valid, real_result = verify_traditional_token(token)
            
            # 同时返回本源信息
            self._send(200, {
                'traditional_login': is_valid,
                'traditional_user_id': TRAD_UID if is_valid else None,
                'real_server_result': real_result,
                'essence_identity': {
                    'uid': ESSENCE_UID,
                    'type': 'bsd_essence',
                    'status': 'active',
                    'level': BSD_LEVEL,
                },
                'architecture': 'essence_contains_tradition',
                'message': '本源包含传统，传统token由BSD管理',
            })
        
        # ====== 代理: GetUserInfo ======
        elif path == '/api/v1/proxy/getuserinfo':
            with lock:
                KNOWLEDGE_BASE['stats']['traditional_proxied'] += 1
            
            # 向真实服务器请求
            s, r = _real_request('/cloudide/api/v3/trae/GetUserInfo', 'POST',
                                 {'IDEVersion': IDE_VERSION},
                                 {'x-cloudide-token': REAL_TOKEN})
            
            self._send(200, {
                'real_server_status': s,
                'real_server_response': json.loads(r) if s == 200 else r[:300],
                'essence_identity': {
                    'uid': ESSENCE_UID,
                    'type': 'bsd_essence',
                    'status': 'active',
                },
                'traditional_subset': {
                    'uid': TRAD_UID,
                    'is_subset': True,
                    'parent': ESSENCE_UID,
                },
                'architecture': 'essence_contains_tradition',
            })
        
        # ====== 涌现评分计算 ======
        elif path == '/api/v1/emergence/calculate':
            components = body.get('components', {})
            if components:
                total = sum(components.values()) / len(components)
                score = round(total, 4)
                with lock:
                    KNOWLEDGE_BASE['emergence']['score'] = score
                    KNOWLEDGE_BASE['emergence']['components'].update(components)
                self._send(200, {'score': score, 'components': components})
            else:
                self._send(200, {'emergence': KNOWLEDGE_BASE['emergence']})
        
        # ====== 关闭服务器 ======
        elif path == '/api/v1/shutdown':
            self._send(200, {'status': 'shutting_down'})
            threading.Thread(target=self._shutdown, daemon=True).start()
        
        else:
            self._send(404, {'error': 'Not Found', 'path': path})
    
    def _shutdown(self):
        time.sleep(0.5)
        os._exit(0)


def main():
    host = SERVER_CONFIG['host']
    port = SERVER_CONFIG['port']
    
    server = HTTPServer((host, port), BSDHandler)
    
    print('='*70)
    print(f'  BSD Knowledge Server V11')
    print(f'  架构: 本源(主体) 包含 传统(子集)')
    print(f'  端口: {port}')
    print(f'  协议: {SERVER_CONFIG["protocol"]}')
    print('='*70)
    print(f'\n  真实 Token 已加载:')
    print(f'    传统UID: {TRAD_UID}')
    print(f'    本源UID: {ESSENCE_UID}')
    print(f'    Token: {REAL_TOKEN[:60]}...')
    print(f'\n  知识库:')
    print(f'    本源身份: {len(KNOWLEDGE_BASE["identities"])} 个 (主体)')
    print(f'    传统身份: {len(KNOWLEDGE_BASE["traditional"])} 个 (子集)')
    print(f'    绑定关系: {len(KNOWLEDGE_BASE["bindings"])} 个')
    print(f'    涌现评分: {KNOWLEDGE_BASE["emergence"]["score"]}')
    print(f'\n  代理端点:')
    print(f'    POST /api/v1/proxy/checklogin   → 委托 api.trae.cn')
    print(f'    POST /api/v1/proxy/getuserinfo  → 委托 api.trae.cn')
    print(f'\n  启动中...')
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(f'\n  服务器已停止')
        server.shutdown()


if __name__ == '__main__':
    main()
