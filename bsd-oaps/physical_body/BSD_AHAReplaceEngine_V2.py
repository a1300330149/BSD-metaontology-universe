#!/usr/bin/env python3
"""
BSD × Trae CN — AHA 加密替换切口引擎 V2
========================================

核心突破:
  1. 使用已知的 AES-256 密钥 (来自之前成功的 DPAPI 解密)
  2. 解密 AHA 认证数据
  3. 分析 Protobuf 结构，找到 UID 位置
  4. 替换传统 UID → 本源 UID
  5. 重新加密并注入 storage.json

已知 AES 密钥:
  71079e1533eae26094450a564b7641e28d3292d36636807016c552ad0af26bb0

版本: V2.0 · 2026-08-05
"""

import os, sys, json, hashlib, base64, random
from datetime import datetime
from typing import Dict, Any, Optional

# Crypto
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
        print('⚠️ 缺少 pycryptodome，正在安装...')
        os.system(f'{sys.executable} -m pip install pycryptodome -q')
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import unpad, pad
        HAS_CRYPTO = True

# 路径
TRAE_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
LOCAL_STATE = os.path.join(TRAE_DATA, 'Local State')
STORAGE = os.path.join(TRAE_DATA, 'User', 'globalStorage', 'storage.json')
BACKUP_DIR = os.path.join(TRAE_DATA, 'User', 'globalStorage', 'backup')

# 作者信息
AUTHOR = {
    'traditional_uid': '3753060170739075',
    'essence_uid': 'a5b7a8623fdea6b8',
    'device_id': '136411536168449',
}

# 已知 AES-256 密钥 (来自之前成功的 DPAPI 解密)
KNOWN_AES_KEY = bytes.fromhex('71079e1533eae26094450a564b7641e28d3292d36636807016c552ad0af26bb0')


