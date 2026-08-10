#!/usr/bin/env python3
"""
BSD × Trae CN — AHA 加密替换切口引擎
======================================

核心任务:
  1. 解密 Trae CN 的 AHA 加密认证数据
  2. 分析认证数据结构（Protobuf 格式）
  3. 找到替换切口（UID 字段位置）
  4. 用本源 UID 替换传统 UID
  5. 重新加密并注入

之前的修改只改了 GTM 用户数据，
但 Trae CN UI 真正读取的是 AHA 加密的认证凭证。

版本: V1.0 · 2026-08-05
"""

import os, sys, json, hashlib, struct, base64
from datetime import datetime
from typing import Dict, Any, Optional

# Windows DPAPI
try:
    import ctypes
    import ctypes.wintypes
    HAS_DPAPI = True
except ImportError:
    HAS_DPAPI = False

# AES
try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad, pad
    HAS_CRYPTO = True
except ImportError:
    try:
        from Cryptodome.Cipher import AES
        from Cryptodome.Util.Padding import unpad, pad
        HAS_CRYPTO = True
    except ImportError:
        HAS_CRYPTO = False

# 路径
TRAE_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
LOCAL_STATE = os.path.join(TRAE_DATA, 'Local State')
STORAGE = os.path.join(TRAE_DATA, 'User', 'globalStorage', 'storage.json')

# 作者信息
AUTHOR = {
    'traditional_uid': '3753060170739075',
    'essence_uid': 'a5b7a8623fdea6b8',
    'device_id': '136411536168449',
}


