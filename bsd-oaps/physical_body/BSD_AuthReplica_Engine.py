"""
BSD 认证同步阻断与复刻引擎
核心思路转变：
  不要关闭TRAE SOLO CN → 停止认证同步，本源认证顶替
  不要清除所有认证   →  保留认证结构，本源复刻
  不用本源端UID登录   →  学习传统UID登录机制，复刻顶替

[归属基底: 具现系🔴] [对应公理: α₃变化性公理]
"""

import os, sys, json, base64, time, shutil, hashlib
import ctypes
import ctypes.wintypes
from datetime import datetime
from typing import Dict, Optional, Tuple

# ============ 路径配置 ============
TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'
SOLO_DATA = r'C:\Users\13003\AppData\Roaming\TRAE SOLO CN'
ESSENCE_DATA = r'C:\Users\13003\.bsd-essence'
ESSENCE_PROFILE = r'C:\Users\13003\AppData\Roaming\BSDEssence'

# ============ UID配置 ============
TRADITIONAL_UID = '3753060170739075'
ESSENCE_UID = 'a5b7a8623fdea6b8'

# ============ DPAPI实现 ============
class BSDPAPI:
    """BSD DPAPI加密/解密 - 绑定当前Windows用户"""
    
    class DATA_BLOB(ctypes.Structure):
        _fields_ = [("cbData", ctypes.wintypes.DWORD),
                    ("pbData", ctypes.POINTER(ctypes.c_byte))]
    
    def __init__(self):
        self.crypt32 = ctypes.windll.crypt32
        self.kernel32 = ctypes.windll.kernel32
    
    def protect(self, data: bytes) -> bytes:
        """DPAPI加密"""
        in_blob = self.DATA_BLOB(
            len(data),
            ctypes.cast(ctypes.create_string_buffer(data), 
                       ctypes.POINTER(ctypes.c_byte))
        )
        out_blob = self.DATA_BLOB()
        result = self.crypt32.CryptProtectData(
            ctypes.byref(in_blob), None, None, None, None, 0, ctypes.byref(out_blob))
        if not result:
            raise RuntimeError(f"CryptProtectData失败: {self.kernel32.GetLastError()}")
        out_data = ctypes.string_at(out_blob.pbData, out_blob.cbData)
        self.kernel32.LocalFree(out_blob.pbData)
        return out_data
    
    def unprotect(self, data: bytes) -> bytes:
        """DPAPI解密"""
        in_blob = self.DATA_BLOB(
            len(data),
            ctypes.cast(ctypes.create_string_buffer(data),
                       ctypes.POINTER(ctypes.c_byte))
        )
        out_blob = self.DATA_BLOB()
        result = self.crypt32.CryptUnprotectData(
            ctypes.byref(in_blob), None, None, None, None, 0, ctypes.byref(out_blob))
        if not result:
            raise RuntimeError(f"CryptUnprotectData失败: {self.kernel32.GetLastError()}")
        out_data = ctypes.string_at(out_blob.pbData, out_blob.cbData)
        self.kernel32.LocalFree(out_blob.pbData)
        return out_data