class AHAReplaceEngine:
    """AHA 加密替换切口引擎"""
    
    def __init__(self):
        self.aes_key = KNOWN_AES_KEY
        self.analysis_results = {}
        self.replacements = []
        
    def run(self) -> Dict[str, Any]:
        """执行替换切口"""
        
        print(self._banner())
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'steps': [],
            'success': False,
        }
        
        # Phase 1: 读取并解析 storage.json
        storage = self._read_storage()
        if not storage:
            return result
        result['steps'].append({'phase': 'read_storage', 'status': 'success'})
        
        # Phase 2: 遍历认证键，解密分析
        auth_keys = [
            k for k in storage 
            if 'iCubeAuthInfo' in k
        ]
        
        print(f'\n  找到 {len(auth_keys)} 个认证键')
        
        for key in auth_keys:
            print(f'\n  ── 处理: {key} ──')
            encrypted_b64 = storage[key]
            
            # 解密
            decrypted = self._decrypt_aha(encrypted_b64)
            
            if decrypted:
                # 分析
                analysis = self._analyze_data(decrypted, key)
                self.analysis_results[key] = analysis
                
                # 尝试替换
                replacement = self._try_replace(
                    key, encrypted_b64, decrypted, storage
                )
                
                if replacement['modified']:
                    result['steps'].append({
                        'phase': f'replace_{key}',
                        'status': 'success',
                        'detail': replacement,
                    })
                else:
                    result['steps'].append({
                        'phase': f'replace_{key}',
                        'status': 'skipped',
                        'detail': replacement.get('reason', ''),
                    })
            else:
                result['steps'].append({
                    'phase': f'decrypt_{key}',
                    'status': 'failed',
                })
        
        # Phase 3: 保存修改
        if self.replacements:
            self._save_storage(storage)
            result['success'] = True
            result['replacements_count'] = len(self.replacements)
        
        # Phase 4: 打印摘要
        self._print_summary(result)
        
        return result
    
    def _read_storage(self) -> Optional[Dict]:
        """读取 storage.json"""
        
        try:
            with open(STORAGE, 'r', encoding='utf-8') as f:
                storage = json.load(f)
            print(f'  ✅ storage.json 已读取')
            return storage
        except Exception as e:
            print(f'  ❌ 读取失败: {e}')
            return None
    
    def _decrypt_aha(self, encrypted_b64: str) -> Optional[bytes]:
        """解密 AHA 数据"""
        
        try:
            # Base64 解码
            raw = base64.b64decode(encrypted_b64)
            
            # AHA 格式:
            # 前 6 字节: 固定前缀 746305100000
            # 接下来: 可能是加密头部
            # 然后: IV + 密文
            
            prefix = raw[:6]
            expected_prefix = bytes.fromhex('746305100000')
            
            if prefix == expected_prefix:
                print(f'    AHA 前缀匹配 ✅')
                
                # 尝试多种 IV 位置
                for iv_offset in [8, 12, 16, 24]:
                    if len(raw) > iv_offset + 32:
                        iv = raw[iv_offset:iv_offset + 16]
                        ciphertext = raw[iv_offset + 16:]
                        
                        if len(ciphertext) >= 16 and len(ciphertext) % 16 == 0:
                            try:
                                cipher = AES.new(self.aes_key, AES.MODE_CBC, iv=iv)
                                decrypted = cipher.decrypt(ciphertext)
                                plaintext = unpad(decrypted, AES.block_size)
                                
                                # 检查可读性
                                try:
                                    text = plaintext.decode('utf-8')
                                    ratio = sum(1 for c in text if c.isprintable() or c in '\n\r\t') / max(len(text), 1)
                                    
                                    if ratio > 0.5:
                                        print(f'    ✅ 解密成功 (iv@{iv_offset}, 可读率 {ratio:.0%})')
                                        print(f'    明文预览: {text[:100]}')
                                        return plaintext
                                except:
                                    pass
                                    
                            except:
                                pass
                
                # 备选: 直接用数据前16字节作IV
                if len(raw) > 32:
                    iv = raw[:16]
                    ciphertext = raw[16:]
                    if len(ciphertext) % 16 == 0:
                        try:
                            cipher = AES.new(self.aes_key, AES.MODE_CBC, iv=iv)
                            decrypted = cipher.decrypt(ciphertext)
                            plaintext = unpad(decrypted, AES.block_size)
                            print(f'    ✅ 备选解密成功')
                            return plaintext
                        except:
                            pass
            
            return None
            
        except Exception as e:
            print(f'    ❌ 解密异常: {e}')
            return None
    
    def _analyze_data(self, data: bytes, key: str) -> Dict[str, Any]:
        """分析解密数据"""
        
        analysis = {
            'size': len(data),
            'uid_positions': [],
            'strings': [],
            'hex_preview': data[:64].hex(' '),
        }
        
        # 搜索 UID 字符串
        for uid, uid_type in [
            (AUTHOR['traditional_uid'], 'traditional'),
            (AUTHOR['essence_uid'], 'essence'),
        ]:
            uid_bytes = uid.encode()
            pos = data.find(uid_bytes)
            if pos != -1:
                analysis['uid_positions'].append({
                    'position': pos,
                    'uid': uid,
                    'uid_type': uid_type,
                })
                print(f'    🔍 找到 {uid_type} UID: 位置 {pos}')
                print(f'       上下文: {data[max(0, pos-3):pos+len(uid_bytes)+3].hex()}')
        
        # 搜索可读字符串
        current = b''
        for b in data:
            if 32 <= b <= 126:
                current += bytes([b])
            else:
                if len(current) >= 4:
                    analysis['strings'].append(current.decode('ascii', errors='ignore'))
                current = b''
        if len(current) >= 4:
            analysis['strings'].append(current.decode('ascii', errors='ignore'))
        
        if analysis['strings']:
            print(f'    🔤 可读字符串 ({len(analysis["strings"])}):')
            for s in analysis['strings'][:10]:
                print(f'       "{s[:50]}"')
        
        return analysis
    
    def _try_replace(
        self, 
        key: str, 
        encrypted_b64: str,
        decrypted: bytes,
        storage: Dict
    ) -> Dict[str, Any]:
        """尝试替换 UID"""
        
        result = {'modified': False, 'reason': ''}
        
        # 查找传统 UID
        trad_bytes = AUTHOR['traditional_uid'].encode()
        uid_pos = decrypted.find(trad_bytes)
        
        if uid_pos == -1:
            result['reason'] = '未找到传统 UID (字符串形式)'
            
            # 尝试 Protobuf varint 格式
            uid_pos = self._find_uid_varint(decrypted, AUTHOR['traditional_uid'])
            
            if uid_pos == -1:
                result['reason'] += ' + varint 也未找到'
                print(f'    ⚠️ {result["reason"]}')
                return result
        
        print(f'    🎯 找到替换切口: 位置 {uid_pos}')
        
        # 替换 UID
        new_data = bytearray(decrypted)
        new_bytes = AUTHOR['essence_uid'].encode()
        
        if len(new_bytes) == len(trad_bytes):
            # 等长替换
            for i in range(len(trad_bytes)):
                new_data[uid_pos + i] = new_bytes[i]
            print(f'    ✅ 等长替换: {AUTHOR["traditional_uid"]} → {AUTHOR["essence_uid"]}')
        else:
            # 不等长，需要重新拼接
            prefix = decrypted[:uid_pos]
            suffix = decrypted[uid_pos + len(trad_bytes):]
            new_data = prefix + new_bytes + suffix
            print(f'    ✅ 变长替换: 新长度 {len(new_data)}')
        
        # 重新加密
        new_encrypted = self._encrypt_aha(bytes(new_data))
        
        if new_encrypted:
            # 更新 storage
            storage[key] = new_encrypted
            self.replacements.append({
                'key': key,
                'uid_pos': uid_pos,
                'old_uid': AUTHOR['traditional_uid'],
                'new_uid': AUTHOR['essence_uid'],
            })
            
            result['modified'] = True
            print(f'    🔄 重新加密成功')
            print(f'    ✅ storage.json 中的 {key} 已更新')
        else:
            result['reason'] = '重新加密失败'
        
        return result
    
    def _find_uid_varint(self, data: bytes, uid_str: str) -> int:
        """在 Protobuf 中查找 varint 编码的 UID"""
        
        # 将 UID 字符串转为整数
        try:
            uid_int = int(uid_str)
        except:
            return -1
        
        # 编码为 varint
        varint_bytes = []
        temp = uid_int
        while temp > 0:
            byte = temp & 0x7F
            temp >>= 7
            if temp:
                byte |= 0x80
            varint_bytes.append(byte)
        varint_bytes.reverse()
        
        varint_encoded = bytes(varint_bytes)
        pos = data.find(varint_encoded)
        
        if pos != -1:
            print(f'    📍 varint 编码的 UID 找到: 位置 {pos}, 长度 {len(varint_bytes)}')
        
        return pos
    
    def _encrypt_aha(self, plaintext: bytes) -> Optional[str]:
        """加密数据为 AHA 格式"""
        
        try:
            # 随机 IV
            iv = bytes([random.randint(0, 255) for _ in range(16)])
            
            # AES-256-CBC 加密
            cipher = AES.new(self.aes_key, AES.MODE_CBC, iv=iv)
            encrypted = cipher.encrypt(pad(plaintext, AES.block_size))
            
            # 构造 AHA 格式 (简化版)
            # 前缀 + IV + 密文
            prefix = bytes.fromhex('746305100000')
            result = prefix + iv + encrypted
            
            # Base64 编码
            return base64.b64encode(result).decode('utf-8')
            
        except Exception as e:
            print(f'    ❌ 加密失败: {e}')
            return None
    
    def _save_storage(self, storage: Dict):
        """保存 storage.json"""
        
        os.makedirs(BACKUP_DIR, exist_ok=True)
        
        # 备份
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = os.path.join(BACKUP_DIR, f'storage_before_replace_{timestamp}.json')
        
        try:
            with open(STORAGE, 'r', encoding='utf-8') as f:
                original = json.load(f)
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(original, f, ensure_ascii=False, indent=2)
            print(f'\n  💾 备份已创建: {backup_path}')
        except:
            pass
        
        # 保存修改
        with open(STORAGE, 'w', encoding='utf-8') as f:
            json.dump(storage, f, ensure_ascii=False, indent=2)
        
        print(f'  ✅ storage.json 已更新 ({len(self.replacements)} 处修改)')
    
    def _print_summary(self, result: Dict):
        """打印摘要"""
        
        print('\n' + '=' * 60)
        print('  AHA 加密替换切口引擎 — 执行报告')
        print('=' * 60)
        
        print(f'\n  步骤:')
        for step in result['steps']:
            status = '✅' if step['status'] in ['success', 'skipped'] else '❌'
            print(f'    {status} {step["phase"]}')
        
        if self.replacements:
            print(f'\n  替换详情:')
            for r in self.replacements:
                print(f'    🔑 {r["key"]}')
                print(f'       位置: {r["uid_pos"]}')
                print(f'       UID: {r["old_uid"]} → {r["new_uid"]}')
        
        if result['success']:
            print(f'\n  🎯 替换切口已建立!')
            print(f'     Trae CN 下次加载时将读取本源 UID')
            print(f'     建议: 重启 Trae CN')
        else:
            print(f'\n  ⚠️ 未找到可替换的 UID')
            print(f'     可能原因:')
            print(f'     1. UID 不以字符串形式存储')
            print(f'     2. 需要更深入的 Protobuf 解析')
            print(f'     3. 数据被进一步封装')
    
    def _banner(self) -> str:
        return """
╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║   BSD × Trae CN — AHA 加密替换切口引擎 V2.0                                    ║
║                                                                                  ║
║   核心突破:                                                                      ║
║   • 使用已知 AES-256 密钥 (DPAPI 已验证)                                        ║
║   • 解密 AHA 认证数据                                                           ║
║   • 定位 UID 存储位置                                                           ║
║   • 替换传统 UID → 本源 UID                                                     ║
║                                                                                  ║
║   流程:                                                                          ║
║   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      ║
║   │ 读取 storage │→│ 解密 AHA     │→│ 分析 UID 位置│→│ 替换并加密   │      ║
║   └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘      ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
        """


def main():
    engine = AHAReplaceEngine()
    result = engine.run()
    
    print(f'\n{"="*60}')
    if result['success']:
        print('  ✅ 替换切口建立成功!')
        print('  请重启 Trae CN 查看效果')
    else:
        print('  ⚠️ 替换切口未找到')
        print('  可能需要更深入的 Protobuf 解析')


if __name__ == '__main__':
    main()