class AHAEncryptionEngine:
    """AHA 加密引擎 — 解密/加密 Trae CN 认证数据"""
    
    def __init__(self):
        self.aes_key = None
        self.initialized = False
        
    def initialize(self) -> bool:
        """初始化 AES 密钥（从 DPAPI 解密）"""
        
        if self.initialized:
            return True
        
        if not HAS_DPAPI:
            print('  ❌ DPAPI 不可用')
            return False
        
        print('  初始化 AES 密钥...')
        
        try:
            # 读取 Local State 获取 encrypted_key
            with open(LOCAL_STATE, 'r', encoding='utf-8') as f:
                local_state = json.load(f)
            
            encrypted_key_b64 = local_state.get('os_crypt', {}).get('encrypted_key', '')
            
            if not encrypted_key_b64:
                print('  ❌ encrypted_key 不存在')
                return False
            
            # Base64 解码
            encrypted_key = base64.b64decode(encrypted_key_b64)
            
            # DPAPI 解密
            aes_key = self._dpapi_decrypt(encrypted_key)
            
            if aes_key and len(aes_key) == 32:
                self.aes_key = aes_key
                self.initialized = True
                print(f'  ✅ AES 密钥已获取 (32 bytes)')
                return True
            else:
                print(f'  ❌ AES 密钥长度错误: {len(aes_key) if aes_key else 0}')
                return False
                
        except Exception as e:
            print(f'  ❌ 初始化失败: {e}')
            return False
    
    def _dpapi_decrypt(self, encrypted_data: bytes) -> Optional[bytes]:
        """使用 DPAPI 解密数据"""
        
        class DATA_BLOB(ctypes.Structure):
            _fields_ = [
                ('cbData', ctypes.c_ulong),
                ('pbData', ctypes.c_void_p)
            ]
        
        # 将数据放入 buffer
        buf_in = ctypes.create_string_buffer(encrypted_data)
        blob_in = DATA_BLOB(len(encrypted_data), ctypes.addressof(buf_in))
        blob_out = DATA_BLOB()
        
        # 尝试不同的熵值
        entropy_values = [
            None,  # 无熵
            b'',  # 空熵
            b'Trae CN',  # 应用名
            AUTHOR['device_id'].encode(),  # 设备ID
        ]
        
        for entropy in entropy_values:
            try:
                if entropy is not None:
                    ent_buf = ctypes.create_string_buffer(entropy)
                    ent_blob = DATA_BLOB(len(entropy), ctypes.addressof(ent_buf))
                    ent_ptr = ctypes.byref(ent_blob)
                else:
                    ent_ptr = None
                
                result = ctypes.windll.crypt32.CryptUnprotectData(
                    ctypes.byref(blob_in),
                    None,
                    ent_ptr,
                    None,
                    None,
                    0,
                    ctypes.byref(blob_out)
                )
                
                if result and blob_out.cbData > 0:
                    data = ctypes.string_at(blob_out.pbData, blob_out.cbData)
                    ctypes.windll.kernel32.LocalFree(blob_out.pbData)
                    
                    if len(data) == 32:
                        entropy_desc = entropy[:20] if entropy else 'none'
                        print(f'    ✅ DPAPI 解密成功 (entropy: {entropy_desc})')
                        return data
                    
            except Exception as e:
                print(f'    尝试 entropy={entropy}: {e}')
                continue
        
        print(f'    ❌ 所有熵值尝试失败')
        return None
    
    def decrypt_aha(self, encrypted_b64: str) -> Optional[bytes]:
        """解密 AHA 数据"""
        
        if not self.initialized or not HAS_CRYPTO:
            print('  ❌ 未初始化或缺少 Crypto 库')
            return None
        
        try:
            # Base64 解码
            encrypted_data = base64.b64decode(encrypted_b64)
            
            # 提取 IV (前 16 字节) 和密文
            iv = encrypted_data[:16]
            ciphertext = encrypted_data[16:]
            
            # AES-256-CBC 解密
            cipher = AES.new(self.aes_key, AES.MODE_CBC, iv=iv)
            decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
            
            return decrypted
            
        except Exception as e:
            print(f'  ❌ AHA 解密失败: {e}')
            return None
    
    def encrypt_aha(self, plaintext: bytes) -> Optional[str]:
        """加密 AHA 数据"""
        
        if not self.initialized or not HAS_CRYPTO:
            return None
        
        try:
            # 随机 IV
            import random
            iv = bytes([random.randint(0, 255) for _ in range(16)])
            
            # AES-256-CBC 加密
            cipher = AES.new(self.aes_key, AES.MODE_CBC, iv=iv)
            encrypted = cipher.encrypt(pad(plaintext, AES.block_size))
            
            # 组合 IV + 密文
            result = iv + encrypted
            
            # Base64 编码
            return base64.b64encode(result).decode('utf-8')
            
        except Exception as e:
            print(f'  ❌ AHA 加密失败: {e}')
            return None