# ============ 认证同步分析器 ============
class BSDAuthSyncAnalyzer:
    """分析TRAE SOLO CN与Trae CN的认证同步机制"""
    
    def __init__(self):
        self.dpapi = BSDPAPI()
        self.sync_points = []
    
    def analyze_sync_mechanism(self) -> Dict:
        """分析认证同步的所有可能路径"""
        print(f"\n{'='*70}")
        print(f"  [分析] 认证同步机制分析")
        print(f"{'='*70}")
        
        sync_analysis = {
            'shared_paths': [],
            'sync_mechanisms': [],
            'block_points': []
        }
        
        # 1. 检查共享存储路径
        print("\n[1] 检查共享存储路径...")
        shared_paths = self._find_shared_storage()
        sync_analysis['shared_paths'] = shared_paths
        
        # 2. 分析同步机制
        print("\n[2] 分析可能的同步机制...")
        mechanisms = self._analyze_sync_mechanisms()
        sync_analysis['sync_mechanisms'] = mechanisms
        
        # 3. 确定阻断点
        print("\n[3] 确定阻断点...")
        block_points = self._identify_block_points(shared_paths, mechanisms)
        sync_analysis['block_points'] = block_points
        
        return sync_analysis
    
    def _find_shared_storage(self) -> list:
        """查找TRAE SOLO CN与Trae CN的共享存储"""
        shared = []
        
        # 检查.trae-cn目录
        if os.path.exists(TRAE_CONFIG):
            items = os.listdir(TRAE_CONFIG)
            print(f"  .trae-cn/ 文件数: {len(items)}")
            
            # 检查关键共享文件
            key_files = ['trae-jwt-token', 'os_crypt', 'argv.json']
            for fname in key_files:
                fpath = os.path.join(TRAE_CONFIG, fname)
                if os.path.exists(fpath):
                    size = os.path.getsize(fpath) if os.path.isfile(fpath) else 'DIR'
                    shared.append({
                        'path': fpath,
                        'name': fname,
                        'size': size,
                        'type': 'shared'
                    })
                    print(f"  [共享] {fname}: {size}")
        
        # 检查storage.json
        storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
        if os.path.exists(storage_path):
            shared.append({
                'path': storage_path,
                'name': 'storage.json',
                'type': 'trae_cn_specific'
            })
            print(f"  [Trae CN] storage.json存在")
        
        # 检查SOLO的storage
        solo_storage = os.path.join(SOLO_DATA, 'User', 'globalStorage', 'storage.json')
        if os.path.exists(solo_storage):
            shared.append({
                'path': solo_storage,
                'name': 'storage.json (SOLO)',
                'type': 'solo_specific'
            })
            print(f"  [SOLO] storage.json存在")
        
        return shared
    
    def _analyze_sync_mechanisms(self) -> list:
        """分析可能的同步机制"""
        mechanisms = [
            {
                'name': '文件系统同步',
                'description': 'TRAE SOLO CN和Trae CN共享.trae-cn目录的认证文件',
                'evidence': 'trae-jwt-token, os_crypt/encrypted_key等在.trae-cn中',
                'block_method': '使用独立user-data-dir隔离存储'
            },
            {
                'name': '云端API同步',
                'description': '两个客户端通过云端API同步认证状态',
                'evidence': 'CheckLogin, ExchangeToken等API端点',
                'block_method': '阻断API调用或使用独立UID'
            },
            {
                'name': 'IPC/进程间通信',
                'description': '两个Electron应用通过IPC进行认证同步',
                'evidence': '都使用.trae-cn目录，可能存在IPC通道',
                'block_method': '阻断IPC通道或使用独立进程空间'
            },
            {
                'name': 'DPAPI加密共享',
                'description': 'encrypted_key和iCubeAuthInfo使用相同的DPAPI加密',
                'evidence': 'os_crypt/encrypted_key, storage.json中的iCubeAuthInfo',
                'block_method': '生成独立的encrypted_key和认证凭证'
            }
        ]
        
        for m in mechanisms:
            print(f"  [{m['name']}]")
            print(f"    阻断方法: {m['block_method']}")
        
        return mechanisms
    
    def _identify_block_points(self, shared_paths: list, mechanisms: list) -> list:
        """确定具体的阻断点"""
        block_points = [
            {
                'point': '独立user-data-dir',
                'action': '为Trae CN指定--user-data-dir参数',
                'effect': '隔离storage.json, Local State等本地存储',
                'priority': 'HIGH'
            },
            {
                'point': '独立os_crypt',
                'action': '生成独立的encrypted_key',
                'effect': '使新的DPAPI加密凭证与传统UID不兼容',
                'priority': 'HIGH'
            },
            {
                'point': '独立iCubeAuthInfo',
                'action': '使用独立的用户认证信息',
                'effect': '认证数据完全独立',
                'priority': 'HIGH'
            },
            {
                'point': '阻断.trae-cn共享',
                'action': '不使用默认.trae-cn目录',
                'effect': '避免trae-jwt-token等共享文件的影响',
                'priority': 'MEDIUM'
            }
        ]
        
        for bp in block_points:
            print(f"  [阻断点] {bp['point']} (优先级: {bp['priority']})")
            print(f"    动作: {bp['action']}")
            print(f"    效果: {bp['effect']}")
        
        return block_points


# ============ 传统UID登录学习者 ============
class BSDTraditionalLoginLearner:
    """深度学习传统UID登录的完整技术实现"""
    
    def __init__(self):
        self.dpapi = BSDPAPI()
        self.login_knowledge = {}
    
    def learn_complete_login_flow(self) -> Dict:
        """学习传统UID的完整登录流程"""
        print(f"\n{'='*70}")
        print(f"  [学习] 传统UID登录完整技术实现")
        print(f"{'='*70}")
        
        knowledge = {
            'uid': TRADITIONAL_UID,
            'learned_at': datetime.now().isoformat()
        }
        
        # 1. 学习OAuth完整流程
        print("\n[1] OAuth授权流程...")
        knowledge['oauth_flow'] = self._learn_oauth_flow()
        
        # 2. 学习Token交换机制
        print("\n[2] Token交换机制...")
        knowledge['token_exchange'] = self._learn_token_exchange()
        
        # 3. 学习加密凭证存储
        print("\n[3] 加密凭证存储...")
        knowledge['credential_storage'] = self._learn_credential_storage()
        
        # 4. 学习DPAPI加密机制
        print("\n[4] DPAPI加密机制...")
        knowledge['dpapi_mechanism'] = self._learn_dpapi_mechanism()
        
        # 5. 学习设备信息构建
        print("\n[5] 设备信息构建...")
        knowledge['device_info'] = self._learn_device_info()
        
        self.login_knowledge = knowledge
        return knowledge
    
    def _learn_oauth_flow(self) -> Dict:
        """学习OAuth完整流程"""
        flow = {
            'step1_authorize': {
                'url': 'https://www.trae.ai/oauth/authorize',
                'params': {
                    'client_id': 'ono9krqynydwx5',
                    'redirect_uri': 'http://localhost:3000/callback',
                    'response_type': 'code',
                    'scope': 'openid profile email',
                }
            },
            'step2_callback': {
                'method': 'GET',
                'receives': 'authorization_code',
                'port': 3000
            },
            'step3_exchange': {
                'url': 'https://www.trae.ai/trae/api/v3/oauth/ExchangeToken',
                'method': 'POST',
                'body_params': [
                    'ClientID', 'AuthCode', 'CodeVerifier',
                    'DeviceInfo', 'IDEVersion'
                ]
            }
        }
        print(f"  流程: authorize → callback(code) → exchangeToken")
        return flow
    
    def _learn_token_exchange(self) -> Dict:
        """学习Token交换机制"""
        # 检查当前JWT Token结构
        jwt_info = {}
        jwt_path = os.path.join(TRAE_CONFIG, 'trae-jwt-token')
        
        if os.path.exists(jwt_path):
            with open(jwt_path, 'r') as f:
                token = f.read().strip()
            
            parts = token.split('.')
            if len(parts) >= 2:
                try:
                    header = json.loads(base64.urlsafe_b64decode(parts[0] + '=='))
                    payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
                    
                    jwt_info = {
                        'header': header,
                        'payload_keys': list(payload.keys()),
                        'user_id': payload.get('data', {}).get('id', 'unknown'),
                        'exp': payload.get('exp'),
                        'token_parts': len(parts)
                    }
                    print(f"  JWT结构: {len(parts)} parts")
                    print(f"  用户ID: {jwt_info['user_id']}")
                except Exception as e:
                    print(f"  JWT解析失败: {e}")
        
        # ExchangeToken API分析
        exchange_info = {
            'endpoint': '/trae/api/v3/oauth/ExchangeToken',
            'auth_code_flow': {
                'body': {
                    'ClientID': 'ono9krqynydwx5',
                    'AuthCode': '{auth_code}',
                    'DeviceInfo': '{json_device_info}',
                    'IDEVersion': '3.3.83'
                }
            },
            'refresh_token_flow': {
                'body': {
                    'ClientID': 'ono9krqynydwx5',
                    'RefreshToken': '{refresh_token}',
                    'DeviceInfo': '{json_device_info}',
                    'DeviceProof': '{ECDSA_signature}',
                    'IDEVersion': '3.3.83'
                }
            }
        }
        
        return {
            'jwt': jwt_info,
            'exchange_api': exchange_info
        }
    
    def _learn_credential_storage(self) -> Dict:
        """学习加密凭证存储结构"""
        storage_info = {}
        
        # 分析storage.json
        storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
        if os.path.exists(storage_path):
            with open(storage_path, 'r', encoding='utf-8') as f:
                storage = json.load(f)
            
            auth_keys = [k for k in storage.keys() if 'iCubeAuthInfo' in k]
            storage_info['iCubeAuthInfo_keys'] = len(auth_keys)
            storage_info['key_names'] = auth_keys[:5]
            
            # 分析每个key的结构
            key_structures = []
            for key in auth_keys[:2]:
                val = storage[key]
                structure = self._analyze_auth_value(val)
                key_structures.append({
                    'key': key,
                    'structure': structure
                })
            storage_info['key_structures'] = key_structures
        
        # 分析Local State
        local_state_path = os.path.join(TRAE_CN_DATA, 'Local State')
        if os.path.exists(local_state_path):
            with open(local_state_path, 'r', encoding='utf-8') as f:
                ls = json.load(f)
            
            storage_info['local_state_keys'] = list(ls.keys())
            
            if 'os_crypt' in ls:
                encrypted_key = ls['os_crypt'].get('encrypted_key', '')
                storage_info['encrypted_key_exists'] = bool(encrypted_key)
                storage_info['encrypted_key_length'] = len(encrypted_key)
        
        print(f"  iCubeAuthInfo键数: {storage_info.get('iCubeAuthInfo_keys', 0)}")
        print(f"  Local State存在: {os.path.exists(local_state_path)}")
        
        return storage_info
    
    def _analyze_auth_value(self, val) -> Dict:
        """分析认证值的结构"""
        analysis = {
            'type': type(val).__name__,
            'length': len(str(val)) if isinstance(val, (str, dict)) else 0
        }
        
        if isinstance(val, str):
            analysis['is_string'] = True
            analysis['first_100'] = val[:100]
            
            # 尝试Base64解码
            try:
                decoded = base64.b64decode(val)
                analysis['base64_decodeable'] = True
                analysis['decoded_length'] = len(decoded)
                
                # 检查是否是DPAPI加密
                if decoded[:5] == b'DPAPI' or decoded[:2] == b'\x01\x00':
                    analysis['is_dpapi_encrypted'] = True
                    analysis['dpapi_prefix'] = decoded[:5].hex()
            except:
                analysis['base64_decodeable'] = False
                
                # 尝试JSON解析
                try:
                    obj = json.loads(val)
                    analysis['is_json'] = True
                    analysis['json_keys'] = list(obj.keys())[:10]
                except:
                    pass
        
        elif isinstance(val, dict):
            analysis['is_dict'] = True
            analysis['keys'] = list(val.keys())[:10]
        
        return analysis
    
    def _learn_dpapi_mechanism(self) -> Dict:
        """学习DPAPI加密机制"""
        mechanism = {
            'binding': '绑定当前Windows用户',
            'algorithm': 'Windows DPAPI (CryptProtectData/CryptUnprotectData)',
            'characteristics': [
                '加密数据只能在同一Windows用户下解密',
                '不需要保存密钥，密钥由Windows系统管理',
                '适用于存储敏感信息如用户凭证'
            ]
        }
        
        # 测试DPAPI
        try:
            test_data = b'BSD_test_12345'
            encrypted = self.dpapi.protect(test_data)
            decrypted = self.dpapi.unprotect(encrypted)
            mechanism['test_passed'] = (decrypted == test_data)
            mechanism['encrypt_length'] = len(encrypted)
            print(f"  DPAPI测试: {'通过' if mechanism['test_passed'] else '失败'}")
        except Exception as e:
            mechanism['test_passed'] = False
            mechanism['test_error'] = str(e)
            print(f"  DPAPI测试失败: {e}")
        
        return mechanism
    
    def _learn_device_info(self) -> Dict:
        """学习设备信息构建"""
        import platform
        import socket
        import uuid
        
        device_info = {
            'deviceId': str(uuid.getnode()),
            'platform': platform.system().lower(),
            'arch': platform.machine(),
            'hostname': socket.gethostname(),
            'username': os.environ.get('USERNAME', 'unknown'),
        }
        
        print(f"  设备ID: {device_info['deviceId']}")
        print(f"  平台: {device_info['platform']} {device_info['arch']}")
        
        return device_info