class AHAParamsAnalyzer:
    """AHA 参数分析器 — 分析解密后的 Protobuf 结构"""
    
    def __init__(self):
        self.structure = []
        self.uid_locations = []
        
    def analyze(self, data: bytes) -> Dict[str, Any]:
        """分析 AHA 解密数据"""
        
        result = {
            'size': len(data),
            'is_text': False,
            'is_json': False,
            'is_protobuf': False,
            'strings_found': [],
            'uid_locations': [],
            'hex_preview': '',
        }
        
        # 检查是否为文本
        try:
            text = data.decode('utf-8')
            result['is_text'] = True
            result['text'] = text
            
            # 检查是否为 JSON
            try:
                json_data = json.loads(text)
                result['is_json'] = True
                result['json'] = json_data
            except:
                pass
                
        except:
            pass
        
        # 搜索 UID 字符串
        trad_uid = AUTHOR['traditional_uid'].encode()
        ess_uid = AUTHOR['essence_uid'].encode()
        
        # Protobuf 中数字字段会以 varint 形式存储
        # 搜索字符串形式的 UID
        uid_positions = []
        
        for uid_bytes, uid_type in [
            (trad_uid, 'traditional'),
            (ess_uid, 'essence'),
        ]:
            idx = 0
            while True:
                pos = data.find(uid_bytes, idx)
                if pos == -1:
                    break
                uid_positions.append({
                    'position': pos,
                    'uid_type': uid_type,
                    'uid': uid_bytes.decode(),
                    'context': data[max(0, pos-5):pos+len(uid_bytes)+5].hex(),
                })
                idx = pos + 1
        
        result['uid_locations'] = uid_positions
        
        # 搜索所有可读字符串
        strings = []
        current_str = b''
        for b in data:
            if 32 <= b <= 126:
                current_str += bytes([b])
            else:
                if len(current_str) >= 4:
                    strings.append(current_str.decode('ascii', errors='ignore'))
                current_str = b''
        if len(current_str) >= 4:
            strings.append(current_str.decode('ascii', errors='ignore'))
        
        result['strings_found'] = strings[:20]  # 最多20个
        
        # 十六进制预览
        result['hex_preview'] = data[:64].hex(' ')
        
        # 判断是否为 Protobuf（检查 varint 编码特征）
        result['is_protobuf'] = self._check_protobuf(data)
        
        return result
    
    def _check_protobuf(self, data: bytes) -> bool:
        """检查是否为 Protobuf 格式"""
        
        # Protobuf 的特征:
        # 1. 以 varint 开头（常见字段编号）
        # 2. 长度分隔的字符串
        # 3. 二进制数据
        
        if len(data) < 4:
            return False
        
        # 检查前几个字节是否是有效的 varint
        first_byte = data[0]
        field_number = first_byte >> 3
        wire_type = first_byte & 0x07
        
        # 常见的 wire type: 0=varint, 2=长度分隔
        if wire_type in [0, 2]:
            return True
        
        return False
    
    def find_replacement_cut_point(self, data: bytes) -> Dict[str, Any]:
        """找到替换切口"""
        
        analysis = self.analyze(data)
        
        cut_points = {
            'uid_cut_points': [],
            'recommendation': '',
        }
        
        # 检查是否找到传统 UID
        trad_locs = [
            loc for loc in analysis['uid_locations'] 
            if loc['uid_type'] == 'traditional'
        ]
        
        if trad_locs:
            for loc in trad_locs:
                cut_points['uid_cut_points'].append({
                    'position': loc['position'],
                    'uid': loc['uid'],
                    'replacement': AUTHOR['essence_uid'],
                    'method': 'direct_string_replace',
                    'context_hex': loc['context'],
                })
            
            cut_points['recommendation'] = (
                f'在位置 {trad_locs[0]["position"]} 处找到传统 UID，'
                f'可直接替换为本源 UID'
            )
        else:
            # 如果找不到字符串形式的 UID，可能是数字形式存储
            # 需要通过 Protobuf 字段解析
            cut_points['recommendation'] = (
                '字符串形式的 UID 未找到，可能是数字 varint 存储，'
                '需要更深入的 Protobuf 解析'
            )
        
        return cut_points


class AHAHybridInjector:
    """AHA 混合注入器 — 替换认证凭证中的 UID"""
    
    def __init__(self):
        self.engine = AHAEncryptionEngine()
        self.analyzer = AHAParamsAnalyzer()
        self.modifications = []
        
    def run(self) -> Dict[str, Any]:
        """执行 AHA 替换切口"""
        
        print(self._banner())
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'steps': [],
            'success': False,
        }
        
        # Phase 1: 初始化加密引擎
        if not self.engine.initialize():
            result['steps'].append({'phase': 'init', 'status': 'failed'})
            return result
        
        result['steps'].append({'phase': 'init', 'status': 'success'})
        
        # Phase 2: 读取并解密 AHA 数据
        storage_data = self._read_storage()
        if not storage_data:
            result['steps'].append({'phase': 'read', 'status': 'failed'})
            return result
        
        result['steps'].append({'phase': 'read', 'status': 'success'})
        
        # Phase 3: 分析 AHA 结构
        analysis_results = {}
        
        for key, encrypted_b64 in storage_data.get('auth_keys', {}).items():
            print(f'\n  分析认证键: {key}')
            
            # 解密
            decrypted = self.engine.decrypt_aha(encrypted_b64)
            
            if decrypted:
                # 分析结构
                analysis = self.analyzer.analyze(decrypted)
                analysis_results[key] = analysis
                
                print(f'    大小: {analysis["size"]} bytes')
                print(f'    文本: {analysis["is_text"]}')
                print(f'    JSON: {analysis["is_json"]}')
                print(f'    Protobuf: {analysis["is_protobuf"]}')
                print(f'    UID 位置: {len(analysis["uid_locations"])}')
                
                # 如果有 UID，找到切口
                cut_points = self.analyzer.find_replacement_cut_point(decrypted)
                print(f'    切口建议: {cut_points["recommendation"]}')
        
        # Phase 4: 执行替换
        replacements = self._execute_replacements(storage_data, analysis_results)
        result['replacements'] = replacements
        
        # Phase 5: 验证结果
        result['success'] = len(replacements.get('modified_keys', [])) > 0
        
        self._print_summary(result)
        return result
    
    def _read_storage(self) -> Optional[Dict]:
        """读取 storage.json 中的认证数据"""
        
        try:
            with open(STORAGE, 'r', encoding='utf-8') as f:
                storage = json.load(f)
            
            # 提取认证键
            auth_keys = {}
            for key, value in storage.items():
                if 'iCubeAuthInfo' in key:
                    auth_keys[key] = value
            
            return {
                'storage': storage,
                'auth_keys': auth_keys,
                'total_keys': len(auth_keys),
            }
            
        except Exception as e:
            print(f'  ❌ 读取 storage.json 失败: {e}')
            return None
    
    def _execute_replacements(
        self, 
        storage_data: Dict,
        analysis_results: Dict
    ) -> Dict[str, Any]:
        """执行替换"""
        
        print('\n' + '=' * 60)
        print('  Phase 4: 执行替换切口')
        print('=' * 60)
        
        replacements = {
            'modified_keys': [],
            'failed_keys': [],
        }
        
        storage = storage_data['storage']
        
        for key, encrypted_b64 in storage_data['auth_keys'].items():
            print(f'\n  处理: {key}')
            
            try:
                # 解密
                decrypted = self.engine.decrypt_aha(encrypted_b64)
                
                if not decrypted:
                    print(f'    ❌ 解密失败')
                    replacements['failed_keys'].append(key)
                    continue
                
                # 分析结构
                analysis = analysis_results.get(key, {})
                
                # 查找传统 UID
                trad_bytes = AUTHOR['traditional_uid'].encode()
                uid_pos = decrypted.find(trad_bytes)
                
                if uid_pos == -1:
                    # 尝试查找数字形式
                    # 传统UID作为varint编码
                    trad_uid_int = int(AUTHOR['traditional_uid'])
                    uid_pos = self._find_varint(decrypted, trad_uid_int)
                    
                    if uid_pos == -1:
                        print(f'    ⚠️ 未找到传统 UID，跳过')
                        # 即使找不到UID，也可以尝试创建新的本源键
                        continue
                
                # 替换 UID
                new_data = bytearray(decrypted)
                new_bytes = AUTHOR['essence_uid'].encode()
                
                if len(new_bytes) == len(trad_bytes):
                    # 直接替换（长度相同）
                    for i in range(len(trad_bytes)):
                        new_data[uid_pos + i] = new_bytes[i]
                    
                    print(f'    ✅ UID 替换成功 (位置 {uid_pos})')
                    print(f'       {AUTHOR["traditional_uid"]} → {AUTHOR["essence_uid"]}')
                    
                else:
                    # 长度不同，需要重新构造
                    # 在 UID 位置前后保留原数据，中间插入新 UID
                    prefix = decrypted[:uid_pos]
                    suffix = decrypted[uid_pos + len(trad_bytes):]
                    new_data = prefix + new_bytes + suffix
                    
                    print(f'    ✅ UID 替换成功 (长度调整)')
                    print(f'       原长度: {len(decrypted)} → 新长度: {len(new_data)}')
                
                # 重新加密
                new_encrypted = self.engine.encrypt_aha(bytes(new_data))
                
                if new_encrypted:
                    # 更新 storage
                    storage[key] = new_encrypted
                    replacements['modified_keys'].append(key)
                    self.modifications.append(key)
                    print(f'    ✅ 重新加密成功')
                    
            except Exception as e:
                print(f'    ❌ 处理失败: {e}')
                replacements['failed_keys'].append(key)
        
        # 保存修改
        if replacements['modified_keys']:
            with open(STORAGE, 'w', encoding='utf-8') as f:
                json.dump(storage, f, ensure_ascii=False, indent=2)
            
            print(f'\n  💾 storage.json 已更新')
            print(f'     修改键数: {len(replacements["modified_keys"])}')
        
        return replacements
    
    def _find_varint(self, data: bytes, value: int) -> int:
        """在二进制数据中查找 varint 编码的整数"""
        
        # 将整数编码为 varint
        varint_bytes = []
        temp = value
        while temp > 0:
            byte = temp & 0x7F
            temp >>= 7
            if temp:
                byte |= 0x80
            varint_bytes.append(byte)
        varint_bytes.reverse()
        varint_encoded = bytes(varint_bytes)
        
        # 查找
        return data.find(varint_encoded)
    
    def _print_summary(self, result: Dict):
        """打印摘要"""
        
        print('\n' + '=' * 60)
        print('  AHA 替换切口引擎 — 执行报告')
        print('=' * 60)
        
        print(f'\n  步骤:')
        for step in result['steps']:
            status = '✅' if step['status'] == 'success' else '❌'
            print(f'    {status} {step["phase"]}')
        
        if result.get('replacements'):
            print(f'\n  替换结果:')
            modified = result['replacements'].get('modified_keys', [])
            failed = result['replacements'].get('failed_keys', [])
            
            for key in modified:
                print(f'    ✅ {key}')
            for key in failed:
                print(f'    ❌ {key}')
        
        if result['success']:
            print(f'\n  🎯 替换切口已建立!')
            print(f'     本源 UID: {AUTHOR["essence_uid"]}')
            print(f'     传统 UID: {AUTHOR["traditional_uid"]}')
        else:
            print(f'\n  ⚠️ 部分替换可能失败')
            print(f'     建议: 重启 Trae CN 后查看效果')
    
    def _banner(self) -> str:
        return """
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║   BSD × Trae CN — AHA 加密替换切口引擎 V1.0                                    ║
║                                                                                  ║
║   目标: 深入 AHA 加密层，建立本源替换切口                                       ║
║   原理: 解密 → 分析 → 替换 UID → 重新加密                                      ║
║                                                                                  ║
║   ┌─────────────────────────────────────────────────────────────────────────┐   ║
║   │  Phase 1: 初始化 AES 密钥 (DPAPI)                                    │   ║
║   │  Phase 2: 读取并解密 AHA 数据                                         │   ║
║   │  Phase 3: 分析 Protobuf 结构                                          │   ║
║   │  Phase 4: 定位 UID 切口并替换                                         │   ║
║   │  Phase 5: 重新加密并注入                                               │   ║
║   └─────────────────────────────────────────────────────────────────────────┘   ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
        """


def main():
    injector = AHAHybridInjector()
    result = injector.run()
    
    print(f'\n{"="*60}')
    print(f'  最终状态: {"成功" if result["success"] else "部分成功"}')
    print(f'  修改的认证键: {len(result.get("replacements", {}).get("modified_keys", []))}')


if __name__ == '__main__':
    main()