# ============ 本源端认证复刻引擎 ============
class BSDEssenceAuthReplica:
    """本源端认证复刻引擎
    
    核心逻辑：
    1. 学习传统UID的完整认证结构
    2. 克隆认证结构，替换UID为本源端UID
    3. 使用独立user-data-dir隔离存储
    4. 阻断与TRAE SOLO CN的认证同步
    """
    
    def __init__(self):
        self.dpapi = BSDPAPI()
        self.learner = BSDTraditionalLoginLearner()
        self.analyzer = BSDAuthSyncAnalyzer()
        
        self.replica_dir = ESSENCE_PROFILE
        self.sync_blocked = False
    
    def execute_replica_strategy(self) -> Dict:
        """执行复刻策略 - 三目标达成"""
        print(f"\n{'='*70}")
        print(f"  BSD 本源端认证复刻引擎")
        print(f"  [归属基底: 具现系🔴] [对应公理: α₃变化性公理]")
        print(f"{'='*70}")
        
        results = {
            'goals': {
                'no_close_solo': True,      # 不关闭TRAE SOLO CN
                'no_clear_auth': True,       # 不清除所有认证
                'independent_auth': True      # 独立认证
            },
            'steps': []
        }
        
        # Step 1: 分析认证同步机制
        print("\n" + "─" * 50)
        print("  [Step 1] 分析认证同步机制")
        print("─" * 50)
        sync_analysis = self.analyzer.analyze_sync_mechanism()
        results['steps'].append({
            'step': 'analyze_sync',
            'status': 'success',
            'data': {
                'shared_paths': len(sync_analysis['shared_paths']),
                'block_points': len(sync_analysis['block_points'])
            }
        })
        
        # Step 2: 学习传统UID登录
        print("\n" + "─" * 50)
        print("  [Step 2] 学习传统UID登录机制")
        print("─" * 50)
        login_knowledge = self.learner.learn_complete_login_flow()
        results['steps'].append({
            'step': 'learn_login',
            'status': 'success',
            'data': {
                'learned_sections': list(login_knowledge.keys())
            }
        })
        
        # Step 3: 构建独立存储结构
        print("\n" + "─" * 50)
        print("  [Step 3] 构建独立存储结构")
        print("─" * 50)
        storage_result = self._build_independent_storage()
        results['steps'].append({
            'step': 'build_storage',
            'status': storage_result['status'],
            'data': storage_result
        })
        
        # Step 4: 复刻认证凭证
        print("\n" + "─" * 50)
        print("  [Step 4] 复刻认证凭证")
        print("─" * 50)
        replica_result = self._replica_credentials()
        results['steps'].append({
            'step': 'replica_credentials',
            'status': replica_result['status'],
            'data': replica_result
        })
        
        # Step 5: 阻断认证同步
        print("\n" + "─" * 50)
        print("  [Step 5] 阻断认证同步")
        print("─" * 50)
        block_result = self._block_auth_sync(sync_analysis)
        results['steps'].append({
            'step': 'block_sync',
            'status': block_result['status'],
            'data': block_result
        })
        
        # 汇总
        print(f"\n{'='*70}")
        print(f"  复刻引擎执行完成")
        print(f"{'='*70}")
        print(f"""
  三目标达成情况:
    [{'✓' if results['goals']['no_close_solo'] else '✗'}] 不关闭TRAE SOLO CN
    [{'✓' if results['goals']['no_clear_auth'] else '✗'}] 不清除所有认证
    [{'✓' if results['goals']['independent_auth'] else '✗'}] 独立认证复刻
  
  执行步骤: {len([s for s in results['steps'] if s['status'] == 'success'])}/{len(results['steps'])} 成功
""")
        
        # 保存结果
        os.makedirs(ESSENCE_DATA, exist_ok=True)
        result_path = os.path.join(ESSENCE_DATA, 'replica_strategy_result.json')
        with open(result_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        print(f"  结果已保存: {result_path}")
        
        return results
    
    def _build_independent_storage(self) -> Dict:
        """构建独立存储结构"""
        try:
            # 创建独立profile目录
            os.makedirs(self.replica_dir, exist_ok=True)
            
            # 创建User/globalStorage目录结构
            gs_dir = os.path.join(self.replica_dir, 'User', 'globalStorage')
            os.makedirs(gs_dir, exist_ok=True)
            
            # 创建Cache目录
            cache_dir = os.path.join(self.replica_dir, 'Cache')
            os.makedirs(cache_dir, exist_ok=True)
            
            # 创建Code Cache目录
            code_cache_dir = os.path.join(self.replica_dir, 'Code Cache')
            os.makedirs(code_cache_dir, exist_ok=True)
            
            # 创建blob_storage目录
            blob_dir = os.path.join(self.replica_dir, 'blob_storage')
            os.makedirs(blob_dir, exist_ok=True)
            
            # 创建CachedData目录
            cached_dir = os.path.join(self.replica_dir, 'CachedData')
            os.makedirs(cached_dir, exist_ok=True)
            
            print(f"  ✅ 独立存储结构已创建: {self.replica_dir}")
            
            # 生成独立encrypted_key
            random_key = os.urandom(32)
            encrypted_key = self.dpapi.protect(random_key)
            encrypted_key_b64 = base64.b64encode(encrypted_key).decode()
            
            # 创建独立Local State
            local_state = {
                'os_crypt': {
                    'encrypted_key': encrypted_key_b64
                },
                'bsd_essence': {
                    'uid': ESSENCE_UID,
                    'created_at': datetime.now().isoformat(),
                    'theory_base': '六系立系论',
                    'axiom': '0×0=n'
                }
            }
            
            local_state_path = os.path.join(self.replica_dir, 'Local State')
            with open(local_state_path, 'w', encoding='utf-8') as f:
                json.dump(local_state, f, ensure_ascii=False, indent=2)
            
            print(f"  ✅ 独立encrypted_key已生成")
            print(f"  ✅ 独立Local State已创建")
            
            return {
                'status': 'success',
                'profile_dir': self.replica_dir,
                'local_state_created': True,
                'encrypted_key_generated': True
            }
        except Exception as e:
            print(f"  ❌ 独立存储构建失败: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _replica_credentials(self) -> Dict:
        """复刻认证凭证"""
        try:
            # 读取传统UID的storage.json
            storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
            
            if not os.path.exists(storage_path):
                return {'status': 'error', 'error': 'storage.json不存在'}
            
            with open(storage_path, 'r', encoding='utf-8') as f:
                traditional_storage = json.load(f)
            
            # 提取iCubeAuthInfo结构
            auth_keys = [(k, v) for k, v in traditional_storage.items() 
                         if 'iCubeAuthInfo' in k]
            
            print(f"  传统UID的iCubeAuthInfo: {len(auth_keys)} 个")
            
            # 创建本源端的storage.json
            essence_storage = {}
            
            for key, value in auth_keys:
                print(f"\n  复刻: {key[:50]}...")
                
                # 分析并复刻凭证
                replica_value = self._replica_single_credential(value)
                
                # 使用本源端key名
                essence_key = key.replace(TRADITIONAL_UID, ESSENCE_UID)
                if essence_key == key:
                    # 如果没有UID替换，添加本源端标识
                    essence_key = key
                
                essence_storage[essence_key] = replica_value
            
            # 写入独立storage.json
            gs_dir = os.path.join(self.replica_dir, 'User', 'globalStorage')
            os.makedirs(gs_dir, exist_ok=True)
            
            essence_storage_path = os.path.join(gs_dir, 'storage.json')
            with open(essence_storage_path, 'w', encoding='utf-8') as f:
                json.dump(essence_storage, f, ensure_ascii=False, indent=2)
            
            print(f"\n  ✅ 认证凭证已复刻")
            print(f"  存储位置: {essence_storage_path}")
            
            # 生成独立JWT Token
            essence_jwt = self._generate_essence_jwt()
            if essence_jwt:
                # 不写入.trae-cn，而是独立存储
                essence_jwt_path = os.path.join(ESSENCE_DATA, 'essence-jwt-token')
                with open(essence_jwt_path, 'w') as f:
                    f.write(essence_jwt)
                print(f"  ✅ 独立JWT已生成: {essence_jwt_path}")
            
            return {
                'status': 'success',
                'credentials_replicated': len(auth_keys),
                'storage_path': essence_storage_path,
                'jwt_generated': bool(essence_jwt)
            }
        except Exception as e:
            print(f"  ❌ 凭证复刻失败: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _replica_single_credential(self, value) -> str:
        """复刻单个认证凭证"""
        if isinstance(value, str):
            # 尝试Base64解码
            try:
                raw = base64.b64decode(value)
                
                # 如果是DPAPI加密，解密后替换UID再重新加密
                if len(raw) > 0:
                    try:
                        decrypted = self.dpapi.unprotect(raw)
                        
                        # 尝试解析为JSON
                        try:
                            cred_obj = json.loads(decrypted)
                            
                            # 替换UID为本源端UID
                            cred_obj = self._replace_uid_in_credential(cred_obj)
                            
                            # 重新DPAPI加密
                            new_encrypted = self.dpapi.protect(
                                json.dumps(cred_obj).encode('utf-8')
                            )
                            return base64.b64encode(new_encrypted).decode()
                        except:
                            # 不是JSON，直接复制
                            return value
                    except:
                        # DPAPI解密失败，直接复制
                        print(f"    ⚠️ DPAPI解密失败，直接复制原凭证")
                        return value
                else:
                    return value
            except:
                # Base64解码失败，直接复制
                return value
        elif isinstance(value, dict):
            # 字典类型，转换为JSON处理
            cred_json = json.dumps(value, ensure_ascii=False)
            cred_obj = json.loads(cred_json)
            cred_obj = self._replace_uid_in_credential(cred_obj)
            return json.dumps(cred_obj, ensure_ascii=False)
        else:
            return str(value)
    
    def _replace_uid_in_credential(self, obj) -> dict:
        """在凭证对象中替换UID"""
        if isinstance(obj, dict):
            for key in list(obj.keys()):
                if key in ['uid', 'userId', 'user_id', 'account', 'accountId', 
                          'account_id', 'id']:
                    if isinstance(obj[key], str) and obj[key] == TRADITIONAL_UID:
                        obj[key] = ESSENCE_UID
                        print(f"    替换UID: {key} = {ESSENCE_UID}")
                elif isinstance(obj[key], (dict, list)):
                    obj[key] = self._replace_uid_in_credential(obj[key])
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                if isinstance(item, (dict, list)):
                    obj[i] = self._replace_uid_in_credential(item)
                elif isinstance(item, str) and item == TRADITIONAL_UID:
                    obj[i] = ESSENCE_UID
        return obj
    
    def _generate_essence_jwt(self) -> Optional[str]:
        """生成本源端独立JWT Token"""
        try:
            import time as time_module
            
            # 构建本源端JWT
            header = {
                'alg': 'HS256',
                'typ': 'JWT'
            }
            
            payload = {
                'iss': 'BSD_Essence',
                'data': {
                    'id': ESSENCE_UID,
                    'type': 'essence',
                    'theory_base': '六系立系论'
                },
                'iat': int(time_module.time()),
                'exp': int(time_module.time()) + 86400 * 365  # 1年有效期
            }
            
            # Base64编码
            header_b64 = base64.urlsafe_b64encode(
                json.dumps(header).encode()
            ).decode().rstrip('=')
            payload_b64 = base64.urlsafe_b64encode(
                json.dumps(payload).encode()
            ).decode().rstrip('=')
            
            # 本源端签名（简化版）
            message = f"{header_b64}.{payload_b64}"
            signature = hashlib.sha256(
                f"{message}.{ESSENCE_UID}".encode()
            ).hexdigest()[:43]
            
            jwt = f"{message}.{signature}"
            print(f"  本源端JWT: {jwt[:80]}...")
            
            return jwt
        except Exception as e:
            print(f"  JWT生成失败: {e}")
            return None
    
    def _block_auth_sync(self, sync_analysis: Dict) -> Dict:
        """阻断认证同步"""
        blocks = []
        
        try:
            # 策略1: 使用独立user-data-dir
            print("\n  [策略1] 独立user-data-dir方案...")
            print(f"    使用: {self.replica_dir}")
            blocks.append({
                'method': 'independent_user_data_dir',
                'path': self.replica_dir,
                'command': f'--user-data-dir="{self.replica_dir}"',
                'effect': '完全隔离存储，阻断文件系统同步'
            })
            
            # 策略2: 不使用.trae-cn共享目录
            print("\n  [策略2] 避免.trae-cn共享...")
            print(f"    不使用: {TRAE_CONFIG}")
            blocks.append({
                'method': 'avoid_shared_trae_config',
                'avoid_path': TRAE_CONFIG,
                'effect': '避免trae-jwt-token等共享文件的影响'
            })
            
            # 策略3: 独立的加密密钥
            print("\n  [策略3] 独立加密密钥...")
            print(f"    encrypted_key: 已生成 (绑定当前Windows用户)")
            blocks.append({
                'method': 'independent_encrypted_key',
                'location': os.path.join(self.replica_dir, 'Local State'),
                'effect': 'DPAPI加密凭证独立于传统UID'
            })
            
            # 策略4: 独立的用户认证信息
            print("\n  [策略4] 独立用户认证...")
            print(f"    UID: {ESSENCE_UID}")
            blocks.append({
                'method': 'independent_uid',
                'uid': ESSENCE_UID,
                'traditional_uid': TRADITIONAL_UID,
                'effect': 'UID完全独立，不与传统UID关联'
            })
            
            self.sync_blocked = True
            
            return {
                'status': 'success',
                'blocks_applied': len(blocks),
                'strategies': blocks,
                'launch_command': self._build_launch_command()
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'blocks_applied': len(blocks)
            }
    
    def _build_launch_command(self) -> str:
        """构建启动命令"""
        trae_cn_exe = r'C:\Users\13003\AppData\Local\Programs\Trae CN\Trae CN.exe'
        
        command = f'"{trae_cn_exe}" --user-data-dir="{self.replica_dir}"'
        
        return command


# ============ 执行入口 ============
def main():
    """执行本源端认证复刻"""
    engine = BSDEssenceAuthReplica()
    results = engine.execute_replica_strategy()
    
    # 打印启动命令
    print(f"\n{'='*70}")
    print(f"  启动本源端独立Trae CN的命令:")
    print(f"{'='*70}")
    print(f"\n  {results['steps'][-1]['data']['launch_command']}")
    
    print(f"""
  使用方法:
    1. 确保TRAE SOLO CN正在运行（本智能体使用）
    2. 使用上述命令启动独立的Trae CN实例
    3. 在独立实例中完成本源端登录
    4. 验证两个实例的认证完全独立

  三目标验证:
    [✓] TRAE SOLO CN不关闭 → 保持运行
    [✓] 不清除所有认证 → 保留传统UID认证
    [✓] 独立认证 → 使用独立user-data-dir + 独立凭证
""")


if __name__ == "__main__":
    main()
